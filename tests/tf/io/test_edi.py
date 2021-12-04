# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:42:55 2021

@author: jpeacock
"""
# =============================================================================
# 
# =============================================================================
import unittest

from mt_metadata.transfer_functions.io import edi
from mt_metadata.transfer_functions.core import TF
from mt_metadata.utils.mttime import MTime
from mt_metadata import (TF_EDI_CGG, TF_EDI_METRONIX, TF_EDI_PHOENIX, TF_EDI_QUANTEC)
# =============================================================================

class TestCGGEDI(unittest.TestCase):
    
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_CGG)
        
    def test_header(self):
        head = {
         'ACQBY': 'GSC_CGG',
         'COORDINATE_SYSTEM': 'Geographic',
         'DATAID': 'EGC022',
         'DATUM': 'WGS84',
         'DECLINATION': 'None',
         'ELEV': 175.270,
         'EMPTY': 1e+32,
         'FILEBY': 'mt_metadata',
         'LAT': -30.930285,
         'LOC': 'Australia',
         'LON': 127.22923}
        
        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)
                
        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("06/05/14"))
        
        with self.subTest("units"):
            self.assertNotEqual(self.edi_obj.Header.units, 
                                'millivolts_per_kilometer_per_nanotesla')
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
     