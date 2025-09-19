# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import ChannelEnum


# =====================================================


class Channel(MetadataBase):
    number: Annotated[
        int | None,
        Field(
            default=None,
            description="Channel number",
            examples=["1"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    azimuth: Annotated[
        float,
        Field(
            default=0.0,
            description="channel azimuth",
            examples=["90"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    tilt: Annotated[
        float,
        Field(
            default=0.0,
            description="channel tilt relative to horizontal.",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    dl: Annotated[
        float | str,
        Field(
            default=0.0,
            description="dipole length in meters",
            examples=["0.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    channel: Annotated[
        ChannelEnum,
        Field(
            default="",
            description="channel name",
            examples=["hx"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @property
    def channel_string(self) -> str:
        """Return the channel name as a string for indexing purposes."""
        if hasattr(self.channel, "value"):
            return self.channel.value
        return str(self.channel)

    def __str__(self):
        lines = ["Channel Metadata:"]
        for key in ["channel", "number", "dl", "azimuth", "tilt"]:
            try:
                value = getattr(self, key)
                # Special formatting for different field types
                if key == "channel" and hasattr(value, "value"):
                    # For enums, use the string value
                    if value.value == "":
                        display_value = "None"
                    else:
                        display_value = value.value
                elif key == "number" and value is None:
                    # Skip None number field completely
                    continue
                else:
                    display_value = value
                lines.append(f"\t{key.capitalize()}: {display_value:<12}")
            except TypeError:
                pass
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    @property
    def index(self):
        if self.number is not None:
            return self.number - 1
        else:
            return None

    def from_dict(self, channel_dict):
        """
        fill attributes from a dictionary
        """

        for key, value in channel_dict.items():
            if key in ["azm", "azimuth", "measurement_azimuth"]:
                self.azimuth = value
            elif key in ["chn_num", "number"]:
                self.number = value
            elif key in ["tilt", "measurement_tilt"]:
                self.tilt = value
            elif key in ["dl", "dipole_length"]:
                self.dl = value
            elif key in ["channel", "component"]:
                self.channel = value
