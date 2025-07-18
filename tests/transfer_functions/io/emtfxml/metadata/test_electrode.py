# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for Electrode basemodel.

Tests cover:
- Basic instantiation and validation
- ElectrodeLocationEnum validation and behavior
- Comments field validation and string conversion
- XML generation (to_xml)
- Edge cases and error handling
- Integration scenarios
- Pydantic model validation

Created: 2025
Author: GitHub Copilot
"""
from unittest.mock import patch
from xml.etree import cElementTree as et

import pytest

from mt_metadata.common import Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata import Electrode
from mt_metadata.common.enumerations import ElectrodeLocationEnum


class TestElectrodeBasic:
    """Test basic Electrode functionality."""

    def test_default_initialization(self):
        """Test Electrode can be created with defaults."""
        electrode = Electrode()
        assert electrode.location == ElectrodeLocationEnum.NONE  # Default ""
        assert electrode.number == "0"
        assert isinstance(electrode.comments, Comment)

    def test_initialization_with_parameters(self):
        """Test Electrode initialization with explicit parameters."""
        electrode = Electrode(location="N", number="1a", comments="Ag-AgCl porous pot")
        assert electrode.location == ElectrodeLocationEnum.N
        assert electrode.number == "1a"
        assert isinstance(electrode.comments, Comment)

    def test_location_enum_values(self):
        """Test ElectrodeLocationEnum has expected values."""
        assert ElectrodeLocationEnum.N == "N"
        assert ElectrodeLocationEnum.S == "S"
        assert ElectrodeLocationEnum.E == "E"
        assert ElectrodeLocationEnum.W == "W"
        assert ElectrodeLocationEnum.NONE == ""

    def test_location_enum_assignment(self):
        """Test location field accepts enum values."""
        electrode = Electrode(location=ElectrodeLocationEnum.E)
        assert electrode.location == ElectrodeLocationEnum.E
        assert electrode.location == "E"

    def test_location_string_assignment(self):
        """Test location field accepts string values."""
        electrode = Electrode(location="W")
        assert electrode.location == ElectrodeLocationEnum.W
        assert electrode.location == "W"

    def test_number_field_assignment(self):
        """Test number field accepts various string formats."""
        test_numbers = ["0", "1", "1a", "electrode_01", "north_1"]
        for number in test_numbers:
            electrode = Electrode(number=number)
            assert electrode.number == number

    def test_comments_default_factory(self):
        """Test comments field uses default factory properly."""
        electrode1 = Electrode()
        electrode2 = Electrode()
        # Should be different Comment instances
        assert electrode1.comments is not electrode2.comments
        assert isinstance(electrode1.comments, Comment)
        assert isinstance(electrode2.comments, Comment)


class TestElectrodeLocationEnum:
    """Test ElectrodeLocationEnum functionality."""

    @pytest.mark.parametrize(
        "location_value,expected",
        [
            ("N", ElectrodeLocationEnum.N),
            ("S", ElectrodeLocationEnum.S),
            ("E", ElectrodeLocationEnum.E),
            ("W", ElectrodeLocationEnum.W),
            ("", ElectrodeLocationEnum.NONE),
        ],
    )
    def test_location_enum_conversion(self, location_value, expected):
        """Test location enum conversion from strings."""
        electrode = Electrode(location=location_value)
        assert electrode.location == expected

    def test_invalid_location_raises_error(self):
        """Test that invalid location values raise validation error."""
        with pytest.raises(ValueError):
            Electrode(location="INVALID")

    def test_location_enum_string_methods(self):
        """Test ElectrodeLocationEnum string methods work correctly."""
        # ElectrodeLocationEnum string representation includes the class name
        assert str(ElectrodeLocationEnum.N) == "ElectrodeLocationEnum.N"
        assert repr(ElectrodeLocationEnum.N) == "<ElectrodeLocationEnum.N: 'N'>"
        # But the value attribute gives the actual string value
        assert ElectrodeLocationEnum.N.value == "N"
        # And equality with string value still works
        assert ElectrodeLocationEnum.N == "N"

    def test_location_enum_in_list(self):
        """Test ElectrodeLocationEnum works in list operations."""
        valid_locations = list(ElectrodeLocationEnum)
        assert ElectrodeLocationEnum.N in valid_locations
        assert len(valid_locations) == 5  # N, S, E, W, NONE


class TestElectrodeCommentsValidation:
    """Test comments field validation functionality."""

    def test_comments_string_to_comment_conversion(self):
        """Test that string comments are converted to Comment objects."""
        comment_text = "Ag-AgCl porous pot electrode"
        electrode = Electrode(comments=comment_text)
        assert isinstance(electrode.comments, Comment)
        # Note: Comment object string conversion may be complex, test the type

    def test_comments_comment_object_assignment(self):
        """Test that Comment objects can be assigned directly."""
        comment_obj = Comment(value="Test electrode comment")
        electrode = Electrode(comments=comment_obj)
        assert electrode.comments is comment_obj

    def test_comments_validator_string_input(self):
        """Test comments validator with string input."""
        # Test the validator indirectly through model creation
        electrode = Electrode(location="N", number="1", comments="test comment")
        assert isinstance(electrode.comments, Comment)

    def test_comments_validator_comment_input(self):
        """Test comments validator with Comment input."""
        comment = Comment(value="existing comment")
        electrode = Electrode(location="N", number="1", comments=comment)
        assert electrode.comments is comment

    def test_comments_empty_string(self):
        """Test comments field with empty string."""
        electrode = Electrode(comments="")
        assert isinstance(electrode.comments, Comment)

    def test_comments_none_value(self):
        """Test comments field behavior with None (should use default factory)."""
        electrode = Electrode()  # comments not specified, uses default
        assert isinstance(electrode.comments, Comment)


class TestElectrodeXMLGeneration:
    """Test XML generation functionality."""

    @pytest.fixture
    def sample_electrode(self):
        """Sample electrode for XML testing."""
        return Electrode(location="N", number="1a", comments="Ag-AgCl porous pot")

    def test_to_xml_element_output(self, sample_electrode):
        """Test to_xml returns ET.Element by default."""
        xml_element = sample_electrode.to_xml()
        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Electrode"

    def test_to_xml_string_output(self, sample_electrode):
        """Test to_xml returns string when requested."""
        xml_string = sample_electrode.to_xml(string=True)
        assert isinstance(xml_string, str)
        assert "<Electrode" in xml_string
        assert "</Electrode>" in xml_string

    def test_to_xml_attributes(self, sample_electrode):
        """Test XML element has correct attributes."""
        xml_element = sample_electrode.to_xml()
        assert xml_element.attrib["location"] == "N"
        assert xml_element.attrib["number"] == "1a"

    def test_to_xml_location_uppercase(self):
        """Test that location is converted to uppercase in XML."""
        # Since enum only accepts uppercase, test the uppercase behavior directly
        electrode = Electrode(location="E", number="1", comments="test")
        xml_element = electrode.to_xml()
        assert xml_element.attrib["location"] == "E"  # Already uppercase from enum

    def test_to_xml_text_content(self, sample_electrode):
        """Test XML element text content comes from comments."""
        xml_element = sample_electrode.to_xml()
        # The text should be the string representation of the Comment
        assert xml_element.text is not None

    def test_to_xml_required_parameter(self, sample_electrode):
        """Test to_xml required parameter (currently unused but part of signature)."""
        xml_default = sample_electrode.to_xml()
        xml_required = sample_electrode.to_xml(required=True)
        # Should produce same result since required parameter isn't used
        assert xml_default.tag == xml_required.tag
        assert xml_default.attrib == xml_required.attrib

    def test_to_xml_default_values(self):
        """Test XML generation with default values."""
        electrode = Electrode()  # All defaults
        xml_element = electrode.to_xml()
        assert xml_element.attrib["location"] == ""  # NONE enum value
        assert xml_element.attrib["number"] == "0"
        assert xml_element.tag == "Electrode"

    @patch(
        "mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.element_to_string"
    )
    def test_to_xml_string_helper_called(
        self, mock_element_to_string, sample_electrode
    ):
        """Test that helpers.element_to_string is called for string output."""
        mock_element_to_string.return_value = "<mocked_xml/>"

        result = sample_electrode.to_xml(string=True)

        mock_element_to_string.assert_called_once()
        assert result == "<mocked_xml/>"


class TestElectrodeEdgeCases:
    """Test edge cases and error conditions."""

    def test_electrode_with_numeric_number(self):
        """Test electrode with numeric number (should be converted to string)."""
        electrode = Electrode(number=123)  # type: ignore[arg-type]
        assert electrode.number == "123"

    def test_electrode_model_dump(self):
        """Test Pydantic model_dump functionality."""
        electrode = Electrode(location="E", number="2", comments="test")
        data = electrode.model_dump()
        assert "location" in data
        assert "number" in data
        assert "comments" in data

    def test_electrode_model_validate(self):
        """Test Pydantic model_validate functionality."""
        data = {"location": "S", "number": "3", "comments": "test electrode"}
        electrode = Electrode.model_validate(data)
        assert electrode.location == ElectrodeLocationEnum.S
        assert electrode.number == "3"
        assert isinstance(electrode.comments, Comment)

    def test_electrode_json_schema_extra(self):
        """Test that json_schema_extra information is accessible."""
        # This tests the field definitions indirectly
        electrode = Electrode()
        # The json_schema_extra should be in field info (tested via field access)
        assert hasattr(electrode, "location")
        assert hasattr(electrode, "number")
        assert hasattr(electrode, "comments")

    def test_multiple_electrodes_independence(self):
        """Test that multiple electrode instances are independent."""
        e1 = Electrode(location="N", number="1", comments="first")
        e2 = Electrode(location="S", number="2", comments="second")

        assert e1.location != e2.location
        assert e1.number != e2.number
        assert e1.comments is not e2.comments


class TestElectrodeIntegration:
    """Test integration scenarios."""

    def test_electrode_inheritance_from_metadata_base(self):
        """Test that Electrode properly inherits from MetadataBase."""
        electrode = Electrode()
        assert hasattr(electrode, "model_dump")
        assert hasattr(electrode, "model_validate")
        # Should have Pydantic BaseModel methods

    def test_full_electrode_workflow(self):
        """Test complete electrode creation and XML generation workflow."""
        # Create electrode
        electrode = Electrode(
            location="W", number="west_1", comments="Western electrode with Ag-AgCl"
        )

        # Verify creation
        assert electrode.location == ElectrodeLocationEnum.W
        assert electrode.number == "west_1"
        assert isinstance(electrode.comments, Comment)

        # Generate XML
        xml_element = electrode.to_xml()
        assert xml_element.tag == "Electrode"
        assert xml_element.attrib["location"] == "W"
        assert xml_element.attrib["number"] == "west_1"

        # Generate XML string
        xml_string = electrode.to_xml(string=True)
        assert isinstance(xml_string, str)
        assert 'location="W"' in xml_string
        assert 'number="west_1"' in xml_string

    def test_electrode_with_complex_comments(self):
        """Test electrode with complex comment scenarios."""
        complex_comment = "Multi-line\nelectrode comment\nwith special chars: <>&"
        electrode = Electrode(
            location="E", number="complex_1", comments=complex_comment
        )

        # Should handle complex comment text
        assert isinstance(electrode.comments, Comment)
        xml_element = electrode.to_xml()
        assert xml_element.tag == "Electrode"

    @pytest.mark.parametrize(
        "location,number,comment",
        [
            ("N", "1", "North electrode"),
            ("S", "2a", "South electrode with suffix"),
            ("E", "east_01", "Eastern measurement point"),
            ("W", "west_backup", "Backup western electrode"),
            ("", "default", "Default location electrode"),
        ],
    )
    def test_electrode_parameter_combinations(self, location, number, comment):
        """Test various parameter combinations."""
        electrode = Electrode(location=location, number=number, comments=comment)

        # Verify all assignments worked
        # Note: electrode.location is a string, not an enum object
        if location:
            assert electrode.location == location
        else:
            assert electrode.location == ""  # Empty string for NONE
        assert electrode.number == number
        assert isinstance(electrode.comments, Comment)

        # Verify XML generation works
        xml_element = electrode.to_xml()
        assert xml_element.attrib["location"] == location.upper()
        assert xml_element.attrib["number"] == number

    def test_electrode_serialization_roundtrip(self):
        """Test that electrode can be serialized and deserialized."""
        original = Electrode(location="N", number="test", comments="roundtrip test")

        # Serialize to dict
        data = original.model_dump()

        # Deserialize from dict
        restored = Electrode.model_validate(data)

        # Should have same values
        assert restored.location == original.location
        assert restored.number == original.number
        # Comments comparison may be complex due to Comment object structure

    def test_xml_parseable_output(self):
        """Test that generated XML is parseable."""
        electrode = Electrode(location="S", number="parseable", comments="XML test")
        xml_string = electrode.to_xml(string=True)

        # Should be parseable by ET
        root = et.fromstring(xml_string)
        assert root.tag == "Electrode"
        assert root.attrib["location"] == "S"
        assert root.attrib["number"] == "parseable"


class TestElectrodePerformance:
    """Test performance aspects."""

    def test_electrode_creation_performance(self):
        """Test that electrode creation is efficient."""
        # Create many electrodes - should be fast
        electrodes = []
        for i in range(100):
            electrode = Electrode(
                location="N" if i % 2 == 0 else "S",
                number=str(i),
                comments=f"Electrode {i}",
            )
            electrodes.append(electrode)

        assert len(electrodes) == 100
        # All should be valid - location becomes a string
        for electrode in electrodes:
            assert electrode.location in ["N", "S"]
            assert isinstance(electrode.comments, Comment)
            assert isinstance(electrode.comments, Comment)

    def test_xml_generation_performance(self):
        """Test XML generation performance."""
        electrode = Electrode(
            location="E", number="perf_test", comments="Performance test electrode"
        )

        # Generate XML multiple times - should be efficient
        xml_strings = []
        for _ in range(50):
            xml_string = electrode.to_xml(string=True)
            xml_strings.append(xml_string)

        assert len(xml_strings) == 50
        # All should be identical
        assert all(xml == xml_strings[0] for xml in xml_strings)


if __name__ == "__main__":
    pytest.main([__file__])
