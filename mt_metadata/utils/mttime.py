# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:10:46 2020

@author: jpeacock
"""
# =============================================================================
# IMPORTS
# =============================================================================
import datetime
import numpy as np
import pandas as pd
from copy import deepcopy

from .mt_logger import setup_logger
from mt_metadata import LOG_LEVEL

# =============================================================================
#  Get leap seconds
# =============================================================================
leap_second_dict = {
    0: {"min": datetime.date(1980, 1, 1), "max": datetime.date(1981, 7, 1)},
    1: {"min": datetime.date(1981, 7, 1), "max": datetime.date(1982, 7, 1)},
    2: {"min": datetime.date(1982, 7, 1), "max": datetime.date(1983, 7, 1)},
    3: {"min": datetime.date(1983, 7, 1), "max": datetime.date(1985, 7, 1)},
    4: {"min": datetime.date(1985, 7, 1), "max": datetime.date(1988, 1, 1)},
    5: {"min": datetime.date(1988, 1, 1), "max": datetime.date(1990, 1, 1)},
    6: {"min": datetime.date(1990, 1, 1), "max": datetime.date(1991, 1, 1)},
    7: {"min": datetime.date(1991, 1, 1), "max": datetime.date(1992, 7, 1)},
    8: {"min": datetime.date(1992, 7, 1), "max": datetime.date(1993, 7, 1)},
    9: {"min": datetime.date(1993, 7, 1), "max": datetime.date(1994, 7, 1)},
    10: {"min": datetime.date(1994, 7, 1), "max": datetime.date(1996, 1, 1)},
    11: {"min": datetime.date(1996, 1, 1), "max": datetime.date(1997, 7, 1)},
    12: {"min": datetime.date(1997, 7, 1), "max": datetime.date(1999, 1, 1)},
    13: {"min": datetime.date(1999, 1, 1), "max": datetime.date(2006, 1, 1)},
    14: {"min": datetime.date(2006, 1, 1), "max": datetime.date(2009, 1, 1)},
    15: {"min": datetime.date(2009, 1, 1), "max": datetime.date(2012, 6, 30)},
    16: {"min": datetime.date(2012, 7, 1), "max": datetime.date(2015, 7, 1)},
    17: {"min": datetime.date(2015, 7, 1), "max": datetime.date(2016, 12, 31)},
    18: {"min": datetime.date(2017, 1, 1), "max": datetime.date(2025, 7, 1)},
}


def calculate_leap_seconds(year, month, day):
    """
    get the leap seconds for the given year to convert GPS time to UTC time

    .. note:: GPS time started in 1980

    .. note:: GPS time is leap seconds ahead of UTC time, therefore you
              should subtract leap seconds from GPS time to get UTC time.

    =========================== ===============================================
    Date Range                  Leap Seconds
    =========================== ===============================================
    1981-07-01 - 1982-07-01     1
    1982-07-01 - 1983-07-01     2
    1983-07-01 - 1985-07-01     3
    1985-07-01 - 1988-01-01     4
    1988-01-01 - 1990-01-01     5
    1990-01-01 - 1991-01-01     6
    1991-01-01 - 1992-07-01     7
    1992-07-01 - 1993-07-01     8
    1993-07-01 - 1994-07-01     9
    1994-07-01 - 1996-01-01     10
    1996-01-01 - 1997-07-01     11
    1997-07-01 - 1999-01-01     12
    1999-01-01 - 2006-01-01     13
    2006-01-01 - 2009-01-01     14
    2009-01-01 - 2012-07-01     15
    2012-07-01 - 2015-07-01     16
    2015-07-01 - 2017-01-01     17
    2017-01-01 - ????-??-??     18
    =========================== ===============================================

    """

    # make the date a datetime object, easier to test
    given_date = datetime.date(int(year), int(month), int(day))

    # made an executive decision that the date can be equal to the min, but
    # not the max, otherwise get an error.
    for leap_key in sorted(leap_second_dict.keys()):
        if (
            given_date < leap_second_dict[leap_key]["max"]
            and given_date >= leap_second_dict[leap_key]["min"]
        ):
            return int(leap_key)

    return None


# ==============================================================================
# convenience date-time container
# ==============================================================================
class MTime:
    """
    Date and Time container based on datetime and dateutil.parsers

    Will read in a string or a epoch seconds into a datetime.datetime object
    assuming the time zone is UTC.  If UTC is not the timezone you need to
    correct the time before inputing.  Use datetime.timezone to shift time.

    Outputs can be an ISO formatted string YYYY-MM-DDThh:mm:ss.ssssss+00:00:

        >>> t = MTtime()
        >>> t.iso_str
        '1980-01-01T00:00:00+00:00'

    .. note:: if microseconds are 0 they are omitted.

    or Epoch seconds (float):

        >>> t.epoch_seconds
        315532800.0


    Convenience getters/setters are provided as properties for the different
    parts of time.

        >>> t = MTtime()
        >>> t.year = 2020
        >>> t.year
        2020

    """

    def __init__(self, time=None, gps_time=False):

        self.logger = setup_logger(
            "{0}.{1}".format(__name__, self.__class__.__name__),
            fn="mt_time.log",
            level=LOG_LEVEL,
        )

        self.from_str(time)

        if gps_time:
            leap_seconds = calculate_leap_seconds(
                self.year, self.month, self.day
            )
            self.logger.debug(
                f"Converting GPS time to UTC with {leap_seconds} leap seconds"
            )
            self._time_stamp -= pd.Timedelta(seconds=leap_seconds)

    def __str__(self):
        return self.isoformat()

    def __repr__(self):
        return self.isoformat()

    def __eq__(self, other):

        if not isinstance(other, MTime):
            other = MTime(other)

        return bool(self._time_stamp == other._time_stamp)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, MTime):
            other = MTime(other)

        return bool(self._time_stamp < other._time_stamp)

    def __le__(self, other):
        if not isinstance(other, MTime):
            other = MTime(other)

        return bool(self._time_stamp <= other._time_stamp)

    def __gt__(self, other):
        return not self.__lt__(other)

    def __ge__(self, other):
        if not isinstance(other, MTime):
            other = MTime(other)

        return bool(self._time_stamp >= other._time_stamp)

    def __add__(self, other):
        """
        add time only using datetime.timedelta, otherwise it does not make
        sense to at 2 times together.

        """
        if isinstance(other, (int, float, datetime.timedelta, np.timede)):
            other = pd.Timedelta(seconds=other)
            self.logger.debug("Assuming other time is in seconds")

        if not isinstance(other, (pd.Timedelta)):
            msg = (
                "Adding times stamps does not make sense, use either "
                "pd.Timedelta or seconds as a float "
            )
            self.logger.error(msg)
            raise ValueError(msg)

        return MTime(self._time_stamp + other)

    def __sub__(self, other):
        """
        Get the time difference between to times in seconds.

        :param other: other time value
        :type other: [ str | float | int | datetime.datetime | np.datetime64 ]
        :return: time difference in seconds
        :rtype: float

        """

        if not isinstance(other, MTime):
            other = MTime(other)

        return (self._time_stamp - other._time_stamp).total_seconds()

    def __hash__(self):
        return hash(self.isoformat())

    @property
    def iso_str(self):
        return self._time_stamp.isoformat()

    @property
    def iso_no_tz(self):
        return self._time_stamp.isoformat().split("+", 1)[0]

    @property
    def epoch_seconds(self):
        return self._time_stamp.timestamp()

    @epoch_seconds.setter
    def epoch_seconds(self, seconds):
        self.logger.debug(
            "reading time from epoch seconds, assuming UTC " + "time zone"
        )
        self._time_stamp = pd.Timestamp(seconds, tz="UTC")

    def from_str(self, dt_str):
        """
        Parse a date-time string using dateutil.parser

        Need to use dateutil.parser.isoparser to get correct tzinfo=tzutc
        If the input is a weird date string then try to use parse.

        :param dt_str: date-time string
        :type: string


        """

        if dt_str is None:
            self.logger.warning(
                "Time string is None, setting to 1980-01-01:00:00:00"
            )
            stamp = pd.Timestamp("1980-01-01T00:00:00+00:00")
        else:
            if isinstance(dt_str, pd.Timestamp):
                stamp = dt_str.tz_convert("UTC")

            else:
                try:
                    stamp = pd.Timestamp(dt_str)
                except (TypeError, ValueError):
                    msg = f"Could not parse {dt_str} into a readable date-time"
                    self.logger.error(msg)
                    raise ValueError(msg)

        # check time zone and enforce UTC
        if stamp.tz is None:
            stamp = stamp.tz_localize("UTC").tz_convert("UTC")

        # there can be a machine round off error, if it is close to 1 round to
        # microseconds
        if round(stamp.nanosecond / 1000) == 1:
            stamp = stamp.round(freq="us")

        self._time_stamp = stamp

    @property
    def date(self):
        return self._time_stamp.date().isoformat()

    @property
    def year(self):
        return self._time_stamp.year

    @year.setter
    def year(self, value):
        self._time_stamp = self._time_stamp.replace(year=value)

    @property
    def month(self):
        return self._time_stamp.month

    @month.setter
    def month(self, value):
        self._time_stamp = self._time_stamp.replace(month=value)

    @property
    def day(self):
        return self._time_stamp.day

    @day.setter
    def day(self, value):
        self._time_stamp = self._time_stamp.replace(day=value)

    @property
    def hour(self):
        return self._time_stamp.hour

    @hour.setter
    def hour(self, value):
        self._time_stamp = self._time_stamp.replace(hour=value)

    @property
    def minutes(self):
        return self._time_stamp.minute

    @minutes.setter
    def minutes(self, value):
        self._time_stamp = self._time_stamp.replace(minute=value)

    @property
    def seconds(self):
        return self._time_stamp.second

    @seconds.setter
    def seconds(self, value):
        self._time_stamp = self._time_stamp.replace(second=value)

    @property
    def microseconds(self):
        return self._time_stamp.microsecond

    @microseconds.setter
    def microseconds(self, value):
        self._time_stamp = self._time_stamp.replace(microsecond=value)

    @property
    def nanoseconds(self):
        return self._time_stamp.nanosecond

    @nanoseconds.setter
    def nanoseconds(self, value):
        self._time_stamp = self._time_stamp.replace(nanosecond=value)

    def now(self):
        """
        set date time to now

        :return: current UTC time
        :rtype: datetime with UTC timezone

        """
        self._time_stamp = pd.Timestamp.utcnow()

        return self

    def copy(self):
        """make a copy of the time"""
        return deepcopy(self)

    def isoformat(self):
        """

        :return: Date-time in ISO format
        :rtype: string

        """
        return self._time_stamp.isoformat()

    def isodate(self):
        """

        :return: Date in ISO format
        :rtype: string

        """
        return self._time_stamp.isodate()

    def isocalendar(self):
        """

        :return: Calendar Date in ISO format
        :rtype: string

        """
        return self._time_stamp.isocalendar()


def get_now_utc():
    """
    Get the current time in UTC format
    :return: ISO formatted string of current time in UTC
    :rtype: string

    """

    m_obj = MTime()
    m_obj.now()
    return m_obj.iso_str
