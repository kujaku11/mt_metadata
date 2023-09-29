# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:11:57 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest

from mt_metadata.base import helpers

# =============================================================================


class TestWrapDescription(unittest.TestCase):
    def test_wrap_description_short(self):
        line = "short description"
        lines = [line] + [""] * 10
        wrapped = helpers.wrap_description(line, 45)

        self.assertListEqual(wrapped, lines)

    def test_wrap_description_long(self):
        line = "this is one of the longest descriptions ever, it is extremely verbose"
        lines = [
            "this is one of the longest descriptions ever,",
            "it is extremely verbose",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        wrapped = helpers.wrap_description(line, 45)

        self.assertListEqual(wrapped, lines)


class TestValidateC1(unittest.TestCase):
    def test_c1_long(self):
        attr_dict = {
            "long_key_that_is_way_too_verbose_and_unseemingly_lengthy": []
        }
        self.assertEqual(helpers.validate_c1(attr_dict, 45), 62)

    def test_c1_short(self):
        attr_dict = {"short_key": []}
        self.assertEqual(helpers.validate_c1(attr_dict, 45), 45)


class TestWriteLines(unittest.TestCase):
    def test_write(self):
        attr_dict = {
            "a": {
                "type": "string",
                "required": False,
                "style": "free form",
                "units": None,
                "description": (
                    "Any publications that use this data of description that "
                    "is way to long and so no one is going to read it because "
                    "it covers way too many lines.  This is a terrible test, "
                    "dont even get started on unit testing, what a painful "
                    "but necessary process."
                ),
                "options": [],
                "alias": [],
                "example": "my paper",
                "default": None,
            },
            "long_key_that_is_way_too_verbose_and_unseemingly_lengthy": {
                "type": "string",
                "required": False,
                "style": "free form",
                "units": None,
                "description": "Any publications that use this data",
                "options": [],
                "alias": [],
                "example": "my paper",
                "default": (
                    "default value  that "
                    "is way to long and so no one is going to read it because "
                    "it covers way too many lines.  This is a terrible test, "
                    "dont even get started on unit testing, what a painful "
                    "but necessary process."
                ),
            },
        }

        true_str = [
            "       +---------------------------------------------------------------+-----------------------------------------------+----------------+",
            "       | **Metadata Key**                                              | **Description**                               | **Example**    |",
            "       +===============================================================+===============================================+================+",
            "       | **a**                                                         | Any publications that use this data of        | my paper       |",
            "       |                                                               | description that is way to long and so no one |                |",
            "       | Required: False                                               | is going to read it because it covers way too |                |",
            "       |                                                               | many lines.  This is a terrible test, dont    |                |",
            "       | Units: None                                                   | even get started on unit testing, what a      |                |",
            "       |                                                               | painful but necessary process.                |                |",
            "       | Type: string                                                  |                                               |                |",
            "       |                                                               |                                               |                |",
            "       | Style: free form                                              |                                               |                |",
            "       |                                                               |                                               |                |",
            "       | **Default**: None                                             |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       +---------------------------------------------------------------+-----------------------------------------------+----------------+",
            "       | **long_key_that_is_way_too_verbose_and_unseemingly_lengthy**  | Any publications that use this data           | my paper       |",
            "       |                                                               |                                               |                |",
            "       | Required: False                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       | Units: None                                                   |                                               |                |",
            "       |                                                               |                                               |                |",
            "       | Type: string                                                  |                                               |                |",
            "       |                                                               |                                               |                |",
            "       | Style: free form                                              |                                               |                |",
            "       |                                                               |                                               |                |",
            "       | **Default**:                                                  |                                               |                |",
            "       | default value  that is way to long and so no one is going to  |                                               |                |",
            "       | read it because it covers way too many lines.  This is a      |                                               |                |",
            "       | terrible test, dont even get started on unit testing, what a  |                                               |                |",
            "       | painful but necessary process.                                |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       |                                                               |                                               |                |",
            "       +---------------------------------------------------------------+-----------------------------------------------+----------------+",
        ]
        self.assertEqual(helpers.write_lines(attr_dict), "\n".join(true_str))


class TestWriteBlock(unittest.TestCase):
    def test_write_long_description(self):
        attr_dict = {
            "type": "string",
            "required": False,
            "style": "free form",
            "units": None,
            "description": (
                "Any publications that use this data of description that "
                "is way to long and so no one is going to read it because "
                "it covers way too many lines.  This is a terrible test, "
                "dont even get started on unit testing, what a painful "
                "but necessary process."
            ),
            "options": [],
            "alias": [],
            "example": "my paper",
            "default": None,
        }

        true_line = [
            ":navy:`a`",
            "~~~~~~~~~",
            "",
            ".. container::",
            "",
            "   .. table::",
            "       :class: tight-table",
            "       :widths: 45 45 15",
            "",
            "       +----------------------------------------------+-----------------------------------------------+----------------+",
            "       | **a**                                        | **Description**                               | **Example**    |",
            "       +==============================================+===============================================+================+",
            "       | **Required**: False                          | Any publications that use this data of        | my paper       |",
            "       |                                              | description that is way to long and so no one |                |",
            "       | **Units**: None                              | is going to read it because it covers way too |                |",
            "       |                                              | many lines.  This is a terrible test, dont    |                |",
            "       | **Type**: string                             | even get started on unit testing, what a      |                |",
            "       |                                              | painful but necessary process.                |                |",
            "       | **Style**: free form                         |                                               |                |",
            "       |                                              |                                               |                |",
            "       | **Default**: None                            |                                               |                |",
            "       |                                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       +----------------------------------------------+-----------------------------------------------+----------------+",
            "",
        ]

        self.assertEqual(helpers.write_block("a", attr_dict), true_line)

    def test_long_default(self):
        attr_dict = {
            "type": "string",
            "required": False,
            "style": "free form",
            "units": None,
            "description": "Any publications that use this data",
            "options": [],
            "alias": [],
            "example": "my paper",
            "default": (
                "default value  that "
                "is way to long and so no one is going to read it because "
                "it covers way too many lines.  This is a terrible test, "
                "dont even get started on unit testing, what a painful "
                "but necessary process."
            ),
        }

        true_line = [
            ":navy:`a`",
            "~~~~~~~~~",
            "",
            ".. container::",
            "",
            "   .. table::",
            "       :class: tight-table",
            "       :widths: 45 45 15",
            "",
            "       +----------------------------------------------+-----------------------------------------------+----------------+",
            "       | **a**                                        | **Description**                               | **Example**    |",
            "       +==============================================+===============================================+================+",
            "       | **Required**: False                          | Any publications that use this data           | my paper       |",
            "       |                                              |                                               |                |",
            "       | **Units**: None                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       | **Type**: string                             |                                               |                |",
            "       |                                              |                                               |                |",
            "       | **Style**: free form                         |                                               |                |",
            "       |                                              |                                               |                |",
            "       | **Default**:                                 |                                               |                |",
            "       | default value  that is way to long and so no |                                               |                |",
            "       | one is going to read it because it covers way|                                               |                |",
            "       | too many lines.  This is a terrible test,    |                                               |                |",
            "       | dont even get started on unit testing, what a|                                               |                |",
            "       | painful but necessary process.               |                                               |                |",
            "       |                                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       |                                              |                                               |                |",
            "       +----------------------------------------------+-----------------------------------------------+----------------+",
            "",
        ]

        self.assertEqual(helpers.write_block("a", attr_dict), true_line)


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
