# -*- coding: utf-8 -*-
"""
.. py:module:: frequency_response_table_filter
    :synopsis: Deal with frequency look-up tables

.. codeauthor:: Jared Peacock <jpeacock@usgs.gov>
.. codeauthor:: Karl Kappler

"""
import numpy as np
from scipy.interpolate import interp1d

from mt_metadata.base.helpers import requires

try:
    from obspy.core.inventory.response import (
        ResponseListResponseStage,
        ResponseListElement,
    )
except ImportError:
    ResponseListResponseStage = ResponseListElement = None

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import get_base_obspy_mapping
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("frequency_response_table_filter", SCHEMA_FN_PATHS))

# =============================================================================


class FrequencyResponseTableFilter(FilterBase):
    """
    Phases should be in radians.

    """

    def __init__(self, **kwargs):
        super().__init__()

        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        self.type = "frequency response table"

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        mapping["amplitudes"] = "_empirical_amplitudes"
        mapping["frequencies"] = "_empirical_frequencies"
        mapping["phases"] = "_empirical_phases"
        return mapping

    @property
    def frequencies(self):
        """

        :return: calibration frequencies
        :rtype: np.ndarray

        """
        return self._empirical_frequencies

    @frequencies.setter
    def frequencies(self, value):
        """
        Set the frequencies, make sure the input is validated

        Linear frequencies
        :param value: Linear Frequencies
        :type value: iterable

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._empirical_frequencies = np.array(value, dtype=float)
        else:
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def amplitudes(self):
        """

        :return: calibrated amplitudes
        :rtype: np.ndarray

        """
        return self._empirical_amplitudes

    @amplitudes.setter
    def amplitudes(self, value):
        """
        Set the amplitudes, make sure the input is validated
        :param value: calibrated amplitudes
        :type value: np.ndarray, list, tuple

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._empirical_amplitudes = np.array(value, dtype=float)

        else:
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def phases(self):
        """
        Should be in units of radians

        :return: calibrated phases
        :rtype: np.ndarray

        """
        return self._empirical_phases

    @phases.setter
    def phases(self, value):
        """
        Set the phases, make sure the input is validated

        The units should be radians

        :param value: calibrated phases
        :type value: np.ndarray

        """

        if isinstance(value, (list, tuple, np.ndarray)):
            self._empirical_phases = np.array(value, dtype=float)

            if self._empirical_phases.size > 0:
                if self._empirical_phases.mean() > 1000 * np.pi / 2:
                    self.logger.warning(
                        "Phases appear to be in milli radians attempting to convert to radians"
                    )
                    self._empirical_phases = self._empirical_phases / 1000

                elif np.abs(self._empirical_phases).max() > 6 * np.pi:
                    self.logger.warning(
                        "Phases appear to be in degrees attempting to convert to radians"
                    )
                    self._empirical_phases = np.deg2rad(self._empirical_phases)

        else:
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def min_frequency(self):
        """

        :return: minimum frequency
        :rtype: float

        """
        return self._empirical_frequencies.min()

    @property
    def max_frequency(self):
        """

        :return: maximum frequency
        :rtype: float

        """
        return self._empirical_frequencies.max()

    @requires(obspy=(ResponseListResponseStage and ResponseListElement))
    def to_obspy(
        self,
        stage_number=1,
        normalization_frequency=1,
        sample_rate=1,
    ):
        """
        Convert to an obspy stage

        :param stage_number: sequential stage number, defaults to 1
        :type stage_number: integer, optional
        :param normalization_frequency: Normalization frequency, defaults to 1
        :type normalization_frequency: float, optional
        :param sample_rate: sample rate, defaults to 1
        :type sample_rate: float, optional
        :return: Obspy stage filter
        :rtype: :class:`obspy.core.inventory.ResponseListResponseStage`

        """
        response_elements = []
        # phase needs to be in degrees.
        if np.abs(self.phases).max() < 2 * np.pi:
            phases = np.rad2deg(self.phases)
        else:
            phases = self.phases
        for f, a, p in zip(self.frequencies, self.amplitudes, phases):
            element = ResponseListElement(f, a, p)
            response_elements.append(element)

        rs = ResponseListResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in,
            self.units_out,
            name=self.name,
            description=self.get_filter_description(),
            input_units_description=self._units_in_obj.name,
            output_units_description=self._units_out_obj.name,
            response_list_elements=response_elements,
        )

        return rs

    def complex_response(self, frequencies, interpolation_method="slinear"):
        """
        Computes complex response for given frequency range
        :param frequencies: array of frequencies to estimate the response
        :type frequencies: np.ndarray
        :return: complex response
        :rtype: np.ndarray

        """
        if np.min(frequencies) < self.min_frequency:
            # if there is a dc component skip it.
            if np.min(frequencies) != 0:
                self.logger.warning(
                    f"Extrapolating frequencies smaller ({np.min(frequencies)} Hz) "
                    f"than table frequencies ({self.min_frequency} Hz)."
                )
        if np.max(frequencies) > self.max_frequency:
            self.logger.warning(
                f"Extrapolating frequencies larger ({np.max(frequencies)} Hz) "
                f"than table frequencies ({self.max_frequency} Hz)."
            )

        phase_response = interp1d(
            self.frequencies,
            self._empirical_phases,
            kind=interpolation_method,
            fill_value="extrapolate",
        )

        amplitude_response = interp1d(
            self.frequencies,
            self._empirical_amplitudes,
            kind=interpolation_method,
            fill_value="extrapolate",
        )
        total_response_function = lambda f: amplitude_response(f) * np.exp(
            1.0j * phase_response(f)
        )

        return self.gain * total_response_function(frequencies)
