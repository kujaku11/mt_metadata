# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.mttime import MTime


# =====================================================
class TypeEnum(str, Enum):
    boxcar = "boxcar"
    triang = "triang"
    blackman = "blackman"
    hamming = "hamming"
    hann = "hann"
    bartlett = "bartlett"
    flattop = "flattop"
    parzen = "parzen"
    bohman = "bohman"
    blackmanharris = "blackmanharris"
    nuttall = "nuttall"
    barthann = "barthann"
    kaiser = "kaiser"
    gaussian = "gaussian"
    general_gaussian = "general_gaussian"
    slepian = "slepian"
    chebwin = "chebwin"
    dpss = "dpss"


class ClockZeroTypeEnum(str, Enum):
    user_specified = "user specified"
    data_start = "data start"
    ignore = "ignore"


class Window(MetadataBase):
    num_samples: Annotated[
        int,
        Field(
            default=None,
            description="Number of samples in a single window",
            examples=["256"],
            alias=None,
            json_schema_extra={
                "units": "samples",
                "required": True,
            },
        ),
    ]

    overlap: Annotated[
        int,
        Field(
            default=None,
            description="Number of samples overlapped by adjacent windows",
            examples=["32"],
            alias=None,
            json_schema_extra={
                "units": "samples",
                "required": True,
            },
        ),
    ]

    type: Annotated[
        TypeEnum,
        Field(
            default="boxcar",
            description="name of the window type",
            examples=["hamming"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    clock_zero_type: Annotated[
        ClockZeroTypeEnum,
        Field(
            default="ignore",
            description="how the clock-zero is specified",
            examples=["user specified"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    clock_zero: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Start date and time of the first data window",
            examples=["2020-02-01T09:23:45.453670+00:00"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    normalized: Annotated[
        bool,
        Field(
            default=True,
            description="True if the window shall be normalized so the sum of the coefficients is 1",
            examples=[False],
            alias=["normalised"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("clock_zero", mode="before")
    @classmethod
    def validate_clock_zero(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
