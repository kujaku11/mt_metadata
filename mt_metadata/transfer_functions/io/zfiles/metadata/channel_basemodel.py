# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated, Any

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class ChannelEnum(str, Enum):
    ex = "ex"
    ey = "ey"
    hx = "hx"
    hy = "hy"
    hz = "hz"


class Channel(MetadataBase):
    number: Annotated[
        int,
        Field(
            default=None,
            description="Channel number",
            examples="1",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    azimuth: Annotated[
        Any,
        Field(
            default=0.0,
            description="channel azimuth",
            examples="90",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    tilt: Annotated[
        Any,
        Field(
            default=0.0,
            description="channel tilt relative to horizontal.",
            examples="100.0",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    dl: Annotated[
        Any,
        Field(
            default=None,
            description="station",
            examples="mt001",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channel: Annotated[
        ChannelEnum,
        Field(
            default="",
            description="channel name",
            examples="hx",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
