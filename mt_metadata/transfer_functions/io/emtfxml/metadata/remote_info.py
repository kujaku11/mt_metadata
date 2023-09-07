# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:04:35 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base, BaseDict
from .standards import SCHEMA_FN_PATHS
from mt_metadata.transfer_functions.io.emtfxml.metadata import Site, FieldNotes
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = BaseDict()
attr_dict.add_dict(get_schema("site", SCHEMA_FN_PATHS), "site")
# =============================================================================


class RemoteInfo(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.site = Site()
        self.field_notes = FieldNotes()
        self._order = ["site", "field_notes"]

        super().__init__(attr_dict=attr_dict, **kwargs)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        try:
            remote_info_dict = input_dict["remote_info"]
        except KeyError:
            return
        for key in ["site", "field_notes"]:
            try:
                pop_dict = {key: remote_info_dict.pop(key)}
                getattr(self, key).read_dict(pop_dict)
            except KeyError:
                self.logger.debug(f"No {key} information in xml.")

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
            order=self._order,
        )
