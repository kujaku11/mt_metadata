# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================

import unittest
import numpy as np
import pandas as pd

from mt_metadata.transfer_functions.processing.aurora import Band

# =============================================================================


class TestBandInitialization(unittest.TestCase):
    """
    Test Station metadata
    """

    def setUp(self):
        self.band = Band()

    def test_initialization(self):
        for key in self.band.get_attribute_list():
            with self.subTest(key):
                self.assertEqual(
                    self.band.get_attr_from_name(key),
                    self.band._attr_dict[key]["default"],
                )


class TestBandDefault(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.freqs = 0.1 * np.arange(100)  # 0-10Hz
        self.min_freq = 2.0
        self.max_freq = 3.0
        self.band = Band(
            frequency_min=self.min_freq, frequency_max=self.max_freq
        )

    def test_copy(self):
        cloned = self.band.copy()
        self.assertEqual(self.band, cloned)
        
    def test_lower_bound(self):
        self.assertEqual(self.band.lower_bound, self.min_freq)

    def test_upper_bound(self):
        self.assertEqual(self.band.upper_bound, self.max_freq)

    def test_lower_closed(self):
        self.assertEqual(self.band.lower_closed, True)

    def test_upper_closed(self):
        self.assertEqual(self.band.upper_closed, False)

    def test_cast_band_to_interval(self):
        interval = self.band.to_interval()
        self.assertIsInstance(interval, pd.Interval)

    def test_indices_from_frequencies(self):
        self.band.set_indices_from_frequencies(self.freqs)
        with self.subTest("min"):
            self.assertEqual(self.band.index_min, 20)
        with self.subTest("max"):
            self.assertEqual(self.band.index_max, 29)

    def test_harmonics(self):
        harmonics = self.band.in_band_harmonics(self.freqs)
        with self.subTest("min"):
            self.assertEqual(harmonics[0], self.min_freq)
        with self.subTest("max"):
            self.assertAlmostEqual(harmonics[-1], self.max_freq - 0.1)

    def test_harmonic_indices(self):
        self.band.set_indices_from_frequencies(self.freqs)
        self.assertTrue((self.band.harmonic_indices == np.arange(20, 30)).all())

    def test_center_frequency_geometric(self):
        self.band.center_averaging_type = "geometric"
        with self.subTest("frequency"):
            self.assertAlmostEqual(
                self.band.center_frequency, 2.449489742783178
            )
        with self.subTest("period"):
            self.assertAlmostEqual(
                self.band.center_period, 1.0 / 2.449489742783178
            )

    def test_center_frequency_arithmetic(self):
        self.band.center_averaging_type = "arithmetic"
        with self.subTest("frequency"):
            self.assertAlmostEqual(self.band.center_frequency, 2.5)
        with self.subTest("period"):
            self.assertAlmostEqual(self.band.center_period, 1.0 / 2.5)

    def test_name(self):
        self.assertTrue(isinstance(self.band.name, str))



class TestBandClosedRight(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.freqs = 0.1 * np.arange(100)  # 0-10Hz
        self.min_freq = 2.0
        self.max_freq = 3.0
        self.band = Band(
            frequency_min=self.min_freq,
            frequency_max=self.max_freq,
            closed="right",
        )

    def test_lower_bound(self):
        self.assertEqual(self.band.lower_bound, self.min_freq)

    def test_upper_bound(self):
        self.assertEqual(self.band.upper_bound, self.max_freq)

    def test_lower_closed(self):
        self.assertEqual(self.band.lower_closed, False)

    def test_upper_closed(self):
        self.assertEqual(self.band.upper_closed, True)

    def test_cast_band_to_interval(self):
        interval = self.band.to_interval()
        self.assertIsInstance(interval, pd.Interval)

    def test_indices_from_frequencies(self):
        self.band.set_indices_from_frequencies(self.freqs)
        with self.subTest("min"):
            self.assertEqual(self.band.index_min, 21)
        with self.subTest("max"):
            self.assertEqual(self.band.index_max, 30)

    def test_harmonics(self):
        harmonics = self.band.in_band_harmonics(self.freqs)
        with self.subTest("min"):
            self.assertAlmostEqual(harmonics[0], self.min_freq + 0.1)
        with self.subTest("max"):
            self.assertEqual(harmonics[-1], self.max_freq)

    def test_harmonic_indices(self):
        self.band.set_indices_from_frequencies(self.freqs)
        self.assertTrue((self.band.harmonic_indices == np.arange(21, 31)).all())

    def test_center_frequency_geometric(self):
        self.band.center_averaging_type = "geometric"
        with self.subTest("frequency"):
            self.assertAlmostEqual(
                self.band.center_frequency, 2.449489742783178
            )
        with self.subTest("period"):
            self.assertAlmostEqual(
                self.band.center_period, 1.0 / 2.449489742783178
            )

    def test_center_frequency_arithmetic(self):
        self.band.center_averaging_type = "arithmetic"
        with self.subTest("frequency"):
            self.assertAlmostEqual(self.band.center_frequency, 2.5)
        with self.subTest("period"):
            self.assertAlmostEqual(self.band.center_period, 1.0 / 2.5)


class TestBandClosedBoth(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.freqs = 0.1 * np.arange(100)  # 0-10Hz
        self.min_freq = 2.0
        self.max_freq = 3.0
        self.band = Band(
            frequency_min=self.min_freq,
            frequency_max=self.max_freq,
            closed="both",
        )

    def test_lower_bound(self):
        self.assertEqual(self.band.lower_bound, self.min_freq)

    def test_upper_bound(self):
        self.assertEqual(self.band.upper_bound, self.max_freq)

    def test_lower_closed(self):
        self.assertEqual(self.band.lower_closed, True)

    def test_upper_closed(self):
        self.assertEqual(self.band.upper_closed, True)

    def test_cast_band_to_interval(self):
        interval = self.band.to_interval()
        self.assertIsInstance(interval, pd.Interval)

    def test_indices_from_frequencies(self):
        self.band.set_indices_from_frequencies(self.freqs)
        with self.subTest("min"):
            self.assertEqual(self.band.index_min, 20)
        with self.subTest("max"):
            self.assertEqual(self.band.index_max, 30)

    def test_harmonics(self):
        harmonics = self.band.in_band_harmonics(self.freqs)
        with self.subTest("min"):
            self.assertEqual(harmonics[0], self.min_freq)
        with self.subTest("max"):
            self.assertEqual(harmonics[-1], self.max_freq)

    def test_harmonic_indices(self):
        self.band.set_indices_from_frequencies(self.freqs)
        self.assertTrue((self.band.harmonic_indices == np.arange(20, 31)).all())

    def test_center_frequency_geometric(self):
        self.band.center_averaging_type = "geometric"
        with self.subTest("frequency"):
            self.assertAlmostEqual(
                self.band.center_frequency, 2.449489742783178
            )
        with self.subTest("period"):
            self.assertAlmostEqual(
                self.band.center_period, 1.0 / 2.449489742783178
            )

    def test_center_frequency_arithmetic(self):
        self.band.center_averaging_type = "arithmetic"
        with self.subTest("frequency"):
            self.assertAlmostEqual(self.band.center_frequency, 2.5)
        with self.subTest("period"):
            self.assertAlmostEqual(self.band.center_period, 1.0 / 2.5)


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
