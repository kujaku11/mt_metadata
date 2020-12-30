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
from . import Diagnostic

# =============================================================================
attr_dict = get_schema("battery", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("diagnostic", SCHEMA_FN_PATHS), "voltage")
# =============================================================================
class Battery(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.type = None
        self.id = None
        self.voltage = Diagnostic()
        self.comments = None
        super().__init__(attr_dict=attr_dict, **kwargs)
