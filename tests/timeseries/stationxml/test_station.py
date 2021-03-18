# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:58:11 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest
from collections import OrderedDict

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLStationMTStation
from tests import STATIONXML_01, STATIONXML_02


class TestReadXMLStation01(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.xml_station = self.inventory.networks[0].stations[0]

        self.converter = XMLStationMTStation()
        self.mt_station = self.converter.xml_to_mt(self.xml_station)

    def test_time_period(self):
        self.assertEqual(self.mt_station.time_period.start, "2020-06-02T18:41:43+00:00")
        self.assertEqual(self.mt_station.time_period.end, "2020-07-13T21:46:12+00:00")

    def test_code(self):
        self.assertEqual(self.mt_station.fdsn.id, "CAS04")
        self.assertEqual(self.mt_station.id, "CAS04")

    def test_location(self):
        self.assertEqual(self.mt_station.location.latitude, 37.633351)
        self.assertEqual(self.mt_station.location.longitude, -121.468382)
        self.assertEqual(self.mt_station.location.elevation, 329.3875)

    def test_geographic_name(self):
        self.assertEqual(self.mt_station.geographic_name, "Corral Hollow, CA, USA")

    def test_run_list(self):
        self.assertEqual(self.mt_station.run_list, [])


class TestMTStationToXML01(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.base_xml_station = self.inventory.networks[0].stations[0]

        self.converter = XMLStationMTStation()
        self.mt_station = self.converter.xml_to_mt(self.base_xml_station)
        self.test_xml_station = self.converter.mt_to_xml(self.mt_station)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_station.start_date, self.test_xml_station.start_date
        )
        self.assertEqual(self.base_xml_station.end_date, self.test_xml_station.end_date)

    def test_code(self):
        self.assertEqual(self.base_xml_station.code, self.test_xml_station.code)
        self.assertEqual(
            self.base_xml_station.alternate_code, self.test_xml_station.alternate_code
        )

    def test_location(self):
        self.assertEqual(self.base_xml_station.latitude, self.test_xml_station.latitude)
        self.assertEqual(
            self.base_xml_station.longitude, self.test_xml_station.longitude
        )
        self.assertEqual(
            self.base_xml_station.elevation, self.test_xml_station.elevation
        )

    def test_site(self):
        self.assertEqual(
            self.base_xml_station.site.name, self.test_xml_station.site.name
        )


class TestReadXMLStation02(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.xml_station = self.inventory.networks[0].stations[0]

        self.converter = XMLStationMTStation()
        self.mt_station = self.converter.xml_to_mt(self.xml_station)

    def test_time_period(self):
        self.assertEqual(self.mt_station.time_period.start, "2020-06-08T22:57:13+00:00")
        self.assertEqual(self.mt_station.time_period.end, "2020-07-17T21:15:32+00:00")

    def test_code(self):
        self.assertEqual(self.mt_station.fdsn.id, "REW09")
        self.assertEqual(self.mt_station.id, "REW09")

    def test_location(self):
        self.assertEqual(self.mt_station.location.latitude, 35.1469128125)
        self.assertEqual(self.mt_station.location.longitude, -117.160798541667)
        self.assertEqual(self.mt_station.location.elevation, 887.775)

    def test_geographic_name(self):
        self.assertEqual(self.mt_station.geographic_name, "Opal Mountain, CA, USA")

    def test_provenance(self):
        self.assertEqual(
            self.mt_station.provenance.software.author, "Anna Kelbert, USGS"
        )
        self.assertEqual(self.mt_station.provenance.software.name, "mth5_metadata.m")
        self.assertEqual(self.mt_station.provenance.software.version, "2021-02-01")

    def test_declination(self):
        self.assertEqual(self.mt_station.location.declination.value, -666)
        self.assertEqual(self.mt_station.location.declination.model, "IGRF-13")
        self.assertEqual(
            self.mt_station.location.declination.comments, "igrf.m by Drew Compston"
        )

    def test_orientation(self):
        self.assertEqual(self.mt_station.orientation.method, "compass")
        self.assertEqual(self.mt_station.orientation.reference_frame, "geographic")

    def test_run_list(self):
        self.assertEqual(self.mt_station.run_list, ["a", "b", "c", "d", "e"])

    def test_data_type(self):
        self.assertEqual(self.mt_station.data_type, "MT")

    def test_run_a(self):
        base_run_a = {
            "run": OrderedDict(
                [
                    ("acquired_by.author", "Kristin Pratscher"),
                    (
                        "acquired_by.comments",
                        (
                            "X array at 0 and 90 degrees. Site i rocky drainage basin proximal "
                            "to basalt lava flows. Ln"
                        ),
                    ),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", []),
                    ("channels_recorded_magnetic", []),
                    ("comments", "author: machine generated, comments: "),
                    ("data_logger.firmware.author", "Barry Narod"),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", ""),
                    ("data_logger.id", "2612-09"),
                    ("data_logger.manufacturer", "Barry Narod"),
                    ("data_logger.model", "NIMS"),
                    ("data_logger.power_source.type", "battery"),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", "GPS"),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", None),
                    ("data_type", "LP"),
                    ("id", "a"),
                    ("metadata_by.author", "Jade Crosbie"),
                    ("metadata_by.comments", ""),
                    ("sample_rate", None),
                    ("time_period.end", "2020-06-08T23:54:50+00:00"),
                    ("time_period.start", "2020-06-08T22:57:13+00:00"),
                ]
            )
        }
        run_a = self.mt_station.get_run("a")
        self.assertDictEqual(base_run_a, run_a.to_dict())

    def test_run_b(self):
        base_run_b = {
            "run": OrderedDict(
                [
                    ("acquired_by.author", "Kristin Pratscher"),
                    (
                        "acquired_by.comments",
                        (
                            "X array a 0 and 90 degreest. Site in rocky drainage basin proximal "
                            "to basalt lava flows. L"
                        ),
                    ),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", []),
                    ("channels_recorded_magnetic", []),
                    (
                        "comments",
                        (
                            "author: machine generated, comments: A.Kelbert--Gap and a spike"
                            " 726 secs into the run. Poor quality data after this event. "
                            "However, timing before and after the gap verified against CAV09."
                        ),
                    ),
                    ("data_logger.firmware.author", "Barry Narod"),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", ""),
                    ("data_logger.id", "2612-09"),
                    ("data_logger.manufacturer", "Barry Narod"),
                    ("data_logger.model", "NIMS"),
                    ("data_logger.power_source.type", "battery"),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", "GPS"),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", None),
                    ("data_type", "LP"),
                    ("id", "b"),
                    ("metadata_by.author", "Jade Crosbie; Anna Kelbert"),
                    (
                        "metadata_by.comments",
                        (
                            "A.Kelbert- Gap and a spike 726 secs into the run. Poor quality "
                            "data after this event. However, timing before and after the gap "
                            "verified against CAV09."
                        ),
                    ),
                    ("sample_rate", None),
                    ("time_period.end", "2020-06-25T17:57:40+00:00"),
                    ("time_period.start", "2020-06-09T00:08:03+00:00"),
                ]
            )
        }

        run_b = self.mt_station.get_run("b")
        self.assertDictEqual(base_run_b, run_b.to_dict())

    def test_run_c(self):
        base_run_c = {
            "run": OrderedDict(
                [
                    ("acquired_by.author", "Kristin Pratscher"),
                    (
                        "acquired_by.comments",
                        (
                            "X array at 0 and 90 degrees. Site in rocky drainage basin proximal"
                            " to basalt lava flows. Li"
                        ),
                    ),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", []),
                    ("channels_recorded_magnetic", []),
                    ("comments", "author: machine generated, comments: "),
                    ("data_logger.firmware.author", "Barry Narod"),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", ""),
                    ("data_logger.id", "2612-09"),
                    ("data_logger.manufacturer", "Barry Narod"),
                    ("data_logger.model", "NIMS"),
                    ("data_logger.power_source.type", "battery"),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", "GPS"),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", None),
                    ("data_type", "LP"),
                    ("id", "c"),
                    ("metadata_by.author", "Jade Crosbie"),
                    ("metadata_by.comments", ""),
                    ("sample_rate", None),
                    ("time_period.end", "2020-07-04T01:16:15+00:00"),
                    ("time_period.start", "2020-06-25T19:57:57+00:00"),
                ]
            )
        }

        run_c = self.mt_station.get_run("c")
        self.assertDictEqual(base_run_c, run_c.to_dict())

    def test_run_d(self):
        base_run_d = {
            "run": OrderedDict(
                [
                    ("acquired_by.author", "Kristin Pratscher"),
                    (
                        "acquired_by.comments",
                        (
                            "Replaced mag cable & NIMS. X array at 0 and 90 degrees. Site in"
                            " rocky drainage basin proxim"
                        ),
                    ),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", []),
                    ("channels_recorded_magnetic", []),
                    ("comments", "author: machine generated, comments: "),
                    ("data_logger.firmware.author", "Barry Narod"),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", ""),
                    ("data_logger.id", "2485"),
                    ("data_logger.manufacturer", "Barry Narod"),
                    ("data_logger.model", "NIMS"),
                    ("data_logger.power_source.type", "battery"),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", "GPS"),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", None),
                    ("data_type", "LP"),
                    ("id", "d"),
                    ("metadata_by.author", "Jade Crosbie"),
                    ("metadata_by.comments", ""),
                    ("sample_rate", None),
                    ("time_period.end", "2020-07-04T03:07:30+00:00"),
                    ("time_period.start", "2020-07-04T02:59:02+00:00"),
                ]
            )
        }

        run_d = self.mt_station.get_run("d")
        self.assertDictEqual(base_run_d, run_d.to_dict())

    def test_run_e(self):
        base_run_e = {
            "run": OrderedDict(
                [
                    ("acquired_by.author", "Kristin Pratscher"),
                    (
                        "acquired_by.comments",
                        (
                            "Replaced mag cable & NIMS. MX array at 0 and 90 degrees. Site "
                            "in rocky drainage basin proxim"
                        ),
                    ),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", []),
                    ("channels_recorded_magnetic", []),
                    ("comments", "author: machine generated, comments: "),
                    ("data_logger.firmware.author", "Barry Narod"),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", ""),
                    ("data_logger.id", "2485"),
                    ("data_logger.manufacturer", "Barry Narod"),
                    ("data_logger.model", "NIMS"),
                    ("data_logger.power_source.type", "battery"),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", "GPS"),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", None),
                    ("data_type", "LP"),
                    ("id", "e"),
                    ("metadata_by.author", "Jade Crosbie"),
                    ("metadata_by.comments", ""),
                    ("sample_rate", None),
                    ("time_period.end", "2020-07-17T21:15:32+00:00"),
                    ("time_period.start", "2020-07-04T03:28:45+00:00"),
                ]
            )
        }

        run_e = self.mt_station.get_run("e")
        self.assertDictEqual(base_run_e, run_e.to_dict())


class TestMTStationToXML02(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_station = self.inventory.networks[0].stations[0]

        self.converter = XMLStationMTStation()
        self.mt_station = self.converter.xml_to_mt(self.base_xml_station)
        self.test_xml_station = self.converter.mt_to_xml(self.mt_station)

    def test_time_period(self):
        self.assertEqual(
            self.base_xml_station.start_date, self.test_xml_station.start_date
        )
        self.assertEqual(self.base_xml_station.end_date, self.test_xml_station.end_date)

    def test_code(self):
        self.assertEqual(self.base_xml_station.code, self.test_xml_station.code)
        # the code and alternate code are the same so removed redundancy
        self.assertNotEqual(
            self.base_xml_station.alternate_code, self.test_xml_station.alternate_code
        )

    def test_location(self):
        self.assertEqual(self.base_xml_station.latitude, self.test_xml_station.latitude)
        self.assertEqual(
            self.base_xml_station.longitude, self.test_xml_station.longitude
        )
        self.assertEqual(
            self.base_xml_station.elevation, self.test_xml_station.elevation
        )

    def test_site(self):
        self.assertEqual(
            self.base_xml_station.site.name, self.test_xml_station.site.name
        )

    def test_equipments(self):
        self.assertEquals(
            len(self.base_xml_station.equipments), len(self.test_xml_station.equipments)
        )
        for be, te in zip(
            self.base_xml_station.equipments, self.test_xml_station.equipments
        ):
            self.assertEqual(be.resource_id, te.resource_id)
            self.assertEqual(be.manufacturer, te.manufacturer)
            self.assertEqual(be.serial_number, te.serial_number)
            self.assertEqual(be.installation_date, te.installation_date)
            self.assertEqual(be.removal_date, te.removal_date)

    def test_comments(self):
        for bc in self.base_xml_station.comments:
            for tc in self.test_xml_station.comments:
                if bc.subject == tc.subject:
                    if bc.value:
                        bk, bv = self.converter.read_xml_comment(bc)
                        tk, tv = self.converter.read_xml_comment(tc)
                        self.assertEqual(bk, tk)
                        if isinstance(bv, dict):
                            for kk, vv in bv.items():
                                if vv not in ["", None]:
                                    self.assertEqual(tv[kk], vv)

                        else:
                            self.assertEqual(bv, tv)

                    continue


# =============================================================================
#     Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
