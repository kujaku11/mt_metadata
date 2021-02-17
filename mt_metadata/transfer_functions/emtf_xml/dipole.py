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
from . import Electrode

# =============================================================================
attr_dict = get_schema("dipole", SCHEMA_FN_PATHS)
attr_dict.add_dict(Electrode()._attr_dict, "positive")
attr_dict.add_dict(Electrode()._attr_dict, "negative")
# =============================================================================
class Dipole(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.manufacturer = None
        self.length = None
        self.azimuth = None
        self.positive = Electrode()
        self.negative = Electrode()

        super().__init__(attr_dict=attr_dict, **kwargs)
