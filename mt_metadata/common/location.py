# =====================================================
# Imports
# =====================================================
from typing import Annotated
from pydantic import Field, field_validator, ValidationInfo, AliasChoices

from mt_metadata.base import MetadataBase
from mt_metadata.utils.location_helpers import validate_position, DatumEnum


# =====================================================


class Location(MetadataBase):
    latitude: Annotated[
        float | str,
        Field(
            default=0.0,
            description="latitude of location in datum specified at survey level",
            examples="23.134",
            alias_value=AliasChoices("latitude", "lat"),
            ge=-90.0,
            le=90.0,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    longitude: Annotated[
        float | str,
        Field(
            default=0.0,
            description="longitude of location in datum specified at survey level",
            examples="14.23",
            alias_value=AliasChoices("longitude", "lon", "long"),
            ge=-180.0,
            le=180.0,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    elevation: Annotated[
        float,
        Field(
            default=0.0,
            description="elevation of location in datum specified at survey level",
            examples="123.4",
            alias_value=AliasChoices("elevation", "elev"),
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    latitude_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in latitude estimation in degrees",
            examples="0.01",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    longitude_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in degrees",
            examples="0.01",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    elevation_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in elevation estimation",
            examples="0.01",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    datum: Annotated[
        DatumEnum,
        Field(
            default="WGS84",
            description="Datum of the location values.  Usually a well known datum like WGS84.",
            examples="WGS84",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = "WGS84"

    x: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            alias_value=AliasChoices("x", "easting", "east"),
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    x2: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            alias_value=AliasChoices("x2", "east", "easting"),
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    y: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            alias_value=AliasChoices("y", "north", "northing"),
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    y2: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            alias_value=AliasChoices("y2", "north", "northing"),
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    z: Annotated[
        float | None,
        Field(
            default=None,
            description="relative elevation to the center of the station",
            examples="10.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    z2: Annotated[
        float | None,
        Field(
            default=None,
            description="relative elevation to the center of the station",
            examples="10.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    x_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in x-direction",
            examples="0.01",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    y_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in y-direction",
            examples="0.01",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    z_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in z-direction",
            examples="0.01",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def validate_position(cls, value, info: ValidationInfo):
        return validate_position(value, info.field_name)
