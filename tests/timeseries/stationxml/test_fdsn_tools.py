# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:23:12 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest

from mt_metadata.timeseries.stationxml import fdsn_tools


class TestOrientationCode(unittest.TestCase):
    """
    get orientation code from azimuth
    """

    def setUp(self):
        self.north = 0
        self.vertical = 3
        self.east = 91
        self.one = -10
        self.two = 134
        self.three = 20

    def test_north(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.north), "N")
        self.assertEqual(fdsn_tools.get_orientation_code(-5), "N")
        self.assertEqual(fdsn_tools.get_orientation_code(5), "N")

    def test_east(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.east), "E")
        self.assertEqual(fdsn_tools.get_orientation_code(85), "E")
        self.assertEqual(fdsn_tools.get_orientation_code(95), "E")

    def test_vertical(self):
        self.assertEqual(fdsn_tools.get_orientation_code(
            self.vertical, "vertical"), "Z")
        self.assertEqual(fdsn_tools.get_orientation_code(-5, "vertical"), "Z")
        self.assertEqual(fdsn_tools.get_orientation_code(5, "vertical"), "Z")
    
    def test_one(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.one), "1")
        
    def test_two(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.two), "2")
    
    def test_three(self):
        self.assertEqual(fdsn_tools.get_orientation_code(self.three, "vertical"), "3")


class TestChannelCode(unittest.TestCase):
    """
    test making and reading channel codes
    """

    def setUp(self):
        self.h_channel_code = "LFN"
        self.e_channel_code = "HQE"
        self.aux_channel_code = "LKZ"

    def test_orientation_code(self):

        self.assertEqual(fdsn_tools.get_orientation_code(0, "vertical"), "Z")
        self.assertEqual(fdsn_tools.get_orientation_code(6), "1")

    def test_read_h_channel(self):
        ch_dict = fdsn_tools.read_channel_code(self.h_channel_code)
        self.assertDictEqual(ch_dict["period"], {"min": 0.95, "max": 1.05})
        self.assertEqual(ch_dict["component"], "magnetics")
        self.assertDictEqual(ch_dict["orientation"], {"min": 0.996, "max": 1})

    def test_read_e_channel(self):
        ch_dict = fdsn_tools.read_channel_code(self.e_channel_code)
        self.assertDictEqual(ch_dict["period"], {"min": 80, "max": 250})
        self.assertEqual(ch_dict["component"], "electric")
        self.assertDictEqual(ch_dict["orientation"], {"min": 0, "max": 0.003805})

    def test_read_aux_channel(self):
        ch_dict = fdsn_tools.read_channel_code(self.aux_channel_code)
        self.assertDictEqual(ch_dict["period"], {"min": 0.95, "max": 1.05})
        self.assertEqual(ch_dict["component"], "temperature")
        self.assertDictEqual(ch_dict["orientation"], {"min": 0.996, "max": 0.996})


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
