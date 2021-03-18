import copy
import numpy as np

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter import Filter
from mt_metadata.timeseries.filters.filter import OBSPY_MAPPING
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
obspy_mapping['stage_gain'] = 'gain'

# =============================================================================
attr_dict = get_schema("filter", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("coefficient_filter", SCHEMA_FN_PATHS))
# =============================================================================

class CoefficientFilter(Filter):

    def __init__(self, **kwargs):
        self.type = 'coefficient'
        self.gain = 1.0
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

        """
        return self.gain * np.ones(len(frequencies))

