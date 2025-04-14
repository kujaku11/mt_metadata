# =====================================================
# Imports
# =====================================================
from typing import Annotated, Any

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class TimingSystem(MetadataBase):
    comments: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="Any comment on the timing system.",
            examples="GPS locked with internal quartz clock",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    drift: Annotated[
        Any,
        Field(
            default=0.0,
            type="float",
            description="Estimated drift of the timing system.",
            examples="0.001",
            alias=None,
            json_schema_extra={
                "units": "seconds",
                "required": True,
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default=GPS,
            type="string",
            description="Type of timing system.",
            examples="GPS",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    uncertainty: Annotated[
        Any,
        Field(
            default=0.0,
            type="float",
            description="Estimated uncertainty of the timing system.",
            examples="0.0002",
            alias=None,
            json_schema_extra={
                "units": "seconds",
                "required": True,
            },
        ),
    ]

    n_satellites: Annotated[
        Any | None,
        Field(
            default=None,
            type="int",
            description="Number of satellites used for timing.",
            examples="6",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
