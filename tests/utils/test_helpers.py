# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:11:57 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata.base import helpers


# =============================================================================


class TestWrapDescription:
    """Test class for wrap_description function with fixtures and subtests."""

    @pytest.fixture
    def wrap_test_cases(self):
        """Fixture providing test cases for wrap_description."""
        return [
            {
                "input": "short description",
                "column_width": 45,
                "expected": ["short description"] + [""] * 10,
            },
            {
                "input": "this is one of the longest descriptions ever, it is extremely verbose",
                "column_width": 45,
                "expected": [
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
                ],
            },
        ]

    def test_wrap_description(self, subtests, wrap_test_cases):
        """Test the wrap_description function with multiple cases."""
        for case in wrap_test_cases:
            with subtests.test(input_text=case["input"][:30] + "..."):
                wrapped = helpers.wrap_description(case["input"], case["column_width"])
                assert wrapped == case["expected"]


class TestValidateC1:
    """Test class for validate_c1 function with fixtures and subtests."""

    @pytest.fixture
    def validate_c1_test_cases(self):
        """Fixture providing test cases for validate_c1."""
        return [
            {
                "attr_dict": {
                    "long_key_that_is_way_too_verbose_and_unseemingly_lengthy": []
                },
                "c1": 45,
                "expected": 62,
            },
            {"attr_dict": {"short_key": []}, "c1": 45, "expected": 45},
        ]

    def test_validate_c1(self, subtests, validate_c1_test_cases):
        """Test the validate_c1 function with multiple cases."""
        for case in validate_c1_test_cases:
            with subtests.test(key_length=len(list(case["attr_dict"].keys())[0])):
                result = helpers.validate_c1(case["attr_dict"], case["c1"])
                assert result == case["expected"]


class TestWriteLines:
    """Test class for write_lines function with fixtures and subtests."""

    @pytest.fixture
    def write_lines_attr_dict(self):
        """Fixture providing complex attribute dictionary for write_lines testing."""
        return {
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

    def test_write_lines_output_structure(self, subtests, write_lines_attr_dict):
        """Test write_lines output structure and content."""
        result = helpers.write_lines(write_lines_attr_dict)
        result_lines = result.split("\n")

        with subtests.test("output_is_string"):
            assert isinstance(result, str)

        with subtests.test("contains_header"):
            assert "**Metadata Key**" in result
            assert "**Description**" in result
            assert "**Example**" in result

        with subtests.test("contains_attribute_entries"):
            assert "**a**" in result
            assert (
                "**long_key_that_is_way_too_verbose_and_unseemingly_lengthy**" in result
            )

        with subtests.test("contains_metadata_fields"):
            assert "Required: False" in result
            assert "Units: None" in result
            assert "Type: string" in result
            assert "Style: free form" in result

        with subtests.test("contains_examples"):
            assert "my paper" in result

        with subtests.test("proper_table_formatting"):
            # Check for table borders
            assert any(
                line.startswith("       +") and line.endswith("+")
                for line in result_lines
            )
            # Check for proper column separators
            assert any("|" in line for line in result_lines)


class TestWriteBlock:
    """Test class for write_block function with fixtures and subtests."""

    @pytest.fixture
    def write_block_test_cases(self):
        """Fixture providing test cases for write_block function."""
        return [
            {
                "key": "a",
                "attr_dict": {
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
                "description": "long_description_case",
            },
            {
                "key": "a",
                "attr_dict": {
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
                "description": "long_default_case",
            },
        ]

    def test_write_block_structure(self, subtests, write_block_test_cases):
        """Test write_block function structure and content."""
        for case in write_block_test_cases:
            with subtests.test(case_type=case["description"]):
                result = helpers.write_block(case["key"], case["attr_dict"])

                with subtests.test("output_is_list", case_type=case["description"]):
                    assert isinstance(result, list)

                with subtests.test(
                    "contains_navy_header", case_type=case["description"]
                ):
                    assert f":navy:`{case['key']}`" in result

                with subtests.test(
                    "contains_rst_elements", case_type=case["description"]
                ):
                    result_text = "\n".join(result)
                    assert ".. container::" in result_text
                    assert ".. table::" in result_text
                    assert ":class: tight-table" in result_text

                with subtests.test(
                    "contains_table_structure", case_type=case["description"]
                ):
                    table_lines = [
                        line
                        for line in result
                        if line.strip().startswith("+") or line.strip().startswith("|")
                    ]
                    assert len(table_lines) > 0  # Should have table formatting

                with subtests.test(
                    "contains_metadata_fields", case_type=case["description"]
                ):
                    result_text = "\n".join(result)
                    assert f"**{case['key']}**" in result_text
                    assert "**Required**" in result_text
                    assert "**Units**" in result_text
                    assert "**Type**" in result_text
                    assert "**Style**" in result_text

                with subtests.test(
                    "handles_defaults_properly", case_type=case["description"]
                ):
                    result_text = "\n".join(result)
                    if case["attr_dict"]["default"] is None:
                        assert "**Default**: None" in result_text
                    else:
                        assert "**Default**:" in result_text

    def test_write_block_column_handling(self, subtests):
        """Test write_block with different column configurations."""
        test_attr = {
            "type": "string",
            "required": True,
            "style": "controlled vocabulary",
            "units": "meters",
            "description": "Test description",
            "options": [],
            "alias": [],
            "example": "example",
            "default": "test",
        }

        column_configs = [
            {"c1": 45, "c2": 45, "c3": 15},
            {"c1": 30, "c2": 60, "c3": 10},
            {"c1": 50, "c2": 40, "c3": 20},
        ]

        for config in column_configs:
            with subtests.test(
                config=f"c1={config['c1']}, c2={config['c2']}, c3={config['c3']}"
            ):
                result = helpers.write_block("test_key", test_attr, **config)

                with subtests.test("output_is_list", config=str(config)):
                    assert isinstance(result, list)

                with subtests.test("contains_width_specification", config=str(config)):
                    width_line = (
                        f"       :widths: {config['c1']} {config['c2']} {config['c3']}"
                    )
                    assert width_line in result


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
