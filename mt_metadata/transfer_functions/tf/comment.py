# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.utils.mttime import MTime

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("comment", SCHEMA_FN_PATHS)


# =============================================================================
class Comment(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self._dt = MTime()
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def date(self):
        return self._dt.iso_str

    @date.setter
    def date(self, dt_str):
        self._dt.parse(dt_str)
