# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Person(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            type="string",
            description="Persons name, should be full first and last name.",
            examples="person name",
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
            type="string",
            description="Persons name, should be full first and last name.",
            examples="person name",
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
            type="string",
            description="Organization full name",
            examples="mt gurus",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    email: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="Email of the contact person",
            examples="mt.guru@em.org",
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
            type="string",
            description="URL of the contact person",
            examples="em.org",
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
            type="string",
            description="Any comments about the person",
            examples="expert digger",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
