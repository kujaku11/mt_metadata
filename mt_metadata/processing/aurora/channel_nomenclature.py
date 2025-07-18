# -*- coding: utf-8 -*-
"""

@author: kkappler
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.transfer_functions import CHANNEL_MAPS
from .standards import SCHEMA_FN_PATHS

from typing import Dict, Literal
# =============================================================================
attr_dict = get_schema("channel_nomenclature", SCHEMA_FN_PATHS)

# ====================== Nomenclature definitions for typehints and docstrings ============= #

SupportedNomenclature = Literal[
    "default",
    "lemi12",
    "lemi34",
    "musgraves",
    "nims",
    "phoenix123",
]


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

    def get_channel_map(self) -> Dict[str,str]:
        """
            Based on self.keyword return the mapping between conventional channel names and
            the custom channel names in the particular nomenclature.

        """
        try:
            return CHANNEL_MAPS[self.keyword.lower()]
        except KeyError:
            msg = f"channel mt_system {self.keyword} unknown)"
            raise NotImplementedError(msg)


    def update(self) -> None:
        """
        Assign values to standard channel names "ex", "ey" etc based on channel_map dict
        """
        channel_map = self.get_channel_map()
        self.ex = channel_map["ex"]
        self.ey = channel_map["ey"]
        self.hx = channel_map["hx"]
        self.hy = channel_map["hy"]
        self.hz = channel_map["hz"]

    def unpack(self) -> tuple:
        return self.ex, self.ey, self.hx, self.hy, self.hz

    @property
    def channels(self):
        channels = list(self.get_channel_map().values())
        return channels
