"""
    Module for a monotonic_weight_kernel.

    TODO: Ensure the standards JSON defaults are set when not specified.

"""



from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from .base import BaseWeightKernel

import numpy as np

attr_dict = get_schema("monotonic_weight_kernel", SCHEMA_FN_PATHS)


class MonotonicWeightKernel(BaseWeightKernel):
    """
    MonotonicWeightKernel

    A weighting kernel that applies a monotonic activation/taper function between defined
    lower and upper bounds, based on a given threshold direction.
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        # Ensure attr_dict is passed to the parent class
        super().__init__(attr_dict=attr_dict, **kwargs)
        self.weight_type = "monotonic"
        #self._attr_dict.update(MonotonicWeightKernel._attr_dict)
        
    def evaluate(self, values):
        """
        Evaluate the monotonic kernel on the input feature values.

        Parameters
        ----------
        values : float or np.ndarray
            The input values of the feature (e.g., coherence) to apply the kernel to.

        Returns
        -------
        weights : float or np.ndarray
            Weight(s) between 0 and 1.
        """

        lb = self.transition_lower_bound
        ub = self.transition_upper_bound
        taper = self.half_window_style
        direction = self.threshold

        # Normalize feature to [0, 1] across transition region
        if direction == "low cut":
            x = np.clip((values - lb) / (ub - lb), 0, 1)
        elif direction == "high cut":
            x = 1 - np.clip((values - lb) / (ub - lb), 0, 1)
        else:
            raise ValueError(f"Unknown threshold direction: {direction}")

        # Activation/taper functions
        if taper == "rectangle":
            return np.where((x >= 0) & (x <= 1), 1.0, 0.0)
        elif taper == "hann":
            return 0.5 * (1 - np.cos(np.pi * x))
        elif taper == "hamming":
            return 0.54 - 0.46 * np.cos(np.pi * x)
        elif taper == "blackman":
            return 0.42 - 0.5 * np.cos(np.pi * x) + 0.08 * np.cos(2 * np.pi * x)
        elif taper == "sigmoid":
            # Steepness can be parameterized if desired
            return 1 / (1 + np.exp(-10 * (x - 0.5)))
        elif taper == "hard_sigmoid":
            return np.clip(0.2 * (x - 0.5) + 0.5, 0, 1)
        elif taper == "tanh":
            return 0.5 * (np.tanh(5 * (x - 0.5)) + 1)
        elif taper == "hard_tanh":
            return np.clip(x, 0, 1)
        else:
            raise ValueError(f"Unsupported taper style: {taper}")

