# -*- coding: utf-8 -*-
"""
    This module contains the Decimation Metadata class.  This class interacts with a decimation JSON.
    It contains the metadata to specify a transformation from time series to a Spectrogram, including
    cascadng decimation info.

    There are two main use cases for this class.  On the one hand, this can be used to specify a
    set of processing parameters to create an FCDecimation, which can then be stored in an MTH5 archive.
    On the other hand, this metadata gets stored along with Spectrograms in an MTH5 archive and can
    be used to access the parameters associated with the spectrograms creation.

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
from typing import List, Optional

from .standards import SCHEMA_FN_PATHS
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries import TimePeriod
from mt_metadata.transfer_functions.processing.short_time_fourier_transform import ShortTimeFourierTransform
from mt_metadata.transfer_functions.processing.time_series_decimation import TimeSeriesDecimation
# from mt_metadata.transfer_functions.processing.aurora.decimation_level import DecimationLevel as AuroraDecimationLevel
from mt_metadata.transfer_functions.processing.fourier_coefficients import (
    Channel as FCChannel
)
from mt_metadata.utils.list_dict import ListDict

import numpy as np
# =============================================================================
attr_dict = get_schema("decimation", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict, "time_period")
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
        self.time_period = TimePeriod()
        self.channels = ListDict()
        self.time_series_decimation = TimeSeriesDecimation()
        self.short_time_fourier_transform = ShortTimeFourierTransform()

        super().__init__(attr_dict=attr_dict, **kwargs)

        if self.short_time_fourier_transform.per_window_detrend_type:
            msg = f"per_window_detrend_type was set to {self.short_time_fourier_transform.per_window_detrend_type}"
            msg += "however, this is not supported -- setting to empty string"
            logger.debug(msg)
            self.short_time_fourier_transform.per_window_detrend_type = ""

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
    def decimation_sample_rate(self) -> float:
        """
            Access the decimation sample rate from the TSDecimation
            :return: Time series sample rate after decimation (from the TSDecimation)
            :rtype: float
        """
        return self.time_series_decimation.sample_rate


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
            self.stft.window.num_samples
            + (self.stft.min_num_stft_windows - 1) * self.stft.window.num_samples_advance
        )
        if n_samples_ts < required_num_samples:
            msg = (
                f"{n_samples_ts} not enough samples for minimum of "
                f"{self.stft.min_num_stft_windows} stft windows of length "
                f"{self.stft.window.num_samples} and overlap {self.stft.window.overlap}"
            )
            self.logger.warning(msg)
            return False
        else:
            return True

    @property
    def fft_frequencies(self) -> np.ndarray:
        """ Returns the one-sided fft frequencies (without Nyquist)"""
        return self.stft.window.fft_harmonics(self.sample_rate)


def fc_decimations_creator(
    initial_sample_rate: float,
    decimation_factors: Optional[list] = None,
    max_levels: Optional[int] = 6,
    time_period: Optional[TimePeriod] = None,
) -> List[Decimation]:
    """

    Creates mt_metadata FCDecimation objects that parameterize Fourier coefficient decimation levels.

    Note 1:  This does not yet work through the assignment of which bands to keep.  Refer to
    mt_metadata.transfer_functions.processing.Processing.assign_bands() to see how this was done in the past

    Parameters
    ----------
    initial_sample_rate: float
        Sample rate of the "level0" data -- usually the sample rate during field acquisition.
    decimation_factors: Optional[list]
        The decimation factors that will be applied at each FC decimation level
    max_levels: Optional[int]
        The maximum number of decimation levels to allow
    time_period: Optional[TimePeriod]
        Provides the start and end times

    Returns
    -------
    fc_decimations: list
        Each element of the list is an object of type
        mt_metadata.transfer_functions.processing.fourier_coefficients.Decimation,
        (a.k.a. FCDecimation).

        The order of the list corresponds the order of the cascading decimation
          - No decimation levels are omitted.
          - This could be changed in future by using a dict instead of a list,
          - e.g. decimation_factors = dict(zip(np.arange(max_levels), decimation_factors))

    """
    if not decimation_factors:
        # msg = "No decimation factors given, set default values to EMTF default values [1, 4, 4, 4, ..., 4]")
        # logger.info(msg)
        default_decimation_factor = 4
        decimation_factors = max_levels * [default_decimation_factor]
        decimation_factors[0] = 1

    # See Note 1
    fc_decimations = []
    for i_dec_level, decimation_factor in enumerate(decimation_factors):
        fc_dec = Decimation()
        fc_dec.time_series_decimation.level = i_dec_level
        fc_dec.id = f"{i_dec_level}"
        fc_dec.time_series_decimation.factor = decimation_factor
        if i_dec_level == 0:
            current_sample_rate = 1.0 * initial_sample_rate
        else:
            current_sample_rate /= decimation_factor
        fc_dec.time_series_decimation.sample_rate = current_sample_rate

        if time_period:
            if isinstance(time_period, TimePeriod):
                fc_dec.time_period = time_period
            else:
                msg = (
                    f"Not sure how to assign time_period with type {type(time_period)}"
                )
                logger.info(msg)
                raise NotImplementedError(msg)

        fc_decimations.append(fc_dec)

    return fc_decimations
