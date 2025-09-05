# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class HalfWindowStyleEnum(StrEnumerationBase):
    hamming = "hamming"
    hann = "hann"
    rectangle = "rectangle"
    blackman = "blackman"


class ActivationStyleEnum(StrEnumerationBase):
    linear = "linear"
    sigmoid = "sigmoid"
    tanh = "tanh"
    relu = "relu"
    hard_tanh = "hard_tanh"
    hard_sigmoid = "hard_sigmoid"


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
