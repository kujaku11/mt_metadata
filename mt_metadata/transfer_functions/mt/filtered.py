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
class Software(Base):
    __doc__ = write_lines(ATTR_DICT["software"])

    def __init__(self, **kwargs):
        self.name = None
        self.version = None
        self._author = Person()

        super().__init__(attr_dict=ATTR_DICT["software"], **kwargs)

    @property
    def author(self):
        return self._author.author

    @author.setter
    def author(self, value):
        self._author.author = value


# =============================================================================
# filter
# =============================================================================
