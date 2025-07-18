# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class ThresholdEnum(str, Enum):
    low_cut = "low cut"
    high_cut = "high cut"


class HalfWindowStyleEnum(str, Enum):
    hamming = "hamming"
    hann = "hann"
    rectangle = "rectangle"


class FeatureWeightingWindow(MetadataBase):
    threshold: Annotated[
        ThresholdEnum,
        Field(
            default="",
            description="Specify which side of a threshold should downweighted.",
            alias=None,
            json_schema_extra={
                "examples": "['low cut']",
                "units": None,
                "required": True,
            },
        ),
    ]

    half_window_style: Annotated[
        HalfWindowStyleEnum,
        Field(
            default="",
            description="What taper to use between the 0 (rejected) and 1 (accepted) values.",
            alias=None,
            json_schema_extra={
                "examples": "['hann']",
                "units": None,
                "required": True,
            },
        ),
    ]

    transition_lower_bound: Annotated[
        float,
        Field(
            default=-inf,
            description="a refernece point for where the function begins to change from 0 to 1 or from 1 to zero",
            alias=None,
            json_schema_extra={
                "examples": "['0.3']",
                "units": None,
                "required": True,
            },
        ),
    ]

    transition_upper_bound: Annotated[
        float,
        Field(
            default=inf,
            description="a refernece point for where the function finishes changing from 0 to 1 or from 1 to zero",
            alias=None,
            json_schema_extra={
                "examples": "['0.999']",
                "units": None,
                "required": True,
            },
        ),
    ]
