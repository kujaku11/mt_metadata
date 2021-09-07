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
from . import Electrode

# =============================================================================
attr_dict = get_schema("dipole", SCHEMA_FN_PATHS)
attr_dict.add_dict(Electrode()._attr_dict, "electrode")

# =============================================================================
class Dipole(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.manufacturer = None
        self.length = None
        self.azimuth = None
        self.name = None

        super().__init__(attr_dict=attr_dict, **kwargs)
        self._electrode = []

    @property
    def electrode(self):
        return self._electrode

    @electrode.setter
    def electrode(self, value):
        if not isinstance(value, list):
            value = [value]
        for item in value:
            e_obj = Electrode()
            e_obj.from_dict(item)
            self._electrode.append(e_obj)
