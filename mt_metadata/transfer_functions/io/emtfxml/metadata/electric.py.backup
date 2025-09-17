# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field

import mt_metadata.transfer_functions.io.emtfxml.metadata.helpers as helpers
from mt_metadata.base import MetadataBase


# =====================================================
class Electric(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the channel",
            examples=["ex"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    orientation: Annotated[
        float,
        Field(
            default=0.0,
            description="orientation angle relative to geographic north",
            examples=["11.9"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    x: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in north direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    x2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in north direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    y: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in east direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    y2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in east direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    z: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in depth",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    z2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in depth",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """

        :param string: return a string representation of the xml, defaults to False
        :type string: bool, optional
        :param required: return a string representation of the xml, defaults to True
        :type required: bool, optional
        :type required: bool, optional
        :return: string or xml element representation of the Electric object
        :rtype: str | et.Element

        """

        for attr in ["orientation", "x", "y", "z", "x2", "y2", "z2"]:
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
                "x2": f"{self.x2:.3f}",
                "y2": f"{self.y2:.3f}",
                "z2": f"{self.z2:.3f}",
            },
        )

        if string:
            return helpers.element_to_string(root)
        return root
