# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime
from mt_metadata.common import AuthorPerson, Person, Comment, Software
from pydantic import Field, field_validator, ValidationInfo


# =====================================================
class Provenance(MetadataBase):
    creation_time: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date and time the file was created.",
            examples="2020-02-08T12:23:40.324600+00:00",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments on provenance of the data.",
            examples="all good",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    log: Annotated[
        str | None,
        Field(
            default=None,
            description="A history of changes made to the data.",
            examples="2020-02-10T14:24:45+00:00 updated metadata",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    creator: Annotated[
        AuthorPerson,
        Field(
            default_factory=AuthorPerson,
            description="Person who created the data.",
            examples="Person(name=J. Pedantic, email=jped@mt.com)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    submitter: Annotated[
        AuthorPerson,
        Field(
            default_factory=AuthorPerson,
            description="Person who submitted the data.",
            examples="Person(name=submitter_name, email=submitter@email)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    archive: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Archive from which the data was downloaded from.",
            examples="Person(name=archive_name, url=https://archive.url)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    software: Annotated[
        Software,
        Field(
            default_factory=Software,
            description="Software used to create the data.",
            examples="Software(name=mt_metadata, version=0.1)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
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
