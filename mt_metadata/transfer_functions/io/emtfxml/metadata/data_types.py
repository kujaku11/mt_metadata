# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from loguru import logger
from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

from . import DataType


# =====================================================
class DataTypes(MetadataBase):
    data_types_list: Annotated[
        list[DataType | dict],
        Field(
            default_factory=list,
            description="list of data types",
            examples=["[Z T]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("data_types_list", mode="before")
    @classmethod
    def validate_data_types_list(
        cls, value: list[DataType | dict], info: ValidationInfo
    ) -> list[DataType]:
        if not isinstance(value, list):
            value = [value]
        dt_list = []
        for item in value:
            if isinstance(item, dict):
                dt = DataType()  # type: ignore
                dt.from_dict(item)
                dt_list.append(dt)
            elif isinstance(item, DataType):
                dt_list.append(item)
            else:
                raise TypeError(
                    f"data_types_list must be a list of DataType instances or dictionaries, got {type(item)}"
                )
        return dt_list

    def read_dict(self, input_dict: dict) -> None:
        """
        Read in statistical estimate descriptions

        :param input_dict: input dictionary containing data types
        :type input_dict: dict
        :return: None
        :rtype: None

        """
        try:
            self.data_types_list = input_dict["data_types"]["data_type"]
        except KeyError:
            logger.warning("Could not read Data Types")

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """

        :param string: return XML string, defaults to False
        :type string: bool, optional
        :param required: include required fields, defaults to True
        :type required: bool, optional
        :return: XML representation of the object
        :rtype: str | et.Element
        :raises TypeError: if data_types_list is not a list of DataType instances or dictionaries
        :raises ValueError: if data_types_list is empty

        """

        root = et.Element(self.__class__.__name__)

        for dtype in self.data_types_list:
            root.append(dtype.to_xml(required=required))  # type: ignore return-value

        if string:
            return helpers.element_to_string(root)
        return root
