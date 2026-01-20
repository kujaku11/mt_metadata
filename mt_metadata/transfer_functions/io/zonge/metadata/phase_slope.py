# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import YesNoEnum


# =====================================================
class SmoothEnum(str, Enum):
    robust = "robust"
    normal = "normal"
    null = "None"
    minimal = "minimal"


class PhaseSlope(MetadataBase):
    smooth: Annotated[
        SmoothEnum,
        Field(
            default=SmoothEnum.null,
            description="Type of smoothing for phase slope algorithm",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["robust"],
            },
        ),
    ]

    to_z_mag: Annotated[
        YesNoEnum,
        Field(
            default=YesNoEnum.no,
            description="Was hz used for smoothing for phase slope algorithm",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["no"],
            },
        ),
    ]
