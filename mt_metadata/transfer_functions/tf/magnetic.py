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
from mt_metadata.transfer_functions.tf.standards.schema import SCHEMA_FN_PATHS
from . import Channel, Instrument, Diagnostic 

# =============================================================================
attr_dict = get_schema("magnetic", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("channel", SCHEMA_FN_PATHS))
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
