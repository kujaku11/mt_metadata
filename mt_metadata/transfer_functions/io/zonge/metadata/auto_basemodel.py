# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class PhaseFlipEnum(str, Enum):
    yes = "yes"
    no = "no"


class Auto(MetadataBase):
    phase_flip: Annotated[
        PhaseFlipEnum,
        Field(
            default="yes",
            description="Was phase automatically flipped in processing",
            examples="yes",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
