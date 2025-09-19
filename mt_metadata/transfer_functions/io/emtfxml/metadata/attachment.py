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
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = get_schema("attachment", SCHEMA_FN_PATHS)
# =============================================================================


class Attachment(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._attachments = []
        super().__init__(attr_dict=attr_dict, **kwargs)

    def read_dict(self, input_dict):
        element_dict = {self._class_name: input_dict[self._class_name]}
        if isinstance(element_dict[self._class_name], type(None)):
            return
        elif isinstance(element_dict[self._class_name], list):
            for item in element_dict[self._class_name]:
                attachment_item = Attachment()
                if not self._class_name in item.keys():
                    item = {self._class_name: item}
                attachment_item.from_dict(item)
                self._attachments.append(attachment_item)

        else:
            self.from_dict(element_dict)

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self._attachments == []:
            return helpers.to_xml(
                self,
                string=string,
                required=required,
                order=["filename", "description"],
            )

        else:
            return [
                helpers.to_xml(
                    item,
                    string=string,
                    required=required,
                    order=["filename", "description"],
                )
                for item in self._attachments
            ]
