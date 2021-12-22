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
        self.default = 0
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
            "default",
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
            "default": self.default,
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
        with self.subTest(msg="string"):
            self.assertEqual("string", validators.validate_type(str))
        with self.subTest(msg="float"):
            self.assertEqual("float", validators.validate_type(float))
        with self.subTest(msg="integer"):
            self.assertEqual("integer", validators.validate_type(int))
        with self.subTest(msg="boolean"):
            self.assertEqual("boolean", validators.validate_type(bool))

    def test_validate_type_fail(self):
        self.assertRaises(MTValidatorError, validators.validate_type, self.type_fail)

    def test_validate_units(self):
        with self.subTest(msg="units"):
            self.assertEqual(self.units, validators.validate_units(self.units))
        with self.subTest(msg="none"):
            self.assertEqual(None, validators.validate_units(None))

    def test_validate_units_fail(self):
        self.assertRaises(MTValidatorError, validators.validate_units, self.units_fail)

    def test_validate_style(self):
        with self.subTest(msg="style"):
            self.assertEqual(self.style, validators.validate_style(self.style))
        with self.subTest(msg="None"):
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
        with self.subTest(msg="is list"):
            self.assertIsInstance(validators.validate_options(self.options), list)
        with self.subTest(msg="list equals"):
            self.assertListEqual(["option01", "option02", "..."], valid_list)
        valid_list = validators.validate_options(["option01", "option02", "..."])
        with self.subTest(msg="valid list"):
            self.assertListEqual(["option01", "option02", "..."], valid_list)

    def test_validate_alias(self):
        valid_alias = validators.validate_alias(self.alias)
        with self.subTest(msg="is list"):
            self.assertIsInstance(valid_alias, list)
        with self.subTest(msg="has alias"):
            self.assertListEqual(valid_alias, ["other_name"])

    def test_validate_default(self):
        for value, dtype in zip(
            [0, 0.0, "0", False], ["integer", "float", "string", "boolean"]
        ):
            with self.subTest(msg=dtype):
                self.value_dict["type"] = dtype
                self.value_dict["default"] = 0
                valid_default = validators.validate_default(self.value_dict)
                self.assertEqual(value, valid_default)

    def test_validate_value_type(self):
        test_dict = [
            {"name": [{"type": "string", "value": "test", "compare": "test"}]},
            {"url": [{"type": "string", "value": "a.com", "compare": "a.com"}]},
            {
                "email": [
                    {"type": "string", "value": "a@test.com", "compare": "2@test.com"}
                ]
            },
            {
                "number": [
                    {"type": "integer", "value": "10", "compare": 10},
                    {"type": "float", "value": "10", "compare": 10.0},
                ]
            },
            {
                "date": [
                    {
                        "type": "string",
                        "value": "2020-10-01T00:12:00",
                        "compare": "2020-10-01T00:12:00",
                    }
                ]
            },
            {
                "free form": [
                    {"type": "string", "value": "free form", "compare": "free form"}
                ]
            },
            {
                "time": [
                    {
                        "type": "string",
                        "value": "2020-10-01T00:12:00",
                        "compare": "2020-10-01T00:12:00",
                    }
                ]
            },
            {
                "date time": [
                    {
                        "type": "string",
                        "value": "2020-10-01T00:12:00",
                        "compare": "2020-10-01T00:12:00",
                    }
                ]
            },
            {
                "name list": [
                    {"type": "string", "value": "a, b, c", "compare": ["a", "b", "c"]}
                ]
            },
            {
                "number list": [
                    {"type": "integer", "value": "1, 2, 3", "compare": [1, 2, 3]},
                    {"type": "float", "value": "1, 2, 3", "compare": [1.0, 2.0, 3.0]},
                ]
            },
        ]

        for key_list in test_dict:
            for key, klist in key_list.items():
                for item in klist:
                    with self.subTest(msg=key):
                        valid_value = validators.validate_value_type(
                            item["value"], item["type"], item["style"]
                        )
                        self.assertEqual(valid_value, item["compare"])


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
