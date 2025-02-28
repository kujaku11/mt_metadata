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
from mt_metadata.utils.mttime import MTime
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = get_schema("software", SCHEMA_FN_PATHS)
# =============================================================================


class ProcessingSoftware(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._last_mod_dt = MTime()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def last_mod(self):
        return self._last_mod_dt.date

    @last_mod.setter
    def last_mod(self, value):
        self._last_mod_dt.parse(value)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "processing_software")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=["name", "last_mod", "author"],
        )
