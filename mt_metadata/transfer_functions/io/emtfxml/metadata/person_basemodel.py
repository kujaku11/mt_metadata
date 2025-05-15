# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import EmailStr, Field, HttpUrl

from mt_metadata.base import MetadataBase


# =====================================================
class Person(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="author name",
            examples="person name",
            alias=["author"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(
            default="",
            description="email of the contact person",
            examples="mt.guru@em.org",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    org: Annotated[
        str,
        Field(
            default="",
            description="organization name",
            examples="mt gurus",
            alias=["organization"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    org_url: Annotated[
        HttpUrl | None,
        Field(
            default=None,
            description="URL of organization",
            examples="https://www.mt_gurus.org",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
