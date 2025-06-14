# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class CenterAveragingTypeEnum(str, Enum):
    arithmetic = "arithmetic"
    geometric = "geometric"


class ClosedEnum(str, Enum):
    left = "left"
    right = "right"
    both = "both"


class Band(MetadataBase):
    decimation_level: Annotated[
        int,
        Field(
            default=None,
            description="Decimation level for the band",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    index_max: Annotated[
        int,
        Field(
            default=None,
            description="maximum band index",
            examples="10",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    index_min: Annotated[
        int,
        Field(
            default=None,
            description="minimum band index",
            examples="10",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    frequency_max: Annotated[
        float,
        Field(
            default=0.0,
            description="maximum band frequency",
            examples="0.04296875",
            alias=None,
            json_schema_extra={
                "units": "Hertz",
                "required": True,
            },
        ),
    ]

    frequency_min: Annotated[
        float,
        Field(
            default=0.0,
            description="minimum band frequency",
            examples="0.03515625",
            alias=None,
            json_schema_extra={
                "units": "Hertz",
                "required": True,
            },
        ),
    ]

    center_averaging_type: Annotated[
        CenterAveragingTypeEnum,
        Field(
            default="geometric",
            description="type of average to apply when computing the band center",
            examples="geometric",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    closed: Annotated[
        ClosedEnum,
        Field(
            default="left",
            description="whether interval is open or closed",
            examples="left",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
