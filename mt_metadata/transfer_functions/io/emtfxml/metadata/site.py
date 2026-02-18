# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from mt_metadata.common.mttime import MTime
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers, Location

from . import DataQualityNotes, DataQualityWarnings, Orientation


# =====================================================
class Site(MetadataBase):
    project: Annotated[
        str,
        Field(
            default="",
            description="Name of the project",
            alias=None,
            pattern="^[a-zA-Z0-9-_]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["USMTArray"],
            },
        ),
    ]

    survey: Annotated[
        str,
        Field(
            default="",
            description="Name of the survey",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["MT 2020"],
            },
        ),
    ]

    year_collected: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default=None,
            description="Year data collected",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2020"],
            },
        ),
    ]

    country: Annotated[
        str,
        Field(
            default="",
            description="Country where data was collected",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["USA"],
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Station ID name.  This should be an alpha numeric name that is typically 5-6 characters long.  Commonly the project name in 2 or 3 letters and the station number.",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["MT001"],
            },
        ),
    ]

    name: Annotated[
        str,
        Field(
            default="",
            description="closest geographic name to the station",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ['"Whitehorse, YK"'],
            },
        ),
    ]

    acquired_by: Annotated[
        str,
        Field(
            default="",
            description="Person or group who collected the data",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["MT Group"],
            },
        ),
    ]

    start: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date time when the data collection started",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2020-01-01T12:00:00"],
            },
        ),
    ]

    end: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date time when the data collection ended",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2020-05-01T12:00:00"],
            },
        ),
    ]

    run_list: Annotated[
        list[str] | None,
        Field(
            default_factory=list,
            description="list of runs recorded by the station. Should be a summary of all runs recorded",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ['"[ mt001a, mt001b, mt001c ]"'],
            },
        ),
    ]

    data_quality_notes: Annotated[
        DataQualityNotes,
        Field(
            default_factory=DataQualityNotes,  # type: ignore
            description="Notes on the data quality",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Data quality is good"],
            },
        ),
    ]

    data_quality_warnings: Annotated[
        DataQualityWarnings,
        Field(
            default_factory=DataQualityWarnings,  # type: ignore
            description="Warnings about the data quality",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Data quality is questionable"],
            },
        ),
    ]
    orientation: Annotated[
        Orientation,
        Field(
            default_factory=Orientation,  # type: ignore
            description="Orientation of the site",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [
                    "Orientation('layout=orthogonal, angle_to_geographic_north=0.0')"
                ],
            },
        ),
    ]

    location: Annotated[
        Location,
        Field(
            default_factory=Location,  # type: ignore
            description="Location of the site",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [
                    "Location('latitude=60.0, longitude=-135.0, declination=10.0')"
                ],
            },
        ),
    ]

    comments: Annotated[
        Comment | str | None,
        Field(
            default_factory=Comment,  # type: ignore
            description="Comments about the site",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Comment('This is a comment about the site')"],
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
        if isinstance(field_value, str):
            if field_value.count("-") == 1:
                field_value = field_value.split("-")[0]
        if isinstance(field_value, MTime):
            return field_value.year
        if isinstance(field_value, int):
            # If it's already an integer year, return as-is
            return field_value
        return MTime(time_stamp=field_value).year

    @field_validator("id", "project", "survey", "name", "acquired_by", mode="before")
    @classmethod
    def validate_string_fields(cls, field_value: str | None) -> str:
        """
        Validate string fields, converting None to empty string.
        """
        if field_value is None:
            return ""
        return str(field_value)

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
            if value.count("[") > 0 and value.count("]") > 0:
                # Handle string representation of a list
                value = value.strip("[]")

            if value.count(",") > 0:
                return value.split(",")
            elif value.count(" ") > 0:
                # Split by space if no commas are present
                return value.split(" ")
            if value == "":
                return []
            return [value]  # Return as a single-item list if no commas or spaces

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
