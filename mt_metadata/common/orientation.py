# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import (
    ChannelOrientationEnum,
    GeographicReferenceFrameEnum,
    OrientationMethodEnum,
)


# =====================================================


class Orientation(MetadataBase):
    method: Annotated[
        OrientationMethodEnum,
        Field(
            default="compass",
            description="method for orienting station layout",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "compass",
                "type": "string",
            },
        ),
    ]

    reference_frame: Annotated[
        GeographicReferenceFrameEnum,
        Field(
            default="geographic",
            description='"Reference frame for station layout.  There are only 2 options geographic and geomagnetic.  Both assume a right-handed coordinate system with North=0 E=90 and vertical positive downward"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "geomagnetic",
                "type": "string",
            },
        ),
    ]

    angle_to_geographic_north: Annotated[
        float | None,
        Field(
            default=None,
            description='"Angle to rotate the data to align with geographic north. If this number is 0 then it is assumed the data are aligned with geographic north in a right handed coordinate system."',
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
                "examples": "geomagnetic",
                "type": "number",
            },
        ),
    ]

    value: Annotated[
        ChannelOrientationEnum | None,
        Field(
            default="orthogonal",
            description='"Channel orientation relative to each other"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "orthogonal",
                "type": "string",
            },
        ),
    ]
