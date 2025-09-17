# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata.helpers import element_to_string


# =====================================================
class Magnetic(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hx"],
            },
        ),
    ]

    orientation: Annotated[
        float,
        Field(
            default=0.0,
            description="orientation angle relative to geographic north",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["11.9"],
            },
        ),
    ]

    x: Annotated[
        float,
        Field(
            default=0.0,
            description="location of sensor relative center point in north direction",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    y: Annotated[
        float,
        Field(
            default=0.0,
            description="location of sensor relative center point in east direction",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    z: Annotated[
        float,
        Field(
            default=0.0,
            description="location of sensor relative center point in depth",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """

        :param string: Whether to return the XML as a string, defaults to False
        :type string: bool, optional
        :param required: Whether to include required fields, defaults to True
        :type required: bool, optional
        :return: The XML representation of the object
        :rtype: str | et.Element

        """
        for attr in ["orientation", "x", "y", "z"]:
            value = getattr(self, attr)
            if value is None:
                setattr(self, attr, 0)
        root = et.Element(
            self.__class__.__name__.capitalize(),
            {
                "name": self.name,
                "orientation": f"{self.orientation:.3f}",
                "x": f"{self.x:.3f}",
                "y": f"{self.y:.3f}",
                "z": f"{self.z:.3f}",
            },
        )

        if string:
            return element_to_string(root)
        return root
