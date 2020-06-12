from __future__ import print_function, division

import torch
import math
from torch.nn import utils


# def constrain_bivariate_gaussian(params):
    # """ Constrain the parameters to represent valid bivariate gaussian
    
    # Assumes the final dimension has size 5 where the elements correspond to
    # mean_x, mean_y, sigma_x, sigma_y, rho. The stddevs sigma_x, sigma_y are
    # constrained by the exp funciton to ensure they are positive. The
    # correlation coefficient rho is constrained with the tanh funciton to be
    # between -1 and 1. The mean is left unchanged.
    # """
    # # Take a view to collapse leading dimensions
    # params_view = params.view(-1, 5)
    # # Call exp on sigma params
    # params_view[:, 2:4] = params_view[:, 2:4].exp()
    # # Call tanh on rho
    # params_view[:, 4] = params_view[:, 4].tanh()

    # return params


def assert_finite(x):
    assert torch.isfinite(x).all()
    return x

def bivariate_gaussian_loss(params, target):
    """
    Compute the loss given parameters of a bivariate gaussian
    distribution (params) and a target point (target)

    Assumed shape of params is * x 5.
    Where * is any number of leading dimensions and the last dimension
    is comprised of mu_x, mu_y, sigma_x, sigma_y, corr_{xy}

    Assumed shape of target is * x 2.
    Where * is any number of leading dimensions and the last dimension
    is comprised of target_x, target_y

    Returns the loss averaged over all leading dimensions *.
    """
    # epsilon to dodge numerical issues
    epsilon = 1e-10
    # Collapse leading dimensions
    params = params.view(-1, 5)
    target = target.view(-1, 2)

    # Extract individual parameters
    mu_x = params[:, 0]
    mu_y = params[:, 1]
    sigma_x = params[:, 2]
    sigma_y = params[:, 3]
    rho = params[:, 4]  # Correlation rather than covariance
    target_x = target[:, 0]
    target_y = target[:, 1]

    z = ((target_x - mu_x).pow(2) / (sigma_x.pow(2) + epsilon)
         + (target_y - mu_y).pow(2) / (sigma_y.pow(2) + epsilon)
         - 2 * rho * (target_x - mu_x) * (target_y - mu_y)
         / (sigma_x * sigma_y + epsilon))

    assert_finite(z)
    if z.requires_grad:
        z.register_hook(assert_finite)

    p = ((-z / (2 * (1 - rho.pow(2)) + epsilon)).exp()
         / (2 * math.pi * sigma_x * sigma_y * (1 - rho.pow(2) + epsilon).sqrt() + epsilon))

    assert_finite(p)
    if p.requires_grad:
        p.register_hook(assert_finite)
    # Clamping p to a min value avoids crazy high gradients of log function near 0
    # p = torch.clamp(p, min=epsilon)
    p = p + epsilon

    losses = -torch.log(p)

    assert_finite(losses)
    if losses.requires_grad:
        losses.register_hook(assert_finite)

    # Average losses over batch dimension
    return torch.mean(losses, dim=0)
