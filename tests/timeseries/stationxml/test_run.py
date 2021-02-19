# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:36:41 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLEquipmentMTRun
from tests import STATIONXML_02


class TestNetwork01(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.xml_equipment = self.inventory.networks[0].stations[0].equipments[0]

        self.converter = XMLEquipmentMTRun()
        self.mt_run = self.converter.xml_to_mt(self.xml_equipment)
        
    def test_id(self):
        self.assertEqual(self.mt_run.id, "a")
        
# =============================================================================
# 
# =============================================================================
if __name__ == "__main__":
    unittest.main()
    