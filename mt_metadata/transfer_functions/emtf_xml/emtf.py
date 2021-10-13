# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 18:21:25 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("emtf", SCHEMA_FN_PATHS)
# =============================================================================


class EMTF(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.description = None
        self.product_id = None
        self.sub_type = "MT_TF"
        self.notes = None
        self.tags = None

        super().__init__(attr_dict=attr_dict, **kwargs)
