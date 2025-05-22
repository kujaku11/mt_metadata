# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment


# =====================================================
class LocationEnum(str, Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    other = "other"


class Electrode(MetadataBase):
    location: Annotated[
        LocationEnum,
        Field(
            default="",
            description="Direction of electrode",
            examples=["N"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    number: Annotated[
        str,
        Field(
            default="0",
            description="Electrode ID number",
            examples=["1a"],
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
            default_factory=lambda: Comment(),
            description="comments on the electrode",
            examples=["Ag-AgCl porous pot"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value
