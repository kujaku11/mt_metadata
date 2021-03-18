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
    get_schema("person", SCHEMA_FN_PATHS), "acquired_by", keys=["author", "comments"]
)
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS), "metadata_by", keys=["author", "comments"]
)
attr_dict.add_dict(
    get_schema("provenance", SCHEMA_FN_PATHS), "provenance", keys=["comments", "log"]
)
# =============================================================================


class Run(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.id = None
        self.sample_rate = None
        self.comments = None
        self._n_chan = None
        self.data_type = None
        self.acquired_by = Person()
        self.provenance = Provenance()
        self.time_period = TimePeriod()
        self.data_logger = DataLogger()
        self.metadata_by = Person()
        self.fdsn = Fdsn()
        self.channels = []

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

    def has_channel(self, component):
        """
        Check to see if the channel already exists
        
        :param component: DESCRIPTION
        :type component: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

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

    def add_channel(self, channel_obj):
        """
        Add a channel to the list, check if one exists if it does overwrite it
        
        :param channel_obj: DESCRIPTION
        :type channel_obj: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        index = self.channel_index(channel_obj.component)
        if index is not None:
            self.channels[index] = channel_obj
        else:
            self.channels.append(channel_obj)

    @property
    def channels(self):
        """ List of channels in the run """
        return self._channels

    @channels.setter
    def channels(self, value):
        """ set the channel list """
        if not hasattr(value, "__iter__"):
            msg = (
                "input channels must be an iterable, should be a list "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)
        channels = []
        fails = []
        for ii, channel in enumerate(value):
            if not isinstance(channel, (Auxiliary, Electric, Magnetic)):
                msg = f"Item {ii} is not type(channel); type={type(channel)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                channels.append(channel)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        self._channels = channels

    @property
    def n_channels(self):
        return self.__len__()

    @property
    def channels_recorded_all(self):
        """

        :return: a list of all channels recorded
        :rtype: TYPE

        """
        return [ch.component for ch in self.channels]

    @property
    def channels_recorded_electric(self):
        return sorted(
            [ch.component for ch in self.channels if isinstance(ch, Electric)]
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
                self.channels.append(Electric(component=entry))
            elif isinstance(entry, Electric):
                self.channels.append(entry)
            else:
                msg = f"entry must be a string or type Electric not {type(entry)}"
                self.logger.error(msg)
                raise ValueError(msg)

    @property
    def channels_recorded_magnetic(self):
        return sorted(
            [ch.component for ch in self.channels if isinstance(ch, Magnetic)]
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
                self.channels.append(Magnetic(component=entry))
            elif isinstance(entry, Magnetic):
                self.channels.append(entry)
            else:
                msg = f"entry must be a string or type Magnetic not {type(entry)}"
                self.logger.error(msg)
                raise ValueError(msg)

    @property
    def channels_recorded_auxiliary(self):
        return sorted(
            [ch.component for ch in self.channels if isinstance(ch, Auxiliary)]
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
                self.channels.append(Auxiliary(component=entry))
            elif isinstance(entry, Auxiliary):
                self.channels.append(entry)
            else:
                msg = f"entry must be a string or type Auxiliary not {type(entry)}"
                self.logger.error(msg)
                raise ValueError(msg)
