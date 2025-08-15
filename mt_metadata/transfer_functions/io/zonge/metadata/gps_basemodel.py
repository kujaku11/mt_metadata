# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo
from pyproj import CRS

from mt_metadata.base import MetadataBase
from mt_metadata.utils import location_helpers


# =====================================================


class Gps(MetadataBase):
    lat: Annotated[
        float,
        Field(
            default=0.0,
            description="latitude",
            examples=["10.3"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    lon: Annotated[
        float,
        Field(
            default=0.0,
            description="longitude",
            examples=["10.3"],
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

    @field_validator("lat", "lon", mode="before")
    @classmethod
    def validate_position(cls, value, info: ValidationInfo):
        if info.field_name in ["lat"]:
            field_name = "latitude"
        elif info.field_name in ["lon"]:
            field_name = "longitude"
        return location_helpers.validate_position(value, field_name)
