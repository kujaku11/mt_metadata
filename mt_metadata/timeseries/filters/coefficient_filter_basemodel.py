# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class CoefficientFilter(MetadataBase):
    gain: Annotated[
        float,
        Field(
            default=1.0,
            description="Scale factor for a simple coefficient filter.",
            examples="100",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
