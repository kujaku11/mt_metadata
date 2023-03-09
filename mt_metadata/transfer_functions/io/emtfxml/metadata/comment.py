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
from mt_metadata.utils.mttime import MTime

# =============================================================================
attr_dict = get_schema("comment", SCHEMA_FN_PATHS)
# =============================================================================


class Comment(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._dt = MTime()
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def date(self):
        return self._dt.iso_str

    @date.setter
    def date(self, dt_str):
        self._dt.from_str(dt_str)

    def to_xml(self, string=False, required=True):
        """ """
        root = et.Element(
            self.__class__.__name__ + "s", {"author": self.author}
        )
        root.text = self.value

        if string:
            return element_to_string(root)
        return root
