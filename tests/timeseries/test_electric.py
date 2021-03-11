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
from mt_metadata.timeseries import Electric

# =============================================================================
#
# =============================================================================
class TestElectric(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.electric_object = Electric()
        self.meta_dict = {
            "electric": {
                "ac.end": 10.2,
                "ac.start": 12.1,
                "comments": "comments",
                "component": "ex",
                "contact_resistance.end": 1.2,
                "contact_resistance.start": 1.1,
                "channel_number": 2,
                "data_quality.rating.author": "mt",
                "data_quality.rating.method": "ml",
                "data_quality.rating.value": 4,
                "data_quality.warnings": "warnings",
                "dc.end": 1.0,
                "dc.start": 2.0,
                "dipole_length": 100.0,
                "filter.applied": [False, True],
                "filter.comments": "filter comments",
                "filter.name": ["counts2mv", "lowpass"],
                "measurement_azimuth": 90.0,
                "measurement_tilt": 0.0,
                "negative.elevation": 100.0,
                "negative.id": "a",
                "negative.latitude": 12.12,
                "negative.longitude": -111.12,
                "negative.manufacturer": "test",
                "negative.model": "fats",
                "negative.type": "pb-pbcl",
                "positive.elevation": 101.0,
                "positive.id": "b",
                "positive.latitude": 12.123,
                "positive.longitude": -111.14,
                "positive.manufacturer": "test",
                "positive.model": "fats",
                "positive.type": "ag-agcl",
                "sample_rate": 256.0,
                "time_period.end": "1980-01-01T00:00:00+00:00",
                "time_period.start": "1980-01-01T00:00:00+00:00",
                "translated_azimuth": 0.0,
                "translated_tilt": 0.0,
                "type": "electric",
                "units": "counts",
            }
        }

        self.meta_dict = {
            "electric": OrderedDict(
                sorted(self.meta_dict["electric"].items(), key=itemgetter(0))
            )
        }

    def test_in_out_dict(self):
        self.electric_object.from_dict(self.meta_dict)
        self.assertDictEqual(self.meta_dict, self.electric_object.to_dict())

    def test_in_out_series(self):
        electric_series = pd.Series(self.meta_dict["electric"])
        self.electric_object.from_series(electric_series)
        self.assertDictEqual(self.meta_dict, self.electric_object.to_dict())

    def test_in_out_json(self):
        survey_json = json.dumps(self.meta_dict)
        self.electric_object.from_json((survey_json))
        self.assertDictEqual(self.meta_dict, self.electric_object.to_dict())

        survey_json = self.electric_object.to_json(nested=True)
        self.electric_object.from_json(survey_json)
        self.assertDictEqual(self.meta_dict, self.electric_object.to_dict())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
