# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import TimePeriod
from mt_metadata.common.units import get_unit_object


# =====================================================
class FCChannel(MetadataBase):
    component: Annotated[
        str,
        Field(
            default="",
            description="Name of channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ex"],
            },
        ),
    ]

    frequency_max: Annotated[
        float,
        Field(
            default=0.0,
            description="Highest frequency present in the sprectrogam data.",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": [77.0],
            },
        ),
    ]

    frequency_min: Annotated[
        float,
        Field(
            default=0.0,
            description="Lowest frequency present in the sprectrogam data.",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": [99.0],
            },
        ),
    ]

    sample_rate_decimation_level: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of the time series that was Fourier transformed to generate the FC decimation level.",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": [60],
            },
        ),
    ]

    sample_rate_window_step: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of the windows.",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": [4],
            },
        ),
    ]

    units: Annotated[
        str,
        Field(
            default="counts",
            description="Units of the channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["millivolts"],
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,  # type: ignore
            description="Time period of the channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [TimePeriod(start="2020-01-01", end="2020-01-02")],
            },
        ),
    ]

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
