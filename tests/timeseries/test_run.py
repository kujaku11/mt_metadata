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
from mt_metadata.timeseries import Auxiliary, Electric, Magnetic, Run

# =============================================================================
#
# =============================================================================
class TestRun(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.meta_dict = {
            "run": {
                "acquired_by.author": "MT guru",
                "acquired_by.comments": "lazy",
                "channels_recorded_auxiliary": ["temperature"],
                "channels_recorded_electric": ["ex", "ey"],
                "channels_recorded_magnetic": ["hx", "hy", "hz"],
                "comments": "Cloudy solar panels failed",
                "data_logger.firmware.author": "MT instruments",
                "data_logger.firmware.name": "FSGMT",
                "data_logger.firmware.version": "12.120",
                "data_logger.id": "mt091",
                "data_logger.manufacturer": "T. Lurric",
                "data_logger.model": "Ichiban",
                "data_logger.power_source.comments": "rats",
                "data_logger.power_source.id": "12",
                "data_logger.power_source.type": "pb acid",
                "data_logger.power_source.voltage.end": 12.0,
                "data_logger.power_source.voltage.start": 14.0,
                "data_logger.timing_system.comments": "solid",
                "data_logger.timing_system.drift": 0.001,
                "data_logger.timing_system.type": "GPS",
                "data_logger.timing_system.uncertainty": 0.000001,
                "data_logger.type": "broadband",
                "data_type": "mt",
                "id": "mt01a",
                "provenance.comments": "provenance comments",
                "provenance.log": "provenance log",
                "metadata_by.author": "MT guru",
                "metadata_by.comments": "lazy",
                "sample_rate": 256.0,
                "time_period.end": "1980-01-01T00:00:00+00:00",
                "time_period.start": "1980-01-01T00:00:00+00:00",
            }
        }

        self.meta_dict = {
            "run": OrderedDict(
                sorted(self.meta_dict["run"].items(), key=itemgetter(0))
            )
        }
        self.run_object = Run()

    def test_in_out_dict(self):
        self.run_object.from_dict(self.meta_dict)
        self.assertDictEqual(self.meta_dict, self.run_object.to_dict())

    def test_in_out_series(self):
        run_series = pd.Series(self.meta_dict["run"])
        self.run_object.from_series(run_series)
        self.assertDictEqual(self.meta_dict, self.run_object.to_dict())

    def test_in_out_json(self):
        run_json = json.dumps(self.meta_dict)
        self.run_object.from_json((run_json))
        self.assertDictEqual(self.meta_dict, self.run_object.to_dict())

    def test_start(self):
        self.run_object.time_period.start = "2020/01/02T12:20:40.4560Z"
        with self.subTest("from Z time"):
            self.assertEqual(
                self.run_object.time_period.start,
                "2020-01-02T12:20:40.456000+00:00",
            )

        self.run_object.time_period.start = "01/02/20T12:20:40.4560"
        with self.subTest("from mixed"):
            self.assertEqual(
                self.run_object.time_period.start,
                "2020-01-02T12:20:40.456000+00:00",
            )

    def test_end_date(self):
        self.run_object.time_period.end = "2020/01/02T12:20:40.4560Z"
        with self.subTest("from Z time"):
            self.assertEqual(
                self.run_object.time_period.end,
                "2020-01-02T12:20:40.456000+00:00",
            )

        self.run_object.time_period.end = "01/02/20T12:20:40.4560"
        with self.subTest("from mixed"):
            self.assertEqual(
                self.run_object.time_period.end,
                "2020-01-02T12:20:40.456000+00:00",
            )

    def test_n_channels(self):
        self.run_object.from_dict(self.meta_dict)
        with self.subTest("n_channels"):
            self.assertEqual(self.run_object.n_channels, 6)
        with self.subTest("length"):
            self.assertEqual(len(self.run_object), 6)

    def test_set_channels(self):
        self.run_object.channels = [Electric(component="ez")]
        with self.subTest("length"):
            self.assertEqual(len(self.run_object), 1)
        with self.subTest("in list"):
            self.assertListEqual(["ez"], self.run_object.channels_recorded_all)

    def test_set_channels_fail(self):
        def set_channels(value):
            self.run_object.channels = value

        with self.subTest("fail from input int"):
            self.assertRaises(TypeError, set_channels, 10)
        with self.subTest("fail from mixed input"):
            self.assertRaises(TypeError, set_channels, [Run(), Electric()])

    def test_add_channels(self):
        run_02 = Run()
        run_02.channels.append(Electric(component="ex"))
        run_02.channels.append(Magnetic(component="hx"))
        run_02.channels.append(Auxiliary(component="temperature"))
        self.run_object.channels.append(Electric(component="ey"))
        self.run_object += run_02
        with self.subTest("length"):
            self.assertEqual(len(self.run_object), 4)
        with self.subTest("In list all"):
            self.assertListEqual(
                sorted(["ex", "ey", "hx", "temperature"]),
                sorted(self.run_object.channels_recorded_all),
            )
        with self.subTest("in list electric"):
            self.assertListEqual(
                sorted(["ex", "ey"]),
                self.run_object.channels_recorded_electric,
            )
        with self.subTest("in list magnetic"):
            self.assertListEqual(
                ["hx"], self.run_object.channels_recorded_magnetic
            )
        with self.subTest("in list auxiliary"):
            self.assertListEqual(
                ["temperature"], self.run_object.channels_recorded_auxiliary
            )

    def test_remove_channel(self):
        self.run_object.channels.append(Electric(component="ex"))
        self.run_object.remove_channel("ex")
        self.assertListEqual([], self.run_object.channels_recorded_all)

    def test_update_time_period(self):
        ch = Electric(component="ex")
        ch.time_period.start = "2020-01-01T00:00:00"
        ch.time_period.end = "2020-12-01T12:12:12"
        self.run_object.add_channel(ch)

        with self.subTest("Test new start"):
            self.assertEqual(
                self.run_object.time_period.start, "2020-01-01T00:00:00+00:00"
            )

        with self.subTest("Test new end"):
            self.assertEqual(
                self.run_object.time_period.end, "2020-12-01T12:12:12+00:00"
            )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
