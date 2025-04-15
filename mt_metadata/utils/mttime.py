# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:10:46 2020

For dealing with obsy.core.UTCDatetime and an soft requirement imports
have a look at https://github.com/pydantic/pydantic/discussions/3673.

@author: jpeacock
"""
# =============================================================================
# IMPORTS
# =============================================================================
from copy import deepcopy
import datetime
from dateutil.parser import parse as dtparser
import numpy as np
import pandas as pd
from pandas._libs.tslibs import OutOfBoundsDatetime
from typing import Optional, Annotated
from loguru import logger

try:
    from obspy.core.utcdatetime import UTCDateTime  # for type hinting

    from_obspy = True
except ImportError:
    from_obspy = False

from pydantic import (
    Field,
    ConfigDict,
    ValidationInfo,
    field_validator,
)

from mt_metadata.base import MetadataBase

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


def calculate_leap_seconds(year: int, month: int, day: int) -> int:
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


# =============================================================================
#  Functions for parsing time stamps
# =============================================================================
def _localize_utc(stamp: pd.Timestamp) -> pd.Timestamp:
    """
    Localize a time stamp to UTC.  This forces a timestamp
    to have a timezone of UTC.

    Parameters
    ----------
    stamp : pd.Timestamp
        input timestamp

    Returns
    -------
    pd.Timestamp
        UTC time stamp
    """

    # check time zone and enforce UTC
    if stamp.tz is None:
        stamp = stamp.tz_localize("UTC").tz_convert("UTC")

    return stamp


# minimum and maximum time stamps for pandas
# these are the minimum and maximum time stamps for pandas
TMIN = _localize_utc(pd.Timestamp.min)
TMAX = _localize_utc(pd.Timestamp.max)


def _parse_string(dt_str: str) -> datetime.datetime:
    """
    arse string, check for order of day and month

    Parameters
    ----------
    dt_str : str
        date time string

    Returns
    -------
    datetime.datetime
        date time object

    Raises
    ------
    ValueError
        If unable to parse the string using datetime.dtparser
    """

    try:
        return dtparser(dt_str)
    except ValueError as ve:
        error_24h = "hour must be in 0..23"
        if error_24h in ve.args[0]:
            # hh=24 was supplied -- this is legal if it is midnight
            one_hour_earlier_dt_str = dt_str.replace("T24", "T23")
            one_hour_earlier_result = dtparser(one_hour_earlier_dt_str)
            result = one_hour_earlier_result + datetime.timedelta(hours=1)
            return result
        else:
            try:
                return dtparser(dt_str, dayfirst=True)
            except ValueError:
                msg = (
                    "Could not parse string %s check formatting, "
                    "should be YYYY-MM-DDThh:mm:ss.ns"
                )
                logger.error(msg, dt_str)
                raise ValueError(msg % dt_str)


def _fix_out_of_bounds_time_stamp(dt):
    """

    :param dt_str: DESCRIPTION
    :type dt_str: TYPE
    :raises ValueError: DESCRIPTION
    :return: DESCRIPTION
    :rtype: TYPE

    """
    t_min_max = False

    if dt.year > 2200:
        logger.info(f"{dt} is too large setting to {TMAX}")
        stamp = TMAX
        t_min_max = True
    elif dt.year < 1900:
        logger.info(f"{dt} is too small setting to {TMIN}")
        stamp = TMIN
        t_min_max = True
    else:
        stamp = pd.Timestamp(dt, tz="UTC")

    return stamp, t_min_max


def _check_timestamp(pd_timestamp):
    """
    check if time stamp is before or after earlies or latest time allowed

    :param pd_timestamp: DESCRIPTION
    :type pd_timestamp: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    t_min_max = False
    pd_timestamp = _localize_utc(pd_timestamp)

    if pd_timestamp <= TMIN:
        t_min_max = True
        pd_timestamp = TMIN
    elif pd_timestamp >= TMAX:
        t_min_max = True
        pd_timestamp = TMAX

    return t_min_max, pd_timestamp


def parse(
    dt_str: Optional[float | int | np.datetime64 | pd.Timestamp | str] = None,
    gps_time: bool = False,
) -> pd.Timestamp:
    """
    Parse a date-time string using dateutil.parser

    Need to use dateutil.parser.isoparser to get correct tzinfo=tzutc
    If the input is a weird date string then try to use parse.

    :param dt_str: date-time string
    :type: string


    """
    t_min_max = False
    if dt_str in [None, "", "none", "None", "NONE", "Na", {}]:
        logger.debug("Time string is None, setting to 1980-01-01:00:00:00")
        stamp = pd.Timestamp("1980-01-01T00:00:00+00:00", tz="UTC")

    elif isinstance(dt_str, pd.Timestamp):
        t_min_max, stamp = _check_timestamp(dt_str)

    elif hasattr(dt_str, "isoformat"):
        try:
            t_min_max, stamp = _check_timestamp(pd.Timestamp(dt_str.isoformat()))
        except OutOfBoundsDatetime:
            stamp, t_min_max = _fix_out_of_bounds_time_stamp(
                _parse_string(dt_str.isoformat())
            )

    elif isinstance(dt_str, (float, int)):
        # using 3E8 which is about the start of GPS time
        ratio = dt_str / 3e8
        if ratio < 1 and gps_time:
            raise ValueError(
                "Input is before GPS start time '1980/01/06', check value."
            )
        if dt_str / 3e8 < 1e3:
            t_min_max, stamp = _check_timestamp(pd.Timestamp(dt_str, unit="s"))
            logger.debug("Assuming time input is in units of seconds")
        else:
            t_min_max, stamp = _check_timestamp(pd.Timestamp(dt_str, unit="ns"))
            logger.debug("Assuming time input is in units of nanoseconds")

    else:
        try:
            t_min_max, stamp = _check_timestamp(pd.Timestamp(dt_str))
        except (ValueError, TypeError, OutOfBoundsDatetime, OverflowError):
            dt = _parse_string(dt_str)
            stamp, t_min_max = _fix_out_of_bounds_time_stamp(dt)

    if isinstance(stamp, (type(pd.NaT), type(None))):
        logger.debug("Time string is None, setting to 1980-01-01:00:00:00")
        stamp = pd.Timestamp("1980-01-01T00:00:00+00:00", tz="UTC")

    # check time zone and enforce UTC
    stamp = _localize_utc(stamp)

    # there can be a machine round off error, if it is close to 1 round to
    # microseconds
    if round(stamp.nanosecond / 1000) == 1 and not t_min_max:
        stamp = stamp.round(freq="us")

    if gps_time:
        leap_seconds = calculate_leap_seconds(stamp.year, stamp.month, stamp.day)
        logger.debug("Converting GPS time to UTC with %s leap seconds", leap_seconds)
        stamp -= pd.Timedelta(seconds=leap_seconds)

    return _localize_utc(stamp)


# ==============================================================================
# convenience date-time container
# ==============================================================================
class MTime(MetadataBase):
    """
    Date and Time container based on :class:`pandas.Timestamp`

    Will read in a string or a epoch seconds into a :class:`pandas.Timestamp`
    object assuming the time zone is UTC.  If UTC is not the timezone then
    the time is corrected to UTC.

    The benefit of using :class:`pandas.Timestamp` is that it can handle
    nanoseconds.

    Accepted inputs are:

    - :class:`pandas.Timestamp`
    - :class:`numpy.datetime64`
    - :class:`datetime.datetime`
    - :class:`datetime.date`
    - :class:`datetime.timedelta`
    - :class:`obspy.UTCDateTime`
    - :class:`str` (ISO format or other formats)
    - :class:`float` (epoch seconds)
    - :class:`int` (epoch seconds)
    - :class:`None` (default to 1980-01-01T00:00:00+00:00)

    Outputs can be an ISO formatted string YYYY-MM-DDThh:mm:ss.ssssss+00:00:

        >>> t = MTtime()
        >>> t.isoformat()
        '1980-01-01T00:00:00+00:00'

    .. note:: if microseconds are 0 they are omitted. Same with nanoseconds.

    or Epoch seconds (float):

        >>> t.epoch_seconds
        315532800.0


    Convenience getters/setters are provided as properties for the different
    parts of time.

        >>> t = MTtime()
        >>> t.year = 2020
        >>> t.year
        2020

    .. note:: If the input data is greater than pandas.Timestamp.max then the
     value is set to
     :class:`pandas.Timestamp.max` = '2262-04-11 23:47:16.854775807'. Similarly,
     If the input data is less than pandas.Timestamp.min then the value is
     set to :class:`pandas.Timestamp.min` = '1677-09-21 00:12:43.145224193'


    >>> t = MTime(time_stamp="3000-01-01")
    [line 295] mt_metadata.utils.mttime.MTime.parse -
    INFO: 3000-01-01 is too large setting to 2262-04-11 23:47:16.854775807

    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={pd.Timestamp: lambda v: v.isoformat()},
    )

    gps_time: Annotated[
        bool,
        Field(
            description="Defines if the time give in GPS time [True] or UTC [False]",
        ),
    ] = False

    time_stamp: Annotated[
        float | int | np.datetime64 | pd.Timestamp | str,
        Field(
            default_factory=lambda: pd.Timestamp("1980-01-01T00:00:00+00:00"),
            description="Time in UTC format",
            examples=["1980-01-01T00:00:00+00:00"],
        ),
    ]

    @field_validator("time_stamp", mode="before")
    @classmethod
    def validate_time_stamp(
        cls,
        field_value: float | int | np.datetime64 | pd.Timestamp | str,
        validation_info: ValidationInfo,
    ) -> pd.Timestamp:
        """
        Validate the input time stamp and convert it to a pandas timestamp.
        This function is called before the model is created and is used to
        validate the input data.

        The function will check if the input data is a string, float, int,
        np.datetime64, pd.Timestamp, or UTCDateTime and convert to a
        pd.Timestamp object.

        If `gps_time` is True, the function will convert the time to UTC time
        by subtracting the leap seconds from the GPS time.

        If the input data is greater than pandas.Timestamp.max then the
        value is set to :class:`pandas.Timestamp.max` = '2262-04-11 23:47:16.854775807'.

        Similarly, If the input data is less than pandas.Timestamp.min then the value is
        set to :class:`pandas.Timestamp.min` = '1677-09-21 00:12:43.145224193'.

        Parameters
        ----------
        field_value : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            input time stamp
        validation_info : ValidationInfo
            Validation information object that contains the data and other
            information about the model.

        Returns
        -------
        pd.Timestamp
            converted time stamp
        """
        # Check if the time_stamp is a string and parse it
        return parse(field_value, gps_time=validation_info.data["gps_time"])

    def __str__(self) -> str:
        """
        Represents the object as a string in ISO format.

        Returns
        -------
        str
            ISO formatted string of the time stamp.
        """
        return self.isoformat()

    def __repr__(self) -> str:
        """
        Represents the object as a string in ISO format.

        Returns
        -------
        str
            ISO formatted string of the time stamp.
        """
        return self.isoformat()

    def __eq__(
        self, other: float | int | np.datetime64 | pd.Timestamp | str  # | UTCDateTime
    ) -> bool:
        """
        Checks if the time stamp is equal to another time stamp.
        This function is used to compare two time stamps and check if they are
        equal.

        The input will be parsed first into a pd.Timestamp object and then
        compared to the current time stamp.

        Parameters
        ----------
        other : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            other time stamp to compare to

        Returns
        -------
        bool
            if equal return True, otherwise False
        """
        if not isinstance(other, MTime):
            other = MTime(time_stamp=other)

        epoch_seconds = bool(self.time_stamp.value == other.time_stamp.value)

        tz = bool(self.time_stamp.tz == other.time_stamp.tz)

        if epoch_seconds and tz:
            return True
        elif epoch_seconds and not tz:
            logger.info(
                f"Time zones are not equal {self.time_stamp.tz} != "
                f"{other.time_stamp.tz}"
            )
            return False
        elif not epoch_seconds:
            return False

    def __ne__(
        self, other: float | int | np.datetime64 | pd.Timestamp | str  # | UTCDateTime
    ) -> bool:
        """
        Checks if the time stamp is not equal to another time stamp.

        Parameters
        ----------
        other : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            other time stamp to compare to

        Returns
        -------
        bool
            True if not equal, otherwise False
        """
        return not self.__eq__(other)

    def __lt__(
        self, other: float | int | np.datetime64 | pd.Timestamp | str  # | UTCDateTime
    ) -> bool:
        """
        Checks if the other is less than the current time stamp.

        Parameters
        ----------
        other : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            other time stamp to compare to

        Returns
        -------
        bool
            _True if other is less than the current time stamp, otherwise False
        """
        if not isinstance(other, MTime):
            other = MTime(time_stamp=other)

        return bool(self.time_stamp < other.time_stamp)

    def __le__(
        self, other: float | int | np.datetime64 | pd.Timestamp | str  # | UTCDateTime
    ) -> bool:
        """
        Checks if the other is less than or equal to the current time stamp.

        Parameters
        ----------
        other : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            other time stamp to compare to

        Returns
        -------
        _type_
            True if other is less than or equal to the current time stamp,
            otherwise False
        """
        if not isinstance(other, MTime):
            other = MTime(time_stamp=other)

        return bool(self.time_stamp <= other.time_stamp)

    def __gt__(
        self, other: float | int | np.datetime64 | pd.Timestamp | str  # | UTCDateTime
    ) -> bool:
        """
        Checks if the other is greater than the current time stamp.

        Parameters
        ----------
        other : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            other time stamp to compare to

        Returns
        -------
        bool
            True if other is greater than the current time stamp, otherwise False
        """
        return not self.__lt__(other)

    def __ge__(
        self, other: float | int | np.datetime64 | pd.Timestamp | str  # | UTCDateTime
    ) -> bool:
        """
        Checks if the other is greater than or equal to the current time stamp.

        Parameters
        ----------
        other : float | int | np.datetime64 | pd.Timestamp | str | UTCDateTime
            other time stamp to compare to

        Returns
        -------
        bool
            True if other is greater than or equal to the current time stamp,
            otherwise False
        """
        if not isinstance(other, MTime):
            other = MTime(time_stamp=other)

        return bool(self.time_stamp >= other.time_stamp)

    def __add__(
        self, other: int | float | datetime.timedelta | np.timedelta64
    ) -> "MTime":
        """
        Add time to the existing time stamp.  Must be a time delta object
        or a number in seconds.

        .. note:: Adding two time stamps does not make sense, use either
                 pd.Timedelta or seconds as a float or int.

        """
        if isinstance(other, (int, float)):
            other = pd.Timedelta(seconds=other)
            logger.debug("Assuming other time is in seconds")

        elif isinstance(other, (datetime.timedelta, np.timedelta64)):
            other = pd.Timedelta(other)

        if not isinstance(other, (pd.Timedelta)):
            msg = (
                "Adding times stamps does not make sense, use either "
                "pd.Timedelta or seconds as a float or int."
            )
            logger.error(msg)
            raise ValueError(msg)

        return MTime(time_stamp=self.time_stamp + other)

    def __sub__(
        self, other: int | float | datetime.timedelta | np.timedelta64
    ) -> "MTime":
        """
        Get the time difference between to times in seconds.

        :param other: other time value
        :type other: [ str | float | int | datetime.datetime | np.datetime64 ]
        :return: time difference in seconds
        :rtype: float

        """

        if isinstance(other, (int, float)):
            other = pd.Timedelta(seconds=other)
            logger.info("Assuming other time is in seconds and not epoch seconds.")

        elif isinstance(other, (datetime.timedelta, np.timedelta64)):
            other = pd.Timedelta(other)

        else:
            try:
                other = MTime(time_stamp=other)
            except ValueError as error:
                raise TypeError(error)

        if not isinstance(other, (pd.Timedelta, MTime)):
            msg = "Subtracting times must be either timedelta or another time."
            logger.error(msg)
            raise ValueError(msg)

        if isinstance(other, MTime):
            other = MTime(time_stamp=other)

            return (self.time_stamp - other.time_stamp).total_seconds()

        elif isinstance(other, pd.Timedelta):
            return MTime(time_stamp=self.time_stamp - other)

    def __hash__(self) -> int:
        return hash(self.isoformat())

    def to_dict(self, nested=False, single=False, required=True) -> dict[str, str]:
        """
        Convert the time stamp to a dictionary with the ISO format string.

        Returns
        -------
        dict[str, str]
            Dictionary with the ISO format string.
        """
        return self.isoformat()

    def from_dict(
        self,
        value: str | int | float | np.datetime64 | pd.Timestamp,
        skip_none=False,
    ) -> None:
        """
        This will have to accept just a single value, not a dict.
        This is to keep original functionality.

        Parameters
        ----------
        value : str | int | float | np.datetime64 | pd.Timestamp
            time stamp value
        """
        self.time_stamp = value

    @property
    def iso_str(self) -> str:
        """

        Returns
        -------
        str
            ISO formatted string of the time stamp.
        """
        logger.warning(
            "iso_str will be deprecated in the future. Use isoformat() instead"
        )
        return self.time_stamp.isoformat()

    @property
    def iso_no_tz(self) -> str:
        """
        ISO formatted string of the time stamp without the timezone.
        This is useful for storing the time stamp in a database or other
        format where the timezone is not needed.

        Returns
        -------
        str
            ISO formatted string of the time stamp without the timezone.
        """
        return self.time_stamp.isoformat().split("+", 1)[0]

    @property
    def epoch_seconds(self) -> float:
        """
        Epoch seconds of the time stamp.  This is the number of seconds
        since the epoch (1970-01-01 00:00:00 UTC).

        Returns
        -------
        float
            epoch seconds of the time stamp.
        """
        return self.time_stamp.timestamp()

    @epoch_seconds.setter
    def epoch_seconds(self, seconds: float | int) -> None:
        """
        Sets the time stamp to the given epoch seconds.  This is the number of
        seconds since the epoch (1970-01-01 00:00:00 UTC).

        Parameters
        ----------
        seconds : float | int
            epoch seconds for the time stamp.
        """
        logger.debug("reading time from epoch seconds, assuming UTC time zone")
        # has to be seconds
        self.time_stamp = pd.Timestamp(seconds, tz="UTC", unit="s")

    @property
    def date(self) -> str:
        """
        Date in ISO format.  This is the date part of the time stamp
        without the time part.  This is useful for storing the date in a
        database or other format where the time is not needed.
        The date is in the format YYYY-MM-DD.

        Returns
        -------
        str
            ISO formatted date string of the time stamp.
        """
        return self.time_stamp.date().isoformat()

    @property
    def year(self) -> int:
        """
        Year of the time stamp

        Returns
        -------
        int
            year of the time stamp
        """
        return self.time_stamp.year

    @year.setter
    def year(self, value: int) -> None:
        """
        Sets the year of the time stamp to the given value.  This is the
        year part of the time stamp.  This is useful for setting the year
        of the time stamp to a specific value.
        The year is in the format YYYY.

        Parameters
        ----------
        value : int
            New year value for the time stamp.
        """
        self.time_stamp = self.time_stamp.replace(year=value)

    @property
    def month(self) -> int:
        """
        Month of the time stamp. This is the month part of the time stamp
        without the time part.  This is useful for storing the month in a
        database or other format where the time is not needed.

        Returns
        -------
        int
            month of time stamp
        """
        return self.time_stamp.month

    @month.setter
    def month(self, value: int) -> None:
        """
        Sets the month of the time stamp to the given value.  This is the
        month part of the time stamp.  This is useful for setting the month


        Parameters
        ----------
        value : int
            new month value for the time stamp.
        """
        self.time_stamp = self.time_stamp.replace(month=value)

    @property
    def day(self) -> int:
        """
        Day of the time stamp. This is the day part of the time stamp
        without the time part.

        Returns
        -------
        int
            Day of the time stamp
        """
        return self.time_stamp.day

    @day.setter
    def day(self, value: int) -> None:
        """
        Sets the day of the time stamp to the given value.  This is the
        day part of the time stamp.

        Parameters
        ----------
        value : int
            new day of the time stamp
        """
        self.time_stamp = self.time_stamp.replace(day=value)

    @property
    def hour(self) -> int:
        """
        Hour of the time stamp.

        Returns
        -------
        int
            hour of the time stamp
        """
        return self.time_stamp.hour

    @hour.setter
    def hour(self, value: int) -> None:
        """
        Sets the hour of the time stamp to the given value.

        Parameters
        ----------
        value : int
            new hour of the time stamp
        """
        self.time_stamp = self.time_stamp.replace(hour=value)

    @property
    def minutes(self) -> int:
        return self.time_stamp.minute

    @minutes.setter
    def minutes(self, value: int) -> None:
        self.time_stamp = self.time_stamp.replace(minute=value)

    @property
    def seconds(self) -> int:
        return self.time_stamp.second

    @seconds.setter
    def seconds(self, value: int) -> None:
        self.time_stamp = self.time_stamp.replace(second=value)

    @property
    def microseconds(self) -> int:
        return self.time_stamp.microsecond

    @microseconds.setter
    def microseconds(self, value: int) -> None:
        self.time_stamp = self.time_stamp.replace(microsecond=value)

    @property
    def nanoseconds(self) -> int:
        return self.time_stamp.nanosecond

    @nanoseconds.setter
    def nanoseconds(self, value: int) -> None:
        self.time_stamp = self.time_stamp.replace(nanosecond=value)

    def now(self) -> "MTime":
        """
        The current time in UTC format.

        Returns
        -------
        MTime
            The current time as an MTime object.
        """
        self.time_stamp = pd.Timestamp.utcnow()

        return self

    def copy(self) -> "MTime":
        """make a copy of the time"""
        return self.model_copy(deep=True)

    def isoformat(self) -> str:
        """
        ISO formatted string of the time stamp.  This is the ISO format
        string of the time stamp.

        formatted as: YYYY-MM-DDThh:mm:ss.ssssss+00:00

        Returns
        -------
        str
            ISO formatted date time string
        """
        return self.time_stamp.isoformat()

    def isodate(self) -> str:
        """
        ISO formatted date string of the time stamp.  This is the ISO format
        string of the date part of the time stamp.

        formatted as: YYYY-MM-DD

        Returns
        -------
        str
            _description_
        """
        return self.time_stamp.isodate()

    def isocalendar(self) -> str:
        """
        ISO formatted calendar string of the time stamp.  This is the ISO
        format string of the calendar part of the time stamp.

        Formatted as: YYYY-WW-D
        where YYYY is the year, WW is the week number, and D is the day of
        the week.

        Returns
        -------
        str
            ISO formatted calendar string of the time stamp.
        """
        return self.time_stamp.isocalendar()


def get_now_utc() -> "MTime":
    """
    Get the current time in UTC format as an MTime object

    Returns
    -------
    MTime
        Current time in UTC format as an MTime object.
    """

    m_obj = MTime()
    m_obj.now()
    return m_obj.isoformat()
