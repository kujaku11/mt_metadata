# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import AliasChoices, Field, field_validator, HttpUrl

from mt_metadata.base import MetadataBase
from mt_metadata.utils.validators import validate_doi


# =====================================================
class Citation(MetadataBase):
    doi: Annotated[
        HttpUrl | str | None,
        Field(
            default=None,
            description="full url of the doi number",
            validation_alias=AliasChoices("doi", "survey_doi"),
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["http://doi.###"],
            },
        ),
    ]

    authors: Annotated[
        str | None,
        Field(
            default=None,
            description="author names",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["M.Tee A. Roura"],
            },
        ),
    ]

    title: Annotated[
        str | None,
        Field(
            default=None,
            description="Full title of the citation",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Paper Title"],
            },
        ),
    ]

    year: Annotated[
        str | None,
        Field(
            default=None,
            description="Year of citation",
            alias=None,
            pattern=r"^\d{4}(-\d{4})?$",  # Allows for ranges like "2020-2021"
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["2020"],
            },
        ),
    ]

    volume: Annotated[
        str | None,
        Field(
            default=None,
            description="Journal volume of the citation",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["12"],
            },
        ),
    ]

    pages: Annotated[
        str | None,
        Field(
            default=None,
            description="Page numbers of the citation",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["10-15"],
            },
        ),
    ]

    journal: Annotated[
        str | None,
        Field(
            default=None,
            description="Journal title of citation",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Journal of Geophysical Research"],
            },
        ),
    ]

    @field_validator("doi", mode="before")
    @classmethod
    def validate_doi(
        cls,
        value: HttpUrl | str | None,
    ) -> HttpUrl | None:
        """
        Validate the DOI.

        Parameters
        ----------
        value : str | None
            The DOI value to validate.
        info : ValidationInfo
            Additional validation information.

        Returns
        -------
        str | None
            The validated DOI or None if not provided.
        """
        return validate_doi(value)
