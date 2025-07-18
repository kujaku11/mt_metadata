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
            examples=["10"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
