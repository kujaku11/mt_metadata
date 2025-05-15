# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class PrimaryData(MetadataBase):
    filename: Annotated[
        str,
        Field(
            default="",
            description="file name of the figure file that displays the data",
            examples="example.png",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
