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
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["0"],
            },
        ),
    ]

    theta2: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation angle for block y",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["90"],
            },
        ),
    ]

    phi: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation angle for block",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["0"],
            },
        ),
    ]
