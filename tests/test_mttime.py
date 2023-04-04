# -*- coding: utf-8 -*-
"""
time test
Created on Thu May 21 14:09:17 2020
@author: jpeacock
"""

import unittest
from dateutil import parser as dtparser
from dateutil import tz
import pandas as pd
import numpy as np
from mt_metadata.utils.mttime import MTime
from mt_metadata.utils.exceptions import MTTimeError

# =============================================================================
# tests
# =============================================================================
class TestMTime(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.date_str_01 = "2020-01-02"
        self.date_str_01 = "01-02-20"
        self.year = 2020
        self.month = 1
        self.day = 2
        self.hour = 12
        self.minutes = 15
        self.seconds = 20
        self.microseconds = 123000
        self.dt_str_01 = "2020-01-02 12:15:20.123"
        self.dt_true = "2020-01-02T12:15:20.123000+00:00"
        self.keys = [
            "year",
            "month",
            "day",
            "hour",
            "minutes",
            "seconds",
            "microseconds",
        ]

        self.epoch_seconds = 1577967320.123
        self.input_fail = "01294055"

    def test_string_input_date(self):
        t = MTime(self.date_str_01)

        for key in self.keys[0:3]:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

    def test_pd_timestamp(self):
        stamp = pd.Timestamp(self.dt_true)

        t = MTime(stamp)
        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))
        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.iso_str)
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(
                self.epoch_seconds, t.epoch_seconds, places=4
            )

    def test_string_input_dt(self):
        t = MTime()
        t.from_str(self.dt_str_01)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.iso_str)
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(
                self.epoch_seconds, t.epoch_seconds, places=4
            )

    def test_np_datetime64_str(self):
        ntime = np.datetime64(self.dt_str_01)
        t = MTime(ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.iso_str)
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(
                self.epoch_seconds, t.epoch_seconds, places=4
            )

    def test_np_datetime64_ns(self):
        ntime = np.datetime64(int(self.epoch_seconds * 1e9), "ns")
        t = MTime(ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.iso_str)
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(
                self.epoch_seconds, t.epoch_seconds, places=4
            )

    def test_np_datetime64_us(self):
        ntime = np.datetime64(int(self.epoch_seconds * 1e6), "us")
        t = MTime(ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.iso_str)
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(
                self.epoch_seconds, t.epoch_seconds, places=4
            )

    def test_np_datetime64_ms(self):
        ntime = np.datetime64(int(self.epoch_seconds * 1e3), "ms")
        t = MTime(ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.iso_str)
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(
                self.epoch_seconds, t.epoch_seconds, places=4
            )

    def test_input_fail(self):
        t = MTime()
        self.assertRaises(ValueError, t.from_str, self.input_fail)

    def test_compare_dt(self):
        dt_01 = MTime()
        dt_02 = MTime()

        with self.subTest("dt"):
            self.assertTrue(dt_01 == dt_02)
        with self.subTest("isostring"):
            self.assertTrue(dt_01 == dt_02.iso_str)
        with self.subTest("epoch_seconds"):
            self.assertTrue(dt_01 == dt_02.epoch_seconds)
        with self.subTest("ge"):
            self.assertTrue(dt_01 >= dt_02)
        with self.subTest("le"):
            self.assertTrue(dt_01 <= dt_02)

    def test_no_tz(self):
        dt_obj = dtparser.isoparse(self.dt_str_01)

        if isinstance(dt_obj, tz.tzlocal):
            self.mtime_obj.logger.warning("Local Time Zone Found")
        self.assertIsInstance(dt_obj.tzinfo, type(None))

    def test_tz(self):
        dt_obj = dtparser.isoparse(self.dt_true)

        if isinstance(dt_obj, tz.tzlocal):
            self.mtime_obj.logger.warning("Local Time Zone Found")
        self.assertIsInstance(dt_obj.tzinfo, tz.tzutc)

    def test_hash(self):
        t1 = MTime(self.dt_true)
        t2 = MTime(self.dt_true)

        t_set = list(set([t1, t2]))
        self.assertListEqual(t_set, [t1.isoformat()])


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
