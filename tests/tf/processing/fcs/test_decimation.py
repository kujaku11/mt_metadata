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
)

# =============================================================================


class TestDecimation(unittest.TestCase):
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


# =============================================================================
if __name__ == "__main__":
    unittest.main()
