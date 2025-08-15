# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class CmpEnum(str, Enum):
    zxx = "zxx"
    zyy = "zyy"
    zyx = "zyx"
    zxy = "zxy"
    txy = "txy"
    tyx = "tyx"
    null = ""


class Rx(MetadataBase):
    gdp_stn: Annotated[
        str,
        Field(
            default="",
            description="Station name",
            examples=["24"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    length: Annotated[
        float,
        Field(
            default=0.0,
            description="Generic dipole length",
            examples=["100"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    h_p_r: Annotated[
        list[float],
        Field(
            default=[],
            description="Horizontal, pitch, roll of array",
            examples=["0, 0, 180"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    cmp: Annotated[
        CmpEnum,
        Field(
            default="",
            description="processed component of impedance or tipper",
            examples=["zxx"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    center: Annotated[
        str | None,
        Field(
            default=None,
            description="center of the sounding location",
            examples=["335754.685:4263553.435:1650.2 m"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    x_y_z1: Annotated[
        str | None,
        Field(
            default=None,
            description="xyz of local station",
            examples=["335754.685:4263553.435:1650.2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    x_y_z2: Annotated[
        str | None,
        Field(
            default=None,
            description="xyz of remote station",
            examples=["335754.685:4263553.435:1650.2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    u_t_m1: Annotated[
        str | None,
        Field(
            default=None,
            description="UTM location of local station",
            examples=["335754.685:4263553.435:1650.2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    a_space: Annotated[
        str | None,
        Field(
            default=None,
            description="spacing of lines",
            examples=["100 m"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    s_space: Annotated[
        str | None,
        Field(
            default=None,
            description="spacing of stations along the line",
            examples=["100"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
