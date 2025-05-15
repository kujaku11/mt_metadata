# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Mtft24(MetadataBase):
    version: Annotated[
        str,
        Field(
            default="",
            description="Version of MT Edit and date",
            examples="3.10m applied 2021/01/27",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
