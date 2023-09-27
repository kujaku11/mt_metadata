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
from mt_metadata.transfer_functions.tf import Station

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
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.comments", "crushed it"),
                ("transfer_function.data_quality.flag", None),
                ("transfer_function.data_quality.good_from_period", 0.01),
                ("transfer_function.data_quality.good_to_period", 1000),
                ("transfer_function.data_quality.rating.author", "author"),
                ("transfer_function.data_quality.rating.method", "eye ball"),
                ("transfer_function.data_quality.rating.value", 5),
                ("transfer_function.data_quality.warnings", "60 hz"),
                ("transfer_function.id", "mt01_sr100"),
                ("transfer_function.processed_by.author", "name"),
                ("transfer_function.processed_by.comments", "took time"),
                ("transfer_function.processed_by.email", "email@email.com"),
                ("transfer_function.processed_date", "2023-01-01"),
                ("transfer_function.processing_parameters", ["param_01=10"]),
                (
                    "transfer_function.processing_type",
                    "robust remote reference",
                ),
                ("transfer_function.remote_references", ["mtrr"]),
                ("transfer_function.runs_processed", ["001"]),
                ("transfer_function.sign_convention", "exp(+i\omega t)"),
                ("transfer_function.software.author", "author"),
                (
                    "transfer_function.software.last_updated",
                    "1980-01-01T00:00:00+00:00",
                ),
                ("transfer_function.software.version", "1.0"),
                (
                    "transfer_function.units",
                    "millivolts per kilometer per nanotesla",
                ),
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


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
