import numpy as np
import scipy.signal as signal

from mt_metadata.timeseries.filters.filter import Filter

class CoefficientFilter(Filter):
    """
    standards for this: gain is floating point
    
    """
    def __init__(self, **kwargs):
        Filter.__init__(self, **kwargs)

    @classmethod
    def from_obspy_stage(cls, stage):
        kwargs = {'gain' : stage.stage_gain}
        return cls(**kwargs)



    def complex_response(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        return self.gain * np.ones(len(frequencies))

