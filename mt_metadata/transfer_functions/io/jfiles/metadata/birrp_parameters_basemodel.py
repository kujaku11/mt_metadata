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
            examples="2",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    inputs: Annotated[
        int,
        Field(
            default=None,
            description="Number of input channels",
            examples="2",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    references: Annotated[
        int,
        Field(
            default=None,
            description="Number of reference channels",
            examples="2",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    tbw: Annotated[
        float,
        Field(
            default=0.0,
            description="total bandwidth of window",
            examples="2.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    deltat: Annotated[
        float,
        Field(
            default=0.0,
            description="sampling spacing, if negative sample rate.",
            examples="1.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nfft: Annotated[
        float,
        Field(
            default=0.0,
            description="length of time window.",
            examples="8192",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nsctinc: Annotated[
        float,
        Field(
            default=0.0,
            description="number by which the segment length is divided by to get next window.",
            examples="2.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nsctmax: Annotated[
        float,
        Field(
            default=0.0,
            description="maximum number of sections",
            examples="2.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nf1: Annotated[
        int,
        Field(
            default=None,
            description="index of first frequency",
            examples="4",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nfinc: Annotated[
        int,
        Field(
            default=None,
            description="increment value of next frequency",
            examples="2",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nfsect: Annotated[
        int,
        Field(
            default=None,
            description="total number of frequencies to process.",
            examples="4",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    uin: Annotated[
        float,
        Field(
            default=0.0,
            description="small leverage point minimum",
            examples="0.00",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ainlin: Annotated[
        float,
        Field(
            default=0.0,
            description="bounded influence value",
            examples="-999",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ainuin: Annotated[
        float,
        Field(
            default=0.0,
            description="large leverage point minimu",
            examples="0.99",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    c2threshe: Annotated[
        float,
        Field(
            default=0.0,
            description="coherencey threshold for electric channels",
            examples="0.35",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nz: Annotated[
        int,
        Field(
            default=None,
            description="Use threshold for hz channels",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    c2threshe1: Annotated[
        float,
        Field(
            default=0.0,
            description="coherencey threshold for hz channels",
            examples="0.35",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    npcs: Annotated[
        int,
        Field(
            default=None,
            description="number of data segments used",
            examples="2",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nar: Annotated[
        int,
        Field(
            default=None,
            description="order of auto-regressive prewhitening filter.",
            examples="5",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    imode: Annotated[
        int,
        Field(
            default=None,
            description="input data file mode",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    jmode: Annotated[
        int,
        Field(
            default=None,
            description="input time mode",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ncomp: Annotated[
        int,
        Field(
            default=None,
            description="number of components",
            examples="5",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
