# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: jpeacock
"""
import numpy as np
import unittest
from mt_metadata.transfer_functions.processing.aurora import Band


class TestBand(unittest.TestCase):
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

    def test_cast_band_to_interval(self):
        self.band.to_interval()

    def test_indices_from_frequencies(self):
        freqs = 0.1 * np.arange(100) # 0-10Hz
        min_freq = 2.0
        max_freq = 3.0
        band = Band(frequency_min=min_freq, frequency_max=max_freq)
        indices = band.set_indices_from_frequencies(freqs)
        assert (band.index_min==20)
        assert (band.index_max==29)
        harmonics = band.in_band_harmonics(freqs)

        band = Band(frequency_min=2.0, frequency_max=3.0, closed="right")
        indices = band.set_indices_from_frequencies(freqs)
        assert (band.index_min == 21)
        assert (band.index_max == 30)

        band = Band(frequency_min=2.0, frequency_max=3.0, closed="both")
        indices = band.set_indices_from_frequencies(freqs)
        assert (band.index_min == 20)
        assert (band.index_max == 30)
        harmonics = band.in_band_harmonics(freqs)
        assert (harmonics[0] == min_freq)
        assert (harmonics[-1] == max_freq)


if __name__ == "__main__":
    unittest.main()
