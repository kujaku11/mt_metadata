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
import numpy as np
from collections import OrderedDict
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from mt_metadata.utils.validators import validate_value_type
from . import (
    Fdsn,
    Orientation,
    Person,
    Provenance,
    Location,
    TimePeriod,
    Run,
)
from mt_metadata.utils.list_dict import ListDict

# =============================================================================
attr_dict = get_schema("station", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
location_dict = get_schema("location", SCHEMA_FN_PATHS)
location_dict.add_dict(
    get_schema("declination", SCHEMA_FN_PATHS), "declination"
)
location_dict.add_dict(
    get_schema("geographic_location", SCHEMA_FN_PATHS),
    None,
)
attr_dict.add_dict(location_dict, "location")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "acquired_by",
    keys=["name", "comments", "organization"],
)
attr_dict.add_dict(get_schema("orientation", SCHEMA_FN_PATHS), "orientation")
attr_dict.add_dict(
    get_schema("provenance", SCHEMA_FN_PATHS),
    "provenance",
    keys=["comments", "creation_time", "log"],
)
attr_dict.add_dict(
    get_schema("software", SCHEMA_FN_PATHS), "provenance.software"
)
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "provenance.submitter",
    keys=["author", "email", "organization"],
)
attr_dict["provenance.submitter.email"]["required"] = True
attr_dict["provenance.submitter.organization"]["required"] = True

attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
attr_dict.add_dict(get_schema("copyright", SCHEMA_FN_PATHS), None)
attr_dict["release_license"]["required"] = False
attr_dict.add_dict(get_schema("citation", SCHEMA_FN_PATHS), None, keys=["doi"])
attr_dict["doi"]["required"] = False
# =============================================================================
class Station(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.fdsn = Fdsn()
        self._channels_recorded = []
        self.orientation = Orientation()
        self.acquired_by = Person()
        self.provenance = Provenance()
        self.location = Location()
        self.time_period = TimePeriod()
        self.runs = ListDict()
        super().__init__(attr_dict=attr_dict, **kwargs)

    def __add__(self, other):
        if isinstance(other, Station):
            self.runs.extend(other.runs)
            return self
        else:
            msg = f"Can only merge Station objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)

    def __len__(self):
        return len(self.runs)

    @property
    def channels_recorded(self):
        """
        A list of all channels recorded

        :return: list of all unique channels recorded for the station
        :rtype: list

        """
        ch_list = []
        for run in self.runs:
            ch_list += run.channels_recorded_all
        ch_list = sorted(set([cc for cc in ch_list if cc is not None]))
        if self._channels_recorded == []:
            return ch_list

        elif ch_list == []:
            return self._channels_recorded

        elif len(self._channels_recorded) != ch_list:
            return ch_list

    @channels_recorded.setter
    def channels_recorded(self, value):
        """
        set channels_recorded

        """
        if isinstance(value, np.ndarray):
            value = value.tolist()

        if value in [None, "None", "none", "NONE", "null"]:
            return
        elif isinstance(value, (list, tuple)):
            self._channels_recorded = value

        else:
            raise TypeError(
                "'channels_recorded' must be set with a list not "
                f"{type(value)}."
            )

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

    def add_run(self, run_obj):
        """
        Add a run, if one of the same name exists overwrite it.

        :param run_obj: run object to add
        :type run_obj: :class:`mt_metadata.timeseries.Run`

        """

        if not isinstance(run_obj, Run):
            raise TypeError(
                f"Input must be a mt_metadata.timeseries.Run object not {type(run_obj)}"
            )

        if self.has_run(run_obj.id):
            self.runs[run_obj.id].update(run_obj)
            self.logger.debug(
                f"Station {run_obj.id} already exists, updating metadata"
            )
        else:
            self.runs.append(run_obj)

    def get_run(self, run_id):
        """
        Get a :class:`mt_metadata.timeseries.Run` object from the given
        id

        :param run_id: run id verbatim
        :type run_id: string

        """

        if self.has_run(run_id):
            return self.runs[run_id]
        self.logger.warning(f"Could not find {run_id} in runs.")
        return None

    def remove_run(self, run_id):
        """
        remove a run from the survey

        :param run_id: run id verbatim
        :type run_id: string

        """

        if self.has_run(run_id):
            self.runs.remove(run_id)
        else:
            self.logger.warning(f"Could not find {run_id} to remove.")

    @property
    def runs(self):
        """Return run list"""
        return self._runs

    @runs.setter
    def runs(self, value):
        """set the run list"""
        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input run_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

        fails = []
        self._runs = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, run in enumerate(value_list):

            if isinstance(run, (dict, OrderedDict)):
                r = Run()
                r.from_dict(run)
                self._runs.append(r)
            elif not isinstance(run, Run):
                msg = f"Item {ii} is not type(Run); type={type(run)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                self._runs.append(run)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

    @property
    def run_list(self):
        """Return names of run in survey"""
        return self.runs.keys()

    @run_list.setter
    def run_list(self, value):
        """Set list of run names"""

        if not hasattr(value, "__iter__"):
            msg = (
                "input station_list must be an iterable, should be a list "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)
        value = validate_value_type(value, str, "name_list")

        for run in value:
            if not isinstance(run, str):
                try:
                    run = str(run)
                except (ValueError, TypeError):
                    msg = f"could not convert {run} to string"
                    self.logger.error(msg)
                    raise ValueError(msg)
            run = run.replace("'", "").replace('"', "")
            if run not in self.runs.keys():
                self.add_run(Run(id=run))

    def update_time_period(self):
        """
        update time period from run information
        """
        start = []
        end = []
        for run in self.runs:
            if run.time_period.start != "1980-01-01T00:00:00+00:00":
                start.append(run.time_period.start)
            if run.time_period.start != "1980-01-01T00:00:00+00:00":
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
