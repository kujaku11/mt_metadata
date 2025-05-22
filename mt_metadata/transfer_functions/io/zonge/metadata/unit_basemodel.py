# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class LengthEnum(str, Enum):
    m = "m"
    ft = "ft"
    km = "km"


class EEnum(str, Enum):
    mV / km = "mV/km"
    uV / m = "uV/m"
    other = "other"


class BEnum(str, Enum):
    nT = "nT"
    uT = "uT"
    other = "other"


class Unit(MetadataBase):
    length: Annotated[
        LengthEnum,
        Field(
            default="m",
            description="Type of smoothing for phase slope algorithm",
            examples=["m"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    e: Annotated[
        EEnum | None,
        Field(
            default=None,
            description="Units for the electric field",
            examples=["mV/km"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    b: Annotated[
        BEnum,
        Field(
            default="nT",
            description="Units for the magnetic field",
            examples=["nT"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
