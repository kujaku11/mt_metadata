# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import AnyHttpUrl, EmailStr, Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment


# =====================================================
class FundingSource(MetadataBase):
    name: Annotated[
        list[str] | str | None,
        Field(
            default=None,
            description="Persons name, should be full first and last name.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "person name",
                "items": {"type": "string"},
            },
        ),
    ]

    organization: Annotated[
        list[str] | str | None,
        Field(
            default=None,
            description="Organization full name",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "mt gurus",
                "items": {"type": "string"},
            },
        ),
    ]

    email: Annotated[
        list[EmailStr] | EmailStr | None,
        Field(
            default=None,
            description="Email of the contact person",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "mt.guru@em.org",
                "items": {"type": "string"},
            },
        ),
    ]

    url: Annotated[
        list[AnyHttpUrl] | AnyHttpUrl | None,
        Field(
            default=None,
            description="URL of the contact person",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "em.org",
                "items": {"type": "string"},
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),
            description="Any comments about the person",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "expert digger",
            },
        ),
    ]

    grant_id: Annotated[
        list[str] | str | None,
        Field(
            default=None,
            description="Grant ID number or name",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "MT-01-2020",
                "items": {"type": "string"},
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("name", "organization", "email", "url", "grant_id", mode="before")
    @classmethod
    def validate_input(cls, value) -> list:
        """
        make sure the inputs are lists

        Parameters
        ----------
        value : _type_
            _description_

        Returns
        -------
        list
            _description_
        """

        if isinstance(value, (list, tuple)):
            return list(value)

        elif isinstance(value, (EmailStr, AnyHttpUrl)):
            return [value]

        elif isinstance(value, str):
            return [item.strip() for item in value.split(",")]

        elif value is None:
            return None

        else:
            raise TypeError(f"Cannot form a list from types {type(value)}.")
