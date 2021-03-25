"""
Channel Response Filter
=========================

Combines all filters for a given channel into a total response that can be used in 
the frequency domain.

.. note:: Time Delay filters should be applied in the time domain otherwise bad
things can happen.   

"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
import scipy.signal as signal

from mt_metadata.timeseries.filters import (
    PoleZeroFilter,
    CoefficientFilter,
    TimeDelayFilter,
)
from obspy.core import inventory
# =============================================================================


class ChannelResponseFilter(object):
    """
    This class holds a list of all the filters associated with a channel.
    It has methods for combining the responses of all the filters into a total
    response that we will apply to a data segment.

    """

    def __init__(self, **kwargs):
        # Filter.__init__(self, **kwargs)
        self.filters_list = kwargs.get("filters_list", None)
        self.lambda_function = kwargs.get("lambda_function", None)
        # if self.lambda_function is None:
        #     self.lambda_function = lambda f: 1.0*f

    @property
    def filters_list(self):
        """ filters list """
        return self._filters_list

    @filters_list.setter
    def filters_list(self, filters_list):
        """ set the filters list and validate the list """
        self._filters_list = self._validate_filters_list(filters_list)

    def _validate_filters_list(self, filters_list):
        """
        make sure the filters list is valid

        :param filters_list: DESCRIPTION
        :type filters_list: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        ACCEPTABLE_FILTERS = [PoleZeroFilter, CoefficientFilter, TimeDelayFilter, ]
        def is_acceptable_filter(item):
            if isinstance(item, tuple(ACCEPTABLE_FILTERS)):
                return True
            else:
                return False

        if filters_list in [[], None]:
            return None

        if not isinstance(filters_list, list):
            msg = f"Input filters list must be a list not {type(filters_list)}"
            raise TypeError(msg)

        fails = []
        return_list = []
        for item in filters_list:
            if is_acceptable_filter(item):
                return_list.append(item)
            else:
                fails.append(f"Item is not an acceptable filter type, {type(item)}")
            
        if fails:
            raise TypeError(", ".join(fails))

        return return_list

    @property
    def total_delay(self):
        delay_filters = self.delay_filters
        total_delay = 0.0
        for delay_filter in delay_filters:
            total_delay += delay_filter.delay
        return total_delay

    @property
    def pass_band(self):
        """ estimate pass band for all filters """
        pb = []
        for f in self.filters_list:
            if hasattr(f, "pass_band"):
                f_pb = f.pass_band()
                if f_pb is np.nan:
                    continue
                pb.append((f_pb.min(), f_pb.max()))

        pb = np.array(pb)
        return np.array([pb[0].max(), pb[1].min()])

    @property
    def normalization_frequency(self):
        """ get normalization frequency from ZPK or FAP filter """

        return self.pass_band.mean()

    @property
    def delay_filters(self):
        """

        Returns the delay of the set of filters
        -------

        """
        delay_filters = [
            x for x in self.filters_list if x.type == "time_delay"]
        return delay_filters

    def complex_response(self, frequencies, include_delay=False):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        frequencies = np.array(frequencies)

        if include_delay:
            lambda_list = [lambda f: x.complex_response(
                f) for x in self.filters_list]
        else:
            lambda_list = [lambda f: x.complex_response(
                f) for x in self.filters_list]
        print("hi")
        evaluated_lambdas = [x(frequencies) for x in lambda_list]

        return self.lambda_function(frequencies)

    def compute_instrument_sensitivity(self):
        """
        Compute the StationXML instrument sensitivity for the given normalization frequency

        :param normalization_frequency: DESCRIPTION
        :type normalization_frequency: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        sensitivity = np.array([0], dtype=np.complex)
        normalization_frequency = np.array([self.normalization_frequency])
        for mt_filter in self.filters_list:
            complex_response = mt_filter.complex_response(
                normalization_frequency)
            sensitivity += complex_response

        return np.abs(sensitivity)[0]

    @property
    def units_in(self):
        """
        returns the units of the channel
        """
        return self.filters_list[0].units_in

    @property
    def units_out(self):
        """
        returns the units of the channel
        """
        return self.filters_list[-1].units_out

    @property
    def check_consistency_of_units(self):
        """
        confirms that the input and output units of each filter state are consistent
        """
        previous_units = self.filters_list[0].units_out
        for mt_filter in self.filters_list[1:]:
            if mt_filter.units_in != previous_units:
                msg = (
                    f"Unit consistency is incorrect,  {previous_units} != {mt_filter.units_in}"
                    f" For filter {mt_filter.name}"
                )
                raise ValueError(msg)
            previous_units = mt_filter.units_out

        return True

    def to_obspy(self):
        """
        Output :class:`obspy.core.inventory.InstrumentSensitivity` object that
        can be used in a stationxml file.

        :param normalization_frequency: DESCRIPTION
        :type normalization_frequency: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        total_sensitivity = self.compute_instrument_sensitivity()

        total_response = inventory.Response()
        total_response.instrument_sensitivity = inventory.InstrumentSensitivity(
            total_sensitivity,
            self.normalization_frequency,
            self.units_in,
            self.units_out)
        
        for ii, f in enumerate(self.filters_list, 1):
            total_response.response_stages.append(f.to_obspy(stage_number=ii, normalization_frequency=self.normalization_frequency))

        return total_response
