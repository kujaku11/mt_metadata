# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class TimeDelayFilter(MetadataBase):
    delay: Annotated[
        float,
        Field(
            default=0.0,
            description="The delay interval of the filter. This should be a single number.",
            examples="-0.201",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "second",
                "required": True,
            },
        ),
    ]
