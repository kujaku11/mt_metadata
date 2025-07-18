# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Run(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="run ID",
            alias=None,
            json_schema_extra={
                "examples": "['001']",
                "units": None,
                "required": True,
            },
        ),
    ]

    input_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="List of input channels (source)",
            alias=None,
            json_schema_extra={
                "examples": "['hx, hy']",
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="List of output channels (response)",
            alias=None,
            json_schema_extra={
                "examples": "['ex, ey, hz']",
                "units": None,
                "required": True,
            },
        ),
    ]

    time_periods: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="List of time periods to process",
            alias=None,
            json_schema_extra={
                "examples": "['']",
                "units": None,
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="sample rate of the run",
            alias=None,
            json_schema_extra={
                "examples": "['1']",
                "units": "samples per second",
                "required": True,
            },
        ),
    ]
