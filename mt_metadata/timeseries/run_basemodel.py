# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class DataTypeEnum(str, Enum):
    RMT = "RMT"
    AMT = "AMT"
    BBMT = "BBMT"
    LPMT = "LPMT"
    ULPMT = "ULPMT"
    other = "other"


class Run(MetadataBase):
    channels_recorded_auxiliary: Annotated[
        str,
        Field(
            default=[],
            type="string",
            items={"type": "string"},
            description="List of auxiliary channels recorded",
            examples="[T]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_recorded_electric: Annotated[
        str,
        Field(
            default=[],
            type="string",
            items={"type": "string"},
            description="List of electric channels recorded",
            examples='"[Ex , Ey]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_recorded_magnetic: Annotated[
        str,
        Field(
            default=[],
            type="string",
            items={"type": "string"},
            description="List of magnetic channels recorded",
            examples='"[Hx , Hy , Hz]"',
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
            description="Any comments on the run.",
            examples="cows chewed cables",
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
            description="Type of data recorded for this run.",
            examples="BBMT",
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
            description="Run ID should be station name followed by a number or character.  Characters should only be used if the run number is small, if the run number is high consider using digits with zeros.  For example if you have 100 runs the run ID could be 001 or {station}001.",
            examples="001",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate for the run",
            examples="100",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]
