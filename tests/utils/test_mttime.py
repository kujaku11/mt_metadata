# -*- coding: utf-8 -*-
"""
time test
Created on Thu May 21 14:09:17 2020
@author: jpeacock
"""
import datetime

import numpy as np
import pandas as pd

# =============================================================================
# Imports
# =============================================================================
import pytest
from dateutil import parser as dtparser
from dateutil import tz
from obspy import UTCDateTime

from mt_metadata.common.mttime import (
    _check_timestamp,
    _fix_out_of_bounds_time_stamp,
    _localize_utc,
    calculate_leap_seconds,
    MDate,
    MTime,
    parse,
    TMAX,
    TMIN,
)


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
        "date_only": "2020-01-20+00:00",
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
        "date_keys": ["year", "month", "day"],
        "epoch_seconds": 1579522520.123,
        "input_fail": "01294055",
    }


@pytest.fixture
def sample_data():
    return {
        "valid_iso": "2020-01-20T12:15:20.123000+00:00",
        "valid_date": "2020-01-20",
        "epoch_seconds": 1579522520.123,
        "epoch_nanoseconds": 1579522520123000000,
        "invalid_date": "3000-01-01",
        "too_small_date": "1400-01-01",
        "gps_time": "2020-01-20T12:15:38.123000+00:00",
    }


# =============================================================================
# Tests
# =============================================================================
def test_string_input_date_01(setup_data, subtests):
    t = MTime(time_stamp=setup_data["date_str_01"])
    for key in setup_data["keys"][:3]:
        with subtests.test(f"{key}"):
            assert getattr(t, key) == setup_data[key]


def test_string_input_date_02(setup_data, subtests):
    t = MTime(time_stamp=setup_data["date_str_02"])
    with subtests.test("year"):
        assert t.year == setup_data["year"]
    with subtests.test("month"):
        assert t.month == setup_data["month"]
    with subtests.test("day not equal"):
        assert t.day != setup_data["day"]


def test_string_input_date_03(setup_data, subtests):
    t = MTime(time_stamp=setup_data["date_str_03"])
    for key in setup_data["keys"][:3]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]


def test_input_epoch_seconds(setup_data, subtests):
    t = MTime(time_stamp=setup_data["epoch_seconds"])
    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]


def test_input_epoch_nanoseconds(setup_data, subtests):
    t = MTime(time_stamp=setup_data["epoch_seconds"] * 1e9)
    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]


def test_input_seconds_fail():
    with pytest.raises(ValueError):
        parse(10, gps_time=True)


def test_pd_timestamp(setup_data, subtests):
    stamp = pd.Timestamp(setup_data["dt_true"])
    t = MTime(time_stamp=stamp)

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_string_input_dt(setup_data, subtests):
    t = MTime(time_stamp=setup_data["dt_str_01"])

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_str(setup_data, subtests):
    ntime = np.datetime64(setup_data["dt_str_01"])
    t = MTime(time_stamp=ntime)

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_ns(setup_data, subtests):
    ntime = np.datetime64(int(setup_data["epoch_seconds"] * 1e9), "ns")
    t = MTime(time_stamp=ntime)

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_us(setup_data, subtests):
    ntime = np.datetime64(int(setup_data["epoch_seconds"] * 1e6), "us")
    t = MTime(time_stamp=ntime)

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_np_datetime64_ms(setup_data, subtests):
    ntime = np.datetime64(int(setup_data["epoch_seconds"] * 1e3), "ms")
    t = MTime(time_stamp=ntime)

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_obspy_utcdatetime(setup_data, subtests):
    t = MTime(time_stamp=UTCDateTime(setup_data["dt_true"]))

    for key in setup_data["keys"]:
        with subtests.test(key):
            assert getattr(t, key) == setup_data[key]

    with subtests.test("isoformat"):
        assert t.isoformat() == setup_data["dt_true"]

    with subtests.test("epoch seconds"):
        assert pytest.approx(t.epoch_seconds, 0.0001) == setup_data["epoch_seconds"]


def test_input_fail(setup_data):
    with pytest.raises(ValueError):
        parse(setup_data["input_fail"])


def test_input_none(subtests):
    for t_value in [None, "", "None", "NONE", "none"]:
        with subtests.test(f"None value: {t_value}"):
            t = MTime(time_stamp=t_value)
            assert t.isoformat() == "1980-01-01T00:00:00+00:00"


def test_compare_dt(subtests):
    dt_01 = MTime()
    dt_02 = MTime()

    with subtests.test("equality"):
        assert dt_01 == dt_02

    with subtests.test("equality with string"):
        assert dt_01 == dt_02.iso_str

    with subtests.test("equality with nanoseconds"):
        assert dt_01 == (dt_02.epoch_seconds * 1e9)

    with subtests.test("greater than or equal"):
        assert dt_01 >= dt_02

    with subtests.test("less than or equal"):
        assert dt_01 <= dt_02


def test_no_tz(subtests):
    dt_obj = dtparser.isoparse("2020-01-20 12:15:20.123")
    with subtests.test("timezone is None"):
        assert dt_obj.tzinfo is None


def test_tz(subtests):
    dt_obj = dtparser.isoparse("2020-01-20T12:15:20.123000+00:00")
    with subtests.test("timezone is UTC"):
        assert isinstance(dt_obj.tzinfo, tz.tzutc)


def test_hash(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    with subtests.test("hash equality"):
        assert hash(t1) == hash(t2)


def test_add_time(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + 30

    with subtests.test("addition result"):
        assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"

    with subtests.test("result type"):
        assert isinstance(t2, MTime)


def test_add_time_datetime_timedelta(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + datetime.timedelta(seconds=30)

    with subtests.test("addition result"):
        assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"

    with subtests.test("result type"):
        assert isinstance(t2, MTime)


def test_add_time_np_timedelta(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + np.timedelta64(30, "s")

    with subtests.test("addition result"):
        assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"

    with subtests.test("result type"):
        assert isinstance(t2, MTime)


def test_add_time_fail():
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    with pytest.raises(ValueError):
        t1 + "invalid"


def test_subtract_time(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = t1 + 30
    with subtests.test("subtraction result"):
        assert (t2 - t1) == 30


def test_subtract_timedelta(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    t2 = pd.Timedelta(seconds=30)
    result = t1 - t2
    with subtests.test("subtraction result"):
        assert result.isoformat() == "2020-01-20T12:14:50.123000+00:00"


def test_too_large(subtests):
    t1 = MTime(time_stamp="3000-01-01T00:00:00")
    with subtests.test("too large date"):
        assert t1.isoformat() == TMAX.isoformat()


def test_too_small(subtests):
    t1 = MTime(time_stamp="1400-01-01T00:00:00")
    with subtests.test("too small date"):
        assert t1.isoformat() == TMIN.isoformat()


def test_utc_too_large(subtests):
    t1 = MTime(time_stamp=UTCDateTime("3000-01-01"))
    with subtests.test("UTC too large date"):
        assert t1.isoformat() == TMAX.isoformat()


def test_utc_too_small(subtests):
    t1 = MTime(time_stamp=UTCDateTime("1400-01-01"))
    with subtests.test("UTC too small date"):
        assert t1.isoformat() == TMIN.isoformat()


def test_gps_time(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00", gps_time=True)
    gps_time = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00") - 18
    with subtests.test("GPS time adjustment"):
        assert t1 == gps_time


def test_localize_utc(subtests):
    t1 = MTime(time_stamp="2020-01-20T12:15:20.123000+00:00")
    stamp = _localize_utc(t1.time_stamp)
    with subtests.test("timezone is not None"):
        assert stamp.tzinfo is not None


def test_check_timestamp_too_large(subtests):
    t1 = pd.Timestamp("3000-01-01T00:00:00")
    too_large, t2 = _check_timestamp(t1)

    with subtests.test("timestamp bounds"):
        assert t2 == TMAX

    with subtests.test("too_large flag"):
        assert too_large is True


def test_check_timestamp_too_small(subtests):
    t1 = pd.Timestamp("1400-01-01T00:00:00")
    too_small, t2 = _check_timestamp(t1)

    with subtests.test("timestamp bounds"):
        assert t2 == TMIN

    with subtests.test("too_small flag"):
        assert too_small is True


def test_fix_out_of_bounds_too_large(subtests):
    dt = dtparser.parse("3000-01-01T00:00:00")
    stamp, too_large = _fix_out_of_bounds_time_stamp(dt)

    with subtests.test("fix bounds"):
        assert stamp == TMAX

    with subtests.test("too_large flag"):
        assert too_large is True


def test_fix_out_of_bounds_too_small(subtests):
    dt = dtparser.parse("1400-01-01T00:00:00")
    stamp, too_small = _fix_out_of_bounds_time_stamp(dt)

    with subtests.test("fix bounds"):
        assert stamp == TMIN

    with subtests.test("too_small flag"):
        assert too_small is True


def test_bad_24hour(subtests):
    t = MTime(time_stamp="2020-01-01T24:00:00")
    with subtests.test("24-hour handling"):
        assert t.isoformat() == "2020-01-02T00:00:00+00:00"


# =============================================================================
# Tests for utility functions
# =============================================================================
def test_util_localize_utc(subtests):
    stamp = pd.Timestamp("2020-01-20T12:15:20", tz="UTC")
    localized = _localize_utc(stamp)

    with subtests.test("timezone is not None"):
        assert localized.tzinfo is not None

    with subtests.test("timezone name"):
        assert localized.tzname() == "UTC"


def test_util_check_timestamp_too_large(subtests):
    t1 = pd.Timestamp("3000-01-01T00:00:00", tz="UTC")
    too_large, t2 = _check_timestamp(t1)

    with subtests.test("timestamp bounds"):
        assert t2 == TMAX

    with subtests.test("too_large flag"):
        assert too_large is True


def test_util_check_timestamp_too_small(subtests):
    t1 = pd.Timestamp("1400-01-01T00:00:00", tz="UTC")
    too_small, t2 = _check_timestamp(t1)

    with subtests.test("timestamp bounds"):
        assert t2 == TMIN

    with subtests.test("too_small flag"):
        assert too_small is True


def test_util_fix_out_of_bounds_time_stamp_too_large(subtests):
    dt = datetime.datetime(3000, 1, 1)
    stamp, too_large = _fix_out_of_bounds_time_stamp(dt)

    with subtests.test("fix bounds"):
        assert stamp == TMAX

    with subtests.test("too_large flag"):
        assert too_large is True


def test_util_fix_out_of_bounds_time_stamp_too_small(subtests):
    dt = datetime.datetime(1400, 1, 1)
    stamp, too_small = _fix_out_of_bounds_time_stamp(dt)

    with subtests.test("fix bounds"):
        assert stamp == TMIN

    with subtests.test("too_small flag"):
        assert too_small is True


def test_calculate_leap_seconds(subtests):
    test_cases = [
        (1981, 7, 1, 1),
        (2017, 1, 1, 18),
        (2025, 1, 1, 18),
    ]

    for year, month, day, expected in test_cases:
        with subtests.test(f"leap seconds {year}-{month}-{day}"):
            assert calculate_leap_seconds(year, month, day) == expected


# =============================================================================
# Tests for parse function
# =============================================================================
def test_parse_iso_string(sample_data, subtests):
    result = parse(sample_data["valid_iso"])
    with subtests.test("ISO string parsing"):
        assert result.isoformat() == sample_data["valid_iso"]


def test_parse_epoch_seconds(sample_data, subtests):
    result = parse(sample_data["epoch_seconds"])
    with subtests.test("epoch seconds parsing"):
        assert result.timestamp() == pytest.approx(sample_data["epoch_seconds"], 0.0001)


def test_parse_epoch_nanoseconds(sample_data, subtests):
    result = parse(sample_data["epoch_nanoseconds"])
    with subtests.test("epoch nanoseconds parsing"):
        assert result.timestamp() == pytest.approx(sample_data["epoch_seconds"], 0.0001)


def test_parse_invalid_date(sample_data, subtests):
    result = parse(sample_data["invalid_date"])
    with subtests.test("invalid date parsing"):
        assert result == TMAX


def test_parse_too_small_date(sample_data, subtests):
    result = parse(sample_data["too_small_date"])
    with subtests.test("too small date parsing"):
        assert result == TMIN


def test_parse_gps_time(sample_data, subtests):
    result = parse(sample_data["gps_time"], gps_time=True)
    with subtests.test("GPS time parsing"):
        assert result.isoformat() == sample_data["valid_iso"]


# =============================================================================
# Tests for MTime class
# =============================================================================
def test_mtime_default(subtests):
    t = MTime()
    with subtests.test("default value"):
        assert t.isoformat() == "1980-01-01T00:00:00+00:00"


def test_mtime_from_iso_string(sample_data, subtests):
    t = MTime(time_stamp=sample_data["valid_iso"])
    with subtests.test("ISO string initialization"):
        assert t.isoformat() == sample_data["valid_iso"]


def test_mtime_from_epoch_seconds(sample_data, subtests):
    t = MTime(time_stamp=sample_data["epoch_seconds"])
    with subtests.test("epoch seconds initialization"):
        assert t.epoch_seconds == pytest.approx(sample_data["epoch_seconds"], 0.0001)


def test_mtime_comparison(sample_data, subtests):
    t1 = MTime(time_stamp=sample_data["valid_iso"])
    t2 = MTime(time_stamp=sample_data["valid_iso"])

    with subtests.test("equality"):
        assert t1 == t2

    with subtests.test("inequality"):
        assert not t1 != t2

    with subtests.test("less than or equal"):
        assert t1 <= t2

    with subtests.test("greater than or equal"):
        assert t1 >= t2


def test_mtime_add_time(sample_data, subtests):
    t = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t + 30
    with subtests.test("addition"):
        assert t2.isoformat() == "2020-01-20T12:15:50.123000+00:00"


def test_mtime_subtract_time(sample_data, subtests):
    t = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t - 30
    with subtests.test("subtraction"):
        assert t2.isoformat() == "2020-01-20T12:14:50.123000+00:00"


def test_mtime_subtract_timestamps(sample_data, subtests):
    t1 = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t1 + 30
    diff = t2 - t1
    with subtests.test("timestamp difference"):
        assert diff == 30


def test_mtime_setters(sample_data, subtests):
    t = MTime(time_stamp=sample_data["valid_iso"])
    t.year = 2025
    t.month = 12
    t.day = 31

    with subtests.test("year setter"):
        assert t.year == 2025

    with subtests.test("month setter"):
        assert t.month == 12

    with subtests.test("day setter"):
        assert t.day == 31

    with subtests.test("isoformat after setters"):
        assert t.isoformat().startswith("2025-12-31")


def test_mtime_hash(sample_data, subtests):
    t = MTime(time_stamp=sample_data["valid_iso"])
    with subtests.test("hash"):
        assert hash(t) == hash(sample_data["valid_iso"])


def test_mtime_copy(sample_data, subtests):
    t1 = MTime(time_stamp=sample_data["valid_iso"])
    t2 = t1.copy()

    with subtests.test("equality after copy"):
        assert t1 == t2

    with subtests.test("identity after copy"):
        assert t1 is not t2


# =============================================================================
# Tests for MDate class
# =============================================================================
def test_mdate_default(subtests):
    d = MDate()
    with subtests.test("default value"):
        assert d.isoformat() == "1980-01-01"


def test_mdate_from_date_string(sample_data, subtests):
    d = MDate(time_stamp=sample_data["valid_date"])
    with subtests.test("date string initialization"):
        assert d.isoformat() == "2020-01-20"


def test_mdate_from_iso_string(sample_data, subtests):
    d = MDate(time_stamp=sample_data["valid_iso"])
    with subtests.test("ISO string initialization"):
        assert d.isoformat() == "2020-01-20"


def test_mdate_from_mtime(sample_data, subtests):
    t = MTime(time_stamp=sample_data["valid_iso"])
    d = MDate(time_stamp=t)
    with subtests.test("MTime initialization"):
        assert d.isoformat() == "2020-01-20"


def test_mdate_comparison(subtests):
    d1 = MDate(time_stamp="2020-01-20")
    d2 = MDate(time_stamp="2020-01-20")
    d3 = MDate(time_stamp="2020-01-21")

    with subtests.test("equality"):
        assert d1 == d2

    with subtests.test("inequality"):
        assert d1 != d3

    with subtests.test("less than"):
        assert d1 < d3

    with subtests.test("greater than"):
        assert d3 > d1


def test_mdate_add_days(subtests):
    d = MDate(time_stamp="2020-01-20")
    d2 = d + pd.Timedelta(5, "days")

    with subtests.test("addition"):
        assert d2.isoformat() == "2020-01-25"

    with subtests.test("result type"):
        assert isinstance(d2, MDate)


def test_mdate_subtract_days(subtests):
    d = MDate(time_stamp="2020-01-20")
    d2 = d - pd.Timedelta(5, "days")

    with subtests.test("subtraction"):
        assert d2.isoformat() == "2020-01-15"

    with subtests.test("result type"):
        assert isinstance(d2, MDate)


def test_mdate_difference(subtests):
    d1 = MDate(time_stamp="2020-01-20")
    d2 = MDate(time_stamp="2020-01-25")

    with subtests.test("date difference"):
        assert d2 - d1 == 5


def test_mdate_setters(subtests):
    d = MDate(time_stamp="2020-01-20")
    d.year = 2025
    d.month = 12
    d.day = 31

    with subtests.test("year setter"):
        assert d.year == 2025

    with subtests.test("month setter"):
        assert d.month == 12

    with subtests.test("day setter"):
        assert d.day == 31

    with subtests.test("isoformat after setters"):
        assert d.isoformat() == "2025-12-31"


def test_mdate_str(subtests):
    d = MDate(time_stamp="2020-01-20")
    with subtests.test("string representation"):
        assert str(d) == "2020-01-20"


def test_mdate_copy(subtests):
    d1 = MDate(time_stamp="2020-01-20")
    d2 = d1.copy()

    with subtests.test("equality after copy"):
        assert d1 == d2

    with subtests.test("identity after copy"):
        assert d1 is not d2


def test_mdate_to_mtime(subtests):
    d = MDate(time_stamp="2020-01-20")
    t = MTime(time_stamp=d.time_stamp)

    with subtests.test("conversion to MTime"):
        assert isinstance(t, MTime)

    with subtests.test("date components"):
        assert t.year == d.year
        assert t.month == d.month
        assert t.day == d.day

    with subtests.test("time components"):
        assert t.hour == 0
        assert t.minutes == 0
        assert t.seconds == 0


if __name__ == "__main__":
    pytest.main([__file__])
