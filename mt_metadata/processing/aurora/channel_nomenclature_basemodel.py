# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class ExEnum(str, Enum):
    ex = "ex"
    e1 = "e1"
    e2 = "e2"
    e3 = "e3"
    e4 = "e4"


class EyEnum(str, Enum):
    ey = "ey"
    e1 = "e1"
    e2 = "e2"
    e3 = "e3"
    e4 = "e4"


class HxEnum(str, Enum):
    bx = "bx"
    hx = "hx"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"


class HyEnum(str, Enum):
    by = "by"
    hy = "hy"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"


class HzEnum(str, Enum):
    bz = "bz"
    hz = "hz"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"


class ChannelNomenclature(MetadataBase):
    ex: Annotated[
        ExEnum,
        Field(
            default="ex",
            description="label for the X electric field channel, X is assumed to be North",
            examples=["ex"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ey: Annotated[
        EyEnum,
        Field(
            default="ey",
            description="label for the Y electric field channel, Y is assumed to be East",
            examples=["ey"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hx: Annotated[
        HxEnum,
        Field(
            default="hx",
            description="label for the X magnetic field channel, X is assumed to be North",
            examples=["hx"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hy: Annotated[
        HyEnum,
        Field(
            default="hy",
            description="label for the Y magnetic field channel, Y is assumed to be East",
            examples=["hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hz: Annotated[
        HzEnum,
        Field(
            default="hz",
            description="label for the Z magnetic field channel, Z is assumed to be vertical Down",
            examples=["hz"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
