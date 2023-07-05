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
attr_dict = get_schema("magnetic", SCHEMA_FN_PATHS)
# =============================================================================


class Magnetic(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.orientation is None:
            self.orientation = 0
        root = et.Element(
            self.__class__.__name__.capitalize(),
            {
                "name": self.name,
                "orientation": f"{self.orientation:.3f}",
                "x": f"{self.x:.3f}",
                "y": f"{self.y:.3f}",
                "z": f"{self.z:.3f}",
            },
        )

        if string:
            return element_to_string(root)
        return root
