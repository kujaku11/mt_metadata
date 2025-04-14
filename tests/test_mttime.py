# -*- coding: utf-8 -*-
"""
time test
Created on Thu May 21 14:09:17 2020
@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest
from dateutil import parser as dtparser
from dateutil import tz
import datetime
import pandas as pd
import numpy as np

from mt_metadata.utils.mttime import (
    MTime,
    parse,
    _check_timestamp,
    _fix_out_of_bounds_time_stamp,
    _localize_utc,
    TMAX,
    TMIN,
)
from obspy import UTCDateTime


# =============================================================================
# tests
# =============================================================================
class TestMTime(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.date_str_01 = "2020-01-20"
        self.date_str_02 = "01-02-20"
        self.date_str_03 = "2020-20-01"
        self.year = 2020
        self.month = 1
        self.day = 20
        self.hour = 12
        self.minutes = 15
        self.seconds = 20
        self.microseconds = 123000
        self.dt_str_01 = "2020-01-20 12:15:20.123"
        self.dt_true = "2020-01-20T12:15:20.123000+00:00"
        self.add_time_true = "2020-01-20T12:15:50.123000+00:00"
        self.keys = [
            "year",
            "month",
            "day",
            "hour",
            "minutes",
            "seconds",
            "microseconds",
        ]

        self.epoch_seconds = 1579522520.123
        self.input_fail = "01294055"

    def test_string_input_date_01(self):
        t = MTime(time_stamp=self.date_str_01)

        for key in self.keys[0:3]:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

    def test_string_input_date_02(self):
        t = MTime(time_stamp=self.date_str_02)
        with self.subTest("year"):
            self.assertEqual(self.year, t.year)
        with self.subTest("month"):
            self.assertEqual(self.month, t.month)
        with self.subTest("day"):
            self.assertNotEqual(self.day, t.day)

    def test_string_input_date_03(self):
        t = MTime(time_stamp=self.date_str_03)

        for key in self.keys[0:3]:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

    def test_input_epoch_seconds(self):
        t = MTime(time_stamp=self.epoch_seconds)

        self.assertEqual(t, self.dt_true)

    def test_input_epoch_nanoseconds(self):
        t = MTime(time_stamp=self.epoch_seconds * 1e9)

        self.assertEqual(t, self.dt_true)

    def test_input_seconds_fail(self):
        self.assertRaises(ValueError, parse, 10, gps_time=True)

    def test_pd_timestamp(self):
        stamp = pd.Timestamp(self.dt_true)

        t = MTime(time_stamp=stamp)
        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))
        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_string_input_dt(self):
        t = MTime(time_stamp=self.dt_str_01)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_np_datetime64_str(self):
        ntime = np.datetime64(self.dt_str_01)
        t = MTime(time_stamp=ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_np_datetime64_ns(self):
        ntime = np.datetime64(int(self.epoch_seconds * 1e9), "ns")
        t = MTime(time_stamp=ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_np_datetime64_us(self):
        ntime = np.datetime64(int(self.epoch_seconds * 1e6), "us")
        t = MTime(time_stamp=ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_np_datetime64_ms(self):
        ntime = np.datetime64(int(self.epoch_seconds * 1e3), "ms")
        t = MTime(time_stamp=ntime)

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_obspy_utcdatetime(self):
        t = MTime(time_stamp=UTCDateTime(self.dt_true))

        for key in self.keys:
            with self.subTest(key):
                self.assertEqual(getattr(self, key), getattr(t, key))

        with self.subTest("isostring"):
            self.assertEqual(self.dt_true, t.isoformat())
        with self.subTest("epoch seconds"):
            self.assertAlmostEqual(self.epoch_seconds, t.epoch_seconds, places=4)

    def test_input_fail(self):
        t = MTime()
        self.assertRaises(ValueError, parse, self.input_fail)

    def test_input_none(self):
        for t_value in [None, "", "None", "NONE", "none"]:
            t = MTime(time_stamp=t_value)
            self.assertEqual(t, "1980-01-01T00:00:00+00:00")

    def test_compare_dt(self):
        dt_01 = MTime()
        dt_02 = MTime()

        with self.subTest("dt"):
            self.assertTrue(dt_01 == dt_02)
        with self.subTest("isostring"):
            self.assertTrue(dt_01 == dt_02.iso_str)
        with self.subTest("epoch_seconds"):
            self.assertTrue(dt_01 == (dt_02.epoch_seconds * 1e9))
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
        t1 = MTime(time_stamp=self.dt_true)
        t2 = MTime(time_stamp=self.dt_true)

        t_set = list(set([t1, t2]))
        self.assertListEqual(t_set, [t1.isoformat()])

    def test_add_time(self):
        t1 = MTime(time_stamp=self.dt_true)
        t2 = t1 + 30

        with self.subTest("result"):
            self.assertEqual(t2, self.add_time_true)

        with self.subTest("type"):
            self.assertIsInstance(t2, MTime)

    def test_add_time_datetime_timedelta(self):
        t1 = MTime(time_stamp=self.dt_true)
        t2 = t1 + datetime.timedelta(seconds=30)

        with self.subTest("result"):
            self.assertEqual(t2, self.add_time_true)

        with self.subTest("type"):
            self.assertIsInstance(t2, MTime)

    def test_add_time_np_timedelta(self):
        t1 = MTime(time_stamp=self.dt_true)
        t2 = t1 + np.timedelta64(30, "s")

        with self.subTest("result"):
            self.assertEqual(t2, self.add_time_true)

        with self.subTest("type"):
            self.assertIsInstance(t2, MTime)

    def test_add_time_fail(self):
        t1 = MTime(time_stamp=self.dt_true)
        self.assertRaises(ValueError, t1.__add__, self.dt_true)

    def test_subtract_time(self):
        t1 = MTime(time_stamp=self.dt_true)
        t2 = t1 + 30

        self.assertEqual(30, t2 - t1)

    def test_subtract_timedelta(self):
        t1 = MTime(time_stamp=self.dt_true)
        t2 = pd.Timedelta(seconds=30)

        self.assertEqual(MTime(time_stamp="2020-01-20T12:14:50.123000+00:00"), t1 - t2)

    def test_too_large(self):
        t1 = MTime(time_stamp="3000-01-01T00:00:00")
        self.assertEqual(t1, pd.Timestamp.max)

    def test_too_small(self):
        t1 = MTime(time_stamp="1400-01-01T00:00:00")
        self.assertEqual(t1, pd.Timestamp.min)

    def test_utc_too_large(self):
        t1 = MTime(time_stamp=UTCDateTime("3000-01-01"))
        self.assertEqual(t1, pd.Timestamp.max)

    def test_utc_too_small(self):
        t1 = MTime(time_stamp=UTCDateTime("1400-01-01"))
        self.assertEqual(t1, pd.Timestamp.min)

    def test_gps_time(self):
        t1 = MTime(time_stamp=self.dt_true, gps_time=True)
        gps_time = MTime(time_stamp=self.dt_true) - 13
        self.assertTrue(gps_time, t1)

    def test_localize_utc(self):
        t1 = MTime(time_stamp=self.dt_true)
        stamp = _localize_utc(t1.time_stamp)
        self.assertTrue(stamp.tz is not None)

    def test_check_timestamp_too_large(self):
        t1 = pd.Timestamp("3000-01-01T00:00:00")
        too_large, t2 = _check_timestamp(t1)

        with self.subTest("time"):
            self.assertEqual(t2, TMAX)
        with self.subTest("too small"):
            self.assertEqual(True, too_large)

    def test_check_timestamp_too_small(self):
        t1 = pd.Timestamp("1400-01-01T00:00:00")
        too_small, t2 = _check_timestamp(t1)
        with self.subTest("time"):
            self.assertEqual(t2, TMIN)
        with self.subTest("too small"):
            self.assertEqual(True, too_small)

    def test_fix_out_of_bounds_too_large(self):
        dt = dtparser.parse("3000-01-01T00:00:00")
        stamp, too_large = _fix_out_of_bounds_time_stamp(dt)
        with self.subTest("time"):
            self.assertEqual(stamp, TMAX)
        with self.subTest("too large"):
            self.assertEqual(True, too_large)

    def test_fix_out_of_bounds_too_small(self):
        dt = dtparser.parse("1400-01-01T00:00:00")
        stamp, too_small = _fix_out_of_bounds_time_stamp(dt)
        with self.subTest("time"):
            self.assertEqual(stamp, TMIN)
        with self.subTest("too small"):
            self.assertEqual(True, too_small)

    def test_bad_24hour(self):
        t = MTime(time_stamp="2020-01-01T24:00:00")
        self.assertEqual(t, MTime(time_stamp="2020-01-02T00:00:00"))


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
