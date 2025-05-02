# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from pydantic import Field, ValidationInfo, field_validator


# =====================================================
class FundingSource(MetadataBase):
    name: Annotated[
        str | None,
        Field(
            default=None,
            items={"type": "string"},
            description="Persons name, should be full first and last name.",
            examples="person name",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    organization: Annotated[
        str | None,
        Field(
            default=None,
            items={"type": "string"},
            description="Organization full name",
            examples="mt gurus",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    email: Annotated[
        str | None,
        Field(
            default=None,
            items={"type": "string"},
            description="Email of the contact person",
            examples="mt.guru@em.org",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    url: Annotated[
        str | None,
        Field(
            default=None,
            items={"type": "string"},
            description="URL of the contact person",
            examples="em.org",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),
            description="Any comments about the person",
            examples="expert digger",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    grant_id: Annotated[
        str | None,
        Field(
            default=None,
            items={"type": "string"},
            description="Grant ID number or name",
            examples="MT-01-2020",
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
