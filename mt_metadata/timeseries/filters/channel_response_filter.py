import numpy as np
import scipy.signal as signal

from mt_metadata.timeseries.filters.filter import Filter

class ChannelResponseFilter(object):
    """
    This class holds a list of all the filters associated with a channel.
    It has methods for combining the responses of all the filters into a total
    response that we will apply to a data segment.
    
    """
    def __init__(self, **kwargs):
        #Filter.__init__(self, **kwargs)
        self.filters_list = kwargs.get('filters_list', None)
        self.lambda_function = kwargs.get('lambda_function', None)
        # if self.lambda_function is None:
        #     self.lambda_function = lambda f: 1.0*f


    @property
    def total_delay(self):
        delay_filters = self.delay_filters
        total_delay = 0.0
        for delay_filter in delay_filters:
            total_delay += delay_filter.delay
        return total_delay

    @property
    def delay_filters(self):
        """

        Returns the delay of the set of filters
        -------

        """
        delay_filters = [x for x in self.filters_list if x.type=='time_delay']
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
        if include_delay:
            lambda_list = [lambda f:x.complex_response(f) for x in self.filters_list]
        else:
            lambda_list = [lambda f: x.complex_response(f) for x in self.filters_list]
        print('hi')
        evaluated_lambdas = [x(frequencies) for x in lambda_list]

        return self.lambda_function(frequencies)

    @property
    def units(self):
        """
        returns the units of the channel
        """
        pass

    @property
    def check_consistency_of_units(self):
        """
        confirms that the input and output units of each filter state are consistent
        """
        pass


