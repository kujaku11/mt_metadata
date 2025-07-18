# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class DetrendEnum(str, Enum):
    linear = "linear"
    constant = "constant"


class Coherence(MetadataBase):
    ch1: Annotated[
        str,
        Field(
            default="",
            description="The first channel of two channels in the coherence calculation.",
            examples=["ex"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ch2: Annotated[
        str,
        Field(
            default="",
            description="The second channel of two channels in the coherence calculation.",
            examples=["hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    detrend: Annotated[
        DetrendEnum,
        Field(
            default="linear",
            description="How to detrend the data segments before fft.",
            examples=["constant"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    station1: Annotated[
        str,
        Field(
            default="",
            description="The station associated with the first channel in the coherence calculation.",
            examples=["PKD"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    station2: Annotated[
        str,
        Field(
            default="",
            description="The station associated with the second channel in the coherence calculation.",
            examples=["SAO"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
