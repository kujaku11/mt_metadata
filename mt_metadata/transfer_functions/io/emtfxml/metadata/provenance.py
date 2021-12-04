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
from . import Person
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("provenance", SCHEMA_FN_PATHS)
person_dict = get_schema("person", SCHEMA_FN_PATHS)
attr_dict.add_dict(person_dict, "creator")
attr_dict.add_dict(person_dict, "submitter")
# =============================================================================


class Provenance(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._creation_dt = MTime()
        self.creating_application = None
        self.submitter = Person()
        self.creator = Person()
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def create_time(self):
        return self._creation_dt.iso_str

    @create_time.setter
    def create_time(self, dt_str):
        self._creation_dt.from_str(dt_str)
