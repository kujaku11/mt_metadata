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
from . import Citation

# =============================================================================
attr_dict = get_schema("copyright", SCHEMA_FN_PATHS)
# =============================================================================
class Copyright(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.citation = Citation()

        super().__init__(attr_dict=attr_dict, **kwargs)
