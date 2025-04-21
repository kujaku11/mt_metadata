# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field, HttpUrl, AliasChoices


# =====================================================
class Citation(MetadataBase):
    doi: Annotated[
        HttpUrl,
        Field(
            default="",
            description="full url of the doi number",
            examples="http://doi.###",
            type="string",
            alias=[],
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
            examples="M.Tee A. Roura",
            type="string",
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
            examples="Paper Title",
            type="string",
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
            examples="2020",
            type="string",
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
            examples="12",
            type="string",
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
            examples="10-15",
            type="string",
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
            examples="Journal of Geophysical Research",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
