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
class Battery(Base):
    __doc__ = write_lines(ATTR_DICT["battery"])

    def __init__(self, **kwargs):

        self.type = None
        self.id = None
        self.voltage = Diagnostic()
        self.comments = None
        super().__init__(attr_dict=ATTR_DICT["battery"], **kwargs)


# =============================================================================
# Electrode
# =============================================================================
