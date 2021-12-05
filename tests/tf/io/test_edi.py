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
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_CGG, TF_EDI_METRONIX, TF_EDI_PHOENIX, TF_EDI_QUANTEC

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
# CGG
# =============================================================================
class TestCGGEDI(unittest.TestCase):
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_CGG)

    def test_header(self):
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": None,
            "DATUM": "WGS84",
            "ELEV": 175.270,
            "EMPTY": "1.000000e+032",
            "FILEBY": "mt_metadata",
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("06/05/14"))

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_obj.Header.units, "millivolts_per_kilometer_per_nanotesla"
            )

    def test_info(self):
        info_list = ['MAXINFO=31',
         '/*',
         'SITE INFO:',
         'OPERATOR=MOOMBARRIGA',
         'ADU_SERIAL=222',
         'E_AZIMUTH=0.0',
         'EX_LEN=100.0',
         'EY_LEN=100.0',
         'EX_RESISTANCE=44479800',
         'EY_RESISTANCE=41693800',
         'H_SITE=E_SITE',
         'H_AZIMUTH=0.0',
         'HX=MFS06e-246',
         'HY=MFS06e-249',
         'HZ=MFS06e-249',
         'HX_RESISTANCE=169869',
         'HY_RESISTANCE=164154',
         'HZ_RESISTANCE=2653',
         'PROCESSING PARAMETERS:',
         'AlgorithmName=L13ss',
         'NDec=1',
         'NFFT=128',
         'Ntype=1',
         'RRType=None',
         'RemoveLargeLines=true',
         'RotMaxE=false',
         '*/']
        
        self.assertListEqual(info_list, self.edi_obj.Info.info_list)
        

# =============================================================================
# Phoenix
# =============================================================================
class TestPhoenixEDI(unittest.TestCase):
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_PHOENIX)

    def test_header(self):
        head = {
            "acqby": "Phoenix",
            "acqdate": "2014-07-28T00:00:00+00:00",
            "coordinate_system": "geographic",
            "dataid": "14-IEB0537A",
            "datum": "WGS84",
            "elevation": 158.0,
            "fileby": "Phoenix",
            "filedate": "2014-08-01",
            "latitude": -22.823722222222223,
            "longitude": 139.29469444444445,
            "progdate": "2010-03-09",
            "progname": "mt_metadata",
            "progvers": "MT-Editor Ver 0.99.2.106",
            "stdvers": "SEG 1.0",
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("is phoenix"):
            self.assertTrue(self.edi_obj.Header.phoenix_edi)
            
    def test_info(self):
        info_list = ['RUN INFORMATION',
         'PROCESSED FROM DFT TIME SERIES',
         'SURVEY: BOULIA',
         'COMPANY: GA',
         'JOB: IEB',
         'Lat 22:49.423 S Lng 139:17.681 E',
         'HARDWARE: MTU5A MTU5A',
         'START-UP: 2014/07/28 - 02:57:00',
         'END-TIME: 2014/07/28 - 23:38:25',
         'FILE: IEB0537A IEB0564M',
         'MTUPROG VERSION: 3112F6',
         'MTU-DFT VERSION: TStoFT.38',
         'MTU-RBS VERSION:R2012-0216-B22',
         'Reference Field: Remote H - Ref.',
         'XPR Weighting: RHO Variance.',
         'RBS: 7  COH: 0.85  RHO VAR: 0.75',
         'CUTOFF: 0.00 COH: 35 % VAR: 25 %',
         'Notch Filters set for 50 Hz.',
         'Comp   MTU box  S/N   Temp',
         'Ex & Ey: MTU5A    2189   39 C',
         'Hx & Hy: MTU5A    2189   39 C',
         'Hz: MTU5A    2189   39 C',
         'Rx & Ry: MTU5A    2779   40 C',
         'Hx Sen: COIL2318',
         'Hy Sen: COIL2319',
         'Hz Sen: COIL2320',
         'Rx Sen: COIL2485',
         'Ry Sen: COIL2487',
         'STATION 1',
         'STN Number: 14-IEB0537A',
         'Site Desc; BadR: 0 SatR: 54',
         'Lat  22:49:254S Long 139:17:409E',
         'Elevation: 158    M. DECL: 0.000',
         'Reference Site: IEB0564M',
         'Site Permitted by:',
         'Site Layout by:',
         'SYSTEM INFORMATION',
         'MTU-Box Serial Number: U-2189',
         'MTU-Box Gains:E`s x 4 H`s x 4',
         'MTU-Ref Serial Number: U-2779',
         'Comp Chan#   Sensor     Azimuth',
         'Ex1   1     100.0 M    0.0 DGtn',
         'Ey1   2     100.0 M   90.0 DGtn',
         'Hx1   3    COIL2318    0.0 DGtn',
         'Hy1   4    COIL2319   90.0 DGtn',
         'Hz1   5    COIL2320',
         'RHx2   6    COIL2485    0.0 DGtn',
         'RHy2   7    COIL2487   90.0 DGtn',
         'Ebat:12.3V Hbat:12.3V Rbat:11.9V',
         'Ex Pot Resist: 1.085 Kohms',
         'Ex Voltage:AC=25.7mV, DC=+1.30mV',
         'Ey Pot Resist: 0.532 Kohms',
         'Ey Voltage:AC=13.8mV, DC=+1.50mV']
        
        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

# =============================================================================
# Metronix
# =============================================================================
class TestMetronixEDI(unittest.TestCase):
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_METRONIX)

    def test_header(self):
        head = {
            "acqby": "Metronix",
            "country": "Germany",
            "dataid": "GEO858",
            "datum": "WGS84",
            "elevation": 181.0,
            "fileby": "Metronix",
            "filedate": "2014-10-17",
            "latitude": 22.691378333333333,
            "longitude": 139.70504,
            "progdate": "2014-08-14",
            "progname": "mt_metadata",
            "progvers": "Version 14 AUG 2014 SVN 1277 MINGW64",
            "state": "LX",
            "stdvers": "SEG 1.0",
            "units": "millivolts_per_kilometer_per_nanotesla",
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("08/17/14 04:58"))

        with self.subTest("end date"):
            self.assertEqual(self.edi_obj.Header._enddate, MTime("08/17/14 20:03"))

    def test_info(self):
        info_list = ["MAXINFO=1000"] 
        
        self.assertListEqual(info_list, self.edi_obj.Info.info_list)
        

# =============================================================================
# Quantec
# =============================================================================
class TestQuantecEDI(unittest.TestCase):
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_QUANTEC)

    def test_header(self):
        head = {
            "acqby": "Quantec Geoscience",
            "acqdate": "2014-11-15T00:00:00+00:00",
            "coordinate_system": "geographic",
            "country": "Australia",
            "county": "Boulia",
            "dataid": "Geoscience Australia",
            "datum": "WGS84",
            "elevation": 122.0,
            "enddate": "2014-11-15T00:00:00+00:00",
            "fileby": "Quantec Geoscience",
            "filedate": "2014-11-17",
            "latitude": -23.051133333333333,
            "longitude": 139.46753333333334,
            "progdate": "2012-10-10",
            "progname": "mt_metadata",
            "progvers": "MTeditor_v1d",
            "state": "Queensland",
            "stdvers": "1.0",
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)
                
    def test_info(self):
        info_list = ['MAXLINES=1000']
        
        self.assertListEqual(info_list, self.edi_obj.Info.info_list)
        


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
