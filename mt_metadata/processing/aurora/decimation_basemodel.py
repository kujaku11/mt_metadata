# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class MethodEnum(str, Enum):
    default = "default"
    other = "other"


class Decimation(MetadataBase):
    level: Annotated[
        int,
        Field(
            default=None,
            description="Decimation level, must be a non-negative integer starting at 0",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    factor: Annotated[
        float,
        Field(
            default=1.0,
            description="Decimation factor between parent sample rate and decimated time series sample rate.",
            examples=["4.0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    method: Annotated[
        MethodEnum,
        Field(
            default="default",
            description="Type of decimation",
            examples=["default"],
            alias=None,
            json_schema_extra={
                "units": "",
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of the decimation level data (after decimation).",
            examples=["256"],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    anti_alias_filter: Annotated[
        str,
        Field(
            default="default",
            description="Type of anti alias filter for decimation.",
            examples=["default"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
