# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field, PrivateAttr

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class Attachment(MetadataBase):
    filename: Annotated[
        str,
        Field(
            default="",
            description="file name of the attached file data",
            examples=["example.zmm"],
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
            description="description of the attached file",
            examples=["The original used to produce the XML"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    _attachments: list = PrivateAttr(default_factory=list)

    def read_dict(self, input_dict: dict) -> None:
        """Read the input dictionary and populate the model fields."""
        element_dict = {self.__class__.__name__: input_dict[self.__class__.__name__]}
        if isinstance(element_dict[self.__class__.__name__], type(None)):
            return
        elif isinstance(element_dict[self.__class__.__name__], list):
            for item in element_dict[self.__class__.__name__]:
                attachment_item = Attachment()  # type: ignore
                if not self.__class__.__name__ in item.keys():
                    item = {self.__class__.__name__: item}
                attachment_item.from_dict(item)
                self._attachments.append(attachment_item)

        else:
            self.from_dict(element_dict)

    def to_xml(
        self, string: bool = False, required: bool = True
    ) -> str | et.Element | list[str] | list[et.Element]:
        """

        :param string: return as an XML string, defaults to False
        :type string: bool, optional
        :param required: whether the field is required, defaults to True
        :type required: bool, optional
        :return: the XML representation of the object
        :rtype: str | list[str]

        """

        if self._attachments == []:
            result = helpers.to_xml(
                self,
                string=string,
                required=required,
                order=["filename", "description"],
            )
            return result
        else:
            return [
                helpers.to_xml(
                    item,
                    string=string,
                    required=required,
                    order=["filename", "description"],
                )
                for item in self._attachments
            ]  # type: ignore
