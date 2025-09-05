# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated
import numpy as np
from numpy._typing._array_like import NDArray

from mt_metadata.base import MetadataBase
from pydantic import Field, computed_field
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class ThresholdEnum(StrEnumerationBase):
    low_cut = "low cut"
    high_cut = "high cut"


class StyleEnum(StrEnumerationBase):
    taper = "taper"
    activation = "activation"


class MonotonicWeightKernel(MetadataBase):
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

    threshold: Annotated[
        ThresholdEnum,
        Field(
            default="low cut",
            description="Which side of a threshold should be downweighted.",
            examples=["low cut"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    style: Annotated[
        StyleEnum,
        Field(
            default="taper",
            description="Tapering/activation function to use between transition bounds.",
            examples=["activation"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    transition_lower_bound: Annotated[
        float,
        Field(
            default=-1000000000.0,
            description="Start of the taper region (weight begins to change).",
            examples=["-inf"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    transition_upper_bound: Annotated[
        float,
        Field(
            default=1000000000.0,
            description="End of the taper region (weight finishes changing).",
            examples=["+inf"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @computed_field
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

    def _normalize(self, values) -> NDArray:
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
            raise ValueError(
                "MonotonicWeightKernel only supports finite transition bounds. "
                "Override _normalize in subclasses for infinite bounds."
            )
