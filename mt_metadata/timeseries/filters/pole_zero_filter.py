import copy
import numpy as np
import obspy
import scipy.signal as signal

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import OBSPY_MAPPING
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("pole_zero_filter", SCHEMA_FN_PATHS))
# =============================================================================

# Decision:
# A
# - import obspy mapping from filter.py
# - add the desired attrs here
# - assign to self._obspy_mapping in __init__
# B
# - augment obspy mapping in __init__()
# C
# - augment obspy mapping in from_obspy_stage()
# D
# - put obspy mapping in json
obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
obspy_mapping["_zeros"] = "zeros"
obspy_mapping["_poles"] = "poles"
obspy_mapping["normalization_factor"] = "normalization_factor"


class PoleZeroFilter(FilterBase):
    def __init__(self, **kwargs):
        
        super().__init__()
        self.type = "zpk"
        self.poles = None
        self.zeros = None
        self.normalization_factor = 1.0
        
        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        

        self.obspy_mapping = obspy_mapping

    @property
    def poles(self):
        return self._poles

    @poles.setter
    def poles(self, value):
        """
        Set the poles, make sure the input is validated
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._poles = np.array(value, dtype=np.complex)

        elif isinstance(value, str):
            self._poles = np.array(value.split(","), dtype=np.complex)

        else:
            self._poles = np.empty(0)

    @property
    def zeros(self):
        return self._zeros

    @zeros.setter
    def zeros(self, value):
        """
        Set the zeros, make sure the input is validated
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._zeros = np.array(value, dtype=np.complex)

        elif isinstance(value, str):
            self._zeros = np.array(value.split(","), dtype=np.complex)

        else:
            self._zeros = np.empty(0)

    @property
    def n_poles(self):
        return len(self._poles)

    @property
    def n_zeros(self):
        return len(self._zeros)

    def zero_pole_gain_representation(self):
        zpg = signal.ZerosPolesGain(self.zeros, self.poles, self.normalization_factor)
        return zpg

    @property
    def total_gain(self):
        return self.gain * self.normalization_factor

    def to_obspy(
        self,
        stage_number=1,
        pz_type="LAPLACE (RADIANS/SECOND)",
        normalization_frequency=1,
        sample_rate=1,
    ):
        """
        create an obspy stage

        :return: DESCRIPTION
        :rtype: TYPE

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
            input_units_description=self.get_unit_description(self.units_in),
            output_units_description=self.get_unit_description(self.units_out),
        )

        return rs

    def complex_response(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        angular_frequencies = 2 * np.pi * frequencies
        w, h = signal.freqs_zpk(
            self.zeros, self.poles, self.total_gain, worN=angular_frequencies
        )
        return h

    def plot_pole_zero_response(self):
        zpg = self.zero_pole_gain_representation()
        frequency_axis = np.logspace(-5, 5, num=100)
        w = 2.0 * np.pi * frequency_axis
        plot_response(zpk_obs=zpg, w_values=w, title=self.name)

    def pass_band(self, window_len=7, tol=1e-4):
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

        if self.poles is None and self.zeros is None:
            return np.nan
        f = np.logspace(-5, 5, num=50 * window_len)  # freq Hz
        cr = self.complex_response(f)
        amp = np.abs(cr)
        if np.all(cr == cr[0]):
            return np.array([f.min(), f.max()])
        pass_band = []
        for ii in range(window_len, len(cr) - window_len, 1):
            cr_window = np.array(amp[ii : ii + window_len])
            cr_window /= cr_window.max()

            if cr_window.std() <= tol and cr_window.std() > 0:
                pass_band.append(f[ii])

        # Check for discontinuities in the pass band
        pass_band = np.array(pass_band)
        if len(pass_band) > 1:
            df_passband = np.diff(np.log(pass_band))
            df_0 = np.log(f[1]) - np.log(f[0])
            if np.isclose(df_passband, df_0).all():
                pass
            else:
                self.logger.warning("Passband appears discontinuous")
        pass_band = np.array([pass_band.min(), pass_band.max()])
        return pass_band

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
