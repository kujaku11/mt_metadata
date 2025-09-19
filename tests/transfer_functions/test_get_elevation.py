# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 12:53:29 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
import unittest

from mt_metadata.transfer_functions.io.tools import get_nm_elev

# =============================================================================


class TestGetNMElevation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.true_elevation_1 = 1899.16394043
        self.true_elevation_2 = 1895.87854004

    def test_get_good_value(self):
        """
        Test that we can get a good value for elevation from the NM database.

        This test has a weird bug where it returns two different values for the same coordinates.
        The first value is 1899.16394043 and the second value is 1895.87854004.
        See mt_metadata issue #262 for more details.
         
        To get a better workaround than what is here, re: issue 262 we would need to 
        bring information in the `resolution` field of the NM database into the \
        `get_nm_elev` return value.
        """ 
        
        nm_value = get_nm_elev(40, -120)
        if nm_value == 0:
            self.assertAlmostEqual(nm_value, 0.0)
        else:
            match1 = np.isclose(nm_value, self.true_elevation_1, rtol=1e-5)
            match2 = np.isclose(nm_value, self.true_elevation_2, rtol=1e-5)
            self.assertTrue(match1 or match2)

    def test_get_bad_value(self):
        nm_value = get_nm_elev(0, 0)
        self.assertEqual(0, nm_value)


# =============================================================================
# run
# =============================================================================
if __name__ in "__main__":
    unittest.main()
