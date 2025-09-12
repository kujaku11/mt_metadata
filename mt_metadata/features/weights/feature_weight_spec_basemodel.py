# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.features.base_feature_basemodel import Feature
from mt_metadata.features.coherence_basemodel import Coherence
from mt_metadata.features.fc_coherence_basemodel import FCCoherence
from mt_metadata.features.weights.activation_monotonic_weight_kernel_basemodel import (
    ActivationMonotonicWeightKernel,
)
from mt_metadata.features.weights.monotonic_weight_kernel_basemodel import (
    MonotonicWeightKernel,
)
from mt_metadata.features.weights.taper_monotonic_weight_kernel_basemodel import (
    TaperMonotonicWeightKernel,
)


## for new features import and add to this dictionary.
feature_classes = {
    "base": Feature,
    "coherence": Coherence,
    "fc_coherence": FCCoherence,
}


# =====================================================
class FeatureNameEnum(str, Enum):
    coherence = "coherence"
    multiple_coherence = "multiple coherence"


class FeatureWeightSpec(MetadataBase):
    feature_name: Annotated[
        FeatureNameEnum,
        Field(
            default="",
            description="The name of the feature to evaluate (e.g., coherence, impedance_ratio).",
            examples=["coherence"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    feature: Annotated[
        dict | Feature | Coherence | FCCoherence,
        Field(
            default_factory=Feature,  # type: ignore
            description="The feature specification.",
            examples=[{"type": "coherence"}],
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    weight_kernels: Annotated[
        list[
            MonotonicWeightKernel
            | TaperMonotonicWeightKernel
            | ActivationMonotonicWeightKernel
        ],
        Field(
            default_factory=list,
            description="List of weight kernel specification.",
            examples=[{"type": "monotonic"}],
            json_schema_extra={"units": None, "required": True},
        ),
    ]

    @field_validator("feature", mode="before")
    @classmethod
    def validate_feature(
        cls, value, info: ValidationInfo
    ) -> Feature | Coherence | FCCoherence:
        """Validate the feature field to ensure it matches the feature_name."""
        while (
            isinstance(value, dict)
            and "feature" in value
            and isinstance(value["feature"], dict)
        ):
            value = value["feature"]
        if isinstance(value, dict):
            feature_name = value.get("name")
            # Import here to avoid circular import at module level
            logger.debug(
                f"Feature setter: feature_name={feature_name}, value={value}"
            )  # DEBUG
            if not isinstance(feature_name, str) or feature_name not in feature_classes:
                feature_cls = Feature
            else:
                feature_cls = feature_classes[feature_name]
            logger.debug(
                f"Feature setter: instantiated {feature_cls.__class__}"
            )  # DEBUG
            return feature_cls(**value)
        elif isinstance(value, (Feature, Coherence, FCCoherence)):
            logger.debug(f"Feature setter: set directly to {type(value)}")  # DEBUG
            return value

    @field_validator("weight_kernels", mode="before")
    @classmethod
    def validate_weight_kernels(
        cls, value, info: ValidationInfo
    ) -> list[
        MonotonicWeightKernel
        | TaperMonotonicWeightKernel
        | ActivationMonotonicWeightKernel
    ]:
        """Validate the weight_kernels field to ensure proper initialization."""
        if not isinstance(value, list):
            value = [value]
        kernels = []
        for item in value:
            if isinstance(item, dict) and "weight_kernel" in item:
                item = item["weight_kernel"]
            if isinstance(item, dict):
                kernel_type = str(item.get("type"))
                kernel_style = str(item.get("style", "linear"))
                if "monotonic" in kernel_type or "monotonic" in kernel_style:
                    kernel_cls = MonotonicWeightKernel
                elif "half_window" in kernel_style or "taper" in kernel_style:
                    kernel_cls = TaperMonotonicWeightKernel
                elif "activation" in kernel_type or "activation" in kernel_style:
                    kernel_cls = ActivationMonotonicWeightKernel
                else:
                    raise ValueError(f"Unknown kernel type: {kernel_type}")
                kernels.append(kernel_cls(**item))
            elif isinstance(
                item,
                (
                    MonotonicWeightKernel,
                    TaperMonotonicWeightKernel,
                    ActivationMonotonicWeightKernel,
                ),
            ):
                kernels.append(item)
            else:
                raise TypeError(f"Invalid type for weight_kernel: {type(item)}")
        return kernels

    def evaluate(self, feature_values):
        """
        Evaluate this feature's weighting based on the list of kernels.

        Parameters
        ----------
        feature_values : np.ndarray or float
            The computed values for this feature.

        Returns
        -------
        combined_weight : np.ndarray or float
            The combined weight from all kernels (e.g., multiplied together).
        """

        weights = [kernel.evaluate(feature_values) for kernel in self.weight_kernels]
        return np.prod(weights, axis=0) if weights else 1.0
