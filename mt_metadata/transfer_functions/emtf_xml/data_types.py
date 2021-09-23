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
from . import DataType

# =============================================================================
attr_dict = get_schema("data_types", SCHEMA_FN_PATHS)
# =============================================================================


class DataTypes(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._data_types_list = []
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def data_types_list(self):
        return self._data_types_list

    @data_types_list.setter
    def data_types_list(self, value):
        if not isinstance(value, list):
            value = [value]

        for item in value:
            dt = DataType()
            dt.from_dict(item)
            self._data_types_list.append(dt)
