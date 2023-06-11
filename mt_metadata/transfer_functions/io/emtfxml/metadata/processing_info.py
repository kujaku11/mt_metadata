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
from . import ProcessingSoftware, RemoteRef, RemoteInfo
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =============================================================================
attr_dict = get_schema("processing_info", SCHEMA_FN_PATHS)
attr_dict.add_dict(ProcessingSoftware()._attr_dict, "processing_software")
attr_dict.add_dict(RemoteRef()._attr_dict, "remote_ref")
attr_dict.add_dict(RemoteInfo()._attr_dict, "remote_info")

for key, ad in attr_dict.items():
    if "remote_info" in key:
        ad["required"] = False
# =============================================================================


class ProcessingInfo(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.remote_ref = RemoteRef()
        self.processing_software = ProcessingSoftware()
        self.remote_info = RemoteInfo()

        super().__init__(attr_dict=attr_dict, **kwargs)

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        try:
            processing_dict = input_dict["processing_info"]
        except KeyError:
            return

        for key in ["remote_ref", "remote_info", "processing_software"]:
            try:
                pop_dict = {key: processing_dict.pop(key)}
                getattr(self, key).read_dict(pop_dict)
            except KeyError:
                self.logger.debug(f"No {key} information in xml.")

        helpers._read_element(self, input_dict, "processing_info")

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
            order=[
                "sign_convention",
                "remote_ref",
                "remote_info",
                "processed_by",
                "processing_software",
                "processing_tag",
            ],
        )
