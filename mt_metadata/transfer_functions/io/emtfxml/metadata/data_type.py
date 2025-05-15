# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("data_type", SCHEMA_FN_PATHS)
# =============================================================================


class DataType(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "estimate")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        element = helpers.to_xml(
            self,
            string=string,
            required=required,
            order=["description", "external_url", "intention", "tag"],
        )
        element.attrib = {
            "name": self.name,
            "type": self.type,
            "output": self.output,
            "input": self.input,
            "units": self.units,
        }

        return element
