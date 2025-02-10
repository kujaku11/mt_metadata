"""
Idea here is to add logic to interrogate stage filters received from StationXML

"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
from loguru import logger

from mt_metadata.timeseries.filters import (
    CoefficientFilter,
    FIRFilter,
    FrequencyResponseTableFilter,
    TimeDelayFilter,
    PoleZeroFilter,
)

# =============================================================================


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


def create_fir_filter_from_stage(stage):
    fir_filter = FIRFilter()
    fir_filter = fir_filter.from_obspy_stage(stage)
    return fir_filter


def create_frequency_response_table_filter_from_stage(stage):
    """
    Notes: Issue here is that the stage has a list of response_list_elements, it does not actually
    have attrs frequencies, amplitudes, phases... will try assigning them on the fly here

    Parameters
    ----------
    stage

    Returns
    -------

    """
    n_freq = len(stage.response_list_elements)
    frequencies = np.full(n_freq, np.nan)
    amplitudes = np.full(n_freq, np.nan)
    phases = np.full(n_freq, np.nan)
    for i, response_list_element in enumerate(stage.response_list_elements):
        frequencies[i] = response_list_element.frequency
        amplitudes[i] = response_list_element.amplitude
        phases[i] = response_list_element.phase
    stage.frequencies = frequencies
    stage.amplitudes = amplitudes
    stage.phases = phases

    fap_filter = FrequencyResponseTableFilter()
    fap_filter = fap_filter.from_obspy_stage(stage)
    return fap_filter


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
    """
    This works on a single stage, we need a catalog of stage classes
    obspy.core.inventory.response.CoefficientsTypeResponseStage
    obspy.core.inventory.response.FIRResponseStage
    obspy.core.inventory.response.PolesZerosResponseStage

    CoefficientsTypeResponseStage: cases include
    -numerator=[],denominator=[]

    Sometimes filter stages in obspy are used to kluge-represent filters of other types
        # Encountered Cases This Far:
        # CoefficientTypeResponseStage Used to package a time-delay filter

    Parameters
    ----------
    stage

    Returns
    -------

    """

    try:
        if stage.poles == [] and stage.zeros == []:
            if (
                "counts" not in stage.input_units.lower()
                and "counts" not in stage.output_units.lower()
            ):
                logger.info(
                    f"Converting PoleZerosResponseStage {stage.name} to a "
                    "CoefficientFilter."
                )
                return create_coefficent_filter_from_stage(stage)

        return create_pole_zero_filter_from_stage(stage)
    except AttributeError:
        pass

    try:
        is_a_delay_filter = check_if_coefficient_filter_is_delay_only(stage)
        if is_a_delay_filter:
            obspy_filter = create_time_delay_filter_from_stage(stage)
        else:
            obspy_filter = create_coefficent_filter_from_stage(stage)
        return obspy_filter
    except AttributeError:
        pass

    try:
        try:
            if isinstance(stage.coefficients, list):
                pass
            else:
                msg = f"Expected list of coefficients, got {type(stage.coefficients)}"
                logger.error(msg)
                raise TypeError(msg)
        except TypeError:
            msg = "Something seems off with this FIR"
            logger.info(msg)
            raise ValueError(msg)
        obspy_filter = create_fir_filter_from_stage(stage)
        return obspy_filter
    except AttributeError:
        pass

    try:
        obspy_filter = create_frequency_response_table_filter_from_stage(stage)
        return obspy_filter
    except AttributeError:
        pass

    try:
        obspy_filter = create_coefficent_filter_from_stage(stage)
        return obspy_filter
    except AttributeError:
        pass

    else:
        msg = f"Filter Stage of type {type(stage)} not known, or supported"
        logger.info(msg)
        raise TypeError(msg)
