from abc import ABC, abstractmethod

import torch
import math

from lstm_motion_model import utils


class SequenceTransform(ABC):
    """Base class for transformations from one set of sequences to another"""
    def __init__(self):
        self._before_length = None
        self._after_length = None

    @abstractmethod
    def __call__(self, sequence, start=None, stop=None):
        pass

    @property
    def before_length(self):
        """Number of additional frames required before the start of the input
        sequence in order to achieve desired output length"""
        return self._before_length

    @property
    def after_length(self):
        """Number of additional frames required after the end of the
        input sequence in order to achieve desired output length"""
        return self._after_length


class PositionToDisplacement(SequenceTransform):
    def __init__(self, offset=0, extrapolate_nans=False):
        super().__init__()
        self._before_length = 1
        self._after_length = 0
        self._offset = offset
        self._extrapolate_nans = extrapolate_nans

    @property
    def before_length(self):
        return max(self._before_length - self._offset, 0)

    @property
    def after_length(self):
        return max(self._after_length + self._offset, 0)

    def __call__(self, sequence, start=None, stop=None):
        pos_seq = sequence['position']
        start = 1 if start is None else start + self._offset
        stop = len(pos_seq) if start is None else stop + self._offset
        # Check sequence dimensions
        assert start >= 1
        assert stop <= len(pos_seq)
        before_start = start - 1
        # Make a copy in which to perform interpolation
        position = pos_seq[before_start:stop].clone()
        if self._extrapolate_nans:
            # Fill in missing ends of position sequences
            utils.extrapolate_nans_in_seq(position)
        # Compute displacements between consecutive positions
        displacement = position[1:] - position[:-1]
        # Trim start off position to match length
        position = position[1:]
        # Pack outputs as dict
        return {'position': position,
                'displacement': displacement}


class PositionToEgoDisplacement(PositionToDisplacement):
    def __init__(self, offset=0, extrapolate_nans=False):
        super().__init__(offset, extrapolate_nans)
        self._before_length = 2
        self._after_length = 0


    def __call__(self, sequence, start=None, stop=None):
        position = sequence['position']
        if start is None:
            start = 2
        if stop is None:
            stop = len(position)
        assert start >= 2
        assert stop <= len(position)
        # Get global displacement first starting one frame early
        sequence = super().__call__(sequence, start - 1, stop)
        #sequence = super().__call__(sequence, start , stop)
        # Unpack sequence dict
        position = sequence['position']
        displacement = sequence['displacement']
        # Compute the angle of orientation at each frame based on displacement
        orientation = torch.atan2(displacement[:-1, ..., 1],
                                  displacement[:-1, ..., 0])
        # Trim displacement and position to match orientation length
        position = position[1:]
        displacement = displacement[1:]
        # Rotate each displacement to be relative to the previous heading
        ego_displacement = utils.rotate_2d(displacement, -orientation)

        return {'position': position,
                'orientation': orientation,
                'ego_displacement': ego_displacement}


class PositionToAPG(SequenceTransform):
    def __init__(self, angular_segments, max_range):
        super().__init__()
        self._before_length = 1
        self._after_length = 0
        self._angular_segments = angular_segments
        self._max_range = max_range

    def __call__(self, sequence, start=None, stop=None):
        position = sequence['position']
        device = position.device
        start = 1 if start is None else start
        stop = len(position) if stop is None else stop
        assert start >= 1
        assert stop <= len(position)
        position = position[start - 1:stop]

        displacement = position[1:] - position[:-1]
        heading_angle = torch.atan2(displacement[..., 1], displacement[..., 0])
        position = position[1:]

        seq_len, num_ppl, dims = position.shape
        assert dims == 2

        # frames, this person, other person, dims
        relative_pos = (position.view(seq_len, 1, num_ppl, dims)
                        - position.view(seq_len, num_ppl, 1, dims))
        # Convert to polar
        r = relative_pos.norm(dim=-1)
        phi = torch.atan2(relative_pos[..., 1], relative_pos[..., 0])

        # Egocentric angular offset
        phi = phi - heading_angle.view(seq_len, num_ppl, 1)

        # Discretise angles
        scale = self._angular_segments / (2 * math.pi)
        angular_index = torch.floor(phi * scale).to(dtype=torch.long)
        angular_index = torch.fmod(angular_index + self._angular_segments,
                                   self._angular_segments)

        assert angular_index.shape == (seq_len, num_ppl, num_ppl)
        assert r.shape == (seq_len, num_ppl, num_ppl)

        segments = torch.arange(self._angular_segments, device=device)
        segment_mask = (
                angular_index.view(seq_len, num_ppl, num_ppl, 1)
                == segments.view(1, 1, 1, self._angular_segments))
        self_mask = torch.eye(num_ppl, device=device, dtype=torch.bool).view(
            1, num_ppl, num_ppl, 1)
        # Ignore self
        segment_mask &= ~self_mask
        r = r.view(seq_len, num_ppl, num_ppl, 1).repeat(
            1, 1, 1, self._angular_segments)
        r[~segment_mask] = self._max_range

        r: torch.Tensor
        apg = r.min(dim=-2, keepdim=False)[0]

        return {'apg': apg, 'heading': heading_angle}


class PositionToLocalGrid(SequenceTransform):
    def __init__(self, global_radius, global_resolution,
                 local_radius, local_resolution):
        super().__init__()
        self._before_length = 0
        self._after_length = 0
        self._global_radius = global_radius
        self._global_resolution = global_resolution
        self._local_radius = local_radius
        self._local_resolution = local_resolution

    def __call__(self, sequence, start=None, stop=None):
        position = sequence['position']
        position = position[start:stop]
        full_seq_len, num_ppl, dims = position.shape
        seq_len = stop - start
        utils.extrapolate_nans_in_seq(position)
        global_grids = utils.point_to_grid(position,
                                           self._global_radius * 2,
                                           self._global_resolution)
        global_grids = (global_grids
                        .sum(dim=1, keepdim=True)
                        .repeat(1, num_ppl, 1, 1)
                        - global_grids)
        local_grids = utils.grid_transform(
            global_grids.view(-1, 1, self._global_resolution,
                              self._global_resolution),
            -position.view(-1, dims),
            self._global_radius, self._local_radius,
            self._local_resolution)

        if torch.isnan(local_grids[:]).any():
            raise Exception('nans found')
        return {'local_grid': local_grids.view(
            (seq_len, num_ppl,) + (self._local_resolution,) * 2)}


class PositionToFutureDisplacements(SequenceTransform):
    def __init__(self, temporal_offsets, egocentric):
        super().__init__()
        self._before_length = 0
        self._after_length = max(temporal_offsets)
        self._temporal_offsets = temporal_offsets
        self._egocentric = egocentric

    def __call__(self, sequence, start=None, stop=None):
        position = sequence['position']
        full_len, num_people, dims = position.shape
        # If no stop is given use maximum length
        if stop is None:
            stop = full_len - self._after_length
        selected_len = stop - start
        assert selected_len > 0
        assert start >= 0
        assert stop + self._after_length <= full_len

        from_frames = [i for o in self._temporal_offsets
                       for i in range(start, stop)]
        to_frames = [i + o for o in self._temporal_offsets
                     for i in range(start, stop)]
        target = {}
        displacements = position[to_frames] - position[from_frames]
        if self._egocentric:
            assert start >= 1
            prev_frames = [i-1 for o in self._temporal_offsets for i in range(start, stop)]
            heading_vector = position[from_frames] - position[prev_frames]
            theta = torch.atan2(heading_vector[..., 1], heading_vector[..., 0])
            displacements = utils.rotate_2d(displacements, -theta)

        displacements = torch.stack(
            torch.chunk(displacements, len(self._temporal_offsets), dim=0),
            dim=2)
        key = 'future_ego_displacements' if self._egocentric else \
            'future_displacements'
        target[key] = displacements
        return target


class PositionToDisplacementTrajectory(SequenceTransform):
    def __init__(self, trajectory_length):
        super().__init__()
        self._before_length = 0
        self._trajectory_length = trajectory_length
        self._after_length = self._trajectory_length
        self._pos_to_disp = PositionToEgoDisplacement(offset=1)

    def __call__(self, sequence, start=None, stop=None):
        position = sequence['position']
        device = position.device
        full_len, num_people, dims = position.shape
        # If no stop is given use maximum length
        if stop is None:
            stop = full_len - self._after_length
        selected_len = stop - start
        assert selected_len > 0
        assert start >= 0
        assert stop + self._after_length <= full_len

        # Get ego displacements
        displacements = self._pos_to_disp(
            sequence, start, stop + self._trajectory_length)

        # Create indexes to form overlapping trajectories
        frame_index = torch.arange(
            selected_len, device=device).view(1, -1)
        trajectory_index = torch.arange(
            self._trajectory_length, device=device).view(-1, 1)
        index = (frame_index + trajectory_index).view(-1)

        key = 'displacement_trajectory'
        target = {}
        target[key] = torch.stack(
            displacements['ego_displacement'].index_select(0, index)
                .chunk(self._trajectory_length), dim=2)
        return target

# class AddNoise(SequenceTransform):
#     def __init__(self, temporal_offsets, egocentric):
#         super().__init__()
#         self._before_length = 0
#         self._after_length = 0
#         self._cov
#         self._temporal_offsets = temporal_offsets
#         self._egocentric = egocentric
#
#     def __call__(self, sequence, start=None, stop=None):
#         position = sequence['position']
#         full_len, num_people, dims = position.shape
#         # If no stop is given use maximum length
#         if stop is None:
#             stop = full_len - self._after_length
#         selected_len = stop - start
#         assert selected_len > 0
#         assert start >= 0
#         assert stop + self._after_length <= full_len
#
#         from_frames = [i for o in self._temporal_offsets
#                        for i in range(start, stop)]
#         to_frames = [i + o for o in self._temporal_offsets
#                      for i in range(start, stop)]
#         target = {}
#         displacements = position[to_frames] - position[from_frames]
#         if self._egocentric:
#             assert start >= 1
#             prev_frames = [i-1 for o in self._temporal_offsets for i in range(start, stop)]
#             heading_vector = position[from_frames] - position[prev_frames]
#             theta = torch.atan2(heading_vector[..., 1], heading_vector[..., 0])
#             displacements = utils.rotate_2d(displacements, -theta)
#
#         displacements = torch.stack(
#             torch.chunk(displacements, len(self._temporal_offsets), dim=0),
#             dim=2)
#         key = 'future_ego_displacements' if self._egocentric else \
#             'future_displacements'
#         target[key] = displacements
#         return target
