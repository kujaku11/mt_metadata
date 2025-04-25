# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    Fdsn,
    TimePeriod,
    Person,
    Provenance,
)

from mt_metadata.timeseries.data_logger_basemodel import DataLogger
from mt_metadata.utils.list_dict import ListDict
from pydantic import Field, field_validator, ValidationInfo


# =====================================================
class DataTypeEnum(str, Enum):
    RMT = "RMT"
    AMT = "AMT"
    BBMT = "BBMT"
    LPMT = "LPMT"
    ULPMT = "ULPMT"
    other = "other"


class Run(MetadataBase):
    channels_recorded_auxiliary: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of auxiliary channels recorded",
            examples="[T]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_recorded_electric: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of electric channels recorded",
            examples="[Ex , Ey]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_recorded_magnetic: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of magnetic channels recorded",
            examples='"[Hx , Hy , Hz]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments on the run.",
            examples="cows chewed cables",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data_type: Annotated[
        DataTypeEnum,
        Field(
            default="BBMT",
            description="Type of data recorded for this run.",
            examples="BBMT",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Run ID should be station name followed by a number or character.  Characters should only be used if the run number is small, if the run number is high consider using digits with zeros.  For example if you have 100 runs the run ID could be 001 or {station}001.",
            examples="001",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate for the run",
            examples="100",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    acquired_by: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Information about the group that collected the data.",
            examples="Person()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    metadata_by: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Information about the group that collected the metadata.",
            examples="Person()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    provenance: Annotated[
        Provenance,
        Field(
            default_factory=Provenance,
            description="Provenance information about the run.",
            examples="Provenance()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,
            description="Time period for the run.",
            examples="TimePeriod(start='2020-01-01', end='2020-12-31')",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data_logger: Annotated[
        DataLogger,
        Field(
            default_factory=DataLogger,
            description="Data Logger information used to collect the run.",
            examples="DataLogger()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    fdsn: Annotated[
        Fdsn,
        Field(
            default_factory=Fdsn,
            description="FDSN information for the run.",
            examples="Fdsn()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    channels: Annotated[
        ListDict,
        Field(
            default_factory=ListDict,
            description="ListDict of channel objects collected in this run.",
            examples="ListDict()",
            alias=None,
            exclude=True,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value
