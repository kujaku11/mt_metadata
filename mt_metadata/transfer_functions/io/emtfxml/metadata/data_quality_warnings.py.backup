# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class DataQualityWarnings(MetadataBase):
    flag: Annotated[
        int | None,
        Field(
            default=None,
            description="Flag for data quality",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
    comments: Annotated[
        Comment | None,
        Field(
            default_factory=Comment,  # type: ignore
            description="Comments about the data quality warnings",
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
    def validate_comments(cls, v):
        """Ensure comments is an instance of Comment."""
        if isinstance(v, Comment):
            return v
        elif isinstance(v, str):
            return Comment(value=v)  # type: ignore
        elif v is None:
            return Comment()  # type: ignore
        else:
            raise TypeError("comments must be a Comment instance or a string")

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "data_quality_warnings")

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
            order=["flag", "comments"],
        )
