# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: jpeacock
"""

import unittest

from mt_metadata.transfer_functions.processing.time_series_decimation import (
    TimeSeriesDecimation,
)


class TestTimeSeriesDecimation(unittest.TestCase):
    """
    Test TimeSeriesDecimation metadata
    """

    def setUp(self):
        self.ts_decimation = TimeSeriesDecimation()

    def test_initialization(self):
        for key in self.ts_decimation.get_attribute_list():
            with self.subTest(key):
                self.assertEqual(
                    self.ts_decimation.get_attr_from_name(key),
                    self.ts_decimation._attr_dict[key]["default"],
                )


if __name__ == "__main__":
    unittest.main()
