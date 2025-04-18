# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field, HttpUrl, EmailStr


# =====================================================
class FundingSource(MetadataBase):
    name: Annotated[
        str | None,
        Field(
            default=None,
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
        HttpUrl | None,
        Field(
            default=None,
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
        str | None,
        Field(
            default=None,
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
        list[str] | str | None,
        Field(
            default=None,
            description="Grant ID number or name",
            examples="MT-01-2020",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
