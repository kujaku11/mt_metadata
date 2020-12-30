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
attr_dict = get_schema("transfer_function", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("person", SCHEMA_FN_PATHS), "processed_by")
attr_dict.add_dict(get_schema("software", SCHEMA_FN_PATHS), "software")
# =============================================================================
class TransferFunction(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.processed_by = Person()
        self.software = Software()
        self.units = "millivolts_per_kilometer_per_nanotesla"
        self.sign_convention = "+"
        self.runs_processed = []
        self.remote_references = []
        self.processing_parameters = []
        self._processed_date = MTime()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def processed_date(self):
        return self._processed_date.date

    @processed_date.setter
    def processed_date(self, value):
        self._processed_date = value


# ==============================================================================
# Site details
# ==============================================================================
