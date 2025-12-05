# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, model_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.features.coherence import Coherence
from mt_metadata.features.fc_coherence import FCCoherence
from mt_metadata.features.feature import Feature
from mt_metadata.features.striding_window_coherence import StridingWindowCoherence
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
    "striding_window_coherence": StridingWindowCoherence,
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
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["coherence"],
            },
        ),
    ]

    feature: Annotated[
        dict | Feature | Coherence | FCCoherence | StridingWindowCoherence,
        Field(
            default_factory=Feature,  # type: ignore
            description="The feature specification.",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [{"type": "coherence"}],
            },
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
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [{"type": "monotonic"}],
            },
        ),
    ]

    @model_validator(mode="before")
    @classmethod
    def pre_process_feature(cls, data: dict) -> dict:
        """Pre-process the feature dict to ensure correct class is instantiated."""
        if isinstance(data, dict) and "feature" in data:
            feature_data = data["feature"]
            # Handle nested feature dict wrapping
            while isinstance(feature_data, dict) and "feature" in feature_data:
                feature_data = feature_data["feature"]

            if isinstance(feature_data, dict):
                feature_name = feature_data.get("name")
                logger.info(f"pre_process_feature: feature_name={feature_name}")
                if feature_name in feature_classes:
                    feature_cls = feature_classes[feature_name]
                    logger.info(
                        f"pre_process_feature: Creating {feature_cls.__name__} instance"
                    )
                    data["feature"] = feature_cls(**feature_data)
                else:
                    logger.warning(
                        f"pre_process_feature: Unknown feature name '{feature_name}', using Feature"
                    )
        return data

    @field_validator("feature", mode="before")
    @classmethod
    def validate_feature(
        cls, value, info: ValidationInfo
    ) -> Feature | Coherence | FCCoherence | StridingWindowCoherence | None:
        """Validate the feature field to ensure it matches the feature_name."""
        logger.info(
            f"validate_feature called with value type: {type(value)}, value: {value}"
        )
        while (
            isinstance(value, dict)
            and "feature" in value
            and isinstance(value["feature"], dict)
        ):
            logger.info(f"Unwrapping nested feature dict")
            value = value["feature"]
        if isinstance(value, dict):
            feature_name = value.get("name")
            # Import here to avoid circular import at module level
            logger.info(
                f"Feature setter: feature_name={feature_name}, value keys={value.keys()}"
            )  # DEBUG
            if not isinstance(feature_name, str) or feature_name not in feature_classes:
                logger.warning(
                    f"Feature name '{feature_name}' not in feature_classes, using base Feature"
                )
                feature_cls = Feature
            else:
                feature_cls = feature_classes[feature_name]
                logger.info(f"Selected feature class: {feature_cls.__name__}")
            logger.debug(
                f"Feature setter: instantiated {feature_cls.__class__}"
            )  # DEBUG
            return feature_cls(**value)
        elif isinstance(
            value, (Feature, Coherence, FCCoherence, StridingWindowCoherence)
        ):
            logger.info(
                f"Feature setter: set directly to {type(value).__name__}"
            )  # DEBUG
            return value
        else:
            logger.warning(
                f"Feature value is neither dict nor Feature instance: {type(value)}"
            )
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
