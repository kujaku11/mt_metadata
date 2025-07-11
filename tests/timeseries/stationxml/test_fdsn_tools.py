# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:23:12 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest
import pytest
try:
    from mt_metadata.timeseries.stationxml import fdsn_tools
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)


class TestOrientationCode(unittest.TestCase):
    """
    get orientation code from azimuth
    """

    @classmethod
    def setUpClass(self):
        self.north = 0
        self.vertical = 3
        self.east = 91
        self.one = -16
        self.two = 134
        self.three = 20

    def test_north(self):
        for angle in [-14, -10, -5, 0, 5, 10, 14]:
            with self.subTest(msg=f"testing angle {angle}"):
                self.assertEqual(fdsn_tools.get_orientation_code(angle), "N")

    def test_east(self):
        for angle in [76, 80, 85, 91, 95, 100, 104]:
            with self.subTest(msg={f"testing angle {angle}"}):
                self.assertEqual(fdsn_tools.get_orientation_code(angle), "E")

    def test_vertical(self):
        for angle in [-14, -10, -5, 0, 3, 5, 10, 14]:
            with self.subTest(msg=f"Testing angle {angle}"):
                self.assertEqual(
                    fdsn_tools.get_orientation_code(
                        angle, orientation="vertical"
                    ),
                    "Z",
                )

    def test_one(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.one), "1")

    def test_two(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.two), "2")

    def test_three(self):
        self.assertEqual(
            fdsn_tools.get_orientation_code(
                self.three, orientation="vertical"
            ),
            "3",
        )

    def test_x_direction(self):
        self.assertEqual(fdsn_tools.get_orientation_code(direction="x"), "N")

    def test_y_direction(self):
        self.assertEqual(fdsn_tools.get_orientation_code(direction="y"), "E")

    def test_z_direction(self):
        self.assertEqual(fdsn_tools.get_orientation_code(direction="z"), "Z")

    def test_direction_fail(self):
        self.assertRaises(
            ValueError, fdsn_tools.get_orientation_code, None, "k"
        )


class TestChannelCode(unittest.TestCase):
    """
    test making and reading channel codes
    """

    @classmethod
    def setUpClass(self):
        self.h_channel_code = "LFN"
        self.e_channel_code = "EQE"
        self.aux_channel_code = "LKZ"

    def test_orientation_code(self):

        with self.subTest("0 to Z"):
            self.assertEqual(
                fdsn_tools.get_orientation_code(0, orientation="vertical"), "Z"
            )
        with self.subTest("16 to 1"):
            self.assertEqual(fdsn_tools.get_orientation_code(16), "1")
        with self.subTest("50 to 2"):
            self.assertEqual(fdsn_tools.get_orientation_code(50), "2")

    def test_read_h_channel(self):
        ch_dict = fdsn_tools.read_channel_code(self.h_channel_code)
        with self.subTest("dict equal"):
            self.assertDictEqual(ch_dict["period"], {"min": 0.95, "max": 1.05})
        with self.subTest("measurement type"):
            self.assertEqual(ch_dict["measurement"], "magnetic")
        with self.subTest("orientation"):
            self.assertDictEqual(
                ch_dict["orientation"], {"angle": 0, "variance": 15}
            )

    def test_read_e_channel(self):
        ch_dict = fdsn_tools.read_channel_code(self.e_channel_code)
        with self.subTest("dict equal"):
            self.assertDictEqual(ch_dict["period"], {"min": 80, "max": 250})
        with self.subTest("measurement type"):
            self.assertEqual(ch_dict["measurement"], "electric")
        with self.subTest("orientation"):
            self.assertDictEqual(
                ch_dict["orientation"], {"angle": 90, "variance": 15}
            )

    def test_read_aux_channel(self):
        ch_dict = fdsn_tools.read_channel_code(self.aux_channel_code)
        with self.subTest("dict equal"):
            self.assertDictEqual(ch_dict["period"], {"min": 0.95, "max": 1.05})
        with self.subTest("measurement type"):
            self.assertEqual(ch_dict["measurement"], "temperature")
        with self.subTest("orientation"):
            self.assertDictEqual(
                ch_dict["orientation"], {"angle": 0, "variance": 15}
            )

    def test_make_h_channel(self):
        ch_code = fdsn_tools.make_channel_code(1, "magnetic", 0)
        self.assertEqual(ch_code, self.h_channel_code)

    def test_make_h_channel_direction(self):
        ch_code = fdsn_tools.make_channel_code(1, "magnetic", "x")
        self.assertEqual(ch_code, self.h_channel_code)

    def test_make_e_channel(self):
        ch_code = fdsn_tools.make_channel_code(100, "electric", 87)
        self.assertEqual(ch_code, self.e_channel_code)

    def test_make_e_channel_direction(self):
        ch_code = fdsn_tools.make_channel_code(100, "electric", "y")
        self.assertEqual(ch_code, self.e_channel_code)

    def test_make_aux_channel(self):
        ch_code = fdsn_tools.make_channel_code(
            1, "temperature", 4, orientation="vertical"
        )
        self.assertEqual(ch_code, self.aux_channel_code)

    def test_make_aux_channel_direction(self):
        ch_code = fdsn_tools.make_channel_code(1, "temperature", "z")
        self.assertEqual(ch_code, self.aux_channel_code)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
