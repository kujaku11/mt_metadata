# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import cElementTree as et

from loguru import logger
from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers

from .electrode_basemodel import Electrode


# =====================================================
class Dipole(MetadataBase):
    manufacturer: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the manufacturer of the instrument",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["MT Gurus"],
            },
        ),
    ]

    length: Annotated[
        float | None,
        Field(
            default=None,
            description="Dipole length",
            json_schema_extra={
                "units": "meters",
                "required": False,
                "examples": ["100.0"],
            },
        ),
    ]

    azimuth: Annotated[
        float | None,
        Field(
            default=None,
            description="Azimuth of the dipole relative to coordinate system",
            json_schema_extra={
                "units": "degrees",
                "required": False,
                "examples": ["90"],
            },
        ),
    ]

    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the dipole",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["dipole1"],
            },
        ),
    ]

    type: Annotated[
        str | None,
        Field(
            default=None,
            description="type of dipole",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["wire"],
            },
        ),
    ]

    electrode: Annotated[
        list[Electrode],
        Field(
            default_factory=list,
            description="List of electrodes that make up the dipole",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": [{"name": "ex", "type": "wire"}],
            },
        ),
    ]

    @field_validator("electrode", mode="before")
    def validate_electrode(cls, value: list[Electrode] | list[dict]) -> list[Electrode]:
        """
        Validate that the value is a list of Electrode objects.
        """
        if not isinstance(value, list):
            value = [value]
        value_list = []
        for item in value:
            if isinstance(item, dict):
                e_obj = Electrode()  # type: ignore
                e_obj.from_dict(item)
                value_list.append(e_obj)
            elif isinstance(item, Electrode):
                value_list.append(item)
            else:
                raise TypeError(
                    "Electrode must be an instance of Electrode class or a dict"
                )
        return value_list

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        root = et.Element(
            self.__class__.__name__, {"name": self.name, "type": self.type}
        )
        try:
            et.SubElement(root, "manufacturer").text = self.manufacturer
        except AttributeError:
            logger.debug("Dipole has no manufacturer information")
        if self.length is not None:
            et.SubElement(
                root, "length", {"units": "meters"}
            ).text = f"{self.length:.3f}"
        if self.azimuth is not None:
            et.SubElement(
                root, "azimuth", {"units": "degrees"}
            ).text = f"{self.azimuth:.3f}"
        for item in self.electrode:
            root.append(item.to_xml())

        if string:
            return helpers.element_to_string(root)
        return root
