# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:33:36 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import unittest
from types import GeneratorType
import numpy as np
import pandas as pd

from mt_metadata.transfer_functions.processing.aurora.band import (
    Band,
    FrequencyBands,
)

# =============================================================================
class TestFrequencyBand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.band_edges = np.vstack(([1, 10], [11, 20]))
        self.fbands = FrequencyBands(band_edges=self.band_edges)

    def test_number_of_bands(self):
        self.assertEqual(self.band_edges.shape[0], self.fbands.number_of_bands)

    def test_validate(self):
        self.assertEqual(None, self.fbands.validate())

    def test_bands(self):
        self.assertIsInstance(self.fbands.bands(), GeneratorType)

    def test_band(self):
        b = self.fbands.band(0)
        other = Band(frequency_min=1, frequency_max=10)
        self.assertEqual(b, other)

    def test_band_centers(self):
        self.assertTrue(
            np.isclose(
                np.array([3.16227766, 14.83239697]), self.fbands.band_centers()
            ).all()
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
