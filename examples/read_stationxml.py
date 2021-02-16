# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:50:30 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from pathlib import Path
from obspy import read_inventory
from mt_metadata.timeseries.stationxml import xml_network_mt_survey

# inv_fn = r"c:\Users\jpeacock\Downloads\fdsn-station_2021-02-12T23_28_49.xml"
inv_fn = r"c:\Users\jpeacock\Documents\GitHub\mth5_test_data\mth5_test_data\stationxml\StationXML_REW09.xml"

inv_obj = read_inventory(inv_fn)

nt = xml_network_mt_survey.XMLNetworkMTSurvey()
survey = nt.network_to_survey(inv_obj.networks[0])
