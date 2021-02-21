# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 15:17:41 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import unittest
from collections import OrderedDict

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLChannelMTChannel
from tests import STATIONXML_01, STATIONXML_02
# =============================================================================

class TestXMLChannel(unittest.TestCase):
    """
    Test reading XML channel to MT Channel
    """
    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.converter = XMLChannelMTChannel() 
    
    def test_channel_hx(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[0]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        
        self.assertDictEqual(mt_channel.to_dict(),
                             {'magnetic': OrderedDict([('channel_number', None),
              ('comments', ', run_ids: a,b'),
              ('component', 'hx'),
              ('data_quality.rating.value', 0),
              ('filter.applied', [False]),
              ('filter.name', ['none']),
              ('location.elevation', 887.775),
              ('location.latitude', 35.1469128125),
              ('location.longitude', -117.160798541667),
              ('measurement_azimuth', 11.8287420852694),
              ('measurement_tilt', 0.0),
              ('sample_rate', 1.0),
              ('sensor.id', '1303-01'),
              ('sensor.manufacturer', 'Barry Narod'),
              ('sensor.model', 'fluxgate NIMS'),
              ('sensor.type', 'Magnetometer'),
              ('time_period.end', '2020-06-25T17:57:40+00:00'),
              ('time_period.start', '2020-06-08T22:57:13+00:00'),
              ('type', 'magnetic'),
              ('units', 'nanotesla')])})
        