# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


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

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

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
                "rating",
                "good_from_period",
                "good_to_period",
                "comments",
            ],
        )
