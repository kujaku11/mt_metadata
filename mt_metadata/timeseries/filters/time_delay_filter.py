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
attr_dict = get_schema("time_delay_filter", SCHEMA_FN_PATHS)
# =============================================================================

class TimeDelayFilter(Filter):

    def __init__(self, **kwargs):
        #Filter.__init__(self, **kwargs)
        super().__init__(**kwargs)
        self._attr_dict.update(attr_dict)
        self._obspy_mapping = obspy_mapping


    def complex_response(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        print('need to add a linear phase calculation here and a test to make '
              'sure the sign on the exponent is correct')
        #e^-jwa
        w = 2 * np.pi * frequencies
        exponent = -1.j * w * self.delay
        np.exp(exponent)
        print('ok')
        return np.exp(exponent)



def main():
    time_delay_filter = TimeDelayFilter()
    print('test')

if __name__ == '__main__':
    main()
