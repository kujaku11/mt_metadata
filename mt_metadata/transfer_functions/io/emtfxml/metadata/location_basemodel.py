# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class DatumEnum(str, Enum):
    WGS84 = "WGS84"
    NAD83 = "NAD83"
    other = "other"


class Location(MetadataBase):
    latitude: Annotated[
        float,
        Field(
            default=0.0,
            description="latitude of location in datum specified at survey level",
            examples="23.134",
            alias=["lat"],
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    longitude: Annotated[
        float,
        Field(
            default=0.0,
            description="longitude of location in datum specified at survey level",
            examples="14.23",
            alias=["lon", "long"],
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
            alias=["elev"],
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
        DatumEnum | None,
        Field(
            default=None,
            description="Datum of the location values.  Usually a well known datum like WGS84.",
            examples="WGS84",
            alias=None,
            json_schema_extra={
                "units": None,
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
            alias=["east", "easting"],
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
            alias=["east", "easting"],
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
            alias=["north", "northing"],
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
            alias=["north", "northing"],
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
