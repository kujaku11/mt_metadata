# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Stn(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="name of the station",
            examples="1",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
