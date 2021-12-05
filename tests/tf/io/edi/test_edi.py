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
from mt_metadata.transfer_functions.io.edi.metadata import (
    Header, EMeasurement, HMeasurement)


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
            
class TestEMeasurement(unittest.TestCase):
    def setUp(self):
        self.e_dict = {'id': '14.001', 'chtype': 'EX', 'x': -50., 
                       'y': 0., 'x2': 50., 'y2': 0.}
        
        self.ex = EMeasurement(**self.e_dict)
        
    def test_attr(self):
        for k, v in self.e_dict.items():
            self.assertEqual(v, getattr(self.ex, k))
            
class TestHMeasurement(unittest.TestCase):
    def setUp(self):
        self.h_dict = {'id': '12.001', 'chtype': 'HY', 'x': 0., 
                       'y': 0., 'azm': 90}
        
        self.hy = HMeasurement(**self.h_dict)
        
    def test_attr(self):
        for k, v in self.h_dict.items():
            self.assertEqual(v, getattr(self.hy, k))
            
        
    

# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
