# -*- coding: utf-8 -*-
"""
==================
EMTF XML metadata
==================

The metadata for transfer functions follows those proposed by Anna Kelbert `EMTF XML: New data interchange format and conversion tools for electromagnetic transfer functions <http://mr.crossref.org/iPage?doi=10.1190%2Fgeo2018-0679.1>`__. 

:copyright:
    Jared Peacock (jpeacock@usgs.gov)
    
:license: 
    MIT


"""

# package file

### !!! DO NOT CHANGE THE ORDER !!!
from .external_url import ExternalUrl
from .primary_data import PrimaryData
from .attachment import Attachment
from .person import Person
from .citation import Citation
from .comment import Comment
from .provenance import Provenance
from .copyright import Copyright
from .data_quality_notes import DataQualityNotes
from .data_quality_warnings import DataQualityWarnings
from .site import Site
from .electrode import Electrode
from .dipole import Dipole
from .field_notes import FieldNotes
from .software import Software
from .processing_info import ProcessingInfo
from .estimate import Estimate
from .statistical_estimates import StatisticalEstimates
from .data_type import DataType
from .data_types import DataTypes
from .magnetic import Magnetic
from .electric import Electric
from .channels import Channels
from .site_layout import SiteLayout


__all__ = [
    "ExternalUrl",
    "PrimaryData",
    "Attachment",
    "Person",
    "Provenance",
    "Citation",
    "Copyright",
    "DataQualityNotes",
    "DataQualityWarnings",
    "Site",
    "Electrode",
    "Dipole",
    "FieldNotes",
    "Software",
    "ProcessingInfo",
    "Estimate",
    "StatisticalEstimates",
    "DataType",
    "DataTypes",
    "Magnetic",
    "Electric",
    "Channels",
    "Layout",
]
