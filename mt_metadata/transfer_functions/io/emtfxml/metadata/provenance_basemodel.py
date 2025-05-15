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
class Provenance(MetadataBase):
    create_time: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="date and time the file was created",
            examples="2020-02-08T12:23:40.324600+00:00",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    creating_application: Annotated[
        str,
        Field(
            default="mt_metadata",
            description="name of the application that created the XML file",
            examples="EMTF File Conversion Utilities 4.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("create_time", mode="before")
    @classmethod
    def validate_create_time(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
