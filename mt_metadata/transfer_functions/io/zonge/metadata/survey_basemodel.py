# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class TypeEnum(str, Enum):
    nsamt = "nsamt"
    csamt = "csamt"
    mt = "mt"


class ArrayEnum(str, Enum):
    tensor = "tensor"


class DatumEnum(str, Enum):
    WGS84 = "WGS84"
    NAD27 = "NAD27"
    other = "other"


class ProjEnum(str, Enum):
    UTM = "UTM"
    other = "other"


class Survey(MetadataBase):
    type: Annotated[
        TypeEnum,
        Field(
            default="nsamt",
            description="Type of EM survey",
            examples=["nsamt"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    array: Annotated[
        ArrayEnum,
        Field(
            default="tensor",
            description="Type of array",
            examples=["tensor"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    datum: Annotated[
        DatumEnum,
        Field(
            default="WGS84",
            description="Datum of the location",
            examples=["WGS84"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    u_t_m_zone: Annotated[
        str,
        Field(
            default="",
            description="UTM zone of location",
            examples=["12"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    proj: Annotated[
        ProjEnum,
        Field(
            default="UTM",
            description="Projection of the location coordinates",
            examples=["UTM"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
