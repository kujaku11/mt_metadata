# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class BirrpBlock(MetadataBase):
    filnam: Annotated[
        str,
        Field(
            default="",
            description="File name of data block",
            examples="hx.dat",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nskip: Annotated[
        int,
        Field(
            default=None,
            description="number of points to skip",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nread: Annotated[
        int,
        Field(
            default=None,
            description="number of points to read",
            examples="10000",
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
            items={"type": "integer"},
            description="number of components in file",
            examples="4",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    indices: Annotated[
        int,
        Field(
            default=None,
            items={"type": "integer"},
            description="index values to use",
            examples="[1, 2]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
