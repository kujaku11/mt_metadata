"""
Idea here is to add logic to interrogate stage filters received from StationXML

"""
import numpy as np
import obspy

from mt_metadata.timeseries.filters.coefficient_filter import CoefficientFilter
from mt_metadata.timeseries.filters.time_delay_filter import TimeDelayFilter
from mt_metadata.timeseries.filters.pole_zero_filter import PoleZeroFilter


def create_time_delay_filter_from_stage(stage):
    time_delay_filter = TimeDelayFilter()
    time_delay_filter = time_delay_filter.from_obspy_stage(stage)
    return time_delay_filter


def create_coefficent_filter_from_stage(stage):
    coeff_filter = CoefficientFilter()
    coeff_filter = coeff_filter.from_obspy_stage(stage)
    return coeff_filter


def create_pole_zero_filter_from_stage(stage):
    pz_filter = PoleZeroFilter()
    pz_filter = pz_filter.from_obspy_stage(stage)
    return pz_filter


def check_if_coefficient_filter_is_delay_only(stage):
    """
    stage: obspy_stage type in obspy.core.inventory.response
    This function may wind up being a method of the CoefficientFilter class, but leaving it
    separate for now.
    Conditions to check:
    1. Gain is unity
    2. Decimation Factor is 1
    3. delay is non-zero
    4. delay has not been corrected on the data-center side.
    If all four of these are true we assume this is a pathological CoefficienFilter
    and would actually be a TimeDelay() filter instance if one existed in StationXML.
    Returns
    -------

    """
    cond1 = stage.stage_gain == 1.0
    cond2 = stage.decimation_factor == 1
    cond3 = stage.decimation_delay != 0.0
    cond4 = stage.decimation_correction == 0.0

    if cond1 & cond2 & cond3 & cond4:
        return True
    else:
        return False


def create_filter_from_stage(stage):
    # this works on a single stage

    if isinstance(stage, obspy.core.inventory.response.PolesZerosResponseStage):
        return create_pole_zero_filter_from_stage(stage)
    if isinstance(stage, obspy.core.inventory.response.ResponseStage):
        print("NEWLY ENCOUNTERED 20210514 -- may need some massaging")
        obspy_filter = create_coefficent_filter_from_stage(stage)
        return obspy_filter
    elif isinstance(stage, obspy.core.inventory.response.CoefficientsTypeResponseStage):
        # Sometimes filter stages are used to kluge-represent filters of other types
        #
        # Encountered Cases This Far:
        #   CoefficientTypeResponseStage Used to package a time-delay filter
        is_a_delay_filter = check_if_coefficient_filter_is_delay_only(stage)
        if is_a_delay_filter:
            obspy_filter = create_time_delay_filter_from_stage(stage)
        else:
            obspy_filter = create_coefficent_filter_from_stage(stage)
        return obspy_filter
    else:
        print("Filter Stage of Type {} not known".format(type(stage)))
        raise Exception
