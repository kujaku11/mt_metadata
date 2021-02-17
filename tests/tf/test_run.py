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
from mt_metadata.transfer_functions.tf import Run

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
                "ex.dipole_length": 0.0,
                "ey.dipole_length": 0.0,
                "id": "mt01a",
                "provenance.comments": "provenance comments",
                "provenance.log": "provenance log",
                "metadata_by.author": "MT guru",
                "metadata_by.comments": "lazy",
                "sample_rate": 256.0,
                "temperature.channel_number": None,
                "temperature.component": "temperature",
                "temperature.measurement_azimuth": 0.0,
                "temperature.sample_rate": 0.0,
                "temperature.type": "auxiliary",
                "temperature.units": None,
                "time_period.end": "1980-01-01T00:00:00+00:00",
                "time_period.start": "1980-01-01T00:00:00+00:00",
            }
        }

        self.meta_dict = {
            "run": OrderedDict(sorted(self.meta_dict["run"].items(), key=itemgetter(0)))
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
        survey_json = json.dumps(self.meta_dict)
        self.run_object.from_json((survey_json))
        self.assertDictEqual(self.meta_dict, self.run_object.to_dict())

        survey_json = self.run_object.to_json(nested=True)
        self.run_object.from_json(survey_json)
        self.assertDictEqual(self.meta_dict, self.run_object.to_dict())

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
        self.run_object.from_dict(self.meta_dict)
        self.assertEqual(self.run_object.n_channels, 6)

        self.run_object.channels_recorded_auxiliary = ["temperature", "battery"]
        self.assertEqual(self.run_object.n_channels, 7)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
