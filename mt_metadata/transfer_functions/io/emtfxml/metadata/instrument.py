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

# =============================================================================
attr_dict = get_schema("magnetometer", SCHEMA_FN_PATHS)
# =============================================================================
class Instrument(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)

    def to_xml(self, string=False, required=False):
        """ """

        root = et.Element(self.__class__.__name__, {"type": self.type})

        for key in ["manufacturer", "name", "id", "settings"]:
            value = getattr(self, key)
            if key not in [None, "", "null"]:
                et.SubElement(root, key).text = value

        if string:
            return element_to_string(root)
        return root
