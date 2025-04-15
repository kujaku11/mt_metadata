# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.utils.location_helpers import convert_position_str2float, DatumEnum


# =====================================================


class Location(MetadataBase):
    latitude: Annotated[
        float | str,
        Field(
            default=0.0,
            description="latitude of location in datum specified at survey level",
            examples="23.134",
            type="number",
            alias=["lat"],
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
            type="number",
            alias=["lon", "long"],
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

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def validate_position(
        cls,
        value,
    ):
        if isinstance(value, str):
            value = convert_position_str2float(value)
        else:
            try:
                value = float(value)
            except ValueError:
                raise ValueError("latitude and longitude must be float or str")
        if not (abs(value) <= 90) and cls.model_fields_set == {"latitude"}:
            raise ValueError("latitude must be between -90 and 90 degrees")
        if not (abs(value) <= 180) and cls.model_fields_set == {"longitude"}:
            raise ValueError("longitude must be between -180 and 180 degrees")
        return value
