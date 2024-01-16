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
            "default": "12",
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
        with self.subTest("extra"):
            self.assertIsInstance(
                self.base_object.extra_attribute, self.extra_v_dict["type"]
            )
        with self.subTest("extra 10"):
            self.assertEqual(self.base_object.extra_attribute, "10")

    def test_validate_type(self):

        with self.subTest("float"):
            self.assertEqual(
                10.0, self.base_object._validate_type("10", "float")
            )
        with self.subTest("integer"):
            self.assertEqual(10, self.base_object._validate_type("10", int))
        with self.subTest("string"):
            self.assertEqual("10", self.base_object._validate_type(10, str))
        with self.subTest("bool"):
            self.assertEqual(
                True, self.base_object._validate_type("true", bool)
            )

    def test_list_validation_type(self):

        number_list = [10, "11", 12.6, "13.3"]
        with self.subTest("int"):
            self.assertEqual(
                [10, 11, 12, 13],
                self.base_object._validate_type(number_list, int),
            )
        with self.subTest("float"):
            self.assertEqual(
                [10.0, 11.0, 12.6, 13.3],
                self.base_object._validate_type(number_list, float),
            )
        with self.subTest("string"):
            self.assertEqual(
                ["10", "11", "12.6", "13.3"],
                self.base_object._validate_type(number_list, str),
            )
        with self.subTest("bool"):
            self.assertEqual(
                [True, False],
                self.base_object._validate_type(["true", "False"], bool),
            )

    def test_update(self):
        other = Base()
        other.add_base_attribute(
            self.extra_name, self.extra_value, self.extra_v_dict
        )

        other.extra_attribute = 12

        self.base_object.update(other)

        self.assertEqual(self.base_object, other)

    def test_copy(self):
        other = Base()
        other.add_base_attribute(
            self.extra_name, self.extra_value, self.extra_v_dict
        )
        other.extra_attribute = 12

        new = other.copy()
        self.assertEqual(other, new)

    def test_equal_other(self):
        assert (self.base_object == self.base_object.to_dict()["base"])



# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
