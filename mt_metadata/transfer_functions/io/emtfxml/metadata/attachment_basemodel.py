# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Attachment(MetadataBase):
    filename: Annotated[
        str,
        Field(
            default="",
            description="file name of the attached file data",
            examples="example.zmm",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    description: Annotated[
        str,
        Field(
            default="",
            description="description of the attached file",
            examples="The original used to produce the XML",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
