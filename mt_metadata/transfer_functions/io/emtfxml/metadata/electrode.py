# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field, field_validator, ValidationInfo

import mt_metadata.transfer_functions.io.emtfxml.metadata.helpers as helpers
from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment
from mt_metadata.common.enumerations import ElectrodeLocationEnum

# =====================================================


class Electrode(MetadataBase):
    location: Annotated[
        ElectrodeLocationEnum,
        Field(
            default="",
            description="Direction of electrode",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["N", "S", "E", "W"],
            },
        ),
    ]

    number: Annotated[
        str,
        Field(
            default="0",
            description="Electrode ID number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["1a"],
            },
        ),
    ]

    value: Annotated[
        str,
        Field(
            default="",
            description="Electrode value",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Ag-AgCl"],
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),  # type: ignore[return-value]
            description="comments on the electrode",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Ag-AgCl porous pot"],
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)  # type: ignore[return-value]
        return value

    def to_xml(self, string: bool = False, required: bool = False) -> str | et.Element:
        """ """

        root = et.Element(
            self.__class__.__name__,
            {"location": self.location.upper(), "number": self.number},
        )

        # this might break in the future when to_dict is updated to return a dict
        # instead of a string, but for now it works.
        root.text = self.comments.as_string()

        if string:
            return helpers.element_to_string(root)
        return root
