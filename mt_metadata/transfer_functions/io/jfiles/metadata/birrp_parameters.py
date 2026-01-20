# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class BirrpParameters(MetadataBase):
    outputs: Annotated[
        int,
        Field(
            default=None,
            description="Number of output channels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    inputs: Annotated[
        int,
        Field(
            default=None,
            description="Number of input channels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    references: Annotated[
        int,
        Field(
            default=None,
            description="Number of reference channels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    tbw: Annotated[
        float,
        Field(
            default=0.0,
            description="total bandwidth of window",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2.0"],
            },
        ),
    ]

    deltat: Annotated[
        float,
        Field(
            default=0.0,
            description="sampling spacing, if negative sample rate.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["1.0"],
            },
        ),
    ]

    nfft: Annotated[
        float,
        Field(
            default=0.0,
            description="length of time window.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["8192"],
            },
        ),
    ]

    nsctinc: Annotated[
        float,
        Field(
            default=0.0,
            description="number by which the segment length is divided by to get next window.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2.0"],
            },
        ),
    ]

    nsctmax: Annotated[
        float,
        Field(
            default=0.0,
            description="maximum number of sections",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2.0"],
            },
        ),
    ]

    nf1: Annotated[
        int,
        Field(
            default=None,
            description="index of first frequency",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["4"],
            },
        ),
    ]

    nfinc: Annotated[
        int,
        Field(
            default=None,
            description="increment value of next frequency",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    nfsect: Annotated[
        int,
        Field(
            default=None,
            description="total number of frequencies to process.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["4"],
            },
        ),
    ]

    uin: Annotated[
        float,
        Field(
            default=0.0,
            description="small leverage point minimum",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.00"],
            },
        ),
    ]

    ainlin: Annotated[
        float,
        Field(
            default=0.0,
            description="bounded influence value",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["-999"],
            },
        ),
    ]

    ainuin: Annotated[
        float,
        Field(
            default=0.0,
            description="large leverage point minimu",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.99"],
            },
        ),
    ]

    c2threshe: Annotated[
        float,
        Field(
            default=0.0,
            description="coherencey threshold for electric channels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.35"],
            },
        ),
    ]

    nz: Annotated[
        int,
        Field(
            default=None,
            description="Use threshold for hz channels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0"],
            },
        ),
    ]

    c2threshe1: Annotated[
        float,
        Field(
            default=0.0,
            description="coherencey threshold for hz channels",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.35"],
            },
        ),
    ]

    npcs: Annotated[
        int,
        Field(
            default=None,
            description="number of data segments used",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    nar: Annotated[
        int,
        Field(
            default=None,
            description="order of auto-regressive prewhitening filter.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["5"],
            },
        ),
    ]

    imode: Annotated[
        int,
        Field(
            default=None,
            description="input data file mode",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0"],
            },
        ),
    ]

    jmode: Annotated[
        int,
        Field(
            default=None,
            description="input time mode",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0"],
            },
        ),
    ]

    ncomp: Annotated[
        int,
        Field(
            default=None,
            description="number of components",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["5"],
            },
        ),
    ]
