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
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("software", SCHEMA_FN_PATHS)
# =============================================================================


class Software(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.author = None
        self._last_mod_dt = MTime()
        self.remote_ref = None

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def last_mod(self):
        return self._last_mod_dt.iso_str

    @last_mod.setter
    def last_mod(self, value):
        self._last_mod_dt.from_str(value)
