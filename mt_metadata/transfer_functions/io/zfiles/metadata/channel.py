# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 18:52:52 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================

from mt_metadata.base import get_schema, Base
from mt_metadata.base.helpers import write_lines
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("channel", SCHEMA_FN_PATHS)

# ==============================================================================
# data section
# ==============================================================================
class Channel(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, channel_dict=None):
        self.number = 1
        self.azimuth = 0
        self.tilt = 0
        self.dl = 0
        self.channel = None

        super().__init__(attr_dict=attr_dict)

        if channel_dict is not None:
            self.from_dict(channel_dict)

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
