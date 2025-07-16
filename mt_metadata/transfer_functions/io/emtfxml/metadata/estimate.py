# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field, HttpUrl

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import ArrayDTypeEnum, EstimateIntentionEnum
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================


class Estimate(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the statistical estimate",
            examples=["var"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    type: Annotated[
        ArrayDTypeEnum,
        Field(
            default="",
            description="Type of number contained in the estimate",
            examples=["real"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    description: Annotated[
        str,
        Field(
            default="",
            description="Description of the statistical estimate",
            examples=["this is an estimate"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    external_url: Annotated[
        HttpUrl,
        Field(
            default="",
            description="Full path to external link that has additional information",
            examples=["http://www.iris.edu/dms/products/emtf/variance.html"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    intention: Annotated[
        EstimateIntentionEnum,
        Field(
            default="",
            description="The intension of the statistical estimate",
            examples=["error estimate"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    tag: Annotated[
        str,
        Field(
            default="",
            description="A useful tag for the estimate",
            examples=["tipper"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    def read_dict(self, input_dict: dict) -> None:
        """

        :param input_dict: input dictionary containing estimate data
        :type input_dict: dict
        :return: None
        :rtype: None

        """
        helpers._read_element(self, input_dict, "estimate")

    def to_xml(self, string: bool = False, required: bool = True):
        """

        :param string: return string representation, defaults to False
        :type string: bool, optional
        :param required: include only required fields, defaults to True
        :type required: bool, optional
        :return: XML representation of the estimate
        :rtype: str | Element

        """

        root = et.Element(
            self.__class__.__name__.capitalize(),
            {"name": self.name.upper(), "type": self.type},
        )

        et.SubElement(root, "Description").text = self.description
        et.SubElement(root, "ExternalUrl").text = (
            str(self.external_url) if self.external_url else ""
        )
        et.SubElement(root, "Intention").text = self.intention
        et.SubElement(root, "tag").text = self.tag

        if string:
            return helpers.element_to_string(root)
        return root
