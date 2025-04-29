# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class CoefficientFilter(MetadataBase):
    gain: Annotated[
        float,
        Field(
            default=1.0,
            description="Scale factor for a simple coefficient filter.",
            examples="100",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
