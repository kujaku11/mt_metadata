# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class MethodEnum(str, Enum):
    compass = "compass"
    GPS = "GPS"
    theodolite = "theodolite"
    other = "other"


class ReferenceFrameEnum(str, Enum):
    geographic = "geographic"
    geomagnetic = "geomagnetic"


class ValueEnum(str, Enum):
    orthogonal = "orthogonal"
    other = "other"


class Orientation(MetadataBase):
    method: Annotated[
        MethodEnum,
        Field(
            default="",
            description="method for orienting station layout",
            examples="compass",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    reference_frame: Annotated[
        ReferenceFrameEnum,
        Field(
            default=geographic,
            description='"Reference frame for station layout.  There are only 2 options geographic and geomagnetic.  Both assume a right-handed coordinate system with North=0 E=90 and vertical positive downward"',
            examples="geomagnetic",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    angle_to_geographic_north: Annotated[
        float | None,
        Field(
            default=None,
            description='"Angle to rotate the data to align with geographic north. If this number is 0 then it is assumed the data are aligned with geographic north in a right handed coordinate system."',
            examples="geomagnetic",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ] = None

    value: Annotated[
        ValueEnum | None,
        Field(
            default=None,
            description='"Channel orientation relative to each other"',
            examples="orthogonal",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
