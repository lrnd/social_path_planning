# Standard imports
from abc import ABC, abstractmethod

# Third party imports
import torch
import torch.nn.functional as F
from torch.distributions import MultivariateNormal

# Local imports
from lstm_motion_model import utils


class OutputTargeter(ABC):
    label = None

    def __init__(self):
        self._dims = None

    @abstractmethod
    def compose_output(self, model_output):
        pass

    @abstractmethod
    def compose_target(self, target):
        pass

    @abstractmethod
    def compute_loss(self, model_output, target):
        pass

    @abstractmethod
    def sample(self, model_output):
        pass

    @abstractmethod
    def expected(self, model_output):
        pass

    @property
    def dims(self):
        return self._dims

    def _check_dims(self, x):
        assert x.shape[-1] == self._dims


class Direct(OutputTargeter):
    label = 'direct'

    def __init__(self, dims=2):
        super().__init__()
        self._dims = dims

    def compose_output(self, model_output):
        self._check_dims(model_output)
        return model_output

    def compose_target(self, target):
        self._check_dims(target)
        return target

    def compute_loss(self, model_output, target):
        assert len(target) == len(model_output)
        self._check_dims(model_output)
        valid_targets = torch.isfinite(target).all(-1)
        return F.mse_loss(model_output[valid_targets], target[valid_targets])

    def sample(self, model_output):
        return self.expected(model_output)

    def expected(self, model_output):
        self._check_dims(model_output)
        return model_output


class BivariateGaussian(OutputTargeter):
    label = 'gaussian'

    def __init__(self, sigma_max = 1.0):
        super().__init__()
        self._dims = 5
        self._sigma_max = sigma_max

    def compose_output(self, model_output):
        """ Constrain the parameters to represent valid bivariate gaussian

        Assumes the final dimension has size 5 where the elements correspond to
        mean_x, mean_y, sigma_x, sigma_y, rho. The stddevs sigma_x, sigma_y are
        constrained by the sigmoid funciton to ensure they are between zero and
        sigma_max. The correlation coefficient rho is constrained with the tanh
        funciton to be between -1 and 1. The mean is left unchanged.
        """
        self._check_dims(model_output)
        # Take a view to collapse leading dimensions
        output_view = model_output.view(-1, 5)
        # Constrain sigma to be between 0 and sigma_max
        output_view[:, 2:4] = output_view[:, 2:4].sigmoid() * self._sigma_max
        # Constrain correlation coefficient (rho) to between -1 and 1
        output_view[:, 4] = output_view[:, 4].tanh()

        return model_output

    def compose_target(self, target):
        self._check_dims(target)
        return target

    def compute_loss(self, model_output, target):
        self._check_dims(model_output)
        assert target.shape[0] == model_output.shape[0]
        # Reshape to treat all dims left of the last as batch dim
        model_output = model_output.view(-1, 5)
        target = target.view(-1, 2)
        assert target.shape[0] == model_output.shape[0]
        # Filter out invalid targets
        valid_targets = torch.isfinite(target).all(-1)
        assert valid_targets.shape[0] == model_output.shape[0]
        model_output = model_output[valid_targets, :]
        target = target[valid_targets, :]
        # There are any frames left compute negative log likelihood of target
        # data given predicted distribution
        if len(target) > 0:
            mu = model_output[:, :2]
            covar = utils.construct_covar_from_params(model_output[..., 2:5])
            scale_tril = torch.cholesky(covar.cpu()).to(device=covar.device)
            dist = MultivariateNormal(mu, scale_tril=scale_tril)
            negative_log_prob = -dist.log_prob(target)
            return torch.mean(negative_log_prob)
        else:
            return None

    def sample(self, model_output):
        self._check_dims(model_output)
        # Establish correct shape for samples output and get flattened views
        device = model_output.device
        sample_shape = model_output.shape[:-1] + (2,)
        samples = torch.empty(sample_shape, device=device)
        samples_view = samples.view(-1, 2)
        params_view = model_output.view(-1, 5)

        # Draw independent normal samples
        normal = torch.randn_like(samples_view)

        normal_x = normal[:, 0]
        normal_y = normal[:, 1]
        mu_x = params_view[:, 0]
        mu_y = params_view[:, 1]
        sigma_x = params_view[:, 2]
        sigma_y = params_view[:, 3]
        rho = params_view[:, 4]  # Correlation rather than covariance

        # Generate correlated samples
        samples_view[:, 0] = (mu_x + sigma_x * normal_x)
        samples_view[:, 1] = (mu_y + sigma_y
                              * (normal_x * rho + normal_y * (1. - rho**2)**0.5))
        return samples

    def expected(self, model_output):
        self._check_dims(model_output)
        return model_output[..., :2]


class Histogram(OutputTargeter):
    label = 'histogram'

    def __init__(self, resolution, radius):
        super().__init__()
        self._resolution = resolution
        self._dims = resolution**2
        self._radius = radius

    def compose_output(self, model_output):
        self._check_dims(model_output)
        return F.log_softmax(model_output, dim=-1)

    def compose_target(self, target):
        index = utils.point_to_index(target, grid_length=2 * self._radius,
                                     grid_resolution=self._resolution,
                                     flatten_index=True)
        return index

    def compute_loss(self, model_output, target):
        self._check_dims(model_output)
        return F.nll_loss(model_output.view(-1, self._dims), target.view(-1))

    def sample(self, model_output):
        """Convert histograms into velocities/displacements according to
        model config
        """
        self._check_dims(model_output)
        dist = torch.distributions.Categorical(logits=model_output)
        index = dist.sample().unsqueeze(-1)
        index = utils.unflatten_2d_index(index)
        point = self.grid_idx_to_2d_point(index)
        return point

    def expected(self, model_output):
        self._check_dims(model_output)
        index = model_output.argmax(dim=-1, keepdim=True)
        index = self._unflatten_2d_index(index)
        point = self._grid_idx_to_2d_point(index)
        return point

    def _unflatten_2d_index(self, index):
        """Convert 1 dimensional index to 2d grid index given grid dims

        Expects final dim of size 1 and replaces it with dim of size 2
        """
        input_shape = index.shape
        if input_shape[-1] != 1:
            raise ValueError('Expected final dimension to be 1 but it was {}'
                             .format(input_shape[-1]))
        index = index.view(-1)
        invalid_idx = index == -100
        unflat_index = torch.stack((index // self._resolution, index %
                                    self._resolution), dim=-1)
        unflat_index[invalid_idx, :] = -100
        return unflat_index.view(input_shape[:-1] + (2,))

    def _grid_idx_to_2d_point(self, grid_idx):
        input_shape = grid_idx.shape
        if input_shape[-1] != 2:
            raise ValueError(
                'Final dimension of grid_idx should be 2 but was {}'
                .format(input_shape[-1]))
        grid_idx = grid_idx.to(torch.float).view(-1, 2)
        point = (self._radius * (2.0 * grid_idx - self._resolution + 1)
                 / self._resolution)
        return point.view(input_shape)


def create(name, kwargs) -> OutputTargeter:
    targeters = [
        Direct,
        BivariateGaussian,
        Histogram,
    ]
    index = {t.label: t for t in targeters}
    return index[name](**kwargs)
