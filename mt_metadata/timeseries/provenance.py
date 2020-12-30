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
from mt_metadata.utils.mttime import MTime
from . import Person, Software

# =============================================================================
attr_dict = get_schema("provenance", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("person", SCHEMA_FN_PATHS), "creator")
attr_dict.add_dict(get_schema("person", SCHEMA_FN_PATHS), "submitter")
attr_dict.add_dict(get_schema("software", SCHEMA_FN_PATHS), "software")
# =============================================================================
class Provenance(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._creation_dt = MTime()
        self._creation_dt.now()
        self.creating_application = "MT Metadata"
        self.creator = Person()
        self.submitter = Person()
        self.software = Software()
        self.log = None
        self.comments = None
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def creation_time(self):
        return self._creation_dt.iso_str

    @creation_time.setter
    def creation_time(self, dt_str):
        self._creation_dt.from_str(dt_str)
