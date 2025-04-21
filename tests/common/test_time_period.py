import pytest
import pandas as pd
import numpy as np
from mt_metadata.timeseries import TimePeriod
from mt_metadata.utils.mttime import MTime


def test_time_period_default_values():
    """
    Test the default values of the TimePeriod model.
    """
    time_period = TimePeriod()
    assert time_period.start.isoformat() == "1980-01-01T00:00:00+00:00"
    assert time_period.end.isoformat() == "1980-01-01T00:00:00+00:00"


def test_time_period_custom_values():
    """
    Test the TimePeriod model with custom start and end values.
    """
    start_time = "2020-02-01T09:23:45.453670+00:00"
    end_time = "2020-02-04T16:23:45.453670+00:00"
    time_period = TimePeriod(start=start_time, end=end_time)

    assert time_period.start.isoformat() == start_time
    assert time_period.end.isoformat() == end_time


def test_time_period_with_epoch():
    """
    Test the TimePeriod model with epoch time as input.
    """
    start_time = 1580541825.453670
    end_time = 1580826225.453670
    time_period = TimePeriod(start=start_time, end=end_time)

    assert time_period.start.isoformat() == "2020-02-01T07:23:45.453670025+00:00"
    assert time_period.end.isoformat() == "2020-02-04T14:23:45.453670025+00:00"


def test_time_period_with_np_datetime64():
    """
    Test the TimePeriod model with numpy datetime64 as input.
    """
    start_time = np.datetime64("2020-02-01T09:23:45.453670+00:00")
    end_time = np.datetime64("2020-02-04T16:23:45.453670+00:00")
    time_period = TimePeriod(start=start_time, end=end_time)

    assert time_period.start.isoformat() == "2020-02-01T09:23:45.453670+00:00"
    assert time_period.end.isoformat() == "2020-02-04T16:23:45.453670+00:00"


def test_time_period_with_invalid_time():
    """
    Test the TimePeriod model with invalid time values.
    """
    with pytest.raises(ValueError):
        TimePeriod(start="invalid-time", end="2020-02-04T16:23:45.453670+00:00")

    with pytest.raises(ValueError):
        TimePeriod(start="2020-02-01T09:23:45.453670+00:00", end="invalid-time")


def test_time_period_with_mtime():
    """
    Test the TimePeriod model with MTime objects as input.
    """
    start_time = MTime(time_stamp="2020-02-01T09:23:45.453670+00:00")
    end_time = MTime(time_stamp="2020-02-04T16:23:45.453670+00:00")
    time_period = TimePeriod(start=start_time, end=end_time)

    assert time_period.start.isoformat() == "2020-02-01T09:23:45.453670+00:00"
    assert time_period.end.isoformat() == "2020-02-04T16:23:45.453670+00:00"
