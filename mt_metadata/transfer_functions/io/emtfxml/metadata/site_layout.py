# =====================================================
# Imports
# =====================================================
from typing import Annotated
from xml.etree import ElementTree as et

from loguru import logger
from pydantic import computed_field, Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import element_to_string

from . import Electric, Magnetic


# =====================================================
class SiteLayout(MetadataBase):
    input_channels: Annotated[
        list[Electric | Magnetic | str],
        Field(
            default_factory=list,
            description="list of input channels for transfer function estimation",
            examples=["[Magnetic(hx), Magnetic(hy)]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        list[Electric | Magnetic | str],
        Field(
            default_factory=list,
            description="list of output channels for transfer function estimation",
            examples=["[Electric(ex), Electric(ey), Magnetic(hz)]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @computed_field
    @property
    def input_channel_names(self) -> list[str]:
        """
        Returns a list of input channel names.
        """
        return [ch.name.lower() for ch in self.input_channels]

    @computed_field
    @property
    def output_channel_names(self) -> list[str]:
        """
        Returns a list of output channel names.
        """
        return [ch.name.lower() for ch in self.output_channels]

    @field_validator("input_channels", "output_channels", mode="before")
    @classmethod
    def validate_channels(
        cls, value: list[Electric | Magnetic | str]
    ) -> list[Electric | Magnetic]:
        channels = []
        if not isinstance(value, list):
            value = [value]

        for item in value:
            if isinstance(item, (Magnetic, Electric)):
                channels.append(item)
            elif isinstance(item, dict):
                try:
                    # Assume the dict has a single key for channel type
                    ch_type = list(item.keys())[0]
                except IndexError:
                    msg = "Channel dict must have a single key for channel type"
                    logger.error(msg)
                    raise ValueError(msg)
                ch_type = list(item.keys())[0]
                if ch_type in ["magnetic"]:
                    ch = Magnetic()  # type: ignore
                elif ch_type in ["electric"]:
                    ch = Electric()  # type: ignore
                else:
                    msg = f"Channel type {ch_type} not supported"
                    logger.error(msg)
                    raise ValueError(msg)
                ch.from_dict(item)
                channels.append(ch)
            elif isinstance(item, str):
                if item.lower().startswith("e"):
                    ch = Electric(name=item)  # type: ignore
                elif item.lower().startswith("b") or item.lower().startswith("h"):
                    ch = Magnetic(name=item)  # type: ignore
                else:
                    msg = f"Channel {item} not supported"
                    logger.error(msg)
                    raise ValueError(msg)
                channels.append(ch)
            else:
                msg = f"Channel {item} not supported"
                logger.error(msg)
                raise TypeError(msg)

        return channels

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        Convert the SiteLayout instance to an XML representation.

        Parameters
        ----------
        string : bool, optional
            Whether to return the XML as a string, by default False
        required : bool, optional
            Whether the XML elements are required, by default True

        Returns
        -------
        str | et.Element
            The XML representation of the SiteLayout instance
        """

        root = et.Element(self.__class__.__name__)

        section = et.SubElement(
            root, "InputChannels", attrib={"ref": "site", "units": "m"}
        )
        for ch in self.input_channels:
            section.append(ch.to_xml(required=required))
        section = et.SubElement(
            root, "OutputChannels", attrib={"ref": "site", "units": "m"}
        )
        for ch in self.output_channels:
            section.append(ch.to_xml(required=required))

        if string:
            return element_to_string(root)
        return root
