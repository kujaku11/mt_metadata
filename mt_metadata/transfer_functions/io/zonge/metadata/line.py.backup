# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Line(MetadataBase):
    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the line data collected on",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    number: Annotated[
        int | None,
        Field(
            default=None,
            description="Line number",
            examples=[0],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
