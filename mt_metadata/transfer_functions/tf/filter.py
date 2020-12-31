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
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("filter", SCHEMA_FN_PATHS)
# =============================================================================
class Filter(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.name = None
        self.type = None
        self.units_in = None
        self.units_out = None
        self._calibration_dt = MTime()
        self.operation = None
        self.normalization_frequency = None
        self.normalization_factor = None
        self.cutoff = None
        self.n_poles = None
        self.n_zeros = None
        self.comments = None
        self.conversion_factor = None

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def calibration_date(self):
        return self._calibration_dt.date

    @calibration_date.setter
    def calibration_date(self, value):
        self._calibration_dt.from_str(value)
