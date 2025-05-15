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
from xml.etree import cElementTree as et

from mt_metadata.base import Base, get_schema
from mt_metadata.base.helpers import element_to_string, write_lines

from . import DataType
from .standards import SCHEMA_FN_PATHS


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
        self._data_types_list = []
        for item in value:
            dt = DataType()
            dt.from_dict(item)
            self._data_types_list.append(dt)

    def read_dict(self, input_dict):
        """
        Read in statistical estimate descriptions

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        try:
            self.data_types_list = input_dict["data_types"]["data_type"]
        except KeyError:
            self.logger.warning("Could not read Data Types")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        root = et.Element(self.__class__.__name__)

        for dtype in self.data_types_list:
            root.append(dtype.to_xml(required=required))

        if string:
            return element_to_string(root)
        return root
