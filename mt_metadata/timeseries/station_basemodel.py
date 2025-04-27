# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field, ValidationInfo, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    DataTypeEnum,
    ChannelLayoutEnum,
    StationLocation,
    Copyright,
    Fdsn,
    Instrument,
    Provenance,
    TimePeriod,
    Person,
    Orientation,
)
from mt_metadata.utils.list_dict import ListDict

# =====================================================


class Station(MetadataBase):
    channel_layout: Annotated[
        ChannelLayoutEnum | None,
        Field(
            default=None,
            description="How the station channels were laid out.",
            examples="x",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    channels_recorded: Annotated[
        str,
        Field(
            default=[],
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

    comments: Comment
    data_type: Annotated[
        DataTypeEnum,
        Field(
            default=BBMT,
            description="Type of data recorded. If multiple types input as a comma separated list.",
            examples="BBMT",
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

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value
