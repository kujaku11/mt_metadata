# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:20:59 2022

@author: jpeacock
"""
from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.timeseries import TimePeriod

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("fc_channel", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict, "time_period")


# =============================================================================
class Channel(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.time_period = TimePeriod()
        super().__init__(attr_dict=attr_dict, **kwargs)
