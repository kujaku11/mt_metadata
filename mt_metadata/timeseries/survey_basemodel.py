# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, ValidationInfo, field_validator
from pyproj import CRS

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    Person,
    Citation,
    Location,
    Fdsn,
    FundingSource,
    TimePeriod,
)

from mt_metadata.timeseries.station_basemodel import Station


# =====================================================


class Survey(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Alpha numeric ID that will be unique for archiving.",
            examples="EMT20",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        str | None,
        Field(
            default_factory=lambda: Comment(),
            description="Any comments about the survey.",
            examples="long survey",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    datum: Annotated[
        str | int,
        Field(
            default="WGS84",
            description="Datum of latitude and longitude coordinates. Should be a well-known datum, such as WGS84, and will be the reference datum for all locations.  This is important for the user, they need to make sure all coordinates in the survey and child items (i.e. stations, channels) are referenced to this datum.",
            examples="WGS84",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    geographic_name: Annotated[
        str,
        Field(
            default="",
            description="Closest geographic reference to survey, usually a city but could be a landmark or some other common geographic reference point.",
            examples="Yukon",
            alias=None,
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
            description="Descriptive name of the survey.",
            examples="MT Characterization of Yukon Terrane",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    project: Annotated[
        str,
        Field(
            default="",
            description="Alpha numeric name for the project e.g USGS-GEOMAG.",
            examples="YUTOO",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    summary: Annotated[
        str,
        Field(
            default="",
            description="Summary paragraph of survey including the purpose; difficulties; data quality; summary of outcomes if the data have been processed and modeled.",
            examples="long project of characterizing mineral resources in Yukon",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,
            description="End date of the survey in UTC.",
            examples="1995-01-01",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("datum", mode="before")
    @classmethod
    def validate_datum(cls, value: str | int) -> str:
        """
        Validate the datum value and convert it to the appropriate enum type.
        """
        try:
            datum_crs = CRS.from_user_input(value)
            return datum_crs.name
        except Exception:
            raise ValueError(
                f"Invalid datum value: {value}. Must be a valid CRS string or identifier."
            )
