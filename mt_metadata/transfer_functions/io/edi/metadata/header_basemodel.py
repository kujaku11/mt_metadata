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
class CoordinateSystemEnum(str, Enum):
    geographic = "geographic"
    geomagnetic = "geomagnetic"
    station = "station"


class StdversEnum(str, Enum):
    SEG_1 = "SEG 1.0"
    base = "1.0"
    SEG_11 = "SEG 1.01"


class Header(MetadataBase):
    acqby: Annotated[
        str | None,
        Field(
            default=None,
            description="person, group, company, university that collected the data",
            examples="mt experts",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    acqdate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Start date the time series data were collected",
            examples="2020-01-01",
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
            default="geographic",
            description="coordinate system the transfer function is currently in. Its preferred the transfer function be in a geographic coordinate system for archiving and sharing.",
            examples="geopgraphic",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    country: Annotated[
        str | None,
        Field(
            default=None,
            description="Country name where data were collected.",
            examples="USA",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    county: Annotated[
        str | None,
        Field(
            default=None,
            description="County name where data were collected.",
            examples="Douglas",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    dataid: Annotated[
        str,
        Field(
            default="",
            description="station ID.",
            examples="mt001",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    enddate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="End date the time series data were collected",
            examples="2020-01-01",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    empty: Annotated[
        float,
        Field(
            default=1e32,
            description="null data values, usually a large number",
            examples="1E+32",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    fileby: Annotated[
        str,
        Field(
            default="",
            description="person, group, company, university that made the file",
            examples="mt experts",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    filedate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date the file was made",
            examples="2020-01-01",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    progdate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date of the most recent update of the program used to make the file",
            examples="2020-01-01",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    progname: Annotated[
        str,
        Field(
            default="mt_metadata",
            description="Name of the program used to make the file.",
            examples="mt_metadata",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    progvers: Annotated[
        str,
        Field(
            default="0.1.6",
            description="Version of the program used to make the file.",
            examples="0.1.6",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    project: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the project the data was collected for, usually a short description or acronym of the project name.",
            examples="iMUSH",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    prospect: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the prospect the data was collected for, usually a short description of the location",
            examples="Benton",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    loc: Annotated[
        str | None,
        Field(
            default=None,
            description="Usually a short description of the location",
            examples="Benton, CA",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    state: Annotated[
        str | None,
        Field(
            default=None,
            description="State where the data were collected.",
            examples="CA",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    stdvers: Annotated[
        StdversEnum,
        Field(
            default="SEG 1.0",
            description="EDI standards version SEG 1.0",
            examples="SEG 1.0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    survey: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the survey",
            examples="CONUS",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    units: Annotated[
        str | None,
        Field(
            default="millivolts_per_kilometer_per_nanotesla",
            description="In the EDI standards this is the elevation units, in newer versions this should be units of the transfer function.",
            examples="millivolts_per_kilometer_per_nanotesla",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("acqdate", mode="before")
    @classmethod
    def validate_acqdate(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("enddate", mode="before")
    @classmethod
    def validate_enddate(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("filedate", mode="before")
    @classmethod
    def validate_filedate(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("progdate", mode="before")
    @classmethod
    def validate_progdate(
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
