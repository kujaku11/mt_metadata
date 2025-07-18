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
    Channel,
    Decimation,
    FC,
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
        self.dl.decimation.factor = 4
        self.dl.decimation.level = 1
        self.dl.id = 1
        self.dl.time_series_decimation.sample_rate = 16.0

        self.start = "2020-01-01T00:00:00+00:00"
        self.end = "2020-01-01T00:20:00+00:00"

        self.ex = Channel(component="ex")
        self.ex.time_period.start = self.start
        self.ex.time_period.end = self.end
        self.ex.sample_rate_window_step = 32
        self.ex.sample_rate_decimation_level = 16

        self.hy = Channel(component="hy")
        self.hy.time_period.start = self.start
        self.hy.time_period.end = self.end
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
        dl2.decimation.level = 6
        dl2.id = 6
        fc2.add_decimation_level(dl2)

        fc3 = fc1 + fc2

        self.assertEqual(len(fc3), 2)

    def test_update(self):
        fc1 = self.fc.copy()
        fc2 = self.fc.copy()
        fc2.levels.remove("1")
        dl2 = self.dl.copy()
        dl2.decimation.level = 6
        dl2.id = 6
        fc2.add_decimation_level(dl2)

        fc1.update(fc2)

        self.assertEqual(len(fc1), 2)

    def test_decimation_levels(self):
        self.assertListEqual([1], self.fc.decimation_levels)

    def test_set_decimation_levels(self):
        fc1 = FC()
        fc1.decimation_levels = [1, 2, 3]

        self.assertListEqual([1, 2, 3], fc1.decimation_levels)

    def test_channels_estimated(self):
        self.assertListEqual(["ex", "hy"], self.fc.channels_estimated)

    def test_set_channels_estimated(self):
        fc1 = FC()
        fc1.channels_estimated = ["ex", "hy"]

        self.assertListEqual(["ex", "hy"], fc1.channels_estimated)

    def test_has_decimation_level(self):
        self.assertTrue(self.fc.has_decimation_level(1))

    def test_decimation_level_index(self):
        self.assertEqual(0, self.fc.decimation_level_index(1))

    def test_get_decimation_level(self):
        self.assertEqual(self.dl, self.fc.get_decimation_level(1))

    def test_n_decimation_levels(self):
        self.assertEqual(1, self.fc.n_decimation_levels)

    def test_time_period(self):
        with self.subTest("start"):
            self.assertEqual(self.start, self.fc.time_period.start)
        with self.subTest("end"):
            self.assertEqual(self.end, self.fc.time_period.end)


# =============================================================================
if __name__ == "__main__":
    unittest.main()
