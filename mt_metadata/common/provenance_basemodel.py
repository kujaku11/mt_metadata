# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime
from pydantic import Field, field_validator


# =====================================================
class Provenance(MetadataBase):
    creation_time: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date and time the file was created.",
            examples="2020-02-08T12:23:40.324600+00:00",
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
            description="Any comments on provenance of the data.",
            examples="all good",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    log: Annotated[
        str | None,
        Field(
            default=None,
            description="A history of changes made to the data.",
            examples="2020-02-10T14:24:45+00:00 updated metadata",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    @field_validator("creation_time", mode="before")
    @classmethod
    def validate_creation_time(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
