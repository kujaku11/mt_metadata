# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Stations(MetadataBase):
    remote: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of remote sites",
            alias=None,
            json_schema_extra={
                "examples": "['10']",
                "units": None,
                "required": True,
            },
        ),
    ]
