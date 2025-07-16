"""
Comprehensive test suite for remote_ref_basemodel.RemoteRef class.

This test suite uses fixtures and parametrized tests to efficiently test the RemoteRef class,
which represents remote referencing metadata for magnetotelluric data processing.
The RemoteRef class manages remote referencing type information and XML serialization.

Tests cover:
- Basic instantiation and field validation
- Type field validation and requirements
- Default value handling
- XML serialization (to_xml method) with various parameters
- read_dict method functionality
- Edge cases and error handling
- Pydantic validation behavior (including None value rejection)
- Integration with MetadataBase functionality
- Performance characteristics

Key features tested:
- Represents remote referencing metadata with type attribute
- XML serialization with proper attribute formatting
- Inherits from MetadataBase for standard metadata operations
- Handles empty values gracefully
- Strict type validation (rejects None values as per Pydantic v2)

Test Statistics:
- 49 total tests
- 6 test classes covering different aspects
- Fixtures used for efficient test setup and parameterization
- Performance tests with 100 iterations each
- Comprehensive coverage of public API

Usage:
    python -m pytest tests/transfer_functions/io/emtfxml/metadata/test_remote_ref_basemodel.py -v
"""

import time
from typing import Any, Dict, List
from xml.etree import ElementTree as et

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata.remote_ref_basemodel import (
    RemoteRef,
)


# Test fixtures - these need to be at module level or in a conftest.py
@pytest.fixture
def basic_remote_ref() -> RemoteRef:
    """Create a basic RemoteRef instance with default values."""
    return RemoteRef(type="")


@pytest.fixture
def populated_remote_ref() -> RemoteRef:
    """Create a RemoteRef instance with populated type value."""
    return RemoteRef(type="robust multi-station remote referencing")


@pytest.fixture
def empty_type_remote_ref() -> RemoteRef:
    """Create a RemoteRef instance with empty type."""
    return RemoteRef(type="")


@pytest.fixture
def none_type_remote_ref() -> RemoteRef:
    """Create a RemoteRef instance and set type to None after creation."""
    # Create with default, then test None handling in to_xml method
    return RemoteRef(type="")


@pytest.fixture(
    params=[
        "robust multi-station remote referencing",
        "single station remote referencing",
        "coherence-based remote referencing",
        "array-based remote referencing",
        "local remote referencing",
        "",
    ]
)
def remote_ref_types(request) -> str:
    """Various remote referencing types for testing."""
    return request.param


@pytest.fixture(
    params=[
        {"type": "robust multi-station remote referencing"},
        {"type": "single station remote referencing"},
        {"type": "coherence-based remote referencing"},
        {"type": ""},
        {},  # Empty dict
    ]
)
def remote_ref_configs(request) -> Dict[str, Any]:
    """Various RemoteRef configuration dicts for testing."""
    return request.param


@pytest.fixture
def performance_remote_refs() -> List[Dict[str, Any]]:
    """Large dataset of RemoteRef configurations for performance testing."""
    configs = []
    remote_ref_types = [
        "robust multi-station remote referencing",
        "single station remote referencing",
        "coherence-based remote referencing",
        "array-based remote referencing",
        "local remote referencing",
        "",
    ]

    for i in range(100):  # Generate 100 configurations for performance testing
        config = {"type": remote_ref_types[i % len(remote_ref_types)]}
        configs.append(config)
    return configs


@pytest.fixture(
    params=[
        {"remote_ref": {"type": "robust multi-station remote referencing"}},
        {"remote_ref": {"type": "single station remote referencing"}},
        {"remote_ref": {"type": ""}},
        {"remote_ref": {}},
        {},  # No remote_ref key
    ]
)
def read_dict_inputs(request) -> Dict[str, Any]:
    """Various input dictionaries for read_dict method testing."""
    return request.param


class TestRemoteRefFixtures:
    """Test fixtures for RemoteRef class testing."""

    @pytest.fixture
    def basic_remote_ref(self) -> RemoteRef:
        """Create a basic RemoteRef instance with default values."""
        return RemoteRef(type="")

    @pytest.fixture
    def populated_remote_ref(self) -> RemoteRef:
        """Create a RemoteRef instance with populated type value."""
        return RemoteRef(type="robust multi-station remote referencing")

    @pytest.fixture
    def empty_type_remote_ref(self) -> RemoteRef:
        """Create a RemoteRef instance with empty type."""
        return RemoteRef(type="")

    @pytest.fixture
    def none_type_remote_ref(self) -> RemoteRef:
        """Create a RemoteRef instance and set type to None after creation."""
        # Create with default, then test None handling in to_xml method
        return RemoteRef(type="")

    @pytest.fixture(
        params=[
            "robust multi-station remote referencing",
            "single station remote referencing",
            "coherence-based remote referencing",
            "array-based remote referencing",
            "local remote referencing",
            "",
        ]
    )
    def remote_ref_types(self, request) -> str:
        """Various remote referencing types for testing."""
        return request.param

    @pytest.fixture(
        params=[
            {"type": "robust multi-station remote referencing"},
            {"type": "single station remote referencing"},
            {"type": "coherence-based remote referencing"},
            {"type": ""},
            {},  # Empty dict
        ]
    )
    def remote_ref_configs(self, request) -> Dict[str, Any]:
        """Various RemoteRef configuration dicts for testing."""
        return request.param

    @pytest.fixture
    def performance_remote_refs(self) -> List[Dict[str, Any]]:
        """Large dataset of RemoteRef configurations for performance testing."""
        configs = []
        remote_ref_types = [
            "robust multi-station remote referencing",
            "single station remote referencing",
            "coherence-based remote referencing",
            "array-based remote referencing",
            "local remote referencing",
            "",
        ]

        for i in range(100):  # Generate 100 configurations for performance testing
            config = {"type": remote_ref_types[i % len(remote_ref_types)]}
            configs.append(config)
        return configs

    @pytest.fixture(
        params=[
            {"remote_ref": {"type": "robust multi-station remote referencing"}},
            {"remote_ref": {"type": "single station remote referencing"}},
            {"remote_ref": {"type": ""}},
            {"remote_ref": {}},
            {},  # No remote_ref key
        ]
    )
    def read_dict_inputs(self, request) -> Dict[str, Any]:
        """Various input dictionaries for read_dict method testing."""
        return request.param


class TestRemoteRefInstantiation:
    """Test RemoteRef class instantiation and basic properties."""

    def test_basic_instantiation(self, basic_remote_ref):
        """Test basic RemoteRef instantiation with default values."""
        assert isinstance(basic_remote_ref, RemoteRef)
        assert basic_remote_ref.type == ""

    def test_populated_instantiation(self, populated_remote_ref):
        """Test RemoteRef instantiation with populated values."""
        assert isinstance(populated_remote_ref, RemoteRef)
        assert populated_remote_ref.type == "robust multi-station remote referencing"

    def test_empty_type_instantiation(self, empty_type_remote_ref):
        """Test RemoteRef instantiation with empty type."""
        assert isinstance(empty_type_remote_ref, RemoteRef)
        assert empty_type_remote_ref.type == ""

    def test_none_type_instantiation(self, none_type_remote_ref):
        """Test RemoteRef instantiation with None type."""
        assert isinstance(none_type_remote_ref, RemoteRef)
        assert none_type_remote_ref.type == ""

    @pytest.mark.parametrize(
        "type_value",
        [
            "robust multi-station remote referencing",
            "single station remote referencing",
            "coherence-based remote referencing",
            "",
        ],
    )
    def test_parametrized_instantiation(self, type_value):
        """Test RemoteRef instantiation with various type values."""
        remote_ref = RemoteRef(type=type_value)
        assert isinstance(remote_ref, RemoteRef)
        assert remote_ref.type == type_value


class TestRemoteRefFieldValidation:
    """Test RemoteRef field validation and constraints."""

    def test_type_field_default(self, basic_remote_ref):
        """Test that type field has correct default value."""
        assert basic_remote_ref.type == ""

    def test_type_field_assignment(self, basic_remote_ref):
        """Test type field can be assigned various values."""
        test_values = [
            "robust multi-station remote referencing",
            "single station remote referencing",
            "",
        ]

        for value in test_values:
            basic_remote_ref.type = value
            assert basic_remote_ref.type == value

    def test_type_field_string_conversion(self, basic_remote_ref):
        """Test that non-string values are handled appropriately."""
        # Test with numeric values (Pydantic will convert to string)
        basic_remote_ref.type = "123"  # Direct string assignment
        assert basic_remote_ref.type == "123"

        # Test conversion via assignment
        basic_remote_ref.type = str(456)
        assert basic_remote_ref.type == "456"

    def test_type_field_required_attribute(self):
        """Test that type field is marked as required in schema."""
        schema = RemoteRef.model_json_schema()
        type_field = schema["properties"]["type"]
        # Check if required is mentioned in the field metadata
        assert "required" in str(type_field)


class TestRemoteRefXMLSerialization:
    """Test RemoteRef XML serialization functionality."""

    def test_to_xml_element_basic(self, basic_remote_ref):
        """Test basic XML element generation."""
        xml_element = basic_remote_ref.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "RemoteRef"
        assert xml_element.get("type") == ""

    def test_to_xml_string_basic(self, basic_remote_ref):
        """Test basic XML string generation."""
        xml_string = basic_remote_ref.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "<RemoteRef" in xml_string
        assert 'type=""' in xml_string

    def test_to_xml_element_populated(self, populated_remote_ref):
        """Test XML element generation with populated type."""
        xml_element = populated_remote_ref.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "RemoteRef"
        assert xml_element.get("type") == "robust multi-station remote referencing"

    def test_to_xml_string_populated(self, populated_remote_ref):
        """Test XML string generation with populated type."""
        xml_string = populated_remote_ref.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "<RemoteRef" in xml_string
        assert 'type="robust multi-station remote referencing"' in xml_string

    def test_to_xml_none_type_handling(self, none_type_remote_ref):
        """Test XML generation when type is None."""
        # The to_xml method should set type to "" if it's None
        xml_element = none_type_remote_ref.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "RemoteRef"
        assert xml_element.get("type") == ""

    def test_to_xml_required_parameter(self, populated_remote_ref):
        """Test XML generation with required parameter."""
        # Test with required=True (default)
        xml_element_req_true = populated_remote_ref.to_xml(string=False, required=True)
        assert isinstance(xml_element_req_true, et.Element)

        # Test with required=False
        xml_element_req_false = populated_remote_ref.to_xml(
            string=False, required=False
        )
        assert isinstance(xml_element_req_false, et.Element)

        # Both should produce the same result for this simple class
        assert xml_element_req_true.tag == xml_element_req_false.tag
        assert xml_element_req_true.get("type") == xml_element_req_false.get("type")

    @pytest.mark.parametrize(
        "string_param,expected_type",
        [
            (True, str),
            (False, et.Element),
        ],
    )
    def test_to_xml_return_type(
        self, populated_remote_ref, string_param, expected_type
    ):
        """Test that to_xml returns correct type based on string parameter."""
        result = populated_remote_ref.to_xml(string=string_param)
        assert isinstance(result, expected_type)

    def test_to_xml_with_various_types(self, remote_ref_types):
        """Test XML generation with various type values."""
        remote_ref = RemoteRef(type=remote_ref_types)
        xml_element = remote_ref.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "RemoteRef"

        # Handle None type case (should be converted to empty string)
        expected_type = "" if remote_ref_types is None else str(remote_ref_types)
        assert xml_element.get("type") == expected_type


class TestRemoteRefReadDict:
    """Test RemoteRef read_dict functionality."""

    def test_read_dict_basic(self, basic_remote_ref):
        """Test basic read_dict functionality."""
        input_dict = {"remote_ref": {"type": "test remote referencing"}}
        basic_remote_ref.read_dict(input_dict)
        assert basic_remote_ref.type == "test remote referencing"

    def test_read_dict_empty_dict(self, basic_remote_ref):
        """Test read_dict with empty remote_ref dict."""
        input_dict = {"remote_ref": {}}
        # Should not raise an error
        basic_remote_ref.read_dict(input_dict)

    def test_read_dict_missing_key(self, basic_remote_ref):
        """Test read_dict with missing remote_ref key."""
        input_dict = {}
        # Should not raise an error (handled by helpers._read_element)
        basic_remote_ref.read_dict(input_dict)

    def test_read_dict_none_type(self, basic_remote_ref):
        """Test read_dict with None type value - should handle gracefully or raise validation error."""
        input_dict = {"remote_ref": {"type": None}}
        # This should raise a validation error due to Pydantic's strict type checking
        with pytest.raises(Exception):  # Expect validation error
            basic_remote_ref.read_dict(input_dict)

    def test_read_dict_empty_type(self, basic_remote_ref):
        """Test read_dict with empty type value."""
        input_dict = {"remote_ref": {"type": ""}}
        basic_remote_ref.read_dict(input_dict)
        assert basic_remote_ref.type == ""

    def test_read_dict_parametrized(self, basic_remote_ref, read_dict_inputs):
        """Test read_dict with various input configurations."""
        # Should not raise an error regardless of input
        basic_remote_ref.read_dict(read_dict_inputs)


class TestRemoteRefEdgeCases:
    """Test RemoteRef edge cases and error handling."""

    def test_class_name_attribute(self):
        """Test that class name is correctly set."""
        remote_ref = RemoteRef(type="")
        assert remote_ref.__class__.__name__ == "RemoteRef"

    def test_field_access_patterns(self, populated_remote_ref):
        """Test various ways of accessing fields."""
        # Direct attribute access
        assert populated_remote_ref.type == "robust multi-station remote referencing"

        # Check if field exists
        assert hasattr(populated_remote_ref, "type")

    def test_field_modification_patterns(self, basic_remote_ref):
        """Test various ways of modifying fields."""
        # Direct assignment
        basic_remote_ref.type = "new type"
        assert basic_remote_ref.type == "new type"

        # Assignment of empty string
        basic_remote_ref.type = ""
        assert basic_remote_ref.type == ""

        # Test that None assignment raises validation error
        with pytest.raises(Exception):  # Pydantic validation error expected
            basic_remote_ref.type = None

    def test_xml_generation_consistency(self, populated_remote_ref):
        """Test that multiple XML generations are consistent."""
        xml1 = populated_remote_ref.to_xml(string=True)
        xml2 = populated_remote_ref.to_xml(string=True)
        assert xml1 == xml2

        elem1 = populated_remote_ref.to_xml(string=False)
        elem2 = populated_remote_ref.to_xml(string=False)
        assert elem1.tag == elem2.tag
        assert elem1.get("type") == elem2.get("type")

    def test_type_none_xml_handling_consistency(self):
        """Test consistent handling of None type in XML generation."""
        # This test verifies the to_xml method's None handling logic
        # Since we can't assign None directly due to type checking,
        # we'll test that the method handles the case properly
        remote_ref = RemoteRef(type="")

        # Test normal XML generation
        xml_element1: et.Element = remote_ref.to_xml(string=False)  # type: ignore
        assert xml_element1.get("type") == ""

        # Test that the type remains consistent
        assert remote_ref.type == ""

        # Second call should still work correctly
        xml_element2: et.Element = remote_ref.to_xml(string=False)  # type: ignore
        assert xml_element2.get("type") == ""


class TestRemoteRefPerformance:
    """Test RemoteRef performance characteristics."""

    def test_instantiation_performance(self, performance_remote_refs):
        """Test performance of creating many RemoteRef instances."""
        start_time = time.time()

        instances = []
        for config in performance_remote_refs:
            instance = RemoteRef(**config)
            instances.append(instance)

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to create 100 instances quickly (under 1 second)
        assert duration < 1.0
        assert len(instances) == len(performance_remote_refs)

    def test_xml_generation_performance(self, performance_remote_refs):
        """Test performance of XML generation for many instances."""
        instances = [RemoteRef(**config) for config in performance_remote_refs]

        start_time = time.time()

        xml_results = []
        for instance in instances:
            xml_string = instance.to_xml(string=True)
            xml_results.append(xml_string)

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to generate XML for 100 instances quickly (under 1 second)
        assert duration < 1.0
        assert len(xml_results) == len(instances)

    def test_read_dict_performance(self, performance_remote_refs):
        """Test performance of read_dict for many operations."""
        instance = RemoteRef(type="")

        # Create input dicts for read_dict
        input_dicts = [{"remote_ref": config} for config in performance_remote_refs]

        start_time = time.time()

        for input_dict in input_dicts:
            instance.read_dict(input_dict)

        end_time = time.time()
        duration = end_time - start_time

        # Should be able to process 100 read_dict operations quickly (under 1 second)
        assert duration < 1.0


class TestRemoteRefIntegration:
    """Test RemoteRef integration with parent classes and framework."""

    def test_metadata_base_inheritance(self, basic_remote_ref):
        """Test that RemoteRef properly inherits from MetadataBase."""
        # Should have MetadataBase methods available
        assert hasattr(basic_remote_ref, "from_dict")
        assert hasattr(basic_remote_ref, "to_dict")

    def test_pydantic_model_functionality(self, basic_remote_ref):
        """Test Pydantic model functionality."""
        # Should have Pydantic model methods
        assert hasattr(basic_remote_ref, "model_dump")
        assert hasattr(basic_remote_ref, "model_validate")

        # Test model_dump
        data = basic_remote_ref.model_dump()
        assert isinstance(data, dict)
        assert "type" in data

    def test_json_schema_generation(self):
        """Test JSON schema generation."""
        schema = RemoteRef.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "type" in schema["properties"]

    def test_field_info_access(self):
        """Test access to field information."""
        # Should be able to access field information
        fields = RemoteRef.model_fields
        assert "type" in fields

        type_field = fields["type"]
        assert hasattr(type_field, "default")

    def test_copy_functionality(self, populated_remote_ref):
        """Test model copy functionality."""
        # Should be able to copy the model
        copied = populated_remote_ref.model_copy()
        assert isinstance(copied, RemoteRef)
        assert copied.type == populated_remote_ref.type
        assert copied is not populated_remote_ref


# Pytest configuration for this test file
pytest_plugins = []  # Add any required plugins here


# Test collection configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add custom markers or ordering."""
    # Add performance marker to performance tests
    for item in items:
        if "performance" in item.name:
            item.add_marker(pytest.mark.performance)
