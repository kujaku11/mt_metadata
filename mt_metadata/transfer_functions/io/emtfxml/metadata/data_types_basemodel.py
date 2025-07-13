# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase

from .data_type_basemodel import DataType


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

    def read_dict(self, input_dict):
        """
        Read in statistical estimate descriptions

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        try:
            self.data_types_list = input_dict["data_types"]["data_type"]
        except KeyError:
            self.logger.warning("Could not read Data Types")

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        root = et.Element(self.__class__.__name__)

        for dtype in self.data_types_list:
            root.append(dtype.to_xml(required=required))

        if string:
            return element_to_string(root)
        return root
