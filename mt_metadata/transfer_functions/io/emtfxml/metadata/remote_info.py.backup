# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:04:35 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from typing import Annotated
from xml.etree import ElementTree as et

from loguru import logger
from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

from . import FieldNotes, Site


class RemoteInfo(MetadataBase):
    site: Annotated[
        Site,
        Field(
            default_factory=Site,  # type: ignore
            description="Site information",
            examples=["Site(name='Test Site', location='Test Location')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    field_notes: Annotated[
        FieldNotes,
        Field(
            default_factory=FieldNotes,  # type: ignore
            description="Field notes information",
            examples=["FieldNotes(...)"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    _order: list = ["site", "field_notes"]

    def read_dict(self, input_dict: dict) -> None:
        """
        Read metadata from a dictionary.

        Parameters
        ----------
        input_dict : dict
            A dictionary containing metadata information.
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
                logger.debug(f"No {key} information in xml.")
            except AttributeError:
                # This handles the case where the key is not an attribute of the class
                # or the attribute does not have a read_dict method.
                logger.warning(
                    f"Failed access {key} from remote_info_dict {remote_info_dict}."
                )
                return

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the RemoteInfo object to XML format.

        Parameters
        ----------
        string : bool, optional
            Whether to return the XML as a string (default is False).
        required : bool, optional
            Whether to include required fields (default is True).

        Returns
        -------
        str | et.Element
            The XML representation of the RemoteInfo object.
        """
        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=self._order,
        )
