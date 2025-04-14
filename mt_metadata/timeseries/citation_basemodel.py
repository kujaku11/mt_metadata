# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime
from pydantic import Field, HttpUrl, field_validator


# =====================================================
class Citation(MetadataBase):
    doi: Annotated[
        HttpUrl,
        Field(
            default="",
            description="full url of the doi number",
            examples="http://doi.###",
            type="string",
            alias=["survey_doi"],
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
    ] = None

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
    ] = None

    year: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Year of citation",
            examples="2020",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

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
    ] = None

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
    ] = None

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
    ] = None

    @field_validator("year", mode="before")
    @classmethod
    def validate_year(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)
