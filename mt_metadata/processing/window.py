"""
Updated 2025-01-02: kkappler, adding methods to generate taper values.  In future this class
   can replace ApodizationWindow in aurora.
"""

# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
import scipy.signal as ssig
from pydantic import AliasChoices, computed_field, Field, field_validator, PrivateAttr

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.common.mttime import MTime


# =====================================================
class TypeEnum(StrEnumerationBase):
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


class ClockZeroTypeEnum(StrEnumerationBase):
    user_specified = "user specified"
    data_start = "data start"
    ignore = "ignore"


class Window(MetadataBase):
    _taper: np.ndarray | None = PrivateAttr(None)
    num_samples: Annotated[
        int,
        Field(
            default=256,
            description="Number of samples in a single window",
            alias=None,
            json_schema_extra={
                "units": "samples",
                "required": True,
                "examples": ["256"],
            },
        ),
    ]

    overlap: Annotated[
        int,
        Field(
            default=32,
            description="Number of samples overlapped by adjacent windows",
            alias=None,
            json_schema_extra={
                "units": "samples",
                "required": True,
                "examples": ["32"],
            },
        ),
    ]

    type: Annotated[
        TypeEnum,
        Field(
            default="boxcar",
            description="name of the window type",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hamming"],
            },
        ),
    ]

    clock_zero_type: Annotated[
        ClockZeroTypeEnum,
        Field(
            default="ignore",
            description="how the clock-zero is specified",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["user specified"],
            },
        ),
    ]

    clock_zero: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Start date and time of the first data window",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["2020-02-01T09:23:45.453670+00:00"],
            },
        ),
    ]

    normalized: Annotated[
        bool,
        Field(
            default=True,
            description="True if the window shall be normalized so the sum of the coefficients is 1",
            validation_alias=AliasChoices("normalised", "normalized"),
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [False],
            },
        ),
    ]

    additional_args: Annotated[
        dict,
        Field(
            default_factory=dict,
            description="Additional arguments for the window function",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [{"param": "value"}],
            },
        ),
    ]

    @field_validator("clock_zero", mode="before")
    @classmethod
    def validate_clock_zero(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @computed_field
    @property
    def num_samples_advance(self) -> int:
        return self.num_samples - self.overlap

    def fft_harmonics(self, sample_rate: float) -> np.ndarray:
        """
            Returns the frequencies for an fft..
        :param sample_rate:
        :return:
        """
        return get_fft_harmonics(
            samples_per_window=self.num_samples, sample_rate=sample_rate
        )

    def taper(self) -> np.ndarray:
        """
            Get's the window coeffcients. via wrapper call to scipy.signal

            Note: see scipy.signal.get_window for a description of what is expected in args[1:]. http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.get_window.html

        Returns
        -------

        """
        if self._taper is None:
            # Repackaging the args so that scipy.signal.get_window() accepts all cases
            window_args = [v for k, v in self.additional_args.items()]
            window_args.insert(0, self.type)
            window_args = tuple(window_args)

            taper = ssig.get_window(window_args, self.num_samples)

            if self.normalized:
                taper /= np.sum(taper)

            self._taper = taper

        return self._taper


def get_fft_harmonics(samples_per_window: int, sample_rate: float) -> np.ndarray:
    """
    Works for odd and even number of points.

    Development notes:
    - Could be modified with arguments to support one_sided, two_sided, ignore_dc
    ignore_nyquist, and etc.  Consider taking FrequencyBands as an argument.
    - This function was in decimation_level, but there were circular import issues.
    The function needs only a window length and sample rate, so putting it here for now.
    - TODO: switch to using np.fft.rfftfreq

    Parameters
    ----------
    samples_per_window: int
        Number of samples in a window that will be Fourier transformed.
    sample_rate: float
            Inverse of time step between samples; Samples per second in Hz.

    Returns
    -------
    harmonic_frequencies: numpy array
        The frequencies that the fft will be computed.
        These are one-sided (positive frequencies only)
        Does _not_ return Nyquist
        Does return DC component
    """
    delta_t = 1.0 / sample_rate
    harmonic_frequencies = np.fft.fftfreq(samples_per_window, d=delta_t)
    n_fft_harmonics = int(samples_per_window / 2)  # no bin at Nyquist,
    harmonic_frequencies = harmonic_frequencies[0:n_fft_harmonics]
    return harmonic_frequencies
