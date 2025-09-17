# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, model_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class MethodEnum(StrEnumerationBase):
    default = "default"
    other = "other"


class TimeSeriesDecimation(MetadataBase):
    level: Annotated[
        int | None,
        Field(
            default=None,
            description="Decimation level, must be a non-negative integer starting at 0",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0"],
            },
        ),
    ]

    factor: Annotated[
        float,
        Field(
            default=1.0,
            description="Decimation factor between parent sample rate and decimated time series sample rate.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["4.0"],
            },
        ),
    ]

    method: Annotated[
        MethodEnum,
        Field(
            default="default",
            description="Type of decimation",
            alias=None,
            json_schema_extra={
                "units": "",
                "required": True,
                "examples": ["default"],
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of the decimation level data (after decimation).",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": ["256"],
            },
        ),
    ]

    anti_alias_filter: Annotated[
        str | None,
        Field(
            default="default",
            description="Type of anti alias filter for decimation.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["default"],
            },
        ),
    ]

    @model_validator(mode="before")
    @classmethod
    def check_level(cls, values):
        """Check that level is a non-negative integer and set anti_alias_filter for level 0."""
        # Handle both dict and model instances
        if isinstance(values, dict):
            level = values.get("level")
        else:
            level = getattr(values, "level", None)

        # Only perform validation if level is an integer or None
        if level is not None and isinstance(level, int) and level < 0:
            raise ValueError("Decimation level must be a non-negative integer.")
        elif level == 0:
            # Set anti_alias_filter to None for level 0
            if isinstance(values, dict):
                values["anti_alias_filter"] = None
            else:
                values.anti_alias_filter = None

        return values
