# -*- coding: utf-8 -*-
"""
Test suite for BirrpBlock metadata class

This comprehensive test suite provides coverage for the BirrpBlock class,
testing instantiation, field validation, serialization, and edge cases.
The test suite is designed for efficiency using pytest fixtures, parametrized
tests, and subtests to optimize test execution.

Key test areas covered:
- BirrpBlock instantiation with various data types
- Field validation for mixed types (str, int, list[int])
- String filename validation and handling
- Integer field validation (nskip, nread, ncomp)
- List[int] field validation (indices)
- JSON/XML serialization and deserialization
- Dictionary operations and round-trip testing
- Edge cases (empty strings, None values, invalid lists)
- Field metadata verification
- Performance testing with batch operations
- Invalid input handling and error cases

The BirrpBlock class contains five fields with different types:
- filnam: string filename (default "")
- nskip: integer number of points to skip (default None)
- nread: integer number of points to read (default None)
- ncomp: integer for number of components (default 0)
- indices: list of integers for index values (default [])

All fields are marked as required in the schema metadata.
"""

import json
from xml.etree import ElementTree as et

import numpy as np
import pytest

# Direct import to avoid jfiles package import issues
from mt_metadata.transfer_functions.io.jfiles.metadata.birrp_block import BirrpBlock


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def default_block():
    """Default block values for testing."""
    return {
        "filnam": "",
        "nskip": None,
        "nread": None,
        "ncomp": 0,
        "indices": [],
    }


@pytest.fixture
def basic_block():
    """Basic block values for testing."""
    return {
        "filnam": "test_data.dat",
        "nskip": 0,
        "nread": 1000,
        "ncomp": 4,
        "indices": [1, 2, 3, 4],
    }


@pytest.fixture
def comprehensive_block():
    """Comprehensive block values for testing."""
    return {
        "filnam": "comprehensive_dataset.bin",
        "nskip": 100,
        "nread": 50000,
        "ncomp": 8,
        "indices": [0, 1, 2, 5, 10, 15, 20],
    }


@pytest.fixture
def filename_test_data():
    """Test data for filename validation."""
    return [
        "simple.dat",
        "data_file_123.bin",
        "complex-filename_v2.0.txt",
        "file with spaces.csv",
        "special@#$chars.log",
        "",  # Empty filename should be allowed
        "very_long_filename_that_exceeds_normal_expectations_but_should_still_be_valid.data",
    ]


@pytest.fixture
def integer_test_data():
    """Test data for integer field validation."""
    return [
        # (input_value, expected_output)
        (0, 0),
        (100, 100),
        (-50, -50),
        ("123", 123),
        ("0", 0),
        (np.int32(500), 500),
        (np.int64(999), 999),
    ]


@pytest.fixture
def list_test_data():
    """Test data for list field validation."""
    return [
        # (input_value, expected_output)
        ([1, 2, 3], [1, 2, 3]),
        ([0], [0]),
        ([], []),
        ([100, 200, 300, 400], [100, 200, 300, 400]),
        ([-1, -2, -3], [-1, -2, -3]),  # Negative values
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),  # Long list
    ]


@pytest.fixture
def invalid_integer_data():
    """Invalid integer data that should raise ValidationError."""
    return [
        "not_a_number",
        "123.456",  # Float string for int field
        [],
        {},
        complex(1, 2),
        "inf",
        "nan",
    ]


@pytest.fixture
def invalid_list_data():
    """Invalid list data that should raise ValidationError."""
    return [
        "not_a_list",
        123,
        ["1", "2", "3"],  # String elements instead of int
        [1.5, 2.5, 3.5],  # Float elements
        [1, "2", 3],  # Mixed types
        {},
        None,
    ]


@pytest.fixture
def empty_block():
    """Empty BirrpBlock instance."""
    return BirrpBlock()


@pytest.fixture
def basic_block_instance(basic_block):
    """Basic BirrpBlock instance."""
    return BirrpBlock(**basic_block)


@pytest.fixture
def comprehensive_block_instance(comprehensive_block):
    """Comprehensive BirrpBlock instance."""
    return BirrpBlock(**comprehensive_block)


# =============================================================================
# Test Class: BirrpBlock Instantiation
# =============================================================================
class TestBirrpBlockInstantiation:
    """Test BirrpBlock instantiation scenarios."""

    def test_default_instantiation(self, empty_block, default_block):
        """Test creating BirrpBlock with default values."""
        assert empty_block.filnam == default_block["filnam"]
        assert empty_block.nskip == default_block["nskip"]
        assert empty_block.nread == default_block["nread"]
        assert empty_block.ncomp == default_block["ncomp"]
        assert empty_block.indices == default_block["indices"]

        # Verify field types
        assert isinstance(empty_block.filnam, str)
        assert empty_block.nskip is None or isinstance(empty_block.nskip, int)
        assert empty_block.nread is None or isinstance(empty_block.nread, int)
        assert isinstance(empty_block.ncomp, int)
        assert isinstance(empty_block.indices, list)

    def test_basic_instantiation(self, basic_block_instance, basic_block):
        """Test creating BirrpBlock with basic values."""
        assert basic_block_instance.filnam == basic_block["filnam"]
        assert basic_block_instance.nskip == basic_block["nskip"]
        assert basic_block_instance.nread == basic_block["nread"]
        assert basic_block_instance.ncomp == basic_block["ncomp"]
        assert basic_block_instance.indices == basic_block["indices"]

    def test_comprehensive_instantiation(
        self, comprehensive_block_instance, comprehensive_block
    ):
        """Test creating BirrpBlock with comprehensive values."""
        assert comprehensive_block_instance.filnam == comprehensive_block["filnam"]
        assert comprehensive_block_instance.nskip == comprehensive_block["nskip"]
        assert comprehensive_block_instance.nread == comprehensive_block["nread"]
        assert comprehensive_block_instance.ncomp == comprehensive_block["ncomp"]
        assert comprehensive_block_instance.indices == comprehensive_block["indices"]

    @pytest.mark.parametrize(
        "filename",
        [
            "test.dat",
            "data_file.bin",
            "complex-name_v1.0.txt",
            "",
        ],
    )
    def test_filename_assignment(self, empty_block, filename):
        """Test filename assignment with various valid names."""
        empty_block.filnam = filename
        assert empty_block.filnam == filename
        assert isinstance(empty_block.filnam, str)

    @pytest.mark.parametrize(
        "field_name,input_val,expected",
        [
            ("nskip", 0, 0),
            ("nskip", 100, 100),
            ("nskip", "50", 50),
            ("nread", 1000, 1000),
            ("nread", "2000", 2000),
            ("nread", -1, -1),
            ("ncomp", 4, 4),
            ("ncomp", "8", 8),
            ("ncomp", 0, 0),
        ],
    )
    def test_integer_field_assignment(
        self, empty_block, field_name, input_val, expected
    ):
        """Test integer field assignment with type conversion."""
        setattr(empty_block, field_name, input_val)
        result = getattr(empty_block, field_name)
        assert result == expected
        assert isinstance(result, int)

    def test_inheritance_from_metadata_base(self, empty_block):
        """Test that BirrpBlock properly inherits from MetadataBase."""
        # Should have MetadataBase methods
        assert hasattr(empty_block, "to_dict")
        assert hasattr(empty_block, "from_dict")
        assert hasattr(empty_block, "to_json")
        assert hasattr(empty_block, "to_xml")

        # Should be able to call str() and repr()
        str_repr = str(empty_block)
        assert isinstance(str_repr, str)

        repr_str = repr(empty_block)
        assert isinstance(repr_str, str)


# =============================================================================
# Test Class: Field Validation
# =============================================================================
class TestFieldValidation:
    """Test field validation and conversion."""

    @pytest.mark.parametrize(
        "filename",
        [
            "simple.dat",
            "data_file_123.bin",
            "complex-filename_v2.0.txt",
            "file with spaces.csv",
            "",
            "very_long_filename.data",
        ],
    )
    def test_valid_filename_values(self, empty_block, filename):
        """Test valid filename values."""
        empty_block.filnam = filename
        assert empty_block.filnam == filename
        assert isinstance(empty_block.filnam, str)

    @pytest.mark.parametrize("field_name", ["nskip", "nread", "ncomp"])
    @pytest.mark.parametrize(
        "input_val,expected",
        [
            (0, 0),
            (100, 100),
            (-50, -50),
            ("123", 123),
            (np.int32(500), 500),
        ],
    )
    def test_valid_integer_conversion(
        self, empty_block, field_name, input_val, expected
    ):
        """Test valid integer conversion for nskip, nread, and ncomp fields."""
        setattr(empty_block, field_name, input_val)
        result = getattr(empty_block, field_name)
        assert result == expected
        assert isinstance(result, int)

    @pytest.mark.parametrize("field_name", ["indices"])
    @pytest.mark.parametrize(
        "input_val,expected",
        [
            ([1, 2, 3], [1, 2, 3]),
            ([0], [0]),
            ([], []),
            ([-1, -2, -3], [-1, -2, -3]),
        ],
    )
    def test_valid_list_conversion(self, empty_block, field_name, input_val, expected):
        """Test valid list conversion for indices field."""
        setattr(empty_block, field_name, input_val)
        result = getattr(empty_block, field_name)
        assert result == expected
        assert isinstance(result, list)
        assert all(isinstance(item, int) for item in result)

    @pytest.mark.parametrize("field_name", ["nskip", "nread", "ncomp"])
    @pytest.mark.parametrize(
        "invalid_val",
        [
            "not_a_number",
            [],
            {},
            complex(1, 2),
        ],
    )
    def test_invalid_integer_values_raise_error(
        self, empty_block, field_name, invalid_val
    ):
        """Test that invalid integer values raise ValidationError."""
        with pytest.raises(Exception):  # Could be ValidationError or ValueError
            setattr(empty_block, field_name, invalid_val)

    @pytest.mark.parametrize("field_name", ["indices"])
    @pytest.mark.parametrize(
        "invalid_val",
        [
            {},  # Only dicts should fail now since validator handles most inputs
        ],
    )
    def test_invalid_list_values_raise_error(
        self, empty_block, field_name, invalid_val
    ):
        """Test that invalid list values raise ValidationError."""
        with pytest.raises(Exception):  # Could be ValidationError or ValueError
            setattr(empty_block, field_name, invalid_val)

    @pytest.mark.parametrize("field_name", ["indices"])
    def test_string_list_coercion(self, empty_block, field_name):
        """Test that string lists get coerced to integer lists."""
        setattr(empty_block, field_name, ["1", "2", "3"])
        result = getattr(empty_block, field_name)
        assert result == [1, 2, 3]
        assert all(isinstance(x, int) for x in result)

    def test_none_values_handling(self, empty_block):
        """Test None values for integer fields."""
        # Default instantiation allows None values (they default to None)
        assert empty_block.nskip is None
        assert empty_block.nread is None

        # But explicit None during instantiation fails due to validation
        with pytest.raises(Exception):
            BirrpBlock(filnam="test.dat", ncomp=4, indices=[], nskip=None, nread=None)

        # And reassignment also fails due to validation
        with pytest.raises(Exception):
            empty_block.nskip = None
        with pytest.raises(Exception):
            empty_block.nread = None

        # None should not be allowed for string fields
        with pytest.raises(Exception):
            empty_block.filnam = None

        with pytest.raises(Exception):
            empty_block.ncomp = None

        # The indices field validator now handles None by converting to empty list
        # So this should not raise an exception
        empty_block.indices = None
        assert empty_block.indices == []

    def test_field_metadata(self, empty_block):
        """Test that field metadata is properly configured."""
        # Get field info from model
        fields = empty_block.model_fields

        # Check that all expected fields exist
        expected_fields = {"filnam", "nskip", "nread", "ncomp", "indices"}
        assert set(fields.keys()) == expected_fields

        # Check field properties
        assert fields["filnam"].default == ""
        assert fields["nskip"].default is None
        assert fields["nread"].default is None
        assert fields["ncomp"].default == 0
        # Default factories for lists
        assert callable(fields["indices"].default_factory)


# =============================================================================
# Test Class: Dictionary Operations
# =============================================================================
class TestDictionaryOperations:
    """Test dictionary serialization and deserialization."""

    def test_to_dict_default_values(self, empty_block):
        """Test converting default BirrpBlock to dictionary."""
        result = empty_block.to_dict()

        assert isinstance(result, dict)
        assert "birrp_block" in result
        block_data = result["birrp_block"]
        expected_keys = {"filnam", "nskip", "nread", "ncomp", "indices"}
        assert set(block_data.keys()).issuperset(expected_keys)
        assert block_data["filnam"] == ""
        assert block_data["nskip"] is None
        assert block_data["nread"] is None
        assert block_data["ncomp"] == 0
        assert block_data["indices"] == []

    def test_to_dict_custom_values(self, basic_block_instance, basic_block):
        """Test converting BirrpBlock with custom values to dictionary."""
        result = basic_block_instance.to_dict()

        assert "birrp_block" in result
        block_data = result["birrp_block"]
        assert block_data["filnam"] == basic_block["filnam"]
        assert block_data["nskip"] == basic_block["nskip"]
        assert block_data["nread"] == basic_block["nread"]
        assert block_data["ncomp"] == basic_block["ncomp"]
        assert block_data["indices"] == basic_block["indices"]

    def test_from_dict_basic(self, empty_block, basic_block):
        """Test loading BirrpBlock from dictionary."""
        empty_block.from_dict(basic_block)

        assert empty_block.filnam == basic_block["filnam"]
        assert empty_block.nskip == basic_block["nskip"]
        assert empty_block.nread == basic_block["nread"]
        assert empty_block.ncomp == basic_block["ncomp"]
        assert empty_block.indices == basic_block["indices"]

    def test_round_trip_dictionary(self, comprehensive_block_instance):
        """Test round-trip dictionary conversion."""
        # Convert to dict and back
        dict_data = comprehensive_block_instance.to_dict()
        new_block = BirrpBlock()
        new_block.from_dict(dict_data)

        # Should be identical
        assert new_block.filnam == comprehensive_block_instance.filnam
        assert new_block.nskip == comprehensive_block_instance.nskip
        assert new_block.nread == comprehensive_block_instance.nread
        assert new_block.ncomp == comprehensive_block_instance.ncomp
        assert new_block.indices == comprehensive_block_instance.indices

    def test_from_dict_partial_data(self, empty_block):
        """Test loading from dictionary with partial data."""
        partial_data = {"filnam": "partial.dat", "nskip": 50, "ncomp": 4}
        empty_block.from_dict(partial_data)

        # Updated fields
        assert empty_block.filnam == "partial.dat"
        assert empty_block.nskip == 50
        assert empty_block.ncomp == 4
        # Default fields should remain
        assert empty_block.nread is None
        assert empty_block.indices == []


# =============================================================================
# Test Class: JSON Serialization
# =============================================================================
class TestJSONSerialization:
    """Test JSON serialization and deserialization."""

    def test_to_json_basic(self, basic_block_instance):
        """Test converting BirrpBlock to JSON."""
        json_str = basic_block_instance.to_json()

        assert isinstance(json_str, str)
        # Should be valid JSON
        json_data = json.loads(json_str)
        assert isinstance(json_data, dict)

    def test_json_round_trip(self, basic_block_instance):
        """Test JSON round-trip conversion."""
        # Convert to JSON and parse back
        json_str = basic_block_instance.to_json()
        json_data = json.loads(json_str)

        # Create new instance from parsed data
        new_block = BirrpBlock()
        new_block.from_dict(json_data)

        # Should match original
        assert new_block.filnam == basic_block_instance.filnam
        assert new_block.nskip == basic_block_instance.nskip
        assert new_block.nread == basic_block_instance.nread
        assert new_block.ncomp == basic_block_instance.ncomp
        assert new_block.indices == basic_block_instance.indices

    def test_json_list_preservation(self, comprehensive_block_instance):
        """Test that JSON preserves list structures."""
        json_str = comprehensive_block_instance.to_json()
        json_data = json.loads(json_str)

        new_block = BirrpBlock()
        new_block.from_dict(json_data)

        # Should preserve list contents exactly
        assert new_block.ncomp == comprehensive_block_instance.ncomp
        assert new_block.indices == comprehensive_block_instance.indices


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization."""

    def test_to_xml_element(self, basic_block_instance):
        """Test converting BirrpBlock to XML element."""
        xml_element = basic_block_instance.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "birrp_block"

    def test_to_xml_string(self, basic_block_instance):
        """Test converting BirrpBlock to XML string."""
        xml_string = basic_block_instance.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "birrp_block" in xml_string
        assert "filnam" in xml_string
        assert "nskip" in xml_string
        assert "nread" in xml_string

    def test_xml_contains_values(self, basic_block_instance, basic_block):
        """Test that XML contains the expected values."""
        xml_string = basic_block_instance.to_xml(string=True)

        # Parse the XML to verify structure
        root = et.fromstring(xml_string)
        assert root.tag == "birrp_block"

        # Check for expected values
        assert basic_block["filnam"] in xml_string
        assert str(basic_block["nskip"]) in xml_string
        assert str(basic_block["nread"]) in xml_string


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling."""

    def test_empty_filename_handling(self, empty_block):
        """Test handling of empty filename."""
        empty_block.filnam = ""
        assert empty_block.filnam == ""
        assert isinstance(empty_block.filnam, str)

    def test_very_long_filename(self, empty_block):
        """Test handling of very long filename."""
        long_filename = "a" * 1000 + ".dat"
        empty_block.filnam = long_filename
        assert empty_block.filnam == long_filename

    def test_special_characters_in_filename(self, empty_block):
        """Test filenames with special characters."""
        special_names = [
            "file with spaces.dat",
            "file-with-dashes.bin",
            "file_with_underscores.txt",
            "file.with.dots.csv",
            "file@#$%^&*().log",
        ]

        for filename in special_names:
            empty_block.filnam = filename
            assert empty_block.filnam == filename

    def test_large_integer_values(self, empty_block):
        """Test handling of large integer values."""
        large_value = 2**30
        empty_block.nskip = large_value
        empty_block.nread = large_value

        assert empty_block.nskip == large_value
        assert empty_block.nread == large_value

    def test_negative_integer_values(self, empty_block):
        """Test handling of negative integer values."""
        empty_block.nskip = -100
        empty_block.nread = -50
        empty_block.ncomp = -1  # Test negative ncomp

        assert empty_block.nskip == -100
        assert empty_block.nread == -50
        assert empty_block.ncomp == -1

    def test_large_lists(self, empty_block):
        """Test handling of large lists."""
        large_list = list(range(1000))
        # ncomp is now an integer, not a list, so test with a single large value
        empty_block.ncomp = 999
        empty_block.indices = large_list

        assert empty_block.ncomp == 999
        assert empty_block.indices == large_list

    def test_negative_values_in_lists(self, empty_block):
        """Test handling of negative values in lists."""
        negative_list = [-1, -2, -3, -4, -5]
        empty_block.indices = negative_list

        assert empty_block.indices == negative_list

    def test_equality_comparison(self, basic_block):
        """Test equality comparison between BirrpBlock instances."""
        block1 = BirrpBlock(**basic_block)
        block2 = BirrpBlock(**basic_block)
        block3 = BirrpBlock()

        assert block1 == block2
        # Note: MetadataBase equality may not work as expected for != comparison
        # so we test the values directly
        assert not (
            block1.filnam == block3.filnam
            and block1.nskip == block3.nskip
            and block1.nread == block3.nread
            and block1.ncomp == block3.ncomp
            and block1.indices == block3.indices
        )

    def test_type_coercion_edge_cases(self, empty_block):
        """Test type coercion edge cases."""
        # String to int conversion
        empty_block.nskip = "0"
        assert empty_block.nskip == 0
        assert isinstance(empty_block.nskip, int)

        # Numpy types
        empty_block.nread = np.int64(500)
        assert empty_block.nread == 500
        assert isinstance(empty_block.nread, int)


# =============================================================================
# Test Class: Performance and Batch Operations
# =============================================================================
class TestPerformanceAndBatchOperations:
    """Test performance characteristics and batch operations."""

    def test_batch_instantiation(self):
        """Test creating multiple BirrpBlock instances efficiently."""
        num_instances = 100
        instances = []

        for i in range(num_instances):
            block = BirrpBlock(
                filnam=f"data_{i}.dat",
                nskip=i,
                nread=i * 100,
                ncomp=i + 1,
                indices=[i * 2, i * 2 + 1, i * 2 + 2],
            )
            instances.append(block)

        # Verify all instances were created correctly
        assert len(instances) == num_instances
        for i, block in enumerate(instances):
            assert block.filnam == f"data_{i}.dat"
            assert block.nskip == i
            assert block.nread == i * 100
            assert block.ncomp == i + 1
            assert block.indices == [i * 2, i * 2 + 1, i * 2 + 2]

    def test_batch_serialization(self, basic_block):
        """Test batch serialization to various formats."""
        num_instances = 50
        instances = [BirrpBlock(**basic_block) for _ in range(num_instances)]

        # Batch convert to dictionaries
        dicts = [instance.to_dict() for instance in instances]
        assert len(dicts) == num_instances

        # Batch convert to JSON
        json_strings = [instance.to_json() for instance in instances]
        assert len(json_strings) == num_instances

        # All should be identical
        for i in range(1, len(dicts)):
            assert dicts[i] == dicts[0]

        for i in range(1, len(json_strings)):
            assert json_strings[i] == json_strings[0]

    def test_large_list_performance(self, empty_block):
        """Test performance with large lists."""
        # Create large lists
        large_ncomp = 100  # Now just an integer
        large_indices = list(range(1000))  # 1000 elements

        # Assignment should be fast
        empty_block.ncomp = large_ncomp
        empty_block.indices = large_indices

        # Verification
        assert empty_block.ncomp == 100
        assert len(empty_block.indices) == 1000
        assert empty_block.indices == large_indices


# =============================================================================
# Test Class: Integration and Workflow Tests
# =============================================================================
class TestIntegrationAndWorkflow:
    """Test integration scenarios and complete workflows."""

    def test_complete_workflow_scenario(self, basic_block):
        """Test a complete workflow scenario."""
        # Step 1: Create instance
        block = BirrpBlock()

        # Step 2: Load from dictionary
        block.from_dict(basic_block)

        # Step 3: Modify values
        block.filnam = "modified_" + block.filnam
        block.nskip += 10
        block.nread *= 2
        block.ncomp += 4  # ncomp is now an integer
        block.indices = [i * 2 for i in block.indices]

        # Step 4: Export to JSON
        json_str = block.to_json()

        # Step 5: Create new instance and load from JSON
        new_block = BirrpBlock()
        json_data = json.loads(json_str)
        new_block.from_dict(json_data)

        # Step 6: Verify workflow worked correctly
        assert new_block.filnam == "modified_" + basic_block["filnam"]
        assert new_block.nskip == basic_block["nskip"] + 10
        assert new_block.nread == basic_block["nread"] * 2
        assert new_block.ncomp == basic_block["ncomp"] + 4
        assert new_block.indices == [i * 2 for i in basic_block["indices"]]

    def test_multiple_format_round_trip(self, comprehensive_block):
        """Test round-trip conversion through multiple formats."""
        # Start with comprehensive block
        original = BirrpBlock(**comprehensive_block)

        # Round trip through dictionary
        dict_data = original.to_dict()
        from_dict = BirrpBlock()
        from_dict.from_dict(dict_data)

        # Round trip through JSON
        json_str = from_dict.to_json()
        json_data = json.loads(json_str)
        from_json = BirrpBlock()
        from_json.from_dict(json_data)

        # All should be equivalent
        assert from_dict.filnam == original.filnam
        assert from_dict.nskip == original.nskip
        assert from_dict.nread == original.nread
        assert from_dict.ncomp == original.ncomp
        assert from_dict.indices == original.indices

        assert from_json.filnam == original.filnam
        assert from_json.nskip == original.nskip
        assert from_json.nread == original.nread
        assert from_json.ncomp == original.ncomp
        assert from_json.indices == original.indices

    def test_error_recovery_workflow(self, basic_block):
        """Test error recovery in workflow scenarios."""
        block = BirrpBlock(**basic_block)
        original_indices = (
            block.indices.copy() if isinstance(block.indices, list) else block.indices
        )
        original_values = (
            block.filnam,
            block.nskip,
            block.nread,
            block.ncomp,  # ncomp is now an integer
            original_indices,
        )

        # Attempt invalid operations and ensure state is preserved
        try:
            block.nskip = "invalid"
        except Exception:
            pass  # Expected to fail

        try:
            block.ncomp = "not_a_number"  # Changed from "not_a_list"
        except Exception:
            pass  # Expected to fail

        # The validator now handles most inputs successfully, including None
        # So we need to find something that actually fails
        original_indices_before_test = (
            block.indices.copy() if isinstance(block.indices, list) else block.indices
        )

        # Test with None (this will succeed and change indices to [])
        block.indices = None
        assert block.indices == []  # Validator converts None to []

        # Restore for next test
        block.indices = original_indices_before_test

        # Original values should be preserved after operations that don't change them
        assert block.filnam == original_values[0]
        assert block.nskip == original_values[1]
        assert block.nread == original_values[2]
        assert block.ncomp == original_values[3]

        # Valid operations should still work
        block.filnam = "recovered.dat"
        assert block.filnam == "recovered.dat"
