# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Magnetic, Electric

# =============================================================================
attr_dict = get_schema("site_layout", SCHEMA_FN_PATHS)
# =============================================================================


class SiteLayout(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._input_channels = []
        self._output_channels = []

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def input_channels(self):
        return self._input_channels

    @input_channels.setter
    def input_channels(self, value):
        if not isinstance(value, list):
            value = [value]

        for item in value:

            ch_type = list(item.keys())[0]
            if ch_type in ["magnetic"]:
                ch = Magnetic()
            elif ch_type in ["electric"]:
                ch = Electric()
            else:
                msg = "Channel type %s not supported"
                self.logger.error(msg, ch_type)
                raise ValueError(msg % ch_type)
            ch.from_dict(item)
            self._input_channels.append(ch)

    @property
    def output_channels(self):
        return self._output_channels

    @output_channels.setter
    def output_channels(self, value):
        if not isinstance(value, list):
            value = [value]

        for item in value:
            ch_type = list(item.keys())[0]
            if ch_type in ["magnetic"]:
                ch = Magnetic()
            elif ch_type in ["electric"]:
                ch = Electric()
            else:
                msg = "Channel type %s not supported"
                self.logger.error(msg, ch_type)
                raise ValueError(msg % ch_type)

            ch.from_dict(item)
            self._output_channels.append(ch)
