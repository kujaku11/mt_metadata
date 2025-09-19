# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 11:18:39 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================

import unittest
from mt_metadata.timeseries import Location

# =============================================================================
#
# =============================================================================
class TestLocation(unittest.TestCase):
    def setUp(self):
        self.lat_str = "40:20:10.15"
        self.lat_value = 40.336153
        self.lon_str = "-115:20:30.40"
        self.lon_value = -115.34178
        self.elev_str = "1234.5"
        self.elev_value = 1234.5
        self.location_object = Location()
        self.lat_fail_01 = "40:20.34556"
        self.lat_fail_02 = 96.78
        self.lon_fail_01 = "-112:23.3453"
        self.lon_fail_02 = 190.87

    def test_str_conversion(self):
        self.location_object.latitude = self.lat_str
        self.assertAlmostEqual(self.lat_value, self.location_object.latitude, places=5)

        self.location_object.longitude = self.lon_str
        self.assertAlmostEqual(self.lon_value, self.location_object.longitude, places=5)

        self.location_object.elevation = self.elev_str
        self.assertAlmostEqual(
            self.elev_value, self.location_object.elevation, places=1
        )

    def test_fails(self):
        self.assertRaises(
            ValueError, self.location_object._assert_lat_value, self.lat_fail_01
        )
        self.assertRaises(
            ValueError, self.location_object._assert_lat_value, self.lat_fail_02
        )
        self.assertRaises(
            ValueError, self.location_object._assert_lon_value, self.lon_fail_01
        )
        self.assertRaises(
            ValueError, self.location_object._assert_lon_value, self.lon_fail_02
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
