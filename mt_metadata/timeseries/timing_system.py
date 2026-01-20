# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment


# =====================================================
class TimingSystem(MetadataBase):
    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comment on the timing system.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "GPS locked with internal quartz clock",
            },
        ),
    ]

    drift: Annotated[
        float,
        Field(
            default=0.0,
            description="Estimated drift of the timing system.",
            alias=None,
            json_schema_extra={
                "units": "seconds",
                "required": True,
                "examples": "0.001",
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="GPS",
            description="Type of timing system.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "GPS",
            },
        ),
    ]

    uncertainty: Annotated[
        float,
        Field(
            default=0.0,
            description="Estimated uncertainty of the timing system.",
            alias=None,
            json_schema_extra={
                "units": "seconds",
                "required": True,
                "examples": "0.0002",
            },
        ),
    ]

    n_satellites: Annotated[
        int | None,
        Field(
            default=None,
            description="Number of satellites used for timing.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "6",
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
