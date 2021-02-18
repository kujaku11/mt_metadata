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
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("filter", SCHEMA_FN_PATHS)
# =============================================================================
class Filter(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
        name: The label for this filter, can act as a key for response info
        type: One of {'pole_zero', 'frequencny_table', 'coefficient', 'fir', 'iir', 'time_shift'}
        units_in: expected units of data coming from the previous stage ...
        ? is this defined by the data itself? Or is this an Idealized Value?
        normalization_frequency: ???
        normalization_factor ???
        cutoff


        **kwargs note: these
        """
        super().__init__(attr_dict=attr_dict, **kwargs)

        self.name = kwargs.get('name', None)
        self.type = kwargs.get('type', None)
        self.input_units = kwargs.get('input_units', None)
        self.output_units = kwargs.get('output_units', None)
        self._calibration_dt = MTime()
        #self.operation = None
        #self.normalization_frequency = None
        #self.normalization_factor = None
        #self.cutoff = None
        #self.n_theoretical_poles = None
        #self.n_theoretical_zeros = None
        self.comments = None
        #self.conversion_factor = None


    @property
    def calibration_date(self):
        return self._calibration_dt.date

    @calibration_date.setter
    def calibration_date(self, value):
        self._calibration_dt.from_str(value)

    def __combine__(self, other, before_or_after='after'):
        #TODO: Add checks here that when you are stitching two filters together the
        #output_units of the before filter match the input units of the after
        """
        Parameters
        ----------
        other

        Returns a filter that has the combined complex response of the product of
        self and other.
        -------

        """
        pass

    def from_obspy_stage(self, stage):
        if isinstance(stage, obspy.core.inventory.response.ResponseStage):
            #this would execute obspy_stages.create_filter_from_stage()
            pass
        else:
            print("Expected a Stage and got a {}".format(type(stage)))
            raise Exception
    
    
    def complex_response(self, frqs):
        print("I dont have one")
        return None

    def plot_complex_response(self, frequency_band):
        pass
    # def complex_response(self, frqs):
    #     h = self.interpolate_fap(frequencies)
    #     return h

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
