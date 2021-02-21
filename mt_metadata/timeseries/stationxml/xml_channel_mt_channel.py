# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:14:41 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.timeseries.stationxml.fdsn_tools import (
    release_dict, read_channel_code, make_channel_code)

from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml.utils import BaseTranslator

from obspy.core import inventory

# =============================================================================


class XMLChannelMTChannel(BaseTranslator):
    """
    translate back and forth between StationXML Channel and MT Channel
    """

    def __init__(self):
        super().__init__()

        self.xml_translator.update(
            {
                "azimuth": "measurement_azimuth",
                "calibration_units": "units",
                "calibration_units_description": None,
                "comments": "comments",
                "clock_drift": None,
                "description": None,
                "dip": "measurement_tilt",
                "end_date": "time_period.end",
                "equipments": None,
                "pre_amplifier": None,
                "response": None,
                "latitude": "location.latitude",
                "longitude": "location.longitude",
                "elevation": "location.elevation",
                "sample_rate": "sample_rate",
                "sample_rate_ratio_number_samples": None,
                "sample_rate_ratio_number_seconds": None,
                "sensor": "special",
                "start_date": "time_period.start",
                "types": "special",
                "water_level": None,
            }
        )

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)

        self.mt_comments_list = [
            "run.id"
        ]

    def xml_to_mt(self, xml_channel):
        """
        Translate :class:`obspy.core.inventory.Channel` to 
        :class:`mt_metadata.timeseries.Channel`

        :param xml_channel: Obspy Channel object
        :type xml_channel: :class:`obspy.core.inventory.Channel`
        :returns: MT Channel
        :rtype: :class:`mt_metadata.timeseries.Channel`

        """

        if not isinstance(xml_channel, inventory.Channel):
            msg = f"Input must be obspy.core.inventory.Channel object not {type(xml_channel)}"
            self.logger.error(msg)
            raise TypeError(msg)
            
        ch_dict = read_channel_code(xml_channel.code)

        channel_code = make_channel_code(xml_channel)

        is_electric = xml_channel.type in ["electric"]
        if is_electric:
            mt_channel
        else:
            xml_channel = inventory.Channel(
                channel_code,
                location_code,
                xml_channel.location.latitude,
                xml_channel.location.longitude,
                xml_channel.location.elevation,
                xml_channel.location.elevation,
            )

        xml_channel.start_date = mt_channel.time_period.start
        xml_channel.end_date = mt_channel.time_period.end

    def mt_to_xml(self, mt_channel):
        """
        Translate :class:`obspy.core.inventory.Channel` to 
        :class:`mt_metadata.timeseries.Channel`

        :param xml_channel: Obspy Channel object
        :type xml_channel: :class:`obspy.core.inventory.Channel`
        :returns: MT Channel
        :rtype: :class:`mt_metadata.timeseries.Channel`

        """

        if not isinstance(mt_channel, (metadata.Electric, metadata.Magnetic, metadata.Auxiliary)):
            msg = f"Input must be mt_metadata.timeseries.Channel object not {type(mt_channel)}"
            self.logger.error(msg)
            raise TypeError(msg)

        location_code = get_location_code(mt_channel)
        channel_code = make_channel_code(mt_channel)

        is_electric = mt_channel.type in ["electric"]
        if is_electric:
            xml_channel = inventory.Channel(
                channel_code,
                location_code,
                mt_channel.positive.latitude,
                mt_channel.positive.longitude,
                mt_channel.positive.elevation,
                mt_channel.positive.elevation,
            )
        else:
            xml_channel = inventory.Channel(
                channel_code,
                location_code,
                mt_channel.location.latitude,
                mt_channel.location.longitude,
                mt_channel.location.elevation,
                mt_channel.location.elevation,
            )

    
        xml_channel.start_date = mt_channel.time_period.start
        xml_channel.end_date = mt_channel.time_period.end
