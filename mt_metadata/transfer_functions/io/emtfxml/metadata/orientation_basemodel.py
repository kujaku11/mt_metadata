# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class LayoutEnum(str, Enum):
    orthogonal = "orthogonal"
    sitelayout = "sitelayout"


class Orientation(MetadataBase):
    angle_to_geographic_north: Annotated[
        float,
        Field(
            default=0.0,
            description="Angle to geographic north of the station orientation",
            examples=0,
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    layout: Annotated[
        LayoutEnum,
        Field(
            default="orthogonal",
            description="Orientation of channels relative to each other",
            examples="orthogonal",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
