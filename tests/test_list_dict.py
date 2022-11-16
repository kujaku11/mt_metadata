# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:22:08 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest
from mt_metadata.utils.dict_list import ListDict
from mt_metadata.timeseries import Survey, Station, Run, Channel

# =============================================================================


class TestListDict(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.ld["a"] = 10

    def test_in_keys(self):
        self.assertIn("a", self.ld.keys())

    def test_value(self):
        self.assertEqual(self.ld["a"], 10)

    def test_from_index(self):
        self.assertEqual(self.ld[0], 10)

    def test_from_key(self):
        self.assertEqual(self.ld["a"], 10)

    def test_get_item_fail(self):
        self.assertRaises(KeyError, self.ld._get_key_from_index, 1)

    def test_str(self):
        self.assertEqual("Keys In Order: a", self.ld.__str__())

    def test_repr(self):
        self.assertEqual("OrderedDict([('a', 10)])", self.ld.__repr__())

    def test_items(self):
        self.assertTupleEqual((("a", 10),), tuple(self.ld.items()))


class TestListDictSetIndex(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.ld[1] = 2

    def test_in_keys(self):
        self.assertIn("1", self.ld.keys())

    def test_from_key(self):
        self.assertEqual(self.ld["1"], 2)

    def test_from_index(self):
        self.assertEqual(self.ld[0], 2)


class TestListDictFromSurvey(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.survey = Survey(id="test")
        self.ld[0] = self.survey
        self.maxDiff = None

    def test_in_keys(self):
        self.assertIn("test", self.ld.keys())

    def test_survey_from_index(self):
        self.assertDictEqual(
            self.survey.to_dict(single=True), self.ld[0].to_dict(single=True)
        )

    def test_survey_from_key(self):
        self.assertDictEqual(
            self.survey.to_dict(single=True),
            self.ld["test"].to_dict(single=True),
        )


class TestListDictFromStation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.station = Station(id="test")
        self.ld[0] = self.station
        self.maxDiff = None

    def test_in_keys(self):
        self.assertIn("test", self.ld.keys())

    def test_station_from_index(self):
        self.assertDictEqual(
            self.station.to_dict(single=True), self.ld[0].to_dict(single=True)
        )

    def test_station_from_key(self):
        self.assertDictEqual(
            self.station.to_dict(single=True),
            self.ld["test"].to_dict(single=True),
        )


### Doens't work for some reason something about TypeError Run not callable
# class TestListDictFromRun(unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.ld = ListDict()
#         self.run = Run(id="test")
#         self.ld[0] = self.run
#         self.maxDiff = None

#     def test_in_keys(self):
#         self.assertIn("test", self.ld.keys())

#     def test_run_from_index(self):
#         self.assertDictEqual(
#             self.run.to_dict(single=True), self.ld[0].to_dict(single=True)
#         )

#     def test_run_from_key(self):
#         self.assertDictEqual(
#             self.run.to_dict(single=True),
#             self.ld["test"].to_dict(single=True),
#         )


class TestListDictFromChannel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.channel = Channel(component="test")
        self.ld[0] = self.channel
        self.maxDiff = None

    def test_in_keys(self):
        self.assertIn("test", self.ld.keys())

    def test_survey_from_index(self):
        self.assertDictEqual(
            self.channel.to_dict(single=True), self.ld[0].to_dict(single=True)
        )

    def test_survey_from_key(self):
        self.assertDictEqual(
            self.channel.to_dict(single=True),
            self.ld["test"].to_dict(single=True),
        )


# =============================================================================
# Run test
# =============================================================================
if __name__ == "__main__":
    unittest.main()
