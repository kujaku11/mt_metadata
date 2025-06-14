# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 12:25:44 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base import Base

from . import Run


# =============================================================================
class FieldNotes(Base):
    def __init__(self, **kwargs):
        self._run_list = []

        super().__init__(**kwargs)

    def __str__(self):
        lines = []
        for r in self.run_list:
            lines.append(r.__str__())
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    @property
    def run_list(self):
        return self._run_list

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
            self.logger.warning("Did not find any field notes in xml")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        return [r.to_xml(string=string, required=required) for r in self._run_list]
