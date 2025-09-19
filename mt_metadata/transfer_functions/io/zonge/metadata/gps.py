# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 10:29:50 2021

:author: Jared Peacock

:license: MIT

"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from mt_metadata.transfer_functions.tf import Location

# =============================================================================
attr_dict = get_schema("gps", SCHEMA_FN_PATHS)
# =============================================================================


class GPS(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._location = Location()
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def lat(self):
        return self._location.latitude

    @lat.setter
    def lat(self, value):
        self._location.latitude = value

    @property
    def lon(self):
        return self._location.longitude

    @lon.setter
    def lon(self, value):
        self._location.longitude = value
