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
        test_pid, test_nid = self.converter._parse_electrode_ids(
            self.comma_only_str)
        self.assertEqual(test_pid, self.pid)
        self.assertEqual(test_nid, self.nid)

    def test_pares_basic(self):
        test_pid, test_nid = self.converter._parse_electrode_ids(
            self.generic_str)
        self.assertEqual(test_pid, "basic")
        self.assertEqual(test_nid, "basic")


class TestParseDipole(unittest.TestCase):
    """
    Test parsing a dipole length string
    """

    def setUp(self):
        self.converter = XMLChannelMTChannel()
        self.dipole_length = 100.0
        self.dipole_str = f"{self.dipole_length} meters"

    def test_parse(self):
        d = self.converter._parse_dipole_length(self.dipole_str)
        self.assertEqual(d, self.dipole_length)
        
class TestXMLChannel01(unittest.TestCase):
    """
    Test reading XML channel to MT Channel
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.converter = XMLChannelMTChannel()
        self.maxDiff = None

    def test_channel_hx(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[0]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(mt_channel.to_dict(),
                             {'magnetic': OrderedDict([('channel_number', None),
              ('comments', ', run_ids: '),
              ('component', None),
              ('data_quality.rating.value', 0),
              ('filter.applied', [False]),
              ('filter.name', ['none']),
              ('location.elevation', 329.4),
              ('location.latitude', 37.633351),
              ('location.longitude', -121.468382),
              ('measurement_azimuth', 103.2),
              ('measurement_tilt', 0.0),
              ('sample_rate', 1.0),
              ('sensor.id', '2593'),
              ('sensor.manufacturer', 'Barry Narod'),
              ('sensor.model', 'fluxgate NIMS'),
              ('sensor.type', 'Magnetometer'),
              ('time_period.end', '2020-07-13T21:46:12+00:00'),
              ('time_period.start', '2020-06-02T18:41:43+00:00'),
              ('type', 'magnetic'),
              ('units', 'nanotesla')])})
        
    def test_channel_ex(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[1]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(mt_channel.to_dict(),
                             {'electric': OrderedDict([('channel_number', None),
              ('comments', ', run_ids: '),
              ('component', None),
              ('data_quality.rating.value', 0),
              ('dipole_length', 92.0),
              ('filter.applied', [False]),
              ('filter.name', ['none']),
              ('measurement_azimuth', 103.2),
              ('measurement_tilt', 0.0),
              ('negative.elevation', 0.0),
              ('negative.id', '2004020'),
              ('negative.latitude', 0.0),
              ('negative.longitude', 0.0),
              ('negative.manufacturer', 'Oregon State University'),
              ('negative.model', 'Pb-PbCl2 kaolin gel Petiau 2 chamber type'),
              ('negative.type', 'electrode'),
              ('positive.elevation', 0.0),
              ('positive.id', '200402F'),
              ('positive.latitude', 0.0),
              ('positive.longitude', 0.0),
              ('positive.manufacturer', 'Oregon State University'),
              ('positive.model', 'Pb-PbCl2 kaolin gel Petiau 2 chamber type'),
              ('positive.type', 'electrode'),
              ('sample_rate', 1.0),
              ('time_period.end', '2020-07-13T21:46:12+00:00'),
              ('time_period.start', '2020-06-02T18:41:43+00:00'),
              ('type', 'electric'),
              ('units', 'millivolts per kilometer')])})


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
                                                       ('comments',
                                                        ', run_ids: a,b'),
                                                       ('component', 'hz'),
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
                                                       ('measurement_azimuth', 0.0),
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

    def test_channel_ex(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[3]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(mt_channel.to_dict(),
                             {'electric': OrderedDict([('channel_number', None),
                                                       ('comments',
                                                        ', run_ids: a,b'),
                                                       ('component', 'ex'),
                                                       ('data_quality.rating.value', 0),
                                                       ('dipole_length', 94.0),
                                                       ('filter.applied',
                                                        [False]),
                                                       ('filter.name',
                                                        ['none']),
                                                       ('measurement_azimuth',
                                                        11.8287420852694),
                                                       ('measurement_tilt', 0.0),
                                                       ('negative.elevation', 0.0),
                                                       ('negative.id', '2004008'),
                                                       ('negative.latitude', 0.0),
                                                       ('negative.longitude', 0.0),
                                                       ('negative.manufacturer',
                                                        'Oregon State University'),
                                                       ('negative.model',
                                                        'Pb-PbCl2 kaolin gel Petiau 2 chamber type'),
                                                       ('negative.type',
                                                        'electrode'),
                                                       ('positive.elevation', 0.0),
                                                       ('positive.id', '2004007'),
                                                       ('positive.latitude', 0.0),
                                                       ('positive.longitude', 0.0),
                                                       ('positive.manufacturer',
                                                        'Oregon State University'),
                                                       ('positive.model',
                                                        'Pb-PbCl2 kaolin gel Petiau 2 chamber type'),
                                                       ('positive.type',
                                                        'electrode'),
                                                       ('sample_rate', 1.0),
                                                       ('time_period.end',
                                                        '2020-06-25T17:57:40+00:00'),
                                                       ('time_period.start',
                                                        '2020-06-08T22:57:13+00:00'),
                                                       ('type', 'electric'),
                                                       ('units', 'millivolts per kilometer')])})

    def test_channel_ey(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[4]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(mt_channel.to_dict(),
                             {'electric': OrderedDict([('channel_number', None),
                                                       ('comments',
                                                        ', run_ids: a,b'),
                                                       ('component', 'ey'),
                                                       ('data_quality.rating.value', 0),
                                                       ('dipole_length', 94.0),
                                                       ('filter.applied',
                                                        [False]),
                                                       ('filter.name',
                                                        ['none']),
                                                       ('measurement_azimuth',
                                                        101.828742085269),
                                                       ('measurement_tilt', 0.0),
                                                       ('negative.elevation', 0.0),
                                                       ('negative.id', '2004004'),
                                                       ('negative.latitude', 0.0),
                                                       ('negative.longitude', 0.0),
                                                       ('negative.manufacturer',
                                                        'Oregon State University'),
                                                       ('negative.model',
                                                        'Pb-PbCl2 kaolin gel Petiau 2 chamber type'),
                                                       ('negative.type',
                                                        'electrode'),
                                                       ('positive.elevation', 0.0),
                                                       ('positive.id', '2004002'),
                                                       ('positive.latitude', 0.0),
                                                       ('positive.longitude', 0.0),
                                                       ('positive.manufacturer',
                                                        'Oregon State University'),
                                                       ('positive.model',
                                                        'Pb-PbCl2 kaolin gel Petiau 2 chamber type'),
                                                       ('positive.type',
                                                        'electrode'),
                                                       ('sample_rate', 1.0),
                                                       ('time_period.end',
                                                        '2020-06-25T17:57:40+00:00'),
                                                       ('time_period.start',
                                                        '2020-06-08T22:57:13+00:00'),
                                                       ('type', 'electric'),
                                                       ('units', 'millivolts per kilometer')])})


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
