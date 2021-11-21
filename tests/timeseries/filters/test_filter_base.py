# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 18:45:48 2021

@author: jpeacock
"""

import unittest
from mt_metadata.timeseries.filters.filter_base import FilterBase

class TestFilterBase(unittest.TestCase):
    """
    Test the filter base class to make sure it does what it should
    """
    
    def setUp(self):
        self.fb = FilterBase()
        
    def test_units_in(self):
        
        with self.subTest(msg="Input short name"):
            self.fb.units_in = "V"
            self.assertEqual("V", self.fb.units_in)
        
        with self.subTest(msg="Input long name"):
            self.fb.units_in = "volts"
            self.assertEqual("V", self.fb.units_in)
            
    def test_units_out(self):
        with self.subTest(msg="Input short name"):
            self.fb.units_out = "V"
            self.assertEqual("V", self.fb.units_out)
        
        with self.subTest(msg="Input long name"):
            self.fb.units_out = "volts"
            self.assertEqual("V", self.fb.units_out)
            
    def test_calibration_date(self):
        self.fb.calibration_date = "2020-01-01T00:00:00"
        self.assertEqual("2020-01-01", self.fb.calibration_date)
        
    def test_name(self):
        with self.subTest(msg="test name with slash"):
            self.fb.name = "v/m"
            self.assertEqual("v per m", self.fb.name)
        
        with self.subTest(msg="normal name"):
            self.fb.name = "normal"
            self.assertEqual("normal", self.fb.name)
            
    def test_gain(self):
        with self.subTest(msg="test string input"):
            self.fb.gain = "1"
            self.assertEqual(1, self.fb.gain)
            
        with self.subTest(msg="test initial value"):
            self.assertEqual(1, self.fb.gain)
            
        
            
        
        