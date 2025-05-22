# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.utils.units import get_unit_object


# =====================================================
class DefineMeasurement(MetadataBase):
    maxchan: Annotated[
        int,
        Field(
            default=None,
            description="maximum number of channels",
            examples=["16"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxrun: Annotated[
        int,
        Field(
            default=None,
            description="maximum number of runs",
            examples=["999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxmeas: Annotated[
        int,
        Field(
            default=None,
            description="maximum number of measurements",
            examples=["999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    reftype: Annotated[
        str | None,
        Field(
            default=None,
            description="Type of offset from reference center point.",
            examples=["cart"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    refloc: Annotated[
        str | None,
        Field(
            default=None,
            description="Description of location reference center point.",
            examples=["here"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    reflat: Annotated[
        float | None,
        Field(
            default=None,
            description="Latitude of reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    reflon: Annotated[
        float | None,
        Field(
            default=None,
            description="Longitude reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    refelev: Annotated[
        float | None,
        Field(
            default=None,
            description="Elevation reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    units: Annotated[
        float | None,
        Field(
            default="m",
            description="In the EDI standards this is the elevation units.",
            examples=["m"],
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
