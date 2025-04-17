# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import EmailStr, Field


# =====================================================
class Person(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Persons name, should be full first and last name.",
            examples="person name",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    author: Annotated[
        str | None,
        Field(
            default=None,
            description="Persons name, should be full first and last name.",
            examples="person name",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    organization: Annotated[
        str | None,
        Field(
            default=None,
            description="Organization full name",
            examples="mt gurus",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    email: Annotated[
        EmailStr | None,
        Field(
            default=None,
            description="Email of the contact person",
            examples="mt.guru@em.org",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    url: Annotated[
        str | None,
        Field(
            default=None,
            description="URL of the contact person",
            examples="em.org",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments about the person",
            examples="expert digger",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
