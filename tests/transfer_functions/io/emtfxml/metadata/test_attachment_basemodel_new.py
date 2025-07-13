#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for Attachment basemodel class.

This test suite covers all functionality of the mt_metadata Attachment basemodel
using modern pytest idioms, fixtures, and parametrization for maximum efficiency.

Created on July 13, 2025
@author: mt_metadata_pytest_suite
"""

from xml.etree import cElementTree as et

# =============================================================================
# Imports
# =============================================================================
import pytest

# Import the Attachment class directly to avoid circular imports
from mt_metadata.transfer_functions.io.emtfxml.metadata.attachment_basemodel import (
    Attachment,
)


# =============================================================================
# Test Data Constants
# =============================================================================

VALID_FILENAME_CASES = [
    "test.zmm",
    "data_file.edi",
    "measurement.txt",
    "experiment_2024.dat",
    "",  # empty string is allowed
]

VALID_DESCRIPTION_CASES = [
    "Original measurement data",
    "The original used to produce the XML",
    "Processed transfer function data",
    "Backup of raw field measurements",
    "",  # empty string is allowed
]

INVALID_FIELD_CASES = [
    (None, "filename cannot be None"),
    (True, "filename must be string"),
    ([], "filename must be string"),
    ({}, "filename must be string"),
]


# =============================================================================
# Core Fixtures
# =============================================================================


@pytest.fixture(scope="session")
def basic_attachment_data():
    """Basic attachment data for testing."""
    return {"filename": "test_data.zmm", "description": "Test measurement file"}


@pytest.fixture(scope="session")
def complex_attachment_data():
    """Complex attachment data for comprehensive testing."""
    return {
        "filename": "complex_experiment_2024.edi",
        "description": "Complete magnetotelluric experiment data with full processing chain",
    }


@pytest.fixture
def basic_attachment(basic_attachment_data):
    """Create a basic attachment instance."""
    return Attachment(**basic_attachment_data)


@pytest.fixture
def empty_attachment():
    """Create an attachment with empty/default values."""
    return Attachment(filename="", description="")


@pytest.fixture
def complex_attachment(complex_attachment_data):
    """Create a complex attachment instance."""
    return Attachment(**complex_attachment_data)


@pytest.fixture(scope="session")
def attachment_dict_single():
    """Single attachment dictionary for read_dict testing."""
    return {
        "Attachment": {
            "filename": "single_file.zmm",
            "description": "Single attachment test data",
        }
    }


@pytest.fixture(scope="session")
def attachment_dict_list():
    """Multiple attachments dictionary for read_dict testing."""
    return {
        "Attachment": [
            {"filename": "file1.zmm", "description": "First attachment"},
            {"filename": "file2.edi", "description": "Second attachment"},
            {"filename": "file3.dat", "description": "Third attachment"},
        ]
    }


@pytest.fixture(scope="session")
def attachment_dict_none():
    """None attachment dictionary for edge case testing."""
    return {"Attachment": None}


# =============================================================================
# Test Classes
# =============================================================================


class TestAttachmentInstantiation:
    """Test Attachment object creation and basic properties."""

    def test_default_creation(self):
        """Test creating attachment with default values."""
        attachment = Attachment(filename="", description="")
        assert attachment.filename == ""
        assert attachment.description == ""
        assert attachment._attachments == []

    def test_basic_creation(self, basic_attachment_data):
        """Test creating attachment with basic data."""
        attachment = Attachment(**basic_attachment_data)
        assert attachment.filename == basic_attachment_data["filename"]
        assert attachment.description == basic_attachment_data["description"]
        assert attachment._attachments == []

    @pytest.mark.parametrize("filename", VALID_FILENAME_CASES)
    def test_valid_filename_values(self, filename):
        """Test attachment creation with various valid filename values."""
        attachment = Attachment(filename=filename, description="test")
        assert attachment.filename == filename

    @pytest.mark.parametrize("description", VALID_DESCRIPTION_CASES)
    def test_valid_description_values(self, description):
        """Test attachment creation with various valid description values."""
        attachment = Attachment(filename="test.zmm", description=description)
        assert attachment.description == description

    def test_model_fields_exist(self, basic_attachment):
        """Test that required model fields are present."""
        assert hasattr(basic_attachment, "model_fields")
        fields = basic_attachment.model_fields
        assert "filename" in fields
        assert "description" in fields

    def test_private_attributes(self, basic_attachment):
        """Test private attributes are properly initialized."""
        assert hasattr(basic_attachment, "_attachments")
        assert isinstance(basic_attachment._attachments, list)


class TestAttachmentValidation:
    """Test field validation and error handling."""

    @pytest.mark.parametrize("invalid_value,expected_error", INVALID_FIELD_CASES)
    def test_invalid_filename_types(self, invalid_value, expected_error):
        """Test that invalid filename types raise appropriate errors."""
        with pytest.raises((ValueError, TypeError)):
            Attachment(filename=invalid_value, description="test")

    @pytest.mark.parametrize("invalid_value,expected_error", INVALID_FIELD_CASES)
    def test_invalid_description_types(self, invalid_value, expected_error):
        """Test that invalid description types raise appropriate errors."""
        with pytest.raises((ValueError, TypeError)):
            Attachment(filename="test.zmm", description=invalid_value)

    def test_field_constraints(self, basic_attachment):
        """Test field constraints and metadata."""
        fields = basic_attachment.model_fields

        # Check filename field
        filename_field = fields["filename"]
        assert filename_field.default == ""
        assert filename_field.json_schema_extra["required"] is True

        # Check description field
        description_field = fields["description"]
        assert description_field.default == ""
        assert description_field.json_schema_extra["required"] is True


class TestAttachmentEquality:
    """Test attachment equality and comparison operations."""

    def test_equal_attachments(self, basic_attachment_data):
        """Test that identical attachments are equal."""
        attachment1 = Attachment(**basic_attachment_data)
        attachment2 = Attachment(**basic_attachment_data)
        assert attachment1.filename == attachment2.filename
        assert attachment1.description == attachment2.description

    def test_different_attachments(
        self, basic_attachment_data, complex_attachment_data
    ):
        """Test that different attachments are not equal."""
        attachment1 = Attachment(**basic_attachment_data)
        attachment2 = Attachment(**complex_attachment_data)
        assert attachment1.filename != attachment2.filename
        assert attachment1.description != attachment2.description

    def test_empty_vs_basic(self, basic_attachment, empty_attachment):
        """Test comparison between empty and basic attachments."""
        assert basic_attachment.filename != empty_attachment.filename
        assert basic_attachment.description != empty_attachment.description


class TestAttachmentReadDict:
    """Test the read_dict functionality for various input formats."""

    def test_read_dict_single(self, attachment_dict_single):
        """Test reading a single attachment from dictionary."""
        attachment = Attachment(filename="", description="")
        attachment.read_dict(attachment_dict_single)

        expected = attachment_dict_single["Attachment"]
        assert attachment.filename == expected["filename"]
        assert attachment.description == expected["description"]

    def test_read_dict_list(self, attachment_dict_list):
        """Test reading multiple attachments from dictionary."""
        attachment = Attachment(filename="", description="")
        attachment.read_dict(attachment_dict_list)

        # Should populate _attachments list
        expected_list = attachment_dict_list["Attachment"]
        assert len(attachment._attachments) == len(expected_list)

        for i, expected in enumerate(expected_list):
            actual = attachment._attachments[i]
            assert actual.filename == expected["filename"]
            assert actual.description == expected["description"]

    def test_read_dict_none(self, attachment_dict_none):
        """Test reading None attachment (edge case)."""
        attachment = Attachment(filename="", description="")
        original_filename = attachment.filename
        original_description = attachment.description

        attachment.read_dict(attachment_dict_none)

        # Values should remain unchanged when input is None
        assert attachment.filename == original_filename
        assert attachment.description == original_description

    def test_read_dict_empty_input(self):
        """Test reading from empty or malformed dictionary."""
        attachment = Attachment(filename="", description="")

        # Test with empty dict
        with pytest.raises(KeyError):
            attachment.read_dict({})

        # Test with missing Attachment key
        with pytest.raises(KeyError):
            attachment.read_dict({"OtherKey": "value"})


class TestAttachmentXMLConversion:
    """Test XML serialization and deserialization."""

    def test_to_xml_basic(self, basic_attachment):
        """Test basic XML conversion."""
        xml_element = basic_attachment.to_xml()

        # Should return Element when string=False (default)
        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Attachment"

    def test_to_xml_string(self, basic_attachment):
        """Test XML conversion to string format."""
        xml_string = basic_attachment.to_xml(string=True)

        # Should return string when string=True
        assert isinstance(xml_string, str)
        assert "<Attachment>" in xml_string
        assert basic_attachment.filename in xml_string
        assert basic_attachment.description in xml_string

    def test_to_xml_empty(self, empty_attachment):
        """Test XML conversion of empty attachment."""
        xml_element = empty_attachment.to_xml()

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Attachment"

    def test_to_xml_with_attachments_list(self):
        """Test XML conversion when _attachments list is populated."""
        main_attachment = Attachment(filename="", description="")

        # Add items to _attachments list
        attachment1 = Attachment(filename="file1.zmm", description="First file")
        attachment2 = Attachment(filename="file2.edi", description="Second file")
        main_attachment._attachments = [attachment1, attachment2]

        xml_result = main_attachment.to_xml()

        # Should return list when _attachments is not empty
        assert isinstance(xml_result, list)
        assert len(xml_result) == 2

        for item in xml_result:
            assert isinstance(item, et.Element)
            assert item.tag == "Attachment"

    def test_to_xml_required_parameter(self, basic_attachment):
        """Test XML conversion with required parameter variations."""
        # Test with required=True (default)
        xml_required = basic_attachment.to_xml(required=True)
        assert isinstance(xml_required, et.Element)

        # Test with required=False
        xml_not_required = basic_attachment.to_xml(required=False)
        assert isinstance(xml_not_required, et.Element)

    @pytest.mark.parametrize("string_param", [True, False])
    @pytest.mark.parametrize("required_param", [True, False])
    def test_to_xml_parameter_combinations(
        self, basic_attachment, string_param, required_param
    ):
        """Test all combinations of to_xml parameters."""
        result = basic_attachment.to_xml(string=string_param, required=required_param)

        if string_param:
            assert isinstance(result, str)
        else:
            assert isinstance(result, et.Element)


class TestAttachmentSerialization:
    """Test various serialization methods."""

    def test_dict_conversion(self, basic_attachment):
        """Test conversion to dictionary format."""
        attachment_dict = basic_attachment.model_dump()

        assert isinstance(attachment_dict, dict)
        assert "filename" in attachment_dict
        assert "description" in attachment_dict
        assert attachment_dict["filename"] == basic_attachment.filename
        assert attachment_dict["description"] == basic_attachment.description

    def test_json_conversion(self, basic_attachment):
        """Test JSON serialization."""
        json_str = basic_attachment.model_dump_json()

        assert isinstance(json_str, str)
        assert basic_attachment.filename in json_str
        assert basic_attachment.description in json_str

    def test_round_trip_dict(self, basic_attachment_data):
        """Test dictionary round-trip conversion."""
        original = Attachment(**basic_attachment_data)
        attachment_dict = original.model_dump()
        reconstructed = Attachment(**attachment_dict)

        assert original.filename == reconstructed.filename
        assert original.description == reconstructed.description


class TestAttachmentEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_filename(self):
        """Test with very long filename."""
        long_filename = "a" * 1000 + ".zmm"
        attachment = Attachment(filename=long_filename, description="test")
        assert attachment.filename == long_filename

    def test_very_long_description(self):
        """Test with very long description."""
        long_description = "This is a very long description. " * 100
        attachment = Attachment(filename="test.zmm", description=long_description)
        assert attachment.description == long_description

    def test_special_characters_in_fields(self):
        """Test with special characters in filename and description."""
        special_filename = "test@#$%^&*()_+.zmm"
        special_description = "Description with special chars: äöü ñ 中文 🎉"

        attachment = Attachment(
            filename=special_filename, description=special_description
        )
        assert attachment.filename == special_filename
        assert attachment.description == special_description

    def test_unicode_handling(self):
        """Test Unicode character handling."""
        unicode_filename = "测试文件.zmm"
        unicode_description = "Archivo de prueba con caracteres especiales: äöü"

        attachment = Attachment(
            filename=unicode_filename, description=unicode_description
        )
        assert attachment.filename == unicode_filename
        assert attachment.description == unicode_description

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("filename", ""),
            ("description", ""),
            ("filename", "test.zmm"),
            ("description", "test description"),
        ],
    )
    def test_individual_field_setting(self, field_name, field_value):
        """Test setting individual fields after creation."""
        attachment = Attachment(filename="", description="")
        setattr(attachment, field_name, field_value)
        assert getattr(attachment, field_name) == field_value


class TestAttachmentPerformance:
    """Test performance-related aspects."""

    def test_bulk_attachment_creation(self):
        """Test creating many attachments efficiently."""
        attachments = []

        for i in range(100):
            attachment = Attachment(
                filename=f"file_{i:03d}.zmm", description=f"Test attachment number {i}"
            )
            attachments.append(attachment)

        assert len(attachments) == 100
        assert all(isinstance(att, Attachment) for att in attachments)

    def test_large_attachments_list(self):
        """Test handling large _attachments lists."""
        main_attachment = Attachment(filename="", description="")

        # Create many sub-attachments
        for i in range(50):
            sub_attachment = Attachment(
                filename=f"sub_{i}.dat", description=f"Sub-attachment {i}"
            )
            main_attachment._attachments.append(sub_attachment)

        assert len(main_attachment._attachments) == 50

        # Test XML conversion with large list
        xml_result = main_attachment.to_xml()
        assert isinstance(xml_result, list)
        assert len(xml_result) == 50


# =============================================================================
# Integration Tests
# =============================================================================


class TestAttachmentIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow_single(self, basic_attachment_data):
        """Test complete workflow: create -> modify -> serialize -> XML."""
        # Create
        attachment = Attachment(**basic_attachment_data)

        # Modify
        attachment.filename = "modified_" + attachment.filename
        attachment.description = "Modified: " + attachment.description

        # Serialize
        attachment_dict = attachment.model_dump()
        json_str = attachment.model_dump_json()

        # XML
        xml_element = attachment.to_xml()
        xml_string = attachment.to_xml(string=True)

        # Verify all formats are consistent
        assert attachment_dict["filename"] == attachment.filename
        assert attachment.filename in json_str
        assert isinstance(xml_element, et.Element)
        assert isinstance(xml_string, str)

    def test_full_workflow_multiple(self, attachment_dict_list):
        """Test complete workflow with multiple attachments."""
        # Read multiple
        main_attachment = Attachment(filename="", description="")
        main_attachment.read_dict(attachment_dict_list)

        # Verify structure
        assert len(main_attachment._attachments) > 0

        # XML conversion
        xml_list = main_attachment.to_xml()
        assert isinstance(xml_list, list)
        assert len(xml_list) == len(main_attachment._attachments)

        # String conversion
        xml_strings = main_attachment.to_xml(string=True)
        assert isinstance(xml_strings, list)
        assert all(isinstance(s, str) for s in xml_strings)


# =============================================================================
# Test Configuration and Markers
# =============================================================================

# Mark slow tests for optional execution
pytestmark = pytest.mark.attachment_basemodel
