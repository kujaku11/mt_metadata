# =====================================================
# Imports
# =====================================================
from collections import OrderedDict
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import (
    computed_field,
    Field,
    field_validator,
    model_validator,
    ValidationInfo,
)
from typing_extensions import Self

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    AuthorPerson,
    Comment,
    DataTypeEnum,
    Fdsn,
    Provenance,
    TimePeriod,
)
from mt_metadata.common.list_dict import ListDict
from mt_metadata.timeseries import Auxiliary, DataLogger, Electric, Magnetic


# =====================================================


class Run(MetadataBase):
    channels_recorded_auxiliary: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of auxiliary channels recorded",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["[T]"],
            },
        ),
    ]

    channels_recorded_electric: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of electric channels recorded",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["[Ex , Ey]"],
            },
        ),
    ]

    channels_recorded_magnetic: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of magnetic channels recorded",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["[Hx , Hy , Hz]"],
            },
        ),
    ]

    @computed_field
    def channels_recorded_all(self) -> list[str]:
        """
        List of all channels recorded in the run.
        """
        return sorted(
            [ch.component for ch in self.channels.values() if ch.component is not None]
        )

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,  # type: ignore
            description="Any comments on the run.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["cows chewed cables"],
            },
        ),
    ]

    data_type: Annotated[
        DataTypeEnum,
        Field(
            default=DataTypeEnum.BBMT,
            description="Type of data recorded for this run.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["BBMT"],
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Run ID should be station name followed by a number or character.  Characters should only be used if the run number is small, if the run number is high consider using digits with zeros.  For example if you have 100 runs the run ID could be 001 or {station}001.",
            alias=None,
            pattern="^[a-zA-Z0-9_]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["001"],
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate for the run",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
                "examples": ["100"],
            },
        ),
    ]

    acquired_by: Annotated[
        AuthorPerson,
        Field(
            default_factory=AuthorPerson,  # type: ignore
            description="Information about the group that collected the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Person()"],
            },
        ),
    ]

    metadata_by: Annotated[
        AuthorPerson,
        Field(
            default_factory=AuthorPerson,  # type: ignore
            description="Information about the group that collected the metadata.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Person()"],
            },
        ),
    ]

    provenance: Annotated[
        Provenance,
        Field(
            default_factory=Provenance,  # type: ignore
            description="Provenance information about the run.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Provenance()"],
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,  # type: ignore
            description="Time period for the run.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["TimePeriod(start='2020-01-01', end='2020-12-31')"],
            },
        ),
    ]

    data_logger: Annotated[
        DataLogger,
        Field(
            default_factory=DataLogger,  # type: ignore
            description="Data Logger information used to collect the run.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["DataLogger()"],
            },
        ),
    ]

    fdsn: Annotated[
        Fdsn,
        Field(
            default_factory=Fdsn,  # type: ignore
            description="FDSN information for the run.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["Fdsn()"],
            },
        ),
    ]

    channels: Annotated[
        ListDict | list | dict | OrderedDict,
        Field(
            default_factory=ListDict,
            description="ListDict of channel objects collected in this run.",
            alias=None,
            exclude=True,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["ListDict(Electric(), Magnetic(), Auxiliary())"],
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("data_type", mode="before")
    @classmethod
    def validate_data_type(cls, value, info: ValidationInfo) -> str:
        """
        Validate that the data_type is a string.
        """
        if isinstance(value, DataTypeEnum):
            value = value.value
        elif isinstance(value, str):
            if "," in value:
                value = value.split(",")[0].strip()
        elif not isinstance(value, str):
            raise TypeError(f"data_type must be a string, not {type(value)}")
        return value

    @field_validator(
        "channels_recorded_electric",
        "channels_recorded_magnetic",
        "channels_recorded_auxiliary",
        mode="before",
    )
    @classmethod
    def validate_list_of_strings(
        cls, value: np.ndarray | list[str] | str, info: ValidationInfo
    ) -> list[str]:
        """
        Validate that the value is a list of strings.
        """
        if value in [None, "None", "none", "NONE", "null"]:
            return []

        if isinstance(value, np.ndarray):
            value = value.astype(str).tolist()

        elif isinstance(value, (list, tuple)):
            value = [str(v) for v in value]

        elif isinstance(value, (str)):
            value = [v.strip() for v in value.split(",")]

        else:
            raise TypeError(
                "'channels_recorded' must be set with a list of strings not "
                f"{type(value)}."
            )
        return value

    @model_validator(mode="after")
    def validate_channels_recorded(self) -> Self:
        """
        Validate that the value is a list of strings.
        """
        # need to make each another object list() otherwise the contents
        # get overwritten with the new channel.
        for electric in list(self.channels_recorded_electric):
            if electric not in self.channels.keys():
                self.add_channel(Electric(component=electric))  # type: ignore
        for magnetic in list(self.channels_recorded_magnetic):
            if magnetic not in self.channels.keys():
                self.add_channel(Magnetic(component=magnetic))  # type: ignore
        for auxiliary in list(self.channels_recorded_auxiliary):
            if auxiliary not in self.channels.keys():
                self.add_channel(Auxiliary(component=auxiliary))  # type: ignore
        return self

    @field_validator("channels", mode="before")
    @classmethod
    def validate_channels(cls, value, info: ValidationInfo) -> ListDict:
        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input run_list must be an iterable, should be a list or dict "
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
                channels.append(cls._get_correct_channel_type(channel))
            except KeyError as error:
                msg = f"Could not find type in {channel}"
                logger.error(msg)
                logger.exception(error)
                fails.append(msg)

        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        return channels

    def _empty_channels_recorded(self):
        """
        Empty the channels recorded lists.
        """
        self.channels_recorded_auxiliary.clear()
        self.channels_recorded_electric.clear()
        self.channels_recorded_magnetic.clear()

    def _update_channels_recorded(self):
        """
        Update the channels recorded lists based on the channels in the run.
        """
        self._empty_channels_recorded()
        aux_components = [
            ch.component
            for ch in self.channels
            if isinstance(ch, Auxiliary)
            and ch.component not in [None, "auxiliary_default"]
        ]
        elec_components = [
            ch.component
            for ch in self.channels
            if isinstance(ch, Electric) and ch.component not in [None, "e_default"]
        ]
        mag_components = [
            ch.component
            for ch in self.channels
            if isinstance(ch, Magnetic) and ch.component not in [None, "h_default"]
        ]
        self.channels_recorded_auxiliary = sorted(aux_components)
        self.channels_recorded_electric = sorted(elec_components)
        self.channels_recorded_magnetic = sorted(mag_components)

    # def __len__(self):
    #     return len(self.channels)

    def merge(self, other, inplace=True):
        if isinstance(other, Run):
            self.channels.extend(other.channels)
            self._update_channels_recorded()
            if inplace:
                self.update_time_period()
            else:
                return self.copy()
        else:
            msg = f"Can only merge Run objects, not {type(other)}"
            logger.error(msg)
            raise TypeError(msg)

    def update(self, other, match=[]):
        """
        Update attribute values from another like element, skipping None

        :param other: DESCRIPTION
        :type other: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        # Check if other is a compatible Run type (handles dynamically created classes)
        if not (
            isinstance(other, type(self))
            or (hasattr(other, "__class__") and other.__class__.__name__ == "Run")
        ):
            logger.warning(f"Cannot update {type(self)} with {type(other)}")
        for k in match:
            if self.get_attr_from_name(k) != other.get_attr_from_name(k):
                msg = (
                    f"{k} is not equal {self.get_attr_from_name(k)} != "
                    "{other.get_attr_from_name(k)}"
                )
                logger.error(msg)
                raise ValueError(msg)
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

    def has_channel(self, component):
        """
        Check to see if the channel already exists

        :param component: channel component to look for
        :type component: string
        :return: True if found, False if not
        :rtype: boolean

        """

        if component in [cc for cc in self.channels_recorded_all]:
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

    def add_channel(self, channel_obj, update=True):
        """
        Add a channel to the run.
        If the channel already exists, update the metadata.
        If the channel does not exist, add it to the list.
        If the channel is a string, create a new channel object assuming the input
        string is the component name.

        parameters
        ----------
        channel_obj: channel object to add to the run
        update: boolean to update the time period of the run
            if True, update the time period of the run to match the channel
            if False, do not update the time period of the run


        """
        channel_obj = self._get_correct_channel_type(channel_obj)

        if self.has_channel(channel_obj.component):
            self.channels[channel_obj.component].update(channel_obj)
            logger.debug(
                f"Run {channel_obj.component} already exists, updating metadata"
            )

        else:
            self.channels.append(channel_obj)

        self._update_channels_recorded()

        if update:
            self.update_time_period()

    def remove_channel(self, channel_id):
        """
        remove a run from the survey

        :param component: channel component to look for
        :type component: string

        """

        if self.has_channel(channel_id):
            self.channels.remove(channel_id)

            self._update_channels_recorded()
        else:
            logger.warning(f"Could not find {channel_id} to remove.")

    def update_channel_keys(self):
        """
        Update the keys in the channels ListDict to match current channel components.

        This is useful when channel components have been modified after channels were
        added to the run, ensuring that channels can be accessed by their
        current component values.

        :returns: mapping of old keys to new keys
        :rtype: dict

        Example:
            >>> run = Run()
            >>> channel = Electric()
            >>> channel.component = ""  # empty component initially
            >>> run.add_channel(channel)
            >>> channel.component = "ex"  # update the component
            >>> key_mapping = run.update_channel_keys()
            >>> print(key_mapping)  # {'': 'ex'}
            >>> # Now channel can be accessed as run.channels['ex']
        """
        return self.channels.update_keys()

    @property
    def n_channels(self):
        return len(self.channels)

    def update_time_period(self):
        """
        update time period from the channels
        """
        if self.n_channels > 0:
            start = []
            end = []
            for channel in self.channels:
                if channel.time_period.start != "1980-01-01T00:00:00+00:00":
                    start.append(channel.time_period.start)
                if channel.time_period.end != "1980-01-01T00:00:00+00:00":
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

    @classmethod
    def _get_correct_channel_type(self, channel_obj):
        """
        Get the correct channel type based on the input channel object.

        :param channel_obj: channel object to check
        :type channel_obj: Channel
        :return: correct channel type
        :rtype: Channel

        """
        if isinstance(channel_obj, str):
            if channel_obj.lower().startswith("e"):
                return Electric(component=channel_obj)
            elif (
                channel_obj.lower().startswith("h")
                or channel_obj.lower().startswith("b")
                or channel_obj.lower() in ["magnetic"]
            ):
                return Magnetic(component=channel_obj)
            else:
                return Auxiliary(component=channel_obj)

        elif isinstance(channel_obj, (dict, OrderedDict)):
            try:
                ch_type = channel_obj["type"]
                if ch_type is None:
                    ch_type = channel_obj["component"][0]

                if ch_type.lower().startswith("e"):
                    return Electric(**channel_obj)
                elif (
                    ch_type.lower().startswith("b")
                    or ch_type.lower().startswith("b")
                    or ch_type.lower() in ["magnetic"]
                ):
                    return Magnetic(**channel_obj)
                else:
                    return Auxiliary(**channel_obj)
            except KeyError as error:
                msg = f"Could not find type in {channel_obj}"
                logger.error(msg)
                logger.exception(error)
                raise error

        elif isinstance(channel_obj, (Electric, Magnetic, Auxiliary)):
            if channel_obj.component is None:
                if not isinstance(channel_obj, Auxiliary):
                    msg = "component cannot be empty"
                    logger.error(msg)
                    raise ValueError(msg)
            return channel_obj
        else:
            msg = (
                f"Input must be mt_metadata.timeseries.Channel not {type(channel_obj)}"
            )
            logger.error(msg)
            raise ValueError(msg)
