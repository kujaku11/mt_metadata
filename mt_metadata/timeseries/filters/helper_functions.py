from loguru import logger
from mt_metadata.timeseries.filters.coefficient_filter import CoefficientFilter
from mt_metadata.timeseries.filters.frequency_response_table_filter import (
    FrequencyResponseTableFilter,
)

def make_coefficient_filter(gain=1.0, name="generic coefficient filter", **kwargs):
    """

    Parameters
    ----------
    gain: float
    name: string
    units_in : string
        A supported unit or "unknown"
        one of "digital counts", "millivolts", etc.
        A complete list of units can be found in mt_metadata/mt_metadata/util/units.py
        and is accessible as a table via:
        from mt_metadata.utils.units import UNITS_DF

    Returns
    -------

    """
    # in general, you need to add all required fields from the standards.json
    default_units_in = "unknown"
    default_units_out = "unknown"

    cf = CoefficientFilter()
    cf.gain = gain
    cf.name = name

    cf.units_in = kwargs.get("units_in", default_units_in)
    cf.units_out = kwargs.get("units_out", default_units_out)

    return cf


def make_frequency_response_table_filter(file_path, case="bf4"):
    """
    Parameters
    ----------
    filepath: pathlib.Path or string
    case : string, placeholder for handling different fap table formats.

    Returns
    -------
    fap_filter: FrequencyResponseTableFilter
    """
    fap_filter = FrequencyResponseTableFilter()

    if case == "bf4":
        import numpy as np
        import pandas as pd

        df = pd.read_csv(file_path)  # , skiprows=1)
        # Hz, V/nT, degrees
        fap_filter.frequencies = df["Frequency [Hz]"].values
        fap_filter.amplitudes = df["Amplitude [V/nT]"].values
        fap_filter.phases = np.deg2rad(df["Phase [degrees]"].values)
        fap_filter.units_in = "volts"
        fap_filter.units_out = "nanotesla"
        fap_filter.gain = 1.0
        fap_filter.name = "bf4"
        return fap_filter
    else:
        msg = f"Case {case} not supported for FAP Table"
        logger.error(msg)
        raise NotImplementedError(msg)


def make_volt_per_meter_to_millivolt_per_km_converter():
    """
    This represents a filter that converts from mV/km to V/m.

    Returns
    -------

    """
    coeff_filter = make_coefficient_filter(
        gain=1e-6,
        units_in="millivolts per kilometer",
        units_out="volts per meter",
        name="MT to SI electric field conversion",
    )
    return coeff_filter


def make_tesla_to_nanotesla_converter():
    """
    This represents a filter that converts from nt to T.

    Returns
    -------

    """
    coeff_filter = make_coefficient_filter(
        gain=1e-9,
        units_in="nanotesla",
        units_out="tesla",
        name="MT to SI magnetic field conversion",
    )
    return coeff_filter



def decimation_info_is_degenerate(obspy_stage):
    """
    Check a few condtions that may apply to an obspy stage which if true
    imply that the decimation information can be stripped out as it bears
    no information about aany data transformation;
    Case 1: All these attrs are None decimation has no information:
    {'decimation_input_sample_rate', 'decimation_factor',
    'decimation_offset', 'decimation_delay', 'decimation_correction'}
    Case 2:

    """
    cond1 = obspy_stage.stage_gain in [1.0, None]
    cond2 = obspy_stage.decimation_factor in [1, None]

    if cond1 & cond2:
        return True
    else:
        return False


def decimation_info_is_pure_delay(stage):
    cond1 = stage.stage_gain == 1.0
    cond2 = stage.decimation_factor == 1
    cond3 = stage.decimation_delay != 0.0
    cond4 = stage.decimation_correction == 0.0

    if cond1 & cond2 & cond3 & cond4:
        return True
    else:
        return False


# def stage_gain_is_degenerate():
#     # if gain is 1.0 ignore it
#     pass


MT2SI_ELECTRIC_FIELD_FILTER = make_volt_per_meter_to_millivolt_per_km_converter()
MT2SI_MAGNETIC_FIELD_FILTER = make_tesla_to_nanotesla_converter()
