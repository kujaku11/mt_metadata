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
class ProcessingInfo(Base):
    __doc__ = write_lines(ATTR_DICT["xml_processing_info"])

    def __init__(self, **kwargs):
        self.sign_convention = None
        self.processed_by = None
        self.remote_ref = None
        self.processing_software = Software()
        self.processing_tag = None

        super().__init__(attr_dict=ATTR_DICT["xml_processing_info"], **kwargs)


