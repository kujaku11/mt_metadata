# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field, field_validator, HttpUrl

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import ArrayDTypeEnum, EstimateIntentionEnum
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers
from mt_metadata.utils.units import get_unit_object


# =====================================================


class OutputEnum(str, Enum):
    E = "E"
    H = "H"


class InputEnum(str, Enum):
    E = "E"
    H = "H"


class DataType(MetadataBase):
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
            default="real",
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

    output: Annotated[
        OutputEnum,
        Field(
            default="",
            description="Type of output channels in data type",
            examples=["E"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    input: Annotated[
        InputEnum,
        Field(
            default="",
            description="Type of input channels in data type",
            examples=["E"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units: Annotated[
        str,
        Field(
            default="",
            description="Units for the data type",
            examples=["[mV/km]/[nT]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str) -> str:
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)

    def read_dict(self, input_dict: dict) -> None:
        """

        :param input_dict: input dictionary to read and populate the model fields.
        :type input_dict: dict
        :return: None
        """
        helpers._read_element(self, input_dict, "estimate")

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """

        :param string: return value as a string, defaults to False
        :type string: bool, optional
        :param required: include required values only, defaults to True
        :type required: bool, optional
        :return: XML representation of the model
        :rtype: str | et.Element

        """

        element = helpers.to_xml(
            self,
            string=string,
            required=required,
            order=["description", "external_url", "intention", "tag"],
        )
        if not string:
            element.attrib = {
                "name": self.name,
                "type": self.type,
                "output": self.output,
                "input": self.input,
                "units": self.units,
            }

        return element
