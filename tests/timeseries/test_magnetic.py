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
from mt_metadata.timeseries import Magnetic

# =============================================================================
#
# =============================================================================
class TestMagnetic(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.magnetic_object = Magnetic()
        self.meta_dict = {
            "magnetic": {
                "measurement_azimuth": 0.0,
                "measurement_tilt": 0.0,
                "channel_number": 2,
                "component": "hy",
                "data_quality.rating.author": "mt",
                "data_quality.rating.method": "ml",
                "data_quality.rating.value": 4,
                "data_quality.warnings": "No warnings",
                "location.elevation": 1230.9,
                "filter.applied": [True],
                "filter.name": ["counts2mv"],
                "filter.comments": "filter comments",
                "h_field_max.end": 12.3,
                "h_field_max.start": 1200.1,
                "h_field_min.end": 12.3,
                "h_field_min.start": 1400.0,
                "location.latitude": 40.234,
                "location.longitude": -113.45,
                "comments": "comments",
                "sample_rate": 256.0,
                "sensor.id": "ant2284",
                "sensor.manufacturer": "mt coils",
                "sensor.type": "induction coil",
                "sensor.model": "ant4",
                "type": "magnetic",
                "units": "mv",
                "time_period.start": "1980-01-01T00:00:00+00:00",
                "time_period.end": "1980-01-01T00:00:00+00:00",
                "translated_azimuth": 0.0,
                "translated_tilt": 0.0,
            }
        }

        self.meta_dict = {
            "magnetic": OrderedDict(
                sorted(self.meta_dict["magnetic"].items(), key=itemgetter(0))
            )
        }

    def test_in_out_dict(self):
        self.magnetic_object.from_dict(self.meta_dict)
        self.assertDictEqual(self.meta_dict, self.magnetic_object.to_dict())

    def test_in_out_series(self):
        magnetic_series = pd.Series(self.meta_dict["magnetic"])
        self.magnetic_object.from_series(magnetic_series)
        self.assertDictEqual(self.meta_dict, self.magnetic_object.to_dict())

    def test_in_out_json(self):
        survey_json = json.dumps(self.meta_dict)
        self.magnetic_object.from_json((survey_json))
        self.assertDictEqual(self.meta_dict, self.magnetic_object.to_dict())

        survey_json = self.magnetic_object.to_json(nested=True)
        self.magnetic_object.from_json(survey_json)
        self.assertDictEqual(self.meta_dict, self.magnetic_object.to_dict())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
