# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
import pandas as pd
from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime
from pydantic import Field, field_validator


# =====================================================
class TypeEnum(str, Enum):
    fap_table = "fap_table"
    zpk = "zpk"
    time_delay = "time_delay"
    coefficient = "coefficient"
    fir = "fir"
    other = "other"


class FilterBase(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of filter applied or to be applied. If more than one filter input as a comma separated list.",
            examples='"lowpass_magnetic"',
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments about the filter.",
            examples="ambient air temperature",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    type: Annotated[
        TypeEnum,
        Field(
            default="",
            description="Type of filter, must be one of the available filters.",
            examples="fap_table",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units_in: Annotated[
        str,
        Field(
            default="",
            description="Name of the input units to the filter. Should be all lowercase and separated with an underscore, use 'per' if units are divided and '-' if units are multiplied.",
            examples="count",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units_out: Annotated[
        str,
        Field(
            default="",
            description="Name of the output units.  Should be all lowercase and separated with an underscore, use 'per' if units are divided and '-' if units are multiplied.",
            examples="millivolt",
            type="string",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    calibration_date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Most recent date of filter calibration in ISO format of YYY-MM-DD.",
            examples="2020-01-01",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    gain: Annotated[
        float,
        Field(
            default=1.0,
            description="scalar gain of the filter across all frequencies, producted with any frequency depenendent terms",
            examples="1.0",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("calibration_date", mode="before")
    @classmethod
    def validate_calibration_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
