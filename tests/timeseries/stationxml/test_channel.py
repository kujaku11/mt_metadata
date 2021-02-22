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
from mt_metadata.utils import STATIONXML_01, STATIONXML_02
# =============================================================================

class TestParseSerialID(unittest.TestCase):
    """
    Test parsing a string that holdes the electrod serial ID numbers
    
    'positive: pid, negative: nid'
    """
    def setUp(self):
        self.converter = XMLChannelMTChannel()
        self.pid = "2004007"
        self.nid = "2004008"
        self.id_str = f"positive: {self.pid}, negative: {self.nid}"
        self.comma_only_str = f"{self.pid}, {self.nid}"
        self.generic_str = "basic"
        
    def test_parse(self):
        test_pid, test_nid = self.converter._parse_electrode_ids(self.id_str)
        self.assertEqual(test_pid, self.pid)
        self.assertEqual(test_nid, self.nid)
        
    def test_pares_comma_only(self):
        test_pid, test_nid = self.converter._parse_electrode_ids(self.comma_only_str)
        self.assertEqual(test_pid, self.pid)
        self.assertEqual(test_nid, self.nid)
        
    def test_pares_basic(self):
        test_pid, test_nid = self.converter._parse_electrode_ids(self.generic_str)
        self.assertEqual(test_pid, "basic")
        self.assertEqual(test_nid, "basic")
    

class TestXMLChannel02(unittest.TestCase):
    """
    Test reading XML channel to MT Channel
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.converter = XMLChannelMTChannel()
        self.maxDiff = None

    def test_channel_hx(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[0]
        mt_channel = self.converter.xml_to_mt(xml_channel)

        self.assertDictEqual(mt_channel.to_dict(),
                             {'magnetic': OrderedDict([('channel_number', None),
                                                       ('comments',
                                                        ', run_ids: a,b'),
                                                       ('component', 'hx'),
                                                       ('data_quality.rating.value', 0),
                                                       ('filter.applied',
                                                        [False]),
                                                       ('filter.name',
                                                        ['none']),
                                                       ('location.elevation',
                                                        887.775),
                                                       ('location.latitude',
                                                        35.1469128125),
                                                       ('location.longitude', -
                                                        117.160798541667),
                                                       ('measurement_azimuth',
                                                        11.8287420852694),
                                                       ('measurement_tilt', 0.0),
                                                       ('sample_rate', 1.0),
                                                       ('sensor.id', '1303-01'),
                                                       ('sensor.manufacturer',
                                                        'Barry Narod'),
                                                       ('sensor.model',
                                                        'fluxgate NIMS'),
                                                       ('sensor.type',
                                                        'Magnetometer'),
                                                       ('time_period.end',
                                                        '2020-06-25T17:57:40+00:00'),
                                                       ('time_period.start',
                                                        '2020-06-08T22:57:13+00:00'),
                                                       ('type', 'magnetic'),
                                                       ('units', 'nanotesla')])})

    def test_channel_hy(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[1]
        mt_channel = self.converter.xml_to_mt(xml_channel)

        self.assertDictEqual(mt_channel.to_dict(),
                             {'magnetic': OrderedDict([('channel_number', None),
                                                       ('comments',
                                                        ', run_ids: a,b'),
                                                       ('component', 'hy'),
                                                       ('data_quality.rating.value', 0),
                                                       ('filter.applied',
                                                        [False]),
                                                       ('filter.name',
                                                        ['none']),
                                                       ('location.elevation',
                                                        887.775),
                                                       ('location.latitude',
                                                        35.1469128125),
                                                       ('location.longitude', -
                                                        117.160798541667),
                                                       ('measurement_azimuth',
                                                        101.828742085269),
                                                       ('measurement_tilt', 0.0),
                                                       ('sample_rate', 1.0),
                                                       ('sensor.id', '1303-01'),
                                                       ('sensor.manufacturer',
                                                        'Barry Narod'),
                                                       ('sensor.model',
                                                        'fluxgate NIMS'),
                                                       ('sensor.type',
                                                        'Magnetometer'),
                                                       ('time_period.end',
                                                        '2020-06-25T17:57:40+00:00'),
                                                       ('time_period.start',
                                                        '2020-06-08T22:57:13+00:00'),
                                                       ('type', 'magnetic'),
                                                       ('units', 'nanotesla')])})

    def test_channel_hz(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[2]
        mt_channel = self.converter.xml_to_mt(xml_channel)

        self.assertDictEqual(mt_channel.to_dict(),
                             {'magnetic': OrderedDict([('channel_number', None),
              ('comments', ', run_ids: a,b'),
              ('component', 'hz'),
              ('data_quality.rating.value', 0),
              ('filter.applied', [False]),
              ('filter.name', ['none']),
              ('location.elevation', 887.775),
              ('location.latitude', 35.1469128125),
              ('location.longitude', -117.160798541667),
              ('measurement_azimuth', 0.0),
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
        
# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()