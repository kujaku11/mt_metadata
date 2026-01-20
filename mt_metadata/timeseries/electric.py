# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, PrivateAttr

from mt_metadata.common import StartEndRange
from mt_metadata.timeseries import ChannelBase, Electrode


# =====================================================
class Electric(ChannelBase):
    _channel_type: str = PrivateAttr("electric")

    component: Annotated[
        str,
        Field(
            default="e_default",
            description="Component of the electric field.",
            alias=None,
            pattern=r"^[eE][a-zA-Z0-9_]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Ex"],
            },
        ),
    ]

    dipole_length: Annotated[
        float,
        Field(
            default=0.0,
            description="Length of the dipole as measured in a straight line from electrode to electrode.",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["55.25"],
            },
        ),
    ]

    positive: Annotated[
        Electrode,
        Field(
            default_factory=Electrode,
            description="Positive electrode.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Electrode()"],
            },
        ),
    ]

    negative: Annotated[
        Electrode,
        Field(
            default_factory=Electrode,
            description="Negative electrode.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Electrode()"],
            },
        ),
    ]

    contact_resistance: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="Contact resistance start and end values.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["StartEndRange()"],
            },
        ),
    ]

    ac: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="AC start and end values.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["StartEndRange()"],
            },
        ),
    ]

    dc: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="DC start and end values.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["StartEndRange()"],
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="electric",
            description="Data type for the channel, should be a descriptive word that a user can understand.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["electric"],
            },
        ),
    ]
