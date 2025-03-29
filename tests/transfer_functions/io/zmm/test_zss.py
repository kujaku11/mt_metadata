# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 16:28:09 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest
import numpy as np

from mt_metadata.transfer_functions import TF
from mt_metadata.transfer_functions.io.zfiles import zmm
from mt_metadata import TF_ZSS_TIPPER, DEFAULT_CHANNEL_NOMENCLATURE

# =============================================================================


class TestTranslateZmm(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf_obj = TF(TF_ZSS_TIPPER)
        self.tf_obj.read()
        self.zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        self.maxDiff = None

    def test_latitude(self):
        self.assertEqual(self.tf_obj.latitude, self.zmm_obj.latitude)

    def test_longitude(self):
        self.assertEqual(self.tf_obj.longitude, self.zmm_obj.longitude)

    def test_station(self):
        self.assertEqual(self.tf_obj.station, self.zmm_obj.station)

    def test_channels_recorded(self):
        self.assertListEqual(["hx", "hy", "hz"], self.zmm_obj.channels_recorded)

    def test_channels_dict(self):
        self.assertDictEqual(
            {"hx": "hx", "hy": "hy", "hz": "hz"}, self.zmm_obj.channel_dict
        )

    def test_channel_nomenclature(self):
        self.assertDictEqual(
            DEFAULT_CHANNEL_NOMENCLATURE,
            self.zmm_obj.channel_nomenclature,
        )

    def test_ch_input_dict(self):
        self.assertDictEqual(
            {
                "isp": ["hx", "hy"],
                "res": ["ex", "ey", "hz"],
                "tf": ["hx", "hy"],
                "tf_error": ["hx", "hy"],
                "all": ["ex", "ey", "hz", "hx", "hy"],
            },
            self.zmm_obj._ch_input_dict,
        )

    def test_ch_output_dict(self):
        self.assertDictEqual(
            {
                "isp": ["hx", "hy"],
                "res": ["ex", "ey", "hz"],
                "tf": ["ex", "ey", "hz"],
                "tf_error": ["ex", "ey", "hz"],
                "all": ["ex", "ey", "hz", "hx", "hy"],
            },
            self.zmm_obj._ch_output_dict,
        )

    def test_hx(self):
        with self.subTest("Testing Channel hx.channel", i=1):
            self.assertEqual(self.zmm_obj.hx.channel, "hx")
        with self.subTest("Testing Channel hx.number", i=2):
            self.assertEqual(self.zmm_obj.hx.number, 1)
        with self.subTest("Testing Channel hx.dl", i=3):
            self.assertEqual(self.zmm_obj.hx.dl, "YSW212")
        with self.subTest("Testing Channel hx.azimuth", i=4):
            self.assertEqual(self.zmm_obj.hx.azimuth, 0.0)
        with self.subTest("Testing Channel hx.tilt", i=5):
            self.assertEqual(self.zmm_obj.hx.tilt, 0.0)

    def test_hy(self):
        with self.subTest("Testing Channel hy.channel", i=1):
            self.assertEqual(self.zmm_obj.hy.channel, "hy")
        with self.subTest("Testing Channel hy.number", i=2):
            self.assertEqual(self.zmm_obj.hy.number, 2)
        with self.subTest("Testing Channel hy.dl", i=3):
            self.assertEqual(self.zmm_obj.hy.dl, "YSW212")
        with self.subTest("Testing Channel hy.azimuth", i=4):
            self.assertEqual(self.zmm_obj.hy.azimuth, 90.0)
        with self.subTest("Testing Channel hy.tilt", i=5):
            self.assertEqual(self.zmm_obj.hy.tilt, 0.0)

    def test_hz(self):
        with self.subTest("Testing Channel hz.channel", i=1):
            self.assertEqual(self.zmm_obj.hz.channel, "hz")
        with self.subTest("Testing Channel hz.number", i=2):
            self.assertEqual(self.zmm_obj.hz.number, 3)
        with self.subTest("Testing Channel hz.dl", i=3):
            self.assertEqual(self.zmm_obj.hz.dl, "YSW212")
        with self.subTest("Testing Channel hz.azimuth", i=4):
            self.assertEqual(self.zmm_obj.hz.azimuth, 0.0)
        with self.subTest("Testing Channel hz.tilt", i=5):
            self.assertEqual(self.zmm_obj.hz.tilt, 0.0)

    def test_ex(self):
        with self.subTest("Testing Channel EX.channel", i=1):
            self.assertEqual(self.zmm_obj.ex, None)

    def test_ey(self):
        with self.subTest("Testing Channel ey.channel", i=1):
            self.assertEqual(self.zmm_obj.ey, None)

    def test_transfer_function(self):
        with self.subTest("testing shape", i=1):
            self.assertEqual(self.zmm_obj.transfer_functions.shape, (44, 1, 2))
        with self.subTest("testing dtype", i=2):
            self.assertEqual(
                self.zmm_obj.transfer_functions.dtype.type, np.complex64
            )

    def test_sigma_s(self):
        with self.subTest("testing shape", i=1):
            self.assertEqual(self.zmm_obj.sigma_s.shape, (44, 2, 2))
        with self.subTest("testing dtype", i=2):
            self.assertEqual(self.zmm_obj.sigma_s.dtype.type, np.complex64)

    def test_sigma_e(self):
        with self.subTest("testing shape", i=1):
            self.assertEqual(self.zmm_obj.sigma_e.shape, (44, 1, 1))
        with self.subTest("testing dtype", i=2):
            self.assertEqual(self.zmm_obj.sigma_e.dtype.type, np.complex64)

    def test_has_impedance(self):
        self.assertFalse(self.tf_obj.has_impedance())

    def test_has_tipper(self):
        self.assertTrue(self.tf_obj.has_tipper())

    def test_station_metadata(self):
        zmm_st = self.zmm_obj.station_metadata.to_dict(single=True)
        tf_st = self.tf_obj.station_metadata.to_dict(single=True)
        for zmm_key, zmm_value in zmm_st.items():
            with self.subTest(zmm_key):
                self.assertEqual(zmm_value, tf_st[zmm_key])

    def test_survey_metadata(self):
        zmm_st = self.zmm_obj.survey_metadata.to_dict(single=True)
        tf_st = self.tf_obj.survey_metadata.to_dict(single=True)
        for zmm_key, zmm_value in zmm_st.items():
            if zmm_key in ["id"]:
                with self.subTest(zmm_key):
                    self.assertNotEqual(zmm_value, tf_st[zmm_key])
            else:
                with self.subTest(zmm_key):
                    self.assertEqual(zmm_value, tf_st[zmm_key])


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
