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
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["24"],
            },
        ),
    ]

    length: Annotated[
        float,
        Field(
            default=0.0,
            description="Generic dipole length",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["100"],
            },
        ),
    ]

    h_p_r: Annotated[
        list[float],
        Field(
            default=[],
            description="Horizontal, pitch, roll of array",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0, 0, 180"],
            },
        ),
    ]

    cmp: Annotated[
        CmpEnum,
        Field(
            default="",
            description="processed component of impedance or tipper",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["zxx"],
            },
        ),
    ]

    center: Annotated[
        str | None,
        Field(
            default=None,
            description="center of the sounding location",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["335754.685:4263553.435:1650.2 m"],
            },
        ),
    ]

    x_y_z1: Annotated[
        str | None,
        Field(
            default=None,
            description="xyz of local station",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["335754.685:4263553.435:1650.2"],
            },
        ),
    ]

    x_y_z2: Annotated[
        str | None,
        Field(
            default=None,
            description="xyz of remote station",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["335754.685:4263553.435:1650.2"],
            },
        ),
    ]

    u_t_m1: Annotated[
        str | None,
        Field(
            default=None,
            description="UTM location of local station",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["335754.685:4263553.435:1650.2"],
            },
        ),
    ]

    a_space: Annotated[
        str | None,
        Field(
            default=None,
            description="spacing of lines",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["100 m"],
            },
        ),
    ]

    s_space: Annotated[
        str | None,
        Field(
            default=None,
            description="spacing of stations along the line",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["100"],
            },
        ),
    ]
