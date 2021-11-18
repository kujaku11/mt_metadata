# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 16:31:55 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from mt_metadata.timeseries.tools import MT2StationXML
# =============================================================================

# name space maping
ns_dict = {
    "iris": r"http://www.fdsn.org/xml/station/1/iris",
    "mt": r"http://emiw.org/xmlns/mt/1.0",
    "xsi": r"http://www.w3.org/2001/XMLSchema-instance",
    }
# =============================================================================
# Input Parameters
# =============================================================================
# path to the folder where all the xmls are
xml_path = Path(r"c:\Users\jpeacock\OneDrive - DOI\mt\annas_connundrums\CAS04")
output_path = Path(r"c:\Users\jpeacock")

# make an instance of MTML2StationXML where the input is the path to the folder
# containing the MTML.xml files
a = MT2StationXML(xml_path)

# if you want to make one stationxml per station then you can loop over
# stations
for station in a.stations[0:1]:
    mtex = a.make_experiment(stations=station)
    inv = a.mt_to_xml(
        mtex, 
        stationxml_fn=output_path.joinpath(f"{station}_stationxml.xml"),
        ns_dict=ns_dict,
    )

# if you want to make a complete stationxml
# mtex = a.make_experiment()
# inv = a.mt_to_xml(mtex, stationxml_fn=output_path.joinpath("full_stationxml.xml"))
