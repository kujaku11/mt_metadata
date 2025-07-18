# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated, Any, List

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class AntiAliasFilterEnum(str, Enum):
    deafult = "deafult"
    other = "other"


class MethodEnum(str, Enum):
    fft = "fft"
    wavelet = "wavelet"
    other = "other"


class PrewhiteningTypeEnum(str, Enum):
    first_difference = "first difference"
    other = "other"


class ExtraPreFftDetrendTypeEnum(str, Enum):
    linear = "linear"
    other = "other"


class PreFftDetrendTypeEnum(str, Enum):
    linear = "linear"
    other = "other"


class SaveFcsTypeEnum(str, Enum):
    h5 = "h5"
    csv = "csv"


class DecimationLevel(MetadataBase):
    anti_alias_filter: Annotated[
        AntiAliasFilterEnum,
        Field(
            default="default",
            description="Name of anti alias filter to be applied",
            examples=["default"],
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
            examples=[True],
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
            examples=[4],
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
            examples=["fft"],
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
            examples=["first difference"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    extra_pre_fft_detrend_type: Annotated[
        ExtraPreFftDetrendTypeEnum,
        Field(
            default="linear",
            description="Extra Pre FFT detrend method to be applied",
            examples=["linear"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    pre_fft_detrend_type: Annotated[
        PreFftDetrendTypeEnum,
        Field(
            default="linear",
            description="Pre FFT detrend method to be applied",
            examples=["linear"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    bands: Annotated[
        List[Any],
        Field(
            default=None,
            items={"type": "integer"},
            description="List of bands",
            examples=["[]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    input_channels: Annotated[
        List[Any],
        Field(
            default=None,
            items={"type": "string"},
            description="list of input channels (sources)",
            examples=["hx, hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        List[Any],
        Field(
            default=None,
            items={"type": "string"},
            description="list of output channels (responses)",
            examples=["ex, ey, hz"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    reference_channels: Annotated[
        List[Any],
        Field(
            default=None,
            items={"type": "string"},
            description="list of reference channels (remote sources)",
            examples=["hx, hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    save_fcs: Annotated[
        Any,
        Field(
            default=None,
            description="Whether the Fourier coefficients are saved [True] or not [False].",
            examples=[True],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    save_fcs_type: Annotated[
        SaveFcsTypeEnum | None,
        Field(
            default=None,
            description="Format to use for fc storage",
            examples=["h5"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
