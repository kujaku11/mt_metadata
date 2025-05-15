# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:20:59 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict

from mt_metadata.base import Base, get_schema
from mt_metadata.base.helpers import write_lines
from mt_metadata.timeseries import TimePeriod
from mt_metadata.transfer_functions.processing.aurora import Window
from mt_metadata.transfer_functions.processing.aurora.decimation_level import (
    get_fft_harmonics,
)
from mt_metadata.transfer_functions.processing.fourier_coefficients import Channel
from mt_metadata.utils.list_dict import ListDict

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("decimation", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict, "time_period")
attr_dict.add_dict(Window()._attr_dict, "window")


# =============================================================================
class Decimation(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.window = Window()
        self.time_period = TimePeriod()
        self.channels = ListDict()
        super().__init__(attr_dict=attr_dict, **kwargs)
        # if self.decimation_level == 0:
        #     self.anti_alias_filter = None

    def __len__(self):
        return len(self.channels)

    def __add__(self, other):
        if isinstance(other, Decimation):
            self.channels.extend(other.channels)

            return self
        else:
            msg = f"Can only merge ch objects, not {type(other)}"
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
            self.logger.warning("Cannot update %s with %s", type(self), type(other))
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

    @property
    def channels_estimated(self):
        """channels for fcs were estimated"""
        return [
            ch.component for ch in self.channels.values() if ch.component is not None
        ]

    @channels_estimated.setter
    def channels_estimated(self, value):
        """set channels esimated"""

        if value is None:
            self.logger.debug("Input channel name is None, skipping")
            return
        if not hasattr(value, "__iter__"):
            value = [value]

        for entry in value:
            if isinstance(entry, str):
                self.add_channel(Channel(component=entry))
            elif entry is None:
                continue
            elif isinstance(entry, Channel):
                self.add_channel(entry)
            else:
                msg = f"entry must be a string or type FCChannel not {type(entry)}"
                self.logger.error(msg)
                raise ValueError(msg)

    def has_channel(self, component):
        """
        Check to see if the channel already exists

        :param component: channel component to look for
        :type component: string
        :return: True if found, False if not
        :rtype: boolean

        """

        if component in self.channels_estimated:
            return True
        return False

    def channel_index(self, component):
        """
        get index of the channel in the channel list
        """
        if self.has_channel(component):
            return self.channels_estimated.index(component)
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
        :type channel_obj: :class:`mt_metadata.transfer_functions.processing.fourier_coefficients.Channel`

        """
        if not isinstance(channel_obj, (Channel)):
            msg = f"Input must be metadata.Channel not {type(channel_obj)}"
            self.logger.error(msg)
            raise ValueError(msg)

        if self.has_channel(channel_obj.component):
            self.channels[channel_obj.component].update(channel_obj)
            self.logger.debug(
                f"ch {channel_obj.component} already exists, updating metadata"
            )

        else:
            self.channels.append(channel_obj)

        self.update_time_period()

    def remove_channel(self, channel_id):
        """
        remove a ch from the survey

        :param component: channel component to look for
        :type component: string

        """

        if self.has_channel(channel_id):
            self.channels.remove(channel_id)
        else:
            self.logger.warning(f"Could not find {channel_id} to remove.")

        self.update_time_period()

    @property
    def channels(self):
        """List of channels in the ch"""
        return self._channels

    @channels.setter
    def channels(self, value):
        """set the channel list"""

        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input ch_list must be an iterable, should be a list or dict "
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
            try:
                ch = Channel()
                if hasattr(channel, "to_dict"):
                    channel = channel.to_dict()
                ch.from_dict(channel)
                self._channels.append(ch)
            except Exception as error:
                msg = "Could not create channel from dictionary: %s"
                fails.append(msg % error)
                self.logger.error(msg, error)

        if len(fails) > 0:
            raise TypeError("\n".join(fails))

    @property
    def n_channels(self):
        return self.__len__()

    def update_time_period(self):
        """
        update time period from ch information
        """
        start = []
        end = []
        for ch in self.channels:
            if ch.time_period.start != "1980-01-01T00:00:00+00:00":
                start.append(ch.time_period.start)
            if ch.time_period.start != "1980-01-01T00:00:00+00:00":
                end.append(ch.time_period.end)
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

    # Workarounds for pass-through usage of same decimation as aurora
    @property
    def factor(self):
        return self.decimation_factor

    @property
    def sample_rate(self):
        return self.sample_rate_decimation

    def is_valid_for_time_series_length(self, n_samples_ts):
        """Given a time series of len n_samples_ts, are there sufficient samples to STFT"""
        required_num_samples = (
            self.window.num_samples
            + (self.min_num_stft_windows - 1) * self.window.num_samples_advance
        )
        if n_samples_ts < required_num_samples:
            msg = (
                f"{n_samples_ts} not enough samples for minimum of "
                f"{self.min_num_stft_windows} stft windows of length "
                f"{self.window.num_samples} and overlap {self.window.overlap}"
            )
            self.logger.warning(msg)
            return False
        else:
            return True

    @property
    def fft_frequencies(self):
        return get_fft_harmonics(self.window.num_samples, self.sample_rate)

    def has_fcs_for_aurora_processing(self, decimation_level, remote):
        """

        Parameters
        ----------
        decimation_level: mt_metadata.transfer_functions.processing.aurora.decimation_level.DecimationLevel
        remote: bool

        Iterates over parameters:
        "channels_estimated", "anti_alias_filter", "sample_rate, "method", "prewhitening_type", "recoloring",
        "pre_fft_detrend_type", "min_num_stft_windows", "window", "harmonic_indices",
        Returns
        -------

        """
        # "channels_estimated"
        if remote:
            required_channels = decimation_level.reference_channels
        else:
            required_channels = decimation_level.local_channels

        try:
            assert set(required_channels).issubset(self.channels_estimated)
        except AssertionError:
            msg = (
                f"required_channels for processing {required_channels} not available"
                f"-- fc channels estimated are {self.channels_estimated}"
            )
            self.logger.info(msg)
            return False

        # anti_alias_filter
        try:
            assert self.anti_alias_filter == decimation_level.anti_alias_filter
        except AssertionError:
            cond1 = decimation_level.anti_alias_filter == "default"
            cond2 = self.anti_alias_filter is None
            if cond1 & cond2:
                pass
            else:
                msg = (
                    "Antialias Filters Not Compatible -- need to add handling for "
                    f"{msg} FCdec {self.anti_alias_filter} and "
                    f"{msg} processing config:{decimation_level.anti_alias_filter}"
                )
                raise NotImplementedError(msg)

        # sample_rate
        try:
            assert (
                self.sample_rate_decimation == decimation_level.decimation.sample_rate
            )
        except AssertionError:
            msg = (
                f"Sample rates do not agree: fc {self.sample_rate_decimation} differs from "
                f"processing config {decimation_level.decimation.sample_rate}"
            )
            self.logger.info(msg)
            return False

        # method (fft, wavelet, etc.)
        try:
            assert self.method == decimation_level.method
        except AssertionError:
            msg = (
                "Transform methods do not agree "
                f"{self.method} != {decimation_level.method}"
            )
            self.logger.info(msg)
            return False

        # prewhitening_type
        try:
            assert self.prewhitening_type == decimation_level.prewhitening_type
        except AssertionError:
            msg = (
                "prewhitening_type does not agree "
                f"{self.prewhitening_type} != {decimation_level.prewhitening_type}"
            )
            self.logger.info(msg)
            return False

        # recoloring
        try:
            assert self.recoloring == decimation_level.recoloring
        except AssertionError:
            msg = (
                "recoloring does not agree "
                f"{self.recoloring} != {decimation_level.recoloring}"
            )
            self.logger.info(msg)
            return False

        # pre_fft_detrend_type
        try:
            assert self.pre_fft_detrend_type == decimation_level.pre_fft_detrend_type
        except AssertionError:
            msg = (
                "pre_fft_detrend_type does not agree "
                f"{self.pre_fft_detrend_type} != {decimation_level.pre_fft_detrend_type}"
            )
            self.logger.info(msg)
            return False

        # min_num_stft_windows
        try:
            assert self.min_num_stft_windows == decimation_level.min_num_stft_windows
        except AssertionError:
            msg = (
                "min_num_stft_windows do not agree "
                f"{self.min_num_stft_windows} != {decimation_level.min_num_stft_windows}"
            )
            self.logger.info(msg)
            return False

        # window
        try:
            assert self.window == decimation_level.window
        except AssertionError:
            msg = "window does not agree: "
            msg = f"{msg} FC Group: {self.window} "
            msg = f"{msg} Processing Config  {decimation_level.window}"
            self.logger.info(msg)
            return False

        if -1 in self.harmonic_indices:
            # if harmonic_indices is -1, it means keep all so we can skip this check.
            pass
        else:
            harmonic_indices_requested = decimation_level.harmonic_indices
            fcdec_group_set = set(self.harmonic_indices)
            processing_set = set(harmonic_indices_requested)
            if processing_set.issubset(fcdec_group_set):
                pass
            else:
                msg = (
                    f"Processing FC indices {processing_set} is not contained "
                    f"in FC indices {fcdec_group_set}"
                )
                self.logger.info(msg)
                return False

        # No checks were failed the FCDecimation supports the processing config
        return True
