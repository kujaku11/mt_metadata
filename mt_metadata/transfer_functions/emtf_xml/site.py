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
from mt_metadata.transfer_functions.tf import Location, Orientation
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("site", SCHEMA_FN_PATHS)
attr_dict.add_dict(Location()._attr_dict, "location")
attr_dict.add_dict(Orientation()._attr_dict, "orientation")
# =============================================================================
class Site(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.project = None
        self.survey = None
        self.year_collected = None
        self.country = None
        self.id = None
        self.name = None
        self.acquired_by = None
        self.location = Location()
        self.orientation = Orientation()
        self.run_list = []
        self._start_dt = MTime()
        self._end_dt = MTime()

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
