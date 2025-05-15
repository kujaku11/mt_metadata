# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Stations(MetadataBase):
    remote: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of remote sites",
            examples="10",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
