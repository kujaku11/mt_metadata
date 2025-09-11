# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated, List, Optional

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, model_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import ListDict, TimePeriod
from mt_metadata.processing.fourier_coefficients.fc_channel_basemodel import FCChannel
from mt_metadata.processing.short_time_fourier_transform_basemodel import (
    ShortTimeFourierTransform,
)
from mt_metadata.processing.time_series_decimation_basemodel import TimeSeriesDecimation


# =====================================================
class Decimation(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Decimation level ID",
            examples=["1"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_estimated: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="list of channels",
            examples=["[ex, hy]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,  # type: ignore
            description="Time period over which these FCs were estimated",
            examples=["TimePeriod()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels: Annotated[
        ListDict,
        Field(
            default_factory=ListDict,
            description="List of channels",
            examples=["[ex, hy]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    time_series_decimation: Annotated[
        TimeSeriesDecimation,
        Field(
            default_factory=TimeSeriesDecimation,  # type: ignore
            description="Time series decimation settings",
            examples=["TimeSeriesDecimation()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    short_time_fourier_transform: Annotated[
        ShortTimeFourierTransform,
        Field(
            default_factory=ShortTimeFourierTransform,  # type: ignore
            description="Short time Fourier transform settings",
            examples=["ShortTimeFourierTransform()"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("short_time_fourier_transform", mode="before")
    @classmethod
    def validate_short_time_fourier_transform(
        cls, value: ShortTimeFourierTransform, info: ValidationInfo
    ) -> ShortTimeFourierTransform:
        if not isinstance(value, ShortTimeFourierTransform):
            msg = f"Input must be metadata ShortTimeFourierTransform not {type(value)}"
            raise TypeError(msg)
        if value.per_window_detrend_type:
            msg = f"per_window_detrend_type was set to {value.per_window_detrend_type}"
            msg += "however, this is not supported -- setting to empty string"
            logger.debug(msg)
            value.per_window_detrend_type = ""
        return value

    @field_validator("channels_estimated", mode="before")
    @classmethod
    def validate_channels_estimated(
        cls, value: list[str], info: ValidationInfo
    ) -> list[str]:
        if not isinstance(value, list):
            msg = f"Input must be a list of strings not {type(value)}"
            raise TypeError(msg)
        for item in value:
            if not isinstance(item, str):
                msg = f"All items in the list must be strings not {type(item)}"
                raise TypeError(msg)
        return value

    @field_validator("channels", mode="before")
    @classmethod
    def validate_channels(cls, value: ListDict, info: ValidationInfo) -> ListDict:
        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input ch_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            logger.error(msg)
            raise TypeError(msg)

        fails = []
        channels = ListDict()
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
                channels.append(ch)
            except Exception as error:
                msg = "Could not create channel from dictionary: %s"
                fails.append(msg % error)
                logger.error(msg, error)

        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        return channels

    @model_validator(mode="after")
    @classmethod
    def validate_channels_consistency(cls, values):
        """
        Ensure that channels_estimated and channels are synchronized.

        - If a channel name exists in channels_estimated but not in channels,
          create a new FCChannel with that component name
        - Ensure all channels in channels ListDict have their component names
          in channels_estimated
        """
        channels_estimated = values.channels_estimated
        channels = values.channels

        # Get existing channel component names from the channels ListDict
        existing_channel_names = set(channels.keys()) if channels.keys() else set()

        # Get the set of estimated channel names
        estimated_channel_names = (
            set(channels_estimated) if channels_estimated else set()
        )

        # Find channels that are estimated but don't exist in channels ListDict
        missing_channels = estimated_channel_names - existing_channel_names

        # Create FCChannel objects for missing channels
        for channel_name in missing_channels:
            logger.info(f"Creating FCChannel for estimated channel: {channel_name}")
            new_channel = FCChannel(component=channel_name)
            channels.append(new_channel)

        # Find channels in ListDict that aren't in channels_estimated and add them
        extra_channels = existing_channel_names - estimated_channel_names
        if extra_channels:
            logger.info(f"Adding channels to channels_estimated: {extra_channels}")
            # Add the extra channel names to channels_estimated
            values.channels_estimated.extend(list(extra_channels))

        return values

    def add(self, other):
        """

        :param other:
        :return:
        """
        if isinstance(other, Decimation):
            self.channels.extend(other.channels)

            return self
        else:
            msg = f"Can only merge ch objects, not {type(other)}"
            logger.error(msg)
            raise TypeError(msg)

    # ----- Begin (Possibly Temporary) methods for integrating TimeSeriesDecimation, STFT Classes -----#

    @property
    def decimation(self) -> TimeSeriesDecimation:
        """
        Passthrough method to access self.time_series_decimation
        """
        return self.time_series_decimation

    @property
    def stft(self):
        return self.short_time_fourier_transform

    # ----- End (Possibly Temporary) methods for integrating TimeSeriesDecimation, STFT Classes -----#

    def update(self, other, match=[]):
        """
        Update attribute values from another like element, skipping None

        :param other: DESCRIPTION
        :type other: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if not isinstance(other, type(self)):
            logger.warning("Cannot update %s with %s", type(self), type(other))
        for k in match:
            if self.get_attr_from_name(k) != other.get_attr_from_name(k):
                msg = "%s is not equal %s != %s"
                logger.error(
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
                    self.update_attribute(k, v)
            else:
                if v not in [None, 0.0, [], "", "1980-01-01T00:00:00+00:00"]:
                    self.update_attribute(k, v)

        ## Need this because channels are set when setting channels_recorded
        ## and it initiates an empty channel, but we need to fill it with
        ## the appropriate metadata.
        for ch in other.channels:
            self.add_channel(ch)

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

    def get_channel(self, component: str) -> FCChannel | None:
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
            logger.error(msg)
            raise ValueError(msg)

        if self.has_channel(channel_obj.component):
            self.channels[channel_obj.component].update(channel_obj)
            logger.debug(
                f"ch {channel_obj.component} already exists, updating metadata"
            )

        else:
            self.channels.append(channel_obj)

        self.update_time_period()

    def remove_channel(self, channel_id: str) -> None:
        """
        remove a channel from the survey

        :param component: channel component to look for
        :type component: string

        """

        if self.has_channel(channel_id):
            self.channels.remove(channel_id)
        else:
            logger.warning(f"Could not find {channel_id} to remove.")

        self.update_time_period()

    @property
    def n_channels(self):
        return len(self.channels)

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
            + (self.stft.min_num_stft_windows - 1)
            * self.stft.window.num_samples_advance
        )
        if n_samples_ts < required_num_samples:
            msg = (
                f"{n_samples_ts} not enough samples for minimum of "
                f"{self.stft.min_num_stft_windows} stft windows of length "
                f"{self.stft.window.num_samples} and overlap {self.stft.window.overlap}"
            )
            logger.warning(msg)
            return False
        else:
            return True

    @property
    def fft_frequencies(self) -> np.ndarray:
        """Returns the one-sided fft frequencies (without Nyquist)"""
        return self.stft.window.fft_harmonics(self.decimation.sample_rate)


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


def get_degenerate_fc_decimation(sample_rate: float) -> list:
    """
        WIP

        Makes a default fc_decimation list.
        This "degenerate" config will only operate on the first decimation level.
        This is useful for testing.  It could also be used in future on an MTH5 stored
        time series in decimation levels already as separate runs.

    Parameters
    ----------
    sample_rate: float
        The sample rate associated with the time-series to convert to spectrogram

    Returns
    -------
    output: list
        List has only one element which is of type FCDecimation, aka.

    """
    output = fc_decimations_creator(
        sample_rate,
        decimation_factors=[
            1,
        ],
        max_levels=1,
    )
    return output
