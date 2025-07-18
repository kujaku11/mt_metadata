# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from pydantic import Field, field_validator, ValidationInfo


# =====================================================
class FeatureFcRun(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Suggested Run ID should be sample rate followed by a number or character.  Characters should only be used if the run number is small, if the run number is high consider using digits with zeros.  For example if you have 100 runs the run ID could be 001 or sr{sample_rate}_001. Should be the same as the time series run ID.",
            examples=["001"],
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
            examples=["100"],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),
            description="Any comments about the feature",
            examples=["estimated using hilburt transform."],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value
