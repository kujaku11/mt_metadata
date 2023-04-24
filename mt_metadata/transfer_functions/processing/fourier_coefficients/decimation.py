# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:20:59 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries import TimePeriod
from mt_metadata.transfer_functions.processing.aurora import Window
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("decimation", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict)
attr_dict.add_dict(Window()._attr_dict, "window")

# =============================================================================
class Decimation(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.window = Window()
        self._time_period = TimePeriod()
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def start(self):
        return self._time_period.start

    @start.setter
    def start(self, start):
        self._time_period.start = start

    @property
    def end(self):
        return self._time_period.end

    @end.setter
    def end(self, end):
        self._time_period.end = end
