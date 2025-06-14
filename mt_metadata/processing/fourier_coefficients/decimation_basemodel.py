# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated, Any, List

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class MethodEnum(str, Enum):
    fft = "fft"
    wavelet = "wavelet"
    other = "other"


class PrewhiteningTypeEnum(str, Enum):
    first_difference = "first difference"
    other = "other"


class Decimation(MetadataBase):
    decimation_level: Annotated[
        int,
        Field(
            default=None,
            description="Decimation level, must be a non-negative integer starting at 0",
            examples="1",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Decimation level ID",
            examples="1",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_estimated: Annotated[
        List[Any],
        Field(
            default=None,
            items={"type": "string"},
            description="list of channels",
            examples="[ex, hy]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sample_rate_decimation: Annotated[
        Any,
        Field(
            default=1.0,
            description="Sample rate of the decimation level.",
            examples=60,
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    decimation_factor: Annotated[
        int,
        Field(
            default=None,
            description="Decimation factor between initial sample rate and decimation sample rate.",
            examples=4,
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    min_num_stft_windows: Annotated[
        int,
        Field(
            default=None,
            description="How many FFT windows must be available for the time series to valid for STFT.",
            examples=4,
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    method: Annotated[
        MethodEnum,
        Field(
            default="fft",
            description="Fourier transform method",
            examples="fft",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    anti_alias_filter: Annotated[
        str,
        Field(
            default="default",
            description="Type of anti alias filter for decimation.",
            examples="default",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    pre_fft_detrend_type: Annotated[
        str,
        Field(
            default="linear",
            description="Type of detrend method before FFT.",
            examples="linear",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    prewhitening_type: Annotated[
        PrewhiteningTypeEnum,
        Field(
            default="first difference",
            description="Prewhitening method to be applied",
            examples="first difference",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    recoloring: Annotated[
        Any,
        Field(
            default=None,
            description="Whether the data are recolored [True] or not [False].",
            examples=True,
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    harmonic_indices: Annotated[
        List[Any],
        Field(
            default=None,
            items={"type": "integer"},
            description="List of harmonics indices kept, if all use -1",
            examples=[0, 4, 8],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
