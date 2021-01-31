# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema
from .standards import SCHEMA_FN_PATHS
from . import Channel, Instrument, Diagnostic

# =============================================================================
attr_dict = get_schema("magnetic", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("channel", SCHEMA_FN_PATHS))
dq_dict = get_schema("data_quality", SCHEMA_FN_PATHS)
dq_dict.add_dict(get_schema("rating", SCHEMA_FN_PATHS), "rating")
attr_dict.add_dict(dq_dict, "data_quality")
attr_dict.add_dict(get_schema("filtered", SCHEMA_FN_PATHS), "filter")
attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
attr_dict.add_dict(get_schema("instrument", SCHEMA_FN_PATHS), "sensor")
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
attr_dict.add_dict(
    get_schema("location", SCHEMA_FN_PATHS),
    "location",
    keys=["latitude", "longitude", "elevation", "x", "y", "z"],
)
# =============================================================================
class Magnetic(Channel):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.sensor = Instrument()
        self.h_field_min = Diagnostic()
        self.h_field_max = Diagnostic()

        Channel.__init__(self, **kwargs)
        self.type = "magnetic"

        self._attr_dict = attr_dict
