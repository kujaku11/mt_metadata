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
import re
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import DataQuality, Filtered, Location, TimePeriod, Instrument, Fdsn
from mt_metadata.timeseries.filters import ChannelResponseFilter

# =============================================================================
attr_dict = get_schema("channel", SCHEMA_FN_PATHS)
dq_dict = get_schema("data_quality", SCHEMA_FN_PATHS)
dq_dict.add_dict(get_schema("rating", SCHEMA_FN_PATHS), "rating")
attr_dict.add_dict(dq_dict, "data_quality")
attr_dict.add_dict(get_schema("filtered", SCHEMA_FN_PATHS), "filter")
attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
attr_dict.add_dict(get_schema("instrument", SCHEMA_FN_PATHS), "sensor")
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
attr_dict.add_dict(
    get_schema("location", SCHEMA_FN_PATHS),
    "location",
    keys=["latitude", "longitude", "elevation"],
)
# =============================================================================
class Channel(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.type = "auxiliary"
        self.units = None
        self.channel_number = None
        self.channel_id = None
        self.comments = None
        self._component = None
        self.sample_rate = 0.0
        self.measurement_azimuth = 0.0
        self.measurement_tilt = 0.0
        self.data_quality = DataQuality()
        self.filter = Filtered()
        self.location = Location()
        self.time_period = TimePeriod()
        self.translated_azimuth = None
        self.translated_tilt = None
        self.sensor = Instrument()
        self.fdsn = Fdsn()
        self._ch_pattern = r"\w+"

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, value):
        if value is not None:
            value = value.lower()
            if re.match(self._ch_pattern, value):
                self._component = value
            else:
                msg = f"component {value} does not match expected pattern {self._ch_pattern}"
                self.logger.error(msg)
                raise ValueError(msg)
                
    def channel_response(self, filters_dict):
        """
        full channel response
        """
        
        mt_filter_list = []
        for name in self.filter.name:
            try:
                mt_filter = filters_dict[name]
                mt_filter_list.append(mt_filter)
            except KeyError:
                msg = f"Could not find {name} in filters dictionary, skipping"
                self.logger.error(msg)
                continue
        # compute instrument sensitivity and units in/out
        return ChannelResponseFilter(filters_list=mt_filter_list)
