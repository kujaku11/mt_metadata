# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class ChtypeEnum(str, Enum):
    ex = "ex"
    ey = "ey"
    other = "other"


class Emeasurement(MetadataBase):
    id: Annotated[
        float,
        Field(
            default=0.0,
            description="Channel number, could be location.channel_number.",
            examples="1",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    chtype: Annotated[
        ChtypeEnum,
        Field(
            default="",
            description="channel type, should start with an 'e'",
            examples="ex",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    x: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in north direction",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    x2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in north direction",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    y: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in east direction",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    y2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in east direction",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    z: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in depth",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    z2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in depth",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    azm: Annotated[
        float,
        Field(
            default=0.0,
            description="orientation of the sensor relative to coordinate system, clockwise positive.",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    acqchan: Annotated[
        str,
        Field(
            default="",
            description="description of acquired channel",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
