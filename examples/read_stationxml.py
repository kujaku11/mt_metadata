# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:50:30 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from obspy import read_inventory
from obspy.core import inventory
from mt_metadata.timeseries.stationxml import xml_network_mt_survey

# inv_fn = r"c:\Users\jpeacock\Downloads\fdsn-station_2021-02-12T23_28_49.xml"

inv_obj = read_inventory(
    r"c:\Users\jpeacock\Documents\GitHub\mt_metadata\data\StationXML_REW09.xml"
)

nt = xml_network_mt_survey.XMLNetworkMTSurvey()
survey = nt.network_to_survey(inv_obj.networks[0])

network = nt.survey_to_network(survey)

inv = inventory.Inventory()
inv.networks.append(network)
inv.write(r"c:\Users\jpeacock\test_network.xml", "stationxml")
