# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.features.weights.taper_monotonic_weight_kernel import (
    TaperMonotonicWeightKernel,
)


# =====================================================


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

    threshold_type: Annotated[
        str,
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

    # TODO: Uncomment if needed for testing or future use
    def _normalize(self, values):
        """
        Normalize input values to the [0, 1] interval, supporting infinite bounds for activation and taper kernels.
        Handles all combinations of finite and infinite transition bounds:
        - Both bounds finite: linear normalization.
        - Lower bound -inf, upper bound finite: exponential normalization.
        - Lower bound finite, upper bound +inf: exponential normalization.
        - Both bounds infinite: all values map to 0.5.
        """

        raise NotImplementedError(
            "Normalization not implemented for ThresholdWeightKernel."
        )
        # lb = float(self.transition_lower_bound)
        # ub = float(self.transition_upper_bound)
        # values = np.asarray(values)
        # # Both bounds finite
        # if np.isfinite(lb) and np.isfinite(ub):
        #     return np.clip((values - lb) / (ub - lb), 0, 1)
        # # Lower bound -inf, upper bound finite
        # elif not np.isfinite(lb) and np.isfinite(ub):
        #     scale = np.std(values) if np.std(values) > 0 else 1.0
        #     x = 1 - np.exp(-(ub - values) / scale)
        #     return np.clip(x, 0, 1)
        # # Lower bound finite, upper bound +inf
        # elif np.isfinite(lb) and not np.isfinite(ub):
        #     scale = np.std(values) if np.std(values) > 0 else 1.0
        #     x = 1 - np.exp(-(values - lb) / scale)
        #     return np.clip(x, 0, 1)
        # # Both bounds infinite
        # else:
        #     return np.full_like(values, 0.5)
