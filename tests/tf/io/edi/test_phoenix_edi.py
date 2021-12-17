# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest

from collections import OrderedDict
from mt_metadata.transfer_functions.io import edi
from mt_metadata import TF_EDI_PHOENIX

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
         'Lat 22:49.423 S Lng 139:17.681 E',
         'FILE: IEB0537A IEB0564M',
         'MTU-DFT VERSION: TStoFT.38',
         'MTU-RBS VERSION:R2012-0216-B22',
         'Reference Field: Remote H - Ref.',
         'RBS: 7  COH: 0.85  RHO VAR: 0.75',
         'CUTOFF: 0.00 COH: 35 % VAR: 25 %',
         'Notch Filters set for 50 Hz.',
         'Comp   MTU box  S/N   Temp',
         'Ex & Ey: MTU5A    2189   39 C',
         'Hx & Hy: MTU5A    2189   39 C',
         'Hz: MTU5A    2189   39 C',
         'Rx & Ry: MTU5A    2779   40 C',
         'STATION 1',
         'Site Desc; BadR: 0 SatR: 54',
         'Lat  22:49:254S Long 139:17:409E',
         'Elevation: 158    M. DECL: 0.000',
         'Reference Site: IEB0564M',
         'Site Permitted by:',
         'Site Layout by:',
         'SYSTEM INFORMATION',
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
         'Ebat:12.3V Hbat:12.3V Rbat:11.9V']

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH1"),
                ("chtype", "EX"),
                ("id", 5374.0537),
                ("x", -50.0),
                ("x2", 50.0),
                ("y", -0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True))

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH2"),
                ("chtype", "EY"),
                ("id", 5375.0537),
                ("x", 22.4),
                ("x2", -22.4),
                ("y", -44.7),
                ("y2", 44.7),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True))

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH3"),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 5371.0537),
                ("x", 8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True))

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH4"),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 5372.0537),
                ("x", -8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True))

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH5"),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 5373.0537),
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True))

    def test_measurement_rrhx(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH6"),
                ("azm", 0.0),
                ("chtype", "RRHX"),
                ("dip", 0.0),
                ("id", 5376.0537),
                ("x", 8.5),
                ("y", 45008.5),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_rrhx.to_dict(single=True)
        )

    def test_measurement_rrhy(self):
        ch = OrderedDict(
            [
                ("acqchan", "CH7"),
                ("azm", 90.0),
                ("chtype", "RRHY"),
                ("dip", 0.0),
                ("id", 5377.0537),
                ("x", -8.5),
                ("y", 45008.5),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_rrhy.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "MAXCHAN=7",
            "MAXRUN=999",
            "MAXMEAS=7",
            "UNITS=M",
            "REFTYPE=CART",
            "REFLAT=-22:49:25.4",
            "REFLONG=139:17:40.9",
            "REFELEV=158",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(-22.82372, self.edi_obj.Measurement.reflat, 5)

        with self.subTest("reflon"):
            self.assertAlmostEqual(139.294694, self.edi_obj.Measurement.reflon, 5)

        with self.subTest("reflong"):
            self.assertAlmostEqual(139.294694, self.edi_obj.Measurement.reflong, 5)

        with self.subTest("refelev"):
            self.assertAlmostEqual(158.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            'SECTID="14-IEB0537A"',
            "NCHAN=7",
            "NFREQ=80",
            "MAXBLKS=80",
            "// 7",
            "05371.0537",
            "05372.0537",
            "05373.0537",
            "05374.0537",
            "05375.0537",
            "05376.0537",
            "05377.0537",
        ]

        self.assertListEqual(d_list, self.edi_obj.Data.data_list)

        for ii, ch in enumerate(["hx", "hy", "hz", "ex", "ey", "rrhx", "rrhy"], 5):
            with self.subTest(msg=ch):
                self.assertEqual(str(float(d_list[ii])), getattr(self.edi_obj.Data, ch))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
