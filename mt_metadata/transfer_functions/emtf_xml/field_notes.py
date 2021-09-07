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
from . import Dipole
from mt_metadata.utils.mttime import MTime
from mt_metadata.transfer_functions.tf import Instrument

# =============================================================================
attr_dict = get_schema("field_notes", SCHEMA_FN_PATHS)
attr_dict.add_dict(Dipole()._attr_dict, "dipole")
attr_dict.add_dict(Instrument()._attr_dict, "magnetometer")
attr_dict.add_dict(Instrument()._attr_dict, "instrument")

# =============================================================================
class FieldNotes(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.errors = None
        self.run = None
        self._start_dt = MTime()
        self._end_dt = MTime()
        self.instrument = Instrument()
        self.magnetometer = [Instrument()]
        self.dipole = [Dipole()]
        self.sampling_rate = None

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def start(self):
        return self._start_dt.iso_str

    @start.setter
    def start(self, value):
        self._start_dt.from_str(value)

    @property
    def end(self):
        return self._end_dt.iso_str

    @end.setter
    def end(self, value):
        self._end_dt.from_str(value)
