# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:52:35 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
import pandas as pd

from mt_metadata import __version__

from mt_metadata.base import BaseDict
from mt_metadata.timeseries import (
    Survey,
    Station,
    Run,
    Auxiliary,
    Electric,
    Magnetic,
)
from mt_metadata.timeseries.filters import (
    PoleZeroFilter,
    FrequencyResponseTableFilter,
    CoefficientFilter,
    FIRFilter,
    TimeDelayFilter,
)

# =============================================================================


def summarize_timeseries_standards():
    """
    Summarize the standards for time series metadata.
    """

    summary_dict = BaseDict()
    summary_dict.add_dict(Survey()._attr_dict.copy(), "survey")
    summary_dict.add_dict(Station()._attr_dict.copy(), "station")
    summary_dict.add_dict(Run()._attr_dict.copy(), "run")
    summary_dict.add_dict(Electric()._attr_dict.copy(), "electric")
    summary_dict.add_dict(Magnetic()._attr_dict.copy(), "magnetic")
    summary_dict.add_dict(Auxiliary()._attr_dict.copy(), "auxiliary")
    summary_dict.add_dict(
        PoleZeroFilter()._attr_dict.copy(), "pole_zero_filter"
    )
    summary_dict.add_dict(
        FrequencyResponseTableFilter()._attr_dict.copy(),
        "frequency_amplitude_phase_filter",
    ),
    summary_dict.add_dict(
        CoefficientFilter()._attr_dict.copy(), "coefficient_filter"
    ),
    summary_dict.add_dict(FIRFilter()._attr_dict.copy(), "fir_filter"),
    summary_dict.add_dict(
        TimeDelayFilter()._attr_dict.copy(), "time_delay_filter"
    )

    return summary_dict


def summary_to_array(summary_dict):
    """
    Summarize all metadata from a summarized dictionary of standards

    :param summary_dict: Dictionary of summarized standards
    :type summary_dict: dict
    :return: numpy structured array
    :rtype: np.array

    """
    dtype = np.dtype(
        [
            ("attribute", "U72"),
            ("type", "U15"),
            ("required", np.bool_),
            ("style", "U72"),
            ("units", "U32"),
            ("description", "U300"),
            ("options", "U150"),
            ("alias", "U72"),
            ("example", "U72"),
        ]
    )

    entries = np.zeros(len(summary_dict.keys()) + 1, dtype=dtype)
    entries[0]["attribute"] = "mt_metadata.standards.version"
    entries[0]["description"] = f"Metadata standards version {__version__}"
    entries[0]["type"] = "string"
    entries[0]["style"] = "free form"
    count = 1
    for key, v_dict in summary_dict.items():
        entries[count]["attribute"] = key
        for dkey in dtype.names[1:]:
            value = v_dict[dkey]

            if isinstance(value, list):
                if len(value) == 0:
                    value = ""

                else:
                    value = ",".join(["{0}".format(ii) for ii in value])
            if value is None:
                value = ""

            entries[count][dkey] = value
        count += 1

    return entries


def summarize_standards(metadata_type="timeseries", csv_fn=None):
    """

    Summarize standards into a numpy array and write a csv if specified

    :param metadata_type: [ timeseries | transfer function | edi | emtf | j | zmm ], defaults to "timeseries"
    :type metadata_type: string, optional
    :param csv_fn: full path to write a csv file, defaults to None
    :type csv_fn: string or Path, optional
    :return: structured numpy array
    :rtype: :class:`numpy.ndarray`

    """

    function_dict = {"timeseries": summarize_timeseries_standards}

    summary_df = pd.DataFrame(summary_to_array(function_dict[metadata_type]()))

    if csv_fn:
        summary_df.to_csv(csv_fn, index=False)

    return summary_df
