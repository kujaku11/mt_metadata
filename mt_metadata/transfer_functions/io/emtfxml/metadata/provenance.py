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
from mt_metadata.base.helpers import (
    write_lines,
    dict_to_xml,
    element_to_string,
)
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Person
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers
from mt_metadata.utils.mttime import MTime, get_now_utc
from mt_metadata import __version__

# =============================================================================
attr_dict = get_schema("provenance", SCHEMA_FN_PATHS)
person_dict = get_schema("person", SCHEMA_FN_PATHS)
attr_dict.add_dict(person_dict, "creator")
attr_dict.add_dict(person_dict, "submitter")
# =============================================================================


class Provenance(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._creation_dt = MTime()
        self.submitter = Person()
        self.creator = Person()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def create_time(self):
        return self._creation_dt.iso_str.split(".")[0]

    @create_time.setter
    def create_time(self, dt_str):
        self._creation_dt.parse(dt_str)

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.creating_application = f"mt_metadata {__version__}"
        self.create_time = get_now_utc()

        element = dict_to_xml(
            self.to_dict(nested=True, required=required), self._attr_dict
        )
        if not string:
            return element
        else:
            return element_to_string(element)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "provenance")
