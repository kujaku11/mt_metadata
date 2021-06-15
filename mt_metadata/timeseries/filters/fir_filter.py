import copy
import matplotlib.pyplot as plt
import numpy as np
from obspy.core.inventory.response import FIRResponseStage
import scipy.signal as signal

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import OBSPY_MAPPING
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fir_filter", SCHEMA_FN_PATHS))
# =============================================================================


obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
# obspy_mapping["_zeros"] = "_zeros"
# obspy_mapping["_symmetry"] = "_symmetry"
obspy_mapping["_coefficients"] = "coefficients"
obspy_mapping["decimation_input_sample_rate"] = "decimation_input_sample_rate"


class FIRFilter(FilterBase):
    def __init__(self, **kwargs):
        super().__init__()
        self.type = "fir"
        self.coefficients = None
        
        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)

        self.obspy_mapping = obspy_mapping

    @property
    def coefficients(self):
        return self._coefficients

    @coefficients.setter
    def coefficients(self, value):
        """
        Set the coefficients, make sure the input is validated
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._coefficients = np.array(value, dtype=float)

        elif isinstance(value, str):
            self._coefficients = np.array(value.split(","), dtype=float)

        else:
            self._coefficients = np.empty(0)

    @property
    def n_coefficients(self):
        return len(self._coefficients)

    def plot_fir_response(self):
        w, h = signal.freqz(self.coefficients)
        fig = plt.figure()
        plt.title("Digital filter frequency response")
        ax1 = fig.add_subplot(111)
        plt.plot(w, 20 * np.log10(abs(h)), "b")
        plt.ylabel("Amplitude [dB]", color="b")
        plt.xlabel("Frequency [rad/sample]")

        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(h))
        plt.plot(w, angles, "g")
        plt.ylabel("Angle (radians)", color="g")
        plt.grid()
        plt.axis("tight")
        plt.show()

    @property
    def total_gain(self):
        return self.gain

    def to_obspy(
        self, stage_number=1, normalization_frequency=1, sample_rate=1,
    ):
        """
        create an obspy stage
    
        :return: DESCRIPTION
        :rtype: TYPE
    
        """

        rs = FIRResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in,
            self.units_out,
            normalization_frequency,
            self.coefficients,
            name=self.name,
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
        w, h = signal.freqz(self.coefficients, worN=angular_frequencies)
        #        w, h = signal.freqs_zpk(
        #            self.zeros, self.poles, self.total_gain, worN=angular_frequencies
        #        )
        return h

    # def pass_band(self, window_len=7, tol=1E-4):
    #     """
    #
    #     Caveat: This should work for most Fluxgate and feedback coil magnetometers, and basically most filters
    #     having a "low" number of poles and zeros.  This method is not 100% robust to filters with a notch in them.
    #
    #     Try to estimate pass band of the filter from the flattest spots in
    #     the amplitude.
    #
    #     The flattest spot is determined by calculating a sliding window
    #     with length `window_len` and estimating normalized std.
    #
    #     ..note:: This only works for simple filters with
    #     on flat pass band.
    #
    #     :param window_len: length of sliding window in points
    #     :type window_len: integer
    #
    #     :param tol: the ratio of the mean/std should be around 1
    #     tol is the range around 1 to find the flat part of the curve.
    #     :type tol: float
    #
    #     :return: pass band frequencies
    #     :rtype: np.ndarray
    #
    #     """
    #
    #     if self.poles is None and self.zeros is None:
    #         return np.nan
    #     f = np.logspace(-5, 5, num=50 * window_len) #freq Hz
    #     cr = self.complex_response(f)
    #     amp = np.abs(cr)
    #     if np.all(cr==cr[0]):
    #         return np.array([f.min(), f.max()])
    #     pass_band = []
    #     for ii in range(window_len, len(cr) - window_len, 1):
    #         cr_window = amp[ii:ii+window_len]
    #         cr_window /= cr_window.max()
    #
    #         if cr_window.std() == 0:
    #             continue
    #
    #         if cr_window.std() <= tol:
    #             pass_band.append(f[ii])
    #
    #
    #     #Check for discontinuities in the pass band
    #     pass_band = np.array(pass_band)
    #     if len(pass_band)>1:
    #         df_passband = np.diff(np.log(pass_band))
    #         df_0 = np.log(f[1]) - np.log(f[0])
    #         if np.isclose(df_passband, df_0).all():
    #             pass
    #         else:
    #             self.logger.warning("Passband appears discontinuous")
    #     pass_band = np.array([pass_band.min(), pass_band.max()])
    #     return pass_band

    # def normalization_frequency(self, estimate="mean", window_len=5, tol=1E-4):
    #     """
    #     Try to estimate the normalization frequency in the pass band
    #     by finding the flattest spot in the amplitude.
    #
    #     The flattest spot is determined by calculating a sliding window
    #     with length `window_len` and estimating normalized std.
    #
    #     ..note:: This only works for simple filters with
    #     on flat pass band.
    #
    #     :param window_len: length of sliding window in points
    #     :type window_len: integer
    #
    #     :param tol: the ratio of the mean/std should be around 1
    #     tol is the range around 1 to find the flat part of the curve.
    #     :type tol: float
    #
    #     :return: estimated normalization frequency Hz
    #     :rtype: float
    #
    #     """
    #     pass_band = self.pass_band(window_len, tol)
    #
    #     if len(pass_band) == 0:
    #         return np.NAN
    #
    #     if estimate == "mean":
    #         return pass_band.mean()
    #
    #     elif estimate == "median":
    #         return np.median(pass_band)
    #
    #     elif estimate == "min":
    #         return pass_band.min()
    #
    #     elif estimate == "max":
    #         return pass_band.max()
    #
    #
