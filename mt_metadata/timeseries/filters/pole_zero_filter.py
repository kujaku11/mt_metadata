import numpy as np
import scipy.signal as signal

from mt_metadata.timeseries.filter import Filter

class PoleZeroFilter(Filter):

    def __init__(self, **kwargs):
        Filter.__init__(self, **kwargs)
        self._poles = kwargs.get('_poles', [])
        self._zeros = kwargs.get('_zeros', [])

        self._scale_factor = kwargs.get('scale_factor', 1.0)


    @property
    def poles(self):
        return self._poles

    @property
    def zeros(self):
        return self._zeros

    @property
    def scale_factor(self):
        return self._scale_factor

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
        w, h = signal.freqs_zpk(self.zeros, self.poles, self.scale_factor, worN=angular_frequencies)
        return h

