import numpy as np
from matplotlib import pyplot as plt, animation

import lstm_motion_model.utils
from lstm_motion_model import datasets, utils
from matplotlib.patches import Ellipse
import torch


def create_plot_from_dict(plot_dict, config=None):
    # Add new plot classes here
    possible_plots = [
        PathPredictionPlot,
        GridPredictionPlot,
        Scatter2dPlot,
        GaussianPredictionPlot,
    ]

    if isinstance(plot_dict, dict):
        print(plot_dict.keys())
        for Plot in possible_plots:
            if any(all(key in plot_dict for key in keys)
                   for keys in Plot.expected_keys):
                print('Plot type: ' + Plot.__name__)
                # try:
                p = Plot(plot_dict)
                yield p
                # except Exception as e:
                #     print(e)
                # plot_list.append(Plot(plot_dict))
        # return plot_list
    else:
        raise TypeError('Expected dictionary but got {}'.format(
            plot_dict.__class__))
    print('No more plots')


class ResultPlot:
    '''A public interface for plots to be extended by actual plots'''

    # List of list of expected keys in the result_data passed to init
    # Each list is an alternative set of keys
    # All elements of any inner list must be present to use the class
    expected_keys = [[None]]

    def __init__(self):
        self._fig = None

    def draw(self):
        raise NotImplementedError


class AnimatedResultPlot(ResultPlot):
    '''A base class for animated plots'''

    expected_keys = [None]

    def __init__(self):
        super().__init__()
        self.interval = 100

    def draw(self):
        self._draw_animation()
        self._play_animation()

    def _play_animation(self):
        ani = animation.FuncAnimation(
            self._fig,
            self._update_animation,
            enumerate(self._plot_data),
            interval=self.interval,
            blit=True)
        plt.show()

    def _draw_animation(self):
        raise NotImplementedError

    def _update_animation(self):
        raise NotImplementedError


class Scatter2dPlot(ResultPlot):

    expected_keys = [['displacement']]

    def __init__(self, result_data):
        self._plot_x = result_data['displacement'][..., 0].numpy()
        self._plot_y = result_data['displacement'][..., 1].numpy()

    def draw(self):
        plt.scatter(self._plot_x, self._plot_y, s=1)
        plt.grid()
        # plt.axis
        plt.show()


class PlotGroundTruth(AnimatedResultPlot):

    expected_keys = [['true_position', 'position']]

    def __init__(self, result_data):
        super().__init__()
        self._ax = None
        self._plot_data = []
        self._plots = []
        self._xlims = np.array([np.inf, -np.inf])
        self._ylims = np.array([np.inf, -np.inf])

        true_positions = result_data['true_position'].cpu().numpy()
       # predicted_positions = result_data['position'].cpu().numpy()

        # Check that the critical dimensions match
       # assert true_positions.shape[0:2] == predicted_positions.shape[0:2]

        # Handle trajectory predictions by squeezing out the recursive
        # inference dimension
       # if (len(predicted_positions.shape) == 5
       #         and predicted_positions.shape[2] == 1):
       #     predicted_positions = predicted_positions.squeeze(2)

       # assert true_positions.shape[2] == predicted_positions.shape[3]
        #num_frames, self._num_people, pred_length, dims =\
        #    predicted_positions.shape
        num_frames, self._num_people, dims =\
            true_positions.shape

        assert dims == 2

        #for idx, pred_sequence in enumerate(predicted_positions):
        #    # Avoid plotting past the end of the ground truth
        #    if idx + pred_length > num_frames:
        #        true_length = num_frames - idx
        #    else:
        #        true_length = pred_length + 1

        true_sequence = (true_positions[idx:idx + true_length, :, :]
                             .transpose((1, 0, 2)))
        #    pred_plot_seq = np.concatenate(
        #        (true_sequence[:, 0, :].reshape(self._num_people, 1, dims),
        #         pred_sequence), axis=1)
        self._plot_data.append({'true': true_sequence})
                                  #  'pred': pred_plot_seq})
        self._update_plot_lims(true_sequence.reshape(-1, dims))
            #self._update_plot_lims(pred_plot_seq.reshape(-1, dims))

    def _update_plot_lims(self, sequence):
        frames, dims = sequence.shape
        assert frames >= 1
        assert dims == 2

        xmin = np.nanmin(sequence[:, 0])
        xmax = np.nanmax(sequence[:, 0])

        ymin = np.nanmin(sequence[:, 1])
        ymax = np.nanmax(sequence[:, 1])

        self._xlims[0] = min(self._xlims[0], xmin)
        self._xlims[1] = max(self._xlims[1], xmax)

        self._ylims[0] = min(self._ylims[0], ymin)
        self._ylims[1] = max(self._ylims[1], ymax)

    def _draw_animation(self):
        self._fig, self._ax = plt.subplots()
        self._plots = []

        for person in range(self._num_people):
        #robot is added on to end of ped_seq
            if(person < self._num_people -1):
                marker, = self._ax.plot(
                    [], [], 'o', linewidth=3.0, color='grey')
            else:
                marker, = self._ax.plot(
                    [], [], 'o', linewidth=3.0, color='red')
            truth, = self._ax.plot(
                [], [], ':', linewidth=2.0, color=marker.get_color())
            self._plots.append((marker, truth))

        self._ax.axis('equal')
        self._ax.set_xlim(self._xlims)
        self._ax.set_ylim(self._ylims)

    def _update_animation(self, frame):
        frame_idx, frame_data = frame
        for plot, true in zip(
                self._plots, frame_data['true']):
            plot[0].set_data(true[0, 0], true[0, 1])
            plot[1].set_data(true[:, 0], true[:, 1])
            #plot[2].set_data(pred[:, 0], pred[:, 1])

        return [artist for person in self._plots for artist in person]


class PathPredictionPlot(AnimatedResultPlot):

    expected_keys = [['true_position', 'position']]

    def __init__(self, result_data):
        super().__init__()
        self._ax = None
        self._plot_data = []
        self._plots = []
        self._xlims = np.array([np.inf, -np.inf])
        self._ylims = np.array([np.inf, -np.inf])

        true_positions = result_data['true_position'].cpu().numpy()
        predicted_positions = result_data['position'].cpu().numpy()

        # Check that the critical dimensions match
        print (true_positions.shape[0:2])
        print(predicted_positions.shape[0:2])
        assert true_positions.shape[0:2] == predicted_positions.shape[0:2]

        # Handle trajectory predictions by squeezing out the recursive
        # inference dimension
        if (len(predicted_positions.shape) == 5
                and predicted_positions.shape[2] == 1):
            predicted_positions = predicted_positions.squeeze(2)

        assert true_positions.shape[2] == predicted_positions.shape[3]
        num_frames, self._num_people, pred_length, dims =\
            predicted_positions.shape

        for idx, pred_sequence in enumerate(predicted_positions):
            # Avoid plotting past the end of the ground truth
            if idx + pred_length > num_frames:
                true_length = num_frames - idx
            else:
                true_length = pred_length + 1

            true_sequence = (true_positions[idx:idx + true_length, :, :]
                             .transpose((1, 0, 2)))
            pred_plot_seq = np.concatenate(
                (true_sequence[:, 0, :].reshape(self._num_people, 1, dims),
                 pred_sequence), axis=1)
            self._plot_data.append({'true': true_sequence,
                                    'pred': pred_plot_seq})
            self._update_plot_lims(true_sequence.reshape(-1, dims))
            self._update_plot_lims(pred_plot_seq.reshape(-1, dims))

    def _update_plot_lims(self, sequence):
        frames, dims = sequence.shape
        assert frames >= 1
        assert dims == 2

        xmin = np.nanmin(sequence[:, 0])
        xmax = np.nanmax(sequence[:, 0])

        ymin = np.nanmin(sequence[:, 1])
        ymax = np.nanmax(sequence[:, 1])

        self._xlims[0] = min(self._xlims[0], xmin)
        self._xlims[1] = max(self._xlims[1], xmax)

        self._ylims[0] = min(self._ylims[0], ymin)
        self._ylims[1] = max(self._ylims[1], ymax)

    def _draw_animation(self):
        self._fig, self._ax = plt.subplots()
        self._plots = []

        for person in range(self._num_people):
        #robot is added on to end of ped_seq
            #if(person < self._num_people -1):
            #    marker, = self._ax.plot(
            #        [], [], 'o', linewidth=3.0, color='grey')
            #else:
            marker, = self._ax.plot(
                    [], [], 'o', linewidth=3.0)
            predicted, = self._ax.plot(
                [], [], '-', linewidth=2.0, color=marker.get_color())
            truth, = self._ax.plot(
                [], [], ':', linewidth=2.0, color=marker.get_color())
            self._plots.append((marker, truth, predicted))

        self._ax.axis('equal')
        self._ax.set_xlim(self._xlims)
        self._ax.set_ylim(self._ylims)

    def _update_animation(self, frame):
        frame_idx, frame_data = frame
        for plot, true, pred in zip(
                self._plots, frame_data['true'], frame_data['pred']):
            plot[0].set_data(true[0, 0], true[0, 1])
            plot[1].set_data(true[:, 0], true[:, 1])
            plot[2].set_data(pred[:, 0], pred[:, 1])

        return [artist for person in self._plots for artist in person]


class GaussianPredictionPlot(AnimatedResultPlot):

    expected_keys = [['true_position', 'displacement_gaussian']]

    def __init__(self, result_data):
        super().__init__()
        self._ax = None
        self._plot_data = []
        self._plots = []
        self._xlims = np.array([np.inf, -np.inf])
        self._ylims = np.array([np.inf, -np.inf])

        # TODO: How to set this?
        pred_length = 5

        true_positions = result_data['true_position'][1:].cpu()
        predicted_gaussians = result_data['displacement_gaussian'].cpu()

        prediction_shape = predicted_gaussians.shape
        if len(prediction_shape) == 5:
            seq_len, self._num_people, num_pred_frames, self._num_gaussians, num_params = prediction_shape
            predicted_gaussians = predicted_gaussians[:, :, 0, :, :]
            # assert num_pred_frames == 1
        elif len(prediction_shape) == 4:
            seq_len, self._num_people, num_pred_frames, num_params = prediction_shape
            predicted_gaussians = predicted_gaussians[:, :, 0, :]
            # assert num_pred_frames == 1
            self._num_gaussians = 1
            predicted_gaussians = predicted_gaussians.view(
                seq_len, self._num_people, self._num_gaussians, num_params)

        assert num_params == 5
        # Check that the critical dimensions match
        seq_len_2, num_people_2, dims = true_positions.shape
        assert dims == 2
        assert seq_len == seq_len_2
        assert self._num_people == num_people_2

        for idx, pred_gaussian in enumerate(predicted_gaussians):
            # Avoid plotting past the end of the ground truth
            if idx + pred_length > seq_len:
                true_length = seq_len - idx
            else:
                true_length = pred_length + 1

            true_sequence = torch.stack(
                true_positions[idx:idx + true_length, :, :].unbind(1))

            ellipse_params = []
            for p_idx, person in enumerate(pred_gaussian):
                ellipse_params.append([])
                for gaussian in person:

                    if torch.all(torch.isfinite(gaussian)):
                        mu = gaussian[0:2]
                        sigma_x = gaussian[2]
                        sigma_y = gaussian[3]
                        rho = gaussian[4]  # Correlation rather than covariance

                        var_x = sigma_x.pow(2)
                        var_y = sigma_y.pow(2)
                        cov_xy = rho * sigma_x * sigma_y
                        covar = torch.tensor([[var_x, cov_xy], [cov_xy, var_y]])

                        eig_val, eig_vec = covar.symeig()
                        theta = np.degrees(torch.atan2(
                            eig_vec[:, 0][1], eig_vec[:, 0][0]))
                        w, h = 4 * eig_val.sqrt()
                        center = true_positions[idx, p_idx, :] + mu
                        ellipse_params[-1].append({
                            'width': w.numpy(),
                            'height': h.numpy(),
                            'angle': theta.numpy(),
                            'center': center.numpy(),
                        })
                    else:
                        ellipse_params[-1].append({
                            'width': np.nan,
                            'height': np.nan,
                            'angle': np.nan,
                            'center': [np.nan, np.nan]
                        })

            self._plot_data.append({'true': true_sequence,
                                    'pred': ellipse_params})
            self._update_plot_lims(true_sequence.view(-1, dims))

    def _update_plot_lims(self, sequence):
        frames, dims = sequence.shape
        assert frames >= 1
        # assert dims == 2

        xmin = np.nanmin(sequence[:, 0])
        xmax = np.nanmax(sequence[:, 0])

        ymin = np.nanmin(sequence[:, 1])
        ymax = np.nanmax(sequence[:, 1])

        self._xlims[0] = min(self._xlims[0], xmin)
        self._xlims[1] = max(self._xlims[1], xmax)

        self._ylims[0] = min(self._ylims[0], ymin)
        self._ylims[1] = max(self._ylims[1], ymax)

    def _draw_animation(self):
        self._fig, self._ax = plt.subplots()
        self._plots = []

        for person in range(self._num_people):
            marker, = self._ax.plot(
                [], [], 'o', linewidth=3.0)
            true_path, = self._ax.plot(
                [], [], '.', linewidth=0.5, color=marker.get_color())
            self._plots.append({
                'marker': marker,
                'true_path': true_path,
                'ellipse': [],
            })
            for i in range(self._num_gaussians):
                ellipse = self._ax.add_patch(
                    Ellipse(xy=[0.0, 0.0], width=0.0, height=0.0,
                            fc='none', ec=marker.get_color()))
                self._plots[-1]['ellipse'].append(ellipse)

        self._ax.axis('equal')
        self._ax.set_xlim(self._xlims)
        self._ax.set_ylim(self._ylims)

    def _update_animation(self, frame):
        frame_idx, frame_data = frame
        artists = []
        for plot, true, pred in zip(
                self._plots, frame_data['true'], frame_data['pred']):
            if torch.any(torch.isfinite(true)):
                plot['marker'].set_data(true[0, 0], true[0, 1])
                plot['true_path'].set_data(true[:, 0], true[:, 1])
                artists.append(plot['marker'])
                artists.append(plot['true_path'])
                for i, gaussian in enumerate(pred):
                    plot['ellipse'][i].width = gaussian['width']
                    plot['ellipse'][i].height = gaussian['height']
                    plot['ellipse'][i].angle = gaussian['angle']
                    plot['ellipse'][i].center = gaussian['center']
                    artists.append(plot['ellipse'][i])

        return artists


class GridPredictionPlot(AnimatedResultPlot):

    expected_keys = [
        ['displacement_histogram'],
        ['glb_ind_rtog'],
        ['displacement_grid'],
        ['displacement_grid_idx'],
        ['local_rtog'],
        ['local_rtog_idx'],
        ['local_grid'],
        ['local_grid_idx'],
    ]

    def __init__(self, result_data):
        super().__init__()
        sum_people = False
        self._plot_data = []
        self._plots = []
        self._expected_keys = [k for l in self.expected_keys for k in l]

        grids = None
        convert_from_idx = False
        for k, v in result_data.items():
            if k in self._expected_keys:
                convert_from_idx = (k.find('idx') != -1)
                grids = v
                break

        if convert_from_idx:
            grids = utils.unflatten_2d_index(grids, result_data['resolution'])
            grids = lstm_motion_model.utils.index_to_grid(grids, result_data['resolution'])

        shape = grids.shape
        dims = len(shape)
        if dims == 5:
            (sequence_length, num_people, channels,
                self._grid_size_a, self._grid_size_b) = shape
        elif dims == 4:
            (sequence_length, num_people,
                self._grid_size_a, self._grid_size_b) = shape
            channels = 1
            grids = grids.unsqueeze(2)
        else:
            raise ValueError('Not sure how to plot grid data with {} '
                             'dimensions'.format(dims))

        for frame_idx in range(sequence_length - 1):
            if channels >= 3:
                frame_grids = grids[frame_idx, :, :3, :, :]
            elif channels == 1:
                frame_grids = grids[frame_idx, :, :, :, :]
            else:
                raise ValueError('Don\'t know how to draw two channel images')

            if sum_people:
                frame_grids = frame_grids.sum(dim=0, keepdim=True)
                value_scale = 2.0
            else:
                value_scale = 2.0

            if frame_grids.shape[1] > 1:
                image = frame_grids.numpy().copy().transpose(0, 2, 3, 1)
            else:
                image = frame_grids.squeeze(dim=1).cpu().numpy().copy()

            # TODO: Switch this
            # image = np.exp(image)

            # for channel in range(3):
                # image[:, :, channel] = image[:, :, channel] / image[:, :, channel].max()
            image = image * value_scale
            # image[image > 1.0] = 1.0
            # print("min {}  max {}".format(image.min(), image.max()))
            # print('min:{}  max:{}'.format(image.min(), image.max()))
            # print('min:{}  max:{}'.format(image.min(), image.max()))
            self._plot_data.append({
                'true': [],
                'pred': image})
            # for person_idx in range(num_people):
                # plot_data[-1]['true'].append(
                    # true[frame_idx:truth_end, person_idx, :])

        # fig = plt.figure()
        # plots = []
        # for person in range(num_people):
            # marker, = plt.plot([], [], 'o', linewidth=3.0)
            # truth, = plt.plot([], [], '-', linewidth=2.0,
                              # color=marker.get_color())
            # plots.append((marker, truth))

        # grid_plot = plt.imshow(
            # np.zeros((grid_resolution, grid_resolution, 3)),
            # interpolation='gaussian')

    def _draw_animation(self):
        num_plots = len(self._plot_data[0]['pred'])
        if num_plots == 1:
            self._fig = plt.figure()
            self._ax = self._fig.subplots(1, 1)
        elif num_plots > 1:
            self._fig = plt.figure()
            self._ax = self._fig.subplots(4, 4)
        else:
            raise ValueError('Zero plots!')

        if not isinstance(self._ax, np.ndarray):
            self._ax = np.array([self._ax])
        for ax in self._ax.flatten():
            self._plots.append(
                ax.imshow(np.zeros((self._grid_size_a, self._grid_size_b, 3)), vmin=0.0, vmax=1.0))#,
                # interpolation='gaussian'))
            ax.set_xticks([])
            ax.set_yticks([])
        # self._text = self._fig.text(0.5, 0.05, '')

    def _update_animation(self, frame):
        frame_idx, frame_data = frame
        print(frame_idx)
        # self._text.set_text(str(frame_idx))
        for person in range(min(len(frame_data['pred']), len(self._plots))):
            self._plots[person].set_data(frame_data['pred'][person])
            # print("min {}  max {}".format(frame_data['pred'][person].min(), frame_data['pred'][person].max()))
        return self._plots
