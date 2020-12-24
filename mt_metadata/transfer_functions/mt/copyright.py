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
from mt_metadata.helpers import write_lines
from mt_metadata.transfer_functions.mt.standards.schema import Standards

ATTR_DICT = Standards().ATTR_DICT
# =============================================================================
class Comment(Base):
    __doc__ = write_lines(ATTR_DICT["comment"])

    def __init__(self, **kwargs):
        self.comment = None
        self.author = None
        self._dt = MTime()

    @property
    def date(self):
        return self._dt.iso_str

    @date.setter
    def date(self, dt_str):
        self._dt.from_str(dt_str)


# ==============================================================================
# Copyright
# ==============================================================================
