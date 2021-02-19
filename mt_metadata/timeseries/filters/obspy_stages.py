import numpy as np
import obspy

from mt_metadata.timeseries.filters.coefficient_filter import CoefficientFilter
from mt_metadata.timeseries.filters.pole_zero_filter import PoleZeroFilter


def create_coefficent_filter_from_stage(stage):
    coeff_filter = CoefficientFilter()
    coeff_filter = coeff_filter.from_obspy_stage(stage)
    return coeff_filter
    

def create_pole_zero_filter_from_stage(stage):
    pz_filter = PoleZeroFilter()
    pz_filter = pz_filter.from_obspy_stage(stage)
    return pz_filter



def create_filter_from_stage(stage):
    #this works on a single stage
    if isinstance(stage, obspy.core.inventory.response.PolesZerosResponseStage):
        return create_pole_zero_filter_from_stage(stage)
    elif isinstance(stage, obspy.core.inventory.response.CoefficientsTypeResponseStage):
        return create_coefficent_filter_from_stage(stage)
    else:
        print("Filter Stage of Type {} not known".format(type(stage)))
        raise Exception
