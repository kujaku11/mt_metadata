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
from . import Person, Citation, Location, TimePeriod, Fdsn, Station

# =============================================================================
attr_dict = get_schema("survey", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS), "acquired_by", keys=["author", "comments"]
)
attr_dict.add_dict(get_schema("citation", SCHEMA_FN_PATHS), "citation_dataset")
attr_dict.add_dict(get_schema("citation", SCHEMA_FN_PATHS), "citation_journal")
attr_dict.add_dict(
    get_schema("location", SCHEMA_FN_PATHS),
    "northwest_corner",
    keys=["latitude", "longitude"],
)
attr_dict.add_dict(
    get_schema("location", SCHEMA_FN_PATHS),
    "southeast_corner",
    keys=["latitude", "longitude"],
)
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "project_lead",
    keys=["author", "email", "organization"],
)
attr_dict.add_dict(get_schema("copyright", SCHEMA_FN_PATHS), None)
# =============================================================================
class Survey(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.acquired_by = Person()
        self.fdsn = Fdsn()
        self.citation_dataset = Citation()
        self.citation_journal = Citation()
        self.comments = None
        self.country = None
        self.datum = None
        self.geographic_name = None
        self.name = None
        self.northwest_corner = Location()
        self.project = None
        self.project_lead = Person()
        self.release_license = "CC-0"
        self.southeast_corner = Location()
        self.summary = None
        self.survey_id = None
        self.time_period = TimePeriod()
        self.stations = []

        super().__init__(attr_dict=attr_dict, **kwargs)

    def __add__(self, other):
        if isinstance(other, Survey):
            self.stations.extend(other.stations)

            return self
        else:
            msg = f"Can only merge Survey objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)

    def __len__(self):
        return len(self.stations)

    @property
    def stations(self):
        """ Return station list """
        return self._stations

    @stations.setter
    def stations(self, value):
        """ set the station list """
        if not hasattr(value, "__iter__"):
            msg = (
                "input survey_list must be an iterable, should be a list "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)
        stations = []
        fails = []
        for ii, station in enumerate(value):
            if not isinstance(station, Station):
                msg = f"Item {ii} is not type(Station); type={type(station)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                stations.append(station)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        self._stations = stations

    @property
    def station_names(self):
        """ Return names of station in survey """
        return [ss.id for ss in self.stations]
