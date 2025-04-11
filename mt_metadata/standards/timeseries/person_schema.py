from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional, List, Dict, Any


class Person(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extras="allow")
    name: Annotated[
        str,
        Field(
            default="",
            type="string",
            description="Persons name, should be full first and last name.",
            title="name",
            examples="person name",
            default="",
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
            default=None,
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
            default=None,
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
            default=None,
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
            default=None,
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
            default=None,
            alias=None,
            units=None,
        ),
    ]
