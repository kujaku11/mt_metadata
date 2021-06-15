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

from obspy.core.inventory.response import ResponseListResponseStage, ResponseListElement

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
        super().__init__()
        self.type = "frequency response table"
        self.instrument_type = None  # FGM or FBC or other?
        
        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)

        self.obspy_mapping = obspy_mapping
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
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
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
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
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
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def min_frequency(self):
        return self._empirical_frequencies.min()

    @property
    def max_frequency(self):
        return self._empirical_frequencies.max()

    def to_obspy(
        self, stage_number=1, normalization_frequency=1, sample_rate=1,
    ):
        """
        Convert to an obspy stage
        
        :param stage_number: DESCRIPTION, defaults to 1
        :type stage_number: TYPE, optional
        :param normalization_frequency: DESCRIPTION, defaults to 1
        :type normalization_frequency: TYPE, optional
        :param sample_rate: DESCRIPTION, defaults to 1
        :type sample_rate: TYPE, optional
        :param : DESCRIPTION
        :type : TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        response_elements = []
        for f, a, p in zip(self.frequencies, self.amplitudes, self.phases):
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
            input_units_description=self.get_unit_description(self.units_in),
            output_units_description=self.get_unit_description(self.units_out),
            response_list_elements=response_elements,
        )

        return rs

    def total_response_function(self, frequencies):
        return self._total_response_function(frequencies)

    def pass_band(self, window_len=7, tol=1e-2):
        """

        Caveat: This should work for most Fluxgate and feedback coil magnetometers, and basically most filters
        having a "low" number of poles and zeros.  This method is not 100% robust to filters with a notch in them.

        Try to estimate pass band of the filter from the flattest spots in 
        the amplitude.
        
        The flattest spot is determined by calculating a sliding window
        with length `window_len` and estimating normalized std. 
        
        ..note:: This only works for simple filters with
        on flat pass band.
        
        :param window_len: length of sliding window in points
        :type window_len: integer
        
        :param tol: the ratio of the mean/std should be around 1 
        tol is the range around 1 to find the flat part of the curve.
        :type tol: float
        
        :return: pass band frequencies
        :rtype: np.ndarray

        """

        if self.amplitudes is None and self.phases is None:
            return np.nan

        if np.all(self.amplitudes == self.amplitudes[0]):
            return np.array([self.frequencies.min(), self.frequencies.max()])

        pass_band = []
        for ii in range(window_len, self.frequencies.size - window_len, 1):
            cr_window = np.array(self.amplitudes[ii : ii + window_len])
            cr_window /= cr_window.max()

            if cr_window.std() <= tol:
                pass_band.append(self.frequencies[ii])

        # Check for discontinuities in the pass band
        pass_band = np.array(pass_band)
        if len(pass_band) > 1:
            df_passband = np.diff(np.log(pass_band))
            df_0 = np.log(self.frequencies[1]) - np.log(self.frequencies[0])
            if np.isclose(df_passband, df_0).all():
                pass
            else:
                self.logger.warning("Passband appears discontinuous")
        pass_band = np.array([pass_band.min(), pass_band.max()])
        return pass_band

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
            self.logger.warning("Extrapolation warning ")

        if np.max(frequencies) > self.max_frequency:
            self.logger.warning("Extrapolation warning ")
        phase_response = InterpolatedUnivariateSpline(
            self.frequencies, self.phases, k=k, ext=ext
        )
        amplitude_response = InterpolatedUnivariateSpline(
            self.frequencies, self.amplitudes, k=k, ext=ext
        )
        total_response_function = lambda f: amplitude_response(f) * np.exp(
            1.0j * phase_response(f)
        )

        return self.gain * total_response_function(frequencies)
