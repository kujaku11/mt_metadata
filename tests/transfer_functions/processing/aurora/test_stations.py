# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: jpeacock
"""

import unittest

from mt_metadata.transfer_functions.processing.aurora import Station, Stations


class TestStation(unittest.TestCase):
    """
    Test Station metadata
    """

    def setUp(self):
        self.stations = Stations()

    def test_initialization(self):
        with self.subTest("test local"):
            self.assertIsInstance(self.stations.local, Station)
        with self.subTest("test remote type"):
            self.assertIsInstance(self.stations.remote, list)
        with self.subTest("test remote list"):
            self.assertEqual(self.stations.remote, [])

    def test_add_remote_station(self):
        rr = Station(id="rr01")
        self.stations.remote = rr
        with self.subTest("is list"):
            self.assertIsInstance(self.stations.remote, list)

        with self.subTest("in keys"):
            self.assertIn("rr01", self.stations.remote_dict.keys())
        with self.subTest("is remote"):
            self.assertTrue(self.stations.remote[0].remote)

    def test_add_remote_list(self):
        rr_dict = [Station(id="rr01")]
        self.stations.remote = rr_dict
        with self.subTest("is list"):
            self.assertIsInstance(self.stations.remote, list)
        with self.subTest("list len"):
            self.assertEqual(1, len(self.stations.remote))
        with self.subTest("in keys"):
            self.assertIn("rr01", self.stations.remote_dict.keys())
        with self.subTest("is remote"):
            self.assertTrue(self.stations.remote[0].remote)

    def test_add_remote_dict(self):
        rr_dict = Station(id="rr01").to_dict()
        self.stations.remote = rr_dict
        with self.subTest("is list"):
            self.assertIsInstance(self.stations.remote, list)
        with self.subTest("list len"):
            self.assertEqual(1, len(self.stations.remote))
        with self.subTest("in keys"):
            self.assertIn("rr01", self.stations.remote_dict.keys())
        with self.subTest("is remote"):
            self.assertTrue(self.stations.remote[0].remote)

    def test_get_station_fail(self):
        self.assertRaises(KeyError, self.stations.get_station, "mt01")


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
