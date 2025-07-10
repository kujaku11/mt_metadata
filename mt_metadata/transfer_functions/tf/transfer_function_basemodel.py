# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    DataQuality,
    GeographicReferenceFrameEnum,
    Person,
    SignConventionEnum,
    Software,
)
from mt_metadata.utils.mttime import MTime
from mt_metadata.utils.units import get_unit_object


# =====================================================


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
        str,
        Field(
            default="milliVolt per kilometer per nanoTesla",
            description="units of the impedance tensor estimates",
            examples=["milliVolt per kilometer per nanoTesla"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    runs_processed: Annotated[
        list[str],
        Field(
            default=list,
            description="list of runs used in the processing",
            examples=[["MT001a", "MT001c"]],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    remote_references: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of remote references",
            examples=[["MT002b", "MT002c"]],
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
        list[str],
        Field(
            default_factory=list,
            description="list of processing parameters with structure name = value",
            examples=[["nfft=4096", "n_windows=16"]],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    processed_by: Annotated[
        Person,
        Field(
            default_factory=Person,  # type: ignore
            description="person who processed the data",
            examples=["Person(name='John Doe', email='john.doe@example.com')"],
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

    software: Annotated[
        Software,
        Field(
            default_factory=Software,
            description="software used to process the data",
            examples=["Software(name='Aurora', version='1.0.0')"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    data_quality: Annotated[
        DataQuality,
        Field(
            default_factory=DataQuality,
            description="data quality information",
            examples=["DataQuality()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    coordinate_system: Annotated[
        GeographicReferenceFrameEnum,
        Field(
            default="geographic",
            description="coordinate system that the transfer function is in.  It is strongly recommended that the transfer functions be rotated to align with geographic coordinates with geographic north as 0 and east as 90.",
            examples=["geographic"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    # this will evenutally be config objects for the various processing programs
    # e.g. aurora, razorback, resistics, etc.
    # for now it is just a string
    processing_config: Annotated[
        str | None,
        Field(
            default=None,
            description="processing configuration",
            examples=["aurora.processing"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("processed_date", mode="before")
    @classmethod
    def validate_processed_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        if isinstance(field_value, MTime):
            return field_value
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
