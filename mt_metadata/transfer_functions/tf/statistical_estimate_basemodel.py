# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.utils.units import get_unit_object


# =====================================================
class DataTypeEnum(str, Enum):
    real = "real"
    complex = "complex"
    other = "other"


class StatisticalEstimate(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the statistical estimate",
            examples="transfer function",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    data_type: Annotated[
        DataTypeEnum,
        Field(
            default="complex",
            description="Type of number contained in the estimate",
            examples="real",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    description: Annotated[
        str,
        Field(
            default="",
            description="Description of the statistical estimate",
            examples="this is an estimate",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    input_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="List of input channels (sources)",
            examples="[hx, hy]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="List of output channels (response).",
            examples=["ex", "ey", "hz"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units: Annotated[
        str,
        Field(
            default="",
            description="Units of the estimate.",
            examples="millivolts per kilometer per nanotesla",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str) -> str:
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)
