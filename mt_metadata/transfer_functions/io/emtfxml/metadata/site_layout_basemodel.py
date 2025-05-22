# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class SiteLayout(MetadataBase):
    input_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of input channels for transfer function estimation",
            examples=["[Magnetic(hx), Magnetic(hy)]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of output channels for transfer function estimation",
            examples=["[Electric(ex), Electric(ey), Magnetic(hz)]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
