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

base_attr_dict = get_schema("monotonic_weight_kernel", SCHEMA_FN_PATHS)
taper_attr_dict = get_schema("taper_monotonic_weight_kernel", SCHEMA_FN_PATHS)
activation_attr_dict = get_schema("activation_monotonic_weight_kernel", SCHEMA_FN_PATHS)

class MonotonicWeightKernel(BaseWeightKernel):
    """
    MonotonicWeightKernel

    Base class for monotonic weight kernels.
    Handles bounds, normalization, and direction.

    A weighting kernel that applies a monotonic activation/taper function between defined
    lower and upper bounds, based on a given threshold direction.

    There are two main types of monotonic kernels: taper and activation. The taper function
    is used to smoothly transition between the lower and upper bounds over some finite interval, 
    while the activation style offers options that asymptote to 0 or 1, such as sigmoid or tanh.
    Thus the activation style supports +/- infinity bounds, while the taper style requires finite bounds.

    """
    __doc__ = write_lines(base_attr_dict)

    def __init__(self, attr_dict=base_attr_dict, **kwargs):
        """
            Constructor.
        """
        super().__init__(attr_dict=base_attr_dict, **kwargs)
        self.weight_type = "monotonic"

    @property
    def _has_finite_transition_bounds(self) -> bool:
        """
        Check if the transition bounds are finite.

        Returns
        -------
        bool
            True if both transition_lower_bound and transition_upper_bound are finite, False otherwise.
        """
        lb = float(self.transition_lower_bound)
        ub = float(self.transition_upper_bound)
        return np.isfinite(lb) and np.isfinite(ub)
    
    def _normalize(self, values):
        """
            Normalize input values to the [0, 1] interval based on finite transition bounds.

            Only supports finite lower and upper bounds. Subclasses should override this method
            if they wish to support infinite bounds or custom normalization.

            Parameters
            ----------
            values : array-like
                Input values to be normalized.

            Returns
            -------
            np.ndarray
                Normalized values in the range [0, 1].

            Raises
            ------
            ValueError
                If either transition bound is infinite.
        """
        if self._has_finite_transition_bounds:
            lb = float(self.transition_lower_bound)
            ub = float(self.transition_upper_bound)
            values = np.asarray(values)
            return (values - lb) / (ub - lb)
        else:
            raise ValueError("MonotonicWeightKernel only supports finite transition bounds. "
                            "Override _normalize in subclasses for infinite bounds.")
    


class TaperMonotonicWeightKernel(MonotonicWeightKernel):
    """
    Handles taper/window styles: rectangle, hann, hamming, blackman.
    """
    __doc__ = write_lines(taper_attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=taper_attr_dict, **kwargs)
        self.weight_type = "taper_monotonic"

    def _normalize(self, values):
        """
        Normalize input values to the [0, 1] interval based on the transition bounds and threshold direction.

        This function maps the input array `values` to a normalized scale between 0 and 1, according to the
        transition_lower_bound and transition_upper_bound attributes. The normalization is performed differently
        depending on the threshold direction:

        - If threshold is 'low cut', values below the lower bound are mapped to 0, values above the upper bound are mapped to 1,
          and values in between are linearly scaled.
        - If threshold is 'high cut', the mapping is reversed: values below the lower bound are mapped to 1, values above the upper bound to 0,
          and values in between are linearly scaled in the opposite direction.

        Parameters
        ----------
        values : array-like
            Input values to be normalized.

        Returns
        -------
        np.ndarray
            Normalized values in the range [0, 1].

        Raises
        ------
        ValueError
            If the threshold direction is not recognized.
        """
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

class ActivationMonotonicWeightKernel(MonotonicWeightKernel):
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

    def _normalize(self, values):
        """
        Normalize input values to the [0, 1] interval for activation kernels, supporting infinite bounds and respecting threshold direction.

        For finite bounds, applies linear normalization and reverses for 'high cut'.
        For infinite bounds, subclasses should define behavior, but this implementation will map all values to 0.5.
        """
        lb = float(self.transition_lower_bound)
        ub = float(self.transition_upper_bound)
        values = np.asarray(values)
        direction = getattr(self, 'threshold', 'low cut')
        # Both bounds finite
        if np.isfinite(lb) and np.isfinite(ub):
            x = (values - lb) / (ub - lb)
            if direction == 'high cut':
                x = 1 - x
            return np.clip(x, 0, 1)
        # Infinite bounds: fallback (could be extended for custom behavior)
        msg = "ActivationMonotonicWeightKernel only supports finite transition bounds. "
        self.logger.warning(msg + "Returning 0.5 for all values.")
        return np.full_like(values, 0.5)

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


# TODO: Uncomment if needed for testing or future use
# def _normalize(self, values):
#     """
#     Normalize input values to the [0, 1] interval, supporting infinite bounds for activation and taper kernels.
#     Handles all combinations of finite and infinite transition bounds:
#     - Both bounds finite: linear normalization.
#     - Lower bound -inf, upper bound finite: exponential normalization.
#     - Lower bound finite, upper bound +inf: exponential normalization.
#     - Both bounds infinite: all values map to 0.5.
#     """
#     lb = float(self.transition_lower_bound)
#     ub = float(self.transition_upper_bound)
#     values = np.asarray(values)
#     # Both bounds finite
#     if np.isfinite(lb) and np.isfinite(ub):
#         return np.clip((values - lb) / (ub - lb), 0, 1)
#     # Lower bound -inf, upper bound finite
#     elif not np.isfinite(lb) and np.isfinite(ub):
#         scale = np.std(values) if np.std(values) > 0 else 1.0
#         x = 1 - np.exp(-(ub - values) / scale)
#         return np.clip(x, 0, 1)
#     # Lower bound finite, upper bound +inf
#     elif np.isfinite(lb) and not np.isfinite(ub):
#         scale = np.std(values) if np.std(values) > 0 else 1.0
#         x = 1 - np.exp(-(values - lb) / scale)
#         return np.clip(x, 0, 1)
#     # Both bounds infinite
#     else:
#         return np.full_like(values, 0.5)