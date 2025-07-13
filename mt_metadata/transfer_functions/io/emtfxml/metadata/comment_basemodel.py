# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

import numpy as np
import pandas as pd
from loguru import logger
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers
from mt_metadata.utils.mttime import MTime


# =====================================================
class Comment(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default=None,
            description="Author who made the comment",
            examples=["M. Tee"],
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date the comment was made",
            examples=["2020-01-21"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    value: Annotated[
        str | None,
        Field(
            default=None,
            description="Comment string",
            examples=["This is a comment"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)  # type: ignore[return-value]

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        key = input_dict["comments"]
        if isinstance(key, str):
            self.value = key
        elif isinstance(key, dict):
            try:
                self.value = key["value"]
            except KeyError:
                logger.debug("No value in comment")

            try:
                self.author = key["author"]
            except KeyError:
                logger.debug("No author of comment")
            try:
                self.date = key["date"]
            except KeyError:
                logger.debug("No date for comment")
        else:
            raise TypeError(f"Comment cannot parse type {type(key)}")

    def to_xml(self, string=False, required=True):
        """ """
        if self.author is None:
            self.author = ""
        root = et.Element(self.__class__.__name__ + "s", {"author": self.author})
        if self.value is None:
            self.value = ""
        root.text = self.value

        if string:
            return helpers.element_to_string(root)
        return root
