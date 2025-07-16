# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 12:25:44 2023

@author: jpeacock
"""
from xml.etree import ElementTree as et

from loguru import logger

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base import MetadataBase

from .run_basemodel import Run


# =============================================================================
class FieldNotes(MetadataBase):
    _run_list: list[Run] = []

    def __str__(self):
        lines = []
        for r in self._run_list:
            lines.append(r.__str__())
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def read_dict(self, input_dict):
        self._run_list = []
        try:
            if not isinstance(input_dict["field_notes"], list):
                run_list = [input_dict["field_notes"]]
            else:
                run_list = input_dict["field_notes"]

            for run in run_list:
                r = Run()
                r.read_dict(run)

                self._run_list.append(r)
        except KeyError:
            logger.warning("Did not find any field notes in xml")

    def to_xml(
        self, string: bool = False, required: bool = True
    ) -> list[str | et.Element]:
        """
        Convert the FieldNotes instance to XML format.

        Parameters
        ----------
        string : bool, optional
            If True, return XML as a string, by default False
        required : bool, optional
            If True, include all required fields, by default True

        Returns
        -------
        list[str | et.Element]
            The XML representation of the FieldNotes instance
        """

        return [r.to_xml(string=string, required=required) for r in self._run_list]
