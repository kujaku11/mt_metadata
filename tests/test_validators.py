# -*- coding: utf-8 -*-
"""
Tests for Schema module

Created on Tue Apr 28 18:08:40 2020

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================

import unittest
from mt_metadata.utils import validators
from mt_metadata.utils.exceptions import MTValidatorError

# =============================================================================
# Tests
# =============================================================================
class TestValidators(unittest.TestCase):
    def setUp(self):
        self.name = "Test/StandardEnd"
        self.type = str
        self.style = "name"
        self.required = True
        self.units = "mv"
        self.description = "test description"
        self.options = "[option01 | option02 | ...]"
        self.alias = "other_name"
        self.example = "example name"
        self.header = [
            "attribute",
            "type",
            "required",
            "units",
            "style",
            "description",
            "options",
            "alias",
            "example",
        ]

        self.value_dict = {
            "type": self.type,
            "required": self.required,
            "units": self.units,
            "style": self.style,
            "description": self.description,
            "options": self.options,
            "alias": self.alias,
            "example": self.example,
        }

        self.name_fail = "0test/WeakSauce"
        self.type_fail = "value"
        self.style_fail = "fancy"
        self.header_fail = ["type", "required", "units"]
        self.required_fail = "Negative"
        self.units_fail = 10
        self.value_dict_fail = {
            "type": self.type_fail,
            "required": self.required_fail,
            "units": self.units_fail,
            "style": self.style_fail,
        }

    def test_validate_header_with_attribute(self):
        self.assertListEqual(
            sorted(self.header),
            sorted(validators.validate_header(self.header, attribute=True)),
        )

    def test_validate_header_without_attribute(self):
        self.assertListEqual(
            sorted(self.header[1:]),
            sorted(validators.validate_header(self.header[1:], attribute=False)),
        )

    def test_validate_header_fail(self):
        self.assertRaises(
            MTValidatorError, validators.validate_header, self.header_fail
        )

    def test_validate_required(self):
        self.assertEqual(self.required, validators.validate_required(self.required))
        self.assertEqual(
            self.required, validators.validate_required(str(self.required))
        )

    def test_validate_required_fail(self):
        self.assertRaises(
            MTValidatorError, validators.validate_required, self.required_fail
        )

    def test_validate_type(self):
        self.assertEqual("string", validators.validate_type(str))
        self.assertEqual("float", validators.validate_type(float))
        self.assertEqual("integer", validators.validate_type(int))
        self.assertEqual("boolean", validators.validate_type(bool))

    def test_validate_type_fail(self):
        self.assertRaises(MTValidatorError, validators.validate_type, self.type_fail)

    def test_validate_units(self):
        self.assertEqual(self.units, validators.validate_units(self.units))
        self.assertEqual(None, validators.validate_units(None))

    def test_validate_units_fail(self):
        self.assertRaises(MTValidatorError, validators.validate_units, self.units_fail)

    def test_validate_style(self):
        self.assertEqual(self.style, validators.validate_style(self.style))
        self.assertEqual("name", validators.validate_style(None))

    def test_validate_style_fail(self):
        self.assertRaises(MTValidatorError, validators.validate_style, self.style_fail)

    def test_validate_attribute(self):
        self.assertEqual("test.standard_end", validators.validate_attribute(self.name))

    def test_validate_attribue_fail(self):
        self.assertRaises(
            MTValidatorError, validators.validate_attribute, self.name_fail
        )

    def test_validate_description(self):
        self.assertEqual(
            self.description, validators.validate_description(self.description)
        )

    def test_validated_options(self):
        valid_list = validators.validate_options(self.options)
        self.assertIsInstance(validators.validate_options(self.options), list)
        self.assertListEqual(["option01", "option02", "..."], valid_list)
        valid_list = validators.validate_options(["option01", "option02", "..."])
        self.assertListEqual(["option01", "option02", "..."], valid_list)

    def test_validate_alias(self):
        valid_alias = validators.validate_alias(self.alias)
        self.assertIsInstance(valid_alias, list)
        self.assertListEqual(valid_alias, ["other_name"])


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
