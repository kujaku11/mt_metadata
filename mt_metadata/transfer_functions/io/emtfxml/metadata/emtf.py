# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 18:21:25 2021

@author: jpeacock
"""
from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("emtf", SCHEMA_FN_PATHS)
# =============================================================================


class EMTF(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
