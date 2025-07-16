# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

from . import Citation


# =====================================================
class ReleaseStatusEnum(str, Enum):
    Unrestricted_release = "Unrestricted release"
    Restricted_release = "Restricted release"
    Paper_Citation_Required = "Paper Citation Required"
    Academic_Use_Only = "Academic Use Only"
    Conditions_Apply = "Conditions Apply"
    Data_Citation_Required = "Data Citation Required"


class Copyright(MetadataBase):
    citation: Annotated[
        Citation,
        Field(
            default_factory=Citation,  # type: ignore
            description="The citation information for the data",
            examples=[
                "Citation(authors='Doe, J.', year='2023', title='Title of the paper', journal='Journal Name', volume='45', pages='123-145')"
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    selected_publications: Annotated[
        str | None,
        Field(
            default=None,
            description="Any publications that use this data",
            examples=["my paper"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    release_status: Annotated[
        ReleaseStatusEnum,
        Field(
            default="Unrestricted Release",
            description="the release status of the data",
            examples=["Unrestricted release"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    conditions_of_use: Annotated[
        str,
        Field(
            default="All data and metadata for this survey are available free of charge and may be copied freely, duplicated and further distributed provided this data set is cited as the reference. While the author(s) strive to provide data and metadata of best possible quality, neither the author(s) of this data set, not IRIS make any claims, promises, or guarantees about the accuracy, completeness, or adequacy of this information, and expressly disclaim liability for errors and omissions in the contents of this file. Guidelines about the quality or limitations of the data and metadata, as obtained from the author(s), are included for informational purposes only.",
            description="Any notes on conditions of use",
            examples=["Cite data upon usage."],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    acknowledgement: Annotated[
        str | None,
        Field(
            default=None,
            description="any acknowledgments the transfer function should have.",
            examples=["This project was funded by x."],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    additional_info: Annotated[
        str | None,
        Field(
            default=None,
            description="any additional information about the data.",
            examples=["This purpose of this project is ..."],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    def read_dict(self, input_dict):
        """

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        helpers._read_element(self, input_dict, "copyright")

    def to_xml(self, string=False, required=True):
        """ """
        # Create a shallow copy to avoid mutating the original object
        import copy

        xml_copy = copy.copy(self)
        # Set the title-cased release_status on the copy using object.__setattr__
        # to bypass Pydantic validation
        object.__setattr__(xml_copy, "release_status", self.release_status.title())

        return helpers.to_xml(
            xml_copy,
            string=string,
            required=required,
            order=[
                "citation",
                "selected_publications",
                "acknowledgement",
                "release_status",
                "conditions_of_use",
                "additional_info",
            ],
        )
