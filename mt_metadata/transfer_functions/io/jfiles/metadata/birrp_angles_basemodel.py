# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class BirrpAngles(MetadataBase):
    theta1: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation angle for block x",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    theta2: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation angle for block y",
            examples="90",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    phi: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation angle for block",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]
