# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class MethodEnum(str, Enum):
    default = "default"
    other = "other"


class Decimation(MetadataBase):
    level: Annotated[
        int,
        Field(
            default=None,
            description="Decimation level in sequential order",
            examples="0",
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
            description="Decimation factor",
            examples="1",
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
            examples="default",
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
            description="Sample rate of the data after decimation.",
            examples="256",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]
