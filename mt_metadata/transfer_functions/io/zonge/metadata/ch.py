# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class CH(MetadataBase):
    a_d_card_s_n: Annotated[
        str | None,
        Field(
            default=None,
            description="serial number of ad card for local and remote stations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["6545BAC6,BE380864"],
            },
        ),
    ]

    gdp_box: Annotated[
        str | None,
        Field(
            default=None,
            description="Box number for local and remote stations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["18,15"],
            },
        ),
    ]

    stn: Annotated[
        str | None,
        Field(
            default=None,
            description="station number of local and remote",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1,2"],
            },
        ),
    ]

    number: Annotated[
        str | None,
        Field(
            default=None,
            description="channel number for local and coil number of remote",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1, 2284"],
            },
        ),
    ]

    cmp: Annotated[
        str | None,
        Field(
            default=None,
            description="component of local and remote stations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["ex,hy"],
            },
        ),
    ]

    c_res: Annotated[
        str | None,
        Field(
            default=None,
            description="contact resistance for local and remote sensors",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["0,0"],
            },
        ),
    ]

    azimuth: Annotated[
        str | None,
        Field(
            default=None,
            description="azimuth for local and remote sensors",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["12.1,12.1"],
            },
        ),
    ]

    incl: Annotated[
        str | None,
        Field(
            default=None,
            description="Inclination ",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["335754.685:4263553.435:1650.2"],
            },
        ),
    ]
