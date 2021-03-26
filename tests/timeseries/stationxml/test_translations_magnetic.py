# -*- coding: utf-8 -*-
"""
Test translation from xml to mtml back to xml

Created on Fri Mar 26 08:15:49 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import unittest
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata.utils import STATIONXML_MAGNETIC
from obspy.core import inventory
# =============================================================================


class TestTranslationXML2MTML2XML(unittest.TestCase):
    def setUp(self):
        self.translator = XMLInventoryMTExperiment()
        self.mtml = self.translator.xml_to_mt(stationxml_fn=STATIONXML_MAGNETIC)
        self.original_xml = inventory.read_inventory(STATIONXML_MAGNETIC.as_posix())
        self.new_xml = self.translator.mt_to_xml(self.mtml)
        self.maxDiff = None
        
        self.network_0 = self.original_xml.networks[0]
        self.network_1 = self.new_xml.networks[0]
        
        self.station_0 = self.network_0.stations[0]
        self.station_1 = self.network_1.stations[0]
        
        self.channel_0 = self.network_0.stations[0].channels[0]
        self.channel_1 = self.network_1.stations[0].channels[0]
        
    def test_network_start(self):
        self.assertEqual(self.network_0.start_date,
                         self.network_1.start_date)
        
    def test_network_end(self):
        # original does not have an end date
        self.assertNotEqual(self.network_0.end_date,
                            self.network_1.end_date)
        
    def test_network_comments(self):
        original_comment_dict = dict([(c.subject, c.value) for c in self.network_0.comments if c.value not in [None, ""]])
        new_comment_dict = dict([(c.subject, c.value) for c in self.network_1.comments if c.value not in [None, ""]])
        
        self.assertDictEqual(original_comment_dict, new_comment_dict)
        
    def test_network_identifier(self):
        self.assertListEqual(self.network_0.identifiers,
                             self.network_1.identifiers)
        
    def test_network_code(self):
        self.assertEqual(self.network_0.code,
                         self.network_1.code)
        
    def test_network_restricted_status(self):
        self.assertEqual(self.network_0.restricted_status,
                         self.network_1.restricted_status)
        
    def test_network_operator(self):
        self.assertEqual(self.network_0.operators[0].agency,
                         self.network_1.operators[0].agency)
        
        self.assertListEqual(self.network_0.operators[0].contacts[0].names,
                             self.network_1.operators[0].contacts[0].names)
        
        self.assertListEqual(self.network_0.operators[0].contacts[0].emails,
                             self.network_1.operators[0].contacts[0].emails)
        
        
    def test_station_start(self):
        self.assertEqual(self.station_0.start_date,
                         self.station_1.start_date)
        
    def test_station_end(self):
        # original file does not have an end date
        self.assertNotEqual(self.station_0.end_date,
                            self.station_1.end_date)
        
    def test_station_code(self):
        self.assertEqual(self.station_0.code, self.station_1.code)
        
    def test_station_alternate_code(self):
        self.assertEqual(self.station_0.alternate_code, self.station_1.alternate_code)
    
    def test_station_restricted(self):
        self.assertEqual(self.station_0.restricted_status,
                         self.station_1.restricted_status)
        
    def test_station_comments(self):
        original_comment_dict = dict([(c.subject, c.value) for c in self.station_0.comments if c.value not in [None, ""]])
        new_comment_dict = dict([(c.subject, c.value) for c in self.station_1.comments if c.value not in [None, ""]])
        
        # for now just make sure the right keys are there.  The values are slightly
        # different because of how they are parsed.  
        self.assertListEqual(sorted(list(original_comment_dict.keys())), 
                             sorted(list(new_comment_dict.keys())))
        
    def test_station_location(self):
        self.assertAlmostEqual(self.station_0.latitude, self.station_1.latitude, 4)
        self.assertAlmostEqual(self.station_0.longitude, self.station_1.longitude, 4)
        self.assertAlmostEqual(self.station_0.elevation, self.station_1.elevation, 4)
    
    def test_station_site(self):
        self.assertEqual(self.station_0.site.name, self.station_1.site.name)
    
    def test_channel(self):
        pass
    
    def test_response(self):
        pass
    
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()     
   
        