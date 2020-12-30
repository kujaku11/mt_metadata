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
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("instrument", SCHEMA_FN_PATHS)
attr_dict.add_dict(
    get_schema("location", SCHEMA_FN_PATHS),
    "northwest_corner",
    keys=["latitude", "longitude", "elevation", "x", "x2", "y", "y2"],
)

# =============================================================================
class Electrode(Base):
    __doc__ = write_lines(attr_dict)

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
        super().__init__(attr_dict=attr_dict, **kwargs)
        
    @property
    def length(self):
        return np.sqrt((self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2)
    
    @property
    def azimuth(self):
        return np.rad2deg(np.arctan2((self.y2 - self.y), (self.x2 - self.x)))
