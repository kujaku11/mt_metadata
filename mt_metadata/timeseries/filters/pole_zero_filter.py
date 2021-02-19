import numpy as np
import scipy.signal as signal

from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries.filters.filter import Filter
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("pole_zero_filter", SCHEMA_FN_PATHS)
# =============================================================================

class PoleZeroFilter(Filter):

    def __init__(self, **kwargs):
        Filter.__init__(self, **kwargs)
        self._attr_dict.update(attr_dict)

    @classmethod
    def from_obspy_stage(cls, stage):
        kwargs = stage.__dict__
        #kwargs['normalization_factor'] = stage['normalization_factor']
        return cls(**kwargs)

    @property
    def poles(self):
        return self._poles

    @property
    def zeros(self):
        return self._zeros

    @property
    def n_poles(self):
        return len(self._poles)

    @property
    def n_zeros(self):
        return len(self._zeros)
    
    def zero_pole_gain_representation(self):
        zpg = signal.ZerosPolesGain(self.zeros, self.poles, self.normalization_factor)
        return zpg

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
        w, h = signal.freqs_zpk(self.zeros, self.poles, self.normalization_factor, worN=angular_frequencies)
        return h

    def plot_pole_zero_response(self):
        zpg = self.zero_pole_gain_representation()
        frequency_axis = np.logspace(-1, 5, num=100)
        w = 2. * np.pi * frequency_axis
        plot_response(zpk_obs=zpg, w_values=w, title=self.name)
