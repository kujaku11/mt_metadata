# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class RemoteRef(MetadataBase):
    type: Annotated[
        str,
        Field(
            default="",
            description="type of remote referencing",
            examples="robust multi-station remote referencing",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
