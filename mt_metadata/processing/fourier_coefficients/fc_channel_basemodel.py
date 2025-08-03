# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.units import get_unit_object


# =====================================================
class FcChannel(MetadataBase):
    component: Annotated[
        str,
        Field(
            default="",
            description="Name of channel",
            examples=["ex"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    frequency_max: Annotated[
        float,
        Field(
            default=0.0,
            description="Highest frequency present in the sprectrogam data.",
            examples=[77.0],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    frequency_min: Annotated[
        float,
        Field(
            default=0.0,
            description="Lowest frequency present in the sprectrogam data.",
            examples=[99.0],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    sample_rate_decimation_level: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of the time series that was Fourier transformed to generate the FC decimation level.",
            examples=[60],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    sample_rate_window_step: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of the windows.",
            examples=[4],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    units: Annotated[
        float,
        Field(
            default="counts",
            description="Units of the channel",
            examples=["millivolts"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
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
