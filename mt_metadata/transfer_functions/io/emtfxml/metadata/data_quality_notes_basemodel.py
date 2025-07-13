# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

from .comment_basemodel import Comment


# =====================================================
class DataQualityNotes(MetadataBase):
    good_from_period: Annotated[
        float | None,
        Field(
            default=None,
            description="Data are good for periods larger than this number",
            examples=["0.01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    good_to_period: Annotated[
        float | None,
        Field(
            default=None,
            description="Data are good for periods smaller than this number",
            examples=["1000"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    rating: Annotated[
        int | None,
        Field(
            default=None,
            description="Rating of the data from 0 to 5 where 5 is the best and 0 is unrated",
            examples=["4"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default=None,
            description="Comments about the data quality",
            examples=["Data quality is good", "Some issues found"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value) -> Comment:
        """
        Validate that the value is a valid string.
        """
        if isinstance(value, str):
            return Comment(value=value)  # type: ignore[return-value]
        return value

    def read_dict(self, input_dict: dict) -> None:
        """

        :param input_dict: input dictionary to read and populate the model fields.
        :type input_dict: dict
        :return: None
        :rtype: None

        """
        try:
            comments_dict = {
                "comments": input_dict["data_quality_notes"].pop("comments")
            }
        except KeyError:
            comments_dict = {"comments": ""}
        self.comments = Comment()  # type: ignore
        self.comments.read_dict(comments_dict)
        helpers._read_element(self, input_dict, "data_quality_notes")

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the DataQualityNotes instance to XML format.

        :param string: If True, return the XML as a string. If False, return an ElementTree Element.
        :type string: bool, optional
        :param required: If True, include all required fields in the XML.
        :type required: bool, optional
        :return: The XML representation of the DataQualityNotes instance.
        :rtype: str | et.Element
        :rtype: TYPE

        """

        return helpers.to_xml(
            self,
            string=string,
            required=required,
            order=[
                "rating",
                "good_from_period",
                "good_to_period",
                "comments",
            ],
        )
