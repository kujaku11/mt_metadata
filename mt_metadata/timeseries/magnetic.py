# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field
from mt_metadata.common import StartEndRange
from mt_metadata.timeseries import Channel


# =====================================================
class Magnetic(Channel):
    component: Annotated[
        str,
        Field(
            default="",
            description="Component of the electric field.",
            examples="hx",
            alias=None,
            pattern=r"^[hHbB][a-zA-Z]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    h_field_min: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="minimum of field strength at the beginning and end",
            examples="StartEndRange(start=0.01, end=0.02)",
            alias=None,
            json_schema_extra={
                "units": "nanotesla",
                "required": True,
            },
        ),
    ]

    h_field_max: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="maximum of field strength at the beginning and end",
            examples="StartEndRange(start=0.1, end=2.0)",
            alias=None,
            json_schema_extra={
                "units": "nanotesla",
                "required": True,
            },
        ),
    ]
