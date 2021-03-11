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
from mt_metadata.timeseries import Channel

# =============================================================================
#
# =============================================================================
class TestChannel(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.channel_object = Channel()
        self.meta_dict = {
            "channel": {
                "comments": "great",
                "component": "temperature",
                "channel_number": 1,
                "data_quality.rating.author": "mt",
                "data_quality.rating.method": "ml",
                "data_quality.rating.value": 4,
                "data_quality.warnings": "No warnings",
                "filter.applied": [True, False],
                "filter.comments": "test",
                "filter.name": ["lowpass", "counts2mv"],
                "location.elevation": 1234.0,
                "location.latitude": 12.324,
                "location.longitude": -112.03,
                "measurement_azimuth": 0.0,
                "measurement_tilt": 0.0,
                "sample_rate": 256.0,
                "sensor.id": "1244A",
                "sensor.manufacturer": "faraday",
                "sensor.model": "ichiban",
                "sensor.type": "diode",
                "time_period.end": "1980-01-01T00:00:00+00:00",
                "time_period.start": "1980-01-01T00:00:00+00:00",
                "translated_azimuth": 0.0,
                "translated_tilt": 0.0,
                "type": "auxiliary",
                "units": "celsius",
            }
        }

        self.meta_dict = {
            "channel": OrderedDict(
                sorted(self.meta_dict["channel"].items(), key=itemgetter(0))
            )
        }

    def test_in_out_dict(self):
        self.channel_object.from_dict(self.meta_dict)
        self.assertDictEqual(self.meta_dict, self.channel_object.to_dict())

    def test_in_out_series(self):
        channel_series = pd.Series(self.meta_dict["channel"])
        self.channel_object.from_series(channel_series)
        self.assertDictEqual(self.meta_dict, self.channel_object.to_dict())

    def test_in_out_json(self):
        survey_json = json.dumps(self.meta_dict)
        self.channel_object.from_json((survey_json))
        self.assertDictEqual(self.meta_dict, self.channel_object.to_dict())

        survey_json = self.channel_object.to_json(nested=True)
        self.channel_object.from_json(survey_json)
        self.assertDictEqual(self.meta_dict, self.channel_object.to_dict())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
