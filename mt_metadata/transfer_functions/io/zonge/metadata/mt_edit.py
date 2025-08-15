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
            examples=["3.10m applied 2021/01/27"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    auto: Annotated[
        Auto,
        Field(
            default_factory=Auto,
            description="Auto metadata",
            examples=[{"param1": "value1", "param2": "value2"}],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    d_plus: Annotated[
        DPlus,
        Field(
            default_factory=DPlus,
            description="DPlus metadata",
            examples=[{"param1": "value1", "param2": "value2"}],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    phase_slope: Annotated[
        PhaseSlope,
        Field(
            default_factory=PhaseSlope,
            description="PhaseSlope metadata",
            examples=[{"param1": "value1", "param2": "value2"}],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
