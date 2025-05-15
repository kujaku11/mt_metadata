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

from . import Electrode
from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("dipole", SCHEMA_FN_PATHS)


# =============================================================================
class Dipole(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
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
            self.__class__.__name__, {"name": self.name, "type": self.type}
        )
        try:
            et.SubElement(root, "manufacturer").text = self.manufacturer
        except AttributeError:
            self.logger.debug("Dipole has no manufacturer information")
        if self.length is not None:
            et.SubElement(
                root, "length", {"units": "meters"}
            ).text = f"{self.length:.3f}"
        if self.azimuth is not None:
            et.SubElement(
                root, "azimuth", {"units": "degrees"}
            ).text = f"{self.azimuth:.3f}"
        for item in self.electrode:
            root.append(item.to_xml())

        if string:
            return element_to_string(root)
        return root
