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

# ### !!! DO NOT CHANGE THE ORDER !!!
from .enumerations import (
    DataTypeEnum,
    ChannelLayoutEnum,
    OrientationMethodEnum,
    GeographicReferenceFrameEnum,
    ChannelOrientationEnum,
    GeomagneticModelEnum,
    FilterTypeEnum,
    SymmetryEnum,
)
from .range import MinMaxRange, StartEndRange
from .comment import Comment
from .declination import Declination
from .geographic_location import GeographicLocation
from .orientation import Orientation
from .instrument import Instrument
from .fdsn import Fdsn
from .rating import Rating
from .data_quality import DataQuality
from .citation import Citation
from .copyright import Copyright
from .person import Person
from .funding_source import FundingSource
from .software import Software
from .time_period import TimePeriod, TimePeriodDate
from .provenance import Provenance
from .location import BasicLocationNoDatum, BasicLocation, Location, StationLocation


__all__ = [
    "DataTypeEnum",
    "ChannelLayoutEnum",
    "OrientationMethodEnum",
    "GeographicReferenceFrameEnum",
    "ChannelOrientationEnum",
    "GeomagneticModelEnum",
    "FilterTypeEnum",
    "SymmetryEnum",
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
