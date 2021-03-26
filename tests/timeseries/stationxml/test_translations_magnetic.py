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
        self.original_xml = inventory.read_inventory(STATIONXML_MAGNETIC)
        self.new_xml = self.translator.mt_to_xml(self.mtml)
        
    def 
        
        