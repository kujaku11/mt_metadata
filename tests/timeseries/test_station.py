# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 11:21:17 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================

import unittest
import json
import pandas as pd
from collections import OrderedDict
from operator import itemgetter
from mt_metadata.timeseries import Run, Station

# =============================================================================
#
# =============================================================================
class TestStation(unittest.TestCase):
    """
    test station metadata
    """

    def setUp(self):
        self.maxDiff = None
        self.station_object = Station()
        self.meta_dict = OrderedDict(
            [
                ("acquired_by.author", "name"),
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                ("comments", "comments"),
                ("data_type", "BBMT"),
                ("geographic_name", "here"),
                ("id", "mt01"),
                ("location.declination.epoch", "2019"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 10.0),
                ("location.elevation", 400.0),
                ("location.latitude", 40.0),
                ("location.longitude", -120.0),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", "compass"),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.comments", "failed"),
                ("provenance.archive.email", "email@email.com"),
                ("provenance.archive.name", "archive name"),
                ("provenance.archive.organization", "archive org"),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.author", "author"),
                ("provenance.creator.comments", "data comments"),
                ("provenance.creator.email", "email@email.com"),
                ("provenance.creator.organization", "org"),
                ("provenance.software.author", "author"),
                (
                    "provenance.software.last_updated",
                    "1980-01-01T00:00:00+00:00",
                ),
                ("provenance.software.name", "mt_metadata"),
                ("provenance.software.version", "0.2.12"),
                ("provenance.submitter.author", "author"),
                ("provenance.submitter.comments", "data comments"),
                ("provenance.submitter.email", "email@email.com"),
                ("release_license", "CC0-1.0"),
                ("run_list", ["001"]),
                ("time_period.end", "2020-01-02T12:20:40.456000+00:00"),
                ("time_period.start", "2020-01-02T12:20:40.456000+00:00"),
            ]
        )

    def test_in_out_dict(self):
        self.station_object.from_dict(self.meta_dict)
        for key, value_og in self.meta_dict.items():
            with self.subTest(f"{key}"):
                value_s = self.station_object.get_attr_from_name(key)
                self.assertEqual(value_og, value_s)

    def test_in_out_series(self):
        station_series = pd.Series(self.meta_dict)
        self.station_object.from_series(station_series)
        for key, value_og in self.meta_dict.items():
            with self.subTest(f"{key}"):
                value_s = self.station_object.get_attr_from_name(key)
                self.assertEqual(value_og, value_s)

    def test_in_out_json(self):
        station_json = json.dumps(self.meta_dict)
        self.station_object.from_json((station_json))
        for key, value_og in self.meta_dict.items():
            with self.subTest(f"{key}"):
                value_s = self.station_object.get_attr_from_name(key)
                self.assertEqual(value_og, value_s)

    def test_start(self):
        self.station_object.time_period.start = "2020/01/02T12:20:40.4560Z"
        self.assertEqual(
            self.station_object.time_period.start,
            "2020-01-02T12:20:40.456000+00:00",
        )

        self.station_object.time_period.start = "01/02/20T12:20:40.4560"
        self.assertEqual(
            self.station_object.time_period.start,
            "2020-01-02T12:20:40.456000+00:00",
        )

    def test_end_date(self):
        self.station_object.time_period.end = "2020/01/02T12:20:40.4560Z"
        self.assertEqual(
            self.station_object.time_period.end,
            "2020-01-02T12:20:40.456000+00:00",
        )

        self.station_object.time_period.end = "01/02/20T12:20:40.4560"
        self.assertEqual(
            self.station_object.time_period.end,
            "2020-01-02T12:20:40.456000+00:00",
        )

    def test_latitude(self):
        self.station_object.location.latitude = "40:10:05.123"
        self.assertAlmostEqual(
            self.station_object.location.latitude, 40.1680897, places=5
        )

    def test_longitude(self):
        self.station_object.location.longitude = "-115:34:24.9786"
        self.assertAlmostEqual(
            self.station_object.location.longitude, -115.57361, places=5
        )

    def test_declination(self):
        self.station_object.location.declination.value = "10.980"
        self.assertEqual(self.station_object.location.declination.value, 10.980)

    def test_set_runs_from_list(self):
        self.station_object.runs = [Run(id="one")]
        with self.subTest("length"):
            self.assertEqual(len(self.station_object), 1)
        with self.subTest("list equal"):
            self.assertListEqual(["one"], self.station_object.run_list)

    def test_set_runs_from_dict(self):
        self.station_object.runs = {"one": Run(id="one")}
        with self.subTest("length"):
            self.assertEqual(len(self.station_object), 1)
        with self.subTest("list equal"):
            self.assertListEqual(["one"], self.station_object.run_list)

    def test_set_runs_fail(self):
        def set_runs(value):
            self.station_object.runs = value

        with self.subTest("Fail from input int"):
            self.assertRaises(TypeError, set_runs, 10)

        with self.subTest("Fail from input list"):
            self.assertRaises(TypeError, set_runs, [Run(), Station()])

    def test_add_rns(self):
        station_02 = Station()
        station_02.runs.append(Run(id="two"))
        self.station_object.runs.append(Run(id="one"))
        self.station_object += station_02
        with self.subTest("length"):
            self.assertEqual(len(self.station_object), 2)
        with self.subTest("list equal"):
            self.assertListEqual(["one", "two"], self.station_object.run_list)

    def test_remove_runs(self):
        self.station_object.runs.append(Run(id="one"))
        self.station_object.remove_run("one")
        self.assertListEqual([], self.station_object.run_list)

    def test_update_time_period(self):
        r = Run(id="001")
        r.time_period.start = "2020-01-01T00:00:00"
        r.time_period.end = "2020-12-01T12:12:12"
        self.station_object.add_run(r)
        self.station_object.update_time_period()

        with self.subTest("Test new start"):
            self.assertEqual(
                self.station_object.time_period.start,
                "2020-01-01T00:00:00+00:00",
            )

        with self.subTest("Test new end"):
            self.assertEqual(
                self.station_object.time_period.end,
                "2020-12-01T12:12:12+00:00",
            )


class TestStationChannelsRecorded(unittest.TestCase):
    def setUp(self):
        self.station = Station()

    def test_full_channels(self):
        self.station.channels_recorded = ["Ex", "Ey", "Hx", "Hy"]
        self.assertListEqual(
            ["Ex", "Ey", "Hx", "Hy"], self.station.channels_recorded
        )

    def test_null(self):
        self.station.channels_recorded = None
        self.assertEqual([], self.station.channels_recorded)

    def test_fail(self):
        def set_channels(values):
            self.station.channels_recorded = values

        self.assertRaises(TypeError, set_channels, 10)

    def test_from_run(self):
        r = Run(id="666")
        r.channels_recorded_electric = ["ex", "ey"]

        r2 = Run(id="667")
        r.channels_recorded_magnetic = ["hx", "hy", "hz"]

        r3 = Run(id="668")
        r.channels_recorded_auxiliary = ["temperature", "voltage"]

        self.station.add_run(r)
        self.station.add_run(r2)
        self.station.add_run(r3)

        self.assertListEqual(
            sorted(["ex", "ey", "hx", "hy", "hz", "temperature", "voltage"]),
            self.station.channels_recorded,
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
