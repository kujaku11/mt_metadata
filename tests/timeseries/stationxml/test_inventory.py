# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 23:13:19 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import unittest

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata import (
    STATIONXML_01,
    STATIONXML_02,
    STATIONXML_MULTIPLE_NETWORKS,
)

# =============================================================================


class TestInventory01(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None

        self.experiment = self.translator.xml_to_mt(self.inventory)

    def test_num_networks(self):
        self.assertEqual(
            len(self.inventory.networks), len(self.experiment.surveys)
        )

    def test_num_stations(self):
        self.assertEqual(
            len(self.inventory.networks[0].stations),
            len(self.experiment.surveys[0].stations),
        )

    def test_num_channels(self):
        self.assertEqual(
            len(self.inventory.networks[0].stations[0].channels),
            len(self.experiment.surveys[0].stations[0].runs[0].channels),
        )


class TestInventory02(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None

        self.experiment = self.translator.xml_to_mt(self.inventory)

    def test_num_networks(self):
        self.assertEqual(
            len(self.inventory.networks), len(self.experiment.surveys)
        )

    def test_num_stations(self):
        self.assertEqual(
            len(self.inventory.networks[0].stations),
            len(self.experiment.surveys[0].stations),
        )


class TestInventoryMultipleNetworks(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(
            STATIONXML_MULTIPLE_NETWORKS.as_posix()
        )
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None

        self.experiment = self.translator.xml_to_mt(self.inventory)

    def test_surveys(self):
        self.assertListEqual(
            ["Kansas 2017 Long Period"], self.experiment.surveys.keys()
        )

    def test_stations(self):
        self.assertListEqual(
            ["MTF20", "WYYS2", "MTC20", "WYYS3"],
            self.experiment.surveys["Kansas 2017 Long Period"].stations.keys(),
        )


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
