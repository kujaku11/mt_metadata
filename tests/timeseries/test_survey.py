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
                "id": "MT001",
                "fdsn.network": "EM",
                "citation_dataset.doi": "http://doi.####",
                "citation_journal.doi": None,
                "comments": "comments",
                "country": ["Canada"],
                "datum": "WGS84",
                "funding_source.name": ["NSF"],
                "funding_source.organization": ["US governement"],
                "funding_source.grant_id": ["a345"],
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
                "state": ["Manitoba"],
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
        with self.subTest("JSON Dumps"):
            survey_json = json.dumps(self.meta_dict)
            self.survey_object.from_json((survey_json))
            self.assertDictEqual(self.meta_dict, self.survey_object.to_dict())

        with self.subTest("json to dict"):
            survey_json = self.survey_object.to_json(nested=True)
            self.survey_object.from_json(survey_json)
            self.assertDictEqual(self.meta_dict, self.survey_object.to_dict())

    def test_start_date(self):
        with self.subTest("input date"):
            self.survey_object.time_period.start_date = "2020/01/02"
            self.assertEqual(
                self.survey_object.time_period.start_date, "2020-01-02"
            )

        with self.subTest("Input datetime"):
            self.survey_object.start_date = "01-02-2020T12:20:30.450000+00:00"
            self.assertEqual(
                self.survey_object.time_period.start_date, "2020-01-02"
            )

    def test_end_date(self):
        with self.subTest("input date"):
            self.survey_object.time_period.end_date = "2020/01/02"
            self.assertEqual(
                self.survey_object.time_period.end_date, "2020-01-02"
            )

        with self.subTest("Input datetime"):
            self.survey_object.end_date = "01-02-2020T12:20:30.45Z"
            self.assertEqual(
                self.survey_object.time_period.end_date, "2020-01-02"
            )

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

    def test_funding_source(self):
        with self.subTest("name"):
            self.survey_object.funding_source.name = "NSF"
            self.assertListEqual(
                self.survey_object.funding_source.name, ["NSF"]
            )
        with self.subTest("organization"):
            self.survey_object.funding_source.organization = (
                "US governement, DOE"
            )
            self.assertListEqual(
                self.survey_object.funding_source.organization,
                ["US governement", "DOE"],
            )
        with self.subTest("grant_id"):
            self.survey_object.funding_source.grant_id = "a345"
            self.assertListEqual(
                self.survey_object.funding_source.grant_id, ["a345"]
            )

    def test_geographic_location(self):
        with self.subTest("country"):
            self.survey_object.country = "Canada"
            self.assertListEqual(self.survey_object.country, ["Canada"])
        with self.subTest("state"):
            self.survey_object.state = "Manitoba, Saskatchewan"
            self.assertListEqual(
                self.survey_object.state, ["Manitoba", "Saskatchewan"]
            )

    def test_aqcuired_by(self):
        self.survey_object.from_dict(self.meta_dict)
        self.assertEqual(self.survey_object.acquired_by.author, "MT")

    def test_add_station(self):
        self.survey_object.add_station(Station(id="one"))

        with self.subTest("length"):
            self.assertEqual(len(self.survey_object.stations), 1)

        with self.subTest("staiton names"):
            self.assertListEqual(["one"], self.survey_object.station_names)

        with self.subTest("has station"):
            self.assertTrue(self.survey_object.has_station("one"))

        with self.subTest("index"):
            self.assertEqual(0, self.survey_object.station_index("one"))

    def test_add_stations_fail(self):
        self.assertRaises(TypeError, self.survey_object.add_station, 10)

    def test_get_station(self):
        input_station = Station(id="one")
        self.survey_object.add_station(input_station)
        s = self.survey_object.get_station("one")
        self.assertTrue(input_station == s)

    def test_set_stations_fail(self):
        def set_stations(value):
            self.survey_object.stations = value

        with self.subTest("integer input"):
            self.assertRaises(TypeError, set_stations, 10)

        with self.subTest("bad object"):
            self.assertRaises(TypeError, set_stations, [Station(), Survey()])

    def test_add_surveys(self):
        survey_02 = Survey()
        survey_02.stations.append(Station(id="two"))
        self.survey_object.stations.append(Station(id="one"))
        self.survey_object += survey_02

        with self.subTest("length"):
            self.assertEqual(len(self.survey_object), 2)

        with self.subTest("compare list"):
            self.assertListEqual(
                ["one", "two"], self.survey_object.station_names
            )

    def test_remove_station(self):
        self.survey_object.stations.append(Station(id="one"))
        self.survey_object.remove_station("one")
        self.assertEqual([], self.survey_object.station_names)

    def test_update_time_period(self):
        s = Station(id="001")
        s.time_period.start = "2020-01-01T00:00:00"
        s.time_period.end = "2020-12-01T12:12:12"
        self.survey_object.add_station(s)
        self.survey_object.update_time_period()

        with self.subTest("Test new start"):
            self.assertEqual(
                self.survey_object.time_period.start,
                "2020-01-01T00:00:00+00:00",
            )

        with self.subTest("Test new end"):
            self.assertEqual(
                self.survey_object.time_period.end,
                "2020-12-01T12:12:12+00:00",
            )


class TestAddStation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.station_01 = Station()
        self.station_01.location.latitude = 40.0
        self.station_01.location.longitude = -120
        self.station_01.id = "mt01"
        self.station_01.time_period.start = "2023-01-01T00:00:00"
        self.station_01.time_period.end = "2023-01-03T00:00:00"

        self.station_02 = Station()
        self.station_02.location.latitude = 35.0
        self.station_02.location.longitude = -115
        self.station_02.id = "mt02"
        self.station_02.time_period.start = "2023-01-03T00:00:00"
        self.station_02.time_period.end = "2023-01-06T00:00:00"

        self.survey = Survey(id="test")
        self.survey.add_station(self.station_01)
        self.survey.add_station(self.station_02)

    def test_time_period(self):
        with self.subTest("start"):
            self.assertEqual(
                self.survey.time_period.start, self.station_01.time_period.start
            )
        with self.subTest("end"):
            self.assertEqual(
                self.survey.time_period.end, self.station_02.time_period.end
            )

    def test_bounding_box(self):
        with self.subTest("northwest corner latitude"):
            self.assertEqual(
                self.station_01.location.latitude,
                self.survey.northwest_corner.latitude,
            )
        with self.subTest("northwest corner longitude"):
            self.assertEqual(
                self.station_01.location.longitude,
                self.survey.northwest_corner.longitude,
            )
        with self.subTest("southeast corner latitude"):
            self.assertEqual(
                self.station_02.location.latitude,
                self.survey.southeast_corner.latitude,
            )
        with self.subTest("southeast corner longitude"):
            self.assertEqual(
                self.station_02.location.longitude,
                self.survey.southeast_corner.longitude,
            )

    def test_station_list(self):
        self.assertListEqual(
            self.survey.station_names, [self.station_01.id, self.station_02.id]
        )

    def test_remove_station(self):
        self.survey.remove_station("mt02")

        self.assertListEqual(self.survey.station_names, [self.station_01.id])

        self.survey.add_station(self.station_02)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
