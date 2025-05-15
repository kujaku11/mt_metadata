# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class SmoothEnum(str, Enum):
    robust = "robust"
    normal = "normal"
    None = "None"
    minimal = "minimal"


class ToZMagEnum(str, Enum):
    no = "no"
    yes = "yes"


class PhaseSlope(MetadataBase):
    smooth: Annotated[
        SmoothEnum,
        Field(
            default="None",
            description="Type of smoothing for phase slope algorithm",
            examples="robust",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    to_z_mag: Annotated[
        ToZMagEnum,
        Field(
            default="no",
            description="Was hz used for smoothing for phase slope algorithm",
            examples="no",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
