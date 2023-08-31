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
from collections import OrderedDict
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import (
    Person,
    Citation,
    Location,
    TimePeriod,
    Fdsn,
    Station,
    FundingSource,
)
from .filters import (
    PoleZeroFilter,
    CoefficientFilter,
    TimeDelayFilter,
    FIRFilter,
    FrequencyResponseTableFilter,
)
from mt_metadata.utils.list_dict import ListDict

# =============================================================================
attr_dict = get_schema("survey", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "acquired_by",
    keys=["author", "comments", "organization"],
)
attr_dict.add_dict(
    get_schema("funding_source", SCHEMA_FN_PATHS),
    "funding_source",
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
    get_schema("geographic_location", SCHEMA_FN_PATHS),
    None,
    keys=["country", "state"],
)
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS),
    "project_lead",
    keys=["author", "email", "organization"],
)
attr_dict["project_lead.email"]["required"] = True
attr_dict["project_lead.organization"]["required"] = True

attr_dict.add_dict(get_schema("copyright", SCHEMA_FN_PATHS), None)
# =============================================================================
class Survey(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.acquired_by = Person()
        self.fdsn = Fdsn()
        self.citation_dataset = Citation()
        self.citation_journal = Citation()
        self.northwest_corner = Location()
        self.project_lead = Person()
        self.funding_source = FundingSource()
        self.southeast_corner = Location()
        self.time_period = TimePeriod()
        self.stations = ListDict()
        self.filters = {}

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
        """Return station list"""
        return self._stations

    @stations.setter
    def stations(self, value):
        """set the station list"""
        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input station_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

        fails = []
        self._stations = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, station in enumerate(value_list):

            if isinstance(station, (dict, OrderedDict)):
                s = Station()
                s.from_dict(station)
                self._stations.append(s)
            elif not isinstance(station, Station):
                msg = f"Item {ii} is not type(Station); type={type(station)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                self._stations.append(station)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

    @property
    def station_names(self):
        """Return names of station in survey"""
        return self.stations.keys()

    @property
    def filters(self):
        """A dictionary of available filters"""
        return self._filters

    @filters.setter
    def filters(self, value):
        """
        Set the filters dictionary

        :param value: dictionary of filter objects
        :type value: dictionary

        """

        filters = ListDict()
        fails = []
        if value is None:
            return

        if isinstance(value, list):
            if len(value) > 0:
                if isinstance(value[0], (dict, OrderedDict, ListDict)):
                    for ff in value:
                        f_type = ff["type"]
                        if f_type is None:
                            msg = "filter type is None do not know how to read the filter"
                            fails.append(msg)
                            self.logger.error(msg)
                        if f_type.lower() in ["zpk"]:
                            f = PoleZeroFilter()
                        elif f_type.lower() in ["coefficient"]:
                            f = CoefficientFilter()
                        elif f_type.lower() in ["time delay"]:
                            f = TimeDelayFilter()
                        elif f_type.lower() in ["fir"]:
                            f = FIRFilter()
                        elif f_type.lower() in ["frequency response table"]:
                            f = FrequencyResponseTableFilter()
                        else:
                            msg = f"filter type {f_type} not supported."
                            fails.append(msg)
                            self.logger.error(msg)

                        f.from_dict(ff)
                        filters[f.name] = f

        elif not isinstance(value, (dict, OrderedDict, ListDict)):
            msg = (
                "Filters must be a dictionary with keys = names of filters, "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)
        else:

            for k, v in value.items():
                if not isinstance(
                    v,
                    (
                        PoleZeroFilter,
                        CoefficientFilter,
                        TimeDelayFilter,
                        FrequencyResponseTableFilter,
                        FIRFilter,
                    ),
                ):
                    msg = f"Item {k} is not Filter type; type={type(v)}"
                    fails.append(msg)
                    self.logger.error(msg)
                else:
                    filters[k.lower()] = v
        if len(fails) > 0:
            raise TypeError("\n".join(fails))

        self._filters = filters

    @property
    def filter_names(self):
        """return a list of filter names"""
        return list(self.filters.keys())

    def has_station(self, station_id):
        """
        Has station id

        :param station_id: station id verbatim
        :type station_id: string
        :return: True if exists or False if not
        :rtype: boolean

        """
        if station_id in self.station_names:
            return True
        return False

    def station_index(self, station_id):
        """
        Get station index

        :param station_id: station id verbatim
        :type station_id: string
        :return: index value if station is found
        :rtype: integer

        """

        if self.has_station(station_id):
            return self.station_names.index(station_id)
        return None

    def add_station(self, station_obj):
        """
        Add a station, if has the same name update that object.

        :param station_obj: station object to add
        :type station_obj: `:class:`mt_metadata.timeseries.Station`

        """

        if not isinstance(station_obj, Station):
            raise TypeError(
                f"Input must be a mt_metadata.timeseries.Station object not {type(station_obj)}"
            )

        if self.has_station(station_obj.id):
            self.stations[station_obj.id].update(station_obj)
            self.logger.warning(
                f"Station {station_obj.id} already exists, updating metadata"
            )
        else:
            self.stations.append(station_obj)

    def get_station(self, station_id):
        """
        Get a station from the station id

        :param station_id: station id verbatim
        :type station_id: string
        :return: station object
        :rtype: :class:`mt_metadata.timeseries.Station`

        """

        if self.has_station(station_id):
            return self.stations[station_id]
        else:
            self.logger.warning(f"Could not find station {station_id}")
            return None

    def remove_station(self, station_id):
        """
        remove a station from the survey

        :param station_id: station id verbatim
        :type station_id: string

        """

        if self.has_station(station_id):
            self.stations.remove(station_id)
        else:
            self.logger.warning(f"Could not find {station_id} to remove.")

    def update_bounding_box(self):
        """
        Update the bounding box of the survey from the station information

        """
        lat = []
        lon = []
        for station in self.stations:
            lat.append(station.location.latitude)
            lon.append(station.location.longitude)

        self.southeast_corner.latitude = min(lat)
        self.southeast_corner.longitude = max(lon)
        self.northwest_corner.latitude = max(lat)
        self.northwest_corner.longitude = min(lon)

    def update_time_period(self):
        """
        Update the start and end time of the survey based on the stations
        """
        start = []
        end = []
        for station in self.stations:
            if station.time_period.start != "1980-01-01T00:00:00+00:00":
                start.append(station.time_period.start)
            if station.time_period.end != "1980-01-01T00:00:00+00:00":
                end.append(station.time_period.end)

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
