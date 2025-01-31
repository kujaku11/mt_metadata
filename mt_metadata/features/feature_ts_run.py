# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:39:39 2025

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

from mt_metadata.timeseries import TimePeriod

# =============================================================================
attr_dict = get_schema("feature_ts_run", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod._attr_dict, "time_period")


# =============================================================================
class FeatureTSRun(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)
