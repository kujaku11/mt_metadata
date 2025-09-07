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
            default="RME_RR",
            description="The transfer function estimator engine",
            examples=["RME_RR"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    estimate_per_channel: Annotated[
        bool,
        Field(
            default=True,
            description="Estimate per channel",
            examples=["True"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
