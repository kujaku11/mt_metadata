# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
from loguru import logger
from numpy._typing import NDArray
from pydantic import Field

from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel


# =====================================================
class ThresholdEnum(str, Enum):
    low_cut = "low cut"
    high_cut = "high cut"


class ActivationStyleEnum(str, Enum):
    sigmoid = "sigmoid"
    hard_sigmoid = "hard_sigmoid"
    tanh = "tanh"
    hard_tanh = "hard_tanh"


class ActivationMonotonicWeightKernel(MonotonicWeightKernel):
    threshold: Annotated[
        ThresholdEnum,
        Field(
            default="low cut",
            description="Which side of a threshold should be downweighted.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["low cut"],
            },
        ),
    ]

    activation_style: Annotated[
        ActivationStyleEnum,
        Field(
            default="sigmoid",
            description="Tapering/activation function to use between transition bounds.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["tanh"],
            },
        ),
    ]

    steepness: Annotated[
        float,  # the definition had default as None, can we set it to 1?
        Field(
            default=1.0,
            description="Controls the sharpness of the activation transition.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["10"],
            },
        ),
    ]

    def _normalize(self, values: NDArray) -> NDArray:
        """
        Normalize input values to the [0, 1] interval for activation kernels, supporting infinite bounds and respecting threshold direction.

        For finite bounds, applies linear normalization and reverses for 'high cut'.
        For infinite bounds, subclasses should define behavior, but this implementation will map all values to 0.5.
        """
        lb = float(self.transition_lower_bound)
        ub = float(self.transition_upper_bound)
        values = np.asarray(values)
        direction = getattr(self, "threshold", "low cut")
        # Both bounds finite
        if np.isfinite(lb) and np.isfinite(ub):
            x = (values - lb) / (ub - lb)
            if direction == "high cut":
                x = 1 - x
            return np.clip(x, 0, 1)
        # Infinite bounds: fallback (could be extended for custom behavior)
        msg = "ActivationMonotonicWeightKernel only supports finite transition bounds. "
        logger.warning(msg + "Returning 0.5 for all values.")
        return np.full_like(values, 0.5)

    def evaluate(self, values: NDArray) -> NDArray:
        """
        Evaluate the activation function for the given input values.

        Parameters
        ----------
        values : NDArray
            Input values to be evaluated.

        Returns
        -------
        NDArray
            Evaluated activation values.

        Raises
        ------
        ValueError
            If the activation style is not recognized.
        """

        x = self._normalize(values)
        activation_style = self.activation_style

        if activation_style == "sigmoid":
            y = 1 / (
                1 + np.exp(-float(self.steepness) * (x - 0.5))
            )  # what happens if steepness is None?
        elif activation_style == "hard_sigmoid":
            y = np.clip(0.2 * (x - 0.5) + 0.5, 0, 1)
        elif activation_style == "tanh":
            y = 0.5 * (np.tanh(float(self.steepness) * (x - 0.5)) + 1)
        elif activation_style == "hard_tanh":
            y = np.clip(x, 0, 1)
        else:
            raise ValueError(f"Unsupported activation style: {activation_style}")

        return y
