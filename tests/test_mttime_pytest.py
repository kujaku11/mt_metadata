# -*- coding: utf-8 -*-
"""
time test
Created on Thu May 21 14:09:17 2020
@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import pytest
from dateutil import parser as dtparser
from dateutil import tz
import datetime
import pandas as pd
import numpy as np

from mt_metadata.utils.mttime import (
    MTime,
    parse,
    _localize_utc,
    _check_timestamp,
    _fix_out_of_bounds_time_stamp,
    TMIN,
    TMAX,
    calculate_leap_seconds,
)
from obspy import UTCDateTime


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def setup_data():
    return {
        "date_str_01": "2020-01-20",
        "date_str_02": "01-02-20",
        "date_str_03": "2020-20-01",
        "year": 2020,
        "month": 1,
        "day": 20,
        "hour": 12,
        "minutes": 15,
        "seconds": 20,
        "microseconds": 123000,
        "dt_str_01": "2020-01-20 12:15:20.123",
        "dt_true": "2020-01-20T12:15:20.123000+00:00",
        "add_time_true": "2020-01-20T12:15:50.123000+00:00",
        "keys": [
            "year",
            "month",
            "day",
            "hour",
            "minutes",
            "seconds",
            "microseconds",
        ],
        "epoch_seconds": 1579522520.123,
        "input_fail": "01294055",
    }


# =============================================================================
# Tests
# =============================================================================
def test_string_input_date_01(setup_data):
    t = MTime(time_stamp=setup_data["date_str_01"])
    for key in setup_data["keys"][:3]:
        assert getattr(t, key) == setup_data[key]


def test_string_input_date_02(setup_data):
    t = MTime(time_stamp=setup_data["date_str_02"])
    assert t.year == setup_data["year"]
    assert t.month == setup_data["month"]
    assert t.day != setup_data["day"]


def test_string_input_date_03(setup_data):
    t = MTime(time_stamp=setup_data["date_str_03"])
    for key in setup_data["keys"][:3]:
        assert getattr(t, key) == setup_data[key]


def test_input_epoch_seconds(setup_data):
    t = MTime(time_stamp=setup_data["epoch_seconds"])
    assert t.isoformat() == setup_data["dt_true"]


def test_input_epoch_nanoseconds(setup_data):
    t = MTime(time_stamp=setup_data["epoch_seconds"] * 1e9)
    assert t.isoformat() == setup_data["dt_true"]


def test_input_seconds_fail():
    with pytest.raises(ValueError):
        parse(10, gps_time=True)


def test_pd_timestamp(setup_data):
    stamp = pd.Timestamp(setup_data["dt_true"])
    t = MTime(time_stamp=stamp)
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_string_input_dt(setup_data):
    t = MTime(time_stamp=setup_data["dt_str_01"])
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_str(setup_data):
    ntime = np.datetime64(setup_data["dt_str_01"])
    t = MTime(time_stamp=ntime)
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_ns(setup_data):
    ntime = np.datetime64(int(setup_data["epoch_seconds"] * 1e9), "ns")
    t = MTime(time_stamp=ntime)
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_us(setup_data):
    ntime = np.datetime64(int(setup_data["epoch_seconds"] * 1e6), "us")
    t = MTime(time_stamp=ntime)
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_ms(setup_data):
    ntime = np.datetime64(int(setup_data["epoch_seconds"] * 1e3), "ms")
    t = MTime(time_stamp=ntime)
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_obspy_utcdatetime(setup_data):
    t = MTime(time_stamp=UTCDateTime(setup_data["dt_true"]))
    for key in setup_data["keys"]:
        assert getattr(t, key) == setup_data[key]
    assert t.isoformat() == setup_data["dt_true"]
    assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_input_fail(setup_data):
    with pytest.raises(ValueError):
        parse(setup_data["input_fail"])


def test_input_none():
    for t_value in [None, "", "None", "NONE", "none"]:
        t = MTime(time_stamp=t_value)
        assert t.isoformat() == "1980-01-01T00:00:00+00:00"


def test_compare_dt():
    dt_01 = MTime()
    dt_02 = MTime()

    assert dt_01 == dt_02
    assert dt_01 == dt_02.iso_str
    assert dt_01 == (dt_02.epoch_seconds * 1e9)
    assert dt_01 >= dt_02
    assert dt_01 <= dt_02


def test_no_tz():
    dt_obj = dtparser.isoparse("2020-01-20 12:15:20.123")
    assert dt_obj.tzinfo is None


def test_tz():
    dt_obj = dtparser.isoparse("2020-01-20T12:15:20.123000+00:00")
    assert isinstance(dt_obj.tzinfo, tz.tzutc)


def test_hash():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    assert hash(t1) == hash(t2)


def test_add_time():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + 30
    assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"
    assert isinstance(t2, MTime)


def test_add_time_datetime_timedelta():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + datetime.timedelta(seconds=30)
    assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"
    assert isinstance(t2, MTime)


def test_add_time_np_timedelta():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + np.timedelta64(30, "s")
    assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"
    assert isinstance(t2, MTime)


def test_add_time_fail():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    with pytest.raises(ValueError):
        t1 + "invalid"


def test_subtract_time():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + 30
    assert (t2 - t1) == 30


def test_subtract_timedelta():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = pd.Timedelta(seconds=30)
    result = t1 - t2
    assert result.isoformat() == "2020-01-20T12:14:50.123000+00:00"


def test_too_large():
    t1 = MTime(time_stamp="3000-01-01T00:00:00")
    assert t1.isoformat() == pd.Timestamp.max.isoformat()


def test_too_small():
    t1 = MTime(time_stamp="1400-01-01T00:00:00")
    assert t1.isoformat() == pd.Timestamp.min.isoformat()


def test_utc_too_large():
    t1 = MTime(time_stamp=UTCDateTime("3000-01-01"))
    assert t1.isoformat() == pd.Timestamp.max.isoformat()


def test_utc_too_small():
    t1 = MTime(time_stamp=UTCDateTime("1400-01-01"))
    assert t1.isoformat() == pd.Timestamp.min.isoformat()


def test_gps_time():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00", gps_time=True)
    gps_time = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00") - 13
    assert t1 == gps_time


def test_localize_utc():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    stamp = _localize_utc(t1.time_stamp)
    assert stamp.tzinfo is not None


def test_check_timestamp_too_large():
    t1 = pd.Timestamp("3000-01-01T00:00:00")
    too_large, t2 = _check_timestamp(t1)
    assert t2 == TMAX
    assert too_large is True


def test_check_timestamp_too_small():
    t1 = pd.Timestamp("1400-01-01T00:00:00")
    too_small, t2 = _check_timestamp(t1)
    assert t2 == TMIN
    assert too_small is True


def test_fix_out_of_bounds_too_large():
    dt = dtparser.parse("3000-01-01T00:00:00")
    stamp, too_large = _fix_out_of_bounds_time_stamp(dt)
    assert stamp == TMAX
    assert too_large is True


def test_fix_out_of_bounds_too_small():
    dt = dtparser.parse("1400-01-01T00:00:00")
    stamp, too_small = _fix_out_of_bounds_time_stamp(dt)
    assert stamp == TMIN
    assert too_small is True


def test_bad_24hour():
    t = MTime(time_stamp="2020-01-01T24:00:00")
    assert t.isoformat() == "2020-01-02T00:00:00+00:00"


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def sample_data():
    return {
        "valid_iso": "2020-01-20T12:15:20.123000+00:00",
        "valid_date": "2020-01-20",
        "epoch_seconds": 1579522520.123,
        "epoch_nanoseconds": 1579522520123000000,
        "invalid_date": "3000-01-01",
        "too_small_date": "1400-01-01",
        "gps_time": 631152000,  # GPS epoch time for 2000-01-01
    }


# =============================================================================
# Tests for utility functions
# =============================================================================
def test_localize_utc():
    stamp = pd.Timestamp("2020-01-20T12:15:20")
    localized = _localize_utc(stamp)
    assert localized.tzinfo is not None
    assert localized.tzinfo.zone == "UTC"


def test_check_timestamp_too_large():
    t1 = pd.Timestamp("3000-01-01T00:00:00")
    too_large, t2 = _check_timestamp(t1)
    assert t2 == TMAX
    assert too_large is True


def test_check_timestamp_too_small():
    t1 = pd.Timestamp("1400-01-01T00:00:00")
    too_small, t2 = _check_timestamp(t1)
    assert t2 == TMIN
    assert too_small is True


def test_fix_out_of_bounds_time_stamp_too_large():
    dt = datetime.datetime(3000, 1, 1)
    stamp, too_large = _fix_out_of_bounds_time_stamp(dt)
    assert stamp == TMAX
    assert too_large is True


def test_fix_out_of_bounds_time_stamp_too_small():
    dt = datetime.datetime(1400, 1, 1)
    stamp, too_small = _fix_out_of_bounds_time_stamp(dt)
    assert stamp == TMIN
    assert too_small is True


def test_calculate_leap_seconds():
    assert calculate_leap_seconds(1981, 7, 1) == 1
    assert calculate_leap_seconds(2017, 1, 1) == 18
    assert calculate_leap_seconds(2025, 1, 1) == 18


# =============================================================================
# Tests for parse function
# =============================================================================
def test_parse_iso_string(sample_data):
    result = parse(sample_data["valid_iso"])
    assert result.isoformat() == sample_data["valid_iso"]


def test_parse_epoch_seconds(sample_data):
    result = parse(sample_data["epoch_seconds"])
    assert result.timestamp() == pytest.approx(sample_data["epoch_seconds"], 0.0001)


def test_parse_epoch_nanoseconds(sample_data):
    result = parse(sample_data["epoch_nanoseconds"])
    assert result.timestamp() == pytest.approx(sample_data["epoch_seconds"], 0.0001)


def test_parse_invalid_date(sample_data):
    result = parse(sample_data["invalid_date"])
    assert result == TMAX


def test_parse_too_small_date(sample_data):
    result = parse(sample_data["too_small_date"])
    assert result == TMIN


def test_parse_gps_time(sample_data):
    result = parse(sample_data["gps_time"], gps_time=True)
    assert result.isoformat() == "2000-01-01T00:00:00+00:00"


# =============================================================================
# Tests for MTime class
# =============================================================================
def test_mtime_default():
    t = MTime()
    assert t.isoformat() == "1980-01-01T00:00:00+00:00"


def test_mtime_from_iso_string(sample_data):
    t = MTime(time_stamp=sample_data["valid_iso"])
    assert t.isoformat() == sample_data["valid_iso"]


def test_mtime_from_epoch_seconds(sample_data):
    t = MTime(time_stamp=sample_data["epoch_seconds"])
    assert t.epoch_seconds == pytest.approx(sample_data["epoch_seconds"], 0.0001)


def test_mtime_comparison(sample_data):
    t1 = MTime(time_stamp=sample_data["valid_iso"])
    t2 = MTime(time_stamp=sample_data["valid_iso"])
    assert t1 == t2
    assert not t1 != t2
    assert t1 <= t2
    assert t1 >= t2


def test_mtime_add_time(sample_data):
    t = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t + 30
    assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"


def test_mtime_subtract_time(sample_data):
    t = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t - 30
    assert t2.isoformat() == "2020-01-20T12:14:50.123000+00:00"


def test_mtime_subtract_timestamps(sample_data):
    t1 = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t1 + 30
    diff = t2 - t1
    assert diff == 30


def test_mtime_setters(sample_data):
    t = MTime(time_stamp=sample_data["valid_iso"])
    t.year = 2025
    t.month = 12
    t.day = 31
    assert t.isoformat().startswith("2025-12-31")


def test_mtime_hash(sample_data):
    t = MTime(time_stamp=sample_data["valid_iso"])
    assert hash(t) == hash(sample_data["valid_iso"])


def test_mtime_copy(sample_data):
    t1 = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t1.copy()
    assert t1 == t2
    assert t1 is not t2
