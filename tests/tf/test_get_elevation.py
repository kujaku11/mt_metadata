# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 12:53:29 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest

from mt_metadata.transfer_functions.io.tools import get_nm_elev

# =============================================================================


class TestGetNMElevation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.true_elevation = 1899.16394043

    def test_get_good_value(self):
        nm_value = get_nm_elev(40, -120)
        if nm_value == 0:
            self.assertAlmostEqual(nm_value, 0.0)
        else:
            self.assertAlmostEqual(nm_value, self.true_elevation)

    def test_get_bad_value(self):
        nm_value = get_nm_elev(0, 0)
        self.assertEqual(0, nm_value)


# =============================================================================
# run
# =============================================================================
if __name__ in "__main__":
    unittest.main()
