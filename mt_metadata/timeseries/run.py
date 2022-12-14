# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import (
    Person,
    Provenance,
    TimePeriod,
    Fdsn,
    DataLogger,
    Electric,
    Magnetic,
    Auxiliary,
)
from mt_metadata.utils.list_dict import ListDict

# =============================================================================
attr_dict = get_schema("run", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
dl_dict = get_schema("instrument", SCHEMA_FN_PATHS)
dl_dict.add_dict(get_schema("timing_system", SCHEMA_FN_PATHS), "timing_system")
dl_dict.add_dict(get_schema("software", SCHEMA_FN_PATHS), "firmware")
dl_dict.add_dict(get_schema("battery", SCHEMA_FN_PATHS), "power_source")
attr_dict.add_dict(dl_dict, "data_logger")
attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "acquired_by",
    keys=["author", "comments", "organization"],
)
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "metadata_by",
    keys=["author", "comments", "organization"],
)
attr_dict.add_dict(
    get_schema("provenance", SCHEMA_FN_PATHS),
    "provenance",
    keys=["comments", "log"],
)
# =============================================================================


class Run(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.acquired_by = Person()
        self.provenance = Provenance()
        self.time_period = TimePeriod()
        self.data_logger = DataLogger()
        self.metadata_by = Person()
        self.fdsn = Fdsn()
        self.channels = ListDict()

        super().__init__(attr_dict=attr_dict, **kwargs)

    def __len__(self):
        return len(self.channels)

    def __add__(self, other):
        if isinstance(other, Run):
            self.channels.extend(other.channels)

            return self
        else:
            msg = f"Can only merge Run objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)

    def update(self, other, match=[]):
        """
        Update attribute values from another like element, skipping None

        :param other: DESCRIPTION
        :type other: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if not isinstance(other, type(self)):
            self.logger.warning(
                "Cannot update %s with %s", type(self), type(other)
            )
        for k in match:
            if self.get_attr_from_name(k) != other.get_attr_from_name(k):
                msg = "%s is not equal %s != %s"
                self.logger.error(
                    msg,
                    k,
                    self.get_attr_from_name(k),
                    other.get_attr_from_name(k),
                )
                raise ValueError(
                    msg,
                    k,
                    self.get_attr_from_name(k),
                    other.get_attr_from_name(k),
                )
        for k, v in other.to_dict(single=True).items():
            if hasattr(v, "size"):
                if v.size > 0:
                    self.set_attr_from_name(k, v)
            else:
                if v not in [None, 0.0, [], "", "1980-01-01T00:00:00+00:00"]:
                    self.set_attr_from_name(k, v)

        ## Need this because channels are set when setting channels_recorded
        ## and it initiates an empty channel, but we need to fill it with
        ## the appropriate metadata.
        for ch in other.channels:
            self.add_channel(ch)

    def has_channel(self, component):
        """
        Check to see if the channel already exists

        :param component: channel component to look for
        :type component: string
        :return: True if found, False if not
        :rtype: boolean

        """

        if component in self.channels_recorded_all:
            return True
        return False

    def channel_index(self, component):
        """
        get index of the channel in the channel list
        """
        if self.has_channel(component):
            return self.channels_recorded_all.index(component)
        return None

    def get_channel(self, component):
        """
        Get a channel

        :param component: channel component to look for
        :type component: string
        :return: channel object based on channel type
        :rtype: :class:`mt_metadata.timeseries.Channel`

        """

        if self.has_channel(component):
            return self.channels[component]

    def add_channel(self, channel_obj):
        """
        Add a channel to the list, check if one exists if it does overwrite it

        :param channel_obj: channel object to add
        :type channel_obj: :class:`mt_metadata.timeseries.Channel`

        """
        if not isinstance(channel_obj, (Magnetic, Electric, Auxiliary)):
            msg = f"Input must be metadata.Channel not {type(channel_obj)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if channel_obj.component is None:
            msg = "component cannot be empty"
            self.logger.error(msg)
            raise ValueError(msg)

        if self.has_channel(channel_obj.component):
            self.channels[channel_obj.component].update(channel_obj)
            self.logger.debug(
                f"Run {channel_obj.component} already exists, updating metadata"
            )

        else:
            self.channels.append(channel_obj)

    def remove_channel(self, channel_id):
        """
        remove a run from the survey

        :param component: channel component to look for
        :type component: string

        """

        if self.has_channel(channel_id):
            self.channels.remove(channel_id)
        else:
            self.logger.warning(f"Could not find {channel_id} to remove.")

    @property
    def channels(self):
        """List of channels in the run"""
        return self._channels

    @channels.setter
    def channels(self, value):
        """set the channel list"""

        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input run_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

        fails = []
        self._channels = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, channel in enumerate(value_list):

            if isinstance(channel, (dict, OrderedDict)):
                try:
                    ch_type = channel["type"]
                    if ch_type is None:
                        ch_type = channel["component"][0]

                    if ch_type in ["electric", "e"]:
                        ch = Electric()
                    elif ch_type in ["magnetic", "b", "h"]:
                        ch = Magnetic()
                    else:
                        ch = Auxiliary()

                    ch.from_dict(channel)
                    self._channels.append(ch)
                except KeyError:
                    msg = (
                        f"Item {ii} is not type(channel); type={type(channel)}"
                    )
                    fails.append(msg)
                    self.logger.error(msg)
            elif not isinstance(channel, (Auxiliary, Electric, Magnetic)):
                msg = f"Item {ii} is not type(channel); type={type(channel)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                self._channels.append(channel)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

    @property
    def n_channels(self):
        return self.__len__()

    @property
    def channels_recorded_all(self):
        """

        :return: a list of all channels recorded
        :rtype: TYPE

        """
        return [
            ch.component
            for ch in self.channels.values()
            if ch.component is not None
        ]

    @property
    def channels_recorded_electric(self):
        return sorted(
            [
                ch.component
                for ch in self.channels.values()
                if isinstance(ch, Electric) and ch.component is not None
            ]
        )

    @channels_recorded_electric.setter
    def channels_recorded_electric(self, value):
        if value is None:
            self.logger.debug("Input channel name is None, skipping")
            return
        if not hasattr(value, "__iter__"):
            value = [value]

        for entry in value:
            if isinstance(entry, str):
                self.add_channel(Electric(component=entry))
            elif entry is None:
                continue
            elif isinstance(entry, Electric):
                self.add_channel(entry)
            else:
                msg = (
                    f"entry must be a string or type Electric not {type(entry)}"
                )
                self.logger.error(msg)
                raise ValueError(msg)

    @property
    def channels_recorded_magnetic(self):
        return sorted(
            [
                ch.component
                for ch in self.channels.values()
                if isinstance(ch, Magnetic) and ch.component is not None
            ]
        )

    @channels_recorded_magnetic.setter
    def channels_recorded_magnetic(self, value):
        if value is None:
            self.logger.debug("Input channel name is None, skipping")
            return
        if not hasattr(value, "__iter__"):
            value = [value]

        for entry in value:
            if isinstance(entry, str):
                self.add_channel(Magnetic(component=entry))
            elif entry is None:
                continue
            elif isinstance(entry, Magnetic):
                self.add_channel(entry)
            else:
                msg = (
                    f"entry must be a string or type Magnetic not {type(entry)}"
                )
                self.logger.error(msg)
                raise ValueError(msg)

    @property
    def channels_recorded_auxiliary(self):
        return sorted(
            [
                ch.component
                for ch in self.channels.values()
                if isinstance(ch, Auxiliary) and ch.component is not None
            ]
        )

    @channels_recorded_auxiliary.setter
    def channels_recorded_auxiliary(self, value):
        if value is None:
            self.logger.debug("Input channel name is None, skipping")
            return
        if not hasattr(value, "__iter__"):
            value = [value]

        for entry in value:
            if isinstance(entry, str):
                self.add_channel(Auxiliary(component=entry))
            elif entry is None:
                continue
            elif isinstance(entry, Auxiliary):
                self.add_channel(entry)
            else:
                msg = f"entry must be a string or type Auxiliary not {type(entry)}"
                self.logger.error(msg)
                raise ValueError(msg)

    def update_time_period(self):
        """
        update time period from the channels
        """
        start = []
        end = []
        for channel in self.channels:
            if channel.time_period.start != "1980-01-01T00:00:00+00:00":
                start.append(channel.time_period.start)
            if channel.time_period.start != "1980-01-01T00:00:00+00:00":
                end.append(channel.time_period.end)

        if start:
            if self.time_period.start == "1980-01-01T00:00:00+00:00":
                self.time_period.start = min(start)
            else:
                if self.time_period.start > min(start):
                    self.time_period.start = min(start)

        if end:
            if self.time_period.end == "1980-01-01T00:00:00+00:00":
                self.time_period.end = max(end)
            else:
                if self.time_period.end < max(end):
                    self.time_period.end = max(end)

    @property
    def ex(self):
        return self.get_channel("ex")

    @ex.setter
    def ex(self, value):
        self.add_channel(value)

    @property
    def ey(self):
        return self.get_channel("ey")

    @ey.setter
    def ey(self, value):
        self.add_channel(value)

    @property
    def hx(self):
        return self.get_channel("hx")

    @hx.setter
    def hx(self, value):
        self.add_channel(value)

    @property
    def hy(self):
        return self.get_channel("hy")

    @hy.setter
    def hy(self, value):
        self.add_channel(value)

    @property
    def hz(self):
        return self.get_channel("hz")

    @hz.setter
    def hz(self, value):
        self.add_channel(value)

    @property
    def temperature(self):
        return self.get_channel("temperature")

    @temperature.setter
    def temperature(self, value):
        self.add_channel(value)
