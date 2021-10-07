# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 16:31:55 2021

@author: jpeacock
"""

# =============================================================================
# Imports 
# =============================================================================
from pathlib import Path
from xml.etree import cElementTree as et

from mt_metadata.timeseries import (Experiment, Survey, Station, Run, 
                                    Electric, Magnetic)
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment

# =============================================================================
# Input Parameters
# =============================================================================
xml_path = Path(r"c:\Users\jpeacock\OneDrive - DOI\mt\mt_array_xmls")

output_filename = "example_station_xml"

# =============================================================================
# Useful functions
# =============================================================================
def get_station(station: str) -> list:
    """
    Get all mtml xml files for a given station.
    """
    pass