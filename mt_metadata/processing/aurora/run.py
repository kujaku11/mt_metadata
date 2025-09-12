# -*- coding: utf-8 -*-
"""
Module for `aurora` Run metadata container with useful built-in methods.

Created on Thu Feb 17 14:15:20 2022

@author: jpeacock

"""
from typing import Union

from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.timeseries import TimePeriod

from .channel import Channel


# =============================================================================
attr_dict = get_schema("run", SCHEMA_FN_PATHS)


# =============================================================================
class Run(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """
        Constructor.

        """
        self._input = []
        self._output = []
        self._time_periods = []

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def input_channel_names(self) -> list:
        """list of channel names"""
        return [ch.id for ch in self._input]

    @property
    def input_channels(self) -> list:
        return self._input

    @input_channels.setter
    def input_channels(self, values: Union[list, str, Channel, dict]) -> None:
        self._input = []
        if not isinstance(values, list):
            values = [values]

        for item in values:
            if isinstance(item, str):
                ch = Channel(id=item)
            elif isinstance(item, Channel):
                ch = item

            elif isinstance(item, dict):
                ch = Channel()
                ch.from_dict(item)

            else:
                raise TypeError(f"not sure what to do with type {type(item)}")

            self._input.append(ch)

    @property
    def output_channel_names(self):
        """list of channel names"""
        return [ch.id for ch in self._output]

    @property
    def output_channels(self):
        return self._output

    @output_channels.setter
    def output_channels(self, values):
        self._output = []
        if not isinstance(values, list):
            values = [values]

        for item in values:
            if isinstance(item, str):
                ch = Channel(id=item)
            elif isinstance(item, Channel):
                ch = item
            elif isinstance(item, dict):
                ch = Channel()
                ch.from_dict(item)

            else:
                raise TypeError(f"not sure what to do with type {type(item)}")

            self._output.append(ch)

    @property
    def time_periods(self):
        return self._time_periods

    @time_periods.setter
    def time_periods(self, values: Union[list, dict, TimePeriod]) -> None:
        """
            Sets self.time_periods

        Parameters
        ----------
        values: Union[list, dict, TimePeriod]
            If it is a list, the elements of the list must be TimePerid or dictionary representations of TimePeriods

        """
        self._time_periods = []
        if not isinstance(values, list):
            values = [values]

        for item in values:
            if isinstance(item, TimePeriod):
                self._time_periods.append(item)
            elif isinstance(item, dict):
                try:
                    tp = TimePeriod()
                    tp.from_dict(item)
                    self._time_periods.append(tp)
                except Exception as e:
                    msg = f"Could not unpack dict to TimePeriod, got exception {e}"
                    raise ValueError(msg)
            else:
                raise TypeError(f"not sure what to do with type {type(item)}")

    @property
    def channel_scale_factors(self):
        """
        return a dictionary of channel scale factors

        :return: DESCRIPTION
        :rtype: TYPE

        """

        scales = {}

        for ch in self.input_channels + self.output_channels:
            scales[ch.id] = ch.scale_factor

        return scales

    @channel_scale_factors.setter
    def channel_scale_factors(self, values):
        """
        Parameters
        ----------
        values: dict
            expected to be keyed like
            {"ex":1.0, "ey":1.0, "hx":1.0, "hy":1.0, "hz":1.0}

        """
        if not isinstance(values, dict):
            raise TypeError(f"not sure what to do with type {type(values)}")
        for i, channel in enumerate(self.input_channels):
            if channel.id in values.keys():
                self.input_channels[i].scale_factor = values[channel.id]
        for i, channel in enumerate(self.output_channels):
            if channel.id in values.keys():
                self.output_channels[i].scale_factor = values[channel.id]
