# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime


# =====================================================
class Site(MetadataBase):
    project: Annotated[
        str,
        Field(
            default="",
            description="Name of the project",
            examples="USMTArray",
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
            examples="MT 2020",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    year_collected: Annotated[
        int,
        Field(
            default=None,
            description="Year data collected",
            examples="2020",
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
            examples="USA",
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
            examples="MT001",
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
            examples='"Whitehorse, YK"',
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
            examples="MT Group",
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
            examples="2020-01-01T12:00:00",
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
            examples="2020-05-01T12:00:00",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    run_list: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of runs recorded by the station. Should be a summary of all runss recorded",
            examples='"[ mt001a, mt001b, mt001c ]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("start", mode="before")
    @classmethod
    def validate_start(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("end", mode="before")
    @classmethod
    def validate_end(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
