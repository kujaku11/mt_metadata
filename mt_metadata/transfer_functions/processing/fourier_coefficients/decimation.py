# -*- coding: utf-8 -*-
"""
    This module contains the Decimation class.  This class interacts with a decimation JSON.
    It contains the metadata to specify a transformation from time series to a Spectrogram, including
    cascadng decimation info.

    TODO: Consider renaming this class to FCDecmiation, to contrast with other Decimation objects,
    or FCDecimationLevel to make it
    Also see notes in mt_metadata issue 235.

    Created on Fri Feb 25 15:20:59 2022

    @author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict
from loguru import logger

from .standards import SCHEMA_FN_PATHS
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries import TimePeriod
from mt_metadata.transfer_functions.processing.short_time_fourier_transform import ShortTimeFourierTransform
from mt_metadata.transfer_functions.processing.time_series_decimation import TimeSeriesDecimation
# from mt_metadata.transfer_functions.processing.aurora.decimation_level import DecimationLevel as AuroraDecimationLevel
from mt_metadata.transfer_functions.processing.aurora.window import Window
from mt_metadata.transfer_functions.processing.fourier_coefficients import (
    Channel as FCChannel
)
from mt_metadata.utils.list_dict import ListDict

import numpy as np
# =============================================================================
attr_dict = get_schema("decimation", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict, "time_period")
attr_dict.add_dict(Window()._attr_dict, "window")
attr_dict.add_dict(ShortTimeFourierTransform()._attr_dict, "short_time_fourier_transform")
attr_dict.add_dict(TimeSeriesDecimation()._attr_dict, "time_series_decimation")

# =============================================================================
class Decimation(Base):
    """
        TODO: the name of this class could be changed to something more appropriate.
        TODO: consider adding an attr decimation to access TimeSeriesDecimation more briefly.
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """
         Constructor.

        :param kwargs: TODO: add doc here
        """
        self.window = Window()
        self.time_period = TimePeriod()
        self.channels = ListDict()
        self.time_series_decimation = TimeSeriesDecimation()
        self.short_time_fourier_transform = ShortTimeFourierTransform()

        super().__init__(attr_dict=attr_dict, **kwargs)

        if self.short_time_fourier_transform.extra_pre_fft_detrend_type:
            msg = f"extra pre-fft detrend was set to {self.short_time_fourier_transform.extra_pre_fft_detrend_type}"
            msg += "however, this is not supported -- setting to empty string"
            logger.debug(msg)
            self.short_time_fourier_transform.extra_pre_fft_detrend_type = None

        # if self.time_series_decimation.level == 0:
        #     self.time_series_decimation.anti_alias_filter = None

    def __len__(self) -> int:
        return len(self.channels)

    def __add__(self, other):
        """

        :param other:
        :return:
        """
        if isinstance(other, Decimation):
            self.channels.extend(other.channels)

            return self
        else:
            msg = f"Can only merge ch objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)

    #----- Begin (Possibly Temporary) methods for integrating TimeSeriesDecimation Class -----#
    @property
    def factor(self):
        """
        TODO: DELETE THIS IN 2025: factor should be deprecated, use TimeSeriesDecimation for this info.
        """
        msg = ("This method will be deprecated in a future release.  Use "
               "self.time_series_decimation.factor or self.decimation_factor instead")
        logger.warning(msg)
        return self.decimation_factor

    @property
    def sample_rate(self) -> float:
        return self.time_series_decimation.sample_rate

    @property
    def decimation_level(self) -> int:
        """
            Access the decimation level from the TSDecimation
            :return: Integer decimation level
            :rtype: int
        """
        return self.time_series_decimation.level

    @decimation_level.setter
    def decimation_level(self, value: int) -> None:
        """
            Set the decimation level in the TSDecimation
        """
        self.time_series_decimation.level = value

    @property
    def decimation_factor(self) -> float:
        """
            Access the decimation factor from the TSDecimation
            :return: decimation factor
            :rtype: float
        """
        return self.time_series_decimation.factor

    @decimation_factor.setter
    def decimation_factor(self, value: float) -> None:
        """
            Set the decimation factor in the TSDecimation
        """
        self.time_series_decimation.factor = value

    @property
    def decimation_method(self) -> str:
        """
            Access the decimation method from the TSDecimation
            :return: Description of how decimation is performed
            :rtype: str
        """
        return self.time_series_decimation.method

    @decimation_method.setter
    def decimation_method(self, value: str) -> None:
        """
            Set the decimation level in the TSDecimation
        """
        self.time_series_decimation.method = value

    @property
    def decimation_anti_alias_filter(self) -> str:
        """
            Access the decimation anti_alias_filter description from the TSDecimation
            :return: Description of how anti_alias_filtering is performed
            :rtype: str
        """
        return self.time_series_decimation.anti_alias_filter

    @decimation_method.setter
    def decimation_anti_alias_filter(self, value: str) -> None:
        """
            Set the decimation_anti_alias_filter in the TSDecimation
        """
        self.time_series_decimation.anti_alias_filter = value

    @property
    def decimation_sample_rate(self) -> float:
        """
            Access the decimation sample rate from the TSDecimation
            :return: Time series sample rate after decimation (from the TSDecimation)
            :rtype: float
        """
        return self.time_series_decimation.sample_rate

    @property
    def sample_rate_decimation(self) -> float:
        """
            TODO: Delete this function in 2025.

            Access the decimation sample rate from the TSDecimation
            :return:Time series sample rate after decimation (from the TSDecimation)
            :rtype: str
        """
        msg = "sample_rate_decimation is deprecated -- use self.time_series_decimation.sample_rate"
        logger.warning(msg)
        return self.time_series_decimation.sample_rate

    @sample_rate_decimation.setter
    def sample_rate_decimation(self, value: float) -> None:
        """
            TODO: Delete this function in 2025.

            Set the decimation sample_rate_decimation in the TSDecimation
        """
        msg = "sample_rate_decimation is deprecated -- use self.time_series_decimation.sample_rate"
        logger.warning(msg)
        self.time_series_decimation.sample_rate = value

    #----- End (Possibly Temporary) methods for integrating TimeSeriesDecimation Class -----#

    #----- Begin (Possibly Temporary) methods for integrating ShortTimeFourierTransform Class -----#

    @property
    def stft(self):
        return self.short_time_fourier_transform

    @property
    def harmonic_indices(self):
        return self.short_time_fourier_transform.harmonic_indices

    #----- End (Possibly Temporary) methods for integrating ShortTimeFourierTransform Class -----#

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

    @property
    def channels_estimated(self) -> list:
        """channels for which fcs were estimated"""
        return [
            ch.component
            for ch in self.channels.values()
            if ch.component is not None
        ]

    @channels_estimated.setter
    def channels_estimated(self, value) -> None:
        """set channels esimated"""

        if value is None:
            self.logger.debug("Input channel name is None, skipping")
            return
        if not hasattr(value, "__iter__"):
            value = [value]

        for entry in value:
            if isinstance(entry, str):
                self.add_channel(FCChannel(component=entry))
            elif entry is None:
                continue
            elif isinstance(entry, FCChannel):
                self.add_channel(entry)
            else:
                msg = f"entry must be a string or type FCChannel not {type(entry)}"
                self.logger.error(msg)
                raise ValueError(msg)

    def has_channel(self, component: str) -> bool:
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

    def get_channel(self, component: str) -> FCChannel:
        """
        Get a channel

        :param component: channel component to look for
        :type component: string
        :return: FCChannel object based on channel type
        :rtype: :class:`mt_metadata.timeseries.Channel`

        """

        if self.has_channel(component):
            return self.channels[component]

    def add_channel(self, channel_obj: FCChannel) -> None:
        """
        Add a channel to the list, check if one exists if it does overwrite it

        :param channel_obj: channel object to add
        :type channel_obj: :class:`mt_metadata.transfer_functions.processing.fourier_coefficients.Channel`

        """
        if not isinstance(channel_obj, (FCChannel)):
            msg = f"Input must be metadata FCChannel not {type(channel_obj)}"
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
                ch = FCChannel()
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


    def is_valid_for_time_series_length(self, n_samples_ts: int) -> bool:
        """
            Given a time series of len n_samples_ts, checks if there are sufficient samples to STFT.

        """
        required_num_samples = (
            self.window.num_samples
            + (self.stft.min_num_stft_windows - 1) * self.window.num_samples_advance
        )
        if n_samples_ts < required_num_samples:
            msg = (
                f"{n_samples_ts} not enough samples for minimum of "
                f"{self.stft.min_num_stft_windows} stft windows of length "
                f"{self.window.num_samples} and overlap {self.window.overlap}"
            )
            self.logger.warning(msg)
            return False
        else:
            return True

    @property
    def fft_frequencies(self) -> np.ndarray:
        """ Returns the one-sided fft frequencies (without Nyquist)"""
        return self.window.fft_harmonics(self.sample_rate)

    def has_fcs_for_aurora_processing(
        self,
        decimation_level,  # TODO: FIXME - Circular import when dtyped. AuroraDecimationLevel,
        remote: bool
    ) -> bool:
        """

        Development notes:
         See TODO FIXME, when trying from mt_metadata.transfer_functions.processing.aurora.decimation_level import DecimationLevel as AuroraDecimationLevel
         we get a circular import.
        Parameters
        ----------
        decimation_level: mt_metadata.transfer_functions.processing.aurora.decimation_level.DecimationLevel
        remote: bool
            If True, we are looking for reference channels, not local channels in the FCGroup.

        Iterates over FCDecimation attributes:
            "channels_estimated": to ensure all expected channels are in the group
            "anti_alias_filter": check that the expected AAF was applied
            "sample_rate,
            "method",
            "prewhitening_type",
            "recoloring",
            "pre_fft_detrend_type",
            "min_num_stft_windows",
            "window",
            "harmonic_indices",
        Returns
        -------

        """
        # channels_estimated
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
            assert self.decimation_anti_alias_filter == decimation_level.anti_alias_filter
        except AssertionError:
            cond1 = decimation_level.anti_alias_filter == "default"
            cond2 = self.decimation_anti_alias_filter is None
            if cond1 & cond2:
                pass
            else:
                msg = (
                    "Antialias Filters Not Compatible -- need to add handling for "
                    f"{msg} FCdec {self.decimation_anti_alias_filter} and "
                    f"{msg} processing config:{decimation_level.anti_alias_filter}"
                )
                raise NotImplementedError(msg)

        # sample_rate
        try:
            assert (
                self.time_series_decimation.sample_rate
                == decimation_level.decimation.sample_rate
            )
        except AssertionError:
            msg = (
                f"Sample rates do not agree: fc {self.time_series_decimation.sample_rate} differs from "
                f"processing config {decimation_level.decimation.sample_rate}"
            )
            self.logger.info(msg)
            return False

        # method (fft, wavelet, etc.)
        # TODO: Add clarification that this is a TRANSFORM method, not a decimation method.
        try:
            assert self.short_time_fourier_transform.method == decimation_level.stft.method  # FFT, Wavelet, etc.
        except AssertionError:
            msg = (
                "Transform methods do not agree "
                f"{self.short_time_fourier_transform.method} != {decimation_level.stft.method}"
            )
            self.logger.info(msg)
            return False

        # prewhitening_type
        try:
            assert self.stft.prewhitening_type == decimation_level.stft.prewhitening_type
        except AssertionError:
            msg = (
                "prewhitening_type does not agree "
                f"{self.stft.prewhitening_type} != {decimation_level.stft.prewhitening_type}"
            )
            self.logger.info(msg)
            return False

        # recoloring
        try:
            assert self.stft.recoloring == decimation_level.stft.recoloring
        except AssertionError:
            msg = (
                "recoloring does not agree "
                f"{self.stft.recoloring} != {decimation_level.stft.recoloring}"
            )
            self.logger.info(msg)
            return False

        # pre_fft_detrend_type
        try:
            assert (
                self.stft.pre_fft_detrend_type
                == decimation_level.stft.pre_fft_detrend_type
            )
        except AssertionError:
            # TODO: FIXME: self.pre_fft_detrend_type should be deprecated, use TimeSeriesDecimation.pre_fft_detrend_type for this info.
            msg = (
                "pre_fft_detrend_type does not agree "
                f"{self.stft.pre_fft_detrend_type} != {decimation_level.stft.pre_fft_detrend_type}"
            )
            self.logger.info(msg)
            return False

        # min_num_stft_windows
        try:
            assert (
                self.stft.min_num_stft_windows
                == decimation_level.stft.min_num_stft_windows
            )
        except AssertionError:
            msg = (
                "min_num_stft_windows do not agree "
                f"{self.stft.min_num_stft_windows} != {decimation_level.stft.min_num_stft_windows}"
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
