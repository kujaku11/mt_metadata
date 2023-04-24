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
)

# =============================================================================


class TestFC(unittest.TestCase):
    """
    Test Station metadata
    """

    def setUp(self):
        self.fc = FC()

    def test_initialization(self):
        for key in self.fc.get_attribute_list():
            with self.subTest(key):
                self.assertEqual(
                    self.fc.get_attr_from_name(key),
                    self.fc._attr_dict[key]["default"],
                )


# =============================================================================
if __name__ == "__main__":
    unittest.main()
