# =====================================================
# Imports
# =====================================================
from typing import Annotated, Any

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from pydantic import Field, field_validator, ValidationInfo


# =====================================================
class TimingSystem(MetadataBase):
    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comment on the timing system.",
            examples="GPS locked with internal quartz clock",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    drift: Annotated[
        float,
        Field(
            default=0.0,
            description="Estimated drift of the timing system.",
            examples="0.001",
            alias=None,
            json_schema_extra={
                "units": "seconds",
                "required": True,
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="GPS",
            description="Type of timing system.",
            examples="GPS",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    uncertainty: Annotated[
        float,
        Field(
            default=0.0,
            description="Estimated uncertainty of the timing system.",
            examples="0.0002",
            alias=None,
            json_schema_extra={
                "units": "seconds",
                "required": True,
            },
        ),
    ]

    n_satellites: Annotated[
        int | None,
        Field(
            default=None,
            description="Number of satellites used for timing.",
            examples="6",
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
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value
