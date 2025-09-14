# =====================================================
# Imports
# =====================================================
from typing import Annotated, Union

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.processing.window import Window


# =====================================================
class MethodEnum(StrEnumerationBase):
    fft = "fft"
    wavelet = "wavelet"
    other = "other"


class PerWindowDetrendTypeEnum(StrEnumerationBase):
    linear = "linear"
    constant = "constant"
    null = ""


class PreFftDetrendTypeEnum(StrEnumerationBase):
    linear = "linear"
    other = "other"
    null = ""


class PrewhiteningTypeEnum(StrEnumerationBase):
    first_difference = "first difference"
    other = "other"


class ShortTimeFourierTransform(MetadataBase):
    harmonic_indices: Annotated[
        Union[int, list[int], None],
        Field(
            default=None,
            description="List of harmonics indices kept, if all use -1",
            examples=[[0, 4, 8]],
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

    per_window_detrend_type: Annotated[
        PerWindowDetrendTypeEnum,
        Field(
            default="",
            description="Additional detrending applied per window.  Not available for standard scipy spectrogram -- placholder for ARMA prewhitening.",
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

    recoloring: Annotated[
        bool,
        Field(
            default=True,
            description="Whether the data are recolored [True] or not [False].",
            examples=[True],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    window: Annotated[
        Window,
        Field(
            default_factory=Window,  # type: ignore
            description="Window settings",
            examples=["Window()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]


# what is the point of this main function?
# def main():
#     stft = ShortTimeFourierTransform()


# if __name__ == "__main__":
#     main()
