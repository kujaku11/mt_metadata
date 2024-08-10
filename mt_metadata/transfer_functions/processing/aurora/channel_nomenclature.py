# -*- coding: utf-8 -*-
"""

@author: kkappler
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

from mt_metadata.transfer_functions import CHANNEL_MAPS

# =============================================================================
attr_dict = get_schema("channel_nomenclature", SCHEMA_FN_PATHS)


# =============================================================================
class ChannelNomenclature(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, keyword=None):

        super().__init__(attr_dict=attr_dict)
        self._keyword = keyword
        if self._keyword is not None:
            self.update()

    @property
    def ex_ey(self):
        return [self.ex, self.ey]

    @property
    def hx_hy(self):
        return [self.hx, self.hy]

    @property
    def hx_hy_hz(self):
        return [self.hx, self.hy, self.hz]

    @property
    def ex_ey_hz(self):
        return [self.ex, self.ey, self.hz]

    @property
    def default_input_channels(self):
        return self.hx_hy

    @property
    def default_output_channels(self):
        return self.ex_ey_hz

    @property
    def default_reference_channels(self):
        return self.hx_hy

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        self._keyword = keyword
        self.update()

    def get_channel_map(self):
        if self.keyword == "default":
            channel_map = CHANNEL_MAPS["default"]
        elif self.keyword.upper() == "LEMI12":
            channel_map = CHANNEL_MAPS["lemi12"]
        elif self.keyword.upper() == "LEMI34":
            channel_map = CHANNEL_MAPS["lemi34"]
        elif self.keyword.upper() == "NIMS":
            channel_map = CHANNEL_MAPS["default"]
        elif self.keyword.upper() == "PHOENIX123":
            channel_map = CHANNEL_MAPS["phoenix123"]
        elif self.keyword.upper() == "MUSGRAVES":
            channel_map = CHANNEL_MAPS["musgraves"]
        else:
            msg = f"channel mt_system {self.keyword} unknown"
            raise NotImplementedError(msg)
        return channel_map

    def update(self):
        """
        Assign values to standard channel names "ex", "ey" etc based on channel_map dict
        """
        channel_map = self.get_channel_map()
        self.ex = channel_map["ex"]
        self.ey = channel_map["ey"]
        self.hx = channel_map["hx"]
        self.hy = channel_map["hy"]
        self.hz = channel_map["hz"]

    def unpack(self):
        return self.ex, self.ey, self.hx, self.hy, self.hz

    @property
    def channels(self):
        channels = list(self.get_channel_map().values())
        return channels
