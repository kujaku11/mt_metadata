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
from . import Person
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("software", SCHEMA_FN_PATHS)
# =============================================================================
class Software(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.name = None
        self.version = None
        self._author = Person()
        self._last_updated = MTime()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def author(self):
        return self._author.author

    @author.setter
    def author(self, value):
        self._author.author = value
        
    @property
    def last_updated(self):
        return self._last_updated.iso_str

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated.from_str(value)


# =============================================================================
# filter
# =============================================================================
