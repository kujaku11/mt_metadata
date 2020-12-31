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
from . import Person, Citation, Location, TimePeriod, Fdsn

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

        super().__init__(attr_dict=attr_dict, **kwargs)
