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
from . import Dipole, Magnetometer, Comment
from mt_metadata.utils.mttime import MTime
from mt_metadata.transfer_functions.tf import Instrument

# =============================================================================
attr_dict = get_schema("field_notes", SCHEMA_FN_PATHS)
attr_dict.add_dict(Instrument()._attr_dict, "instrument")
attr_dict.add_dict(get_schema("comment", SCHEMA_FN_PATHS), "comments")

# =============================================================================
class FieldNotes(Base):
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
        self._start_dt.from_str(value)

    @property
    def end(self):
        return self._end_dt.iso_str

    @end.setter
    def end(self, value):
        self._end_dt.from_str(value)

    def read_dict(self, input_dict):
        """
        Field notes are odd so have a special reader to do it piece by
        painstaking piece.

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        field_notes = []
        if not isinstance(input_dict["field_notes"], list):
            field_notes = [input_dict["field_notes"]]
        else:
            field_notes = input_dict["field_notes"]

        for run in field_notes:
            f = FieldNotes()
            f.run = run["run"]
            f.instrument.from_dict({"instrument": run["instrument"]})
            f.sampling_rate = run["sampling_rate"]
            f.start = run["start"]
            f.end = run["end"]
            try:
                if isinstance(run["comments"], list):
                    f.comments.from_dict({"comments": run["comments"][0]})
                else:
                    f.comments.from_dict({"comments": run["comments"]})
            except KeyError:
                self.logger.debug("run has no comments")
            f.errors = run["errors"]

            try:
                if isinstance(run["magnetometer"], list):
                    f.magnetometer = []
                    for mag in run["magnetometer"]:
                        m = Magnetometer()
                        m.from_dict({"magnetometer": mag})
                        f.magnetometer.append(m)
                else:
                    f.magnetometer = []
                    m = Magnetometer()
                    m.from_dict({"magnetometer": run["magnetometer"]})
                    f.magnetometer.append(m)
            except KeyError:
                self.logger.debug("run has no magnetotmeter information")

            try:
                if isinstance(run["dipole"], list):
                    f.dipole = []
                    for mag in run["dipole"]:
                        m = Dipole()
                        m.from_dict({"dipole": mag})
                        f.dipole.append(m)
                else:
                    m = Dipole()
                    m.from_dict({"dipole": run["dipole"]})
                    f.dipole.append(m)
            except KeyError:
                self.logger.debug("run has no dipole information")

            field_notes.append(f)

        return field_notes

    def to_xml(self, string=True, required=False):
        """

        :param string: DESCRIPTION, defaults to True
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to False
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        for fn in self.field_notes:
            fn_element = self._convert_tag_to_capwords(
                fn.to_xml(required=False)
            )
            for dp in fn.dipole:
                dp_element = self._convert_tag_to_capwords(dp.to_xml())
                for electrode in dp.electrode:
                    self._write_element(dp_element, electrode)
                fn_element.append(dp_element)
            for mag in fn.magnetometer:
                self._write_element(fn_element, mag)
            parent.append(fn_element)
