# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:58:11 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import xml_network_mt_survey
from tests import STATIONXML_01, STATIONXML_02 

class TestNetwork(unittest.TestCase):
    """
    Test reading network into MT Survey object
    """
    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02)
        self.network = self.inventory.networks[0]
        
        self.converter = xml_network_mt_survey.XMLNetworkMTSurvey()
        self.survey = self.converter.network_to_survey(self.network)
        
    def test_acquired_by(self):
        self.assertEqual(self.survey.acquired_by.author, "Pellerin, L.")
      
# =============================================================================
#     Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()   
    