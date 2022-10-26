# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:04:35 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base, BaseDict
from .standards import SCHEMA_FN_PATHS
from mt_metadata.transfer_functions.io.emtfxml.metadata import Site, FieldNotes

# =============================================================================
attr_dict = BaseDict()
attr_dict.add_dict(get_schema("site", SCHEMA_FN_PATHS), "site")
attr_dict.add_dict(get_schema("field_notes", SCHEMA_FN_PATHS), "field_notes")
# =============================================================================


class RemoteInfo(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.site = Site()
        self.field_notes = FieldNotes()

        super().__init__(attr_dict=attr_dict, **kwargs)
