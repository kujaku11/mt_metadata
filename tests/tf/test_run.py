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
            "run": OrderedDict(
                [
                    ("acquired_by.author", None),
                    ("channels_recorded_auxiliary", []),
                    ("channels_recorded_electric", ["ex", "ey"]),
                    ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
                    ("data_logger.firmware.author", None),
                    (
                        "data_logger.firmware.last_updated",
                        "1980-01-01T00:00:00+00:00",
                    ),
                    ("data_logger.firmware.name", None),
                    ("data_logger.firmware.version", None),
                    ("data_logger.id", None),
                    ("data_logger.manufacturer", None),
                    ("data_logger.timing_system.drift", None),
                    ("data_logger.timing_system.type", None),
                    ("data_logger.timing_system.uncertainty", None),
                    ("data_logger.type", None),
                    ("data_type", None),
                    ("ex.channel_id", "4.0"),
                    ("ex.channel_number", 4),
                    ("ex.component", "ex"),
                    ("ex.contact_resistance.end", 11.1),
                    ("ex.contact_resistance.start", 11.4),
                    ("ex.data_quality.flag", 0),
                    ("ex.data_quality.rating.value", 0),
                    ("ex.dipole_length", 55.0),
                    ("ex.filter.applied", [False]),
                    ("ex.filter.name", ["none"]),
                    ("ex.measurement_azimuth", 0.0),
                    ("ex.measurement_tilt", 0.0),
                    ("ex.negative.datum", "WGS84"),
                    ("ex.negative.elevation", 0.0),
                    ("ex.negative.id", None),
                    ("ex.negative.latitude", 0.0),
                    ("ex.negative.longitude", 0.0),
                    ("ex.negative.manufacturer", None),
                    ("ex.negative.type", None),
                    ("ex.negative.x", 0.0),
                    ("ex.negative.x2", 0.0),
                    ("ex.negative.y", 0.0),
                    ("ex.negative.y2", 0.0),
                    ("ex.negative.z", 0.0),
                    ("ex.negative.z2", 0.0),
                    ("ex.positive.datum", "WGS84"),
                    ("ex.positive.elevation", 0.0),
                    ("ex.positive.id", None),
                    ("ex.positive.latitude", 0.0),
                    ("ex.positive.longitude", 0.0),
                    ("ex.positive.manufacturer", None),
                    ("ex.positive.type", None),
                    ("ex.positive.x", 0.0),
                    ("ex.positive.x2", 0.0),
                    ("ex.positive.y", 0.0),
                    ("ex.positive.y2", 0.0),
                    ("ex.positive.z", 0.0),
                    ("ex.positive.z2", 0.0),
                    ("ex.sample_rate", 0.0),
                    ("ex.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("ex.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("ex.translated_azimuth", -12.5),
                    ("ex.type", "electric"),
                    ("ex.units", "millivolts"),
                    ("ey.channel_id", "5.0"),
                    ("ey.channel_number", 5),
                    ("ey.component", "ey"),
                    ("ey.contact_resistance.end", 7.9),
                    ("ey.contact_resistance.start", 12.6),
                    ("ey.data_quality.flag", 0),
                    ("ey.data_quality.rating.value", 0),
                    ("ey.dipole_length", 55.0),
                    ("ey.filter.applied", [False]),
                    ("ey.filter.name", ["none"]),
                    ("ey.measurement_azimuth", 90.0),
                    ("ey.measurement_tilt", 0.0),
                    ("ey.negative.datum", "WGS84"),
                    ("ey.negative.elevation", 0.0),
                    ("ey.negative.id", None),
                    ("ey.negative.latitude", 0.0),
                    ("ey.negative.longitude", 0.0),
                    ("ey.negative.manufacturer", None),
                    ("ey.negative.type", None),
                    ("ey.negative.x", 0.0),
                    ("ey.negative.x2", 0.0),
                    ("ey.negative.y", 0.0),
                    ("ey.negative.y2", 0.0),
                    ("ey.negative.z", 0.0),
                    ("ey.negative.z2", 0.0),
                    ("ey.positive.datum", "WGS84"),
                    ("ey.positive.elevation", 0.0),
                    ("ey.positive.id", None),
                    ("ey.positive.latitude", 0.0),
                    ("ey.positive.longitude", 0.0),
                    ("ey.positive.manufacturer", None),
                    ("ey.positive.type", None),
                    ("ey.positive.x", 0.0),
                    ("ey.positive.x2", 0.0),
                    ("ey.positive.y", 0.0),
                    ("ey.positive.y2", 0.0),
                    ("ey.positive.z", 0.0),
                    ("ey.positive.z2", 0.0),
                    ("ey.sample_rate", 0.0),
                    ("ey.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("ey.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("ey.translated_azimuth", 77.5),
                    ("ey.type", "electric"),
                    ("ey.units", "millivolts"),
                    ("hx.channel_id", "1.0"),
                    ("hx.channel_number", 2284),
                    ("hx.component", "hx"),
                    ("hx.data_quality.flag", 0),
                    ("hx.data_quality.rating.value", 0),
                    ("hx.filter.applied", [False]),
                    ("hx.filter.name", ["none"]),
                    ("hx.location.elevation", 0.0),
                    ("hx.location.latitude", 0.0),
                    ("hx.location.longitude", 0.0),
                    ("hx.location.x", 0.0),
                    ("hx.location.y", 0.0),
                    ("hx.location.z", 0.0),
                    ("hx.measurement_azimuth", 0.0),
                    ("hx.measurement_tilt", 0.0),
                    ("hx.sample_rate", 0.0),
                    ("hx.sensor.id", None),
                    ("hx.sensor.manufacturer", None),
                    ("hx.sensor.type", None),
                    ("hx.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("hx.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("hx.translated_azimuth", -12.5),
                    ("hx.type", "magnetic"),
                    ("hx.units", "nanotesla"),
                    ("hy.channel_id", "2.0"),
                    ("hy.channel_number", 2294),
                    ("hy.component", "hy"),
                    ("hy.data_quality.flag", 0),
                    ("hy.data_quality.rating.value", 0),
                    ("hy.filter.applied", [False]),
                    ("hy.filter.name", ["none"]),
                    ("hy.location.elevation", 0.0),
                    ("hy.location.latitude", 0.0),
                    ("hy.location.longitude", 0.0),
                    ("hy.location.x", 0.0),
                    ("hy.location.y", 0.0),
                    ("hy.location.z", 0.0),
                    ("hy.measurement_azimuth", 90.0),
                    ("hy.measurement_tilt", 0.0),
                    ("hy.sample_rate", 0.0),
                    ("hy.sensor.id", None),
                    ("hy.sensor.manufacturer", None),
                    ("hy.sensor.type", None),
                    ("hy.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("hy.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("hy.translated_azimuth", 77.5),
                    ("hy.type", "magnetic"),
                    ("hy.units", "nanotesla"),
                    ("hz.channel_id", "3.0"),
                    ("hz.channel_number", 2304),
                    ("hz.component", "hz"),
                    ("hz.data_quality.flag", 0),
                    ("hz.data_quality.rating.value", 0),
                    ("hz.filter.applied", [False]),
                    ("hz.filter.name", ["none"]),
                    ("hz.location.elevation", 0.0),
                    ("hz.location.latitude", 0.0),
                    ("hz.location.longitude", 0.0),
                    ("hz.location.x", 0.0),
                    ("hz.location.y", 0.0),
                    ("hz.location.z", 0.0),
                    ("hz.measurement_azimuth", 0.0),
                    ("hz.measurement_tilt", 90.0),
                    ("hz.sample_rate", 0.0),
                    ("hz.sensor.id", None),
                    ("hz.sensor.manufacturer", None),
                    ("hz.sensor.type", None),
                    ("hz.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("hz.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("hz.translated_azimuth", 0.0),
                    ("hz.translated_tilt", 90.0),
                    ("hz.type", "magnetic"),
                    ("hz.units", "nanotesla"),
                    ("id", "gv163a"),
                    ("metadata_by.author", None),
                    ("rrhx.channel_number", None),
                    ("rrhx.component", None),
                    ("rrhx.data_quality.flag", 0),
                    ("rrhx.data_quality.rating.value", 0),
                    ("rrhx.filter.applied", [False]),
                    ("rrhx.filter.name", ["none"]),
                    ("rrhx.location.elevation", 0.0),
                    ("rrhx.location.latitude", 0.0),
                    ("rrhx.location.longitude", 0.0),
                    ("rrhx.location.x", 0.0),
                    ("rrhx.location.y", 0.0),
                    ("rrhx.location.z", 0.0),
                    ("rrhx.measurement_azimuth", 0.0),
                    ("rrhx.measurement_tilt", 0.0),
                    ("rrhx.sample_rate", 0.0),
                    ("rrhx.sensor.id", None),
                    ("rrhx.sensor.manufacturer", None),
                    ("rrhx.sensor.type", None),
                    ("rrhx.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("rrhx.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("rrhx.type", "magnetic"),
                    ("rrhx.units", None),
                    ("rrhy.channel_number", None),
                    ("rrhy.component", None),
                    ("rrhy.data_quality.flag", 0),
                    ("rrhy.data_quality.rating.value", 0),
                    ("rrhy.filter.applied", [False]),
                    ("rrhy.filter.name", ["none"]),
                    ("rrhy.location.elevation", 0.0),
                    ("rrhy.location.latitude", 0.0),
                    ("rrhy.location.longitude", 0.0),
                    ("rrhy.location.x", 0.0),
                    ("rrhy.location.y", 0.0),
                    ("rrhy.location.z", 0.0),
                    ("rrhy.measurement_azimuth", 0.0),
                    ("rrhy.measurement_tilt", 0.0),
                    ("rrhy.sample_rate", 0.0),
                    ("rrhy.sensor.id", None),
                    ("rrhy.sensor.manufacturer", None),
                    ("rrhy.sensor.type", None),
                    ("rrhy.time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("rrhy.time_period.start", "1980-01-01T00:00:00+00:00"),
                    ("rrhy.type", "magnetic"),
                    ("rrhy.units", None),
                    ("sample_rate", None),
                    ("temperature.channel_number", None),
                    ("temperature.component", None),
                    ("temperature.measurement_azimuth", 0.0),
                    ("temperature.measurement_tilt", 0.0),
                    ("temperature.sample_rate", 0.0),
                    ("temperature.type", "auxiliary"),
                    ("temperature.units", None),
                    ("time_period.end", "1980-01-01T00:00:00+00:00"),
                    ("time_period.start", "2020-01-02T12:20:40.456000+00:00"),
                ]
            )
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
        self.assertEqual(self.run_object.n_channels, 5)

        self.run_object.channels_recorded_auxiliary = ["temperature", "battery"]
        self.assertEqual(self.run_object.n_channels, 7)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
