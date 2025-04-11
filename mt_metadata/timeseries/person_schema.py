# =====================================================
# Imports
# =====================================================
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional, List, Dict, Any


# =====================================================
class Person(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True, coerce_numbers_to_str=True, validate_default=True
    )
    name: Annotated[
        str,
        Field(
            default="",
            type="string",
            description="Persons name, should be full first and last name.",
            title="name",
            examples="person name",
            alias=None,
            units=None,
            required=True,
        ),
    ]

    author: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="Persons name, should be full first and last name.",
            title="author",
            examples="person name",
            alias=None,
            units=None,
            required=False,
        ),
    ] = None

    organization: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="Organization full name",
            title="organization",
            examples="mt gurus",
            alias=None,
            units=None,
            required=False,
        ),
    ] = None

    email: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="Email of the contact person",
            title="email",
            examples="mt.guru@em.org",
            alias=None,
            units=None,
            required=False,
        ),
    ] = None

    url: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="URL of the contact person",
            title="url",
            examples="em.org",
            alias=None,
            units=None,
            required=False,
        ),
    ] = None

    comments: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            description="Any comments about the person",
            title="comments",
            examples="expert digger",
            alias=None,
            units=None,
            required=False,
        ),
    ] = None
