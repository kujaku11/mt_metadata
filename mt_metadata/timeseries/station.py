# =====================================================
# Imports
# =====================================================
from typing import Annotated
from typing_extensions import Self
import numpy as np
from collections import OrderedDict
from loguru import logger

from pydantic import Field, ValidationInfo, field_validator, model_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    DataTypeEnum,
    ChannelLayoutEnum,
    StationLocation,
    Provenance,
    TimePeriod,
    Person,
    Orientation,
    Fdsn,
)
from mt_metadata.utils.list_dict import ListDict
from mt_metadata.timeseries import Run

# =====================================================


class Station(MetadataBase):
    channel_layout: Annotated[
        ChannelLayoutEnum,
        Field(
            default="x",
            description="How the station channels were laid out.",
            examples="x",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    channels_recorded: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of components recorded by the station. Should be a summary of all channels recorded. Dropped channels will be recorded in Run metadata.",
            examples='"[ Ex, Ey, Hx, Hy, Hz, T]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments on the station.",
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
            description="Type of data recorded. If multiple types input as a comma separated list.",
            examples="BBMT",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    fdsn: Annotated[
        Fdsn,
        Field(
            default_factory=Fdsn,
            description="FDSN information for the station.",
            examples="",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    geographic_name: Annotated[
        str,
        Field(
            default="",
            description="Closest geographic name to the station, usually a city, but could be another common geographic location.",
            examples='"Whitehorse, YK"',
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
            description="Station ID name.  This should be an alpha numeric name that is typically 5-6 characters long.  Commonly the project name in 2 or 3 letters and the station number.",
            examples="MT001",
            alias=None,
            pattern="^[a-zA-Z0-9]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    run_list: Annotated[
        list[str],
        Field(
            default_factory=list,
            items={"type": "string"},
            description="List of runs recorded by the station. Should be a summary of all runs recorded.",
            examples='"[ mt001a, mt001b, mt001c ]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    location: Annotated[
        StationLocation,
        Field(
            default_factory=StationLocation,
            description="Location of the station.",
            examples="",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    orientation: Annotated[
        Orientation,
        Field(
            default_factory=Orientation,
            description="Orientation of the station.",
            examples="",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    acquired_by: Annotated[
        Person,
        Field(
            default_factory=Person,
            description="Group or person who acquired the data.",
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
            description="Provenance of the data.",
            examples="",
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
            description="Time period of the data.",
            examples="",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    runs: Annotated[
        ListDict | list | dict | OrderedDict | tuple,
        Field(
            default_factory=ListDict,
            description="List of runs recorded by the station.",
            examples="",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("channels_recorded", "run_list", mode="before")
    @classmethod
    def validate_list_of_strings(cls, value, info: ValidationInfo) -> list[str]:
        """
        Validate that the value is a list of strings.
        """
        if value in [None, "None", "none", "NONE", "null"]:
            return

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
    def validate_runs_and_channels_recorded(self) -> Self:
        """
        Validate that the value is a list of strings.
        """

        # need to make each another object list() otherwise the contents
        # get overwritten with the new channel.
        if self.run_list != list(self.runs.keys()):
            if len(self.run_list) > len(self.runs.keys()):
                for run_id in self.run_list:
                    if run_id not in self.runs.keys():
                        self.runs.append(Run(id=run_id))
            else:
                self.update_all()
        estimate_channels_recorded = self._get_channels_recorded()
        if self.channels_recorded != estimate_channels_recorded:
            if len(self.channels_recorded) > len(estimate_channels_recorded):
                if len(self.runs) > 0:
                    for channel in self.channels_recorded:
                        if channel not in estimate_channels_recorded:
                            self.runs[0].add_channel(channel)
            else:
                self.update_channels_recorded()
        return self

    @model_validator(mode="after")
    def validate_station_id(self) -> Self:
        """
        Validate that the value is a list of strings.
        """
        if self.id in [None, "None", "none", "NONE", "null", ""]:
            if self.fdsn.id is not None:
                self.id = self.fdsn.id

        return self

    @field_validator("runs", mode="before")
    @classmethod
    def validate_runs(cls, value, info: ValidationInfo) -> ListDict:
        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input runs must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            logger.error(msg)
            raise TypeError(msg)

        fails = []
        runs = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, run_entry in enumerate(value_list):

            if isinstance(run_entry, (dict, OrderedDict)):
                try:
                    run = Run()
                    run.from_dict(run_entry)
                    runs.append(run)
                except KeyError:
                    msg = f"Item {ii} is not type(Run); type={type(run_entry)}"
                    fails.append(msg)
                    logger.error(msg)
            elif not isinstance(run_entry, (Run)):
                msg = f"Item {ii} is not type(Run); type={type(run_entry)}"
                fails.append(msg)
                logger.error(msg)
            else:
                runs.append(run_entry)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        return runs

    def merge(self, other, inplace=False):
        if isinstance(other, Station):
            self.runs.extend(other.runs)
            self.update_all()
            if not inplace:
                return self
        else:
            msg = f"Can only merge Station objects, not {type(other)}"
            logger.error(msg)
            raise TypeError(msg)

    @property
    def n_runs(self) -> int:
        """
        Return the number of runs in the station.

        :return: number of runs in the station
        :rtype: int

        """
        return len(self.runs)

    def has_run(self, run_id):
        """
        Check to see if the run id already exists

        :param run_id: run id verbatim
        :type run_id: string
        :return: Tru if exists, False if not
        :rtype: boolean

        """
        if run_id in self.run_list:
            return True
        return False

    def run_index(self, run_id):
        """
        Get the index of the run_id

        :param run_id: run id verbatim
        :type run_id: string
        :return: index of the run
        :rtype: integer

        """

        if self.has_run(run_id):
            return self.run_list.index(run_id)
        return None

    def _empty_channels_recorded(self):
        """
        Empty the channels recorded lists.
        """
        self.channels_recorded.clear()

    def _empty_run_list(self):
        """
        Empty the runs lists.
        """
        self.run_list.clear()

    def _get_channels_recorded(self) -> list[str]:
        """
        Get the channels recorded list.

        :return: channels recorded list
        :rtype: list[str]

        """
        ch_list = []
        for run in self.runs:
            ch_list += run.channels_recorded_all
        return sorted(set([cc for cc in ch_list if cc is not None]))

    def update_channels_recorded(self) -> None:
        """
        Update the channels recorded lists based on the channels in the run.
        """
        self._empty_channels_recorded()
        self.channels_recorded = self._get_channels_recorded()

    def update_run_list(self) -> None:
        """
        Update the run list based on the runs in the station.
        """
        self._empty_run_list()
        self.run_list = list(self.runs.keys())

    def update_time_period(self):
        """
        update time period from run information
        """
        if self.__len__() > 0:
            start = []
            end = []
            for run in self.runs:
                if run.time_period.start != "1980-01-01T00:00:00+00:00":
                    start.append(run.time_period.start)
                if run.time_period.end != "1980-01-01T00:00:00+00:00":
                    end.append(run.time_period.end)
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

    def update_all(self):
        """
        Update the time period, channels recorded and run list.

        """
        self.update_time_period()
        # self.update_channels_recorded()
        self.update_run_list()

    def add_run(self, run_obj, update=True):
        """
        Add a run, if one of the same name exists overwrite it.

        :param run_obj: run object to add
        :type run_obj: :class:`mt_metadata.timeseries.Run`

        """

        if not isinstance(run_obj, Run):
            raise TypeError(
                f"Input must be a mt_metadata.timeseries.Run object not {type(run_obj)}"
            )

        if run_obj.id is None:
            raise ValueError("The input run id is None. Input a string or integer.")
        if self.has_run(run_obj.id):
            self.runs[run_obj.id].update(run_obj)
            logger.debug(f"Station {run_obj.id} already exists, updating metadata")
        else:
            self.runs.append(run_obj)

        if update:
            self.update_all()

    def get_run(self, run_id):
        """
        Get a :class:`mt_metadata.timeseries.Run` object from the given
        id

        :param run_id: run id verbatim
        :type run_id: string

        """

        if self.has_run(run_id):
            return self.runs[run_id]
        logger.warning(f"Could not find {run_id} in runs.")
        return None

    def remove_run(self, run_id, update=True):
        """
        remove a run from the survey

        :param run_id: run id verbatim
        :type run_id: string

        """

        if self.has_run(run_id):
            self.runs.remove(run_id)
            if update:
                self.update_all()
        else:
            logger.warning(f"Could not find {run_id} to remove.")

    def sort_runs_by_time(self, inplace=True, ascending=True):
        """
        return a list of runs sorted by start time in the order of ascending or
        descending.

        :param ascending: DESCRIPTION, defaults to True
        :type ascending: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        run_ids = []
        run_starts = []
        for run_key, run_obj in self.runs.items():
            run_ids.append(run_key)
            run_starts.append(run_obj.time_period.start.split("+")[0])

        index = np.argsort(np.array(run_starts, dtype=np.datetime64))

        new_runs = ListDict()
        for ii in index:
            new_runs[run_ids[ii]] = self.runs[run_ids[ii]]

        if inplace:
            self.runs = new_runs
        else:
            return new_runs
