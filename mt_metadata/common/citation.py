# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import AliasChoices, Field, HttpUrl

from mt_metadata.base import MetadataBase


# =====================================================
class Citation(MetadataBase):
    doi: Annotated[
        HttpUrl | None,
        Field(
            default=None,
            description="full url of the doi number",
            examples=["http://doi.###"],
            validation_alias=AliasChoices("doi", "survey_doi"),
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    authors: Annotated[
        str | None,
        Field(
            default=None,
            description="author names",
            examples=["M.Tee A. Roura"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    title: Annotated[
        str | None,
        Field(
            default=None,
            description="Full title of the citation",
            examples=["Paper Title"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    year: Annotated[
        str | None,
        Field(
            default=None,
            description="Year of citation",
            examples=["2020"],
            alias=None,
            pattern=r"^\d{4}$",
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    volume: Annotated[
        str | None,
        Field(
            default=None,
            description="Journal volume of the citation",
            examples=["12"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    pages: Annotated[
        str | None,
        Field(
            default=None,
            description="Page numbers of the citation",
            examples=["10-15"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    journal: Annotated[
        str | None,
        Field(
            default=None,
            description="Journal title of citation",
            examples=["Journal of Geophysical Research"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
