# -*- coding: utf-8 -*-
"""
======================
time series metadata
======================

:mod:`mt_metadata.timeseries` is a package that contains classes for
describing time series metadata.

MetadataBase Objects
--------------------
* Diagnostic - Diagnostic information for data quality and instrument performance
* Battery - Battery voltage and power supply metadata
* Electrode - Electrode specifications and contact information
* TimingSystem - GPS and timing system metadata (synchronization, accuracy)
* AppliedFilter - Filters applied to time series data during acquisition or processing
* FilterBase - Base class for all filter types (analog, digital, frequency response)
* DataLogger - Data logger/acquisition system specifications and settings
* Channel - Base channel metadata common to all channel types
* ChannelBase - Fundamental channel properties and attributes
* Auxiliary - Auxiliary channel metadata (e.g., temperature, humidity, tilt)
* Electric - Electric field channel metadata (dipole length, orientation, electrode info)
* Magnetic - Magnetic field channel metadata (sensor type, calibration)
* Run - Time series run metadata (collection of channels recorded together)
* Station - Station-level metadata (location, orientation, equipment)
* Survey - Survey-level metadata (project information, participants, objectives)
* Experiment - Top-level experiment metadata encompassing multiple surveys

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
from .filtered import AppliedFilter
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
