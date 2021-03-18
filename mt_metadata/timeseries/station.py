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
    Fdsn,
    Orientation,
    Person,
    Provenance,
    Location,
    TimePeriod,
    Run,
)

# =============================================================================
attr_dict = get_schema("station", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
location_dict = get_schema("location", SCHEMA_FN_PATHS)
location_dict.add_dict(get_schema("declination", SCHEMA_FN_PATHS), "declination")
attr_dict.add_dict(location_dict, "location")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS), "acquired_by", keys=["author", "comments"]
)
attr_dict.add_dict(get_schema("orientation", SCHEMA_FN_PATHS), "orientation")
attr_dict.add_dict(
    get_schema("provenance", SCHEMA_FN_PATHS),
    "provenance",
    keys=["comments", "creation_time", "log"],
)
attr_dict.add_dict(get_schema("software", SCHEMA_FN_PATHS), "provenance.software")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "provenance.submitter",
    keys=["author", "email", "organization"],
)
attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
# =============================================================================
class Station(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.id = None
        self.fdsn = Fdsn()
        self.geographic_name = None
        self.datum = None
        self.num_channels = None
        self.channels_recorded = []
        self.run_list = []
        self.channel_layout = None
        self.comments = None
        self.data_type = None
        self.orientation = Orientation()
        self.acquired_by = Person()
        self.provenance = Provenance()
        self.location = Location()
        self.time_period = TimePeriod()
        self.runs = []

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

    def has_run(self, run_id):
        """
        Check to see if the run id already exists
        
        :param run_id: DESCRIPTION
        :type run_id: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if run_id in self.run_list:
            return True
        return False

    def run_index(self, run_id):
        """
        Get the index of the run_id
        
        :param run_id: DESCRIPTION
        :type run_id: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self.has_run(run_id):
            return self.run_list.index(run_id)
        return None

    def add_run(self, run_obj):
        """
        Add a run, if one of the same name exists overwrite it.
        
        :param run_obj: DESCRIPTION
        :type run_obj: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        index = self.run_index(run_obj.id)
        if index is not None:
            self.logger.warning(
                f"Run {run_obj.id} is being overwritten with current information"
            )
            self.runs[index] = run_obj
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
            return self.runs[self.run_index(run_id)]
        self.logger.warning(f"Could not find {run_id} in runs.")
        return None

    @property
    def runs(self):
        """ Return run list """
        return self._runs

    @runs.setter
    def runs(self, value):
        """ set the run list """
        if not hasattr(value, "__iter__"):
            msg = (
                "input station_list must be an iterable, should be a list "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)
        runs = []
        fails = []
        for ii, run in enumerate(value):
            if not isinstance(run, Run):
                msg = f"Item {ii} is not type(Run); type={type(run)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                runs.append(run)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        self._runs = runs

    @property
    def run_list(self):
        """ Return names of run in survey """
        return [ss.id for ss in self.runs]

    @run_list.setter
    def run_list(self, value):
        """ Set list of run names """
        if not hasattr(value, "__iter__"):
            msg = (
                "input station_list must be an iterable, should be a list "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)
        for run in value:
            if not isinstance(run, str):
                try:
                    run = str(run)
                except (ValueError, TypeError):
                    msg = f"could not convert {run} to string"
                    self.logger.error(msg)
                    raise ValueError(msg)

            run = run.replace("'", "").replace('"', "")
            self.runs.append(Run(id=run))
