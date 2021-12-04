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
from mt_metadata.transfer_functions.io.edi.metadata import Header
# from mt_metadata.transfer_functions.core import TF
from mt_metadata.utils.mttime import MTime
from mt_metadata import (TF_EDI_CGG, TF_EDI_METRONIX, TF_EDI_PHOENIX, TF_EDI_QUANTEC)
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
        
        
    


class TestCGGEDI(unittest.TestCase):
    
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_CGG)
        
    def test_header(self):
        head = {
          'ACQBY': 'GSC_CGG',
          'COORDINATE_SYSTEM': 'geographic',
          'DATAID': None,
          'DATUM': 'WGS84',
          'ELEV': 175.270,
          'EMPTY': "1.000000e+032",
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
            
class TestPhoenixEDI(unittest.TestCase):
    
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_PHOENIX)
        
    def test_header(self):
        head = {
            'acqby': 'Phoenix',
         'acqdate': '2014-07-28T00:00:00+00:00',
         'coordinate_system': 'geographic',
         'dataid': '14-IEB0537A',
         'datum': 'WGS84',
         'elevation': 158.0,
         'fileby': 'Phoenix',
         'filedate': '2014-08-01',
         'latitude': -22.823722222222223,
         'longitude': 139.29469444444445,
         'progdate': '2010-03-09',
         'progname': 'mt_metadata',
         'progvers': 'MT-Editor Ver 0.99.2.106',
         'stdvers': 'SEG 1.0'}
        
        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)
                
        with self.subTest("is phoenix"):
            self.assertTrue(self.edi_obj.Header.phoenix_edi)
                
class TestMetronixEDI(unittest.TestCase):
    
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_METRONIX)
        
    def test_header(self):
        head = {
            'acqby': 'Metronix',
         'country': 'Germany',
         'dataid': 'GEO858',
         'datum': 'WGS84',
         'elevation': 181.0,
         'fileby': 'Metronix',
         'filedate': '2014-10-17',
         'latitude': 22.691378333333333,
         'longitude': 139.70504,
         'progdate': '2014-08-14',
         'progname': 'mt_metadata',
         'progvers': 'Version 14 AUG 2014 SVN 1277 MINGW64',
         'state': 'LX',
         'stdvers': 'SEG 1.0',
         'units': 'millivolts_per_kilometer_per_nanotesla'}
        
        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)
                
        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("08/17/14 04:58"))
            
        with self.subTest("end date"):
            self.assertEqual(self.edi_obj.Header._enddate, MTime("08/17/14 20:03"))      

class TestQuantecEDI(unittest.TestCase):
    
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_QUANTEC)
        
    def test_header(self):
        head = {
            'acqby': 'Quantec Geoscience',
         'acqdate': '2014-11-15T00:00:00+00:00',
         'coordinate_system': 'geographic',
         'country': 'Australia',
         'county': 'Boulia',
         'dataid': 'Geoscience Australia',
         'datum': 'WGS84',
         'elevation': 122.0,
         'enddate': '2014-11-15T00:00:00+00:00',
         'fileby': 'Quantec Geoscience',
         'filedate': '2014-11-17',
         'latitude': -23.051133333333333,
         'longitude': 139.46753333333334,
         'progdate': '2012-10-10',
         'progname': 'mt_metadata',
         'progvers': 'MTeditor_v1d',
         'state': 'Queensland',
         'stdvers': '1.0'}
        
        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
     