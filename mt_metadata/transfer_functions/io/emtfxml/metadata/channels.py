# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.units import get_unit_object


# =====================================================
class Channels(MetadataBase):
    ref: Annotated[
        str,
        Field(
            default="",
            description="reference to the site name",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["site"],
            },
        ),
    ]

    units: Annotated[
        str,
        Field(
            default="",
            description="units of the distance coordinates",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["site"],
            },
        ),
    ]

    inputs: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of input channel names (sources)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [["Hx", "Hy"]],
            },
        ),
    ]

    outputs: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of output channel names (responses)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [["Ex", "Ey", "Hz"]],
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
