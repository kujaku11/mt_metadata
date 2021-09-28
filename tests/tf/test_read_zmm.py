# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 16:28:09 2021

@author: jpeacock
"""

import unittest
import xarray as xr
import numpy as np

from mt_metadata.transfer_functions.core import TF, TFError
from mt_metadata.transfer_functions.io import zmm
from mt_metadata import TF_ZMM

class TestTranslateZmm(unittest.TestCase):
    def setUp(self):
        self.tf_obj = TF(TF_ZMM)
        self.zmm_obj = zmm.ZMM(TF_ZMM) 
    
    def test_latitude(self):
        self.assertEqual(self.tf_obj.latitude, self.zmm_obj.latitude)
        
    def test_longitude(self):
        self.assertEqual(self.tf_obj.longitude, self.zmm_obj.longitude)
        
    def test_station(self):
        self.assertEqual(self.tf_obj.station, self.zmm_obj.station)
        
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()        