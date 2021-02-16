# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:50:30 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from pathlib import Path
from obspy import read_inventory
from mth5.utils import stationxml_translator

inv_fn = r"c:\Users\jpeacock\Downloads\fdsn-station_2021-02-12T23_28_49.xml"

inv_obj = read_inventory(inv_fn)

survey = stationxml_translator.inventory_network_to_mt_survey(inv_obj.networks[0])
