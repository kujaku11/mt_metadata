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

from mt_metadata.base.helpers import element_to_string
from mt_metadata.common import Instrument as CommonInstrument


# =============================================================================
class Instrument(CommonInstrument):
    def to_xml(self, string: bool = False, required: bool = False) -> str | et.Element:
        """
        Convert the Instrument object to an XML element or string.
        :param string: If True, return as a string; otherwise, return as an XML element.
        :type string: bool, optional
        :param required: If True, include only required fields; otherwise, include all fields.
        :type required: bool, optional
        :return: XML representation of the Instrument object.
        :rtype: str | et.Element

        """

        root = et.Element(self.__class__.__name__)
        if self.type not in [None, ""]:
            root.attrib["type"] = self.type

        for key in ["manufacturer", "name", "id", "settings"]:
            value = getattr(self, key)
            if key not in [None, "", "null"]:
                et.SubElement(root, key).text = value

        if string:
            return element_to_string(root)
        return root
