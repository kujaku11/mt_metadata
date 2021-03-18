# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 23:13:19 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import unittest
from collections import OrderedDict

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata.utils import STATIONXML_01, STATIONXML_02
# =============================================================================

class TestInventory01(unittest.TestCase):
    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None
        
        self.experiment = self.translator.xml_to_mt(self.inventory)
        
    def test_num_networks(self):
        self.assertEqual(len(self.inventory.networks), len(self.experiment.surveys))
        
    def test_num_stations(self):
        self.assertEqual(len(self.inventory.networks[0].stations), 
                         len(self.experiment.surveys[0].stations))
        
    def test_num_channels(self):
        self.assertEqual(len(self.inventory.networks[0].stations[0].channels), 
                         len(self.experiment.surveys[0].stations[0].runs[0].channels))
        
class TestInventory02(unittest.TestCase):
    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None
        
        self.experiment = self.translator.xml_to_mt(self.inventory)
        
    def test_num_networks(self):
        self.assertEqual(len(self.inventory.networks), len(self.experiment.surveys))
        
    def test_num_stations(self):
        self.assertEqual(len(self.inventory.networks[0].stations), 
                         len(self.experiment.surveys[0].stations))
        
    # def test_num_channels(self):
    #     self.assertEqual(len(self.inventory.networks[0].stations[0].channels), 
    #                      len(self.experiment.surveys[0].stations[0].runs) * 
    #                      len(self.experiment.surveys[0].stations[0].channels))
        
# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()