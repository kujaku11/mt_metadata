# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.mttime import MTime


# =====================================================
class GDP(MetadataBase):
    date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None).date,
            description="start date of the measurement",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["01/01/2020"],
            },
        ),
    ]

    time: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="start time of the measurement",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["12:00:00"],
            },
        ),
    ]

    type: Annotated[
        str | None,
        Field(
            default=None,
            description="Type of GPD",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["zen"],
            },
        ),
    ]

    prog_ver: Annotated[
        str | None,
        Field(
            default=None,
            description="version of hadware in the GDP",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [0],
            },
        ),
    ]

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value).isodate()

    @field_validator("time", mode="before")
    @classmethod
    def validate_time(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value).isoformat().split("T")[1]
