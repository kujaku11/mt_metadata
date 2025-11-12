# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator, PrivateAttr, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import AuthorPerson, Comment, Person, Software
from mt_metadata.common.mttime import MTime


# =====================================================
class Provenance(MetadataBase):
    _skip_equals: list[str] = PrivateAttr(["creation_time"])
    creation_time: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date and time the file was created.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "2020-02-08T12:23:40.324600+00:00",
                "type": "string",
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments on provenance of the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "all good",
                "type": "string",
            },
        ),
    ]

    log: Annotated[
        str | None,
        Field(
            default=None,
            description="A history of changes made to the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "2020-02-10T14:24:45+00:00 updated metadata",
                "type": "string",
            },
        ),
    ]

    creator: Annotated[
        AuthorPerson,
        Field(
            default_factory=AuthorPerson,
            description="Person who created the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Person(name=J. Pedantic, email=jped@mt.com)",
            },
        ),
    ]

    submitter: Annotated[
        AuthorPerson,
        Field(
            default_factory=AuthorPerson,
            description="Person who submitted the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Person(name=submitter_name, email=submitter@email)",
            },
        ),
    ]

    archive: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Archive from which the data was downloaded from.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Person(name=archive_name, url=https://archive.url)",
            },
        ),
    ]

    software: Annotated[
        Software,
        Field(
            default_factory=Software,
            description="Software used to create the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Software(name=mt_metadata, version=0.1)",
            },
        ),
    ]

    @field_validator("creation_time", mode="before")
    @classmethod
    def validate_creation_time(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value
