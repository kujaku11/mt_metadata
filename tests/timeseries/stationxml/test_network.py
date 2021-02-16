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
from tests import STATIONXML_02 

class TestNetwork(unittest.TestCase):
    """
    Test reading network into MT Survey object
    """
    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.network = self.inventory.networks[0]
        
        self.converter = xml_network_mt_survey.XMLNetworkMTSurvey()
        self.survey = self.converter.network_to_survey(self.network)
        
    def test_comments(self):
        self.assertEqual(self.survey.acquired_by.author, "Pellerin, L.")
        self.assertEqual(self.survey.survey_id, "CONUS South-USGS")
        self.assertEqual(self.survey.project, "USMTArray")
        self.assertEqual(self.survey.geographic_name, "Southern USA")
        self.assertEqual(self.survey.comments, 
                         "Long-period EarthScope-style coverage of southern United States")
        self.assertEqual(self.survey.project_lead.author, "Schultz, A.")
        self.assertEqual(self.survey.project_lead.email, "Adam.Schultz@oregonstate.edu")
        self.assertEqual(self.survey.project_lead.organization, 
                         "Oregon State University")
        
    def test_time_period(self):
        self.assertEqual(self.survey.time_period.start_date, "2020-06-01")
        self.assertEqual(self.survey.time_period.end_date, "2023-12-31")
    
    def test_dataset_doi(self):
        self.assertEqual(self.survey.citation_dataset.doi, 
                         "10.17611/DP/EMTF/USMTARRAY/SOUTH")
        
    def test_journal_doi(self):
        self.assertEqual(self.survey.citation_journal.doi, 
                         "10.666/test.doi")
        
    
      
# =============================================================================
#     Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()   
    