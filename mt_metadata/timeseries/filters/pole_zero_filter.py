# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
from pydantic import Field, field_validator, ValidationInfo


try:
    import obspy
except ImportError:
    obspy = None
import scipy.signal as signal

from mt_metadata.base.helpers import object_to_array, requires
from mt_metadata.timeseries.filters import FilterBase, get_base_obspy_mapping


# =====================================================
class PoleZeroFilter(FilterBase):
    _filter_type: str = "zpk"
    type: Annotated[
        str,
        Field(
            default="zpk",
            description="Type of filter.  Must be 'zpk'",
            examples="zpk",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    poles: Annotated[
        np.ndarray | list[complex] | complex,
        Field(
            default_factory=lambda: np.empty(0, dtype=complex),
            description="The complex-valued poles associated with the filter response.",
            examples='"[-1/4., -0.1+j*0.3, -0.1-j*0.3]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    zeros: Annotated[
        np.ndarray | list[complex] | complex,
        Field(
            default_factory=lambda: np.empty(0, dtype=complex),
            description="The complex-valued zeros associated with the filter response.",
            examples='"[0.0, ]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    normalization_factor: Annotated[
        float,
        Field(
            default=1.0,
            description="The scale factor to apply to the monic response.",
            examples='"[-1000.1]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("poles", "zeros", mode="before")
    @classmethod
    def validate_input_arrays(cls, value, info: ValidationInfo) -> np.ndarray:
        """
        Validate that the input is a list, tuple, or np.ndarray and convert to np.ndarray.
        """
        return object_to_array(value, dtype=complex)

    @property
    def n_poles(self):
        """
        :return: number of poles
        :rtype: integer

        """
        return len(self.poles)

    @property
    def n_zeros(self):
        """

        :return: number of zeros
        :rtype: integer

        """
        return len(self.zeros)

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        mapping["_zeros"] = "zeros"
        mapping["_poles"] = "poles"
        mapping["normalization_factor"] = "normalization_factor"
        return mapping

    def zero_pole_gain_representation(self):
        """

        :return: scipy.signal.ZPG object
        :rtype: :class:`scipy.signal.ZerosPolesGain`

        """
        zpg = signal.ZerosPolesGain(self.zeros, self.poles, self.normalization_factor)
        return zpg

    @property
    def total_gain(self):
        """

        :return: total gain of the filter
        :rtype: float

        """
        return self.gain * self.normalization_factor

    @requires(obspy=obspy)
    def to_obspy(
        self,
        stage_number=1,
        pz_type="LAPLACE (RADIANS/SECOND)",
        normalization_frequency=1,
        sample_rate=1,
    ):
        """
        Convert the filter to an obspy filter

        :param stage_number: sequential stage number, defaults to 1
        :type stage_number: integer, optional
        :param pz_type: Pole Zero type, defaults to "LAPLACE (RADIANS/SECOND)"
        :type pz_type: string, optional
        :param normalization_frequency: Normalization frequency, defaults to 1
        :type normalization_frequency: float, optional
        :param sample_rate: sample rate, defaults to 1
        :type sample_rate: float, optional
        :return: Obspy stage filter
        :rtype: :class:`obspy.core.inventory.PolesZerosResponseStage`

        """
        if self.zeros is None:
            self.zeros = []
        if self.poles is None:
            self.poles = []

        rs = obspy.core.inventory.PolesZerosResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in_object.symbol,
            self.units_out_object.symbol,
            pz_type,
            normalization_frequency,
            self.zeros,
            self.poles,
            name=self.name,
            normalization_factor=self.normalization_factor,
            description=self.get_filter_description(),
            input_units_description=self.units_in_object.name,
            output_units_description=self.units_out_object.name,
        )

        return rs

    def complex_response(self, frequencies, **kwargs):
        """
        Computes complex response for given frequency range
        :param frequencies: array of frequencies to estimate the response
        :type frequencies: np.ndarray

        :return: complex response
        :rtype: np.ndarray

        """
        angular_frequencies = 2 * np.pi * np.array(frequencies)
        w, h = signal.freqs_zpk(
            self.zeros, self.poles, self.total_gain, worN=angular_frequencies
        )

        return h

    def normalization_frequency(
        self,
        frequencies: np.ndarray = np.logspace(-4, 4, 32),
        estimate: str = "mean",
        window_len: int = 5,
        tol: float = 1e-4,
    ) -> float:
        """
        Try to estimate the normalization frequency in the pass band
        by finding the flattest spot in the amplitude.

        The flattest spot is determined by calculating a sliding window
        with length `window_len` and estimating normalized std.

        ..note:: This only works for simple filters with
        on flat pass band.

        :param window_len: length of sliding window in points
        :type window_len: integer

        :param tol: the ratio of the mean/std should be around 1
         tol is the range around 1 to find the flat part of the curve.
        :type tol: float

        :return: estimated normalization frequency Hz
        :rtype: float

        """
        pass_band = self.pass_band(frequencies, window_len, tol)
        if pass_band is None:
            return np.NAN
        if pass_band.size == 0:
            return np.NAN

        if estimate == "mean":
            return pass_band.mean()

        elif estimate == "median":
            return np.median(pass_band)

        elif estimate == "min":
            return pass_band.min()

        elif estimate == "max":
            return pass_band.max()
