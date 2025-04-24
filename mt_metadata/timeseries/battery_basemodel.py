# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import StartEndRange, Comment
from pydantic import Field, field_validator, ValidationInfo


# =====================================================
class Battery(MetadataBase):
    type: Annotated[
        str | None,
        Field(
            default=None,
            description="Description of battery type.",
            examples="pb-acid gel cell",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    id: Annotated[
        str | None,
        Field(
            default=None,
            description="battery id",
            examples="battery01",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    voltage: Annotated[
        StartEndRange,
        Field(
            default=StartEndRange(),
            description="Range of voltages.",
            examples="Range(minimum=0.0, maximum=1.0)",
            type="object",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments about the channel.",
            examples="ambient air temperature was chilly, ice on cables",
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
