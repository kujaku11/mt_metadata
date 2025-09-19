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
            examples=["6545BAC6,BE380864"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    gdp_box: Annotated[
        str | None,
        Field(
            default=None,
            description="Box number for local and remote stations",
            examples=["18,15"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    stn: Annotated[
        str | None,
        Field(
            default=None,
            description="station number of local and remote",
            examples=["1,2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    number: Annotated[
        str | None,
        Field(
            default=None,
            description="channel number for local and coil number of remote",
            examples=["1, 2284"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    cmp: Annotated[
        str | None,
        Field(
            default=None,
            description="component of local and remote stations",
            examples=["ex,hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    c_res: Annotated[
        str | None,
        Field(
            default=None,
            description="contact resistance for local and remote sensors",
            examples=["0,0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    azimuth: Annotated[
        str | None,
        Field(
            default=None,
            description="azimuth for local and remote sensors",
            examples=["12.1,12.1"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    incl: Annotated[
        str | None,
        Field(
            default=None,
            description="Inclination ",
            examples=["335754.685:4263553.435:1650.2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
