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

# =============================================================================
attr_dict = get_schema(name, SCHEMA_FN_PATHS)
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


# =============================================================================
# Station Class
# =============================================================================
