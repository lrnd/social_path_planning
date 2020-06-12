import logging
import warnings
from typing import Dict, Any, Union

import torch
from torch import nn
import torch.nn.functional as F

from lstm_motion_model import criterion, utils
from torch.distributions.multivariate_normal import MultivariateNormal

import matplotlib.pyplot as plt

from . import sequence_transforms as tf, output_targeters as ot


def create_mlp(dim_list, activation='leaky_relu', layer_norm=False,
               dropout=0.0):
    layers = []
    for dim_in, dim_out in zip(dim_list[:-1], dim_list[1:]):
        if len(layers) > 0 and dropout > 0.0:
            layers.append(nn.Dropout(p=dropout))
        layers.append(nn.Linear(dim_in, dim_out))
        if layer_norm:
            layers.append(nn.LayerNorm(dim_out))
        if activation == 'relu':
            layers.append(nn.ReLU())
        elif activation == 'leaky_relu':
            layers.append(nn.LeakyReLU())
    return nn.Sequential(*layers)


class PedestrianMotionModel(nn.Module):
    """Base class for pedestrian motion models"""

    def __init__(self, config):
        super().__init__()
        self._config = self.default_config()
        # Expose props before updating with passed in config
        # this avoids user provided configs shadowing and adding members
        self._expose_config_as_ro_props()
        self._config.update(config)
        self._step = 0
        self.tb_writer = None
        self.register_forward_hook(self._increment_step)
        self.register_forward_hook(self._process_output)

        self._input_tfs = []
        self._target_tfs = []
        self._output_targeter = ot.Direct()
        self._input_key = ''
        self._target_key = ''

        self.register_buffer('input_accum', torch.empty((0, 2)))
        self.register_buffer('target_accum', torch.empty((0, 2)))
        self.register_buffer('input_mean', torch.zeros(2))
        self.register_buffer('input_std', torch.zeros(2))
        self.register_buffer('target_mean', torch.zeros(2))
        self.register_buffer('target_std', torch.zeros(2))

    def _expose_config_as_ro_props(self):
        for k in self._config:
            setattr(self.__class__, '_' + k,
                    property(lambda o, k=k: o._config[k]))
            # Default arg k=k evaluates k at time of declaring lambda
            # rather than evaluating k from this functions scope later

    @staticmethod
    def _increment_step(module, input, output):
        module._step += 1

    @staticmethod
    def _process_output(module, input, output):
        out, hidden = output
        key = '_'.join((module._target_key, module._output_targeter.label))
        out[key] = module._output_targeter.compose_output(
            out[module._target_key])
        return out, hidden

    @staticmethod
    def _apply_transforms(tf_list, sequence, start, stop):
        output = {}
        for t in tf_list:
            output.update(t(sequence, start, stop))
        return output

    def prepare_input(self, position_sequence, start=None, stop=None):
        return self._apply_transforms(
            self._input_tfs, {'position': position_sequence}, start, stop)

    def prepare_target(self, position_sequence, start=None, stop=None):
        return self._apply_transforms(
            self._target_tfs, {'position': position_sequence}, start, stop)

    def compute_loss(self, model_output, target):
        output_key = '_'.join((self._target_key, self._output_targeter.label))
        return self._output_targeter.compute_loss(model_output[output_key],
                                                  target[self._target_key])

    def accumulate_normalisation_data(self, position_sequence,
                                      start=None, stop=None):
        # Prepare input and target
        input_data = self.prepare_input(position_sequence, start, stop)
        target_data = self.prepare_target(position_sequence, start, stop)

        # Accumulate input displacements
        self.input_accum = torch.cat((
            self.input_accum,
            input_data[self._input_key].view(
                -1, input_data[self._input_key].shape[-1])
        ))

        # Accumulate target displacements
        self.target_accum = torch.cat((
            self.target_accum,
            target_data[self._target_key].view(
                -1, target_data[self._target_key].shape[-1])
        ))
        return None

    def release_normalisation_data(self):
        self.input_accum = self.input_accum[0:0]
        self.target_accum = self.target_accum[0:0]
        return None

    def compute_normalisation_parameters(self):

        valid_inputs = torch.isfinite(self.input_accum).all(-1)
        self.input_mean = (self.input_accum[valid_inputs, :]
                                .mean(dim=0))
        self.input_std = (self.input_accum[valid_inputs, :]
                               - self.input_mean).std(dim=0)

        valid_targets = torch.isfinite(self.target_accum).all(-1)
        self.target_mean = (self.target_accum[valid_targets, :]
                                 .mean(dim=0))
        self.target_std = (self.target_accum[valid_targets, :]
                                - self.target_mean).std(dim=0)
        assert (self.input_mean.shape[-1] ==
                self.input_accum.shape[-1])
        assert (self.input_std.shape[-1] ==
                self.input_accum.shape[-1])
        assert (self.target_mean.shape[-1] ==
                self.target_accum.shape[-1])
        assert (self.target_std.shape[-1] ==
                self.target_accum.shape[-1])
        return self.get_normalisation_parameters()

    def set_normalisation_parameters(self, params):
        (self.input_mean, self.input_std,
         self.target_mean, self.target_std) = params
        return None

    def get_normalisation_parameters(self):
        return (self.input_mean,
                self.input_std,
                self.target_mean,
                self.target_std)

    def clear_normalisation_parameters(self):
        self.input_mean[:] = 0
        self.input_std[:] = 0
        self.target_mean[:] = 0
        self.target_std[:] = 0
        return None

    def normalise_input(self, model_input):
        model_input[self._input_key] = (model_input[self._input_key]
                                        - self.input_mean) / self.input_std

    def normalise_target(self, target):
        target[self._target_key] = (target[self._target_key]
                                    - self.target_mean) / self.target_std

    def unnormalise_target(self, target):
        target[self._target_key] = (target[self._target_key] *
                                    self.target_std + self.target_mean)

    def sample_output(self, model_output, stochastic=True):
        output_key = '_'.join((self._target_key, self._output_targeter.label))
        if stochastic:
            sample = self._output_targeter.sample(
                model_output[output_key])
        else:
            sample = self._output_targeter.expected(
                model_output[output_key])

        return {self._target_key: sample}

    def propagate_input(self, model_input, model_output):
        """Given input to, and output from, model at time t generate input for
        time t+t

        model_input should be a dict such as that returned by this models
        prepare input funciton

        model_output should be a dict like that output by forward combined
        with that output by sample output
        """
        next_input = {
            'displacement': model_output['displacement'],
            'position': model_input['position']
            + model_output['displacement']
        }
        return next_input

    @classmethod
    def default_config(cls) -> Dict[str, any]:
        config = {
            'input_size': 2,
        }
        return config

    @property
    def before_length(self):
        input_max = max([t.before_length for t in self._input_tfs])
        target_max = max([t.before_length for t in self._target_tfs])
        return max(input_max, target_max)

    @property
    def after_length(self):
        input_max = max([t.after_length for t in self._input_tfs])
        target_max = max([t.after_length for t in self._target_tfs])
        return max(input_max, target_max)


class ConstantVelocityModel(PedestrianMotionModel):

    def __init__(self, config):
        super().__init__(config)
        self._input_tfs.append(tf.PositionToDisplacement(extrapolate_nans=True))
        self._target_tfs.append(tf.PositionToDisplacement(offset=1))
        self._output_targeter = ot.Direct()
        self._input_key = 'displacement'
        self._target_key = 'displacement'

    def forward(self, model_input, hidden=None):
        return {self._target_key: model_input['displacement']}


class SocialForcesModel(PedestrianMotionModel):

    def __init__(self, config):
        super().__init__(config)
        self._input_tfs.append(tf.PositionToDisplacement(extrapolate_nans=True))
        self._target_tfs.append(tf.PositionToDisplacement(offset=1))
        self._output_targeter = ot.Direct()
        self._input_key = 'displacement'
        self._target_key = 'displacement'

    def forward(self, model_input, hidden=None):
        displacement = model_input['displacement']
        position = model_input['position']

        assert displacement.shape == position.shape
        original_shape = displacement.shape
        seq_len, num_people, dims = original_shape
        assert seq_len == 1

        HZ = 6.0
        DT = 1.0 / HZ

        n_steps = 10
        dt = DT / float(n_steps)

        #  constants
        A = 2e3  # N
        B = 0.08  # m
        k1 = 1.2e5  # kg/s^2 (roman k)
        k2 = 2.4e5  # kg/m/s (kappa)
        R = 0.6  # m
        tau = 0.5  # s
        m = 80  # kg

        # push dims: [I, J, 2]
        xi = position.clone().view(num_people, 1, 2)
        vi = displacement.clone().view(num_people, 1, 2) * HZ

        for _ in range(n_steps):

            v0 = vi
            xj = xi.view(1, num_people, 2)
            vj = vi.view(1, num_people, 2)

            # control force
            fc = m / tau * (v0 - vi)
            # social forces
            r = xi - xj
            d = torch.norm(r, dim=-1, keepdim=True)
            n = r / d
            t = torch.stack((-1 * n[:, :, 1], n[:, :, 0]), dim=2)
            g = ((R - d) > 0).to(dtype=torch.float)
            Dvt = torch.bmm((vj - vi).view(-1, 1, 2), t.view(-1, 2, 1))
            Dvt = Dvt.view(num_people, num_people, 1)
            fs = ((A * torch.exp((R - d) / B) + k1 * g * (R - d)) * n
                  + k2 * g * (R - d) * Dvt * t)
            torch.diagonal(fs, dim1=0, dim2=1)[:] = 0
            fs = fs.sum(dim=1, keepdim=True)
            # walls not included
            fw = 0

            # sum
            div_dt = (fc + fs + fw) / m

            # update velocities

            div_dt_mag = div_dt.norm(dim=-1, keepdim=True).expand(-1, -1, 2)
            div_dt_high = div_dt_mag > 3.0
            div_dt[div_dt_high] *= 3.0 / div_dt_mag[div_dt_high]
            vi += div_dt * dt

            vi_mag = vi.norm(dim=-1, keepdim=True).expand(-1, -1, 2)
            vi_high = vi_mag > 10.0
            vi[vi_high] *= 10.0 / vi_mag[vi_high]
            xi += vi * dt

        output = {self._target_key: xi.view(original_shape) - position}
        return output, hidden


class RecurrentPedestrianMotionModel(PedestrianMotionModel):

    def __init__(self, config):
        super().__init__(config)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        return config

    def init_hidden(self, num_people, device=None):
        raise NotImplementedError('init hidden not implemented')

    def _init_lstm_hidden(self, num_people, layers, size, device=None):
        num_dir = 1
        hidden_shape = (layers * num_dir, num_people, size)
        return (torch.zeros(hidden_shape, device=device),
                torch.zeros(hidden_shape, device=device))


class SimpleMotionModel(RecurrentPedestrianMotionModel):
    """Simple LSTM motion model"""

    def __init__(self, config):
        super().__init__(config)
        self._input_tfs.append(tf.PositionToDisplacement(extrapolate_nans=True))
        self._target_tfs.append(tf.PositionToDisplacement(offset=1))
        self._input_key = 'displacement'
        self._target_key = 'displacement'
        self._output_targeter = ot.create(config['output_type'],
                                          config['output_args'])

        self._rnn = nn.LSTM(input_size=self._input_size,
                            hidden_size=self._rnn_hidden_size,
                            num_layers=self._rnn_layers)

        self._output_layer = nn.Linear(self._rnn_hidden_size,
                                       self._output_targeter.dims)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'output_type': 'direct',
            'output_args': {},
            'rnn_hidden_size': 64,
            'rnn_layers': 2,
        })
        return config

    def init_hidden(self, num_people, device=torch.device('cpu')):
        hidden = super()._init_lstm_hidden(
            num_people, self._rnn_layers, self._rnn_hidden_size, device)
        return hidden

    def forward(self, model_input, hidden=None):
        displacement = model_input['displacement']

        seq_len, num_people, dims = displacement.shape
        assert dims == self._input_size

        rnn_output, hidden = self._rnn(displacement, hidden)
        fc_output = self._output_layer(rnn_output)
        output = {self._target_key: fc_output}
        return output, hidden


class SimpleEgoModel(RecurrentPedestrianMotionModel):
    """Simple LSTM motion model"""

    def __init__(self, config):
        super().__init__(config)
        self._input_tfs = [tf.PositionToEgoDisplacement(extrapolate_nans=True)]
        self._target_tfs = [tf.PositionToEgoDisplacement(offset=1)]
        self._input_key = 'ego_displacement'
        self._target_key = 'ego_displacement'
        self._output_targeter = ot.create(config['output_type'],
                                          config['output_args'])

        self._rnn = nn.LSTM(input_size=self._input_size,
                            hidden_size=self._rnn_hidden_size,
                            num_layers=self._rnn_layers)

        self._output_layer = nn.Linear(self._rnn_hidden_size,
                                       self._output_targeter.dims)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'output_type': 'direct',
            'output_args': {},
            'rnn_hidden_size': 64,
            'rnn_layers': 2,
        })
        return config

    def init_hidden(self, num_people, device=torch.device('cpu')):
        hidden = super()._init_lstm_hidden(
            num_people, self._rnn_layers, self._rnn_hidden_size, device)
        return hidden

    def forward(self, model_input, hidden=None):
        displacement = model_input['ego_displacement']

        seq_len, num_people, dims = displacement.shape
        assert dims == self._input_size

        rnn_output, hidden = self._rnn(displacement, hidden)
        fc_output = self._output_layer(rnn_output)
        output = {self._target_key: fc_output}
        return output, hidden

    def propagate_input(self, model_input, model_output):
        position = model_input['position']
        orientation = model_input['orientation']
        ego_displacement = model_output['ego_displacement']
        displacement = utils.rotate_2d(ego_displacement, orientation)
        position = position + displacement
        return {'position': position,
                'displacement': displacement,
                'orientation': orientation,
                'ego_displacement': ego_displacement}


class IndividualEgoTrajectoryModel(RecurrentPedestrianMotionModel):
    """Non social model for predticing a future trajectory at each prediction
    step"""

    def __init__(self, config):
        super().__init__(config)
        self._temporal_offsets = range(1, 1 + self._trajectory_length)
        self._input_tfs = [tf.PositionToEgoDisplacement(extrapolate_nans=True)]
        self._target_tfs = [tf.PositionToDisplacementTrajectory(
            self._trajectory_length)]
        self._input_key = 'ego_displacement'
        self._target_key = 'displacement_trajectory'
        self._output_targeter = ot.create(config['output_type'],
                                          config['output_args'])

        self._rnn = nn.LSTM(input_size=self._input_size,
                            hidden_size=self._rnn_hidden_size,
                            num_layers=self._rnn_layers,
                            dropout=self._dropout)

        self._output_layer = nn.Linear(
            self._rnn_hidden_size,
            self._trajectory_length * self._output_targeter.dims)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'output_type': 'direct',
            'output_args': {},
            'rnn_hidden_size': 64,
            'rnn_layers': 2,
            'trajectory_length': 15,
            'dropout': 0.0
        })
        return config

    def init_hidden(self, num_people, device=torch.device('cpu')):
        hidden = super()._init_lstm_hidden(
            num_people, self._rnn_layers, self._rnn_hidden_size, device)
        return hidden

    def forward(self, model_input, hidden=None):
        displacement = model_input['ego_displacement']

        seq_len, num_people, dims = displacement.shape
        assert dims == self._input_size

        rnn_output, hidden = self._rnn(displacement, hidden)
        fc_output = self._output_layer(F.dropout(rnn_output, p=self._dropout))
        fc_output = fc_output.view(seq_len, num_people,
                                   self._trajectory_length,
                                   self._output_targeter.dims)
        output = {self._target_key: fc_output}
        return output, hidden

    def propagate_input(self, model_input, model_output):

        # Get only the last position from the input and check dims
        last_position = model_input['position'][-1:]
        last_position: torch.Tensor
        assert len(last_position.shape) == 3
        assert last_position.shape[-1] == 2

        # Get only the last orientation from the input and check dims
        last_orientation = model_input['orientation'][-1:]
        last_orientation: torch.Tensor
        assert len(last_orientation.shape) == 2
        assert last_position.shape[0:2] == last_orientation.shape[0:2]

        # Convert displacements from local orientation to global orientation
        local_displacements = model_output['displacement_trajectory'][-1:]
        local_displacements: torch.Tensor
        local_angles = torch.atan2(local_displacements[..., 1],
                                   local_displacements[..., 0])
        last_orientation = last_orientation.view(1, -1, 1)
        local_angles = torch.cat((last_orientation, local_angles), dim=2)
        global_angles = local_angles.cumsum(dim=2)
        global_displacements = utils.rotate_2d(local_displacements,
                                               global_angles[:, :, :-1])

        # Accumulate displacements on top of last pos to get positions
        last_position = last_position.view(1, -1, 1, 2)
        global_displacements = torch.cat((last_position, global_displacements),
                                         dim=2)
        global_positions = global_displacements.cumsum(dim=2)
        global_positions = global_positions[:, :, 1:]

        return {'position': global_positions}

    # def propagate_input(self, model_input, model_output):
    #     last_position = model_input['position'][-1:]
    #     assert len(last_position.shape) == 3
    #     assert last_position.shape[-1] == 2
    #     last_orientation = model_input['orientation'][-1:]
    #     assert len(last_orientation.shape) == 2
    #     assert last_position.shape[0:2] == last_orientation.shape[0:2]
    #     ego_future_displacements = model_output['future_ego_displacements'][-1:]
    #     assert last_position.shape[1] == ego_future_displacements.shape[1]
    #     seq_len, num_ppl, num_steps, dims = ego_future_displacements.shape
    #     displacements = utils.rotate_2d(
    #         ego_future_displacements,
    #         last_orientation.view(1, num_ppl, 1, 1)
    #             .expand(-1, num_ppl, num_steps, -1))
    #     positions = displacements + last_position.view(1, num_ppl, 1, 2)
    #     return {'position': positions,
    #             'future_displacements': displacements,
    #             'orientation': last_orientation}


class SimpleSocialModel(RecurrentPedestrianMotionModel):
    '''Simple social LSTM motion model'''

    def __init__(self, config):
        super().__init__(config)
        self._input_tfs.append(tf.PositionToDisplacement(extrapolate_nans=True))
        self._input_tfs.append(tf.PositionToLocalGrid(
            self._global_radius,
            self._global_resolution,
            self._local_radius,
            self._local_resolution))
        self._target_tfs.append(tf.PositionToDisplacement(offset=1))
        self._input_key = 'displacement'
        self._target_key = 'displacement'
        self._input_grid_size = self._local_resolution**2
        self._output_targeter = ot.create(config['output_type'],
                                          config['output_args'])

        self._input_mlp = create_mlp(
            [self._input_size]
            + [self._input_mlp_size]
            * self._input_mlp_layers,
            'leaky_relu', layer_norm=False)

        self._input_grid_mlp = create_mlp(
            [self._input_grid_size]
            + [self._input_grid_mlp_size]
            * self._input_grid_mlp_layers,
            'leaky_relu', layer_norm=False)

        self._rnn = nn.LSTM(
            self._input_mlp_size
            + self._input_grid_mlp_size,
            self._rnn_hidden_size,
            self._rnn_layers)

        self._output_layer = nn.Linear(self._rnn_hidden_size,
                                       self._output_targeter.dims)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'output_type': 'direct',
            'output_args': {},
            'global_radius': 10.0,
            'global_resolution': 40,
            'local_radius': 1.0,
            'local_resolution': 8,
            'input_mlp_layers': 2,
            'input_mlp_size': 64,
            'input_grid_mlp_layers': 2,
            'input_grid_mlp_size': 128,
            'rnn_layers': 2,
            'rnn_hidden_size': 128,
        })
        return config

    def forward(self, model_input, hidden=None):
        displacement = model_input['displacement']
        local_grid = model_input['local_grid']
        seq_len, num_people, dims = displacement.shape
        assert dims == self._input_size
        a = self._input_mlp(displacement)
        b = self._input_grid_mlp(local_grid.view(seq_len, num_people, -1))
        x, hidden = self._rnn(torch.cat((a, b), dim=-1), hidden)
        x = self._output_layer(x)
        output = {self._target_key: x}
        return output, hidden


class APGModel(RecurrentPedestrianMotionModel):
    '''Simple social LSTM motion model'''

    def __init__(self, config):
        super().__init__(config)
        self._apg_tf = tf.PositionToAPG(self._angular_segments, self._max_range)
        self._input_tfs.append(tf.PositionToEgoDisplacement(extrapolate_nans=True))
        self._input_tfs.append(self._apg_tf)
        self._target_tfs.append(tf.PositionToEgoDisplacement(offset=1))
        self._input_key = 'ego_displacement'
        self._target_key = 'ego_displacement'
        self._output_targeter = ot.create(config['output_type'],
                                          config['output_args'])


        warnings.filterwarnings('ignore', message='.*non-zero dropout expects '
                                                  'num_layers greater than 1.*')
        self._disp_rnn = nn.LSTM(self._input_size,
                                 self._disp_rnn_size,
                                 self._disp_rnn_layers,
                                 dropout=self._dropout)

        self._apg_fc = nn.Linear(self._angular_segments,
                                 self._apg_rnn_size)

        self._apg_rnn = nn.LSTM(self._apg_rnn_size,
                                self._apg_rnn_size,
                                self._apg_rnn_layers,
                                dropout=self._dropout)

        self._final_rnn = nn.LSTM(self._disp_rnn_size + self._apg_rnn_size,
                                  self._final_rnn_size,
                                  self._final_rnn_layers,
                                  dropout=self._dropout)

        self._final_mlp = create_mlp(
            [self._final_rnn_size]
            + [self._final_mlp_size] * self._final_mlp_layers,
            dropout=self._dropout)

        self._final_fc = nn.Linear(self._final_mlp_size,
                                   self._output_targeter.dims)

    def init_hidden(self, num_people, device=torch.device('cpu')):
        hidden = (
                super()._init_lstm_hidden(num_people, self._disp_rnn_layers,
                                          self._disp_rnn_size, device)
                + super()._init_lstm_hidden(num_people, self._apg_rnn_layers,
                                            self._apg_rnn_size, device)
                + super()._init_lstm_hidden(num_people, self._final_rnn_layers,
                                            self._final_rnn_size, device)
        )
        return hidden

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'output_type': 'direct',
            'output_args': {},
            'angular_segments': 72,
            'max_range': 6.0,
            'disp_rnn_size': 32,
            'disp_rnn_layers': 1,
            'apg_rnn_size': 128,
            'apg_rnn_layers': 1,
            'final_rnn_size': 512,
            'final_rnn_layers': 1,
            'final_mlp_size': 256,
            'final_mlp_layers': 1,
            'dropout': 0.0
        })
        return config

    def forward(self, model_input, hidden=None):
        disp = model_input['ego_displacement']
        #disp = model_input['displacement_trajectory_direct']

        apg = model_input['apg']
        assert torch.isfinite(apg).all()
        seq_len, num_people, dims = disp.shape
        assert dims == self._input_size

        if hidden is None:
            disp_hidden = None
            apg_hidden = None
            final_hidden = None
        else:
            disp_hidden = hidden[0:2]
            apg_hidden = hidden[2:4]
            final_hidden = hidden[4:6]

        a, disp_hidden = self._disp_rnn(disp, disp_hidden)
        assert torch.isfinite(a).all()
        b = self._apg_fc(apg)
        b, apg_hidden = self._apg_rnn(F.dropout(b, p=self._dropout),
                                      apg_hidden)
        assert torch.isfinite(b).all()
        c, final_hidden = self._final_rnn(
            F.dropout(torch.cat((a, b), dim=-1), p=self._dropout),
            final_hidden)
        assert torch.isfinite(c).all()
        c = self._final_mlp(F.dropout(c, p=self._dropout))
        x = self._final_fc(F.dropout(c, p=self._dropout))

        hidden = disp_hidden + apg_hidden + final_hidden
        output = {self._target_key: x}
        return output, hidden

    def propagate_input(self, model_input, model_output):
        position = model_input['position']
        orientation = model_input['orientation']
        ego_displacement = model_output['ego_displacement']
        displacement = utils.rotate_2d(ego_displacement, orientation)
        position = torch.cat((position, position + displacement))
        output = {'position': position[-1:],
                'displacement': displacement,
                'orientation': orientation,
                'ego_displacement': ego_displacement}
        output.update(self._apg_tf({'position': position[-2:]}))
        return output


class APGTrajectoryModel(APGModel):
    def __init__(self, config):
        super().__init__(config)
        self._target_tfs = [tf.PositionToDisplacementTrajectory(
            self._trajectory_length)]
        self._target_key = 'displacement_trajectory'

        self._final_fc = nn.Linear(
            self._final_mlp_size,
            self._trajectory_length * self._output_targeter.dims)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'trajectory_length': 0,
        })
        return config

    def forward(self, model_input, hidden=None):
        output, hidden = super().forward(model_input, hidden=None)
        output_shape = output[self._target_key].shape
        output[self._target_key] = output[self._target_key].view(
            output_shape[:-1]
            + (self._trajectory_length, self._output_targeter.dims))
        return output, hidden

    def propagate_input(self, model_input, model_output):

        # Get only the last position from the input and check dims
        last_position = model_input['position'][-1:]
        last_position: torch.Tensor
        assert len(last_position.shape) == 3
        assert last_position.shape[-1] == 2

        # Get only the last orientation from the input and check dims
        last_orientation = model_input['orientation'][-1:]
        last_orientation: torch.Tensor
        assert len(last_orientation.shape) == 2
        assert last_position.shape[0:2] == last_orientation.shape[0:2]

        # Convert displacements from local orientation to global orientation
        local_displacements = model_output['displacement_trajectory'][-1:]
        local_displacements: torch.Tensor
        local_angles = torch.atan2(local_displacements[..., 1],
                                   local_displacements[..., 0])
        last_orientation = last_orientation.view(1, -1, 1)
        local_angles = torch.cat((last_orientation, local_angles), dim=2)
        global_angles = local_angles.cumsum(dim=2)
        global_displacements = utils.rotate_2d(local_displacements,
                                              global_angles[:, :, :-1])

        # Accumulate displacements on top of last pos to get positions
        last_position = last_position.view(1, -1, 1, 2)
        global_displacements = torch.cat((last_position, global_displacements),
                                         dim=2)
        global_positions = global_displacements.cumsum(dim=2)
        global_positions = global_positions[:, :, 1:]

        return {'position': global_positions}

# class SocialRTOGModel(RecurrentPedestrianMotionModel):
#
#     def __init__(self, config):
#         super().__init__(config)
#
#         # Make sure RTOG dimensions are even numbers
#         assert(self._local_resolution % 2 == 0)
#         assert(self._global_resolution % 2 == 0)
#
#         self._scale = (float(self._global_radius)
#                        / float(self._local_radius))
#         assert(self._scale >= 1.0)
#
#         self._temporal_slices = len(self._temporal_offsets)
#         self._rtog_size = (self._local_resolution**2
#                            * self._temporal_slices)
#
#         # What mode/phase of training are we in?
#         # used to phase training
#         self._mode = None
#
#         self._rnn = nn.LSTM(
#             input_size=self._input_size,
#             hidden_size=self._rnn_hidden_size,
#             num_layers=self._rnn_layers)
#
#         # Linear mapping of hidden state to personal RTOG
#         self._rtog = nn.Linear(self._rnn_hidden_size,
#                                self._rtog_size)
#
#         # MLP used to regress displacement from RNN output and social RTOG
#         self._mlp = create_mlp([self._rnn_hidden_size
#                                + self._rtog_size]
#                                + [self._social_hidden_size]
#                                * self._social_layers,
#                                'leaky_relu')
#
#         # Linear mapping of mlp output to prediction space
#         self._regression = nn.Linear(self._social_hidden_size,
#                                      self._output_targeter.dims)
#
#     @classmethod
#     def default_config(cls):
#         config = super().default_config()
#         config.update({
#             'rnn_layers': 2,
#             'rnn_hidden_size': 512,
#             'social_layers': 2,
#             'social_hidden_size': 512,
#             'local_radius': 0.4,
#             'local_resolution': 10,
#             'global_radius': 10.0,
#             'global_resolution': 20,
#             'temporal_offsets': [5, 10],
#         })
#         return config
#
#     def prepare_input(self, position_sequence, start=0, stop=None):
#         return self.prepare_input_displacement(position_sequence, start, stop)
#
#     @property
#     def _local_radius(self):
#         return self._config['local_radius']
#
#     @property
#     def _local_resolution(self):
#         return self._config['local_resolution']
#
#     @property
#     def _global_radius(self):
#         return self._config['global_radius']
#
#     @property
#     def _global_resolution(self):
#         return self._config['global_resolution']
#
#     @property
#     def _temporal_offsets(self):
#         return self._config['temporal_offsets']
#
#     @property
#     def _social_layers(self):
#         return self._config['social_layers']
#
#     @property
#     def _social_hidden_size(self):
#         return self._config['social_hidden_size']
#
#     def mode(self, mode):
#         """Switch the learning mode, locks some layers from learning
#
#         This facilitates a staged learning approach where the end-to-end
#         problem can be broken into sub-problems.
#         """
#
#         if mode == 'individual':
#             self._rnn.requires_grad_(True)
#             self._mlp.requires_grad_(True)
#             self._regression.requires_grad_(True)
#             self._rtog.requires_grad_(False)
#         elif mode == 'rtog':
#             self._rnn.requires_grad_(True)
#             self._mlp.requires_grad_(False)
#             self._regression.requires_grad_(False)
#             self._rtog.requires_grad_(True)
#         elif mode == 'full':
#             self._rnn.requires_grad_(True)
#             self._mlp.requires_grad_(True)
#             self._regression.requires_grad_(True)
#             self._rtog.requires_grad_(True)
#         else:
#             ValueError('Mode {} not implemented'.format(mode))
#
#         self._mode = mode
#         return
#
#     def forward(self, model_input, hidden=None):
#         displacement = model_input['displacement']
#         position = model_input['position']
#
#         if displacement.shape != position.shape:
#             raise ValueError(
#                 'Displacement and position must be the same shape')
#
#         assert not torch.isnan(displacement).any()
#         assert not torch.isnan(position).any()
#
#         # Store the sequence and length and number of people (batch dimension)
#         seq_len, num_people, dims = displacement.shape
#
#         # Pass velocities through the RNN
#         rnn_output, hidden = self._rnn(displacement, hidden)
#
#         # Lets define some shorthand to make naming easier
#         # lcl - "local" centered around person
#         # glb - "global" centered on scene
#         # ind - "individual" information about single person
#         # tot - "total" information about everyone
#         # soc - "social" information about others
#         # rtog - relative temporal occupancy grid
#
#         output = {}
#
#         if self._mode == 'individual':
#             # In individual mode we just create blank rtogs
#             lcl_soc_rtog = torch.zeros(
#                 (seq_len, num_people, self._rtog_size),
#                 device=displacement.device)
#         else:
#
#             # Map RNN output to RTOG space
#             lcl_ind_rtog = self._rtog(rnn_output)
#
#             # Softmax per temporal slice to ensure each grid sums to 1
#             lcl_ind_rtog = lcl_ind_rtog.view(
#                 seq_len, num_people, self._temporal_slices,
#                 self._local_resolution**2)
#             lcl_ind_rtog = F.log_softmax(lcl_ind_rtog, dim=-1)
#
#             if self._mode == 'rtog':
#                 output['local_rtog'] = lcl_ind_rtog.view(
#                     seq_len, num_people, self._temporal_slices,
#                     self._local_resolution,
#                     self._local_resolution)
#                 return output, hidden
#
#             lcl_ind_rtog = lcl_ind_rtog.view(-1, self._temporal_slices,
#                 self._local_resolution,
#                 self._local_resolution)
#
#             glb_ind_rtog = utils.grid_transform(
#                 lcl_ind_rtog, position.view(-1, dims),
#                 self._local_radius,
#                 self._global_radius,
#                 self._global_resolution)
#
#             # Sum global individual RTOGs to create total global RTOG
#             glb_ind_rtog = glb_ind_rtog.view(
#                 seq_len, num_people,
#                 self._temporal_slices
#                 * self._global_resolution**2)
#
#             glb_tot_rtog = (glb_ind_rtog.sum(1, keepdim=True)
#                                         .expand(-1, num_people, -1))
#
#             # Remove the information of each indiviudal from the total RTOG
#             # to obtain an RTOG about other people only
#             glb_soc_rtog = glb_tot_rtog - glb_ind_rtog
#
#             glb_soc_rtog = glb_soc_rtog.view(-1, self._temporal_slices,
#                 self._global_resolution,
#                 self._global_resolution)
#
#             lcl_soc_rtog = utils.grid_transform(
#                 glb_soc_rtog, -position.view(-1, dims),
#                 self._global_radius,
#                 self._local_radius,
#                 self._local_resolution)
#
#         rnn_output = rnn_output.view(seq_len * num_people, -1)
#         lcl_soc_rtog = lcl_soc_rtog.view(seq_len * num_people, -1)
#         prediction = self._mlp(torch.cat((rnn_output, lcl_soc_rtog), dim=-1))
#         prediction = self._regression(prediction)
#         prediction = prediction.view(seq_len, num_people, -1)
#
#         if self._output_type == '2d':
#             output['displacement'] = prediction
#         elif self._output_type == '2d_gaussian':
#             output['displacement_2d_gaussian'] =\
#                 utils.constrain_bivariate_gaussian(prediction)
#         elif self._output_type == 'grid':
#             prediction = prediction.view(
#                 seq_len, num_people, self._output_resolution**2)
#             output['displacement_grid'] =\
#                 F.log_softmax(prediction, dim=-1).view(
#                 seq_len, num_people, self._output_resolution,
#                 self._output_resolution)
#
#         return output, hidden
#
#     def predict(self, pos_seq, hidden=None, start=0, stop=None, sample_steps=0,
#                 stochastic=True):
#         if self._mode == 'rtog':
#             assert sample_steps == 0
#             input = self.prepare_input(pos_seq, start, stop)
#             return self(input, hidden)
#         else:
#             return super().predict(
#                 pos_seq, hidden, start, stop, sample_steps, stochastic)
#
#     def prepare_target(self, input_sequence, start=0, stop=None, sample_steps=0):
#         if self._mode == 'rtog':
#             return self.prepare_target_rtog(input_sequence, start, stop, sample_steps)
#         else:
#             return super().prepare_target(input_sequence, start, stop, sample_steps)
#
#     def prepare_target_rtog(self, pos_seq, start=0, stop=None, sample_steps=0):
#         assert sample_steps == 0
#         full_len, num_people, dims = pos_seq.shape
#         max_offset = self._temporal_offsets[-1]
#         if stop is None:
#             stop = full_len - max_offset
#         if stop + max_offset > full_len:
#             return None
#
#         # Compute velocities and frame aligned positions
#
#         true_relative_ind = lstm_motion_model.utils.pos_seq_to_relative_indices(
#             pos_seq, start, stop,
#             self._local_radius,
#             self._local_resolution,
#             self._temporal_offsets, flatten_index=True)
#         # assert not torch.isnan(pos_seq).any()
#         # Zero out all nan velocities
#         # TODO: Should handle nans in a smart way than this
#         # velocity_sequence[torch.isnan(velocity_sequence)] = 0.0
#
#         target = {}
#         target['local_rtog_idx'] = true_relative_ind.view(
#             stop - start, num_people, len(self._temporal_offsets), 1)
#         target['resolution'] = self._local_resolution
#
#         # support = torch.bincount(
#             # true_relative_ind[true_relative_ind >= 0],
#             # minlength=self._local_resolution**2) + 1
#         # weight = support.max() / support.to(dtype=torch.float)
#         # weight = None
#         return target
#
#
#     def compute_loss(self, predicted, target):
#         if self._mode == 'rtog':
#             pred_local_rtog = predicted['local_rtog'].view(
#                 -1, self._local_resolution**2)
#             target_rtog_idx = target['local_rtog_idx'].view(-1)
#             return F.nll_loss(pred_local_rtog, target_rtog_idx)
#         else:
#             return super().compute_loss(predicted, target)
#
#

class SocialContinuousModel(RecurrentPedestrianMotionModel):

    def __init__(self, config):
        super().__init__(config)
        self._preview_len = 2

        self._social_resolution = 21
        self._temporal_slices = len(self._temporal_offsets)
        self._social_context_size = self._social_resolution**2 * self._temporal_slices
        self._input_key = 'ego_displacement'

        self._input_tfs.append(tf.PositionToEgoDisplacement(extrapolate_nans=True))
        # target_tfs and targeter are set in mode()
        self._target_tf_default = tf.PositionToEgoDisplacement(offset=1)
        self._ot_phase_1 = ot.BivariateGaussian()
        self._ot_phase_2 = ot.create(config['output_type'],
                                     config['output_args'])

        # What mode/phase of training are we in?
        # used to phase training
        self._mode = None

        # Interpret input sequences to make individual prediction
        self._rnn_individual = nn.LSTM(
            input_size=self._input_size,
            hidden_size=self._rnn_hidden_size,
            num_layers=self._rnn_layers)

        # Linear mapping of hidden state to individual prediction
        self._fc_individual = nn.Linear(self._rnn_hidden_size,
                                        self._temporal_slices * 5)

        # Interpret input sequences to make social prediction
        self._rnn_social = nn.LSTM(
            input_size=self._input_size,
            hidden_size=self._rnn_hidden_size,
            num_layers=self._rnn_layers)

        # Combine output of rnn with social context to make social prediction
        self._mlp_social = create_mlp([self._rnn_hidden_size
                               + self._social_context_size]
                               + [self._social_hidden_size]
                               * self._social_layers,
                               'leaky_relu', layer_norm=False)

        # Linear mapping of mlp output to prediction space
        self._fc_social = nn.Linear(self._social_hidden_size,
                               self._ot_phase_2.dims)

    @classmethod
    def default_config(cls):
        config = super().default_config()
        config.update({
            'output_type': 'direct',
            'output_args': {},
            'rnn_layers': 2,
            'rnn_hidden_size': 512,
            'social_layers': 2,
            'social_hidden_size': 512,
            'temporal_offsets': [1, 2, 4],
        })
        return config

    def init_hidden(self, num_people, device=torch.device('cpu')):
        return (super()._init_lstm_hidden(num_people, self._rnn_layers,
                                         self._rnn_size, device)
                + super()._init_lstm_hidden(num_people, self._rnn_layers,
                                         self._rnn_size, device))

    def mode(self, mode):
        """Switch the learning mode, affects forward pass
        """

        # Use default target_tf and targeter unless overridden by mode below
        self._target_tfs = [self._target_tf_default]
        self._output_targeter = self._ot_phase_2
        self._target_key = 'ego_displacement'

        if mode == 'phase_1':
            self._rnn_individual.requires_grad_(True)
            self._fc_individual.requires_grad_(True)
            self._rnn_social.requires_grad_(False)
            self._mlp_social.requires_grad_(False)
            self._fc_social.requires_grad_(False)
            self._target_tfs = [tf.PositionToFutureDisplacements(
                self._temporal_offsets, egocentric=True)]
            self._output_targeter = self._ot_phase_1
            self._target_key = 'future_displacements'
        elif mode == 'phase_2':
            self._rnn_individual.requires_grad_(False)
            self._fc_individual.requires_grad_(False)
            self._rnn_social.requires_grad_(True)
            self._mlp_social.requires_grad_(True)
            self._fc_social.requires_grad_(True)
        elif mode == 'full':
            self._rnn_individual.requires_grad_(True)
            self._fc_individual.requires_grad_(True)
            self._rnn_social.requires_grad_(True)
            self._mlp_social.requires_grad_(True)
            self._fc_social.requires_grad_(True)
        else:
            ValueError('Mode {} not implemented'.format(mode))

        self._mode = mode
        return

    def forward(self, model_input, hidden=None):

        if self._mode is None:
            raise RuntimeError('No mode has been set')

        if hidden is None:
            hidden_individual = None
            hidden_social = None
        else:
            hidden_individual = hidden[:2]
            hidden_social = hidden[2:]

        displacement = model_input['ego_displacement']
        position = model_input['position']
        orientation = model_input['orientation']

        if displacement.shape != position.shape:
            raise ValueError(
                'Displacement and position must be the same shape')

        assert not torch.isnan(displacement).any()
        assert not torch.isnan(position).any()

        # Store the sequence and length and number of people (batch dimension)
        seq_len, num_people, dims = displacement.shape
        assert seq_len > 0
        assert num_people > 0
        assert dims > 0

        rnn_output_individual, hidden_individual = self._rnn_individual(
            displacement, hidden_individual)

        fc_individual_output = self._fc_individual(rnn_output_individual)
        fc_individual_output = fc_individual_output.view(
            seq_len, num_people, self._temporal_slices, 5)
        individual_predictions = self._ot_phase_1.compose_output(
            fc_individual_output)

        if self.tb_writer is not None and self._step % 100 == 0:
            self.tb_writer.add_histogram('fc individual output',
                                         fc_individual_output)
            for s in range(self._temporal_slices):
                self.tb_writer.add_histogram(
                    'mu_x/{}'.format(s), individual_predictions[..., s, 0])
                self.tb_writer.add_histogram(
                    'mu_y/{}'.format(s), individual_predictions[..., s, 1])
                self.tb_writer.add_histogram(
                    'sigma_x/{}'.format(s), individual_predictions[..., s, 2])
                self.tb_writer.add_histogram(
                    'sigma_y/{}'.format(s), individual_predictions[..., s, 3])
                self.tb_writer.add_histogram(
                    'rho/{}'.format(s), individual_predictions[..., s, 4])

        if self._mode == 'phase_1':
            key = '_'.join((self._target_key, self._output_targeter.label))
            output = {key: individual_predictions}
            return output, hidden_individual + hidden_social
        else:
            social_context = self.compute_social_context_egocentric(position, orientation, individual_predictions)
            if self._mode == 'phase_2':
                social_context = social_context.detach()

            # rnn_output_social, hidden_social = self._rnn_social(
                # displacement, hidden_social)

            if self.tb_writer is not None and self._step % 1000 == 0:
                self.tb_writer.add_video('social_context', social_context.transpose(0, 1), fps=5)
            social_context = social_context.view(seq_len, num_people, self._social_context_size)

            mlp_output = self._mlp_social(torch.cat((rnn_output_individual, social_context), dim=-1))
            fc_social_output = self._fc_social(mlp_output)
            criterion.assert_finite(fc_social_output)
            social_predictions = self._ot_phase_2.compose_output(
                fc_social_output)

            if self.tb_writer is not None and self._step % 100 == 0:
                self.tb_writer.add_histogram('fc_social_output',
                                             fc_social_output)
                self.tb_writer.add_histogram('social_mu/x',
                                             social_predictions[..., 0])
                self.tb_writer.add_histogram('social_mu/y',
                                             social_predictions[..., 1])
                if social_predictions.shape[-1] == 5:
                    self.tb_writer.add_histogram('social_sigma/x',
                                                 social_predictions[..., 2])
                    self.tb_writer.add_histogram('social_sigma/y',
                                                 social_predictions[..., 3])
                    self.tb_writer.add_histogram('rho',
                                                 social_predictions[..., 4])

            key = '_'.join((self._target_key, self._output_targeter.label))
            output = {key: social_predictions}
            return output, hidden_individual + hidden_social

    def sample_prediction_output(self, predicted, stochastic):
        if self._mode == 'phase_1':
            predicted['displacement_2d_gaussian'] = \
                predicted['displacement_2d_gaussian'][:, :, 0, :]
        predicted = super().sample_prediction_output(predicted, stochastic)
        return predicted
#    def predict_multi_gaussian(self, pos_seq, hidden=None, start=0, stop=None,
#                               sample_steps=0, stochastic=True):
#        assert sample_steps == 0
#        input = self.prepare_input(pos_seq, start, stop)
#        model_output = self(input, hidden)
#        model_output

    def compute_social_context(self, position, predicted_displacements):
        '''
        Compute a grid around each person representing the social context

        The input predicted_displacements is excepted to contain num_gaussians
        gaussian distributions describing the displacement of each person at
        num_gaussians moments in the future from their current position.
        The return is a grid centered on each person representing the
        probability density of the point being occupied by any other person
        '''
        # TODO: Bring in these parameters from config
        radius = 3.0
        distance_threshold = 2.0
        # distance_threshold = radius
        assumed_probability = 0.95
        res = self._social_resolution

        # oversize_ratio = 2.0
        # oversize_res = res * oversize_ratio
        # oversize_radius = radius * oversize_ratio

        local_debug = False

        device = position.device
        seq_len, num_ppl, dims = position.shape
        (seq_len_2, num_ppl_2, num_gaussians, num_params) = (
            predicted_displacements.shape)

        assert dims == 2
        assert num_params == 5
        assert seq_len == seq_len_2
        assert num_ppl == num_ppl_2

        # Extract individual parameters from NN output
        mu = predicted_displacements[..., :2]

        # Construct covariance matricies
        covar = utils.construct_covar_from_params(
            predicted_displacements[..., 2:])

        # Offset means by position
        # Use of slicing notation (:) below updates elements of
        # predicted_displacements of which mu is a view
        # Unsqueeze to broadcast across gaussians
        mu[:] = mu + position.unsqueeze(2)

        # Create an evenly spaced grid
        x = torch.linspace(-radius, radius, res, device=device)
        grid = torch.stack(torch.meshgrid([x, x]), dim=-1)

        # Compute distance between each current position and each predicted
        # future position. This adds a second ppl dimension.
        # (frames, actual person, predicted person, predictions, dimensions)
        distance = (
            mu.view(seq_len, 1, num_ppl, num_gaussians, dims)
            - position.view(seq_len, num_ppl, 1, 1, dims)).norm(2, dim=-1)

        assert distance.shape == (seq_len, num_ppl, num_ppl, num_gaussians)

        # Mask to select those within distance threshold
        near = distance < distance_threshold
        p_indicies = torch.arange(num_ppl, device=device)
        # Mask to ignore self comparison
        valid_pairs = p_indicies.view(-1, 1) != p_indicies.view(1, -1)
        # Combine masks
        neighbours = near & valid_pairs.view(1, num_ppl, num_ppl, 1)
        assert neighbours.shape == (seq_len, num_ppl, num_ppl, num_gaussians)
        # How many neighbours
        num_neighbours = neighbours.sum()

        if num_neighbours > 0:
            mu_view = mu.view(seq_len, 1, num_ppl, num_gaussians, dims)
            mu_view = mu_view.expand(-1, num_ppl, -1, -1, -1)
            covar_view = covar.view(seq_len, 1, num_ppl, num_gaussians, dims, dims)
            covar_view = covar_view.expand(-1, num_ppl, -1, -1, -1, -1)
            mu_select = mu_view[neighbours]
            covar_select = covar_view[neighbours]
            assert mu_select.shape == (num_neighbours, dims)
            assert covar_select.shape == (num_neighbours, dims, dims)

            # Create distributions
            scale_tril = torch.cholesky(covar_select.cpu()).to(device=covar_select.device)
            dist = MultivariateNormal(mu_select, scale_tril=scale_tril)

            # Offset the grids by position
            all_grids = (grid.view(res, res, 1, 1, dims)
                         + position.view(1, 1, seq_len, num_ppl, dims))
            assert all_grids.shape == (res, res, seq_len, num_ppl, dims)

            # batch = seq_len, num_ppl, num_ppl, num_gaussians
            # (batch), seq_len, num_ppl_mu, num_gaussian, dims
            all_grids_view = all_grids.view(res, res, seq_len, num_ppl, 1, 1, dims)
            all_grids_view = all_grids_view.expand(-1, -1, -1, -1, num_ppl, num_gaussians, dims)
            all_grids_select = all_grids_view[:, :, neighbours, :]

            p_is = dist.log_prob(all_grids_select).exp()
            assert p_is.shape == (res, res, num_neighbours)
            p_is = torch.stack(p_is.unbind(-1), dim=0)
            assert p_is.shape == (num_neighbours, res, res); p_is_sums = p_is.view(num_neighbours, res**2).sum(dim=-1)
            assert p_is_sums.shape == (num_neighbours,)
            # Sums computed above could equal zero
            # Untreated this would cause elements of norm_coef to be inf
            # Which would result (below) in 0 / inf which yields nan
            # We treat this by setting all elements of grids which sum to zero
            # to zero after normalilization effectively ignoring these people

            norm_coef = assumed_probability / p_is_sums
            p_is = p_is * norm_coef.view(num_neighbours, 1, 1)
            p_is = p_is.clone()
            p_is[torch.isinf(norm_coef), :, :] = 0.0
            assert p_is.shape == (num_neighbours, res, res)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                is_sum = p_is.view(num_neighbours, res * res).sum(-1)
                logging.debug('p_is max: {:.5f}, min: {:.5f}\n'
                              'max_sum: {:.5f}, min_sum: {:.5f}'.format(
                    p_is.max(), p_is.min(), is_sum.max(), is_sum.min()))


            p_is_full = torch.zeros(
                seq_len, num_ppl, num_ppl, num_gaussians, res, res, device=device)
            p_is_full[neighbours, :, :] = p_is

            p_any = 1 - (1 - p_is_full).prod(dim=2)
            assert p_any.shape == (seq_len, num_ppl, num_gaussians, res, res)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                any_sum = p_any.view(seq_len * num_ppl * num_gaussians, res * res).sum(-1)
                logging.debug('p_any max: {:.5f}, min: {:.5f}\n'
                              'max_sum: {:.5f}, min_sum: {:.5f}'.format(
                    p_any.max(), p_any.min(), any_sum.max(), any_sum.min()))

            if local_debug:
                plt.ion()
                for p in range(num_ppl):
                    image = p_any[0, p, 2, :, :]
                    plot = plt.imshow(image.cpu().detach().numpy(), vmax=0.03, vmin=0.0)
                    for f in range(seq_len):
                        image = p_any[f, p, 2, :, :]
                        plot.set_data(image.cpu().detach().numpy())
                        plt.show()
                        plt.pause(0.01)
                    plt.clf()
                    plt.pause(1.0)
        else:
            p_any = torch.zeros(
                seq_len, num_ppl, num_gaussians, res, res, device=device)

        assert torch.isfinite(p_any).all()
        return p_any


    def compute_social_context_egocentric(self, position, orientation, predicted_displacements):
        '''
        Compute a grid around each person representing the social context

        The input predicted_displacements is excepted to contain num_gaussians
        gaussian distributions describing the displacement of each person at
        num_gaussians moments in the future from their current position.
        The return is a grid centered on each person representing the
        probability density of the point being occupied by any other person
        '''
        # TODO: Bring in these parameters from config
        radius = 2.0
        distance_threshold = 1.5
        # distance_threshold = radius
        assumed_probability = 0.95
        res = self._social_resolution

        # oversize_ratio = 2.0
        # oversize_res = res * oversize_ratio
        # oversize_radius = radius * oversize_ratio

        local_debug = False

        device = position.device
        seq_len, num_ppl, dims = position.shape
        (seq_len_2, num_ppl_2, num_gaussians, num_params) = (
            predicted_displacements.shape)

        assert dims == 2
        assert num_params == 5
        assert seq_len == seq_len_2
        assert num_ppl == num_ppl_2

        # Extract individual parameters from NN output
        mu = predicted_displacements[..., :2]
        # Construct covariance matricies
        covar = utils.construct_covar_from_params(
            predicted_displacements[..., 2:])

        # Create an evenly spaced grid
        x = torch.linspace(-radius, radius, res, device=device)
        grid = torch.stack(torch.meshgrid([x, x]), dim=-1)

        # Compute position of each person(dim=2) relative to each other person(dim=0)
        rel_position = (position.view(seq_len, 1, num_ppl, dims)
                        - position.view(seq_len, num_ppl, 1, dims))
        rel_position = utils.rotate_2d(rel_position, -orientation
                                      .view(seq_len, num_ppl, 1)
                                      .expand(-1, -1, num_ppl))
        rel_orientation = (orientation.view(seq_len, 1, num_ppl)
                           - orientation.view(seq_len, num_ppl, 1))

        assert rel_orientation.shape == (seq_len, num_ppl, num_ppl)
        assert rel_position.shape == (seq_len, num_ppl, num_ppl, dims)


        # Compute distance to each person from each predicted future position
        # (frames, from predicted person, to person, predictions, dimensions)
        distance = (rel_position.view(seq_len, num_ppl, num_ppl, 1, dims)
                    - mu.view(seq_len, num_ppl, 1, num_gaussians, dims)
                    ).norm(2, dim=-1)

        assert distance.shape == (seq_len, num_ppl, num_ppl, num_gaussians)

        # Mask to select those within distance threshold
        near = distance < distance_threshold
        p_indicies = torch.arange(num_ppl, device=device)
        # Mask to ignore self comparison
        valid_pairs = p_indicies.view(-1, 1) != p_indicies.view(1, -1)
        # Combine masks
        neighbours = near & valid_pairs.view(1, num_ppl, num_ppl, 1)
        assert neighbours.shape == (seq_len, num_ppl, num_ppl, num_gaussians)
        # How many neighbours
        num_neighbours = neighbours.sum()

        if num_neighbours > 0:
            mu_view = mu.view(seq_len, num_ppl, 1, num_gaussians, dims)
            mu_view = mu_view.expand(-1, -1, num_ppl, -1, -1)
            covar_view = covar.view(seq_len, num_ppl, 1, num_gaussians, dims, dims)
            covar_view = covar_view.expand(-1, -1, num_ppl, -1, -1, -1)
            mu_select = mu_view[neighbours]
            covar_select = covar_view[neighbours]
            assert mu_select.shape == (num_neighbours, dims)
            assert covar_select.shape == (num_neighbours, dims, dims)

            # Create distributions
            scale_tril = torch.cholesky(covar_select.cpu()).to(device=covar_select.device)
            dist = MultivariateNormal(mu_select, scale_tril=scale_tril)

            # Offset the grids by position
            all_grids = grid.view(res, res, 1, 1, 1, dims)
            all_grids = all_grids.expand(-1, -1, seq_len, num_ppl, num_ppl, -1)
            all_grids = utils.rotate_2d(all_grids, rel_orientation
                                       .view(1, 1, seq_len, num_ppl, num_ppl)
                                       .expand(res, res, -1, -1, -1))
            all_grids = all_grids + rel_position
            assert all_grids.shape == (res, res, seq_len, num_ppl, num_ppl, dims)

            # batch = seq_len, num_ppl, num_ppl, num_gaussians
            # (batch), seq_len, num_ppl_mu, num_gaussian, dims
            all_grids_view = all_grids.view(res, res, seq_len, num_ppl, num_ppl, 1, dims)
            all_grids_view = all_grids_view.expand(-1, -1, -1, -1, -1, num_gaussians, -1)
            all_grids_select = all_grids_view[:, :, neighbours, :]

            p_is = dist.log_prob(all_grids_select).exp()
            assert p_is.shape == (res, res, num_neighbours)
            p_is = torch.stack(p_is.unbind(-1), dim=0)
            assert p_is.shape == (num_neighbours, res, res)
            p_is_sums = p_is.view(num_neighbours, res**2).sum(dim=-1)
            assert p_is_sums.shape == (num_neighbours,)
            # Sums computed above could equal zero
            # Untreated this would cause elements of norm_coef to be inf
            # Which would result (below) in 0 / inf which yields nan
            # We treat this by setting all elements of grids which sum to zero
            # to zero after normalilization effectively ignoring these people

            norm_coef = assumed_probability / p_is_sums
            p_is = p_is * norm_coef.view(num_neighbours, 1, 1)
            p_is = p_is.clone()
            p_is[torch.isinf(norm_coef), :, :] = 0.0
            assert p_is.shape == (num_neighbours, res, res)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                is_sum = p_is.view(num_neighbours, res * res).sum(-1)
                logging.debug(
                    'p_is max: {:.5f}, min: {:.5f}\n'
                    'max_sum: {:.5f}, min_sum: {:.5f}'.format(
                        p_is.max(), p_is.min(), is_sum.max(), is_sum.min()))

            p_is_full = torch.zeros(
                seq_len, num_ppl, num_ppl, num_gaussians, res, res, device=device)
            p_is_full[neighbours, :, :] = p_is

            p_any = 1 - (1 - p_is_full).prod(dim=1)
            assert p_any.shape == (seq_len, num_ppl, num_gaussians, res, res)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                any_sum = p_any.view(seq_len * num_ppl * num_gaussians, res * res).sum(-1)
                logging.debug('p_any max: {:.5f}, min: {:.5f}\n'
                              'max_sum: {:.5f}, min_sum: {:.5f}'.format(
                    p_any.max(), p_any.min(), any_sum.max(), any_sum.min()))

            if local_debug:
                plt.ion()
                for p in range(num_ppl):
                    image = p_any[0, p, 2, :, :]
                    plot = plt.imshow(image.cpu().detach().numpy(), vmax=0.03, vmin=0.0)
                    for f in range(seq_len):
                        image = p_any[f, p, 2, :, :]
                        plot.set_data(image.cpu().detach().numpy())
                        plt.show()
                        plt.pause(0.01)
                    plt.clf()
                    plt.pause(1.0)
        else:
            p_any = torch.zeros(
                seq_len, num_ppl, num_gaussians, res, res, device=device)

        assert torch.isfinite(p_any).all()
        return p_any


def get_model_dict():
    return {
        'simple': SimpleMotionModel,
        'simple_ego': SimpleEgoModel,
        'simple_social': SimpleSocialModel,
        'ego_trajectory': IndividualEgoTrajectoryModel,
        'apg': APGModel,
        'apg_trajectory': APGTrajectoryModel,
        # 'rtog': SocialRTOGModel,
        'cv': ConstantVelocityModel,
        'sfm': SocialForcesModel,
        'continuous': SocialContinuousModel,
    }

def lookup(model_name) -> nn.Module:
    if not isinstance(model_name, str):
        raise TypeError('Expected string for model name lookup')
    try:
        return get_model_dict()[model_name]
    except KeyError:
        raise ValueError('Unknown model type: {}'.format(model_name))


def instantiate_model(model_name, model_config, device=None) -> \
        PedestrianMotionModel:
    model = lookup(model_name)(model_config)
    if device:
        model.to(device)
    return model
