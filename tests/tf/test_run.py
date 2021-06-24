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
            'run':
                OrderedDict([('acquired_by.author', None),
                  ('channels_recorded_auxiliary', []),
                  ('channels_recorded_electric', ['ex', 'ey']),
                  ('channels_recorded_magnetic', ['hx', 'hy', 'hz']),
                  ('data_logger.firmware.author', None),
                  ('data_logger.firmware.name', None),
                  ('data_logger.firmware.version', None),
                  ('data_logger.id', None),
                  ('data_logger.manufacturer', None),
                  ('data_logger.timing_system.drift', None),
                  ('data_logger.timing_system.type', None),
                  ('data_logger.timing_system.uncertainty', None),
                  ('data_logger.type', None),
                  ('data_type', None),
                  ('ex.channel_id', '4.0'),
                  ('ex.channel_number', 4),
                  ('ex.component', 'ex'),
                  ('ex.contact_resistance.end', 11.1),
                  ('ex.contact_resistance.start', 11.4),
                  ('ex.dipole_length', 55.0),
                  ('ex.measurement_azimuth', 0.0),
                  ('ex.measurement_tilt', 0.0),
                  ('ex.sample_rate', 0.0),
                  ('ex.translated_azimuth', -12.5),
                  ('ex.type', 'electric'),
                  ('ex.units', 'millivolts'),
                  ('ey.channel_id', '5.0'),
                  ('ey.channel_number', 5),
                  ('ey.component', 'ey'),
                  ('ey.contact_resistance.end', 7.9),
                  ('ey.contact_resistance.start', 12.6),
                  ('ey.dipole_length', 55.0),
                  ('ey.measurement_azimuth', 90.0),
                  ('ey.measurement_tilt', 0.0),
                  ('ey.sample_rate', 0.0),
                  ('ey.translated_azimuth', 77.5),
                  ('ey.type', 'electric'),
                  ('ey.units', 'millivolts'),
                  ('hx.channel_id', '1.0'),
                  ('hx.channel_number', 2284),
                  ('hx.component', 'hx'),
                  ('hx.measurement_azimuth', 0.0),
                  ('hx.measurement_tilt', 0.0),
                  ('hx.sample_rate', 0.0),
                  ('hx.translated_azimuth', -12.5),
                  ('hx.type', 'magnetic'),
                  ('hx.units', 'nanotesla'),
                  ('hy.channel_id', '2.0'),
                  ('hy.channel_number', 2294),
                  ('hy.component', 'hy'),
                  ('hy.measurement_azimuth', 90.0),
                  ('hy.measurement_tilt', 0.0),
                  ('hy.sample_rate', 0.0),
                  ('hy.translated_azimuth', 77.5),
                  ('hy.type', 'magnetic'),
                  ('hy.units', 'nanotesla'),
                  ('hz.channel_id', '3.0'),
                  ('hz.channel_number', 2304),
                  ('hz.component', 'hz'),
                  ('hz.measurement_azimuth', 0.0),
                  ('hz.measurement_tilt', 90.0),
                  ('hz.sample_rate', 0.0),
                  ('hz.translated_azimuth', 0.0),
                  ('hz.translated_tilt', 90.0),
                  ('hz.type', 'magnetic'),
                  ('hz.units', 'nanotesla'),
                  ('id', 'gv163a'),
                  ('metadata_by.author', None),
                  ('rrhx.channel_number', None),
                  ('rrhx.component', None),
                  ('rrhx.measurement_azimuth', 0.0),
                  ('rrhx.measurement_tilt', 0.0),
                  ('rrhx.sample_rate', 0.0),
                  ('rrhx.type', 'magnetic'),
                  ('rrhx.units', None),
                  ('rrhy.channel_number', None),
                  ('rrhy.component', None),
                  ('rrhy.measurement_azimuth', 0.0),
                  ('rrhy.measurement_tilt', 0.0),
                  ('rrhy.sample_rate', 0.0),
                  ('rrhy.type', 'magnetic'),
                  ('rrhy.units', None),
                  ('sample_rate', None),
                  ('temperature.channel_number', None),
                  ('temperature.component', None),
                  ('temperature.measurement_azimuth', 0.0),
                  ('temperature.measurement_tilt', 0.0),
                  ('temperature.sample_rate', 0.0),
                  ('temperature.type', 'auxiliary'),
                  ('temperature.units', None),
                  ('time_period.end', '1980-01-01T00:00:00+00:00'),
                  ('time_period.start', '2020-01-02T12:20:40.456000+00:00')])}

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
