# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import ChannelOrientationEnum
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================


class Orientation(MetadataBase):
    angle_to_geographic_north: Annotated[
        float,
        Field(
            default=0.0,
            description="Angle to geographic north of the station orientation",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": [0],
            },
        ),
    ]

    layout: Annotated[
        ChannelOrientationEnum,
        Field(
            default=ChannelOrientationEnum.orthogonal,
            description="Orientation of channels relative to each other",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["orthogonal"],
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
        element_dict = {self._class_name: input_dict[self._class_name]}
        if isinstance(element_dict[self._class_name], str):
            element_dict[self._class_name] = {"layout": element_dict[self._class_name]}

        self.from_dict(element_dict)

    def to_xml(self, string=False, required=True):
        """
        Overwrite to XML to follow EMTF XML format

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self.layout == "orthogonal":
            if self.angle_to_geographic_north is None:
                self.angle_to_geographic_north = 0.0
            root = et.Element(
                self.__class__.__name__.capitalize(),
                {"angle_to_geographic_north": f"{self.angle_to_geographic_north:.3f}"},
            )
            root.text = self.layout
        else:
            root = et.Element(self.__class__.__name__.capitalize())
            root.text = self.layout

        if not string:
            return root
        else:
            return helpers.element_to_string(root)
