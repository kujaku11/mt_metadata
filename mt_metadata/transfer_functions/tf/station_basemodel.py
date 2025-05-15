# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment


# =====================================================
class ChannelLayoutEnum(str, Enum):
    L = "L"
    X = "X"
    other = "other"


class DataTypeEnum(str, Enum):
    RMT = "RMT"
    AMT = "AMT"
    BBMT = "BBMT"
    LPMT = "LPMT"
    ULPMT = "ULPMT"
    other = "other"


class Station(MetadataBase):
    channel_layout: Annotated[
        ChannelLayoutEnum | None,
        Field(
            default=None,
            description="how the station was laid out",
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
            default="[]",
            items={"type": "string"},
            description="list of components recorded by the station. Should be a summary of all channels recorded dropped channels will be recorded in Run metadata.",
            examples='"[ Ex, Ey, Hx, Hy, Hz, T]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),
            description="any comments on the station",
            examples="5 runs",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data_type: Annotated[
        DataTypeEnum,
        Field(
            default="BBMT",
            description="type of data recorded. If multiple types input as a comma separated list",
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
            description="closest geographic name to the station",
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
            default="[]",
            items={"type": "string"},
            description="list of runs recorded by the station. Should be a summary of all runss recorded",
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
