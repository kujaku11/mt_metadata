# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from pydantic import (
    EmailStr,
    Field,
    AnyUrl,
    field_validator,
    ValidationInfo,
    AliasChoices,
)


# =====================================================
class Person(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Persons name, should be full first and last name.",
            examples="person name",
            validation_alias=AliasChoices("name", "author"),
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    organization: Annotated[
        str | None,
        Field(
            default=None,
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
        EmailStr | None,
        Field(
            default=None,
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
        AnyUrl | None,
        Field(
            default=None,
            description="URL of the contact person",
            examples="https://em.org",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment | str,
        Field(
            default_factory=Comment,
            description="Any comments about the person",
            examples="expert digger",
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
