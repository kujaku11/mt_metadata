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
class TimingSystem(Base):
    __doc__ = write_lines(ATTR_DICT["timing_system"])

    def __init__(self, **kwargs):

        self.type = None
        self.drift = None
        self.drift_units = None
        self.uncertainty = None
        self.uncertainty_units = None
        self.comments = None
        super().__init__(attr_dict=ATTR_DICT["timing_system"], **kwargs)


