# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common.mttime import MDate, MTime


# =====================================================
class TimePeriod(MetadataBase):
    """
    Time span of a period of time.
    """

    end: Annotated[
        str | float | int | np.datetime64 | pd.Timestamp | MTime,
        Field(
            default_factory=lambda: MTime(time_stamp="1980-01-01T00:00:00+00:00"),
            description="End date and time of collection in UTC.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "2020-02-04T16:23:45.453670+00:00",
                "type": "string",
            },
        ),
    ]

    start: Annotated[
        str | float | int | np.datetime64 | pd.Timestamp | MTime,
        Field(
            default_factory=lambda: MTime(),
            description="Start date and time of collection in UTC.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "2020-02-01T09:23:45.453670+00:00",
                "type": "string",
            },
        ),
    ]

    @field_validator("start", "end", mode="before")
    @classmethod
    def validate_time(cls, value, info: ValidationInfo) -> MTime:
        """
        Validate that the value is a valid time.
        """
        return MTime(time_stamp=value)

    def start_is_default(self) -> bool:
        """
        Check if the start time is the default time.
        """
        return MTime(time_stamp=self.start).is_default()

    def end_is_default(self) -> bool:
        """
        Check if the end time is the default time.
        """
        return MTime(time_stamp=self.end).is_default()


class TimePeriodDate(MetadataBase):
    """
    Time span of a period of time.
    """

    end_date: Annotated[
        str | float | int | np.datetime64 | pd.Timestamp | MTime | MDate,
        Field(
            default_factory=lambda: MDate(time_stamp="1980-01-01"),
            description="End date and time of collection in UTC.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "2020-02-04",
                "type": "string",
            },
        ),
    ]

    start_date: Annotated[
        str | float | int | np.datetime64 | pd.Timestamp | MTime | MDate,
        Field(
            default_factory=lambda: MDate(time_stamp="1980-01-01"),
            description="Start date and time of collection in UTC.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "2020-02-01",
                "type": "string",
            },
        ),
    ]

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def validate_time(cls, value, info: ValidationInfo) -> MTime:
        """
        Validate that the value is a valid time.
        """
        mt_date = MDate(time_stamp=value)
        return mt_date.isodate()

    def start_is_default(self) -> bool:
        """
        Check if the start time is the default time.
        """
        return MDate(time_stamp=self.start_date).is_default()

    def end_is_default(self) -> bool:
        """
        Check if the end time is the default time.
        """
        return MDate(time_stamp=self.end_date).is_default()
