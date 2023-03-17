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

from mt_metadata.base.helpers import write_lines, element_to_string
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = get_schema("period_range", SCHEMA_FN_PATHS)
# =============================================================================
class PeriodRange(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)

    def read_dict(self, input_dict):
        helpers._read_element(self, input_dict, "period_range")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        root = et.Element(
            self.__class__.__name__,
            {"min": f"{self.min:.9f}", "max": f"{self.max:.9f}"},
        )
        if string:
            return element_to_string(root)
        return root
