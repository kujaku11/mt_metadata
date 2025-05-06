# =====================================================
# Imports
# =====================================================
from typing import Annotated
from loguru import logger
from collections import OrderedDict
from typing_extensions import Self

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    Fdsn,
    TimePeriod,
    Person,
    Provenance,
    DataTypeEnum,
)

from mt_metadata.timeseries import DataLogger, Auxiliary, Electric, Magnetic
from mt_metadata.utils.list_dict import ListDict
from pydantic import (
    Field,
    field_validator,
    ValidationInfo,
    computed_field,
    model_validator,
)


# =====================================================


class Run(MetadataBase):
    channels_recorded_auxiliary: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of auxiliary channels recorded",
            examples="[T]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_recorded_electric: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of electric channels recorded",
            examples="[Ex , Ey]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channels_recorded_magnetic: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of magnetic channels recorded",
            examples='"[Hx , Hy , Hz]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
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
            default_factory=Comment,
            description="Any comments on the run.",
            examples="cows chewed cables",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data_type: Annotated[
        DataTypeEnum,
        Field(
            default="BBMT",
            description="Type of data recorded for this run.",
            examples="BBMT",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Run ID should be station name followed by a number or character.  Characters should only be used if the run number is small, if the run number is high consider using digits with zeros.  For example if you have 100 runs the run ID could be 001 or {station}001.",
            examples="001",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate for the run",
            examples="100",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    acquired_by: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Information about the group that collected the data.",
            examples="Person()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    metadata_by: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Information about the group that collected the metadata.",
            examples="Person()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    provenance: Annotated[
        Provenance,
        Field(
            default_factory=Provenance,
            description="Provenance information about the run.",
            examples="Provenance()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,
            description="Time period for the run.",
            examples="TimePeriod(start='2020-01-01', end='2020-12-31')",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    data_logger: Annotated[
        DataLogger,
        Field(
            default_factory=DataLogger,
            description="Data Logger information used to collect the run.",
            examples="DataLogger()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    fdsn: Annotated[
        Fdsn,
        Field(
            default_factory=Fdsn,
            description="FDSN information for the run.",
            examples="Fdsn()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    channels: Annotated[
        ListDict | list | dict | OrderedDict,
        Field(
            default_factory=ListDict,
            description="ListDict of channel objects collected in this run.",
            examples="ListDict(Electric(), Magnetic(), Auxiliary())",
            alias=None,
            exclude=True,
            json_schema_extra={
                "units": None,
                "required": False,
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

    @model_validator(mode="after")
    def validate_channels_recorded(self) -> Self:
        """
        Validate that the value is a list of strings.
        """
        # need to make each another object list() otherwise the contents
        # get overwritten with the new channel.
        for electric in list(self.channels_recorded_electric):
            if electric not in self.channels.keys():
                self.add_channel(Electric(component=electric))
        for magnetic in list(self.channels_recorded_magnetic):
            if magnetic not in self.channels.keys():
                self.add_channel(Magnetic(component=magnetic))
        for auxiliary in list(self.channels_recorded_auxiliary):
            if auxiliary not in self.channels.keys():
                self.add_channel(Auxiliary(component=auxiliary))
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
                    channels.append(ch)
                except KeyError as error:
                    msg = f"Item {ii} is not type(channel); type={type(channel)}"
                    fails.append(msg)
                    logger.error(msg)
                    logger.exception(error)
            elif not isinstance(channel, (Auxiliary, Electric, Magnetic)):
                msg = f"Item {ii} is not type(channel); type={type(channel)}"
                fails.append(msg)
                logger.error(msg)
            else:
                channels.append(channel)
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
        self.channels_recorded_auxiliary = sorted(
            [ch.component for ch in self.channels if isinstance(ch, Auxiliary)]
        )
        self.channels_recorded_electric = sorted(
            [ch.component for ch in self.channels if isinstance(ch, Electric)]
        )
        self.channels_recorded_magnetic = sorted(
            [ch.component for ch in self.channels if isinstance(ch, Magnetic)]
        )

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
        if not isinstance(other, type(self)):
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
        if isinstance(channel_obj, (str)):

            if channel_obj in ["electric", "e"]:
                channel_obj = Electric(component=channel_obj)
            elif channel_obj in ["magnetic", "b", "h"]:
                channel_obj = Magnetic(component=channel_obj)
            else:
                channel_obj = Auxiliary(component=channel_obj)

        elif not isinstance(channel_obj, (Magnetic, Electric, Auxiliary)):
            msg = f"Input must be metadata.Channel not {type(channel_obj)}"
            logger.error(msg)
            raise ValueError(msg)

        if channel_obj.component is None:
            if not isinstance(channel_obj, Auxiliary):
                msg = "component cannot be empty"
                logger.error(msg)
                raise ValueError(msg)

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
