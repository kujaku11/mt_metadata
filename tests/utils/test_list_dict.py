# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:22:08 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest

from mt_metadata.common.list_dict import ListDict
from mt_metadata.timeseries import Channel, Run, Station, Survey


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
        self.assertEqual("Contents:\n------------\n\ta = 10", self.ld.__str__())

    def test_repr(self):
        self.assertEqual("OrderedDict([('a', 10)])", self.ld.__repr__())

    def test_items(self):
        self.assertTupleEqual((("a", 10),), tuple(self.ld.items()))

    def test_get_index_from_key(self):
        self.assertEqual(0, self.ld._get_index_from_key("a"))

    def test_get_index_from_key_fail(self):
        self.assertRaises(KeyError, self.ld._get_index_from_key, "b")

    def test_get_key_from_index(self):
        self.assertEqual("a", self.ld._get_key_from_index(0))

    def test_get_key_from_index_fail(self):
        self.assertRaises(KeyError, self.ld._get_key_from_index, 2)

    def test_copy(self):
        lc = self.ld.copy()
        self.assertEqual(self.ld, lc)

    def test_pop(self):
        self.ld["b"] = 1
        b = self.ld.pop("b")
        with self.subTest("value of b"):
            self.assertEqual(b["b"], 1)
        with self.subTest("b not in keys"):
            self.assertNotIn("b", self.ld.keys())

    def test_pop_fail(self):
        self.assertRaises(KeyError, self.ld.pop, "h")


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
        self.ld.append(self.survey)
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
        self.ld.append(self.station)
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


class TestListDictFromRun(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.run_obj = Run(id="test")
        self.ld[0] = self.run_obj
        self.maxDiff = None

    def test_in_keys(self):
        self.assertIn("test", self.ld.keys())

    def test_run_from_index(self):
        self.assertDictEqual(
            self.run_obj.to_dict(single=True), self.ld[0].to_dict(single=True)
        )

    def test_run_from_key(self):
        self.assertDictEqual(
            self.run_obj.to_dict(single=True),
            self.ld["test"].to_dict(single=True),
        )


class TestListDictFromChannel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict()
        self.channel = Channel(component="test")
        self.ld.append(self.channel)
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


class TestListDictRemove(unittest.TestCase):
    def setUp(self):
        self.ld = ListDict()
        self.ld["a"] = 0

    def test_remove_by_key(self):
        self.ld.remove("a")
        self.assertListEqual([], self.ld.keys())

    def test_remove_by_index(self):
        self.ld.remove(0)
        self.assertListEqual([], self.ld.keys())


class TestListDictSlice(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ld = ListDict([("a", 0), ("b", 1), ("c", 2), ("d", 3)])

    def test_slice_01(self):
        b = self.ld[0:1]
        self.assertTrue(b == ListDict([("a", 0)]))

    def test_slice_02(self):
        b = self.ld[0:2]
        self.assertTrue(b == ListDict([("a", 0), ("b", 1)]))

    def test_slice_03(self):
        b = self.ld[1:2]
        self.assertTrue(b == ListDict([("b", 1)]))

    def test_slice_04(self):
        b = self.ld[1:-1]
        self.assertTrue(b == ListDict([("b", 1), ("c", 2)]))

    def test_slice_05(self):
        b = self.ld[1:]
        self.assertTrue(b == ListDict([("b", 1), ("c", 2), ("d", 3)]))

    def test_slice_06(self):
        b = self.ld[:-1]
        self.assertTrue(b == ListDict([("a", 0), ("b", 1), ("c", 2)]))

    def test_slice_keys_01(self):
        b = self.ld["a":"b"]
        self.assertTrue(b == ListDict([("a", 0)]))

    def test_slice_keys_02(self):
        b = self.ld["a":"c"]
        self.assertTrue(b == ListDict([("a", 0), ("b", 1)]))

    def test_slice_keys_03(self):
        b = self.ld["b":"c"]
        self.assertTrue(b == ListDict([("b", 1)]))

    def test_slice_keys_04(self):
        b = self.ld["b":"d"]
        self.assertTrue(b == ListDict([("b", 1), ("c", 2)]))

    def test_slice_keys_05(self):
        b = self.ld["b":]
        self.assertTrue(b == ListDict([("b", 1), ("c", 2), ("d", 3)]))

    def test_slice_keys_06(self):
        b = self.ld[:"d"]
        self.assertTrue(b == ListDict([("a", 0), ("b", 1), ("c", 2)]))

    def test_slice_mixed_01(self):
        b = self.ld[1:"d"]
        self.assertTrue(b == ListDict([("b", 1), ("c", 2)]))

    def test_slice_mixed_02(self):
        b = self.ld["a":-1]
        self.assertTrue(b == ListDict([("a", 0), ("b", 1), ("c", 2)]))

    def test_slice_mixed_03(self):
        b = self.ld[0:"b"]
        self.assertTrue(b == ListDict([("a", 0)]))

    def test_get_index_slice_from_slice_fail(self):
        self.assertRaises(
            TypeError,
            self.ld._get_index_slice_from_slice(False, slice(None, None, None)),
        )

    def test_get_index_slice_from_slice_fail_bad_keys(self):
        self.assertRaises(
            TypeError,
            self.ld._get_index_slice_from_slice(None, slice(False, False, False)),
        )

    def test_getitem_fail(self):
        self.assertRaises(KeyError, self.ld.__getitem__, "z")

    def test_getitem_fail_bad_type(self):
        self.assertRaises(TypeError, self.ld.__getitem__, 10.0)

    def test_setitem_fail(self):
        self.assertRaises(NotImplementedError, self.ld.__setitem__, slice(0, 1), None)

    def test_remove_fail(self):
        self.assertRaises(KeyError, self.ld.remove, "z")

    def test_remove_fail_bad_key_type(self):
        self.assertRaises(TypeError, self.ld.remove, 10.0)

    def test_extend_fail(self):
        self.assertRaises(TypeError, self.ld.extend, ("x"))

    def test_update_fail(self):
        self.assertRaises(TypeError, self.ld.update, ("x"))


# =============================================================================
# Run test
# =============================================================================
if __name__ == "__main__":
    unittest.main()
