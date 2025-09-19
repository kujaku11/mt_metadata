# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class ThresholdEnum(StrEnumerationBase):
    low_cut = "low cut"
    high_cut = "high cut"


class HalfWindowStyleEnum(StrEnumerationBase):
    hamming = "hamming"
    hann = "hann"
    rectangle = "rectangle"


class FeatureWeightingWindow(MetadataBase):
    threshold: Annotated[
        ThresholdEnum,
        Field(
            default="low cut",
            description="Specify which side of a threshold should downweighted.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["low cut"],
            },
        ),
    ]

    half_window_style: Annotated[
        HalfWindowStyleEnum,
        Field(
            default="hann",
            description="What taper to use between the 0 (rejected) and 1 (accepted) values.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hann"],
            },
        ),
    ]

    transition_lower_bound: Annotated[
        float,
        Field(
            default=-np.inf,
            description="a refernece point for where the function begins to change from 0 to 1 or from 1 to zero",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.3"],
            },
        ),
    ]

    transition_upper_bound: Annotated[
        float,
        Field(
            default=np.inf,
            description="a refernece point for where the function finishes changing from 0 to 1 or from 1 to zero",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.999"],
            },
        ),
    ]
