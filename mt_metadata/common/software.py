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
class Software(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default="",
            description="Author of the software",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Neo"],
            },
        ),
    ]

    version: Annotated[
        str,
        Field(
            default="",
            description="Software version",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["12.01a"],
            },
        ),
    ]

    last_updated: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Most recent date the software was updated.  Prefer to use version, but this works for non-versioned software.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["2020-01-01"],
            },
        ),
    ]

    name: Annotated[
        str,
        Field(
            default="",
            description="Software name",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["mtrules"],
            },
        ),
    ]

    @field_validator("last_updated", mode="before")
    @classmethod
    def validate_last_updated(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
