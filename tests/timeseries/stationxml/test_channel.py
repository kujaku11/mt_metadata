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

    def test_channel_hy(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[0]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: []"),
                        ("component", "hy"),
                        ("data_quality.rating.value", 0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("location.elevation", 329.4),
                        ("location.latitude", 37.633351),
                        ("location.longitude", -121.468382),
                        ("measurement_azimuth", 103.2),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "2593"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-07-13T21:46:12+00:00"),
                        ("time_period.start", "2020-06-02T18:41:43+00:00"),
                        ("type", "magnetic"),
                        ("units", "nanotesla"),
                    ]
                )
            },
        )

    def test_channel_ey(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[1]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "electric": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: []"),
                        ("component", "ey"),
                        ("data_quality.rating.value", 0),
                        ("dipole_length", 92.0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("measurement_azimuth", 103.2),
                        ("measurement_tilt", 0.0),
                        ("negative.elevation", 329.4),
                        ("negative.id", "2004020"),
                        ("negative.latitude", 37.633351),
                        ("negative.longitude", -121.468382),
                        ("negative.manufacturer", "Oregon State University"),
                        ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("negative.type", "electrode"),
                        ("positive.elevation", 329.4),
                        ("positive.id", "200402F"),
                        ("positive.latitude", 37.633351),
                        ("positive.longitude", -121.468382),
                        ("positive.manufacturer", "Oregon State University"),
                        ("positive.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("positive.type", "electrode"),
                        ("sample_rate", 1.0),
                        ("time_period.end", "2020-07-13T21:46:12+00:00"),
                        ("time_period.start", "2020-06-02T18:41:43+00:00"),
                        ("type", "electric"),
                        ("units", "millivolts per kilometer"),
                    ]
                )
            },
        )


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

        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "hx"),
                        ("data_quality.rating.value", 0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("location.elevation", 887.775),
                        ("location.latitude", 35.1469128125),
                        ("location.longitude", -117.160798541667),
                        ("measurement_azimuth", 11.8287420852694),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "1303-01"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "magnetic"),
                        ("units", "nanotesla"),
                    ]
                )
            },
        )

    def test_channel_hy(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[1]
        mt_channel = self.converter.xml_to_mt(xml_channel)

        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "hy"),
                        ("data_quality.rating.value", 0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("location.elevation", 887.775),
                        ("location.latitude", 35.1469128125),
                        ("location.longitude", -117.160798541667),
                        ("measurement_azimuth", 101.828742085269),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "1303-01"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "magnetic"),
                        ("units", "nanotesla"),
                    ]
                )
            },
        )

    def test_channel_hz(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[2]
        mt_channel = self.converter.xml_to_mt(xml_channel)

        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "hz"),
                        ("data_quality.rating.value", 0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("location.elevation", 887.775),
                        ("location.latitude", 35.1469128125),
                        ("location.longitude", -117.160798541667),
                        ("measurement_azimuth", 0.0),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "1303-01"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "magnetic"),
                        ("units", "nanotesla"),
                    ]
                )
            },
        )

    def test_channel_ex(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[3]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "electric": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "ex"),
                        ("data_quality.rating.value", 0),
                        ("dipole_length", 94.0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("measurement_azimuth", 11.8287420852694),
                        ("measurement_tilt", 0.0),
                        ("negative.elevation", 887.775),
                        ("negative.id", "2004008"),
                        ("negative.latitude", 35.1469128125),
                        ("negative.longitude", -117.160798541667),
                        ("negative.manufacturer", "Oregon State University"),
                        ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("negative.type", "electrode"),
                        ("positive.elevation", 887.775),
                        ("positive.id", "2004007"),
                        ("positive.latitude", 35.1469128125),
                        ("positive.longitude", -117.160798541667),
                        ("positive.manufacturer", "Oregon State University"),
                        ("positive.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("positive.type", "electrode"),
                        ("sample_rate", 1.0),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "electric"),
                        ("units", "millivolts per kilometer"),
                    ]
                )
            },
        )

    def test_channel_ey(self):
        xml_channel = self.inventory.networks[0].stations[0].channels[4]
        mt_channel = self.converter.xml_to_mt(xml_channel)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "electric": OrderedDict(
                    [
                        ("channel_number", None),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "ey"),
                        ("data_quality.rating.value", 0),
                        ("dipole_length", 94.0),
                        ("filter.applied", [False]),
                        ("filter.name", ["none"]),
                        ("measurement_azimuth", 101.828742085269),
                        ("measurement_tilt", 0.0),
                        ("negative.elevation", 887.775),
                        ("negative.id", "2004004"),
                        ("negative.latitude", 35.1469128125),
                        ("negative.longitude", -117.160798541667),
                        ("negative.manufacturer", "Oregon State University"),
                        ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("negative.type", "electrode"),
                        ("positive.elevation", 887.775),
                        ("positive.id", "2004002"),
                        ("positive.latitude", 35.1469128125),
                        ("positive.longitude", -117.160798541667),
                        ("positive.manufacturer", "Oregon State University"),
                        ("positive.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("positive.type", "electrode"),
                        ("sample_rate", 1.0),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "electric"),
                        ("units", "millivolts per kilometer"),
                    ]
                )
            },
        )


class TestMTChannelToXML01HY(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[0]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertNotEqual(
            self.base_xml_channel.alternate_code, self.test_xml_channel.alternate_code
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)


class TestMTChannelToXML01EX(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[1]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E        self.assertNotEqual(self.base_xml_channel.code,
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertNotEqual(
            self.base_xml_channel.alternate_code, self.test_xml_channel.alternate_code
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)


class TestMTChannelToXML02HX(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[0]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E        self.assertNotEqual(self.base_xml_channel.code,
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertEqual(
            self.base_xml_channel.alternate_code.lower(),
            self.test_xml_channel.alternate_code.lower(),
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)

    def test_comments(self):
        for comment_base, comment_test in zip(
            self.base_xml_channel.comments, self.test_xml_channel.comments
        ):
            self.assertEqual(comment_base.value, comment_test.value)
            self.assertEqual(comment_base.subject, comment_test.subject)


class TestMTChannelToXML02HY(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[1]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E        self.assertNotEqual(self.base_xml_channel.code,
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertEqual(
            self.base_xml_channel.alternate_code.lower(),
            self.test_xml_channel.alternate_code.lower(),
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)

    def test_comments(self):
        for comment_base, comment_test in zip(
            self.base_xml_channel.comments, self.test_xml_channel.comments
        ):
            self.assertEqual(comment_base.value, comment_test.value)
            self.assertEqual(comment_base.subject, comment_test.subject)


class TestMTChannelToXML02HZ(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[2]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E        self.assertNotEqual(self.base_xml_channel.code,
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertEqual(
            self.base_xml_channel.alternate_code.lower(),
            self.test_xml_channel.alternate_code.lower(),
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)

    def test_comments(self):
        for comment_base, comment_test in zip(
            self.base_xml_channel.comments, self.test_xml_channel.comments
        ):
            self.assertEqual(comment_base.value, comment_test.value)
            self.assertEqual(comment_base.subject, comment_test.subject)


class TestMTChannelToXML02EX(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[3]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E        self.assertNotEqual(self.base_xml_channel.code,
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertEqual(
            self.base_xml_channel.alternate_code.lower(),
            self.test_xml_channel.alternate_code.lower(),
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)

    def test_comments(self):
        for comment_base, comment_test in zip(
            self.base_xml_channel.comments, self.test_xml_channel.comments
        ):
            self.assertEqual(comment_base.value, comment_test.value)
            self.assertEqual(comment_base.subject, comment_test.subject)


class TestMTChannelToXML02EY(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[4]

        self.converter = XMLChannelMTChannel()
        self.mt_channel = self.converter.xml_to_mt(self.base_xml_channel)
        self.test_xml_channel = self.converter.mt_to_xml(self.mt_channel)

    def test_location(self):
        self.assertEqual(self.base_xml_channel.latitude, self.test_xml_channel.latitude)
        self.assertEqual(
            self.base_xml_channel.longitude, self.test_xml_channel.longitude
        )
        self.assertEqual(
            self.base_xml_channel.elevation, self.test_xml_channel.elevation
        )
        self.assertEqual(self.base_xml_channel.depth, self.test_xml_channel.depth)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_channel.start_date, self.test_xml_channel.start_date
        )
        self.assertEqual(self.base_xml_channel.end_date, self.test_xml_channel.end_date)

    def test_code(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E        self.assertNotEqual(self.base_xml_channel.code,
        self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)
        self.assertEqual(
            self.base_xml_channel.alternate_code.lower(),
            self.test_xml_channel.alternate_code.lower(),
        )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type, self.test_xml_channel.sensor.type
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model, self.test_xml_channel.sensor.model
        )
        self.assertEqual(
            self.base_xml_channel.sensor.manufacturer,
            self.test_xml_channel.sensor.manufacturer,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.serial_number,
            self.test_xml_channel.sensor.serial_number,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.description,
            self.test_xml_channel.sensor.description,
        )

    def test_units(self):
        self.assertEqual(
            self.base_xml_channel.calibration_units,
            self.test_xml_channel.calibration_units,
        )
        self.assertEqual(
            self.base_xml_channel.calibration_units_description,
            self.test_xml_channel.calibration_units_description,
        )

    def test_sample_rate(self):
        self.assertEqual(
            self.base_xml_channel.sample_rate, self.test_xml_channel.sample_rate
        )

    def test_azimuth(self):
        self.assertEqual(self.base_xml_channel.azimuth, self.test_xml_channel.azimuth)
        self.assertEqual(self.base_xml_channel.dip, self.test_xml_channel.dip)

    def test_types(self):
        self.assertEqual(self.base_xml_channel.types, self.test_xml_channel.types)

    def test_comments(self):
        for comment_base, comment_test in zip(
            self.base_xml_channel.comments, self.test_xml_channel.comments
        ):
            self.assertEqual(comment_base.value, comment_test.value)
            self.assertEqual(comment_base.subject, comment_test.subject)


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
