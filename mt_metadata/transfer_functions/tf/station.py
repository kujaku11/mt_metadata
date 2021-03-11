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
    TransferFunction,
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
attr_dict.add_dict(
    get_schema("transfer_function", SCHEMA_FN_PATHS), "transfer_function"
)
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
        self.transfer_function = TransferFunction()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def run_names(self):
        runs = []
        for rr in self.run_list:
            if isinstance(rr, Run):
                runs.append(rr.id)
            else:
                runs.append(rr)
        return runs
