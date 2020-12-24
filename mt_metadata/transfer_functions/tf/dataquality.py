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

# =============================================================================
attr_dict = get_schema(name, SCHEMA_FN_PATHS)
# =============================================================================
class DataQuality(Base):
    __doc__ = write_lines(ATTR_DICT["data_quality"])

    def __init__(self, **kwargs):

        self.rating = Rating()
        self.warnings = None

        super().__init__(attr_dict=ATTR_DICT["data_quality"], **kwargs)


# ==============================================================================
# Citation
# ==============================================================================
