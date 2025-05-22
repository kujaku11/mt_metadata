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
    NAD27 = "NAD27"
    other = "other"


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
        DatumEnum,
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
        str,
        Field(
            default="",
            description="UTM zone of location",
            examples=["12"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
