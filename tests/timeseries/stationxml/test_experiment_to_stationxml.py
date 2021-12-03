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

from mt_metadata.timeseries import Experiment
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata import (
    MT_EXPERIMENT_MULTIPLE_RUNS, MT_EXPERIMENT_MULTIPLE_RUNS_02
    )

# =============================================================================


class TestExperiment2StationXML(unittest.TestCase):
    def setUp(self):
        self.experiment = Experiment()
        self.experiment.from_xml(fn=MT_EXPERIMENT_MULTIPLE_RUNS.as_posix())
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None

        self.inventory = self.translator.mt_to_xml(self.experiment)

    def test_num_networks(self):
        self.assertEqual(len(self.inventory.networks), len(self.experiment.surveys))

    def test_num_stations(self):
        self.assertEqual(
            len(self.inventory.networks[0].stations),
            len(self.experiment.surveys[0].stations),
        )

    def test_num_channels(self):
        # the length is 8 because the h-sensor id's are not the same.
        self.assertEqual(
            len(self.inventory.networks[0].stations[0].channels),
            len(self.experiment.surveys[0].stations[0].runs[0].channels) + 3,
        )
        
    def test_channel_time_periods(self):
        for code in ["LFN", "LFE", "LFZ", "LQN", "LQE"]:
            channels = self.inventory.networks[0].stations[0].select(channel=code).channels
            for ii, channel in enumerate(channels[1:], 0):
                with self.subTest(f"{code} test start"):
                    self.assertTrue(channels[ii].start_date < channel.start_date)
                with self.subTest(f"{code} test end"):
                    self.assertTrue(channels[ii].end_date < channel.end_date)
                with self.subTest(f"{code} contintuity"):
                    self.assertTrue(channels[ii].end_date < channel.start_date)
                    
    def test_station_time_periods(self):
        with self.subTest("test station start time period in channels"):
            c_start = [c.start_date for c in self.inventory.networks[0].stations[0].channels]
            self.assertTrue(self.inventory.networks[0].stations[0].start_date <= min(c_start))
         
        with self.subTest("test station end time period in channels"):
            c_end = [c.end_date for c in self.inventory.networks[0].stations[0].channels]
            self.assertTrue(self.inventory.networks[0].stations[0].end_date >= max(c_end))
            
    def test_network_time_periods(self):
        with self.subTest("test network start time period in stations"):
            c_start = [c.start_date for c in self.inventory.networks[0].stations]
            self.assertTrue(self.inventory.networks[0].start_date <= min(c_start))
         
        with self.subTest("test station end time period in channels"):
            c_end = [c.end_date for c in self.inventory.networks[0].stations]
            self.assertTrue(self.inventory.networks[0].end_date >= max(c_end))

class TestExperiment2StationXML02(unittest.TestCase):
    def setUp(self):
        self.experiment = Experiment()
        self.experiment.from_xml(fn=MT_EXPERIMENT_MULTIPLE_RUNS_02.as_posix())
        self.translator = XMLInventoryMTExperiment()
        self.maxDiff = None

        self.inventory = self.translator.mt_to_xml(self.experiment)

    def test_num_networks(self):
        self.assertEqual(len(self.inventory.networks), len(self.experiment.surveys))

    def test_num_stations(self):
        self.assertEqual(
            len(self.inventory.networks[0].stations),
            len(self.experiment.surveys[0].stations),
        )

    def test_num_channels(self):
        # the length is 10 because channel metadata changes.
        self.assertEqual(
            len(self.inventory.networks[0].stations[0].channels),
            10,
        )
    
    def test_channel_time_periods(self):
        for code in ["LFN", "LFE", "LFZ", "LQN", "LQE"]:
            channels = self.inventory.networks[0].stations[0].select(channel=code).channels
            for ii, channel in enumerate(channels[1:], 0):
                with self.subTest(f"{code} test start"):
                    self.assertTrue(channels[ii].start_date < channel.start_date)
                with self.subTest(f"{code} test end"):
                    self.assertTrue(channels[ii].end_date < channel.end_date)
                with self.subTest(f"{code} contintuity"):
                    self.assertTrue(channels[ii].end_date < channel.start_date)
              
    def test_station_time_periods(self):
        with self.subTest("test station start time period in channels"):
            c_start = [c.start_date for c in self.inventory.networks[0].stations[0].channels]
            self.assertTrue(self.inventory.networks[0].stations[0].start_date <= min(c_start))
         
        with self.subTest("test station end time period in channels"):
            c_end = [c.end_date for c in self.inventory.networks[0].stations[0].channels]
            self.assertTrue(self.inventory.networks[0].stations[0].end_date >= max(c_end))
            
    def test_network_time_periods(self):
        with self.subTest("test network start time period in stations"):
            c_start = [c.start_date for c in self.inventory.networks[0].stations]
            self.assertTrue(self.inventory.networks[0].start_date <= min(c_start))
         
        with self.subTest("test station end time period in channels"):
            c_end = [c.end_date for c in self.inventory.networks[0].stations]
            self.assertTrue(self.inventory.networks[0].end_date >= max(c_end)) 
    
                    

# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
