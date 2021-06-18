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
    FrequencyResponseTableFilter,
    FIRFilter,
)
from mt_metadata.utils.units import obspy_units_descriptions as units_descriptions
from obspy.core import inventory

# =============================================================================


class ChannelResponseFilter(object):
    """
    This class holds a list of all the filters associated with a channel.
    It has methods for combining the responses of all the filters into a total
    response that we will apply to a data segment.

    """

    def __init__(self, **kwargs):
        self.filters_list = []
        self.normalization_frequency = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        lines = ["Filters Included:\n", "=" * 25, "\n"]
        for f in self.filters_list:
            lines.append(f.__str__())
            lines.append(f"\n{'-'*20}\n")

        return "".join(lines)

    def __repr__(self):
        return self.__str__()

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
        ACCEPTABLE_FILTERS = [
            PoleZeroFilter,
            CoefficientFilter,
            TimeDelayFilter,
            FrequencyResponseTableFilter,
            FIRFilter,
        ]

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
        """ estimate pass band for all filters in frequency"""
        pb = []
        for f in self.filters_list:
            if hasattr(f, "pass_band"):
                f_pb = f.pass_band()
                if f_pb is np.nan:
                    continue
                pb.append((f_pb.min(), f_pb.max()))

        pb = np.array(pb)
        return np.array([pb[:, 0].max(), pb[:, 1].min()])

    @property
    def normalization_frequency(self):
        """ get normalization frequency from ZPK or FAP filter """

        if self._normalization_frequency is None:
            return np.round(self.pass_band.mean(), decimals=3)

        return self._normalization_frequency

    @normalization_frequency.setter
    def normalization_frequency(self, value):
        """ Set normalization frequency if input """

        self._normalization_frequency = value

    @property
    def non_delay_filters(self):
        """

        Returns all the non-time_delay filters as a list
        -------

        """
        non_delay_filters = [x for x in self.filters_list if x.type != "time delay"]
        return non_delay_filters

    @property
    def delay_filters(self):
        """

        Returns all the time delay filters as a list
        -------

        """
        delay_filters = [x for x in self.filters_list if x.type == "time delay"]
        return delay_filters

    @property
    def total_delay(self):
        """

        Returns the total delay of all filters
        -------

        """
        delay_filters = self.delay_filters
        total_delay = 0.0
        for delay_filter in delay_filters:
            total_delay += delay_filter.delay
        return total_delay

    def complex_response(self, frequencies, include_delay=False, normalize=False):
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
            filters_list = self.filters_list
        else:
            filters_list = self.non_delay_filters

        filter_stage = filters_list.pop(0)
        result = filter_stage.complex_response(frequencies)
        while len(filters_list):
            filter_stage = filters_list.pop(0)
            result *= filter_stage.complex_response(frequencies)

        if normalize:
            result /= np.max(np.abs(result))
        return result

    def compute_instrument_sensitivity(self, normalization_frequency=None):
        """
        Compute the StationXML instrument sensitivity for the given normalization frequency

        :param normalization_frequency: DESCRIPTION
        :type normalization_frequency: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if normalization_frequency is not None:
            self.normalization_frequency = normalization_frequency
        sensitivity = 1.0
        for mt_filter in self.filters_list:
            complex_response = mt_filter.complex_response(self.normalization_frequency)
            sensitivity *= complex_response

        return np.round(np.abs(sensitivity[0]), 3)

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

    def to_obspy(self, sample_rate=1):
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
            self.units_out,
            input_units_description=units_descriptions[self.units_in],
            output_units_description=units_descriptions[self.units_out],
        )

        for ii, f in enumerate(self.filters_list, 1):
            total_response.response_stages.append(
                f.to_obspy(
                    stage_number=ii,
                    normalization_frequency=self.normalization_frequency,
                    sample_rate=sample_rate,
                )
            )

        return total_response
