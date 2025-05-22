# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime
from mt_metadata.utils.units import get_unit_object


# =====================================================
class SignConventionEnum(str, Enum):
    plus = "+"
    minus = "-"
    other = "other"


class UnitsEnum(str, Enum):
    millivolts_per_kilometer_per_nanotesla = "millivolts_per_kilometer_per_nanotesla"
    ohms = "ohms"
    other = "other"


class CoordinateSystemEnum(str, Enum):
    geographic = "geographic"
    geomagnetic = "geomagnetic"
    other = "other"


class TransferFunction(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="transfer function id",
            examples=["mt01_256"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sign_convention: Annotated[
        SignConventionEnum,
        Field(
            default="+",
            description="sign of the transfer function estimates",
            examples=["+"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units: Annotated[
        UnitsEnum,
        Field(
            default="",
            description="units of the impedance tensor estimates",
            examples=["millivolts_per_kilometer_per_nanotesla"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    runs_processed: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of runs used in the processing",
            examples=["[ MT001a MT001c]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    remote_references: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of remote references",
            examples=["[ MT002b MT002c ]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    processed_date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="date the data were processed",
            examples=["2020-01-01T12:00:00"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    processing_parameters: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of processing parameters with structure name = value",
            examples=["[nfft=4096, n_windows=16]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    processing_type: Annotated[
        str,
        Field(
            default="",
            description="Type of processing",
            examples=["robust remote reference"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    coordinate_system: Annotated[
        CoordinateSystemEnum,
        Field(
            default="geopgraphic",
            description="coordinate system that the transfer function is in.  It is strongly recommended that the transfer functions be rotated to align with geographic coordinates with geographic north as 0 and east as 90.",
            examples=["geographic"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("processed_date", mode="before")
    @classmethod
    def validate_processed_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str) -> str:
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)
