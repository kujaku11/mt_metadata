# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Run(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="run ID",
            examples=["001"],
            alias=None,
            json_schema_extra={
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
            examples=["hx, hy"],
            alias=None,
            json_schema_extra={
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
            examples=["ex, ey, hz"],
            alias=None,
            json_schema_extra={
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
            examples=[""],
            alias=None,
            json_schema_extra={
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
            examples=["1"],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]
