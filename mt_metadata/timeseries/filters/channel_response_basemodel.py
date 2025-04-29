# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class ChannelResponse(MetadataBase):
    normalization_frequency: Annotated[
        float,
        Field(
            default=0.0,
            description="Pass band frequency",
            examples="100",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]
