# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field
import numpy as np


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
            default="low cut",
            description="Specify which side of a threshold should downweighted.",
            examples=["low cut"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    half_window_style: Annotated[
        HalfWindowStyleEnum,
        Field(
            default="hann",
            description="What taper to use between the 0 (rejected) and 1 (accepted) values.",
            examples=["hann"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    transition_lower_bound: Annotated[
        float,
        Field(
            default=-np.inf,
            description="a refernece point for where the function begins to change from 0 to 1 or from 1 to zero",
            examples=["0.3"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    transition_upper_bound: Annotated[
        float,
        Field(
            default=np.inf,
            description="a refernece point for where the function finishes changing from 0 to 1 or from 1 to zero",
            examples=["0.999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
