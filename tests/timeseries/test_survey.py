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
from mt_metadata.timeseries import Station, Survey

# =============================================================================
#
# =============================================================================
class TestSurvey(unittest.TestCase):
    """
    test metadata in is metadata out
    """

    def setUp(self):
        self.maxDiff = None
        self.meta_dict = {
            "survey": {
                "acquired_by.author": "MT",
                "acquired_by.comments": "tired",
                "survey_id": "MT001",
                "fdsn.network": "EM",
                "citation_dataset.doi": "http://doi.####",
                "citation_journal.doi": None,
                "comments": "comments",
                "country": "Canada",
                "datum": "WGS84",
                "geographic_name": "earth",
                "name": "entire survey of the earth",
                "northwest_corner.latitude": 80.0,
                "northwest_corner.longitude": 179.9,
                "project": "EM-EARTH",
                "project_lead.author": "T. Lurric",
                "project_lead.email": "mt@mt.org",
                "project_lead.organization": "mt rules",
                "release_license": "CC-0",
                "southeast_corner.latitude": -80.0,
                "southeast_corner.longitude": -179.9,
                "summary": "Summary paragraph",
                "time_period.end_date": "1980-01-01",
                "time_period.start_date": "2080-01-01",
            }
        }

        self.meta_dict = {
            "survey": OrderedDict(
                sorted(self.meta_dict["survey"].items(), key=itemgetter(0))
            )
        }

        self.survey_object = Survey()

    def test_in_out_dict(self):
        self.survey_object.from_dict(self.meta_dict)
        self.assertDictEqual(self.meta_dict, self.survey_object.to_dict())

    def test_in_out_series(self):
        survey_series = pd.Series(self.meta_dict["survey"])
        self.survey_object.from_series(survey_series)
        self.assertDictEqual(self.meta_dict, self.survey_object.to_dict())

    def test_in_out_json(self):
        survey_json = json.dumps(self.meta_dict)
        self.survey_object.from_json((survey_json))
        self.assertDictEqual(self.meta_dict, self.survey_object.to_dict())

        survey_json = self.survey_object.to_json(nested=True)
        self.survey_object.from_json(survey_json)
        self.assertDictEqual(self.meta_dict, self.survey_object.to_dict())

    def test_start_date(self):
        self.survey_object.time_period.start_date = "2020/01/02"
        self.assertEqual(self.survey_object.time_period.start_date, "2020-01-02")

        self.survey_object.start_date = "01-02-2020T12:20:30.450000+00:00"
        self.assertEqual(self.survey_object.time_period.start_date, "2020-01-02")

    def test_end_date(self):
        self.survey_object.time_period.start_date = "2020/01/02"
        self.assertEqual(self.survey_object.time_period.start_date, "2020-01-02")

        self.survey_object.start_date = "01-02-2020T12:20:30.45Z"
        self.assertEqual(self.survey_object.time_period.start_date, "2020-01-02")

    def test_latitude(self):
        self.survey_object.southeast_corner.latitude = "40:10:05.123"
        self.assertAlmostEqual(
            self.survey_object.southeast_corner.latitude, 40.1680897, places=5
        )

    def test_longitude(self):
        self.survey_object.southeast_corner.longitude = "-115:34:24.9786"
        self.assertAlmostEqual(
            self.survey_object.southeast_corner.longitude, -115.57361, places=5
        )

    def test_acuired_by(self):
        self.survey_object.from_dict(self.meta_dict)
        self.assertEqual(self.survey_object.acquired_by.author, "MT")

    def test_set_stations(self):
        self.survey_object.stations = [Station(id="one")]
        self.assertEqual(len(self.survey_object.stations), 1)
        self.assertListEqual(["one"], self.survey_object.station_names)

    def test_set_stations_fail(self):
        def set_stations(value):
            self.survey_object.stations = value

        self.assertRaises(TypeError, set_stations, 10)
        self.assertRaises(TypeError, set_stations, [Station(), Survey()])

    def test_add_surveys(self):
        survey_02 = Survey()
        survey_02.stations.append(Station(id="two"))
        self.survey_object.stations.append(Station(id="one"))
        self.survey_object += survey_02
        self.assertEqual(len(self.survey_object), 2)
        self.assertListEqual(["one", "two"], self.survey_object.station_names)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
