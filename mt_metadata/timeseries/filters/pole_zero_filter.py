# -*- coding: utf-8 -*-
"""
.. py:module:: pole_zero_filter
    :synopsis: Deal with Pole Zero Filters 

.. codeauthor:: Jared Peacock <jpeacock@usgs.gov>

"""
import copy
import numpy as np
import obspy
import scipy.signal as signal

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import OBSPY_MAPPING
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("pole_zero_filter", SCHEMA_FN_PATHS))
# =============================================================================

obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
obspy_mapping["_zeros"] = "zeros"
obspy_mapping["_poles"] = "poles"
obspy_mapping["normalization_factor"] = "normalization_factor"


class PoleZeroFilter(FilterBase):
    def __init__(self, **kwargs):

        super().__init__()

        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        self.type = "zpk"

        self.obspy_mapping = obspy_mapping

    @property
    def poles(self):
        """
        
        :return: array of poles
        :rtype: np.ndarray

        """
        return self._poles

    @poles.setter
    def poles(self, value):
        """
        Set the poles, make sure the input is validated
        :param value: pole values
        :type value: list, tuple, np.ndarray

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._poles = np.array(value, dtype=complex)

        elif isinstance(value, str):
            self._poles = np.array(value.split(","), dtype=complex)

        else:
            self._poles = np.empty(0)

    @property
    def zeros(self):
        """
        
        :return: array of zeros
        :rtype: np.ndarray

        """
        return self._zeros

    @zeros.setter
    def zeros(self, value):
        """
        
        Set the zeros, make sure the input is validated
        :param value: zero values
        :type value: list, tuple, np.ndarray

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._zeros = np.array(value, dtype=complex)

        elif isinstance(value, str):
            self._zeros = np.array(value.split(","), dtype=complex)

        else:
            self._zeros = np.empty(0)

    @property
    def n_poles(self):
        """
        :return: number of poles
        :rtype: integer
        
        """
        return len(self._poles)

    @property
    def n_zeros(self):
        """
        
        :return: number of zeros
        :rtype: integer

        """
        return len(self._zeros)

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
            self.units_in,
            self.units_out,
            pz_type,
            normalization_frequency,
            self.zeros,
            self.poles,
            name=self.name,
            normalization_factor=self.normalization_factor,
            description=self.get_filter_description(),
            input_units_description=self._units_in_obj.name,
            output_units_description=self._units_out_obj.name,
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
        angular_frequencies = 2 * np.pi * frequencies
        w, h = signal.freqs_zpk(
            self.zeros, self.poles, self.total_gain, worN=angular_frequencies
        )
        return h

    def normalization_frequency(self, estimate="mean", window_len=5, tol=1e-4):
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
        pass_band = self.pass_band(window_len, tol)

        if len(pass_band) == 0:
            return np.NAN

        if estimate == "mean":
            return pass_band.mean()

        elif estimate == "median":
            return np.median(pass_band)

        elif estimate == "min":
            return pass_band.min()

        elif estimate == "max":
            return pass_band.max()
