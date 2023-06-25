# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:12:41 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import unittest
from mt_metadata.transfer_functions.processing.fourier_coefficients import (
    FC,
    Decimation,
    Channel,
)

# =============================================================================
class TestFCInitialization(unittest.TestCase):
    def setUp(self):
        self.fc = FC()

    def test_initialization(self):
        for key in self.fc.get_attribute_list():
            with self.subTest(key):
                self.assertEqual(
                    self.fc.get_attr_from_name(key),
                    self.fc._attr_dict[key]["default"],
                )


class TestFC(unittest.TestCase):
    """
    Test Station metadata
    """

    @classmethod
    def setUpClass(self):
        self.fc = FC()
        self.fc.id = "processing_run_001"
        self.fc.starting_sample_rate = 64

        self.dl = Decimation()
        self.dl.decimation_factor = 4
        self.dl.decimation_level = 1
        self.dl.id = 1
        self.dl.sample_rate_decimation = 16

        self.start = "2020-01-01T00:00:00+00:00"
        self.end = "2020-01-01T00:20:00+00:00"

        self.ex = Channel(component="ex")
        self.ex.time_period.start = self.start
        self.ex.time_period.start = self.end
        self.ex.sample_rate_window_step = 32
        self.ex.sample_rate_decimation_level = 16

        self.hy = Channel(component="hy")
        self.hy.time_period.start = self.start
        self.hy.time_period.start = self.end
        self.hy.sample_rate_window_step = 32
        self.hy.sample_rate_decimation_level = 16

        self.dl.add_channel(self.ex)
        self.dl.add_channel(self.hy)
        self.dl.update_time_period()

        self.fc.add_decimation_level(self.dl)
        self.fc.update_time_period()

    def test_length(self):
        self.assertEqual(len(self.fc), 1)

    def test_add(self):
        fc1 = self.fc.copy()
        fc2 = self.fc.copy()
        fc2.levels.remove("1")
        dl2 = self.dl.copy()
        dl2.decimation_level = 6
        dl2.id = 6
        fc2.add_decimation_level(dl2)

        fc3 = fc1 + fc2

        self.assertEqual(len(fc3), 2)


# =============================================================================
if __name__ == "__main__":
    unittest.main()
