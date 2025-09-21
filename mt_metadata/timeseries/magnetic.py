# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, PrivateAttr

from mt_metadata.common import StartEndRange
from mt_metadata.timeseries import Channel


# =====================================================
class Magnetic(Channel):
    _channel_type: str = PrivateAttr("magnetic")
    component: Annotated[
        str,
        Field(
            default="h_default",
            description="Component of the magnetic field.",
            alias=None,
            pattern=r"^[hHbBrR][a-zA-Z1-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hx"],
            },
        ),
    ]

    h_field_min: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="minimum of field strength at the beginning and end",
            alias=None,
            json_schema_extra={
                "units": "nanotesla",
                "required": True,
                "examples": ["StartEndRange(start=0.01, end=0.02)"],
            },
        ),
    ]

    h_field_max: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="maximum of field strength at the beginning and end",
            alias=None,
            json_schema_extra={
                "units": "nanotesla",
                "required": True,
                "examples": ["StartEndRange(start=0.1, end=2.0)"],
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="magnetic",
            description="Data type for the channel, should be a descriptive word that a user can understand.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["magnetic"],
            },
        ),
    ]
