# -*- coding: utf-8 -*-
"""
==================
metadata
==================

This module deals with metadata as defined by the MT metadata standards.
`metadata documentation 
<https://github.com/kujaku11/MTarchive/blob/tables/docs/mt_metadata_guide.pdf>`_.

There are multiple containers for each type of metadata, named appropriately.

Each container will be able to read and write:
    * dictionary
    * json
    * xml
    * csv?
    * pandas.Series
    * anything else?

Because a lot of the name words in the metadata are split by '.' there are some
issues we need to deal with.  I wrote in get and set attribute functions
to handle these types of names so the user shouldn't have to work about
splitting the names themselves.

These containers will be the building blocks for the metadata and how they are
interchanged between the HDF5 file and the user.  A lot of the metadata you
can get directly from the raw time series files, but the user will need to
input a decent amount on their own.  Dictionaries are the most fundamental
type we should be dealing with.

Each container has an attribute called _attr_dict which dictates if the
attribute is included in output objects, the data type, whether it is a
required parameter, and the style of output.  This should help down the road
with validation and keeping the data types consistent.  And if things change
you should only have to changes these dictionaries.

self._attr_dict = {'nameword':{'type': str, 'required': True, 'style': 'name'}}

Created on Sun Apr 24 20:50:41 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)
    
:license: 
    MIT


"""

# package file

### !!! DO NOT CHANGE THE ORDER !!!
from mt_metadata.timeseries.declination import Declination
from mt_metadata.timeseries.location import Location
from mt_metadata.timeseries.instrument import Instrument
from mt_metadata.timeseries.fdsn import Fdsn
from mt_metadata.timeseries.rating import Rating
from mt_metadata.timeseries.data_quality import DataQuality
from mt_metadata.timeseries.citation import Citation
from .comment import Comment
from mt_metadata.timeseries.copyright import Copyright
from mt_metadata.timeseries.person import Person
from mt_metadata.timeseries.software import Software
from mt_metadata.timeseries.provenance import Provenance
from mt_metadata.timeseries.diagnostic import Diagnostic
from mt_metadata.timeseries.battery import Battery
from mt_metadata.timeseries.electrode import Electrode
from mt_metadata.timeseries.timing_system import TimingSystem
from mt_metadata.timeseries.time_period import TimePeriod
from mt_metadata.timeseries.orientation import Orientation
from mt_metadata.timeseries.filters.filtered import Filtered
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.data_logger import DataLogger
from .transfer_function import TransferFunction
from mt_metadata.timeseries.survey import Survey
from mt_metadata.timeseries.channel import Channel
from mt_metadata.timeseries.auxiliary import Auxiliary
from mt_metadata.timeseries.electric import Electric
from mt_metadata.timeseries.magnetic import Magnetic
from .statistical_estimate import StatisticalEstimate
from mt_metadata.timeseries.run import Run
from mt_metadata.timeseries.station import Station


__all__ = [
    "Standards",
    "Declination",
    "Location",
    "Instrument",
    "Fdsn",
    "Rating",
    "DataQuality",
    "Citation",
    "Comment",
    "Copyright",
    "Provenance",
    "Person",
    "Diagnostic",
    "Battery",
    "Electrode",
    "TimingSystem",
    "TimePeriod",
    "Orientation",
    "Software",
    "Filtered",
    "FilterBase",
    "DataLogger",
    "TransferFunction",
    "Survey",
    "Station",
    "Run",
    "Channel",
    "Auxiliary",
    "Electric",
    "Magnetic",
    "StatisticalEstimate",
]
