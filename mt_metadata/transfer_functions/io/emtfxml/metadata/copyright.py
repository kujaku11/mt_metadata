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
from . import Citation
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = get_schema("copyright", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("citation", SCHEMA_FN_PATHS), "citation")

# =============================================================================
class Copyright(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.citation = Citation()

        super().__init__(attr_dict=attr_dict, **kwargs)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "copyright")

    def to_xml(self, string=False, required=True):
        """ """
        self.release_status = self.release_status.title()
        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=[
                "citation",
                "acknowledgement",
                "release_status",
                "conditions_of_use",
            ],
        )
