# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Description(MetadataBase):
    description: Annotated[
        str,
        Field(
            default="",
            description="description of what is in the file; default is magnetotelluric transfer functions",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Magnetotelluric Transfer Functions"],
            },
        ),
    ]
