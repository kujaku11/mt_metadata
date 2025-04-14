# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


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
            type="number",
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
            type="number",
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
            type="number",
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
            type="number",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ] = None

    longitude_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in degrees",
            examples="0.01",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ] = None

    elevation_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in elevation estimation",
            examples="0.01",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    datum: Annotated[
        DatumEnum | None,
        Field(
            default=None,
            description="Datum of the location values.  Usually a well known datum like WGS84.",
            examples="WGS84",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    x: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            type="number",
            alias=["east", "easting"],
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    x2: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            type="number",
            alias=["east", "easting"],
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    y: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            type="number",
            alias=["north", "northing"],
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    y2: Annotated[
        float | None,
        Field(
            default=None,
            description="relative distance to the center of the station",
            examples="10.0",
            type="number",
            alias=["north", "northing"],
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    z: Annotated[
        float | None,
        Field(
            default=None,
            description="relative elevation to the center of the station",
            examples="10.0",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    z2: Annotated[
        float | None,
        Field(
            default=None,
            description="relative elevation to the center of the station",
            examples="10.0",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    x_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in x-direction",
            examples="0.01",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    y_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in y-direction",
            examples="0.01",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None

    z_uncertainty: Annotated[
        float | None,
        Field(
            default=None,
            description="uncertainty in longitude estimation in z-direction",
            examples="0.01",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ] = None
