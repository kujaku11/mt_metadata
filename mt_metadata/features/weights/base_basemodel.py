# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class WeightTypeEnum(StrEnumerationBase):
    monotonic = "monotonic"
    learned = "learned"
    spatial = "spatial"
    custom = "custom"


class Base(MetadataBase):
    weight_type: Annotated[
        WeightTypeEnum,
        Field(
            default="monotonic",
            description="Type of weighting kernel (e.g., monotonic, learned, spatial).",
            examples=["monotonic"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    description: Annotated[
        str | None,
        Field(
            default=None,
            description="Human-readable description of what this kernel is for.",
            examples=[
                "This kernel smoothly transitions between 0 and 1 in a monotonic way"
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    active: Annotated[
        bool | None,
        Field(
            default=None,
            description="If false, this kernel will be skipped during weighting.",
            examples=["false"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    def evaluate(self, values):
        """
        Evaluate the kernel on the input feature values.

        Parameters
        ----------
        values : np.ndarray or float
            The feature values to apply the weight kernel to.

        Returns
        -------
        weights : np.ndarray or float
            The resulting weight(s).
        """
        raise NotImplementedError("BaseWeightKernel cannot be evaluated directly.")
