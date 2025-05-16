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

import json
import unittest
from collections import OrderedDict
from operator import itemgetter

import pandas as pd

from mt_metadata.transfer_functions.tf import Auxiliary, Run


# =============================================================================
#
# =============================================================================
class TestRun(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.meta_dict = {
            "run": OrderedDict(
                [
                    ("acquired_by.author", "test"),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", ["ex", "ey"]),
                    ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
                    ("data_logger.firmware.author", None),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", None),
                    ("data_logger.id", None),
                    ("data_logger.manufacturer", None),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", None),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", "MT"),
                    ("data_type", "MT"),
                    ("id", "gv163a"),
                    ("metadata_by.author", "metadata_by.author"),
                    ("sample_rate", 1.0),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "2020-01-02T12:20:40.456000+00:00"),
                ]
            )
        }

        self.ex_dict = {
            "electric": OrderedDict(
                [
                    ("channel_id", "4.0"),
                    ("channel_number", 4),
                    ("component", "ex"),
                    ("contact_resistance.end", 11.1),
                    ("contact_resistance.start", 11.4),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("dipole_length", 55.0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("measurement_azimuth", 0.0),
                    ("measurement_tilt", 0.0),
                    ("negative.datum", "WGS84"),
                    ("negative.elevation", 0.0),
                    ("negative.id", None),
                    ("negative.latitude", 0.0),
                    ("negative.longitude", 0.0),
                    ("negative.manufacturer", None),
                    ("negative.type", None),
                    ("negative.x", 0.0),
                    ("negative.x2", 0.0),
                    ("negative.y", 0.0),
                    ("negative.y2", 0.0),
                    ("negative.z", 0.0),
                    ("negative.z2", 0.0),
                    ("positive.datum", "WGS84"),
                    ("positive.elevation", 0.0),
                    ("positive.id", None),
                    ("positive.latitude", 0.0),
                    ("positive.longitude", 0.0),
                    ("positive.manufacturer", None),
                    ("positive.type", None),
                    ("positive.x", 0.0),
                    ("positive.x2", 0.0),
                    ("positive.y", 0.0),
                    ("positive.y2", 0.0),
                    ("positive.z", 0.0),
                    ("positive.z2", 0.0),
                    ("sample_rate", 0.0),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("translated_azimuth", -12.5),
                    ("type", "electric"),
                    ("units", "millivolts"),
                ]
            )
        }

        self.ey_dict = {
            "electric": OrderedDict(
                [
                    ("channel_id", "5.0"),
                    ("channel_number", 5),
                    ("component", "ey"),
                    ("contact_resistance.end", 7.9),
                    ("contact_resistance.start", 12.6),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("dipole_length", 55.0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("measurement_azimuth", 90.0),
                    ("measurement_tilt", 0.0),
                    ("negative.datum", "WGS84"),
                    ("negative.elevation", 0.0),
                    ("negative.id", None),
                    ("negative.latitude", 0.0),
                    ("negative.longitude", 0.0),
                    ("negative.manufacturer", None),
                    ("negative.type", None),
                    ("negative.x", 0.0),
                    ("negative.x2", 0.0),
                    ("negative.y", 0.0),
                    ("negative.y2", 0.0),
                    ("negative.z", 0.0),
                    ("negative.z2", 0.0),
                    ("positive.datum", "WGS84"),
                    ("positive.elevation", 0.0),
                    ("positive.id", None),
                    ("positive.latitude", 0.0),
                    ("positive.longitude", 0.0),
                    ("positive.manufacturer", None),
                    ("positive.type", None),
                    ("positive.x", 0.0),
                    ("positive.x2", 0.0),
                    ("positive.y", 0.0),
                    ("positive.y2", 0.0),
                    ("positive.z", 0.0),
                    ("positive.z2", 0.0),
                    ("sample_rate", 0.0),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("translated_azimuth", 77.5),
                    ("type", "electric"),
                    ("units", "millivolts"),
                ]
            )
        }

        self.hx_dict = {
            "magnetic": OrderedDict(
                [
                    ("channel_id", "1.0"),
                    ("channel_number", 2284),
                    ("component", "hx"),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("location.elevation", 0.0),
                    ("location.latitude", 0.0),
                    ("location.longitude", 0.0),
                    ("location.x", 0.0),
                    ("location.y", 0.0),
                    ("location.z", 0.0),
                    ("measurement_azimuth", 0.0),
                    ("measurement_tilt", 0.0),
                    ("sample_rate", 0.0),
                    ("sensor.id", None),
                    ("sensor.manufacturer", None),
                    ("sensor.type", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("translated_azimuth", -12.5),
                    ("type", "magnetic"),
                    ("units", "nanotesla"),
                ]
            )
        }

        self.hy_dict = {
            "magnetic": OrderedDict(
                [
                    ("channel_id", "2.0"),
                    ("channel_number", 2294),
                    ("component", "hy"),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("location.elevation", 0.0),
                    ("location.latitude", 0.0),
                    ("location.longitude", 0.0),
                    ("location.x", 0.0),
                    ("location.y", 0.0),
                    ("location.z", 0.0),
                    ("measurement_azimuth", 90.0),
                    ("measurement_tilt", 0.0),
                    ("sample_rate", 0.0),
                    ("sensor.id", None),
                    ("sensor.manufacturer", None),
                    ("sensor.type", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("translated_azimuth", 77.5),
                    ("type", "magnetic"),
                    ("units", "nanotesla"),
                ]
            )
        }

        self.hz_dict = {
            "magnetic": OrderedDict(
                [
                    ("channel_id", "3.0"),
                    ("channel_number", 2304),
                    ("component", "hz"),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("location.elevation", 0.0),
                    ("location.latitude", 0.0),
                    ("location.longitude", 0.0),
                    ("location.x", 0.0),
                    ("location.y", 0.0),
                    ("location.z", 0.0),
                    ("measurement_azimuth", 0.0),
                    ("measurement_tilt", 90.0),
                    ("sample_rate", 0.0),
                    ("sensor.id", None),
                    ("sensor.manufacturer", None),
                    ("sensor.type", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("translated_azimuth", 0.0),
                    ("translated_tilt", 90.0),
                    ("type", "magnetic"),
                    ("units", "nanotesla"),
                ]
            )
        }

        self.rrhx_dict = {
            "magnetic": OrderedDict(
                [
                    ("channel_number", 0),
                    ("component", "rrhx"),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("location.elevation", 0.0),
                    ("location.latitude", 0.0),
                    ("location.longitude", 0.0),
                    ("location.x", 0.0),
                    ("location.y", 0.0),
                    ("location.z", 0.0),
                    ("measurement_azimuth", 0.0),
                    ("measurement_tilt", 0.0),
                    ("sample_rate", 0.0),
                    ("sensor.id", None),
                    ("sensor.manufacturer", None),
                    ("sensor.type", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("type", "magnetic"),
                    ("units", None),
                ]
            )
        }

        self.rrhx_dict = {
            "magnetic": OrderedDict(
                [
                    ("channel_number", 0),
                    ("component", "rrhy"),
                    ("data_quality.flag", 0),
                    ("data_quality.rating.value", 0),
                    ("filter.applied", [True]),
                    ("filter.name", ["none"]),
                    ("location.elevation", 0.0),
                    ("location.latitude", 0.0),
                    ("location.longitude", 0.0),
                    ("location.x", 0.0),
                    ("location.y", 0.0),
                    ("location.z", 0.0),
                    ("measurement_azimuth", 0.0),
                    ("measurement_tilt", 0.0),
                    ("sample_rate", 0.0),
                    ("sensor.id", None),
                    ("sensor.manufacturer", None),
                    ("sensor.type", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("type", "magnetic"),
                    ("units", None),
                ]
            )
        }

        self.temperature_dict = {
            "auxiliary": OrderedDict(
                [
                    ("channel_number", 0),
                    ("component", "temperature"),
                    ("data_quality.rating.value", 0),
                    ("filter.applied", [True]),
                    ("filter.name", []),
                    ("location.elevation", 0.0),
                    ("location.latitude", 0.0),
                    ("location.longitude", 0.0),
                    ("measurement_azimuth", 0.0),
                    ("measurement_tilt", 0.0),
                    ("sample_rate", 0.0),
                    ("sensor.id", None),
                    ("sensor.manufacturer", None),
                    ("sensor.type", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("type", "auxiliary"),
                    ("units", None),
                ]
            )
        }

        self.meta_dict = {
            "run": OrderedDict(sorted(self.meta_dict["run"].items(), key=itemgetter(0)))
        }
        self.run_object = Run()
        self.run_object.from_dict(self.meta_dict)

    def test_in_out_dict(self):
        self.assertDictEqual(self.meta_dict, self.run_object.to_dict())

    def test_in_out_series(self):
        run_series = pd.Series(self.meta_dict["run"])
        run_obj = Run()
        run_obj.from_series(run_series)
        self.assertDictEqual(self.meta_dict, run_obj.to_dict())

    def test_in_out_json_full(self):
        run_json = json.dumps(self.meta_dict)
        run_obj = Run()
        run_obj.from_json((run_json))
        self.assertDictEqual(self.meta_dict, run_obj.to_dict())

    def test_in_out_json_nested(self):
        run_json = self.run_object.to_json(nested=True)
        run_obj = Run()
        run_obj.from_json(run_json)
        with self.subTest("test_nested"):
            self.assertDictEqual(self.meta_dict, run_obj.to_dict())

    def test_start(self):
        self.run_object.time_period.start = "2020/01/02T12:20:40.4560Z"
        self.assertEqual(
            self.run_object.time_period.start, "2020-01-02T12:20:40.456000+00:00"
        )

        self.run_object.time_period.start = "01/02/20T12:20:40.4560"
        self.assertEqual(
            self.run_object.time_period.start, "2020-01-02T12:20:40.456000+00:00"
        )

    def test_end_date(self):
        self.run_object.time_period.end = "2020/01/02T12:20:40.4560Z"
        self.assertEqual(
            self.run_object.time_period.end, "2020-01-02T12:20:40.456000+00:00"
        )

        self.run_object.time_period.end = "01/02/20T12:20:40.4560"
        self.assertEqual(
            self.run_object.time_period.end, "2020-01-02T12:20:40.456000+00:00"
        )

    def test_n_channels(self):
        self.assertEqual(self.run_object.n_channels, 5)

    def test_add_channels(self):
        self.run_object.channels_recorded_auxiliary = ["temperature", "battery"]
        self.assertEqual(self.run_object.n_channels, 7)

    def test_channels(self):
        for comp in ["ex", "ey", "hx", "hy", "hz"]:
            with self.subTest(f"testing {comp}"):
                getattr(self.run_object, comp).from_dict(getattr(self, f"{comp}_dict"))
                ch = self.run_object.get_channel(comp)
                self.assertDictEqual(ch.to_dict(), getattr(self, f"{comp}_dict"))

    def test_auxiliary_channel(self):
        temp = Auxiliary()
        temp.from_dict(self.temperature_dict)
        self.run_object.add_channel(temp)

        with self.subTest("Has Channel"):
            self.assertTrue(self.run_object.has_channel(temp.component))

        with self.subTest("Dict Equal"):
            self.assertDictEqual(
                self.run_object.get_channel(temp.component).to_dict(),
                self.temperature_dict,
            )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
