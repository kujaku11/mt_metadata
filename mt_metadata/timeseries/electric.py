# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.common import StartEndRange
from mt_metadata.timeseries import Channel, Electrode


# =====================================================
class Electric(Channel):

    component: Annotated[
        str,
        Field(
            default="",
            description="Component of the electric field.",
            examples="Ex",
            alias=None,
            pattern=r"^[eE][a-zA-Z]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    dipole_length: Annotated[
        float,
        Field(
            default=0.0,
            description="Length of the dipole as measured in a straight line from electrode to electrode.",
            examples="55.25",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    positive: Annotated[
        Electrode,
        Field(
            default_factory=Electrode,
            description="Positive electrode.",
            examples="Electrode()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    negative: Annotated[
        Electrode,
        Field(
            default_factory=Electrode,
            description="Negative electrode.",
            examples="Electrode()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    contact_resistance: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="Contact resistance start and end values.",
            examples="StartEndRange()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ac: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="AC start and end values.",
            examples="StartEndRange()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    dc: Annotated[
        StartEndRange,
        Field(
            default_factory=StartEndRange,
            description="DC start and end values.",
            examples="StartEndRange()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
