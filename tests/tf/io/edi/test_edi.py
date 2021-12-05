# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:42:55 2021

@author: jpeacock
"""
# =============================================================================
#
# =============================================================================
import unittest

from collections import OrderedDict
from mt_metadata.transfer_functions.io.edi.metadata import Header

# =============================================================================


class TestHeader(unittest.TestCase):
    def setUp(self):
        self.header = Header()

    def test_latitude(self):
        self.header.lat = "20:06:00"
        with self.subTest("lat"):
            self.assertEqual(20.1, self.header.lat)
        with self.subTest("latitude"):
            self.assertEqual(20.1, self.header.latitude)

    def test_longitude(self):
        self.header.lon = "20:06:00"
        with self.subTest("lon"):
            self.assertEqual(20.1, self.header.lon)
        with self.subTest("longitude"):
            self.assertEqual(20.1, self.header.longitude)

    def test_elevation(self):
        self.header.elevation = 10.9
        with self.subTest("elev"):
            self.assertEqual(10.9, self.header.elev)
        with self.subTest("elevation"):
            self.assertEqual(10.9, self.header.elevation)

# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
