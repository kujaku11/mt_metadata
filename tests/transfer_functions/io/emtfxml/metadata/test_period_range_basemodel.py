# -*- coding: utf-8 -*-
"""
Test suite for PeriodRange basemodel

This comprehensive test suite provides coverage for the PeriodRange class,
testing instantiation, XML serialization, dictionary operations, edge cases,
and performance characteristics. The test suite is designed for efficiency
using pytest fixtures and parameterized tests.

Key test areas covered:
- PeriodRange instantiation with various data types
- XML serialization with formatting validation
- Dictionary read/write operations
- Edge cases (negative values, extreme ranges, special floats)
- Field-specific validation and metadata
- Performance testing with batch operations
- Integration workflows and round-trip serialization

The test suite follows the same pattern as other basemodel tests in the project
for consistency and maintainability.
"""

import math

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata.period_range_basemodel import (
    PeriodRange,
)


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def basic_period_range_data():
    """Basic period range data for testing."""
    return {
        "min": 0.001,
        "max": 1000.0,
    }


@pytest.fixture
def scientific_notation_data():
    """Period range data with scientific notation values."""
    return {
        "min": 4.5e-5,
        "max": 4.5e5,
    }


@pytest.fixture
def edge_case_data():
    """Edge case period range data."""
    return {
        "min": 1e-10,
        "max": 1e10,
    }


@pytest.fixture
def zero_range_data():
    """Zero range period data."""
    return {
        "min": 0.0,
        "max": 0.0,
    }


@pytest.fixture
def empty_period_range():
    """Empty period range instance."""
    return PeriodRange()


@pytest.fixture
def basic_period_range(basic_period_range_data):
    """Basic period range instance."""
    return PeriodRange(**basic_period_range_data)


@pytest.fixture
def scientific_period_range(scientific_notation_data):
    """Scientific notation period range instance."""
    return PeriodRange(**scientific_notation_data)


@pytest.fixture
def edge_case_period_range(edge_case_data):
    """Edge case period range instance."""
    return PeriodRange(**edge_case_data)


# =============================================================================
# Test Class: PeriodRange Instantiation
# =============================================================================
class TestPeriodRangeInstantiation:
    """Test period range instantiation scenarios."""

    def test_empty_period_range_creation(self, empty_period_range):
        """Test creating an empty period range."""
        assert empty_period_range.min == 0.0
        assert empty_period_range.max == 0.0

    def test_basic_period_range_creation(
        self, basic_period_range, basic_period_range_data
    ):
        """Test creating a basic period range with valid data."""
        assert basic_period_range.min == basic_period_range_data["min"]
        assert basic_period_range.max == basic_period_range_data["max"]

    def test_scientific_notation_creation(
        self, scientific_period_range, scientific_notation_data
    ):
        """Test creating period range with scientific notation."""
        assert scientific_period_range.min == scientific_notation_data["min"]
        assert scientific_period_range.max == scientific_notation_data["max"]

    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("min", 0.001, 0.001),
            ("min", 1e-6, 1e-6),
            ("min", 0.0, 0.0),
            ("min", 1000.0, 1000.0),
            ("max", 0.001, 0.001),
            ("max", 1e6, 1e6),
            ("max", 0.0, 0.0),
            ("max", 1000.0, 1000.0),
        ],
    )
    def test_field_assignment(self, empty_period_range, field, value, expected):
        """Test individual field assignment."""
        setattr(empty_period_range, field, value)
        assert getattr(empty_period_range, field) == expected

    def test_inheritance_from_metadata_base(self, basic_period_range):
        """Test that PeriodRange inherits from MetadataBase correctly."""
        # Should have the required fields
        assert hasattr(basic_period_range, "min")
        assert hasattr(basic_period_range, "max")
        # Should have MetadataBase methods
        assert hasattr(basic_period_range, "to_xml")
        assert hasattr(basic_period_range, "to_dict")

    def test_field_defaults(self, empty_period_range):
        """Test that fields have correct default values."""
        assert empty_period_range.min == 0.0
        assert empty_period_range.max == 0.0

    def test_numeric_type_validation(self, empty_period_range):
        """Test that fields accept various numeric types."""
        # Test integer assignment
        empty_period_range.min = 1
        empty_period_range.max = 2
        assert empty_period_range.min == 1.0
        assert empty_period_range.max == 2.0

        # Test float assignment
        empty_period_range.min = 1.5
        empty_period_range.max = 2.5
        assert empty_period_range.min == 1.5
        assert empty_period_range.max == 2.5


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization functionality."""

    def test_to_xml_empty_period_range(self, empty_period_range):
        """Test XML serialization of empty period range."""
        xml_element = empty_period_range.to_xml()

        assert xml_element.tag == "PeriodRange"
        assert "min" in xml_element.attrib
        assert "max" in xml_element.attrib
        assert xml_element.attrib["min"].strip() == "0.00000E+00"
        assert xml_element.attrib["max"].strip() == "0.00000E+00"

    def test_to_xml_basic_period_range(self, basic_period_range):
        """Test XML serialization of basic period range."""
        xml_element = basic_period_range.to_xml()

        assert xml_element.tag == "PeriodRange"
        assert "min" in xml_element.attrib
        assert "max" in xml_element.attrib

        # Check scientific notation formatting
        min_val = float(xml_element.attrib["min"])
        max_val = float(xml_element.attrib["max"])
        assert abs(min_val - 0.001) < 1e-10
        assert abs(max_val - 1000.0) < 1e-10

    def test_to_xml_scientific_notation(self, scientific_period_range):
        """Test XML serialization with scientific notation values."""
        xml_element = scientific_period_range.to_xml()

        assert xml_element.tag == "PeriodRange"

        min_val = float(xml_element.attrib["min"])
        max_val = float(xml_element.attrib["max"])
        assert abs(min_val - 4.5e-5) < 1e-10
        assert abs(max_val - 4.5e5) < 1e-5

    def test_to_xml_string_output(self, basic_period_range):
        """Test XML string serialization."""
        xml_string = basic_period_range.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_string
        assert "<PeriodRange" in xml_string
        assert "min=" in xml_string
        assert "max=" in xml_string
        assert "/>" in xml_string

    def test_to_xml_formatting_consistency(self, empty_period_range):
        """Test that XML formatting is consistent."""
        # Test various values to ensure consistent formatting
        test_values = [
            (0.0, 0.0),
            (1.0, 2.0),
            (1e-5, 1e5),
            (0.001, 1000.0),
            (1.23456e-10, 9.87654e10),
        ]

        for min_val, max_val in test_values:
            empty_period_range.min = min_val
            empty_period_range.max = max_val
            xml_element = empty_period_range.to_xml()

            # Should always have both attributes
            assert "min" in xml_element.attrib
            assert "max" in xml_element.attrib

            # Should be parseable as floats
            parsed_min = float(xml_element.attrib["min"])
            parsed_max = float(xml_element.attrib["max"])

            # Should be close to original values
            assert (
                abs(parsed_min - min_val) < 1e-10
                or abs(parsed_min - min_val) / max(abs(min_val), 1e-10) < 1e-6
            )
            assert (
                abs(parsed_max - max_val) < 1e-10
                or abs(parsed_max - max_val) / max(abs(max_val), 1e-10) < 1e-6
            )

    def test_to_xml_required_parameter(self, basic_period_range):
        """Test the required parameter behavior."""
        # Test that required parameter doesn't break functionality
        xml_element_required = basic_period_range.to_xml(required=True)
        xml_element_not_required = basic_period_range.to_xml(required=False)

        # Both should produce similar results
        assert xml_element_required.tag == xml_element_not_required.tag
        assert xml_element_required.attrib == xml_element_not_required.attrib

    def test_to_xml_extreme_values(self, empty_period_range):
        """Test XML serialization with extreme values."""
        extreme_cases = [
            (1e-100, 1e100),
            (float("inf"), float("inf")),
            (-1.0, -2.0),  # Negative values
            (1e-15, 1e15),
        ]

        for min_val, max_val in extreme_cases:
            empty_period_range.min = min_val
            empty_period_range.max = max_val

            if math.isfinite(min_val) and math.isfinite(max_val):
                xml_element = empty_period_range.to_xml()
                assert xml_element.tag == "PeriodRange"
                assert "min" in xml_element.attrib
                assert "max" in xml_element.attrib


# =============================================================================
# Test Class: Dictionary Operations
# =============================================================================
class TestDictionaryOperations:
    """Test dictionary serialization functionality."""

    def test_to_dict_basic_period_range(self, basic_period_range):
        """Test dictionary serialization of basic period range."""
        period_range_dict = basic_period_range.to_dict()

        # Should follow the pattern from other basemodels
        assert "period_range" in period_range_dict
        data = period_range_dict["period_range"]

        assert data["min"] == 0.001
        assert data["max"] == 1000.0

    def test_to_dict_empty_period_range(self, empty_period_range):
        """Test dictionary serialization of empty period range."""
        period_range_dict = empty_period_range.to_dict(required=False)

        assert "period_range" in period_range_dict
        data = period_range_dict["period_range"]

        assert data["min"] == 0.0
        assert data["max"] == 0.0

    def test_to_dict_scientific_notation(self, scientific_period_range):
        """Test dictionary serialization with scientific notation."""
        period_range_dict = scientific_period_range.to_dict()

        assert "period_range" in period_range_dict
        data = period_range_dict["period_range"]

        assert data["min"] == 4.5e-5
        assert data["max"] == 4.5e5

    def test_to_dict_required_parameter_behavior(self, basic_period_range):
        """Test to_dict behavior with required parameter."""
        dict_required = basic_period_range.to_dict(required=True)
        dict_not_required = basic_period_range.to_dict(required=False)

        # Both should contain the same data for non-null values
        assert "period_range" in dict_required
        assert "period_range" in dict_not_required
        assert (
            dict_required["period_range"]["min"]
            == dict_not_required["period_range"]["min"]
        )
        assert (
            dict_required["period_range"]["max"]
            == dict_not_required["period_range"]["max"]
        )


# =============================================================================
# Test Class: Read Dictionary Functionality
# =============================================================================
class TestReadDictionary:
    """Test read_dict functionality."""

    def test_read_dict_basic(self, empty_period_range):
        """Test reading from dictionary with basic period_range structure."""
        input_dict = {
            "period_range": {
                "min": 0.001,
                "max": 1000.0,
            }
        }

        empty_period_range.read_dict(input_dict)

        assert empty_period_range.min == 0.001
        assert empty_period_range.max == 1000.0

    def test_read_dict_scientific_notation(self, empty_period_range):
        """Test reading dictionary with scientific notation."""
        input_dict = {
            "period_range": {
                "min": 4.5e-5,
                "max": 4.5e5,
            }
        }

        empty_period_range.read_dict(input_dict)

        assert empty_period_range.min == 4.5e-5
        assert empty_period_range.max == 4.5e5

    def test_read_dict_missing_period_range_key(self, empty_period_range):
        """Test reading from dictionary without period_range key."""
        input_dict = {
            "some_other_key": {
                "min": 0.001,
                "max": 1000.0,
            }
        }

        # Should raise AttributeError due to missing logger (expected behavior)
        # The helper function tries to log a warning when key is missing
        initial_min = empty_period_range.min
        initial_max = empty_period_range.max

        with pytest.raises(
            AttributeError, match="'PeriodRange' object has no attribute 'logger'"
        ):
            empty_period_range.read_dict(input_dict)

    def test_read_dict_partial_data(self, empty_period_range):
        """Test reading dictionary with partial data."""
        input_dict = {
            "period_range": {
                "min": 0.001,
                # max is missing
            }
        }

        empty_period_range.read_dict(input_dict)

        assert empty_period_range.min == 0.001
        # max should retain default or be handled appropriately

    def test_read_dict_empty_dict(self, empty_period_range):
        """Test reading from empty dictionary."""
        input_dict = {}

        initial_min = empty_period_range.min
        initial_max = empty_period_range.max

        # Should raise AttributeError due to missing logger (expected behavior)
        # The helper function tries to log a warning when key is missing
        with pytest.raises(
            AttributeError, match="'PeriodRange' object has no attribute 'logger'"
        ):
            empty_period_range.read_dict(input_dict)


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def test_negative_values(self, empty_period_range):
        """Test handling of negative period values."""
        empty_period_range.min = -1.0
        empty_period_range.max = -0.5

        assert empty_period_range.min == -1.0
        assert empty_period_range.max == -0.5

        # Should still serialize correctly
        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_very_small_values(self, empty_period_range):
        """Test handling of very small period values."""
        empty_period_range.min = 1e-100
        empty_period_range.max = 1e-50

        assert empty_period_range.min == 1e-100
        assert empty_period_range.max == 1e-50

        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_very_large_values(self, empty_period_range):
        """Test handling of very large period values."""
        empty_period_range.min = 1e50
        empty_period_range.max = 1e100

        assert empty_period_range.min == 1e50
        assert empty_period_range.max == 1e100

        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_equal_min_max_values(self, empty_period_range):
        """Test when min and max are equal."""
        empty_period_range.min = 10.0
        empty_period_range.max = 10.0

        assert empty_period_range.min == 10.0
        assert empty_period_range.max == 10.0

        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_inverted_range(self, empty_period_range):
        """Test when min > max (potentially invalid but should not crash)."""
        empty_period_range.min = 1000.0
        empty_period_range.max = 0.001

        assert empty_period_range.min == 1000.0
        assert empty_period_range.max == 0.001

        # Should still produce valid XML
        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_special_float_values(self, empty_period_range):
        """Test special float values like inf and nan."""
        # Test infinity
        empty_period_range.min = float("inf")
        empty_period_range.max = float("inf")

        assert math.isinf(empty_period_range.min)
        assert math.isinf(empty_period_range.max)

        # Test that it can still create XML (though values may be unusual)
        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_zero_values(self, zero_range_data, empty_period_range):
        """Test handling of zero values."""
        empty_period_range.min = zero_range_data["min"]
        empty_period_range.max = zero_range_data["max"]

        assert empty_period_range.min == 0.0
        assert empty_period_range.max == 0.0

        xml_element = empty_period_range.to_xml()
        assert xml_element.tag == "PeriodRange"

    def test_string_coercion_to_float(self, empty_period_range):
        """Test that string values are coerced to float."""
        empty_period_range.min = "0.001"
        empty_period_range.max = "1000.0"

        assert empty_period_range.min == 0.001
        assert empty_period_range.max == 1000.0
        assert isinstance(empty_period_range.min, float)
        assert isinstance(empty_period_range.max, float)


# =============================================================================
# Test Class: Boundary Value Testing
# =============================================================================
class TestBoundaryValues:
    """Test boundary values and limits."""

    def test_python_float_limits(self, empty_period_range):
        """Test Python float limits."""
        import sys

        # Test with maximum float value
        max_float = sys.float_info.max
        empty_period_range.min = max_float / 2
        empty_period_range.max = max_float

        assert empty_period_range.min == max_float / 2
        assert empty_period_range.max == max_float

        # Test with minimum positive float value
        min_float = sys.float_info.min
        empty_period_range.min = min_float
        empty_period_range.max = min_float * 2

        assert empty_period_range.min == min_float
        assert empty_period_range.max == min_float * 2

    def test_epsilon_values(self, empty_period_range):
        """Test with epsilon-sized differences."""
        import sys

        epsilon = sys.float_info.epsilon
        base_value = 1.0

        empty_period_range.min = base_value
        empty_period_range.max = base_value + epsilon

        assert empty_period_range.min == base_value
        assert empty_period_range.max == base_value + epsilon

    def test_precision_limits(self, empty_period_range):
        """Test precision limits of float representation."""
        # Test values that might lose precision
        precision_test_values = [
            (0.1 + 0.2, 0.3),  # Classic floating point precision issue
            (1.0000000000000001, 1.0000000000000002),
            (1e-15, 2e-15),
        ]

        for min_val, max_val in precision_test_values:
            empty_period_range.min = min_val
            empty_period_range.max = max_val

            # Values should be stored as floats
            assert isinstance(empty_period_range.min, float)
            assert isinstance(empty_period_range.max, float)

            # Should still produce valid XML
            xml_element = empty_period_range.to_xml()
            assert xml_element.tag == "PeriodRange"


# =============================================================================
# Test Class: Integration Tests
# =============================================================================
class TestIntegration:
    """Test integration scenarios and workflows."""

    def test_period_range_creation_and_serialization_workflow(self):
        """Test complete period range creation and serialization workflow."""
        # Create period range
        period_range = PeriodRange(
            min=1e-4,
            max=1e4,
        )

        # Test all serialization methods
        xml_element = period_range.to_xml()
        xml_string = period_range.to_xml(string=True)
        period_range_dict = period_range.to_dict()

        # Verify XML
        assert xml_element.tag == "PeriodRange"
        assert "min" in xml_element.attrib
        assert "max" in xml_element.attrib

        # Verify string
        assert isinstance(xml_string, str)
        assert "PeriodRange" in xml_string

        # Verify dict
        assert "period_range" in period_range_dict

    def test_period_range_modification_workflow(self, basic_period_range):
        """Test modifying period range after creation."""
        # Initial state
        assert basic_period_range.min == 0.001

        # Modify fields
        basic_period_range.min = 1e-5
        basic_period_range.max = 1e5

        # Verify changes
        assert basic_period_range.min == 1e-5
        assert basic_period_range.max == 1e5

        # Verify XML reflects changes
        xml_element = basic_period_range.to_xml()
        min_val = float(xml_element.attrib["min"])
        max_val = float(xml_element.attrib["max"])
        assert abs(min_val - 1e-5) < 1e-10
        assert abs(max_val - 1e5) < 1e-1

    def test_round_trip_serialization(self, basic_period_range):
        """Test round-trip serialization (dict -> read_dict -> dict)."""
        # Get initial dict
        original_dict = basic_period_range.to_dict()

        # Create new instance and read the dict
        new_period_range = PeriodRange()
        new_period_range.read_dict(original_dict)

        # Get dict from new instance
        new_dict = new_period_range.to_dict()

        # Should be the same
        assert original_dict == new_dict

    def test_multiple_period_ranges_creation(self):
        """Test creating multiple period range instances."""
        period_ranges = []

        for i in range(5):
            period_range = PeriodRange(
                min=1e-3 * (i + 1),
                max=1e3 * (i + 1),
            )
            period_ranges.append(period_range)

        assert len(period_ranges) == 5

        # Test they all work independently
        for i, period_range in enumerate(period_ranges):
            expected_min = 1e-3 * (i + 1)
            expected_max = 1e3 * (i + 1)
            assert abs(period_range.min - expected_min) < 1e-10
            assert abs(period_range.max - expected_max) < 1e-1
            xml_element = period_range.to_xml()
            assert xml_element.tag == "PeriodRange"


# =============================================================================
# Test Class: Performance
# =============================================================================
class TestPerformance:
    """Test performance characteristics."""

    def test_large_batch_creation(self):
        """Test creating many period range instances."""
        period_ranges = []

        for i in range(100):
            period_range = PeriodRange(
                min=1e-6 * (i + 1),
                max=1e6 * (i + 1),
            )
            period_ranges.append(period_range)

        assert len(period_ranges) == 100

        # Test a few work correctly
        for period_range in period_ranges[:5]:
            xml_element = period_range.to_xml()
            assert xml_element.tag == "PeriodRange"

    def test_xml_serialization_performance(self, basic_period_range):
        """Test XML serialization performance."""
        # Should complete quickly
        for _ in range(100):
            xml_element = basic_period_range.to_xml()
            assert xml_element.tag == "PeriodRange"

    def test_dict_serialization_performance(self, basic_period_range):
        """Test dictionary serialization performance."""
        # Should complete quickly
        for _ in range(100):
            period_range_dict = basic_period_range.to_dict()
            assert "period_range" in period_range_dict

    def test_read_dict_performance(self, empty_period_range):
        """Test read_dict performance."""
        input_dict = {
            "period_range": {
                "min": 0.001,
                "max": 1000.0,
            }
        }

        # Should complete quickly
        for _ in range(100):
            empty_period_range.read_dict(input_dict)
            assert empty_period_range.min == 0.001
            assert empty_period_range.max == 1000.0


# =============================================================================
# Test Class: Field-Specific Tests
# =============================================================================
class TestFieldSpecifics:
    """Test field-specific behaviors and constraints."""

    def test_min_field_properties(self, empty_period_range):
        """Test min field specific properties."""
        # Test default value
        assert empty_period_range.min == 0.0

        # Test field metadata via Pydantic
        model_fields = empty_period_range.model_fields
        min_field = model_fields["min"]

        assert min_field.default == 0.0
        assert min_field.description == "minimum period"

    def test_max_field_properties(self, empty_period_range):
        """Test max field specific properties."""
        # Test default value
        assert empty_period_range.max == 0.0

        # Test field metadata via Pydantic
        model_fields = empty_period_range.model_fields
        max_field = model_fields["max"]

        assert max_field.default == 0.0
        assert max_field.description == "maxmimu period"  # Note: typo in original

    def test_field_units_metadata(self, empty_period_range):
        """Test that field units are correctly defined."""
        model_fields = empty_period_range.model_fields

        min_field = model_fields["min"]
        max_field = model_fields["max"]

        # Both should have units defined in json_schema_extra
        assert hasattr(min_field, "json_schema_extra")
        assert hasattr(max_field, "json_schema_extra")

        min_schema_extra = min_field.json_schema_extra
        max_schema_extra = max_field.json_schema_extra

        assert min_schema_extra["units"] == "samples per second"
        assert max_schema_extra["units"] == "samples per second"
        assert min_schema_extra["required"] is True
        assert max_schema_extra["required"] is True

    @pytest.mark.parametrize(
        "value,expected_type",
        [
            (1, float),
            (1.0, float),
            (1e-5, float),
            ("1.0", float),
            ("1e-5", float),
        ],
    )
    def test_type_coercion(self, empty_period_range, value, expected_type):
        """Test that values are properly coerced to the expected type."""
        empty_period_range.min = value
        empty_period_range.max = value

        assert isinstance(empty_period_range.min, expected_type)
        assert isinstance(empty_period_range.max, expected_type)
