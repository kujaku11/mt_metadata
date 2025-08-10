# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated, Any

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class ChannelEnum(str, Enum):
    ex = "ex"
    ey = "ey"
    hx = "hx"
    hy = "hy"
    hz = "hz"


class Channel(MetadataBase):
    number: Annotated[
        int,
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
        Any,
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
        Any,
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
        Any,
        Field(
            default=None,
            description="station",
            examples=["mt001"],
            alias=None,
            json_schema_extra={
                "units": None,
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

    def __str__(self):
        lines = ["Channel Metadata:"]
        for key in ["channel", "number", "dl", "azimuth", "tilt"]:
            try:
                lines.append(f"\t{key.capitalize()}: {getattr(self, key):<12}")
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
