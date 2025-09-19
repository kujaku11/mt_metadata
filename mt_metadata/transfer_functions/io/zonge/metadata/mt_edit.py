# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase

from . import Auto, DPlus, PhaseSlope


# =====================================================
class MTEdit(MetadataBase):
    version: Annotated[
        str,
        Field(
            default="",
            description="Version of MT Edit and date",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["3.10m applied 2021/01/27"],
            },
        ),
    ]

    auto: Annotated[
        Auto,
        Field(
            default_factory=Auto,
            description="Auto metadata",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [{"param1": "value1", "param2": "value2"}],
            },
        ),
    ]

    d_plus: Annotated[
        DPlus,
        Field(
            default_factory=DPlus,
            description="DPlus metadata",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [{"param1": "value1", "param2": "value2"}],
            },
        ),
    ]

    phase_slope: Annotated[
        PhaseSlope,
        Field(
            default_factory=PhaseSlope,
            description="PhaseSlope metadata",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [{"param1": "value1", "param2": "value2"}],
            },
        ),
    ]
