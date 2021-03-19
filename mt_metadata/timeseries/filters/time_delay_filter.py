import copy
import numpy as np
import scipy.signal as signal

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter import Filter
from mt_metadata.timeseries.filters.filter import OBSPY_MAPPING
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
obspy_mapping['decimation_delay'] = 'delay'
# =============================================================================
attr_dict = get_schema("filter", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("time_delay_filter", SCHEMA_FN_PATHS))
# =============================================================================

class TimeDelayFilter(Filter):

    def __init__(self, **kwargs):
        self.type = 'time delay'
        self.delay = None
        super(Filter, self).__init__(attr_dict=attr_dict, **kwargs)
        self.obspy_mapping = obspy_mapping


    def complex_response(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        See notes in mt_metadata issue#14
        The complex response for the time delay filter should in general be avoided.  Phase wrapping
        artefacts at high frequency and non-causal time-series segments are expected.
        In general, delay corrections should be applied in time domain before spectral processing.

        """
        print("WARNING - USING FREQUENCY DOMAIN VERSION OF THIS METHOD NOT RECOMMENDED FOR MT PROCESSING")
        w = 2 * np.pi * frequencies
        exponent = -1.j * w * self.delay
        spectral_shift_multiplier = np.exp(exponent)
        return spectral_shift_multiplier


def test_expected_behaviour():
    import matplotlib.pyplot as plt
    np.random.seed(1)


def main():
    time_delay_filter = TimeDelayFilter()
    print('test')

if __name__ == '__main__':
    main()