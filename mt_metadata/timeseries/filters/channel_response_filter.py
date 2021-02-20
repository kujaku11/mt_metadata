import numpy as np
import scipy.signal as signal

from mt_metadata.timeseries.filters.filter import Filter

class ChannelResponseFilter(object):
    """
    OK, the point of this class is that is has a list of filters and adds them all.
    
    """
    def __init__(self, **kwargs):
        #Filter.__init__(self, **kwargs)
        self.filters_list = kwargs.get('filters_list', None)
        self.lambda_function = kwargs.get('lambda_function', None)
        # if self.lambda_function is None:
        #     self.lambda_function = lambda f: 1.0*f

    # def combine(self, other):
    #     # TODO: Add checks here that when you are stitching two filters together the
    #     # output_units of the before filter match the input units of the after
    #     """
    #     Parameters
    #     ----------
    #     other
    # 
    #     Returns a filter that has the combined complex response of the product of
    #     self and other.  The assumption is the the output of self matches to the imput of other.
    #     -------
    # 
    #     """
    #     print("units consistency check:")
    #     print("self output {}".format(self.output_units))
    #     print("other input {}".format(other.input_units))
    # 
    #     cr1 = lambda f: self.complex_response(f)
    #     cr2 = lambda f: other.complex_response(f)
    #     cr3 = lambda f: cr1(f) * cr2(f)
    #     self.lambda_function = cr3

    def complex_response(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        lambda_list = [lambda f:x.complex_response(f) for x in self.filters_list]
        print('hi')
        evaluated_lambdas = [x(frequencies) for x in lambda_list]

        return self.lambda_function(frequencies)


