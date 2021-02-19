# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:50:30 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from obspy import read_inventory
from obspy.core import inventory
from mt_metadata.timeseries.stationxml import XMLNetworkMTSurvey, XMLStationMTStation
# inv_fn = r"c:\Users\jpeacock\Downloads\fdsn-station_2021-02-12T23_28_49.xml"

inv_obj = read_inventory(r"c:\Users\jpeacock\Documents\GitHub\mt_metadata\data\StationXML_REW09.xml")
inv_test = inventory.Inventory()

# read network
nt = XMLNetworkMTSurvey()
survey = nt.xml_to_mt(inv_obj.networks[0])
network = nt.mt_to_xml(survey)
inv_test.networks.append(network)

# read station
st = XMLStationMTStation()
mt_station, run_comments = st.xml_to_mt(inv_obj.networks[0].stations[0])
# inv_test.networks[0].stations.append(st.mt_to_xml)


# check to see if a stationxml can be written
inv_test.write(r"c:\Users\jpeacock\test_network.xml", "stationxml")

# check the written stationxml can be read
inv2 = read_inventory(r"c:\Users\jpeacock\test_network.xml")
