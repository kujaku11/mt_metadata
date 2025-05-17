"""
ThresholdWeightKernel
"""

from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel
from typing import Literal
import numpy as np

class ThresholdWeightKernel(MonotonicWeightKernel):
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
        super().__init__(**kwargs)
        kernel_dict = {
            "transition_lower_bound": threshold,
            "transition_upper_bound": threshold,
            "half_window_style": "rectangle",
            "threshold": threshold_type
        }
        self.from_dict(kernel_dict)

        # super().__init__(
        #     threshold: Literal["low cut", "high cut"]=threshold_type,
        #     transition_lower_bound: float=threshold,
        #     transition_upper_bound=threshold,
        #     **kwargs
        # )

    def evaluate(self, values):
        """
        Evaluate the threshold kernel on the input values.

        Parameters
        ----------
        values : float or np.ndarray
            Input values to threshold.

        Returns
        -------
        weights : float or np.ndarray
            0 or 1, depending on threshold_type and threshold.
        """
        values = np.asarray(values)
        if self.threshold == "low cut":
            return (values >= self.transition_lower_bound).astype(float)
        elif self.threshold == "high cut":
            return (values <= self.transition_upper_bound).astype(float)
        else:
            raise ValueError(f"Unknown threshold type: {self.threshold}")

# Example usage:
# kernel = ThresholdWeightKernel(0.8, threshold_type="low cut")
# weights = kernel.evaluate(np.array([0.7, 0.8, 0.9]))
# print(weights)  # Output: [0. 1. 1.]
