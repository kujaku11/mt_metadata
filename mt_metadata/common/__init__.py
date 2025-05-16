# # -*- coding: utf-8 -*-
# """
# ======================
# common metadata
# ======================

# This module deals with metadata as defined by the MT metadata standards.
# `metadata documentation
# <https://github.com/kujaku11/MTarchive/blob/tables/docs/mt_metadata_guide.pdf>`_.

# There are multiple containers for each type of metadata, named appropriately.
# These are common metadata containers. They all inherit from MetadataBase.

# Created on Sun Apr 24 20:50:41 2020

# :copyright:
#     Jared Peacock (jpeacock@usgs.gov)

# :license:
#     MIT


# """

# fmt: off

from .citation import Citation
from .comment import Comment
from .copyright import Copyright
from .data_quality import DataQuality
from .declination import Declination

# ### !!! DO NOT CHANGE THE ORDER !!!
from .enumerations import (
    ArrayDTypeEnum,
    ChannelLayoutEnum,
    ChannelOrientationEnum,
    DataTypeEnum,
    FilterTypeEnum,
    GeographicReferenceFrameEnum,
    GeomagneticModelEnum,
    LicenseEnum,
    OrientationMethodEnum,
    SignConventionEnum,
    SymmetryEnum,
)
from .fdsn import Fdsn
from .funding_source import FundingSource
from .geographic_location import GeographicLocation
from .instrument import Instrument
from .location import BasicLocation, BasicLocationNoDatum, Location, StationLocation
from .orientation import Orientation
from .person import AuthorPerson, Person
from .provenance import Provenance
from .range import MinMaxRange, StartEndRange
from .rating import Rating
from .software import Software
from .time_period import TimePeriod, TimePeriodDate


__all__ = [
    "DataTypeEnum",
    "ArrayDTypeEnum",
    "ChannelLayoutEnum",
    "OrientationMethodEnum",
    "GeographicReferenceFrameEnum",
    "ChannelOrientationEnum",
    "GeomagneticModelEnum",
    "FilterTypeEnum",
    "SymmetryEnum",
    "SignConventionEnum",
    "LicenseEnum",
    "Comment",
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
]

# fmt: on
