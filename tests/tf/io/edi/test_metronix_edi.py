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
from mt_metadata.transfer_functions.core import TF
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_METRONIX

# =============================================================================
# Metronix
# =============================================================================
class TestMetronixEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_METRONIX)
        self.maxDiff = None

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
            self.assertEqual(
                self.edi_obj.Header._acqdate, MTime("08/17/14 04:58")
            )

        with self.subTest("end date"):
            self.assertEqual(
                self.edi_obj.Header._enddate, MTime("08/17/14 20:03")
            )

    def test_info(self):
        info_list = []

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 1000.0001),
                ("x", -50.0),
                ("x2", 50.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "EY"),
                ("id", 1001.0001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -50.0),
                ("y2", 50.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 1002.0001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 1003.0001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 1004.0001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "MAXCHAN=9",
            "MAXRUN=999",
            "MAXMEAS=1000",
            "REFTYPE=CART",
            "REFLOC=Braunschweig",
            "REFLAT=22:41:28.962",
            "REFLONG=139:42:18.144",
            "REFELEV=181",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                22.6913783, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                139.70504, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("reflong"):
            self.assertAlmostEqual(
                139.70504, self.edi_obj.Measurement.reflong, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(181.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            "SECTID=GEO858",
            "NFREQ=73",
            "EX=1000.0001",
            "EY=1001.0001",
            "HX=1002.0001",
            "HY=1003.0001",
            "HZ=1004.0001",
        ]

        self.assertListEqual(d_list, self.edi_obj.Data.data_list)

        for ii, ch in enumerate(["ex", "ey", "hx", "hy", "hz"], 2):
            with self.subTest(ch):
                self.assertEqual(
                    d_list[ii].split("=")[1], getattr(self.edi_obj.Data, ch)
                )


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi = edi.EDI(fn=TF_EDI_METRONIX)
        self.tf = TF(fn=TF_EDI_METRONIX)
        self.tf.read()

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            with self.subTest(edi_key):
                self.assertEqual(edi_value, tf_st[edi_key])

    def test_survey_metadata(self):
        edi_st = self.edi.survey_metadata.to_dict(single=True)
        tf_st = self.tf.survey_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            with self.subTest(edi_key):
                self.assertEqual(edi_value, tf_st[edi_key])

    def test_has_impedance(self):
        self.assertTrue(self.tf.has_impedance())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_EDI_METRONIX)
        self.tf.read()

        self.edi = self.tf.to_edi()
        self.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True, required=False)
        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments", "transfer_function.remote_references"]:
                with self.subTest(edi_key):
                    self.assertNotEqual(edi_value, tf_st[edi_key])
            else:
                with self.subTest(edi_key):
                    self.assertEqual(edi_value, tf_st[edi_key])

    def test_survey_metadata(self):
        edi_st = self.edi.survey_metadata.to_dict(single=True)
        tf_st = self.tf.survey_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            with self.subTest(edi_key):
                self.assertEqual(edi_value, tf_st[edi_key])

    def test_has_impedance(self):
        self.assertTrue(self.tf.has_impedance())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
