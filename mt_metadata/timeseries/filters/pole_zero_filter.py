import copy
import numpy as np
import obspy
import scipy.signal as signal

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter import Filter
from mt_metadata.timeseries.filters.filter import OBSPY_MAPPING
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("filter", SCHEMA_FN_PATHS)
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
obspy_mapping['_zeros'] = '_zeros'
obspy_mapping['_poles'] = '_poles'
obspy_mapping['normalization_factor'] = 'normalization_factor'


class PoleZeroFilter(Filter):

    def __init__(self, **kwargs):
        self.type = 'zpk'
        self._poles = None
        self._zeros = None
        super(Filter, self).__init__(attr_dict=attr_dict, **kwargs)

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
            self._poles = np.array(value.split(','), dtype=np.complex)

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
            self._zeros = np.array(value.split(','), dtype=np.complex)

    @property
    def n_poles(self):
        return len(self._poles)

    @property
    def n_zeros(self):
        return len(self._zeros)

    def zero_pole_gain_representation(self):
        zpg = signal.ZerosPolesGain(
            self.zeros, self.poles, self.normalization_factor)
        return zpg

    def to_obspy(self, stage_number=1, gain=1, normalization_frequency=.01, pz_type="LAPLACE (RADIANS/SECOND)"):
        """
        create an obspy stage

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.zeros is None:
            self.zeros = []
        if self.poles is None:
            self.poles = []
            
        rs = obspy.core.inventory.PolesZerosResponseStage(stage_number,
                                                gain,
                                                normalization_frequency,
                                                self.units_in,
                                                self.units_out,
                                                pz_type,
                                                normalization_frequency,
                                                self.zeros,
                                                self.poles,
                                                name=self.name,
                                                normalization_factor=self.normalization_factor)

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
            self.zeros, self.poles, self.normalization_factor, worN=angular_frequencies)
        return h

    def plot_pole_zero_response(self):
        zpg = self.zero_pole_gain_representation()
        frequency_axis = np.logspace(-1, 5, num=100)
        w = 2. * np.pi * frequency_axis
        plot_response(zpk_obs=zpg, w_values=w, title=self.name)


def main():
    pz_filter = PoleZeroFilter()
    print('test')


if __name__ == '__main__':
    main()
