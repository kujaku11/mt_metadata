"""
Comprehensive test suite for statistical_estimates_basemodel.StatisticalEstimates class.

This test suite uses fixtures and parametrized tests to efficiently test the StatisticalEstimates class,
which manages a collection of statistical estimate objects for magnetotelluric data processing.
The StatisticalEstimates class handles validation, XML serialization, and manipulation of estimate collections.

Tests cover:
- Basic instantiation and field validation
- Estimates list management and validation
- Field validator functionality for estimate processing
- XML serialization (to_xml method) with various parameters
- Dictionary reading (read_dict method) functionality
- Edge cases and error handling
- Integration with Estimate objects
- Performance characteristics
- Collection manipulation and validation

Key features tested:
- Manages a list of Estimate objects or dictionaries
- Validates and converts various input types to Estimate objects
- XML serialization with proper structure and nesting
- Inherits from MetadataBase for standard metadata operations
- Handles empty collections gracefully
- Field validation with automatic type conversion

Test Statistics:
- Comprehensive coverage of all public methods
- Fixtures used for efficient test setup and parameterization
- Performance tests with multiple iterations
- Edge case testing for robustness

Usage:
    python -m pytest tests/transfer_functions/io/emtfxml/metadata/test_statistical_estimates_basemodel.py -v
"""

import time
from typing import Any, Dict, List
from xml.etree import ElementTree as et

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata import (
    Estimate,
    StatisticalEstimates,
)


# Module-level fixtures for efficiency
@pytest.fixture
def basic_statistical_estimates() -> StatisticalEstimates:
    """Create a basic StatisticalEstimates instance with default values."""
    return StatisticalEstimates()  # type: ignore


@pytest.fixture
def sample_estimate_data() -> Dict[str, Any]:
    """Sample estimate data for testing."""
    return {
        "name": "variance",
        "type": "real",
        "description": "Error variance estimate",
        "external_url": "http://example.com/variance",
        "intention": "error estimate",  # Use actual enum value
        "tag": "error",
    }


@pytest.fixture
def sample_estimate(sample_estimate_data) -> Estimate:
    """Create a sample Estimate instance."""
    return Estimate(**sample_estimate_data)


@pytest.fixture
def multiple_estimates_data() -> List[Dict[str, Any]]:
    """Multiple estimate data for testing."""
    return [
        {
            "name": "variance",
            "type": "real",
            "description": "Error variance estimate",
            "external_url": "http://example.com/variance",
            "intention": "error estimate",
            "tag": "error",
        },
        {
            "name": "coherence",
            "type": "real",
            "description": "Signal coherence estimate",
            "external_url": "http://example.com/coherence",
            "intention": "signal coherence",
            "tag": "coherence",
        },
        {
            "name": "covariance",
            "type": "complex",
            "description": "Covariance matrix estimate",
            "external_url": "http://example.com/covariance",
            "intention": "error estimate",
            "tag": "covariance",
        },
    ]


@pytest.fixture
def populated_statistical_estimates(multiple_estimates_data) -> StatisticalEstimates:
    """Create a StatisticalEstimates instance with populated estimates."""
    # Use the field validator to convert dicts to Estimate objects
    return StatisticalEstimates(estimates_list=multiple_estimates_data)


@pytest.fixture
def mixed_estimates_input() -> List[Any]:
    """Mixed input types for estimates list testing."""
    # Use string input since that works well with the field validator
    estimate_string1 = "test_estimate"
    estimate_dict = {
        "name": "dict_estimate",
        "type": "complex",
        "description": "Dictionary estimate",
    }
    estimate_string2 = "string_estimate"
    return [estimate_string1, estimate_dict, estimate_string2]


@pytest.fixture(
    params=[
        [],  # Empty list
        [
            {"name": "single", "type": "real", "description": "Single estimate"}
        ],  # Single dict
        ["string_estimate"],  # Single string
        [
            {"name": "first", "type": "real", "description": "First estimate"},
            {"name": "second", "type": "complex", "description": "Second estimate"},
        ],  # Multiple dicts
    ]
)
def various_estimates_inputs(request) -> List[Any]:
    """Various estimate input configurations for testing."""
    return request.param


@pytest.fixture
def performance_estimates_data() -> List[Dict[str, Any]]:
    """Large dataset of estimate configurations for performance testing."""
    estimates = []
    for i in range(50):
        estimates.append(
            {
                "name": f"estimate_{i:03d}",
                "type": "real" if i % 2 == 0 else "complex",
                "description": f"Performance test estimate {i}",
                "external_url": f"http://example.com/estimate_{i}",
                "intention": "error estimate" if i % 3 == 0 else "signal coherence",
                "tag": f"tag_{i % 5}",
            }
        )
    return estimates


@pytest.fixture
def read_dict_input_data() -> Dict[str, Any]:
    """Sample input data for read_dict method testing."""
    return {
        "statistical_estimates": {
            "estimate": [
                {
                    "name": "variance",
                    "type": "real",
                    "description": "Error variance",
                },
                {
                    "name": "coherence",
                    "type": "real",
                    "description": "Signal coherence",
                },
            ]
        }
    }


class TestStatisticalEstimatesFixtures:
    """Test fixtures for StatisticalEstimates class testing."""

    def test_fixture_availability(
        self, basic_statistical_estimates, sample_estimate_data
    ):
        """Test that fixtures are available and working."""
        assert isinstance(basic_statistical_estimates, StatisticalEstimates)
        assert isinstance(sample_estimate_data, dict)
        assert "name" in sample_estimate_data


class TestStatisticalEstimatesInstantiation:
    """Test StatisticalEstimates class instantiation and basic functionality."""

    def test_basic_instantiation(self, basic_statistical_estimates):
        """Test basic StatisticalEstimates instantiation with default values."""
        assert isinstance(basic_statistical_estimates, StatisticalEstimates)
        assert isinstance(basic_statistical_estimates.estimates_list, list)
        assert len(basic_statistical_estimates.estimates_list) == 0

    def test_populated_instantiation(self, populated_statistical_estimates):
        """Test StatisticalEstimates instantiation with populated estimates."""
        assert isinstance(populated_statistical_estimates, StatisticalEstimates)
        assert len(populated_statistical_estimates.estimates_list) == 3
        for estimate in populated_statistical_estimates.estimates_list:
            assert isinstance(estimate, Estimate)

    def test_inheritance_from_metadata_base(self, basic_statistical_estimates):
        """Test that StatisticalEstimates properly inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        assert isinstance(basic_statistical_estimates, MetadataBase)

        # Should have MetadataBase methods
        expected_methods = ["model_dump", "model_dump_json"]
        for method in expected_methods:
            assert hasattr(basic_statistical_estimates, method)

    def test_field_types(self, basic_statistical_estimates):
        """Test that all fields have correct types."""
        assert isinstance(basic_statistical_estimates.estimates_list, list)

    def test_field_defaults(self, basic_statistical_estimates):
        """Test that field defaults are properly set."""
        # estimates_list should default to empty list
        assert basic_statistical_estimates.estimates_list == []

    def test_model_dump_behavior(
        self, basic_statistical_estimates, populated_statistical_estimates
    ):
        """Test model_dump method behavior."""
        # Basic instance should dump with empty list
        basic_dump = basic_statistical_estimates.model_dump()
        assert isinstance(basic_dump, dict)
        assert "estimates_list" in basic_dump
        assert basic_dump["estimates_list"] == []

        # Populated instance
        populated_dump = populated_statistical_estimates.model_dump()
        assert isinstance(populated_dump, dict)
        assert "estimates_list" in populated_dump
        assert len(populated_dump["estimates_list"]) == 3

    @pytest.mark.parametrize(
        "estimates_input",
        [
            [],
            [{"name": "test", "type": "real", "description": "Test"}],
            ["string_estimate"],
        ],
    )
    def test_parametrized_instantiation(self, estimates_input):
        """Test StatisticalEstimates instantiation with various estimate inputs."""
        stat_est = StatisticalEstimates(estimates_list=estimates_input)
        assert isinstance(stat_est, StatisticalEstimates)
        assert len(stat_est.estimates_list) == len(estimates_input)


class TestStatisticalEstimatesFieldValidation:
    """Test StatisticalEstimates field validation and assignment."""

    def test_estimates_list_empty_assignment(self, basic_statistical_estimates):
        """Test assignment of empty estimates list."""
        basic_statistical_estimates.estimates_list = []
        assert basic_statistical_estimates.estimates_list == []

    def test_estimates_list_dict_assignment(self, basic_statistical_estimates):
        """Test assignment of dictionary to estimates list."""
        test_dict = {"name": "test", "type": "real", "description": "Test estimate"}
        basic_statistical_estimates.estimates_list = [test_dict]

        assert len(basic_statistical_estimates.estimates_list) == 1
        assert isinstance(basic_statistical_estimates.estimates_list[0], Estimate)  # type: ignore
        assert basic_statistical_estimates.estimates_list[0].name == "test"  # type: ignore

    def test_estimates_list_estimate_object_assignment(
        self, basic_statistical_estimates, sample_estimate
    ):
        """Test assignment of Estimate objects to estimates list."""
        basic_statistical_estimates.estimates_list = [sample_estimate]

        assert len(basic_statistical_estimates.estimates_list) == 1
        assert isinstance(basic_statistical_estimates.estimates_list[0], Estimate)  # type: ignore
        assert basic_statistical_estimates.estimates_list[0].name == sample_estimate.name  # type: ignore

    def test_estimates_list_string_assignment(self, basic_statistical_estimates):
        """Test assignment of strings to estimates list."""
        basic_statistical_estimates.estimates_list = ["string_estimate"]

        assert len(basic_statistical_estimates.estimates_list) == 1
        assert isinstance(basic_statistical_estimates.estimates_list[0], Estimate)  # type: ignore
        assert basic_statistical_estimates.estimates_list[0].name == "string_estimate"  # type: ignore

    def test_estimates_list_mixed_assignment(
        self, basic_statistical_estimates, mixed_estimates_input
    ):
        """Test assignment of mixed types to estimates list."""
        basic_statistical_estimates.estimates_list = mixed_estimates_input

        assert len(basic_statistical_estimates.estimates_list) == 3
        for estimate in basic_statistical_estimates.estimates_list:
            assert isinstance(estimate, Estimate)  # type: ignore

    def test_estimates_list_single_value_conversion(self, basic_statistical_estimates):
        """Test that single non-list values are converted to list."""
        # Single dict
        test_dict = {"name": "single", "type": "real", "description": "Single estimate"}
        basic_statistical_estimates.estimates_list = test_dict  # type: ignore

        assert len(basic_statistical_estimates.estimates_list) == 1
        assert isinstance(basic_statistical_estimates.estimates_list[0], Estimate)  # type: ignore

    def test_field_validator_with_various_inputs(self, various_estimates_inputs):
        """Test field validator with various input configurations."""
        stat_est = StatisticalEstimates(estimates_list=various_estimates_inputs)

        assert len(stat_est.estimates_list) == len(various_estimates_inputs)
        for estimate in stat_est.estimates_list:
            assert isinstance(estimate, Estimate)  # type: ignore

    def test_estimates_list_modification(self, populated_statistical_estimates):
        """Test modification of estimates list after instantiation."""
        original_length = len(populated_statistical_estimates.estimates_list)

        # Add a new estimate using string (which works with the validator)
        populated_statistical_estimates.estimates_list.append("new_estimate")  # type: ignore

        assert (
            len(populated_statistical_estimates.estimates_list) == original_length + 1
        )
        # Note: This test shows the limitation - appending doesn't trigger the validator
        # so we get a string instead of an Estimate object


class TestStatisticalEstimatesXMLSerialization:
    """Test StatisticalEstimates XML serialization functionality."""

    def test_to_xml_element_basic(self, basic_statistical_estimates):
        """Test basic XML element generation."""
        xml_element = basic_statistical_estimates.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "StatisticalEstimates"
        assert len(xml_element) == 0  # No child elements for empty list

    def test_to_xml_string_basic(self, basic_statistical_estimates):
        """Test basic XML string generation."""
        xml_string = basic_statistical_estimates.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "<StatisticalEstimates" in xml_string
        # For empty elements, XML can be either self-closing or with closing tag
        assert (
            "</StatisticalEstimates>" in xml_string
            or "<StatisticalEstimates/>" in xml_string
        )

    def test_to_xml_element_populated(self, populated_statistical_estimates):
        """Test XML element generation with populated estimates."""
        xml_element = populated_statistical_estimates.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "StatisticalEstimates"
        assert len(xml_element) == 3  # Should have 3 child elements

        # Check that child elements are Estimate XML elements
        for child in xml_element:
            assert child.tag == "Estimate"

    def test_to_xml_string_populated(self, populated_statistical_estimates):
        """Test XML string generation with populated estimates."""
        xml_string = populated_statistical_estimates.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "<StatisticalEstimates" in xml_string
        assert "</StatisticalEstimates>" in xml_string
        assert "<Estimate" in xml_string
        assert "</Estimate>" in xml_string

    def test_to_xml_required_parameter(self, populated_statistical_estimates):
        """Test XML generation with required parameter."""
        # Test with required=True (default)
        xml_element_req_true = populated_statistical_estimates.to_xml(
            string=False, required=True
        )
        assert isinstance(xml_element_req_true, et.Element)

        # Test with required=False
        xml_element_req_false = populated_statistical_estimates.to_xml(
            string=False, required=False
        )
        assert isinstance(xml_element_req_false, et.Element)

        # Both should have the same structure for this class
        assert xml_element_req_true.tag == xml_element_req_false.tag
        assert len(xml_element_req_true) == len(xml_element_req_false)

    @pytest.mark.parametrize(
        "string_param,expected_type",
        [
            (True, str),
            (False, et.Element),
        ],
    )
    def test_to_xml_return_type(
        self, populated_statistical_estimates, string_param, expected_type
    ):
        """Test that to_xml returns correct type based on string parameter."""
        result = populated_statistical_estimates.to_xml(string=string_param)
        assert isinstance(result, expected_type)

    def test_to_xml_empty_vs_populated(
        self, basic_statistical_estimates, populated_statistical_estimates
    ):
        """Test XML generation differences between empty and populated instances."""
        empty_xml = basic_statistical_estimates.to_xml(string=False)
        populated_xml = populated_statistical_estimates.to_xml(string=False)

        assert empty_xml.tag == populated_xml.tag
        assert len(empty_xml) == 0
        assert len(populated_xml) > 0

    def test_xml_generation_consistency(self, populated_statistical_estimates):
        """Test that multiple XML generations are consistent."""
        xml1 = populated_statistical_estimates.to_xml(string=True)
        xml2 = populated_statistical_estimates.to_xml(string=True)
        assert xml1 == xml2

        elem1 = populated_statistical_estimates.to_xml(string=False)
        elem2 = populated_statistical_estimates.to_xml(string=False)
        assert elem1.tag == elem2.tag
        assert len(elem1) == len(elem2)

    def test_to_xml_with_single_estimate(self, sample_estimate):
        """Test XML generation with a single estimate."""
        stat_est = StatisticalEstimates(estimates_list=[sample_estimate])
        xml_element = stat_est.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "StatisticalEstimates"
        assert len(xml_element) == 1
        assert xml_element[0].tag == "Estimate"


class TestStatisticalEstimatesReadDict:
    """Test StatisticalEstimates read_dict functionality."""

    def test_read_dict_basic(self, basic_statistical_estimates, read_dict_input_data):
        """Test basic read_dict functionality."""
        basic_statistical_estimates.read_dict(read_dict_input_data)

        assert len(basic_statistical_estimates.estimates_list) == 2
        for estimate in basic_statistical_estimates.estimates_list:
            assert isinstance(estimate, Estimate)

    def test_read_dict_with_valid_data(self, basic_statistical_estimates):
        """Test read_dict with valid input data."""
        input_data = {
            "statistical_estimates": {
                "estimate": [
                    {
                        "name": "variance",
                        "type": "real",
                        "description": "Error variance",
                    },
                    {
                        "name": "coherence",
                        "type": "real",
                        "description": "Signal coherence",
                    },
                ]
            }
        }

        basic_statistical_estimates.read_dict(input_data)

        assert len(basic_statistical_estimates.estimates_list) == 2
        assert basic_statistical_estimates.estimates_list[0].name == "variance"
        assert basic_statistical_estimates.estimates_list[1].name == "coherence"

    def test_read_dict_missing_key(self, basic_statistical_estimates):
        """Test read_dict with missing key (should not raise error)."""
        input_data = {"other_data": {}}

        # Should not raise an error, but should log a warning
        basic_statistical_estimates.read_dict(input_data)

        # estimates_list should remain unchanged (empty)
        assert len(basic_statistical_estimates.estimates_list) == 0

    def test_read_dict_empty_estimates(self, basic_statistical_estimates):
        """Test read_dict with empty estimates list."""
        input_data = {"statistical_estimates": {"estimate": []}}

        basic_statistical_estimates.read_dict(input_data)
        assert len(basic_statistical_estimates.estimates_list) == 0

    def test_read_dict_single_estimate(self, basic_statistical_estimates):
        """Test read_dict with single estimate."""
        input_data = {
            "statistical_estimates": {
                "estimate": {
                    "name": "single",
                    "type": "real",
                    "description": "Single estimate",
                }
            }
        }

        basic_statistical_estimates.read_dict(input_data)
        assert len(basic_statistical_estimates.estimates_list) == 1
        assert basic_statistical_estimates.estimates_list[0].name == "single"

    def test_read_dict_partial_data(self, basic_statistical_estimates):
        """Test read_dict with partial estimate data."""
        input_data = {
            "statistical_estimates": {
                "estimate": [
                    {"name": "incomplete"},  # Missing other fields
                ]
            }
        }

        basic_statistical_estimates.read_dict(input_data)
        assert len(basic_statistical_estimates.estimates_list) == 1
        assert basic_statistical_estimates.estimates_list[0].name == "incomplete"

    @pytest.mark.parametrize(
        "estimate_data",
        [
            [{"name": "test1", "type": "real"}],
            [{"name": "test2", "type": "complex"}, {"name": "test3", "type": "real"}],
            {"name": "single_dict", "type": "real"},
        ],
    )
    def test_read_dict_parametrized(self, basic_statistical_estimates, estimate_data):
        """Test read_dict with various estimate data configurations."""
        input_data = {"statistical_estimates": {"estimate": estimate_data}}

        basic_statistical_estimates.read_dict(input_data)

        expected_length = len(estimate_data) if isinstance(estimate_data, list) else 1
        assert len(basic_statistical_estimates.estimates_list) == expected_length


class TestStatisticalEstimatesEdgeCases:
    """Test StatisticalEstimates edge cases and error handling."""

    def test_class_name_attribute(self):
        """Test that class name is correctly set."""
        stat_est = StatisticalEstimates()  # type: ignore
        assert stat_est.__class__.__name__ == "StatisticalEstimates"

    def test_field_access_patterns(self, populated_statistical_estimates):
        """Test various ways of accessing fields."""
        # Direct attribute access
        assert isinstance(populated_statistical_estimates.estimates_list, list)
        assert len(populated_statistical_estimates.estimates_list) > 0

        # Check if field exists
        assert hasattr(populated_statistical_estimates, "estimates_list")

    def test_field_modification_patterns(self, basic_statistical_estimates):
        """Test various ways of modifying fields."""
        # Direct assignment with list - use dictionaries that will be converted to Estimate objects
        test_estimate_dicts = [
            {"name": "test1", "type": "real", "description": "Test 1"},
            {"name": "test2", "type": "complex", "description": "Test 2"},
        ]
        basic_statistical_estimates.estimates_list = test_estimate_dicts
        assert len(basic_statistical_estimates.estimates_list) == 2

        # Clear the list
        basic_statistical_estimates.estimates_list = []
        assert len(basic_statistical_estimates.estimates_list) == 0

    def test_copy_and_modify(self, populated_statistical_estimates):
        """Test copying and modifying instances."""
        # Use Pydantic's model_copy method
        copied = populated_statistical_estimates.model_copy()
        assert len(copied.estimates_list) == len(
            populated_statistical_estimates.estimates_list
        )

        # Modify copy
        copied.estimates_list = []

        # Original should be unchanged
        assert len(populated_statistical_estimates.estimates_list) == 3

        # Copy should be changed
        assert len(copied.estimates_list) == 0

    def test_estimates_list_type_preservation(self, basic_statistical_estimates):
        """Test that estimates_list maintains proper types."""
        # Add various types and ensure they're all converted to Estimate
        mixed_inputs = [
            {"name": "dict_est", "type": "real"},
            "string_est",
        ]

        basic_statistical_estimates.estimates_list = mixed_inputs

        for estimate in basic_statistical_estimates.estimates_list:
            assert isinstance(estimate, Estimate)  # type: ignore

    def test_empty_list_operations(self, basic_statistical_estimates):
        """Test operations on empty estimates list."""
        # Should handle empty list gracefully
        xml_element = basic_statistical_estimates.to_xml(string=False)
        assert len(xml_element) == 0

        # Should handle model_dump with empty list
        dump_data = basic_statistical_estimates.model_dump()
        assert dump_data["estimates_list"] == []


class TestStatisticalEstimatesPerformance:
    """Test StatisticalEstimates performance characteristics."""

    def test_instantiation_performance(self, performance_estimates_data):
        """Test performance of creating StatisticalEstimates with many estimates."""
        start_time = time.time()

        # Use the data directly - field validator will create Estimate objects
        stat_est = StatisticalEstimates(estimates_list=performance_estimates_data)

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to create instance with 50 estimates quickly (under 1 second)
        assert duration < 1.0
        assert len(stat_est.estimates_list) == 50

    def test_xml_generation_performance(self, performance_estimates_data):
        """Test performance of XML generation for many estimates."""
        stat_est = StatisticalEstimates(estimates_list=performance_estimates_data)

        start_time = time.time()

        xml_string = stat_est.to_xml(string=True)

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to generate XML for 50 estimates quickly (under 1 second)
        assert duration < 1.0
        assert isinstance(xml_string, str)
        assert "<StatisticalEstimates" in xml_string

    def test_field_validation_performance(self, performance_estimates_data):
        """Test performance of field validation for many estimates."""
        start_time = time.time()

        # Test direct assignment which triggers field validation
        stat_est = StatisticalEstimates(estimates_list=[])
        stat_est.estimates_list = (
            performance_estimates_data  # This will trigger validation
        )

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to validate 50 estimates quickly (under 1 second)
        assert duration < 1.0
        assert len(stat_est.estimates_list) == 50

    def test_read_dict_performance(self, performance_estimates_data):
        """Test performance of read_dict for many estimates."""
        input_data = {"statistical_estimates": {"estimate": performance_estimates_data}}
        stat_est = StatisticalEstimates(estimates_list=[])

        start_time = time.time()

        stat_est.read_dict(input_data)

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to read 50 estimates quickly (under 1 second)
        assert duration < 1.0
        assert len(stat_est.estimates_list) == 50


class TestStatisticalEstimatesIntegration:
    """Test StatisticalEstimates integration with parent classes and framework."""

    def test_metadata_base_inheritance(self, basic_statistical_estimates):
        """Test that StatisticalEstimates properly inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        assert isinstance(basic_statistical_estimates, MetadataBase)

        # Should have MetadataBase methods available
        assert hasattr(basic_statistical_estimates, "model_dump")
        assert hasattr(basic_statistical_estimates, "model_dump_json")
        assert hasattr(basic_statistical_estimates, "model_copy")

    def test_pydantic_model_functionality(self, basic_statistical_estimates):
        """Test Pydantic model functionality."""
        # Should have Pydantic model methods
        assert hasattr(basic_statistical_estimates, "model_validate")
        assert hasattr(basic_statistical_estimates, "model_fields")

        # Test model_dump
        data = basic_statistical_estimates.model_dump()
        assert isinstance(data, dict)
        assert "estimates_list" in data

    def test_json_schema_generation(self):
        """Test JSON schema generation."""
        schema = StatisticalEstimates.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "estimates_list" in schema["properties"]

    def test_field_info_access(self):
        """Test access to field information."""
        # Should be able to access field information
        fields = StatisticalEstimates.model_fields
        assert "estimates_list" in fields

        estimates_list_field = fields["estimates_list"]
        assert hasattr(estimates_list_field, "default_factory")

    def test_model_validation(self, sample_estimate_data):
        """Test model validation functionality."""
        # Valid data should validate
        valid_data = {"estimates_list": [sample_estimate_data]}
        stat_est = StatisticalEstimates.model_validate(valid_data)
        assert isinstance(stat_est, StatisticalEstimates)
        assert len(stat_est.estimates_list) == 1

    def test_copy_functionality(self, populated_statistical_estimates):
        """Test model copy functionality."""
        # Should be able to copy the model
        copied = populated_statistical_estimates.model_copy()
        assert isinstance(copied, StatisticalEstimates)
        assert len(copied.estimates_list) == len(
            populated_statistical_estimates.estimates_list
        )
        assert copied is not populated_statistical_estimates

        # Test copy with updates
        updated_copy = populated_statistical_estimates.model_copy(
            update={"estimates_list": []}
        )
        assert len(updated_copy.estimates_list) == 0
        assert (
            len(populated_statistical_estimates.estimates_list) == 3
        )  # Original unchanged

    def test_json_serialization(self, populated_statistical_estimates):
        """Test JSON serialization functionality."""
        # Test JSON dump
        json_str = populated_statistical_estimates.model_dump_json()
        assert isinstance(json_str, str)

        # Should be valid JSON
        import json

        data = json.loads(json_str)
        assert "estimates_list" in data
        assert len(data["estimates_list"]) == 3

    def test_estimate_integration(self, sample_estimate):
        """Test integration with Estimate objects."""
        # Should work seamlessly with Estimate objects
        stat_est = StatisticalEstimates(estimates_list=[sample_estimate])

        # Should preserve Estimate object properties
        first_estimate = stat_est.estimates_list[0]  # type: ignore
        assert first_estimate.name == sample_estimate.name  # type: ignore
        assert first_estimate.type == sample_estimate.type  # type: ignore

        # Should be able to call Estimate methods through the list
        xml_element = first_estimate.to_xml()  # type: ignore
        assert isinstance(xml_element, et.Element)


# Pytest configuration for this test file
pytest_plugins = []  # Add any required plugins here


# Test collection configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add custom markers or ordering."""
    # Add performance marker to performance tests
    for item in items:
        if "performance" in item.name:
            item.add_marker(pytest.mark.performance)
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
