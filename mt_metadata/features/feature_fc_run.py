# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment, TimePeriod


# =====================================================
class FeatureFCRun(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Suggested Run ID should be sample rate followed by a number or character.  Characters should only be used if the run number is small, if the run number is high consider using digits with zeros.  For example if you have 100 runs the run ID could be 001 or sr{sample_rate}_001. Should be the same as the time series run ID.",
            alias=None,
            pattern="^[a-zA-Z0-9_]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["001"],
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate for the run",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": ["100"],
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),  # type: ignore
            description="Any comments about the feature",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["estimated using hilburt transform."],
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=lambda: TimePeriod(),  # type: ignore
            description="The time period over which the feature was calculated.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2020-01-01T00:00:00"],
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value
