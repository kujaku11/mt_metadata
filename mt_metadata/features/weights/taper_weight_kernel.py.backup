"""
Module with a compound kernel, mixing multiple monotonic kernels.
"""

from typing import Annotated, Tuple

import numpy as np
from pydantic import computed_field, Field

from mt_metadata.features.weights.taper_monotonic_weight_kernel import (
    TaperMonotonicWeightKernel,
)
from mt_metadata.processing.window import TypeEnum

from .base import Base


class TaperWeightKernel(Base):
    """
    A composite weight kernel that multiplies a low-cut and a high-cut monotonic taper kernel.

    Parameters
    ----------
    low_cut : tuple[float, float]
        (lower_bound, upper_bound) for the low-cut transition region.
    high_cut : tuple[float, float]
        (lower_bound, upper_bound) for the high-cut transition region.
    style : str, optional
        The taper style to use (default is 'hann').
    **kwargs
        Additional keyword arguments passed to BaseWeightKernel.
    """

    low_cut: Annotated[
        Tuple[float, float],
        Field(
            description="Low cut transition bounds",
            examples=[(0.1, 0.5)],
            json_schema_extra={"units": None, "required": True},
        ),
    ]
    high_cut: Annotated[
        Tuple[float, float],
        Field(
            description="High cut transition bounds",
            examples=[(0.5, 1.0)],
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    style: Annotated[
        TypeEnum,
        Field(
            description="Taper style",
            examples=["hann", "hamming", "blackman"],
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    @computed_field
    @property
    def low_kernel(self) -> TaperMonotonicWeightKernel:
        """The low-cut taper kernel."""
        return TaperMonotonicWeightKernel(  # type: ignore
            threshold="low cut",
            transition_lower_bound=self.low_cut[0],
            transition_upper_bound=self.low_cut[1],
            half_window_style=self.style,
        )

    @computed_field
    @property
    def high_kernel(self) -> TaperMonotonicWeightKernel:
        """The high-cut taper kernel."""
        return TaperMonotonicWeightKernel(  # type: ignore
            threshold="high cut",
            transition_lower_bound=self.high_cut[0],
            transition_upper_bound=self.high_cut[1],
            half_window_style=self.style,
        )

    def evaluate(self, values: np.ndarray) -> np.ndarray:
        """
        Evaluate the composite taper weight kernel on the input values.

        Parameters
        ----------
        values : np.ndarray
            Input values to evaluate the kernel on.

        Returns
        -------
        np.ndarray
            The product of the low-cut and high-cut kernel evaluations.
        """
        return self.low_kernel.evaluate(values) * self.high_kernel.evaluate(values)
