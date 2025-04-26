# =====================================================
# Imports
# =====================================================

from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field
from mt_metadata.common import (
    DataTypeEnum,
    ChannelLayoutEnum,
    Fdsn,
    Location,
    Person,
    Declination,
    GeographicLocation,
)


# =====================================================


class Station(MetadataBase):
    channel_layout: Annotated[
        ChannelLayoutEnum | None,
        Field(
            default=None,
            description="How the station channels were laid out.",
            examples="x",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    channels_recorded: Annotated[
        str,
        Field(
            default=[],
            type="string",
            items={"type": "string"},
            description="List of components recorded by the station. Should be a summary of all channels recorded. Dropped channels will be recorded in Run metadata.",
            examples='"[ Ex, Ey, Hx, Hy, Hz, T]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments on the station.",
            examples="5 runs",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    data_type: Annotated[
        DataTypeEnum,
        Field(
            default=BBMT,
            description="Type of data recorded. If multiple types input as a comma separated list.",
            examples="BBMT",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    geographic_name: Annotated[
        str,
        Field(
            default="",
            description="Closest geographic name to the station, usually a city, but could be another common geographic location.",
            examples='"Whitehorse, YK"',
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Station ID name.  This should be an alpha numeric name that is typically 5-6 characters long.  Commonly the project name in 2 or 3 letters and the station number.",
            examples="MT001",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    run_list: Annotated[
        str,
        Field(
            default=[],
            type="string",
            items={"type": "string"},
            description="List of runs recorded by the station. Should be a summary of all runs recorded.",
            examples='"[ mt001a, mt001b, mt001c ]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
