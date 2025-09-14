# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.features.coherence import Coherence
from mt_metadata.features.fc_coherence import FCCoherence
from mt_metadata.features.feature import Feature
from mt_metadata.features.weights.activation_monotonic_weight_kernel import (
    ActivationMonotonicWeightKernel,
)
from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel
from mt_metadata.features.weights.taper_monotonic_weight_kernel import (
    TaperMonotonicWeightKernel,
)


## for new features import and add to this dictionary.
feature_classes = {
    "base": Feature,
    "coherence": Coherence,
    "fc_coherence": FCCoherence,
}

weight_classes = {
    "monotonic": MonotonicWeightKernel,
    "taper": TaperMonotonicWeightKernel,
    "activation": ActivationMonotonicWeightKernel,
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
    ) -> Feature | Coherence | FCCoherence | None:
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
        else:
            return None

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
                # Use the 'style' field to determine which kernel class to use
                style = str(item.get("style", ""))
                if style in weight_classes:
                    try:
                        kernels.append(weight_classes[style](**item))
                    except Exception as e:
                        msg = (
                            f"Failed to create weight kernel with style '{style}': {e}"
                        )
                        logger.warning(msg)
                else:
                    # Fallback to weight_type for backward compatibility
                    weight_type = str(item.get("weight_type", ""))
                    if weight_type in weight_classes:
                        try:
                            kernels.append(weight_classes[weight_type](**item))
                        except Exception as e:
                            msg = f"Failed to create weight kernel with weight_type '{weight_type}': {e}"
                            logger.warning(msg)
                    else:
                        msg = f"Neither style '{style}' nor weight_type '{weight_type}' recognized -- skipping"
                        logger.warning(msg)

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
