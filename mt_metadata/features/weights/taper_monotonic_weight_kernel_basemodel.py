# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class HalfWindowStyleEnum(str, Enum):
    hamming = "hamming"
    hann = "hann"
    rectangle = "rectangle"
    blackman = "blackman"


class TaperMonotonicWeightKernel(MetadataBase):
    half_window_style: Annotated[
        HalfWindowStyleEnum,
        Field(
            default="rectangle",
            description="Tapering/activation function to use between transition bounds.",
            examples=["hann"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
