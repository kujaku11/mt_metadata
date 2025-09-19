# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field, field_validator
from pyproj import CRS

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import DataTypeEnum


# =====================================================


class ArrayEnum(str, Enum):
    tensor = "tensor"


class ProjEnum(str, Enum):
    UTM = "UTM"
    other = "other"


class Survey(MetadataBase):
    type: Annotated[
        DataTypeEnum,
        Field(
            default="nsamt",
            description="Type of EM survey",
            examples=["nsamt"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    array: Annotated[
        ArrayEnum,
        Field(
            default="tensor",
            description="Type of array",
            examples=["tensor"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    datum: Annotated[
        str,
        Field(
            default="WGS84",
            description="Datum of the location",
            examples=["WGS84"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    u_t_m_zone: Annotated[
        int,
        Field(
            default=0,
            description="UTM zone of location",
            examples=["12"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    proj: Annotated[
        ProjEnum,
        Field(
            default="UTM",
            description="Projection of the location coordinates",
            examples=["UTM"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("datum", mode="before")
    @classmethod
    def validate_datum(cls, value: str | int) -> str:
        """
        Validate the datum value and convert it to the appropriate enum type.
        """
        try:
            datum_crs = CRS.from_user_input(value)
            return datum_crs.name
        except Exception:
            raise ValueError(
                f"Invalid datum value: {value}. Must be a valid CRS string or identifier."
            )
