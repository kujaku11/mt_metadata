# =====================================================
# Imports
# =====================================================
from typing import Annotated
from pydantic import Field, field_validator, ValidationInfo, AliasChoices

from mt_metadata.base import MetadataBase
from mt_metadata.utils.location_helpers import validate_position
from mt_metadata.common import Declination, GeographicLocation
from pyproj import CRS


# =====================================================


class BasicLocationNoDatum(MetadataBase):
    """
    A partial location class that only includes the latitude, longitude, and elevation.
    This is used to avoid circular imports.
    """

    latitude: Annotated[
        float | None,
        Field(
            default=None,
            description="Latitude of the location.",
            examples="12.324",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    longitude: Annotated[
        float | None,
        Field(
            default=None,
            description="Longitude of the location.",
            examples="12.324",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def validate_position(cls, value, info: ValidationInfo):
        return validate_position(value, info.field_name)


class BasicLocation(BasicLocationNoDatum):
    elevation: Annotated[
        float | None,
        Field(
            default=None,
            description="Elevation of the location.",
            examples="1234.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]
    datum: Annotated[
        str | int,
        Field(
            default="WGS 84",
            description="Datum of the location values.  Usually a well known datum like WGS84.",
            examples="WGS 84",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
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


class Location(BasicLocation):
    """
    Positional location of a geographic point
    """

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


class StationLocation(Location):
    """
    A class that represents the location of a station. It includes latitude, longitude, elevation,
    and other related attributes.
    """

    declination: Annotated[
        Declination,
        Field(
            default_factory=Declination,
            description="Declination of the location.",
            examples="Declination(10.0)",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    geographic_location: Annotated[
        GeographicLocation,
        Field(
            default_factory=GeographicLocation,
            description="Geographic location of the station.",
            examples="GeographicLocation(latitude=12.34, longitude=56.78)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
