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

from mt_metadata import TF_EDI_QUANTEC
from mt_metadata.transfer_functions import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Quantec
# =============================================================================
class TestQuantecEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_QUANTEC)

    def test_header(self):
        head = {
            "acqby": "Quantec Geoscience",
            "acqdate": "2014-11-15T00:00:00+00:00",
            "coordinate_system": "geographic",
            "country": "Australia",
            "county": "Boulia",
            "dataid": "TEST_01",
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
        info_list = ["MAXLINES=1000"]

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 14.001),
                ("x", -50.0),
                ("x2", 50.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True))

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "EY"),
                ("id", 15.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -50.0),
                ("y2", 50.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True))

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 11.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True))

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 12.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True))

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 13.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True))

    def test_measurement_rrhx(self):
        self.assertFalse(hasattr(self.edi_obj.Measurement, "rrhx"))

    def test_measurement_rrhy(self):
        self.assertFalse(hasattr(self.edi_obj.Measurement, "rrhy"))

    def test_measurement(self):
        m_list = [
            "MAXCHAN=7",
            "MAXRUN=999",
            "MAXMEAS=99999",
            "UNITS=M",
            "REFLAT=-23:03:4.08",
            "REFLONG=139:28:3.12",
            "REFELEV=122",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(-23.05113, self.edi_obj.Measurement.reflat, 5)

        with self.subTest("reflon"):
            self.assertAlmostEqual(139.46753, self.edi_obj.Measurement.reflon, 5)

        with self.subTest("refelev"):
            self.assertAlmostEqual(122.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = OrderedDict(
            [
                ("ex", "14.001"),
                ("ey", "15.001"),
                ("hx", "11.001"),
                ("hy", "12.001"),
                ("hz", "13.001"),
                ("maxblocks", 999),
                ("nchan", 7),
                ("nfreq", 41),
                ("rrhx", "0"),
                ("rrhy", "0"),
                ("sectid", "TEST_01"),
            ]
        )

        self.assertDictEqual(d_list, self.edi_obj.Data.to_dict(single=True))

        for ch in ["hx", "hy", "hz", "ex", "ey", "rrhx", "rrhy"]:
            with self.subTest(ch):
                self.assertEqual(d_list[ch], getattr(self.edi_obj.Data, ch))


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi = edi.EDI(fn=TF_EDI_QUANTEC)
        self.tf = TF(fn=TF_EDI_QUANTEC)
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

    def test_impedance_error(self):
        self.assertTrue((self.tf.impedance_error.data != 0).all())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_EDI_QUANTEC)
        self.tf.read()

        self.edi = self.tf.to_edi()
        self.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True, required=False)
        for edi_key, edi_value in edi_st.items():
            if edi_key in [
                "comments",
                "transfer_function.remote_references",
            ]:
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

    def test_impedance_error(self):
        self.assertTrue((self.tf.impedance_error.data != 0).all())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
