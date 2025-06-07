"""
    Module with a compound kernel, mixing multiple monotonic kernels.
"""

import numpy as np
from .monotonic_weight_kernel import TaperMonotonicWeightKernel
from .base import BaseWeightKernel

class TaperWeightKernel(BaseWeightKernel):
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
    def __init__(
            self, 
            low_cut: tuple[float, float], 
            high_cut: tuple[float, float], 
            style: str = "hann", 
            **kwargs
            ):
        super().__init__(**kwargs)
        self._low_kernel = TaperMonotonicWeightKernel(
            threshold="low cut",
            transition_lower_bound=low_cut[0],
            transition_upper_bound=low_cut[1],
            half_window_style=style
        )
        self._high_kernel = TaperMonotonicWeightKernel(
            threshold="high cut",
            transition_lower_bound=high_cut[0],
            transition_upper_bound=high_cut[1],
            half_window_style=style
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
        return self._low_kernel.evaluate(values) * self._high_kernel.evaluate(values)
