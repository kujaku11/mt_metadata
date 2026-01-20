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
class PeriodRange(MetadataBase):
    min: Annotated[
        float,
        Field(
            default=0.0,
            description="minimum period",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": ['"4.5E-5"'],
            },
        ),
    ]

    max: Annotated[
        float,
        Field(
            default=0.0,
            description="maxmimu period",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": ['"4.5E5"'],
            },
        ),
    ]

    def read_dict(self, input_dict: dict) -> None:
        """
        Read the period_range element from the input dictionary.

        Parameters
        ----------
        input_dict : dict
            The input dictionary containing the period_range element.
        """
        helpers._read_element(self, input_dict, "period_range")

    def to_xml(self, string=False, required=True) -> et.Element | str:
        """
        Convert the period_range element to XML.

        Parameters
        ----------
        string : bool, optional
            Whether to return the XML as a string, by default False
        required : bool, optional
            Whether the element is required, by default True

        Returns
        -------
        et.Element | str
            The XML representation of the period_range element.
        """

        root = et.Element(
            self.__class__.__name__,
            {
                "min": f"{self.min:<16.5E}".strip(),
                "max": f"{self.max:<16.5E}".strip(),
            },
        )
        if string:
            return element_to_string(root)
        return root
