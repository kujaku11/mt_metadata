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
class Electrode(Base):
    __doc__ = write_lines(ATTR_DICT["electrode"])

    def __init__(self, **kwargs):

        self.id = None
        self.manufacturer = None
        self.type = None
        self.model = None
        self.latitude = 0.0
        self.longitude = 0.0
        self.elevation = 0.0
        self.x = 0.0
        self.x2 = 0.0
        self.y = 0.0
        self.y2 = 0.0
        super().__init__(attr_dict=ATTR_DICT["electrode"], **kwargs)

    @property
    def length(self):
        return np.sqrt((self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2)

    @property
    def azimuth(self):
        return np.rad2deg(np.arctan2((self.y2 - self.y), (self.x2 - self.x)))


# =============================================================================
# Timing System
# =============================================================================
