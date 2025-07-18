# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:39:39 2025

@author: jpeacock
"""
<<<<<<<< HEAD:mt_metadata/processing/aurora/decimation.py
from mt_metadata.base import Base, get_schema
========
>>>>>>>> main:mt_metadata/features/feature_fc_run.py

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines

from .standards import SCHEMA_FN_PATHS

<<<<<<<< HEAD:mt_metadata/processing/aurora/decimation.py
========
from mt_metadata.timeseries import TimePeriod
>>>>>>>> main:mt_metadata/features/feature_fc_run.py

# =============================================================================
attr_dict = get_schema("feature_fc_run", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict, "time_period")


# =============================================================================
class FeatureFCRun(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
<<<<<<<< HEAD:mt_metadata/processing/aurora/decimation.py
========

        self.time_period = TimePeriod()
>>>>>>>> main:mt_metadata/features/feature_fc_run.py
        super().__init__(attr_dict=attr_dict, **kwargs)
