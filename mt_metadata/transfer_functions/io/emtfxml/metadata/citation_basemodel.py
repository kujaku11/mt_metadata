# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from pydantic import Field, field_validator, HttpUrl

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers
from mt_metadata.utils.mttime import MTime


# =====================================================
class Citation(MetadataBase):
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

    year: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Year of citation",
            examples=["2020"],
            alias=None,
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

    doi: Annotated[
        HttpUrl | None,
        Field(
            default=None,
            description="doi number of the citation",
            examples=["###/###"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    survey_d_o_i: Annotated[
        HttpUrl | None,
        Field(
            default=None,
            description="doi number of the survey",
            examples=["###/###"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("year", mode="before")
    @classmethod
    def validate_year(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=[
                "title",
                "authors",
                "year",
                "survey_d_o_i",
            ],
        )
