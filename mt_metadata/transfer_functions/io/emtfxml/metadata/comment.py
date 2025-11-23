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
from mt_metadata.common.mttime import MTime

from .standards import SCHEMA_FN_PATHS


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
        return self._dt.isoformat()

    @date.setter
    def date(self, dt_str):
        self._dt.parse(dt_str)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        key = input_dict["comments"]
        if isinstance(key, str):
            self.value = key
        elif isinstance(key, dict):
            try:
                self.value = key["value"]
            except KeyError:
                self.logger.debug("No value in comment")

            try:
                self.author = key["author"]
            except KeyError:
                self.logger.debug("No author of comment")
            try:
                self.date = key["date"]
            except KeyError:
                self.logger.debug("No date for comment")
        else:
            raise TypeError(f"Comment cannot parse type {type(key)}")

    def to_xml(self, string=False, required=True):
        """ """
        if self.author is None:
            self.author = ""
        root = et.Element(self.__class__.__name__ + "s", {"author": self.author})
        if self.value is None:
            self.value = ""
        root.text = self.value

        if string:
            return element_to_string(root)
        return root
