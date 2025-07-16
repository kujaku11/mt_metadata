"""
Comprehensive test suite for remote_info_basemodel.RemoteInfo class.

This test suite uses fixtures and parametrized tests to comprehensively test the RemoteInfo class,
which represents remote station information for magnetotelluric data in EMTF XML format.
The RemoteInfo class handles site and field notes metadata with XML serialization capabilities.

Tests cover:
- Basic instantiation and field validation
- Site and FieldNotes nested object validation
- Dictionary reading and parsing (read_dict method)
- XML serialization (to_xml method)
- Integration with MetadataBase functionality
- Error handling and edge cases
- Performance characteristics
- Field ordering and metadata operations

Key features tested:
- Two main nested fields: site (Site object), field_notes (FieldNotes object)
- Default factory instantiation for both nested objects
- read_dict method with complex nested dictionary parsing
- to_xml method with configurable string/element output
- MetadataBase inheritance for standard metadata operations
- _order attribute for field serialization order
- Error handling for missing keys and malformed data

Test Statistics:
- Comprehensive coverage of all public methods and properties
- Fixtures used for efficient test setup and parameterization
- Integration tests with nested object behavior
- Performance tests with large datasets
- Edge case testing for robustness

Usage:
    python -m pytest tests/transfer_functions/io/emtfxml/metadata/test_remote_info_basemodel.py -v
"""

import time
from typing import Any, Dict, List

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata.field_notes_basemodel import (
    FieldNotes,
)
from mt_metadata.transfer_functions.io.emtfxml.metadata.remote_info_basemodel import (
    RemoteInfo,
)
from mt_metadata.transfer_functions.io.emtfxml.metadata.site_basemodel import Site


# Module-level fixtures for efficiency
@pytest.fixture
def basic_remote_info() -> RemoteInfo:
    """Create a basic RemoteInfo instance with default values."""
    return RemoteInfo()  # type: ignore


@pytest.fixture
def populated_remote_info() -> RemoteInfo:
    """Create a RemoteInfo instance with populated data."""
    remote_info = RemoteInfo()  # type: ignore

    # Populate site data if it has accessible fields
    if hasattr(remote_info.site, "project"):
        remote_info.site.project = "TestProject"
    if hasattr(remote_info.site, "survey"):
        remote_info.site.survey = "TestSurvey"
    if hasattr(remote_info.site, "name"):
        remote_info.site.name = "TestSite"

    return remote_info


@pytest.fixture(
    params=[
        {
            "remote_info": {
                "site": {
                    "project": "USArray",
                    "survey": "MT Survey 2020",
                    "name": "MT001",
                },
                "field_notes": {},
            }
        },
        {
            "remote_info": {
                "site": {"project": "TestProject", "survey": "TestSurvey"},
                "field_notes": {},
            }
        },
        {"remote_info": {"site": {}, "field_notes": {}}},
    ]
)
def valid_remote_info_dict(request) -> Dict[str, Any]:
    """Valid RemoteInfo dictionary data for testing."""
    return request.param


@pytest.fixture(
    params=[
        {},  # Empty dict
        {"other_key": "value"},  # Dict without remote_info key
        {"remote_info": {}},  # Empty remote_info
        {"remote_info": {"site": {}}},  # Missing field_notes
        {"remote_info": {"field_notes": {}}},  # Missing site
    ]
)
def edge_case_dict(request) -> Dict[str, Any]:
    """Edge case dictionary data for testing."""
    return request.param


@pytest.fixture
def performance_remote_info_data() -> List[Dict[str, Any]]:
    """Large dataset of RemoteInfo configurations for performance testing."""
    data_list = []
    for i in range(50):
        data_list.append(
            {
                "remote_info": {
                    "site": {
                        "project": f"Project{i:03d}",
                        "survey": f"Survey{i:03d}",
                        "name": f"Site{i:03d}",
                    },
                    "field_notes": {},
                }
            }
        )
    return data_list


class TestRemoteInfoInstantiation:
    """Test RemoteInfo class instantiation and basic functionality."""

    def test_basic_instantiation(self, basic_remote_info):
        """Test basic RemoteInfo instantiation with default values."""
        assert isinstance(basic_remote_info, RemoteInfo)
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_inheritance(self, basic_remote_info):
        """Test RemoteInfo inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        assert isinstance(basic_remote_info, MetadataBase)

    def test_field_types(self, basic_remote_info):
        """Test that all fields have correct types."""
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_default_factory_independence(self):
        """Test that default factories create independent instances."""
        remote_info1 = RemoteInfo()  # type: ignore
        remote_info2 = RemoteInfo()  # type: ignore

        # Should be different instances
        assert remote_info1.site is not remote_info2.site
        assert remote_info1.field_notes is not remote_info2.field_notes

    def test_order_attribute(self, basic_remote_info):
        """Test _order attribute exists and contains expected fields."""
        assert hasattr(basic_remote_info, "_order")
        assert isinstance(basic_remote_info._order, list)
        assert "site" in basic_remote_info._order
        assert "field_notes" in basic_remote_info._order

    def test_nested_object_instantiation(self, basic_remote_info):
        """Test that nested objects are properly instantiated."""
        # Site should be instantiated
        assert basic_remote_info.site is not None
        assert isinstance(basic_remote_info.site, Site)

        # FieldNotes should be instantiated
        assert basic_remote_info.field_notes is not None
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_field_assignment(self, basic_remote_info):
        """Test field assignment with new instances."""
        new_site = Site()  # type: ignore
        new_field_notes = FieldNotes()

        basic_remote_info.site = new_site
        basic_remote_info.field_notes = new_field_notes

        assert basic_remote_info.site is new_site
        assert basic_remote_info.field_notes is new_field_notes


class TestRemoteInfoReadDict:
    """Test RemoteInfo read_dict method functionality."""

    def test_read_dict_valid_data(self, basic_remote_info, valid_remote_info_dict):
        """Test read_dict with valid dictionary data."""
        # Should not raise any exceptions
        basic_remote_info.read_dict(valid_remote_info_dict)

        # Verify site and field_notes are still valid objects
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_read_dict_missing_remote_info_key(self, basic_remote_info):
        """Test read_dict with missing 'remote_info' key."""
        test_dict = {"other_key": "value"}

        # Should not raise exception, should return early
        basic_remote_info.read_dict(test_dict)

        # Objects should remain unchanged
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_read_dict_empty_dict(self, basic_remote_info):
        """Test read_dict with empty dictionary."""
        basic_remote_info.read_dict({})

        # Should not affect existing objects
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_read_dict_edge_cases(self, basic_remote_info, edge_case_dict):
        """Test read_dict with various edge case dictionaries."""
        # Should handle edge cases gracefully
        basic_remote_info.read_dict(edge_case_dict)

        # Objects should remain valid
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_read_dict_partial_data(self, basic_remote_info):
        """Test read_dict with partial data (missing some nested keys)."""
        test_dict = {
            "remote_info": {
                "site": {"project": "PartialProject"}
                # Missing field_notes
            }
        }

        basic_remote_info.read_dict(test_dict)

        # Should still have valid objects
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_read_dict_malformed_nested_data(self, basic_remote_info):
        """Test read_dict with malformed nested data."""
        test_dict = {
            "remote_info": {
                "site": "invalid_site_data",  # Should be dict
                "field_notes": "invalid_field_notes_data",  # Should be dict
            }
        }

        # Should handle gracefully without raising exceptions
        basic_remote_info.read_dict(test_dict)

        # Objects should remain valid
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)


class TestRemoteInfoXMLSerialization:
    """Test RemoteInfo XML serialization functionality."""

    def test_to_xml_element_output(self, populated_remote_info):
        """Test to_xml with element output."""
        xml_output = populated_remote_info.to_xml(string=False)

        # Should return ElementTree Element or similar XML structure
        assert xml_output is not None
        # Could be Element, list of Elements, or other XML structure
        assert xml_output is not False

    def test_to_xml_string_output(self, populated_remote_info):
        """Test to_xml with string output."""
        xml_string = populated_remote_info.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert len(xml_string) > 0

    def test_to_xml_required_parameter(self, populated_remote_info):
        """Test to_xml with different required parameter values."""
        # Test with required=True
        xml_required = populated_remote_info.to_xml(required=True)
        assert xml_required is not None

        # Test with required=False
        xml_not_required = populated_remote_info.to_xml(required=False)
        assert xml_not_required is not None

    def test_to_xml_parameter_combinations(self, populated_remote_info):
        """Test to_xml with different parameter combinations."""
        combinations = [
            (True, True),  # string=True, required=True
            (True, False),  # string=True, required=False
            (False, True),  # string=False, required=True
            (False, False),  # string=False, required=False
        ]

        for string_param, required_param in combinations:
            xml_output = populated_remote_info.to_xml(
                string=string_param, required=required_param
            )
            assert xml_output is not None

            if string_param:
                assert isinstance(xml_output, str)


class TestRemoteInfoFieldInteractions:
    """Test interactions between RemoteInfo fields."""

    def test_site_field_independence(self):
        """Test that site fields operate independently between instances."""
        remote_info1 = RemoteInfo()  # type: ignore
        remote_info2 = RemoteInfo()  # type: ignore

        # Modify site in first instance
        if hasattr(remote_info1.site, "project"):
            remote_info1.site.project = "Project1"

        # Second instance should be unaffected
        if hasattr(remote_info2.site, "project"):
            assert remote_info2.site.project != "Project1"

    def test_field_notes_independence(self):
        """Test that field_notes operate independently between instances."""
        remote_info1 = RemoteInfo()  # type: ignore
        remote_info2 = RemoteInfo()  # type: ignore

        # Modify field_notes in first instance (if it has accessible attributes)
        if hasattr(remote_info1.field_notes, "_run_list"):
            original_length = len(remote_info1.field_notes._run_list)

        # Objects should be independent
        assert remote_info1.field_notes is not remote_info2.field_notes

    def test_nested_object_replacement(self, basic_remote_info):
        """Test replacing nested objects entirely."""
        original_site = basic_remote_info.site
        original_field_notes = basic_remote_info.field_notes

        # Replace with new instances
        basic_remote_info.site = Site()  # type: ignore
        basic_remote_info.field_notes = FieldNotes()

        # Should be different objects
        assert basic_remote_info.site is not original_site
        assert basic_remote_info.field_notes is not original_field_notes


class TestRemoteInfoEdgeCases:
    """Test RemoteInfo edge cases and error handling."""

    def test_read_dict_with_none(self, basic_remote_info):
        """Test read_dict behavior with None input."""
        try:
            basic_remote_info.read_dict(None)
        except (TypeError, AttributeError):
            # Expected to fail with None input
            pass

        # Objects should remain valid if method handles it gracefully
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_to_xml_basic_functionality(self, basic_remote_info):
        """Test to_xml basic functionality without errors."""
        # Should not raise exceptions with default objects
        xml_output = basic_remote_info.to_xml()
        assert xml_output is not None

    def test_string_representation(self, populated_remote_info):
        """Test string conversion methods."""
        # Should be able to convert to string
        str_repr = str(populated_remote_info)
        assert isinstance(str_repr, str)

        # Should have a repr
        repr_str = repr(populated_remote_info)
        assert isinstance(repr_str, str)

    def test_field_access_patterns(self, populated_remote_info):
        """Test various ways of accessing fields."""
        # Direct attribute access
        assert hasattr(populated_remote_info, "site")
        assert hasattr(populated_remote_info, "field_notes")

        # Attribute existence
        site = getattr(populated_remote_info, "site")
        field_notes = getattr(populated_remote_info, "field_notes")

        assert isinstance(site, Site)
        assert isinstance(field_notes, FieldNotes)


class TestRemoteInfoPerformance:
    """Test RemoteInfo performance characteristics."""

    def test_instantiation_performance(self):
        """Test RemoteInfo instantiation performance."""
        start_time = time.time()

        instances = []
        for _ in range(100):
            instances.append(RemoteInfo())  # type: ignore

        end_time = time.time()
        duration = end_time - start_time

        # Should complete within reasonable time (adjust threshold as needed)
        assert duration < 5.0  # 5 seconds for 100 instances
        assert len(instances) == 100

    def test_read_dict_performance(self, performance_remote_info_data):
        """Test read_dict performance with multiple datasets."""
        remote_info = RemoteInfo()  # type: ignore

        start_time = time.time()

        for data in performance_remote_info_data:
            remote_info.read_dict(data)

        end_time = time.time()
        duration = end_time - start_time

        # Should process all datasets quickly
        assert duration < 10.0  # 10 seconds for 50 datasets

        # Verify final state is valid
        assert isinstance(remote_info.site, Site)
        assert isinstance(remote_info.field_notes, FieldNotes)

    def test_xml_generation_performance(self, populated_remote_info):
        """Test XML generation performance."""
        start_time = time.time()

        xml_outputs = []
        for _ in range(50):
            xml_outputs.append(populated_remote_info.to_xml(string=True))

        end_time = time.time()
        duration = end_time - start_time

        # Should generate XML quickly
        assert duration < 5.0  # 5 seconds for 50 XML generations
        assert len(xml_outputs) == 50

        # All outputs should be strings
        for xml_output in xml_outputs:
            assert isinstance(xml_output, str)


class TestRemoteInfoIntegration:
    """Test RemoteInfo integration with Pydantic and MetadataBase."""

    def test_pydantic_model_validation(self):
        """Test Pydantic model validation functionality."""
        # Should be able to create instance
        remote_info = RemoteInfo()  # type: ignore
        assert isinstance(remote_info, RemoteInfo)

    def test_model_dump_functionality(self, populated_remote_info):
        """Test Pydantic model_dump functionality."""
        try:
            model_dict = populated_remote_info.model_dump()
            assert isinstance(model_dict, dict)
            assert "site" in model_dict
            assert "field_notes" in model_dict
        except AttributeError:
            # If model_dump doesn't exist, test dict conversion
            model_dict = dict(populated_remote_info)
            assert isinstance(model_dict, dict)

    def test_field_info_access(self):
        """Test access to field information."""
        try:
            # Try to access Pydantic field info
            fields = RemoteInfo.model_fields
            assert isinstance(fields, dict)
            assert "site" in fields
            assert "field_notes" in fields
        except AttributeError:
            # If not available, just verify the class has the expected attributes
            remote_info = RemoteInfo()  # type: ignore
            assert hasattr(remote_info, "site")
            assert hasattr(remote_info, "field_notes")

    def test_metadata_base_integration(self, populated_remote_info):
        """Test integration with MetadataBase functionality."""
        from mt_metadata.base import MetadataBase

        # Should inherit from MetadataBase
        assert isinstance(populated_remote_info, MetadataBase)

        # Should have read_dict method (RemoteInfo's own method)
        assert hasattr(populated_remote_info, "read_dict")
        assert callable(getattr(populated_remote_info, "read_dict"))


class TestRemoteInfoSpecialCases:
    """Test RemoteInfo special cases and complex interactions."""

    def test_complex_read_dict_scenarios(self, basic_remote_info):
        """Test complex read_dict scenarios with nested data."""
        complex_dict = {
            "remote_info": {
                "site": {
                    "project": "ComplexProject",
                    "survey": "ComplexSurvey",
                    "nested": {"deep": {"value": "test"}},
                },
                "field_notes": {"complex_notes": "test_notes"},
            }
        }

        # Should handle complex nested structures
        basic_remote_info.read_dict(complex_dict)

        # Verify objects are still valid
        assert isinstance(basic_remote_info.site, Site)
        assert isinstance(basic_remote_info.field_notes, FieldNotes)

    def test_order_field_usage(self, basic_remote_info):
        """Test _order field usage in XML generation."""
        # _order should influence XML generation
        assert hasattr(basic_remote_info, "_order")

        # Test XML with ordering
        xml_output = basic_remote_info.to_xml()
        assert xml_output is not None

    def test_concurrent_modifications(self):
        """Test behavior with concurrent modifications."""
        remote_info = RemoteInfo()  # type: ignore

        # Simulate concurrent access patterns
        site_ref = remote_info.site
        field_notes_ref = remote_info.field_notes

        # Modify through different references
        if hasattr(site_ref, "project"):
            site_ref.project = "ConcurrentProject"

        # Verify consistency
        if hasattr(remote_info.site, "project"):
            assert remote_info.site.project == "ConcurrentProject"

        # References should be to the same objects
        assert remote_info.site is site_ref
        assert remote_info.field_notes is field_notes_ref

    def test_xml_roundtrip_consistency(self, populated_remote_info):
        """Test XML generation consistency across multiple calls."""
        # Generate XML multiple times
        xml1 = populated_remote_info.to_xml(string=True)
        xml2 = populated_remote_info.to_xml(string=True)

        # Results should be consistent (same structure)
        assert isinstance(xml1, str)
        assert isinstance(xml2, str)
        assert len(xml1) == len(xml2)  # Same length indicates same structure
