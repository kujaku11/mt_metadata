# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 13:05:54 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

from mth5 import mth5
from mt_metadata.timeseries import stationxml
from mt_metadata.utils import STATIONXML_01

translator = stationxml.XMLInventoryMTExperiment()
experiment = translator.xml_to_mt(stationxml_fn=STATIONXML_01)

m = mth5.MTH5()
m.open_mth5(r"c:\Users\jpeacock\from_stationxml.h5")

for station in experiment.surveys[0].stations:
    mt_station = m.add_station(station.id, station_metadata=station)
    for run in station.runs:
        mt_run = mt_station.add_run(run.id, run_metadata=run)
        for channel in run.channels:
            mt_channel = mt_run.add_channel(
                channel.component, channel.type, None, channel_metadata=channel)
m.close_mth5()
