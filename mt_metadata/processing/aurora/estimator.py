# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class EngineEnum(StrEnumerationBase):
    RME_RR = "RME_RR"
    RME = "RME"
    other = "other"


class Estimator(MetadataBase):
    engine: Annotated[
        EngineEnum,
        Field(
            default=EngineEnum.RME_RR,
            description="The transfer function estimator engine",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["RME_RR"],
            },
        ),
    ]

    estimate_per_channel: Annotated[
        bool,
        Field(
            default=True,
            description="Estimate per channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["True"],
            },
        ),
    ]
