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
from mt_metadata.timeseries import Run, Station

# =============================================================================
#
# =============================================================================
class TestStation(unittest.TestCase):
    """
    test station metadata
    """

    def setUp(self):
        self.maxDiff = None
        self.station_object = Station()
        self.meta_dict = {
            "station": {
                "acquired_by.author": "mt",
                "acquired_by.comments": "Aqcuired by comments",
                "fdsn.id": "MT012",
                "channel_layout": "L",
                "channels_recorded": ["Ex", "Ey", "Hx", "Hy"],
                "comments": "comments",
                "data_type": "MT",
                "geographic_name": "london",
                "id": "mt012",
                "location.declination.comments": "declination comments",
                "location.declination.model": "WMM",
                "location.declination.value": 12.3,
                "location.elevation": 1234.0,
                "location.latitude": 10.0,
                "location.longitude": -112.98,
                "orientation.method": "compass",
                "orientation.reference_frame": "geographic",
                "provenance.comments": "Provenance comments",
                "provenance.creation_time": "1980-01-01T00:00:00+00:00",
                "provenance.log": "provenance log",
                "provenance.software.author": "test",
                "provenance.software.name": "name",
                "provenance.software.version": "1.0a",
                "provenance.submitter.author": "name",
                "provenance.submitter.email": "test@here.org",
                "provenance.submitter.organization": "submitter org",
                "run_list": [],
                "time_period.end": "1980-01-01T00:00:00+00:00",
                "time_period.start": "1980-01-01T00:00:00+00:00",
            }
        }

        self.meta_dict = {
            "station": OrderedDict(
                sorted(self.meta_dict["station"].items(), key=itemgetter(0))
            )
        }

    def test_in_out_dict(self):
        self.station_object.from_dict(self.meta_dict)
        self.assertDictEqual(self.meta_dict, self.station_object.to_dict())

    def test_in_out_series(self):
        station_series = pd.Series(self.meta_dict["station"])
        self.station_object.from_series(station_series)
        self.assertDictEqual(self.meta_dict, self.station_object.to_dict())

    def test_in_out_json(self):
        survey_json = json.dumps(self.meta_dict)
        self.station_object.from_json((survey_json))
        self.assertDictEqual(self.meta_dict, self.station_object.to_dict())

        survey_json = self.station_object.to_json(nested=True)
        self.station_object.from_json(survey_json)
        self.assertDictEqual(self.meta_dict, self.station_object.to_dict())

    def test_start(self):
        self.station_object.time_period.start = "2020/01/02T12:20:40.4560Z"
        self.assertEqual(
            self.station_object.time_period.start, "2020-01-02T12:20:40.456000+00:00"
        )

        self.station_object.time_period.start = "01/02/20T12:20:40.4560"
        self.assertEqual(
            self.station_object.time_period.start, "2020-01-02T12:20:40.456000+00:00"
        )

    def test_end_date(self):
        self.station_object.time_period.end = "2020/01/02T12:20:40.4560Z"
        self.assertEqual(
            self.station_object.time_period.end, "2020-01-02T12:20:40.456000+00:00"
        )

        self.station_object.time_period.end = "01/02/20T12:20:40.4560"
        self.assertEqual(
            self.station_object.time_period.end, "2020-01-02T12:20:40.456000+00:00"
        )

    def test_latitude(self):
        self.station_object.location.latitude = "40:10:05.123"
        self.assertAlmostEqual(
            self.station_object.location.latitude, 40.1680897, places=5
        )

    def test_longitude(self):
        self.station_object.location.longitude = "-115:34:24.9786"
        self.assertAlmostEqual(
            self.station_object.location.longitude, -115.57361, places=5
        )

    def test_declination(self):
        self.station_object.location.declination.value = "10.980"
        self.assertEqual(self.station_object.location.declination.value, 10.980)

    def test_set_runs(self):
        self.station_object.runs = [Run(id="one")]
        self.assertEqual(len(self.station_object), 1)
        self.assertListEqual(["one"], self.station_object.run_list)

    def test_set_runs_fail(self):
        def set_runs(value):
            self.station_object.runs = value

        self.assertRaises(TypeError, set_runs, 10)
        self.assertRaises(TypeError, set_runs, [Run(), Station()])

    def test_add_stations(self):
        station_02 = Station()
        station_02.runs.append(Run(id="two"))
        self.station_object.runs.append(Run(id="one"))
        self.station_object += station_02
        self.assertEqual(len(self.station_object), 2)
        self.assertListEqual(["one", "two"], self.station_object.run_list)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
