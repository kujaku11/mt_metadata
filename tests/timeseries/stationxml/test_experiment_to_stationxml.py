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
from collections import OrderedDict

from mt_metadata.timeseries import Experiment
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata import MT_EXPERIMENT_MULTIPLE_RUNS

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
        self.assertEqual(
            len(self.inventory.networks[0].stations[0].channels),
            len(self.experiment.surveys[0].stations[0].runs[0].channels) + 3,
        )


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
