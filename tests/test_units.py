# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:26:52 2021

@author: jpeacock
"""

import unittest

from mt_metadata.utils.units import UNITS_LIST, get_unit_object


class TestUnits(unittest.TestCase):
    def test_get_unit(self):
        for item in UNITS_LIST:
            with self.subTest(name=f"name_{item['name']}"):
                self.assertDictEqual(item, get_unit_object(item["name"]).to_dict())

            with self.subTest(name=f"abbreviation_{item['abbreviation']}"):
                self.assertDictEqual(
                    item, get_unit_object(item["abbreviation"]).to_dict()
                )

            if item["alias"] not in [""]:
                with self.subTest(name=f"alias_{item['alias']}"):
                    self.assertDictEqual(item, get_unit_object(item["alias"]).to_dict())

    def test_get_unit_fail(self):
        self.assertRaises(KeyError, get_unit_object, "bad_unit")

    def test_get_unit_none(self):
        self.assertRaises(KeyError, get_unit_object, None, False)

    def test_get_unit_allow_none(self):
        self.assertDictEqual(
            get_unit_object("unknown", allow_none=True).to_dict(),
            get_unit_object(None, allow_none=True).to_dict(),
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
