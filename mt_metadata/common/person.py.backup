# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import (
    AliasChoices,
    AnyUrl,
    EmailStr,
    Field,
    field_validator,
    ValidationInfo,
)

from mt_metadata import NULL_VALUES
from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment


# =====================================================
class GenericPerson(MetadataBase):
    organization: Annotated[
        str | None,
        Field(
            default=None,
            description="Organization full name",
            examples=["mt gurus"],
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
            examples=["mt.guru@em.org"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    url: Annotated[
        AnyUrl | None | str,
        Field(
            default=None,
            description="URL of the contact person",
            examples=["https://em.org"],
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
            default_factory=Comment,  # type: ignore[return-value]
            description="Any comments about the person",
            examples=["expert digger"],
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
            return Comment(value=value)  # type: ignore[return-value]
        return value

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value, info: ValidationInfo) -> AnyUrl | None:
        """
        Validate that the value is a valid URL.
        """
        if isinstance(value, str):
            if value in NULL_VALUES:
                return None
            return AnyUrl(value)
        elif isinstance(value, AnyUrl):
            return value
        elif value is None:
            return None


class Person(GenericPerson):
    name: Annotated[
        str | None,
        Field(
            default="",
            description="Persons name, should be full first and last name.",
            examples=["person name"],
            validation_alias=AliasChoices("name", "author"),
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]


## Its too complicated to have an alias for name, because there is no getter for author
## and with serialization it becomes complicates, easiest solution is to make a different
## object with a field for author instead of name.


class AuthorPerson(GenericPerson):
    author: Annotated[
        str | None,
        Field(
            default="",
            description="Persons name, should be full first and last name.",
            examples=["person name"],
            validation_alias=AliasChoices("author", "name"),
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
