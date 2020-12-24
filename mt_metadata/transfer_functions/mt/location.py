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
class Declination(Base):
    __doc__ = write_lines(ATTR_DICT["declination"])

    def __init__(self, **kwargs):

        self.value = None
        self.epoch = None
        self.model = None
        self.comments = None
        super(Declination, self).__init__(attr_dict=ATTR_DICT["declination"], **kwargs)


