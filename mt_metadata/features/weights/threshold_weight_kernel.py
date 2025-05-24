"""
ThresholdWeightKernel
"""

from typing import Literal
import numpy as np

from mt_metadata.features.weights.monotonic_weight_kernel import TaperMonotonicWeightKernel

class ThresholdWeightKernel(TaperMonotonicWeightKernel):
    """
    ThresholdWeightKernel

    A special case of MonotonicWeightKernel where the transition region is a single value,
    resulting in a hard threshold (step function). This kernel outputs 0 or 1 depending on
    whether the input is above or below the threshold, according to the threshold_type.

    Parameters
    ----------
    threshold : float
        The threshold value.
    threshold_type : str, optional
        "low cut" (default) or "high cut". Determines which side is downweighted.
    **kwargs :
        Additional keyword arguments passed to MonotonicWeightKernel.
    """
    def __init__(self, threshold, threshold_type="low cut", **kwargs):
        super().__init__(
            transition_lower_bound=threshold,
            transition_upper_bound=threshold,
            half_window_style="rectangle",
            threshold=threshold_type,
            **kwargs
        )
