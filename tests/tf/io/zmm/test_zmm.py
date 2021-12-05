# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 16:28:09 2021

@author: jpeacock
"""

import unittest
import numpy as np

from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.zfiles import zmm
from mt_metadata import TF_ZMM


class TestTranslateZmm(unittest.TestCase):
    def setUp(self):
        self.tf_obj = TF(TF_ZMM)
        self.zmm_obj = zmm.ZMM(TF_ZMM)

    def test_latitude(self):
        self.assertEqual(self.tf_obj.latitude, self.zmm_obj.latitude)

    def test_longitude(self):
        self.assertEqual(self.tf_obj.longitude, self.zmm_obj.longitude)

    def test_station(self):
        self.assertEqual(self.tf_obj.station, self.zmm_obj.station)

    def test_channels_recorded(self):
        self.assertListEqual(
            ["hx", "hy", "hz", "ex", "ey"], self.zmm_obj.channels_recorded
        )

    def test_hx(self):
        with self.subTest("Testing Channel hx.channel", i=1):
            self.assertEqual(self.zmm_obj.hx.channel, "hx")
        with self.subTest("Testing Channel hx.number", i=2):
            self.assertEqual(self.zmm_obj.hx.number, 1)
        with self.subTest("Testing Channel hx.dl", i=3):
            self.assertEqual(self.zmm_obj.hx.dl, str(300))
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
            self.assertEqual(self.zmm_obj.hy.dl, str(300))
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
            self.assertEqual(self.zmm_obj.hz.dl, str(300))
        with self.subTest("Testing Channel hz.azimuth", i=4):
            self.assertEqual(self.zmm_obj.hz.azimuth, 0.0)
        with self.subTest("Testing Channel hz.tilt", i=5):
            self.assertEqual(self.zmm_obj.hz.tilt, 0.0)

    def test_ex(self):
        with self.subTest("Testing Channel EX.channel", i=1):
            self.assertEqual(self.zmm_obj.ex.channel, "ex")
        with self.subTest("Testing Channel EX.number", i=2):
            self.assertEqual(self.zmm_obj.ex.number, 4)
        with self.subTest("Testing Channel EX.dl", i=3):
            self.assertEqual(self.zmm_obj.ex.dl, str(300))
        with self.subTest("Testing Channel EX.azimuth", i=4):
            self.assertEqual(self.zmm_obj.ex.azimuth, 0.0)
        with self.subTest("Testing Channel EX.tilt", i=5):
            self.assertEqual(self.zmm_obj.ex.tilt, 0.0)

    def test_ey(self):
        with self.subTest("Testing Channel ey.channel", i=1):
            self.assertEqual(self.zmm_obj.ey.channel, "ey")
        with self.subTest("Testing Channel ey.number", i=2):
            self.assertEqual(self.zmm_obj.ey.number, 5)
        with self.subTest("Testing Channel ey.dl", i=3):
            self.assertEqual(self.zmm_obj.ey.dl, str(300))
        with self.subTest("Testing Channel ey.azimuth", i=4):
            self.assertEqual(self.zmm_obj.ey.azimuth, 90.0)
        with self.subTest("Testing Channel ey.tilt", i=5):
            self.assertEqual(self.zmm_obj.ey.tilt, 0.0)

    def test_transfer_function(self):
        with self.subTest("testing shape", i=1):
            self.assertEqual(self.zmm_obj.transfer_functions.shape, (38, 3, 2))
        with self.subTest("testing dtype", i=2):
            self.assertEqual(self.zmm_obj.transfer_functions.dtype.type, np.complex64)

    def test_sigma_s(self):
        with self.subTest("testing shape", i=1):
            self.assertEqual(self.zmm_obj.sigma_s.shape, (38, 2, 2))
        with self.subTest("testing dtype", i=2):
            self.assertEqual(self.zmm_obj.sigma_s.dtype.type, np.complex64)

    def test_sigma_e(self):
        with self.subTest("testing shape", i=1):
            self.assertEqual(self.zmm_obj.sigma_e.shape, (38, 3, 3))
        with self.subTest("testing dtype", i=2):
            self.assertEqual(self.zmm_obj.sigma_e.dtype.type, np.complex64)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()