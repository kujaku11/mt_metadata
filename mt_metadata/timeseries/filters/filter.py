# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

This is a base class for filters.  We will extend this class for each specific 
types of filter we need to implement. The "stages" that are described in the 
IRIS StationXML documentation appear to be a fairly complete collection of 
instance types we are likely to encounter.

current ZU.xml recieved Friday 12 Feb, 2021, 
Karl will prototype some extension classes and try to make those containers
behave themselves.
Mostly this means 
-the container has a place for all the (relevant) info in the "Stage"
-The stages (or filters) can be combined,
-desired: Each Stage needs to be able to generate a resposne function
-Required
The total response function of all the stage can be represented in a way that
works with FFTs.



"""
# =============================================================================
# Imports
# =============================================================================
import copy
import obspy
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.mttime import MTime


# =============================================================================
attr_dict = get_schema("filter", SCHEMA_FN_PATHS)
# =============================================================================

#Form is OBSPY_MAPPING['obspy_label'] = 'mth5_label'
OBSPY_MAPPING = {}
OBSPY_MAPPING['input_units'] = 'units_in'
OBSPY_MAPPING['name'] = 'name'
OBSPY_MAPPING['output_units'] = 'units_out'

class Filter(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
        name: The label for this filter, can act as a key for response info
        type: One of {'pole_zero', 'frequency_table', 'coefficient', 'fir', 'iir', 'time_shift'}
        units_in: expected units of data coming from the previous stage ...
        ? is this defined by the data itself? Or is this an Idealized Value?
        normalization_frequency: ???
        normalization_factor ???
        cutoff

        """
#        super().__init__(attr_dict=attr_dict, **kwargs)
        self.type = None
        self.units_in = None
        self.units_out = None
        self._calibration_dt = MTime()
        self.comments = None
        self._obspy_mapping = None

        super().__init__(attr_dict=attr_dict, **kwargs)



    @property
    def obspy_mapping(self):
        return self._obspy_mapping

    @property
    def calibration_date(self):
        return self._calibration_dt.date

    @calibration_date.setter
    def calibration_date(self, value):
        self._calibration_dt.from_str(value)



    @classmethod
    def from_obspy_stage(cls, stage, mapping=None):
        """
        purpose of this method is to un-bloat the obspy stage dictionary which typically
        contains a lot of extraneous information.
        If you want to propagate all that info : you can make a mapping which is basically
        dict(zip(stage.__dict__.keys(), stage.__dict__.keys()),
        or we could maybe support something cleaner...

        Parameters
        ----------
        stage:
        mapping

        Returns
        -------

        """
        if not isinstance(stage, obspy.core.inventory.response.ResponseStage):
            print("Expected a Stage and got a {}".format(type(stage)))
            raise Exception

        if mapping is None:
            mapping = cls().obspy_mapping
        kwargs = {}
        for obspy_label, mth5_label in mapping.items():
            kwargs[mth5_label] = stage.__dict__[obspy_label]

        return cls(**kwargs)

    def complex_response(self, frqs):
        print("Filter Base Class does not have a complex response defined")
        return None

    def generate_frequency_axis(self, sampling_rate, n_observations):
        dt = 1./sampling_rate
        frequency_axis = np.fft.fftfreq(n_observations, d=dt)
        return frequency_axis

    def plot_complex_response(self, frequency_axis, x_units='period'):
        import mt_metadata
        if frequency_axis is None:
            frequency_axis = self.generate_frequency_axis(10.0, 1000)
            x_units = 'frequency'
        #angular_frequency_axis = 2 * np.pi * frequency_axis
        #frequency_axis = np.logspace(-1, 5, num=100)
        w = 2. * np.pi * frequency_axis
        complex_response = self.complex_response(frequency_axis)
        plot_response(w_obs=w, resp_obs=complex_response, title=self.name, x_units=x_units)
        # if isinstance(self, mt_metadata.timeseries.filters.pole_zero_filter.PoleZeroFilter):
        #     plot_response(zpk_obs=zpg, w_values=w, title=pz_filter.name)
        # else:
        #     print("we dont yet have a custom plotter for filter of type {}".format(type(self)))

    @property
    def decimation_inactive(self):
        pass

    # @property
    # def gain_(self):
    #     pass

    def apply(self, ts):
        data_spectum = ts.fft()
        complex_response = self.complex_response(ts.frequencies)
        calibrated_spectrum = data_spectum / complex_response
        calibrated_data = np.fft.ifft(calibrated_spectrum)
        output = ts._deepcopy()
        output.data = calibrated_data
        return output



"""
timeseries.calibrate(Filter())
filter.apply(TimeSeries())

def apply_filter(mc_filter):
    complex_response = mc_filter.complex_response(self.frequencies)
    data_spectum = self.fft()
    calibrated_spectrum = data_spectum / complex_response
    calibrated_data = np.fft.ifft(calibrated_spectrum)
    


"""
def main():
    filter_instance = Filter()
    print('test')

if __name__ == '__main__':
    main()
