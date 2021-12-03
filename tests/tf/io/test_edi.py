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
from mt_metadata import (TF_EDI_CGG, TF_EDI_METRONIX, TF_EDI_PHOENIX, TF_EDI_QUANTEC)
# =============================================================================

class TestCGGEDI(unittest.TestCase):
    
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_CGG)
        
    def test_header(self):
        head = {
         'ACQBY': 'GSC_CGG',
         'ACQDATE': '2014-06-05',
         'COORDINATE_SYSTEM': 'Geographic',
         'DATAID': 'EGC022',
         'DATUM': 'WGS84',
         'DECLINATION': 'None',
         'ELEV': '175.270',
         'EMPTY': '1e+32',
         'FILEBY': 'mt_metadata',
         'LAT': '-30.930285',
         'LOC': 'Australia',
         'LON': '127.22923',
         'PROGDATE': '2020-11-10',
         'PROGNAME': 'mt_metadata',
         'PROGVERS': '0.1.4',
         'PROJECT': 'EGC',
         'STDVERS': 'SEG 1.0',
         'SURVEY': 'None',
         'UNITS': 'millivolts_per_kilometer_per_nanotesla'}
        
        for key, value in head.items():
            with self.subTest(key):
                self.assertEqual(getattr(self.edi_obj.Header, key.lower()), value)
                
 
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
     