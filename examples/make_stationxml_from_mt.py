# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 16:31:55 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from copy import deepcopy

from mt_metadata.timeseries.tools import MT2StationXML
from mt_metadata.utils.mttime import get_now_utc, MTime

# =============================================================================

# name space maping
ns_dict = {
    "iris": r"http://www.fdsn.org/xml/station/1/iris",
    "mt": r"http://emiw.org/xmlns/mt/1.0",
    "xsi": r"http://www.w3.org/2001/XMLSchema-instance",
}
# ns_dict = None
# =============================================================================
# Input Parameters
# =============================================================================
# path to the folder where all the xmls are
xml_path = Path(r"c:\Users\jpeacock\OneDrive - DOI\mt\annas_connundrums\mth5_newer")
output_path = Path(r"c:\Users\jpeacock")

# make an instance of MTML2StationXML where the input is the path to the folder
# containing the MTML.xml files
a = MT2StationXML(xml_path)

now = MTime(get_now_utc())
today = f"{now.year}{now.month:02}{now.day:02}"
# if you want to make one stationxml per station then you can loop over
# stations
for station in a.stations[-2:-1]:
    mtex = a.make_experiment(stations=station)

    # name the file as network_year_station_today.xml
    xml_fn = "_".join(
        [
            f"{mtex.surveys[0].fdsn.network}",
            f"{mtex.surveys[0].time_period._start_dt.year}",
            f"{station}",
            f"{today}.xml",
        ]
    )

    # create an inventory object and write stationxml
    inv = a.mt_to_xml(
        mtex,
        stationxml_fn=output_path.joinpath(xml_fn),
        ns_dict=deepcopy(ns_dict),
    )

# if you want to make a complete stationxml
# mtex = a.make_experiment()
# inv = a.mt_to_xml(mtex, stationxml_fn=output_path.joinpath("full_stationxml.xml"))
