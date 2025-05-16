# -*- coding: utf-8 -*-
"""
======================
time series metadata
======================

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

### !!! DO NOT CHANGE THE ORDER !!!

from .diagnostic import Diagnostic
from .battery import Battery
from .electrode import Electrode
from .timing_system import TimingSystem
from .filtered import Filter, AppliedFilter
from .filters.filter_base import FilterBase
from .data_logger import DataLogger
from .channel import Channel, ChannelBase
from .auxiliary import Auxiliary
from .electric import Electric
from .magnetic import Magnetic
from .run import Run
from .station import Station
from .survey import Survey
from .experiment import Experiment


__all__ = [
    "Diagnostic",
    "Battery",
    "Electrode",
    "TimingSystem",
    "Filter",
    "AppliedFilter",
    "FilterBase",
    "DataLogger",
    "Survey",
    "Station",
    "Run",
    "Channel",
    "ChannelBase",
    "Auxiliary",
    "Electric",
    "Magnetic",
    "Experiment",
]
