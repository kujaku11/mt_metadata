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
from mt_metadata.base.helpers import write_lines, element_to_string
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Dipole, Magnetometer, Comment, Instrument
from mt_metadata.utils.mttime import MTime
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

# =============================================================================
attr_dict = get_schema("run", SCHEMA_FN_PATHS)
attr_dict.add_dict(Instrument()._attr_dict, "instrument")
attr_dict.add_dict(get_schema("comment", SCHEMA_FN_PATHS), "comments")

# =============================================================================
class Run(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.errors = None
        self.run = None
        self._start_dt = MTime()
        self._end_dt = MTime()
        self.instrument = Instrument()
        self.magnetometer = [Magnetometer()]
        self.dipole = [Dipole()]
        self.sampling_rate = None
        self.comments = Comment()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def start(self):
        return self._start_dt.iso_str

    @start.setter
    def start(self, value):
        self._start_dt.parse(value)

    @property
    def end(self):
        return self._end_dt.iso_str

    @end.setter
    def end(self, value):
        self._end_dt.parse(value)

    def read_dict(self, input_dict):
        """
        Field notes are odd so have a special reader to do it piece by
        painstaking piece.

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.run = input_dict["run"]
        self.instrument.from_dict({"instrument": input_dict["instrument"]})
        self.sampling_rate = input_dict["sampling_rate"]
        self.start = input_dict["start"]
        self.end = input_dict["end"]
        try:
            if isinstance(input_dict["comments"], list):
                self.comments.from_dict(
                    {"comments": input_dict["comments"][0]}
                )
            else:
                self.comments.from_dict({"comments": input_dict["comments"]})
        except KeyError:
            self.logger.debug("run has no comments")
        self.errors = input_dict["errors"]

        try:
            if isinstance(input_dict["magnetometer"], list):
                self.magnetometer = []
                for mag in input_dict["magnetometer"]:
                    m = Magnetometer()
                    m.from_dict({"magnetometer": mag})
                    self.magnetometer.append(m)
            else:
                self.magnetometer = []
                m = Magnetometer()
                m.from_dict({"magnetometer": input_dict["magnetometer"]})
                self.magnetometer.append(m)
        except KeyError:
            self.logger.debug("run has no magnetotmeter information")

        try:
            if isinstance(input_dict["dipole"], list):
                self.dipole = []
                for mag in input_dict["dipole"]:
                    m = Dipole()
                    m.from_dict({"dipole": mag})
                    self.dipole.append(m)
            else:
                m = Dipole()
                m.from_dict({"dipole": input_dict["dipole"]})
                self.dipole.append(m)
        except KeyError:
            self.logger.debug("run has no dipole information")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to True
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to False
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        element = helpers.to_xml(
            self,
            string=False,
            required=required,
            order=[
                "instrument",
                "magnetometer",
                "dipole",
                "comments",
                "errors",
                "sampling_rate",
                "start",
                "end",
            ],
        )
        element.attrib = {"run": self.run}
        element.tag = "field_notes"

        element.find("SamplingRate").attrib["units"] = "Hz"

        if string:
            return element_to_string(element)
        return element
