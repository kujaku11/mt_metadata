# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import SignConventionEnum
from mt_metadata.utils.mttime import MTime


# =====================================================


class ProcessingInfo(MetadataBase):
    sign_convention: Annotated[
        SignConventionEnum,
        Field(
            default="exp(+ i\omega t)",
            description="Sign convention of the processing software output",
            examples=["exp(+ i\\omega t)"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    processed_by: Annotated[
        str | None,
        Field(
            default=None,
            description="Names of people who processed the data",
            examples=["MT Guru"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    process_date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date the data were processed",
            examples=["2020-01-01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    processing_tag: Annotated[
        str | None,
        Field(
            default=None,
            description="List of remote references",
            examples=["mt001-mt002"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("process_date", mode="before")
    @classmethod
    def validate_process_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
