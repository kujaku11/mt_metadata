# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("birrp_angles", SCHEMA_FN_PATHS)


# =============================================================================
class BirrpAngles(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
