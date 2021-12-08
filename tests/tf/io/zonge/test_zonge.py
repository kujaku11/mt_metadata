# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 11:29:57 2021

:author: Jared Peacock

:license: MIT

"""
# =============================================================================
# 
# =============================================================================
import unittest

from mt_metadata import TF_AVG
from mt_metadata.transfer_functions.io.zonge.metadata import Header

class TestAVGHeader(unittest.TestCase):
    
    def setUp(self):
        
        self.header = Header()
        with open(TF_AVG, "r") as fid:
            self.lines = fid.readlines()
            
        self.header.read_header(self.lines)
            
        
    def test_survey(self):
        with self.subTest("survey type"):
            self.assertEqual(self.header.survey.type, "nsamt")
            
        with self.subTest("survey array"):
            self.assertEqual(self.header.survey.array, "tensor")
            
    def test_tx(self):
        self.assertEqual(self.header.tx.type, "natural")
        
    def test_mt_edit(self):
        with self.subTest("auto phase flip"):
            self.assertEqual(self.header.m_t_edit.auto.phase_flip, "yes")
            
        with self.subTest("dplus use"):
            self.assertEqual(self.header.m_t_edit.d_plus.use, "no")
        
        with self.subTest("phase slope smooth"):
            self.assertEqual(self.header.m_t_edit.phase_slope.smooth, "robust")
            
        with self.subTest("phase slope to_z_mag"):
            self.assertEqual(self.header.m_t_edit.phase_slope.to_z_mag, "no")
            
        with self.subTest("version"):
            self.assertEqual(self.header.m_t_edit.version, "3.10m applied 2021/01/27")
        
    def test_rx(self):
        with self.subTest("gdp_stn"):
            self.assertEqual(self.header.rx.gdp_stn, "24")
            
        with self.subTest("h_p_r"):
            self.assertListEqual(self.header.rx.h_p_r, [0., 0., 180.])
            
        with self.subTest("length"):
            self.assertEqual(self.header.rx.length, 100.)
            
        with self.subTest("station"):
            self.assertEqual(self.header.station, "24")
            
    def test_gps(self):
        with self.subTest("lat"):
            self.assertAlmostEqual(self.header.g_p_s.lat, 32.83331167, 5)
            
        with self.subTest("lon"):
            self.assertAlmostEqual(self.header.g_p_s.lon, -107.08305667, 5)
            
        with self.subTest("latitude"):
            self.assertAlmostEqual(self.header.latitude, 32.83331167, 5)
            
        with self.subTest("longitude"):
            self.assertAlmostEqual(self.header.longitude, -107.08305667, 5)
            
      
        
            
        
            

# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()       
        
        
        
            
    