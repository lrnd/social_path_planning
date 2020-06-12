from __future__ import print_function, division

import math

import numpy as np
import torch
import torch.nn.functional as F


def translate_and_scale_image(src, offset, old_radius, new_radius, new_resolution):
    # scale is new image radius / old_image radius
    scale = new_radius / old_radius

    # Check shape of src_rtog and offset
    n, c, h, w = src.shape
    n_offsets, dims = offset.shape
    assert(h == w)
    assert(c >= 1)
    assert(h >= 1)
    assert(h % 2 == 0)
    assert(n == n_offsets)
    assert(dims == 2)

    # Generate affine transform matrix per n
    theta = torch.zeros(n, 2, 3)
    theta[:, 0, 0] = scale
    theta[:, 1, 1] = scale
    # Offset from position scaled by original radius
    theta[:, 0, 2] = offset[:, 0] / old_radius
    theta[:, 1, 2] = offset[:, 1] / old_radius
    # Create flow grid with transform and new size
    grid_size = torch.Size((n, c, new_resolution, new_resolution))
    flow_grid = F.affine_grid(theta, grid_size)

    return F.grid_sample(src, flow_grid)


def flatten_2d_index(index, n, m=None):
    input_shape = index.shape
    if m is None:
        m = n
    if input_shape[-1] != 2:
        raise ValueError('Expected final dimension to be 2 but it was {}'
            .format(input_shape[-1]))
    index = index.view(-1, 2)
    invalid_idx = (index == -100).any(-1)
    index = index[:, 0] * m + index[:, 1]
    index[invalid_idx] = -100
    return index.view(input_shape[:-1] + (1,))


def unflatten_2d_index(index, n, m=None):
    '''Convert 1 dimensional index to 2d grid index given grid dims

    Expects final dim of size 1 and replaces it with dim of size 2
    '''
    input_shape = index.shape
    if m is None:
        m = n
    if input_shape[-1] != 1:
        raise ValueError('Expected final dimension to be 1 but it was {}'
            .format(input_shape[-1]))
    index = index.view(-1)
    invalid_idx = index == -100
    unflat_index = torch.stack((index // m, index % m), dim=-1)
    unflat_index[invalid_idx, :] = -100
    return unflat_index.view(input_shape[:-1] + (2,))


def grid_transform(src_grid, offset, old_radius, new_radius,
                   new_resolution):
    # Check shape of src_grid and offset
    n, c, h, w = src_grid.shape
    n_offsets, dims = offset.shape
    assert(h == w)
    assert(c >= 1)
    assert(h >= 1)
    assert(h % 2 == 0)
    assert(n == n_offsets)
    assert(dims == 2)

    scale = new_radius / old_radius
    # Generate affine transform matrix per n
    theta = torch.zeros(n, 2, 3)
    theta[:, 0, 0] = scale
    theta[:, 1, 1] = scale
    # Offset from position scaled by original radius
    theta[:, 0, 2] = -offset[:, 1] / old_radius
    theta[:, 1, 2] = -offset[:, 0] / old_radius
    # Create flow grid with transform and new size
    grid_size = torch.Size((n, c, new_resolution, new_resolution))
    flow_grid = F.affine_grid(theta, grid_size).to(src_grid.device)

    return F.grid_sample(src_grid, flow_grid, mode='bilinear')


def rotate_2d(x, theta):
    input_shape = x.shape
    rotation = angle_to_rotation_matrix(theta)
    x_rotated = torch.matmul(rotation, x.reshape(-1, 2, 1))
    return x_rotated.view(input_shape)


def rotate_2d_covariance(covariance, theta):
    input_shape = covariance.shape
    rotation = angle_to_rotation_matrix(theta)
    covariance_rotated = torch.matmul(torch.matmul(
        rotation, covariance.reshape(-1, 2, 2)), rotation.transpose(0, 1))
    return covariance_rotated.view(input_shape)


def angle_to_rotation_matrix(theta):
    c = torch.cos(theta.reshape(-1))
    s = torch.sin(theta.reshape(-1))
    rotation_matrix = torch.stack([
        torch.stack([c, -s], dim=-1),
        torch.stack([s, c], dim=-1)], dim=-2)
    return rotation_matrix


def construct_covar_from_params(params, min_var=1e-8):
    sigma = params[..., 0:2]
    rho = params[..., 2]
    var = sigma.pow(2) + min_var
    cov_xy = rho * sigma[..., 0] * sigma[..., 1]
    covar = torch.stack([var[..., 0], cov_xy, cov_xy, var[..., 1]], dim=-1)
    covar = covar.view(covar.shape[:-1] + (2, 2))
    return covar


def extrapolate_nans_in_seq(seq):
    for person_idx in range(seq.shape[1]):
        for dim_idx in range(seq.shape[2]):
            extrapolate_nans_1d(seq[:, person_idx, dim_idx].view(-1))


def extrapolate_nans_1d(seq):
    dtype = seq.dtype
    device = seq.device
    if len(seq.shape) != 1:
        raise ValueError('Expected input with single dimension')
    valid = torch.nonzero(~torch.isnan(seq))
    if len(valid) < 2:
        print(len(valid))
        raise ValueError('Not enough vaild data points')
    if valid[0] > 0:
        delta = seq[valid[1]] - seq[valid[0]]
        offset = seq[valid[0]]
        nan_length = int(valid[0])
        seq[:valid[0]] = offset + torch.arange(
            start=-nan_length, end=0, step=1, dtype=dtype, device=device) * delta
    if valid[-1] < (len(seq) - 1):
        delta = seq[valid[-2]] - seq[valid[-1]]
        offset = seq[valid[-1]]
        nan_length = int((len(seq) - 1) - valid[-1])
        seq[valid[-1] + 1:] = offset + torch.arange(
            start=0, end=nan_length, step=1, dtype=dtype, device=device) * delta


class LossMonitor(object):

    def __init__(self, patience=10, threshold=1e-4):
        self.threshold = threshold
        self.rel_epsilon = 1.0 - threshold
        self.patience = patience
        self.stall_counter = 0
        self.min = float('inf')

    def reset(self):
        self.stall_counter = 0
        self.min = float('inf')

    def step(self, loss):
        loss = float(loss)
        if loss < self.min * self.rel_epsilon:
            self.min = loss
            self.stall_counter = 0
        else:
            self.stall_counter += 1
        return self.patience - self.stall_counter

    def stalled(self):
        if self.stall_counter >= self.patience:
            return True
        else:
            return False


def random_rotate_tensor(x):
    '''Rotate a tensor of x,y points about the origin by a random angle.

    Accepts any tensor who's final dimension has a size of 2. All leading
    dimensions are collapsed prior to the rotation and restored afterwards.
    '''
    original_shape = x.shape
    if original_shape[-1] != 2:
        raise ValueError('Can only rotate x if last dimension has size 2')
    # Generate random angle between 0 and 2pi
    theta = torch.empty(1, 1, device=x.device).uniform_(0, 2 * math.pi)
    # Create 2d rotation matrix
    # Constructed as a transpose of the typical case to fit shape of the tensor
    rotm = torch.cat((torch.cat((torch.cos(theta), torch.sin(theta)), dim=1),
                      torch.cat((-torch.sin(theta), torch.cos(theta)), dim=1)
                      ), dim=0)
    return torch.mm(x.view(-1, 2), rotm).view(*original_shape)


def random_offset_tensor(x, lower=-1.0, upper=1.0):
    '''Offset a tensor of x,y points by a random vector.

    Accepts any tensor who's final dimension has a size of 2. All leading
    dimensions are collapsed prior to the rotation and restored afterwards.
    '''
    original_shape = x.shape
    if original_shape[-1] != 2:
        raise ValueError('Can only rotate x if last dimension has size 2')
    # Generate offset
    offset = torch.empty(2, device=x.device).uniform_(lower, upper)

    return (x.view(-1, 2) + offset).view(*original_shape)


def random_flip_tensor(x):
    '''Flip a tensor of x,y points about the x and/or y axis randomly

    Accepts any tensor who's final dimension has a size of 2. All leading
    dimensions are collapsed prior to the flip and restored afterwards.
    '''
    original_shape = x.shape
    if original_shape[-1] != 2:
        raise ValueError('Can only rotate x if last dimension has size 2')

    flip = torch.bernoulli(torch.tensor([0.5, 0.5])).to(torch.bool)
    coef = torch.ones(2, device=x.device)
    coef[flip] = -1
    return x * coef


def pos_seq_to_relative_indices(x, start, stop, grid_radius, grid_resolution,
                                frame_offsets, flatten_index=False):
    num_frames, num_people, dims = x.shape
    assert(dims == 2)
    relative_positions = []
    for offset in frame_offsets:
        relative_positions.append(
            x[start + offset:stop + offset] - x[start:stop])
    relative_positions = torch.stack(relative_positions, dim=2)
    indices = point_to_index(x=relative_positions, grid_length=2 * grid_radius,
                             grid_resolution=grid_resolution,
                             flatten_index=flatten_index)
    return indices


def point_to_grid(x, grid_length=2.0, grid_resolution=10,
                  grid_centre=None):
    '''Convert tensor of continuous 2d points into tensor of occupancy grids.

    Accepts any tensor who's final dimension has a size of 2. The final tensor
    dimension of 2 is replaced by two dimensions of size grid_resolution.
    [*, 2] -> [*, grid_resolution, grid_resolution]
    ...where * is any number of leading dimensions
    '''
    indices = point_to_index(x, grid_length, grid_resolution, grid_centre)
    grids = index_to_grid(indices, grid_resolution)
    return grids


def point_to_index(x, grid_length=2.0, grid_resolution=10,
                   grid_centre=None, flatten_index=False):
    '''Convert tensor of 2d points into tensor of 2d grid indices.

    Accepts any tensor who's final dimension has a size of 2. The output
    tensor has the same dimensions by default. If flatten_index=True
    then the 2d grid indices ix, iy are flattened to single indices i
    such that grid[ix, iy] == grid.view(-1)[i]. The final dimension is
    therefore removed.
    [*, 2] -> [*]
    ...where * is any number of leading dimensions
    '''
    dev = x.device
    if grid_centre is None:
        grid_centre = torch.tensor((0.0, 0.0), device=dev)
    x_shape = x.shape
    if x_shape[-1] != 2:
        raise ValueError('Can only work if last dimension of x has size 2')
    if not isinstance(grid_centre, torch.Tensor) or grid_centre.shape != (2,):
        raise ValueError('grid_centre must be a tensor with shape (2,)')
    # Centre the points around grid_centre
    x_centred = x - grid_centre
    # Define bins for the grid, shared for x and y
    bins = np.linspace(
        -0.5 * grid_length,
        0.5 * grid_length,
        grid_resolution + 1)

    # Copy points to cpu and compute to discrete indices in numpy
    indices_np = np.digitize(x_centred.cpu().detach().numpy(), bins)
    outside_grid = np.logical_or(indices_np == 0, indices_np == len(bins))
    indices_np = indices_np - 1
    indices_np[outside_grid] = -100

    # Bring back to torch tensor and move to device
    indices = torch.from_numpy(indices_np).to(dev)
    # Handle out of range indices
    # TODO: Should ignore bad indices rather than cap them
    # indices[indices >= grid_resolution] = grid_resolution - 1
    # indices[indices < 0] = 0
    if flatten_index:
        x_idx = indices.index_select(-1, torch.tensor(0, device=dev))
        y_idx = indices.index_select(-1, torch.tensor(1, device=dev))
        invalid_idx = (x_idx == -100) | (y_idx == -100)
        indices = x_idx * grid_resolution + y_idx
        indices[invalid_idx] = -100

    return indices


def index_to_grid(x, grid_resolution=10):
    '''Convert tensor of 2d grid indices into tensor of occupancy grids.

    Accepts any tensor who's final dimension has a size of 2. The final tensor
    dimension of 2 is replaced by two dimensions of size grid_resolution.
    [*, 2] -> [*, grid_resolution, grid_resolution]
    ...where * is any number of leading dimensions
    '''
    x_shape = x.shape
    ind_view = x.view(-1, 2)
    valid_ind = (ind_view >= 0).all(-1)
    # Allocate empty grids with leading dims based on x
    grids = torch.zeros(
        x_shape[:-1] + (grid_resolution, grid_resolution), device=x.device)
    # Get view with leading dims flattened
    grids_view = grids.view(-1, grid_resolution, grid_resolution)
    # Set 1.0 for correct cell in each grid
    grids_view[
        valid_ind,
        ind_view[valid_ind, 0],
        ind_view[valid_ind, 1]] = 1.0
    return grids

def create_obstacle_list(ped_seq, radius):
    '''creates a list of obstacles (x, y, radius)
    from positions of pedestians at time of call for use in path planning 
    ped_seq is one sequence of (num_ped, dims)
    '''
    obstacles = []
    num_ped, dims = ped_seq.shape
    print("ped-seq", ped_seq)
    if dims != 2:
        raise Exception("incorrect number of dimensions")
    for ped in ped_seq:
        obstacle = np.append(ped[0], ped[1], radius)
        obstacles.append(obstacle)
    return obstacles



