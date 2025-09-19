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
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import TimingSystem, Software, Battery, Instrument

# =============================================================================
attr_dict = get_schema("instrument", SCHEMA_FN_PATHS)
attr_dict.add_dict(
    get_schema("timing_system", SCHEMA_FN_PATHS), "timing_system"
)
attr_dict.add_dict(get_schema("software", SCHEMA_FN_PATHS), "firmware")
attr_dict.add_dict(get_schema("battery", SCHEMA_FN_PATHS), "power_source")
attr_dict.add_dict(get_schema("instrument", SCHEMA_FN_PATHS), "data_storage")
attr_dict["data_storage.id"]["required"] = False
attr_dict["data_storage.manufacturer"]["required"] = False
attr_dict["data_storage.type"]["required"] = False


# =============================================================================
class DataLogger(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.timing_system = TimingSystem()
        self.firmware = Software()
        self.power_source = Battery()
        self.data_storage = Instrument()

        super().__init__(attr_dict=attr_dict, **kwargs)
