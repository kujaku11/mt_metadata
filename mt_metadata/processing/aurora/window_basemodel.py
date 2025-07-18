# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


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
        str | None,
        Field(
            default=None,
            description="Start date and time of the first data window",
            examples=["2020-02-01T09:23:45.453670+00:00"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
