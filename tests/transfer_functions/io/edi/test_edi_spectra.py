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

import numpy as np

from mt_metadata import TF_EDI_SPECTRA, TF_EDI_SPECTRA_OUT
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.edi import EDI
from mt_metadata.utils.mttime import MTime


# =============================================================================
# CGG
# =============================================================================
class TestSpectraEDI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edi_spectra = EDI(fn=TF_EDI_SPECTRA)
        cls.edi_z = EDI(fn=TF_EDI_SPECTRA_OUT)
        cls.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "Quantec Consulting",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "sage_2005_og",
            "DATUM": "WGS 84",
            "ELEV": 0,
            "EMPTY": 1e32,
            "FILEBY": "Quantec Consulting",
            "LAT": 35.55,
            "LON": -106.28333333333333,
        }

        for key, value in head.items():
            with self.subTest(key):
                if key == "LAT":
                    key = "LATITUDE"
                elif key == "LON":
                    key = "LONGITUDE"
                elif key == "ELEV":
                    key = "ELEVATION"
                h_value = getattr(self.edi_spectra.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(
                self.edi_spectra.Header.acqdate, MTime(time_stamp="2004-07-03")
            )

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_spectra.Header.units,
                "millivolt per kilometer per nanotesla",
            )

    def test_info(self):
        info_list = [">INFO\n"]

        self.assertListEqual(info_list, self.edi_spectra.Info.write_info())

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 106.97549946792975),
                ("chtype", "EX"),
                ("id", 14.001),
                ("x", 4872.0),
                ("x2", 4843.0),
                ("y", -3577.0),
                ("y2", -3482.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.measurements["ex"].to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
                ("azm", -163.19130837379313),
                ("chtype", "EY"),
                ("id", 15.001),
                ("x", 4906.0),
                ("x2", 4810.0),
                ("y", -3515.0),
                ("y2", -3544.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.measurements["ey"].to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 107.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 11.001),
                ("x", 4858.0),
                ("y", -3530.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.measurements["hx"].to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
                ("azm", -163.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 12.001),
                ("x", 4858.0),
                ("y", -3530.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.measurements["hy"].to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 13.001),
                ("x", 4858.0),
                ("y", -3530.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.measurements["hz"].to_dict(single=True)
        )

    def test_measurement_rrhx(self):
        with self.subTest("spectra"):
            self.assertNotIn("rrhx", self.edi_spectra.Measurement.measurements.keys())
        with self.subTest("z"):
            self.assertNotIn("rrhx", self.edi_z.Measurement.measurements.keys())

        with self.subTest("spectra"):
            self.assertNotIn("rrhy", self.edi_spectra.Measurement.measurements.keys())
        with self.subTest("z"):
            self.assertNotIn("rrhy", self.edi_z.Measurement.measurements.keys())

    def test_measurement(self):
        m_list = [
            "\n>=DEFINEMEAS\n",
            "    MAXCHAN=7\n",
            "    MAXRUN=999\n",
            "    MAXMEAS=99999\n",
            "    REFLAT=35:33:0.000000\n",
            "    REFLON=-106:17:0.000000\n",
            "    REFELEV=0\n",
            "    REFTYPE=cartesian\n",
            "    UNITS=meter\n",
        ]

        self.assertListEqual(
            m_list,
            self.edi_spectra.Measurement.write_measurement()[0 : len(m_list)],
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(35.55, self.edi_spectra.Measurement.reflat, 2)

        with self.subTest("reflon"):
            self.assertAlmostEqual(-106.2833, self.edi_spectra.Measurement.reflon, 4)

        with self.subTest("refelev"):
            self.assertAlmostEqual(0.0, self.edi_spectra.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            "\n>=MTSECT\n",
            "    NFREQ=33\n",
            "    SECTID=Ex\n",
            "    NCHAN=7\n",
            "    MAXBLOCKS=999\n",
            "    HX=11.001\n",
            "    HY=12.001\n",
            "    HZ=13.001\n",
            "    EX=14.001\n",
            "    EY=15.001\n",
        ]

        self.assertListEqual(
            d_list, self.edi_spectra.Data.write_data()[0 : len(d_list)]
        )

    def test_z(self):
        self.assertTrue(np.isclose(self.edi_spectra.z, self.edi_z.z).all())

    def test_z_err(self):
        self.assertTrue(np.isclose(self.edi_spectra.z_err, self.edi_z.z_err).all())

    def test_t(self):
        self.assertTrue(np.isclose(self.edi_spectra.t, self.edi_z.t).all())

    def test_t_err(self):
        self.assertTrue(np.isclose(self.edi_spectra.t_err, self.edi_z.t_err).all())


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edi = EDI(fn=TF_EDI_SPECTRA)
        cls.tf = TF(fn=TF_EDI_SPECTRA)
        cls.tf.read()

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
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tf = TF(fn=TF_EDI_SPECTRA)
        cls.tf.read()

        cls.edi = cls.tf.to_edi()
        cls.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments"]:
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
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
