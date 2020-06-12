from __future__ import print_function, division
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pack_sequence
from lstm_motion_model.pedestrian_sequence import DenseCrowdSequence
import numpy as np


class SocialDataset(Dataset):
    """Dataset comprised of multiple simultaneous human trajectories"""

    def __init__(self, csv_files, sequence_length=None, device=None,
                 transform=None):
        if isinstance(csv_files, str):
            csv_files = [csv_files]
        self._sequences = []
        self._transform = transform
        if device:
            self._device = device
        else:
            self._device = torch.device('cpu')

        # next_person_id = 0
        for file_idx, csv_file in enumerate(csv_files):
            # Load frames of trajectory data from csv and transpose so rows are
            # observations
            raw_data = np.genfromtxt(csv_file, delimiter=',').transpose()
            # Get frame ids from raw data and compute start and end frame
            frames = raw_data[:, 0].astype(int)
            start_frame = frames.min()
            end_frame = frames.max() + 1
            seq_length = (sequence_length if sequence_length
                          else end_frame - start_frame)
            # For each segment we compute the start and end frame and hence
            # number of frames
            for seq_start in range(start_frame, end_frame, seq_length):
                seq_end = seq_start + seq_length
                if seq_end > end_frame:
                    seq_end = end_frame
                num_frames = seq_end - seq_start
                # Compute a mask for the rows of raw_data that belong to this
                # segment
                in_segment = np.logical_and(
                    frames >= seq_start, frames < seq_end)
                # Collect all the unique person ids in this segment and assign
                # a segment idx to each
                person_ids = np.unique(raw_data[in_segment, 1]).astype(int)
                id_to_idx = {pid: idx for idx, pid in enumerate(person_ids)}
                # Create a tensor of zeros for this segment based on the no. of
                # frames, people and state size
                self._sequences.append(torch.full(
                    (num_frames, len(person_ids), 2), float('nan')))
                # For each row in the segment calculate the frame and person
                # indices
                # Copy the observation/state data to the correct section of the
                # tensor
                for row in raw_data[in_segment, :]:
                    frame_idx = row[0].astype(int) - seq_start
                    person_idx = id_to_idx[row[1].astype(int)]
                    self._sequences[-1][frame_idx, person_idx, 0] = row[2]
                    self._sequences[-1][frame_idx, person_idx, 1] = row[3]

    def __len__(self):
        return len(self._sequences)

    def __getitem__(self, item):
        if self._transform:
            return self._transform(self._sequences[item]).to(self._device)
        else:
            return self._sequences[item].to(self._device)


class CrowdSequenceDataset(Dataset):
    """Dataset comprised of multiple simultaneous human trajectories"""

    def __init__(self, file_paths, sequence_length=None, device=None,
                 transform=None):
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        self._sequences = []
        self._transform = transform
        if device:
            self._device = device
        else:
            self._device = torch.device('cpu')

        # Load all the datasets into memory
        self._crowd_datasets = [DenseCrowdSequence.load(path)
                               for path in file_paths]

        # Here we store sufficient information to access each subsequence
        # directly just in time
        self._sequence_indicies = []

        seq_len = sequence_length
        for dataset_idx, dataset in enumerate(self._crowd_datasets):
            if sequence_length is None:
                seq_len = len(dataset)
            for start_frame in range(dataset.start_frame, dataset.stop_frame,
                                     seq_len):
                # slice objects are passed when using the x[start:stop:step]
                # syntax. Here we prepare a slice for each subsequence
                seq_slice = slice(
                    start_frame,
                    min(start_frame + seq_len, dataset.stop_frame),
                    None)
                self._sequence_indicies.append((dataset_idx, seq_slice))

    def __len__(self):
        return len(self._sequence_indicies)

    def __getitem__(self, item):
        # Retrieve the data using our precomputed (idx, slice) pairs and create
        # a tensor on the correct device
        dataset_idx, seq_slice = self._sequence_indicies[item]
        sequence = torch.tensor(self._crowd_datasets[dataset_idx][seq_slice],
                                device=self._device, dtype=torch.float)
        # Apply data augmentation if configured
        if self._transform:
            sequence = self._transform(sequence)
        return sequence
