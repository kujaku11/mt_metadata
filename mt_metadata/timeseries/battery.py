# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment, StartEndRange


# =====================================================
class Battery(MetadataBase):
    type: Annotated[
        str | None,
        Field(
            default=None,
            description="Description of battery type.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "pb-acid gel cell",
                "type": "string",
            },
        ),
    ] = None

    id: Annotated[
        str | None,
        Field(
            default=None,
            description="battery id",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "battery01",
                "type": "string",
            },
        ),
    ] = None

    voltage: Annotated[
        StartEndRange,
        Field(
            default=StartEndRange(),
            description="Range of voltages.",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
                "examples": "Range(minimum=0.0, maximum=1.0)",
                "type": "object",
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments about the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "ambient air temperature was chilly, ice on cables",
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
