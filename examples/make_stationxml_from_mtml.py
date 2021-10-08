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
class MTML2StationXML(XMLInventoryMTExperiment):
    """
    A class to convert multiple MTML xml files into a stationXML
    
    """
    
    def __init__(self, xml_path=None):
        self.xml_path = xml_path
        
        
    @property
    def xml_path(self):
        return self._xml_path
    
    @xml_path.setter
    def xml_path(self, value):
        if value is None:
            self._xml_path = None
        else:
            self._xml_path = Path(value)
            
    def has_xml_path(self):
        if self.xml_path is not None and self.xml_path.exists():
            return True
        return False

    @staticmethod
    def is_a_station_xml(fn):
        return fn.count(".") == 1
    
    @staticmethod
    def is_a_run_xml(fn):
        return fn.count(".") == 2
    
    @staticmethod
    def is_a_channel_xml(fn):
        return fn.count(".") > 2
    
    def get_station_files(self, station: str) -> list:
        """
        Get all mtml xml files for a given station.
        """
        return list(self.xml_path.glob(f"{station}*"))




fn_list = get_station_files(xml_path, "CAR02")

    
    
    