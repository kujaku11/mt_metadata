# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import ElementTree as et

import numpy as np
import pandas as pd
from loguru import logger
from pydantic import (
    Field,
    field_validator,
    model_validator,
    ValidationError,
    ValidationInfo,
)
from typing_extensions import Self

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import element_to_string
from mt_metadata.utils.mttime import MTime


# =====================================================
class Comment(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default=None,
            description="person who authored the comment",
            examples=["J. Pedantic"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    time_stamp: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str | MTime | None,
        Field(
            default_factory=lambda: MTime(time_stamp="1980-01-01T00:00:00+00:00"),
            description="Date and time of in UTC of when comment was made.",
            examples=["2020-02-01T09:23:45.453670+00:00"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    value: Annotated[
        str | list | None,
        Field(
            default=None,
            description="comment string",
            examples=["failure at midnight."],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    @field_validator("time_stamp", mode="before")
    @classmethod
    def validate_time(cls, value, info: ValidationInfo) -> MTime:
        """
        Validate that the value is a valid time.
        """
        return MTime(time_stamp=value)

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, value, info: ValidationInfo) -> str | list | None:
        """
        Validate that the value is a valid string or list.
        """
        if isinstance(value, str):
            return value.strip()
        elif isinstance(value, list):
            return ",".join([v.strip() for v in value if isinstance(v, str)])
        elif value is None:
            return None
        else:
            raise TypeError(f"Invalid type for value: {type(value)}")

    @model_validator(mode="after")
    def set_variables(self) -> Self:
        """
        Validate that the value is a valid string.
        """
        if self.value is not None:
            if "|" in self.value:
                parts = [ss.strip() for ss in self.value.split("|")]
                self.value = parts[-1]
                if len(parts) == 3:
                    self.time_stamp = parts[0]
                    self.author = parts[1]
                elif len(parts) == 2:
                    try:
                        self.time_stamp = parts[0]
                    except ValidationError:
                        self.author = parts[0]
        return self

    # need to override __eq__ to compare the values of the object
    # otherwise the __eq__ from MetadataBase will be used which
    # assumes an object.
    def __eq__(self, other: object) -> bool:
        """
        Check if two Comment objects are equal.

        Parameters
        ----------
        other : object
            The object to compare with.

        Returns
        -------
        bool
            True if the objects are equal, False otherwise.
        """
        if other is None:
            return Comment(value=None)  # type: ignore
        if isinstance(other, str):
            other = Comment(value=other)  # type: ignore
        elif isinstance(other, dict):
            other = Comment(**other)
        return (
            self.author == other.author
            and self.time_stamp == other.time_stamp
            and self.value == other.value
        )

    def to_dict(self, nested=False, single=False, required=True) -> str:
        """
        Returns the comment as "{time_stamp} | {author} | {comment}"

        TODO: in the future this should return an actual dictionary to
         comply with all other objects.

        Returns
        -------
        str
            formatted comment
        """
        if self.value is None:
            return None

        if self.time_stamp == "1980-01-01T00:00:00+00:00":
            if self.author in [None, ""]:
                return self.value
            return f" {self.author} | {self.value}"
        if self.author in [None, ""]:
            return f"{self.time_stamp} | {self.value}"
        return f"{self.time_stamp} | {self.author} | {self.value}"

    def from_dict(
        self,
        value: str | dict,
        skip_none=False,
    ) -> None:
        """
        Parse input comment assuming "{time_stamp} | {author} | {comment}"

        Parameters
        ----------
        value : str
            _description_
        skip_none : bool, optional
            _description_, by default False
        """
        if isinstance(value, str):
            self.value = value
        elif isinstance(value, dict):
            if len(value.keys()) > 1:
                self.time_stamp = value.get("time_stamp", None)
                self.author = value.get("author", None)
                self.value = value.get("value", None)

            elif len(value.keys()) == 1:
                key = list(value.keys())[0]
                value = value[key]
                if isinstance(value, dict):
                    self.time_stamp = value.get("time_stamp", None)
                    self.author = value.get("author", None)
                    self.value = value.get("value", None)
                elif isinstance(value, str):
                    self.value = value

            # this only happens on instance creation, so we can ignore it
            else:
                pass

        else:
            raise TypeError(f"Cannot parse type {type(value)}")

    def read_dict(self, input_dict: dict) -> None:
        """

        can probably use from_dict method instead, but to keep consistency in EMTF XML
        metadata, this method is used to read the comment from a dictionary.

        :param input_dict: input dictionary containing comment data
        :type input_dict: dict
        :return: None
        :rtype: None

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
                self.time_stamp = key["date"]
            except KeyError:
                logger.debug("No date for comment")
        else:
            raise TypeError(f"Comment cannot parse type {type(key)}")

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the Comment instance to XML format.

        :param string: If True, return the XML as a string. If False, return an ElementTree Element.
        :type string: bool, optional
        :param required: If True, include all required fields.
        :type required: bool, optional
        :return: XML representation of the Comment.
        :rtype: str | et.Element
        """

        if self.author is None:
            self.author = ""
        root = et.Element(self.__class__.__name__ + "s", {"author": self.author})
        if self.value is None:
            self.value = ""
        root.text = self.value

        if string:
            return element_to_string(root)
        return root
