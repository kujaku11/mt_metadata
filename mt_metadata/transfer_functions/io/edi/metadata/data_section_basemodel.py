# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class DataSection(MetadataBase):
    nfreq: Annotated[
        int | None,
        Field(
            default=None,
            description="Number of frequencies",
            examples="16",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    sectid: Annotated[
        str,
        Field(
            default="",
            description="ID of the station that the data is from. This is important if you have more than one station per file.",
            examples="mt001",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nchan: Annotated[
        int,
        Field(
            default=None,
            description="Number of channels in the transfer function",
            examples="7",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxblocks: Annotated[
        int,
        Field(
            default=None,
            description="Maximum number of data blocks",
            examples="999",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ex: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for EX",
            examples="1",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ey: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for EY",
            examples="2",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hx: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for HX",
            examples="3",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hy: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for HY",
            examples="4",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hz: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for HZ",
            examples="5",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    rrhx: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for RRHX",
            examples="6",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    rrhy: Annotated[
        str,
        Field(
            default="0",
            description="Measurement ID for RRHY",
            examples="7",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
