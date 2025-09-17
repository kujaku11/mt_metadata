# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import element_to_string
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class RemoteRef(MetadataBase):
    type: Annotated[
        str,
        Field(
            default="",
            description="type of remote referencing",
            examples=["robust multi-station remote referencing"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
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
        helpers._read_element(self, input_dict, "remote_ref")

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the RemoteRef object to XML format.

        Parameters
        ----------
        string : bool, optional
            Whether to return the XML as a string (default is False).
        required : bool, optional
            Whether to include required fields (default is True).

        Returns
        -------
        str | et.Element
            The XML representation of the RemoteRef object.
        """

        if self.type is None:
            self.type = ""

        root = et.Element(self.__class__.__name__, {"type": self.type})
        if string:
            return element_to_string(root)
        return root
