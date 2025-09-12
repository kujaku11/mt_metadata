# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
from numpy._typing import NDArray
from pydantic import Field

from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.features.weights.monotonic_weight_kernel_basemodel import (
    MonotonicWeightKernel,
)


# =====================================================
class HalfWindowStyleEnum(StrEnumerationBase):
    hamming = "hamming"
    hann = "hann"
    rectangle = "rectangle"
    blackman = "blackman"


class ActivationStyleEnum(StrEnumerationBase):
    linear = "linear"
    sigmoid = "sigmoid"
    tanh = "tanh"
    relu = "relu"
    hard_tanh = "hard_tanh"
    hard_sigmoid = "hard_sigmoid"


class TaperMonotonicWeightKernel(MonotonicWeightKernel):
    half_window_style: Annotated[
        HalfWindowStyleEnum,
        Field(
            default="rectangle",
            description="Tapering/activation function to use between transition bounds.",
            examples=["hann"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    def _normalize(self, values: NDArray) -> NDArray:
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

    def evaluate(self, values: NDArray) -> NDArray:
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
