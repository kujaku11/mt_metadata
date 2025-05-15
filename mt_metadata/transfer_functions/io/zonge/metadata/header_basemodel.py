# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Header(MetadataBase):
    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Station name",
            examples="null",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
