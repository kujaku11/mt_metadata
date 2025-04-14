# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class ChannelResponse(MetadataBase):
    normalization_frequency: Annotated[
        float,
        Field(
            default=0.0,
            description="Pass band frequency",
            examples="100",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
