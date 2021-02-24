# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:52:35 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import numpy as np
import mt_metadata.timeseries as metadata
from mt_metadata.base import BaseDict


def summarize_timeseries_standards():
    """
    Summarize the standards for time series metadata.
    """

    summary_dict = BaseDict()
    summary_dict.add_dict(metadata.Survey()._attr_dict.copy(), "survey")
    summary_dict.add_dict(metadata.Station()._attr_dict.copy(), "station")
    summary_dict.add_dict(metadata.Run()._attr_dict.copy(), "run")
    summary_dict.add_dict(metadata.Electric()._attr_dict.copy(), "electric")
    summary_dict.add_dict(metadata.Magnetic()._attr_dict.copy(), "magnetic")
    summary_dict.add_dict(metadata.Auxiliary()._attr_dict.copy(), "auxiliary")

    return summary_dict


def summary_to_array(summary_dict):
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

    entries = np.zeros(len(summary_dict.keys()), dtype=dtype)
    count = 0
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
            