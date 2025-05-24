"""
    Module for a monotonic_weight_kernel.

    TODO: Ensure the standards JSON defaults are set when not specified.

"""



from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from .base import BaseWeightKernel

import numpy as np


# Separate schemas for each type (optional, but recommended for clarity)
TAPER_STYLES = ["rectangle", "hann", "hamming", "blackman"]
ACTIVATION_STYLES = ["sigmoid", "hard_sigmoid", "tanh", "hard_tanh"]

base_attr_dict = get_schema("base_monotonic_weight_kernel", SCHEMA_FN_PATHS)
taper_attr_dict = get_schema("taper_monotonic_weight_kernel", SCHEMA_FN_PATHS)
activation_attr_dict = get_schema("activation_monotonic_weight_kernel", SCHEMA_FN_PATHS)

class BaseMonotonicWeightKernel(BaseWeightKernel):
    """
    MonotonicWeightKernel

    Base class for monotonic weight kernels.
    Handles bounds, normalization, and direction.

    A weighting kernel that applies a monotonic activation/taper function between defined
    lower and upper bounds, based on a given threshold direction.

    There are two main types of monotonic kernels: taper and activation. The taper function
    is used to smoothly transition between the lower and upper bounds, while the activation
    """
    __doc__ = write_lines(base_attr_dict)

    def __init__(self, attr_dict=base_attr_dict, **kwargs):
        super().__init__(attr_dict=base_attr_dict, **kwargs)
        self.weight_type = "monotonic"
#    def __init__(self, **kwargs):
#        # Ensure attr_dict is passed to the parent class
#        super().__init__(attr_dict=base_attr_dict, **kwargs)
        #self.weight_type = "monotonic"
        #self._attr_dict.update(MonotonicWeightKernel._attr_dict)


    def _normalize(self, values):
        lb = float(self.transition_lower_bound)
        ub = float(self.transition_upper_bound)
        direction = self.threshold
        transition_range = ub - lb
        if direction == "low cut":
            return np.clip((values - lb) / transition_range, 0, 1)
        elif direction == "high cut":
            return 1 - np.clip((values - lb) / transition_range, 0, 1)
        else:
            raise ValueError(f"Unknown threshold direction: {direction}")


class TaperMonotonicWeightKernel(BaseMonotonicWeightKernel):
    """
    Handles taper/window styles: rectangle, hann, hamming, blackman.
    """
    __doc__ = write_lines(taper_attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=taper_attr_dict, **kwargs)
        self.weight_type = "taper_monotonic"
    # def __init__(self, **kwargs):
    #     kwargs.pop("attr_dict", None)  # Remove if present
    #     super().__init__(attr_dict=taper_attr_dict, **kwargs)
    #     self.weight_type = "taper_monotonic"

    def evaluate(self, values):
        x = self._normalize(values)
        taper = self.half_window_style
        if taper == "rectangle":
            if self.threshold == "low cut":
                return np.where(values < self.transition_lower_bound, 0.0, 1.0)
            else:
                return np.where(values > self.transition_upper_bound, 0.0, 1.0)
        elif taper == "hann":
            return 0.5 * (1 - np.cos(np.pi * x))
        elif taper == "hamming":
            return 0.54 - 0.46 * np.cos(np.pi * x)
        elif taper == "blackman":
            return 0.42 - 0.5 * np.cos(np.pi * x) + 0.08 * np.cos(2 * np.pi * x)
        else:
            raise ValueError(f"Unsupported taper style: {taper}")

class ActivationMonotonicWeightKernel(BaseMonotonicWeightKernel):
    """
    Handles activation styles: sigmoid, hard_sigmoid, tanh, hard_tanh.

    TODO: Add more testing - this is an experimental class.

    """
    __doc__ = write_lines(activation_attr_dict)
    def __init__(self, steepness: float = 10, **kwargs):
        kwargs.pop("attr_dict", None)  # Remove if present
        super().__init__(attr_dict=activation_attr_dict, **kwargs)
        self.weight_type = "activation_monotonic"
        self.steepness = steepness

    def evaluate(self, values):

        x = self._normalize(values)
        activation_style = self.activation_style
        
        if activation_style == "sigmoid":
            y = 1 / (1 + np.exp(-float(self.steepness) * (x - 0.5)))
        elif activation_style == "hard_sigmoid":
            y = np.clip(0.2 * (x - 0.5) + 0.5, 0, 1)
        elif activation_style == "tanh":
            y = 0.5 * (np.tanh(float(self.steepness) * (x - 0.5)) + 1)
        elif activation_style == "hard_tanh":
            y = np.clip(x, 0, 1)
        else:
            raise ValueError(f"Unsupported activation style: {activation_style}")

        return y
