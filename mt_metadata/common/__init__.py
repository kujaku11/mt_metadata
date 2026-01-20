# -*- coding: utf-8 -*-
"""
======================
common metadata
======================

There are multiple containers for each type of metadata, named appropriately.
These are common metadata containers. They all inherit from MetadataBase.

MetadataBase Objects
--------------------
* MTime - Time representation with validation
* Comment - Structured comment metadata
* ListDict - Dictionary of lists for multi-valued attributes
* MinMaxRange - Numeric range with min/max values
* StartEndRange - Time or value range with start/end
* Declination - Magnetic declination information
* GeographicLocation - Geographic coordinates and location data
* Orientation - Sensor orientation parameters
* Instrument - Instrument specifications and metadata
* Fdsn - FDSN (International Federation of Digital Seismograph Networks) metadata
* Rating - Data quality rating information
* DataQuality - Comprehensive data quality metrics
* Citation - Publication and citation information
* Copyright - Copyright and licensing details
* Person - Person contact information
* AuthorPerson - Author-specific metadata
* FundingSource - Funding agency and grant information
* Software - Software and processing tool metadata
* TimePeriod - Time period with start/end times
* TimePeriodDate - Time period using dates
* Provenance - Data provenance and processing history
* BasicLocation - Basic location without datum
* BasicLocationNoDatum - Minimal location information
* Location - Full location with datum and projection
* StationLocation - Station-specific location metadata
* Band - Frequency band definition

Created on Sun Apr 24 20:50:41 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license:
    MIT


"""
# isort:skip_file
# fmt: off

# ### !!! DO NOT CHANGE THE ORDER !!!
from .enumerations import (
    ChannelLayoutEnum,
    ChannelOrientationEnum,
    DataTypeEnum,
    ArrayDTypeEnum,
    FilterTypeEnum,
    GeographicReferenceFrameEnum,
    GeomagneticModelEnum,
    StdEDIversionsEnum,
    LicenseEnum,
    OrientationMethodEnum,
    SignConventionEnum,
    SymmetryEnum,
)
from .mttime import MTime
from .comment import Comment
from .list_dict import ListDict
from .range import MinMaxRange, StartEndRange
from .declination import Declination
from .geographic_location import GeographicLocation
from .orientation import Orientation
from .instrument import Instrument
from .fdsn import Fdsn
from .rating import Rating
from .data_quality import DataQuality
from .citation import Citation
from .copyright import Copyright
from .person import AuthorPerson, Person
from .funding_source import FundingSource
from .software import Software
from .time_period import TimePeriod, TimePeriodDate
from .provenance import Provenance
from .location import BasicLocation, BasicLocationNoDatum, Location, StationLocation
from .band import Band, CenterAveragingTypeEnum, ClosedEnum

__all__ = [
    "DataTypeEnum",
    "ArrayDTypeEnum",
    "ChannelLayoutEnum",
    "OrientationMethodEnum",
    "GeographicReferenceFrameEnum",
    "ChannelOrientationEnum",
    "StdEDIversionsEnum",
    "GeomagneticModelEnum",
    "FilterTypeEnum",
    "SymmetryEnum",
    "SignConventionEnum",
    "LicenseEnum",
    "MTime",
    "Comment",
    "ListDict",
    "MinMaxRange",
    "StartEndRange",
    "Declination",
    "GeographicLocation",
    "Orientation",
    "Instrument",
    "Fdsn",
    "Rating",
    "DataQuality",
    "Citation",
    "Copyright",
    "Person",
    "AuthorPerson",
    "FundingSource",
    "Software",
    "TimePeriod",
    "TimePeriodDate",
    "Provenance",
    "BasicLocationNoDatum",
    "BasicLocation",
    "Location",
    "StationLocation",
    "Band",
    "CenterAveragingTypeEnum",
    "ClosedEnum",
]

# fmt: on
