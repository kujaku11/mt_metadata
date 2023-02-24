# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: jpeacock
"""

import unittest
from mt_metadata.transfer_functions.fourier_coefficients import Station


class TestStation(unittest.TestCase):
    """
    Test Station metadata
    """

    def setUp(self):
        self.station = Station()

    def test_initialization(self):
        with self.subTest("test id"):
            self.assertEqual(None, self.station.id)
        with self.subTest("test mth5_path"):
            self.assertEqual(None, self.station.mth5_path)
        with self.subTest("test id"):
            self.assertEqual(False, self.station.remote)


if __name__ == "__main__":
    unittest.main()
