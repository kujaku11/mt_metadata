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
class Rating(Base):
    __doc__ = write_lines(ATTR_DICT["rating"])

    def __init__(self, **kwargs):
        self.author = None
        self.method = None
        self.value = 0.0

        super().__init__(attr_dict=ATTR_DICT["rating"], **kwargs)


