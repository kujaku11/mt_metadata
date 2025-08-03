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
class Comment(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default=None,
            description="Author who made the comment",
            examples=["M. Tee"],
            alias=["nome"],
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date the comment was made",
            examples=["2020-01-21"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    value: Annotated[
        str | None,
        Field(
            default=None,
            description="Comment string",
            examples=["This is a comment"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
