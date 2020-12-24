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
class Instrument(Base):
    __doc__ = write_lines(ATTR_DICT["instrument"])

    def __init__(self, **kwargs):

        self.id = None
        self.manufacturer = None
        self.type = None
        self.model = None
        self.name = None
        self.settings = None
        super().__init__(attr_dict=ATTR_DICT["instrument"], **kwargs)


# =============================================================================
# FDSN
# =============================================================================
