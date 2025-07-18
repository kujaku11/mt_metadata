# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Decimation(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Decimation level ID",
            alias=None,
            json_schema_extra={
                "examples": "['1']",
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_estimated: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of channels",
            alias=None,
            json_schema_extra={
                "examples": "['[ex, hy]']",
                "units": None,
                "required": True,
            },
        ),
    ]
