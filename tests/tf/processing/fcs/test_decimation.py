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
    Decimation,
    Channel,
)

# =============================================================================


class TestDecimationInitialization(unittest.TestCase):
    """
    Test Station metadata
    """

    def setUp(self):
        self.decimation = Decimation()

    def test_initialization(self):
        for key in self.decimation.get_attribute_list():
            with self.subTest(key):
                self.assertEqual(
                    self.decimation.get_attr_from_name(key),
                    self.decimation._attr_dict[key]["default"],
                )


class TestDecimation(unittest.TestCase):
    """
    Test Station metadata
    """

    @classmethod
    def setUpClass(self):

        self.dl = Decimation()
        self.dl.decimation_factor = 4
        self.dl.decimation_level = 1
        self.dl.id = 1
        self.dl.sample_rate_decimation = 16

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

    def test_length(self):
        self.assertEqual(len(self.dl), 2)

    def test_add(self):
        dl1 = self.dl.copy()
        dl2 = self.dl.copy()
        dl2.channels.remove("ex")
        ch_ey = self.ex.copy()
        ch_ey.component = "ey"
        dl2.add_channel(ch_ey)

        dl3 = dl1 + dl2

        self.assertEqual(len(dl3), 3)

    def test_update(self):
        dl1 = self.dl.copy()
        dl2 = self.dl.copy()
        dl2.channels.remove("ex")
        ch_ey = self.ex.copy()
        ch_ey.component = "ey"
        dl2.add_channel(ch_ey)

        dl1.update(dl2)

        self.assertEqual(len(dl1), 3)

    def test_channels_estimated(self):
        self.assertListEqual(["ex", "hy"], self.dl.channels_estimated)

    def test_set_channels_estimated(self):
        dl1 = Decimation()
        dl1.channels_estimated = ["ex", "hy"]

        self.assertListEqual(["ex", "hy"], dl1.channels_estimated)

    def test_has_channel(self):
        self.assertTrue(self.dl.has_channel("ex"))

    def test_channel_index(self):
        self.assertEqual(0, self.dl.channel_index("ex"))

    def test_get_channel(self):
        self.assertEqual(self.ex, self.dl.get_channel("ex"))

    def test_n_channels(self):
        self.assertEqual(2, self.dl.n_channels)

    def test_time_period(self):
        with self.subTest("start"):
            self.assertEqual(self.start, self.dl.time_period.start)
        with self.subTest("end"):
            self.assertEqual(self.end, self.dl.time_period.end)


# =============================================================================
if __name__ == "__main__":
    unittest.main()
