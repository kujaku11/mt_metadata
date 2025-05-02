# =====================================================
# Imports
# =====================================================
from typing import Annotated
from pydantic import Field, field_validator, ValidationInfo
import pandas as pd
import numpy as np

from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime, MDate


# =====================================================
class TimePeriod(MetadataBase):
    """
    Time span of a period of time.
    """

    end: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str | MTime,
        Field(
            default_factory=lambda: MTime(time_stamp="1980-01-01T00:00:00+00:00"),
            description="End date and time of collection in UTC.",
            examples="2020-02-04T16:23:45.453670+00:00",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    start: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str | MTime,
        Field(
            default_factory=lambda: MTime(time_stamp="1980-01-01T00:00:00+00:00"),
            description="Start date and time of collection in UTC.",
            examples="2020-02-01T09:23:45.453670+00:00",
            alias=None,
            type="string",
            json_schema_extra={
                "units": None,
                "required": True,
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


class TimePeriodDate(MetadataBase):
    """
    Time span of a period of time.
    """

    end_date: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str | MTime | MDate,
        Field(
            default_factory=lambda: MDate(time_stamp="1980-01-01"),
            description="End date and time of collection in UTC.",
            examples="2020-02-04",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    start_date: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str | MTime | MDate,
        Field(
            default_factory=lambda: MDate(time_stamp="1980-01-01"),
            description="Start date and time of collection in UTC.",
            examples="2020-02-01",
            alias=None,
            type="string",
            json_schema_extra={
                "units": None,
                "required": True,
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
