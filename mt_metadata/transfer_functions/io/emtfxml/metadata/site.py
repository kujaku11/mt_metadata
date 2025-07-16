# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import BasicLocation, Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers
from mt_metadata.utils.mttime import MTime

from . import DataQualityNotes, DataQualityWarnings, Orientation


# =====================================================
class Site(MetadataBase):
    project: Annotated[
        str,
        Field(
            default="",
            description="Name of the project",
            examples=["USMTArray"],
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    survey: Annotated[
        str,
        Field(
            default="",
            description="Name of the survey",
            examples=["MT 2020"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    year_collected: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default=None,
            description="Year data collected",
            examples=["2020"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    country: Annotated[
        str,
        Field(
            default="",
            description="Country where data was collected",
            examples=["USA"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Station ID name.  This should be an alpha numeric name that is typically 5-6 characters long.  Commonly the project name in 2 or 3 letters and the station number.",
            examples=["MT001"],
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    name: Annotated[
        str,
        Field(
            default="",
            description="closest geographic name to the station",
            examples=['"Whitehorse, YK"'],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    acquired_by: Annotated[
        str,
        Field(
            default="",
            description="Person or group who collected the data",
            examples=["MT Group"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
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

    run_list: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of runs recorded by the station. Should be a summary of all runs recorded",
            examples=['"[ mt001a, mt001b, mt001c ]"'],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    data_quality_notes: Annotated[
        DataQualityNotes,
        Field(
            default_factory=DataQualityNotes,  # type: ignore
            description="Notes on the data quality",
            examples=["Data quality is good"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data_quality_warnings: Annotated[
        DataQualityWarnings,
        Field(
            default_factory=DataQualityWarnings,  # type: ignore
            description="Warnings about the data quality",
            examples=["Data quality is questionable"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
    orientation: Annotated[
        Orientation,
        Field(
            default_factory=Orientation,  # type: ignore
            description="Orientation of the site",
            examples=[
                "Orientation('layout=orthogonal, angle_to_geographic_north=0.0')"
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    location: Annotated[
        BasicLocation,
        Field(
            default_factory=BasicLocation,  # type: ignore
            description="Location of the site",
            examples=["BasicLocation('latitude=60.0, longitude=-135.0')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment | str | None,
        Field(
            default_factory=Comment,  # type: ignore
            description="Comments about the site",
            examples=["Comment('This is a comment about the site')"],
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
        if isinstance(field_value, MTime):
            return field_value
        return MTime(time_stamp=field_value)

    @field_validator("year_collected", mode="before")
    @classmethod
    def validate_year_collected(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        if isinstance(field_value, MTime):
            return field_value.year
        return MTime(time_stamp=field_value).year

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value) -> Comment:
        """
        Validate that the value is a valid string.
        """
        if isinstance(value, str):
            return Comment(value=value)  # type: ignore[return-value]
        return value

    @field_validator("run_list", mode="before")
    @classmethod
    def validate_run_list(cls, value: str | list[str] | None) -> list[str] | None:
        """
        Validate that the value is a list of strings.
        """
        if value is None:
            return None
        if isinstance(value, str):
            if value.count(",") > 0:
                return value.split(",")
            else:
                return value.split(" ")

        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            return value
        raise ValueError("run_list must be a list of strings.")

    def read_dict(self, input_dict: dict) -> None:
        """
        Read the input dictionary and update the object's attributes.

        Parameters
        ----------
        input_dict : dict
            The input dictionary containing the data to read.
        """
        for element in input_dict["site"].keys():
            attr = getattr(self, element)
            if hasattr(attr, "read_dict"):
                attr.read_dict(input_dict["site"])
            else:
                helpers._read_single(self, input_dict["site"], element)

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the object to XML format.

        Parameters
        ----------
        string : bool, optional
            Whether to return the XML as a string, by default False
        required : bool, optional
            Whether the XML is required, by default True

        Returns
        -------
        str | et.Element
            The XML representation of the object.
        """

        if self.end < self.start:  # type: ignore
            self.end = self.start

        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=[
                "project",
                "survey",
                "year_collected",
                "country",
                "id",
                "name",
                "location",
                "orientation",
                "acquired_by",
                "start",
                "end",
                "run_list",
                "data_quality_notes",
                "data_quality_warnings",
            ],
        )
