# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Channel(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="channel ID",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["mt001"],
            },
        ),
    ]

    scale_factor: Annotated[
        float,
        Field(
            default=1.0,
            description="scale factor of the channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10.0"],
            },
        ),
    ]
