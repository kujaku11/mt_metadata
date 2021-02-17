# -*- coding: utf-8 -*-
"""
Tests for Metadata module

.. todo::
    * write tests for to/from_xml
    

Created on Tue Apr 28 18:08:40 2020

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================

import unittest
from mt_metadata.base import Base
from mt_metadata.utils.exceptions import MTValidatorError

# =============================================================================
# Tests
# =============================================================================
class TestBase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.base_object = Base()
        self.extra_name = "ExtraAttribute"
        self.extra_v_dict = {
            "type": str,
            "required": True,
            "units": "mv",
            "style": "controlled vocabulary",
            "description": "test adding attribute",
            "options": ["10", "12"],
            "alias": ["other"],
            "example": "extra",
        }
        self.extra_value = 10

    def test_validate_name(self):
        self.assertEqual(
            "name.test_case", self.base_object._validate_name("name/TestCase")
        )

        self.assertRaises(
            MTValidatorError, self.base_object._validate_name, "0Name/Test_case"
        )

    def test_add_attribute(self):
        self.base_object.add_base_attribute(
            self.extra_name, self.extra_value, self.extra_v_dict
        )
        self.assertIsInstance(
            self.base_object.extra_attribute, self.extra_v_dict["type"]
        )
        self.assertEqual(self.base_object.extra_attribute, "10")

    def test_validate_type(self):
        self.assertEqual(10.0, self.base_object._validate_type("10", "float"))
        self.assertEqual(10, self.base_object._validate_type("10", int))
        self.assertEqual("10", self.base_object._validate_type(10, str))
        self.assertEqual(True, self.base_object._validate_type("true", bool))

        number_list = [10, "11", 12.6, "13.3"]
        self.assertEqual(
            [10, 11, 12, 13], self.base_object._validate_type(number_list, int)
        )
        self.assertEqual(
            [10.0, 11.0, 12.6, 13.3],
            self.base_object._validate_type(number_list, float),
        )
        self.assertEqual(
            ["10", "11", "12.6", "13.3"],
            self.base_object._validate_type(number_list, str),
        )
        self.assertEqual(
            [True, False], self.base_object._validate_type(["true", "False"], bool)
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
