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
import pytest
from collections import OrderedDict

try:
    from obspy import read_inventory
    from mt_metadata.timeseries.filters.obspy_stages import (
        create_filter_from_stage,
    )
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)
from mt_metadata.timeseries.stationxml import XMLChannelMTChannel
from mt_metadata import STATIONXML_01, STATIONXML_02


# =============================================================================


class TestParseSerialID(unittest.TestCase):
    """
    Test parsing a string that holdes the electrod serial ID numbers

    'positive: pid, negative: nid'
    """

    @classmethod
    def setUpClass(self):
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

    def test_parse_comma_only(self):
        test_pid, test_nid = self.converter._parse_electrode_ids(self.comma_only_str)
        self.assertEqual(test_pid, self.pid)
        self.assertEqual(test_nid, self.nid)

    def test_parse_basic(self):
        test_pid, test_nid = self.converter._parse_electrode_ids(self.generic_str)
        self.assertEqual(test_pid, "basic")
        self.assertEqual(test_nid, "basic")


class TestParseDipole(unittest.TestCase):
    """
    Test parsing a dipole length string
    """

    @classmethod
    def setUpClass(self):
        self.converter = XMLChannelMTChannel()
        self.dipole_length = 100.0
        self.dipole_str = f"{self.dipole_length} meters"

    def test_parse(self):
        d = self.converter._parse_dipole_length(self.dipole_str)
        self.assertEqual(d, self.dipole_length)


class TestXMLChannelTwoChannels(unittest.TestCase):
    """
    Test reading XML channel to MT Channel
    """

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.xml_hy = self.inventory.networks[0].stations[0].channels[0]
        self.xml_ey = self.inventory.networks[0].stations[0].channels[1]
        self.filters_dict = dict(
            [
                (c.name, c)
                for c in [
                    create_filter_from_stage(s)
                    for s in self.xml_hy.response.response_stages
                ]
            ]
        )
        self.converter = XMLChannelMTChannel()
        self.maxDiff = None

    def test_channel_hy(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_hy)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", 0),
                        ("comments", "run_ids: []"),
                        ("component", "hy"),
                        ("data_quality.rating.value", None),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "magnetic field 3 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (magnetic)"),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "hy time offset"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("h_field_max.end", 0.0),
                        ("h_field_max.start", 0.0),
                        ("h_field_min.end", 0.0),
                        ("h_field_min.start", 0.0),
                        ("location.datum", "WGS 84"),
                        ("location.elevation", 329.4),
                        ("location.latitude", 37.633351),
                        ("location.longitude", -121.468382),
                        ("measurement_azimuth", 103.2),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "2593"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.name", "NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-07-13T21:46:12+00:00"),
                        ("time_period.start", "2020-06-02T18:41:43+00:00"),
                        ("type", "magnetic"),
                        ("units", "digital counts"),
                    ]
                )
            },
        )

    def test_channel_ey(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_ey)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "electric": OrderedDict(
                    [
                        ("ac.end", 0.0),
                        ("ac.start", 0.0),
                        ("channel_number", 0),
                        ("comments", "run_ids: []"),
                        ("component", "ey"),
                        ("contact_resistance.end", 0.0),
                        ("contact_resistance.start", 0.0),
                        ("data_quality.rating.value", None),
                        ("dc.end", 0.0),
                        ("dc.start", 0.0),
                        ("dipole_length", 92.0),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "electric field 5 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "electric field 1 pole butterworth high-pass",
                                            ),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "mv/km to v/m"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v/m to v"),
                                            ("stage", 4),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (electric)"),
                                            ("stage", 5),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "electric time offset"),
                                            ("stage", 6),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("location.datum", "WGS 84"),
                        ("measurement_azimuth", 103.2),
                        ("measurement_tilt", 0.0),
                        ("negative.datum", "WGS 84"),
                        ("negative.elevation", 329.4),
                        ("negative.id", "2004020"),
                        ("negative.latitude", 37.633351),
                        ("negative.longitude", -121.468382),
                        ("negative.manufacturer", "Oregon State University"),
                        ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("negative.type", "electrode"),
                        ("positive.datum", "WGS 84"),
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
                        ("units", "digital counts"),
                    ]
                )
            },
        )


class TestXMLChannelSingleStation(unittest.TestCase):
    """
    Test reading XML channel to MT Channel
    """

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.xml_hx = self.inventory.networks[0].stations[0].channels[0]
        self.xml_hy = self.inventory.networks[0].stations[0].channels[1]
        self.xml_hz = self.inventory.networks[0].stations[0].channels[2]
        self.xml_ex = self.inventory.networks[0].stations[0].channels[3]
        self.xml_ey = self.inventory.networks[0].stations[0].channels[4]

        self.filters_dict = dict(
            [
                (c.name, c)
                for c in [
                    create_filter_from_stage(s)
                    for s in self.xml_hy.response.response_stages
                ]
            ]
        )
        self.converter = XMLChannelMTChannel()
        self.maxDiff = None

    def test_channel_hx(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_hx)

        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", 0),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "Hx"),
                        ("data_quality.rating.value", None),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "magnetic field 3 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (magnetic)"),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "hx time offset"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("h_field_max.end", 0.0),
                        ("h_field_max.start", 0.0),
                        ("h_field_min.end", 0.0),
                        ("h_field_min.start", 0.0),
                        ("location.datum", "WGS 84"),
                        ("location.elevation", 887.775),
                        ("location.latitude", 35.1469128125),
                        ("location.longitude", -117.160798541667),
                        ("measurement_azimuth", 11.8287420852694),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "1303-01"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.name", "NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "magnetic"),
                        ("units", "digital counts"),
                    ]
                )
            },
        )

    def test_channel_hy(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_hy)

        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", 0),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "Hy"),
                        ("data_quality.rating.value", None),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "magnetic field 3 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (magnetic)"),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "hy time offset"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("h_field_max.end", 0.0),
                        ("h_field_max.start", 0.0),
                        ("h_field_min.end", 0.0),
                        ("h_field_min.start", 0.0),
                        ("location.datum", "WGS 84"),
                        ("location.elevation", 887.775),
                        ("location.latitude", 35.1469128125),
                        ("location.longitude", -117.160798541667),
                        ("measurement_azimuth", 101.828742085269),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "1303-01"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.name", "NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "magnetic"),
                        ("units", "digital counts"),
                    ]
                )
            },
        )

    def test_channel_hz(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_hz)

        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "magnetic": OrderedDict(
                    [
                        ("channel_number", 0),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "Hz"),
                        ("data_quality.rating.value", None),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "magnetic field 3 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (magnetic)"),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "hz time offset"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("h_field_max.end", 0.0),
                        ("h_field_max.start", 0.0),
                        ("h_field_min.end", 0.0),
                        ("h_field_min.start", 0.0),
                        ("location.datum", "WGS 84"),
                        ("location.elevation", 887.775),
                        ("location.latitude", 35.1469128125),
                        ("location.longitude", -117.160798541667),
                        ("measurement_azimuth", 0.0),
                        ("measurement_tilt", 0.0),
                        ("sample_rate", 1.0),
                        ("sensor.id", "1303-01"),
                        ("sensor.manufacturer", "Barry Narod"),
                        ("sensor.model", "fluxgate NIMS"),
                        ("sensor.name", "NIMS"),
                        ("sensor.type", "Magnetometer"),
                        ("time_period.end", "2020-06-25T17:57:40+00:00"),
                        ("time_period.start", "2020-06-08T22:57:13+00:00"),
                        ("type", "magnetic"),
                        ("units", "digital counts"),
                    ]
                )
            },
        )

    def test_channel_ex(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_ex)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "electric": OrderedDict(
                    [
                        ("ac.end", 0.0),
                        ("ac.start", 0.0),
                        ("channel_number", 0),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "Ex"),
                        ("contact_resistance.end", 0.0),
                        ("contact_resistance.start", 0.0),
                        ("data_quality.rating.value", None),
                        ("dc.end", 0.0),
                        ("dc.start", 0.0),
                        ("dipole_length", 94.0),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "electric field 5 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "electric field 1 pole butterworth high-pass",
                                            ),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "mv/km to v/m"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v/m to v"),
                                            ("stage", 4),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (electric)"),
                                            ("stage", 5),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "electric time offset"),
                                            ("stage", 6),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("location.datum", "WGS 84"),
                        ("measurement_azimuth", 11.8287420852694),
                        ("measurement_tilt", 0.0),
                        ("negative.datum", "WGS 84"),
                        ("negative.elevation", 887.775),
                        ("negative.id", "2004008"),
                        ("negative.latitude", 35.1469128125),
                        ("negative.longitude", -117.160798541667),
                        ("negative.manufacturer", "Oregon State University"),
                        ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("negative.type", "electrode"),
                        ("positive.datum", "WGS 84"),
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
                        ("units", "digital counts"),
                    ]
                )
            },
        )

    def test_channel_ey(self):
        mt_channel, mt_filters = self.converter.xml_to_mt(self.xml_ey)
        self.assertDictEqual(
            mt_channel.to_dict(),
            {
                "electric": OrderedDict(
                    [
                        ("ac.end", 0.0),
                        ("ac.start", 0.0),
                        ("channel_number", 0),
                        ("comments", "run_ids: [a,b]"),
                        ("component", "Ey"),
                        ("contact_resistance.end", 0.0),
                        ("contact_resistance.start", 0.0),
                        ("data_quality.rating.value", None),
                        ("dc.end", 0.0),
                        ("dc.start", 0.0),
                        ("dipole_length", 94.0),
                        (
                            "filtered.filter_list",
                            [
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "electric field 5 pole butterworth low-pass",
                                            ),
                                            ("stage", 1),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            (
                                                "name",
                                                "electric field 1 pole butterworth high-pass",
                                            ),
                                            ("stage", 2),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "mv/km to v/m"),
                                            ("stage", 3),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v/m to v"),
                                            ("stage", 4),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "v to counts (electric)"),
                                            ("stage", 5),
                                        ]
                                    )
                                },
                                {
                                    "applied_filter": OrderedDict(
                                        [
                                            ("applied", True),
                                            ("name", "electric time offset"),
                                            ("stage", 6),
                                        ]
                                    )
                                },
                            ],
                        ),
                        ("location.datum", "WGS 84"),
                        ("measurement_azimuth", 101.828742085269),
                        ("measurement_tilt", 0.0),
                        ("negative.datum", "WGS 84"),
                        ("negative.elevation", 887.775),
                        ("negative.id", "2004004"),
                        ("negative.latitude", 35.1469128125),
                        ("negative.longitude", -117.160798541667),
                        ("negative.manufacturer", "Oregon State University"),
                        ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                        ("negative.type", "electrode"),
                        ("positive.datum", "WGS 84"),
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
                        ("units", "digital counts"),
                    ]
                )
            },
        )


class TestMTChannelToXML01HY(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[0]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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
        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, self.test_xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertNotEqual(
                self.base_xml_channel.alternate_code,
                self.test_xml_channel.alternate_code,
            )

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertNotEqual(
                self.base_xml_channel.alternate_code,
                xml_channel.alternate_code,
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[1]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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
            self.base_xml_channel.alternate_code,
            self.test_xml_channel.alternate_code,
        )

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertNotEqual(
                self.base_xml_channel.alternate_code,
                xml_channel.alternate_code,
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[0]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertEqual(
                self.base_xml_channel.alternate_code.lower(),
                xml_channel.alternate_code.lower(),
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[1]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertEqual(
                self.base_xml_channel.alternate_code.lower(),
                xml_channel.alternate_code.lower(),
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[2]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertEqual(
                self.base_xml_channel.alternate_code.lower(),
                xml_channel.alternate_code.lower(),
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[3]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertEqual(
                self.base_xml_channel.alternate_code.lower(),
                xml_channel.alternate_code.lower(),
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_channel = self.inventory.networks[0].stations[0].channels[4]

        self.converter = XMLChannelMTChannel()
        self.mt_channel, self.filters_dict = self.converter.xml_to_mt(
            self.base_xml_channel
        )
        self.test_xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict
        )

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

    def test_code_unforced(self):
        # the codes are not the same because the azimuth is more than 5 degrees from E
        xml_channel = self.converter.mt_to_xml(
            self.mt_channel, self.filters_dict, hard_code=False
        )

        with self.subTest(msg="Test Channel Code"):
            self.assertEqual(self.base_xml_channel.code, xml_channel.code)

        with self.subTest(msg="Test Channel Alternate Code"):
            self.assertEqual(
                self.base_xml_channel.alternate_code.lower(),
                xml_channel.alternate_code.lower(),
            )

    def test_sensor(self):
        self.assertEqual(
            self.base_xml_channel.sensor.type,
            self.test_xml_channel.sensor.type,
        )
        self.assertEqual(
            self.base_xml_channel.sensor.model,
            self.test_xml_channel.sensor.model,
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
            self.base_xml_channel.sample_rate,
            self.test_xml_channel.sample_rate,
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
    # TestMTChannelToXML01HY()
    unittest.main()
