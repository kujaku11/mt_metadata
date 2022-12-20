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
    Header,
    EMeasurement,
    HMeasurement,
    DefineMeasurement,
)


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
    @classmethod
    def setUpClass(self):
        self.e_dict = {
            "id": 14.001,
            "azm": 0,
            "chtype": "EX",
            "x": -50.0,
            "y": 0.0,
            "x2": 50.0,
            "y2": 0.0,
        }

        self.ex = EMeasurement(**self.e_dict)

    def test_attr(self):
        for k, v in self.e_dict.items():
            if isinstance(v, (float, int)):
                self.assertAlmostEqual(v, getattr(self.ex, k))
            else:
                self.assertEqual(v, getattr(self.ex, k))


class TestEMeasurementAZM(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.e_dict = {
            "id": 14.001,
            "azm": 0,
            "chtype": "EX",
            "x": -50.0,
            "y": 0.0,
            "x2": 50.0,
            "y2": 10.0,
        }

        self.ex = EMeasurement(**self.e_dict)

    def test_attr(self):
        for k, v in self.e_dict.items():
            if k != "azm":
                self.assertEqual(v, getattr(self.ex, k))
            else:
                self.assertalmostEqual(5.7105931374996, getattr(self.ex, k))


class TestHMeasurement(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.h_dict = {
            "id": 12.001,
            "chtype": "HY",
            "x": 0.0,
            "y": 0.0,
            "azm": 90,
        }

        self.hy = HMeasurement(**self.h_dict)

    def test_attr(self):
        for k, v in self.h_dict.items():
            self.assertEqual(v, getattr(self.hy, k))


class TestDefineMeasurement(unittest.TestCase):
    def setUp(self):
        self.dm = DefineMeasurement()

        self.test_lines = [
            ">=DEFINEMEAS",
            "",
            "    MAXCHAN=7",
            "    MAXRUN=999",
            "    MAXMEAS=7",
            "    UNITS=M",
            "    REFTYPE=CART",
            "",
            ">!****THE X,Y OFFSETS ARE RELATIVE TO THIS REFERENCE****!",
            "    REFLAT=-22:49:25.4",
            "    REFLONG=139:17:40.9",
            "    REFELEV=158",
            "",
            ">!****DEFINE MEASUREMENTS FOR MT SOUNDING****!",
            ">HMEAS ID=05371.0537 CHTYPE=HX X=8.5 Y=8.5 AZM=0 ACQCHAN=CH3",
            ">HMEAS ID=05372.0537 CHTYPE=HY X=-8.5 Y=8.5 AZM=90 ACQCHAN=CH4",
            ">HMEAS ID=05373.0537 CHTYPE=HZ X=21.2 Y=-21.2 AZM=0 ACQCHAN=CH5",
            ">EMEAS ID=05374.0537 CHTYPE=EX X=-50.0 Y=-0.0 X2=50.0 Y2=0.0 ACQCHAN=CH1",
            ">EMEAS ID=05375.0537 CHTYPE=EY X=22.4 Y=-44.7 X2=-22.4 Y2=44.7 ACQCHAN=CH2",
            ">HMEAS ID=05376.0537 CHTYPE=HX X=8.5 Y=45008.5 AZM=0 ACQCHAN=CH6",
            ">HMEAS ID=05377.0537 CHTYPE=HY X=-8.5 Y=45008.5 AZM=90 ACQCHAN=CH7",
        ]

        self.meas_list = [
            "MAXCHAN=7",
            "MAXRUN=999",
            "MAXMEAS=7",
            "UNITS=M",
            "REFTYPE=CART",
            "REFLAT=-22:49:25.4",
            "REFLONG=139:17:40.9",
            "REFELEV=158",
            {
                "id": "05371.0537",
                "chtype": "HX",
                "x": "8.5",
                "y": "8.5",
                "azm": "0",
                "acqchan": "CH3",
            },
            {
                "id": "05372.0537",
                "chtype": "HY",
                "x": "-8.5",
                "y": "8.5",
                "azm": "90",
                "acqchan": "CH4",
            },
            {
                "id": "05373.0537",
                "chtype": "HZ",
                "x": "21.2",
                "y": "-21.2",
                "azm": "0",
                "acqchan": "CH5",
            },
            {
                "id": "05374.0537",
                "chtype": "EX",
                "x": "-50.0",
                "y": "-0.0",
                "x2": "50.0",
                "y2": "0.0",
                "acqchan": "CH1",
            },
            {
                "id": "05375.0537",
                "chtype": "EY",
                "x": "22.4",
                "y": "-44.7",
                "x2": "-22.4",
                "y2": "44.7",
                "acqchan": "CH2",
            },
            {
                "id": "05376.0537",
                "chtype": "HX",
                "x": "8.5",
                "y": "45008.5",
                "azm": "0",
                "acqchan": "CH6",
            },
            {
                "id": "05377.0537",
                "chtype": "HY",
                "x": "-8.5",
                "y": "45008.5",
                "azm": "90",
                "acqchan": "CH7",
            },
        ]

    def test_ref_type(self):
        self.assertEqual(self.dm.reftype, "cartesian")

    def test_units(self):
        self.assertEqual(self.dm.units, "m")

    def test_maxrun(self):
        self.assertEqual(self.dm.maxrun, 999)

    def test_latitude(self):
        self.dm.reflat = "40.9"
        self.assertEqual(self.dm.reflat, 40.9)

    def test_longitude(self):
        self.dm.reflon = "40.9"
        self.assertEqual(self.dm.reflon, 40.9)

    def test_elevation(self):
        self.dm.refelev = "40.9"
        self.assertEqual(self.dm.refelev, 40.9)

    def test_read_lines(self):
        self.dm.read_measurement(self.test_lines)

        self.assertListEqual(self.meas_list, self.dm.measurement_list)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
