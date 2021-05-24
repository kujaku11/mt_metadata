"""
20210323: Considerations:
Input units will typically be Volts and outputs nT, but this is configurable.

This could be populated by frequency or Period and phase could have units of radians or degrees.
Rather than build all the possible conversions/cases into the class, suggest fix the class
so that it takes as input frequency - amplitude - phase (radians) "FAP" format.
We can than use a FAPFormatter() class to address casting received tables into the desired formats.

The table should have default outputs, suggested frequency, amplitude, phase (degrees)

.. todo:: Need to add to/from obspy methods

"""
import copy
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import OBSPY_MAPPING
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("frequency_response_table_filter", SCHEMA_FN_PATHS))

# =============================================================================

obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
obspy_mapping["amplitudes"] = "_empirical_amplitudes"
obspy_mapping["frequencies"] = "_empirical_frequencies"
obspy_mapping["phases"] = "_empirical_phases"

class FrequencyResponseTableFilter(FilterBase):

    def __init__(self, **kwargs):
        self.type = 'frequency response table'
        self.instrument_type = None #FGM or FBC or other?
        self.gain = 1.0
        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        
        self.obspy_mapping = obspy_mapping
        #self._empirical_frequencies = kwargs.get('frequencies', None)
        #self._empirical_amplitudes = kwargs.get('amplitudes', None)
        #self._empirical_phases = kwargs.get('phases', None)
        self.amplitude_response = None
        self.phase_response = None
        self._total_response_function = None


    @property
    def frequencies(self):
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
            msg = f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            self.logger.error(msg)
            raise TypeError(msg)
            
    @property
    def amplitudes(self):
        return self._empirical_amplitudes

    @amplitudes.setter
    def amplitudes(self, value):
        """
        Set the amplitudes, make sure the input is validated
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._empirical_amplitudes = np.array(value, dtype=float)

        else:
            msg = f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def phases(self):
        return self._empirical_phases

    @phases.setter
    def phases(self, value):
        """
        Set the amplitudes, make sure the input is validated
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._empirical_phases = np.array(value, dtype=float)
        else:
            msg = f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def min_frequency(self):
        return self._empirical_frequencies.min()

    @property
    def max_frequency(self):
        return self._empirical_frequencies.max()

    def total_response_function(self, frequencies):
        return self._total_response_function(frequencies)


    def complex_response(self, frequencies, k=3, ext=2):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        #I would like a separate step that calculates self._total_response_function
        and stores it but the validator doesn't seem to like when I assign that attribute
        """
        if np.min(frequencies) < self.min_frequency:
            print("Extrapolation warning ")

        if np.max(frequencies) > self.max_frequency:
            print("Extrapolation warning ")
        phase_response = InterpolatedUnivariateSpline(self.frequencies, self.phases, k=k, ext=ext)
        amplitude_response = InterpolatedUnivariateSpline(self.frequencies, self.amplitudes, k=k, ext=ext)
        total_response_function = lambda f: amplitude_response(f) * np.exp(1.j * phase_response(f))

        return self.gain * total_response_function(frequencies)
