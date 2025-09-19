# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
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
            default=WeightTypeEnum.monotonic,
            description="Type of weighting kernel (e.g., monotonic, learned, spatial).",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["monotonic"],
            },
        ),
    ]

    description: Annotated[
        str | None,
        Field(
            default=None,
            description="Human-readable description of what this kernel is for.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [
                    "This kernel smoothly transitions between 0 and 1 in a monotonic way"
                ],
            },
        ),
    ]

    active: Annotated[
        bool | None,
        Field(
            default=None,
            description="If false, this kernel will be skipped during weighting.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["false"],
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
