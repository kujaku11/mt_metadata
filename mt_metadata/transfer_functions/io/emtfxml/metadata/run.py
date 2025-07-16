# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from loguru import logger
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import element_to_string
from mt_metadata.common import Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers
from mt_metadata.utils.mttime import MTime

from . import Dipole, Instrument, Magnetometer


# =====================================================
class Run(MetadataBase):
    errors: Annotated[
        str | None,
        Field(
            default=None,
            description="Any field errors",
            examples=["moose ate cables"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    run: Annotated[
        str,
        Field(
            default="",
            description="Run name",
            examples=["mt001a"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sampling_rate: Annotated[
        float | None,
        Field(
            default=None,
            description="Sample rate of the run",
            examples=["1"],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": False,
            },
        ),
    ]

    start: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date time when the data collection started",
            examples=["2020-01-01T12:00:00"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    end: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date time when the data collection ended",
            examples=["2020-05-01T12:00:00"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    comments: Annotated[
        Comment | str | None,
        Field(
            default_factory=Comment,  # type: ignore
            description="Comments about the run",
            examples=["Comment(text='This is a comment')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    instrument: Annotated[
        Instrument,
        Field(
            default_factory=Instrument,  # type: ignore
            description="Instrument used for the run",
            examples=["Instrument(name='MT Sensor', type='magnetometer')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    magnetometer: Annotated[
        list[Magnetometer],
        Field(
            default_factory=list,
            description="List of magnetometers used in the run",
            examples=["Magnetometer(name='Magnetometer 1', type='fluxgate')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
    dipole: Annotated[
        list[Dipole],
        Field(
            default_factory=list,
            description="List of dipoles used in the run",
            examples=["Dipole(name='Dipole 1', type='fluxgate')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("start", "end", mode="before")
    @classmethod
    def validate_start(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, field_value: Comment | str | None):
        if isinstance(field_value, str):
            return Comment(value=field_value)
        return field_value

    def read_dict(self, input_dict: dict) -> None:
        """
        Field notes are odd so have a special reader to do it piece by
        painstaking piece.

        :param input_dict: input dictionary containing run data
        :type input_dict: dict
        :return: None
        :rtype: None

        """

        self.run = input_dict["run"]
        self.instrument.from_dict({"instrument": input_dict["instrument"]})
        self.sampling_rate = input_dict["sampling_rate"]
        self.start = input_dict["start"]
        self.end = input_dict["end"]
        try:
            if isinstance(input_dict["comments"], list):
                self.comments.from_dict({"comments": input_dict["comments"][0]})
            else:
                self.comments.from_dict({"comments": input_dict["comments"]})
        except KeyError:
            logger.debug("run has no comments")
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
            logger.debug("run has no magnetotmeter information")

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
            logger.debug("run has no dipole information")

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
