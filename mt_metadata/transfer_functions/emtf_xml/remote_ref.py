# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:04:35 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("remote_ref", SCHEMA_FN_PATHS)
# =============================================================================

class RemoteRef(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.type = None

        super().__init__(attr_dict=attr_dict, **kwargs)