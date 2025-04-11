from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional, List, Dict, Any


class Person(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True, extras="allow", coerce_numbers_to_str=True
    )
    name: Annotated[
        str,
        Field(
            default=None,
            type="string",
            description="Persons name, should be full first and last name.",
            title="name",
            examples="person name",
            alias=None,
            units=None,
        ),
    ]

    author: Annotated[
        Optional[str],
        Field(
            default=None,
            type="string",
            description="Persons name, should be full first and last name.",
            title="author",
            examples="person name",
            alias=None,
            units=None,
        ),
    ]

    organization: Annotated[
        Optional[str],
        Field(
            default=None,
            type="string",
            description="Organization full name",
            title="organization",
            examples="mt gurus",
            alias=None,
            units=None,
        ),
    ]

    email: Annotated[
        Optional[str],
        Field(
            default=None,
            type="string",
            description="Email of the contact person",
            title="email",
            examples="mt.guru@em.org",
            alias=None,
            units=None,
        ),
    ]

    url: Annotated[
        Optional[str],
        Field(
            default=None,
            type="string",
            description="URL of the contact person",
            title="url",
            examples="em.org",
            alias=None,
            units=None,
        ),
    ]

    comments: Annotated[
        Optional[str],
        Field(
            default=None,
            type="string",
            description="Any comments about the person",
            title="comments",
            examples="expert digger",
            alias=None,
            units=None,
        ),
    ]
