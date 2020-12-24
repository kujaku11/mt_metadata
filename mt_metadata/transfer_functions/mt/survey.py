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
from mt_metadata.helpers import write_lines
from mt_metadata.transfer_functions.mt.standards.schema import Standards

ATTR_DICT = Standards().ATTR_DICT
# =============================================================================
class TransferFunction(Base):
    __doc__ = write_lines(ATTR_DICT["transfer_function"])

    def __init__(self, **kwargs):

        self.processed_by = Person()
        self.software = Software()
        self.units = "millivolts_per_kilometer_per_nanotesla"
        self.sign_convention = "+"
        self.runs_processed = []
        self.remote_references = []
        self.processing_parameters = []
        self._processed_date = MTime()

        super().__init__(attr_dict=ATTR_DICT["transfer_function"], **kwargs)

    @property
    def processed_date(self):
        return self._processed_date.date

    @processed_date.setter
    def processed_date(self, value):
        self._processed_date = value


# ==============================================================================
# Site details
# ==============================================================================
