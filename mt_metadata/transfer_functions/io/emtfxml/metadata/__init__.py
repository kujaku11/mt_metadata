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

from .attachment import Attachment
from .channels import Channels
from .citation import Citation
from .comment import Comment
from .copyright import Copyright
from .data import TransferFunction
from .data_quality_notes import DataQualityNotes
from .data_quality_warnings import DataQualityWarnings
from .data_type import DataType
from .data_types import DataTypes
from .dipole import Dipole
from .electric import Electric
from .electrode import Electrode
from .emtf import EMTF
from .estimate import Estimate

### !!! DO NOT CHANGE THE ORDER !!!
from .external_url import ExternalUrl
from .field_notes import FieldNotes
from .instrument import Instrument
from .location import Location
from .magnetic import Magnetic
from .magnetometer import Magnetometer
from .orientation import Orientation
from .period_range import PeriodRange
from .person import Person
from .primary_data import PrimaryData
from .processing_info import ProcessingInfo
from .provenance import Provenance
from .remote_info import RemoteInfo
from .remote_ref import RemoteRef
from .run import Run
from .site import Site
from .site_layout import SiteLayout
from .software import ProcessingSoftware
from .statistical_estimates import StatisticalEstimates


__all__ = [
    "ExternalUrl",
    "PrimaryData",
    "Attachment",
    "Person",
    "Provenance",
    "Citation",
    "Copyright",
    "Comment",
    "DataQualityNotes",
    "DataQualityWarnings",
    "Orientation",
    "Location",
    "Site",
    "Electrode",
    "Dipole",
    "Magnetometer",
    "Instrument",
    "Run",
    "FieldNotes",
    "ProcessingSoftware",
    "RemoteRef",
    "RemoteInfo",
    "ProcessingInfo",
    "Estimate",
    "StatisticalEstimates",
    "DataType",
    "DataTypes",
    "Magnetic",
    "Electric",
    "Channels",
    "SiteLayout",
    "PeriodRange",
    "TransferFunction",
    "EMTF",
]
