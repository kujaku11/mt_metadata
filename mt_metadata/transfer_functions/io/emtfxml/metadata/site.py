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
from . import (
    DataQualityNotes,
    DataQualityWarnings,
    Comment,
    Location,
    Orientation,
)
from mt_metadata.utils.mttime import MTime
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = get_schema("site", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("location", SCHEMA_FN_PATHS), "location")
attr_dict.add_dict(get_schema("orientation", SCHEMA_FN_PATHS), "orientation")
attr_dict.add_dict(DataQualityNotes()._attr_dict, "data_quality_notes")
attr_dict.add_dict(DataQualityWarnings()._attr_dict, "data_quality_warnings")
attr_dict.add_dict(get_schema("comment", SCHEMA_FN_PATHS), "comments")
# =============================================================================
class Site(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self._year_collected = None
        self.data_quality_notes = DataQualityNotes()
        self.data_quality_warnings = DataQualityWarnings()
        self.orientation = Orientation()
        self.location = Location()
        self._run_list = []
        self._start_dt = MTime()
        self._end_dt = MTime()
        self.comments = Comment()

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

    @property
    def year_collected(self):
        if self.start != "1980-01-01T00:00:00+00:00":
            return self._start_dt.year
        else:
            return self._year_collected

    @year_collected.setter
    def year_collected(self, value):
        self._year_collected = value

    @property
    def run_list(self):
        return " ".join(self._run_list)

    @run_list.setter
    def run_list(self, value):
        if value is None:
            return
        if isinstance(value, (str)):
            if value.count(",") > 0:
                delimiter = ","
            else:
                delimiter = " "
            value = value.split(delimiter)

        self._run_list = value

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "site")

    def to_xml(self, string=False, required=True):
        """ """

        return helpers.to_xml(self, string=string, required=required)
