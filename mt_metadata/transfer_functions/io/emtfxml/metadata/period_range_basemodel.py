# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class PeriodRange(MetadataBase):
    min: Annotated[
        float,
        Field(
            default=0.0,
            description="minimum period",
            examples=['"4.5E-5"'],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    max: Annotated[
        float,
        Field(
            default=0.0,
            description="maxmimu period",
            examples=['"4.5E5"'],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]
