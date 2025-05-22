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
