# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for Copyright basemodel class.

This module tests the Copyright basemodel class from the transfer_functions.io.emtfxml.metadata
module, including validation, XML generation, and enum handling.
"""

from unittest.mock import patch

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.emtfxml.metadata import Citation, Copyright
from mt_metadata.transfer_functions.io.emtfxml.metadata.copyright import (
    ReleaseStatusEnum,
)


@pytest.fixture(scope="module")
def basic_citation():
    """Return a basic Citation instance for testing."""
    return Citation(
        title="Test Citation Title",
        doi="http://doi.org/10.1234/test.citation",
        authors="John Doe, Jane Smith",
    )


@pytest.fixture(scope="module")
def complete_citation():
    """Return a complete Citation instance for testing."""
    return Citation(
        title="Comprehensive MT Study",
        doi="http://doi.org/10.5678/complete.study",
        authors="Alice Johnson, Bob Williams, Carol Davis",
        volume="42",
        pages="123-145",
        journal="Journal of Geophysical Research",
    )


@pytest.fixture(scope="module")
def basic_copyright(basic_citation):
    """Return a Copyright instance with basic required fields."""
    return Copyright(citation=basic_citation)


@pytest.fixture(scope="module")
def complete_copyright(complete_citation):
    """Return a Copyright instance with all fields populated."""
    return Copyright(
        citation=complete_citation,
        selected_publications="Smith et al. (2023), Johnson & Williams (2024)",
        release_status=ReleaseStatusEnum.Academic_Use_Only,
        conditions_of_use="Data may be used for academic research only. Commercial use prohibited.",
        acknowledgement="This work was funded by NSF grant XYZ-123456.",
        additional_info="Data collected during field campaign in Alaska, July 2023.",
    )


@pytest.fixture(scope="module")
def minimal_copyright():
    """Return a Copyright instance with minimal Citation."""
    minimal_citation = Citation(
        title="Minimal Test", doi="http://doi.org/10.1111/minimal"
    )
    return Copyright(citation=minimal_citation)


@pytest.fixture(
    params=[
        ReleaseStatusEnum.Unrestricted_release,
        ReleaseStatusEnum.Restricted_release,
        ReleaseStatusEnum.Paper_Citation_Required,
        ReleaseStatusEnum.Academic_Use_Only,
        ReleaseStatusEnum.Conditions_Apply,
        ReleaseStatusEnum.Data_Citation_Required,
    ]
)
def all_release_statuses(request):
    """Return all possible ReleaseStatusEnum values."""
    return request.param


@pytest.fixture(
    params=[
        {"field": "citation", "value": None, "error_type": "missing"},
        {"field": "citation", "value": "invalid_citation", "error_type": "type"},
        {"field": "release_status", "value": "Invalid Status", "error_type": "enum"},
    ]
)
def invalid_inputs(request):
    """Return invalid input values with expected error types."""
    return request.param


class TestCopyrightBasicFunctionality:
    """Test basic Copyright functionality."""

    def test_default_initialization(self, basic_copyright):
        """Test Copyright with default values."""
        # Test that required fields are set
        assert basic_copyright.citation is not None
        assert isinstance(basic_copyright.citation, Citation)

        # Test default values for optional fields
        assert basic_copyright.selected_publications is None
        assert basic_copyright.acknowledgement is None
        assert basic_copyright.additional_info is None

        # Test default values for required fields
        assert basic_copyright.release_status == "Unrestricted Release"
        assert basic_copyright.conditions_of_use is not None  # Has long default text
        assert (
            len(basic_copyright.conditions_of_use) > 100
        )  # Should have the long default text

    def test_complete_initialization(self, complete_copyright):
        """Test Copyright with all fields populated."""
        # Test Citation field
        assert complete_copyright.citation is not None
        assert isinstance(complete_copyright.citation, Citation)
        assert complete_copyright.citation.title == "Comprehensive MT Study"

        # Test string fields
        assert (
            complete_copyright.selected_publications
            == "Smith et al. (2023), Johnson & Williams (2024)"
        )
        assert (
            complete_copyright.acknowledgement
            == "This work was funded by NSF grant XYZ-123456."
        )
        assert (
            complete_copyright.additional_info
            == "Data collected during field campaign in Alaska, July 2023."
        )

        # Test enum field
        assert complete_copyright.release_status == ReleaseStatusEnum.Academic_Use_Only

        # Test conditions_of_use override
        assert (
            complete_copyright.conditions_of_use
            == "Data may be used for academic research only. Commercial use prohibited."
        )

    def test_minimal_initialization(self, minimal_copyright):
        """Test Copyright with minimal Citation."""
        assert minimal_copyright.citation is not None
        assert minimal_copyright.citation.title == "Minimal Test"
        assert (
            minimal_copyright.citation.doi.unicode_string()
            == "http://doi.org/10.1111/minimal"
        )

        # Other fields should have defaults
        assert minimal_copyright.selected_publications is None
        assert minimal_copyright.release_status == "Unrestricted Release"


class TestCopyrightValidation:
    """Test Copyright validation logic."""

    def test_citation_field_required(self):
        """Test that citation field is required."""
        with pytest.raises(ValidationError) as excinfo:
            Copyright()

        error_str = str(excinfo.value).lower()
        assert "citation" in error_str
        assert "required" in error_str or "missing" in error_str

    def test_valid_release_statuses(self, all_release_statuses, basic_citation):
        """Test all valid ReleaseStatusEnum values."""
        copyright_obj = Copyright(
            citation=basic_citation, release_status=all_release_statuses
        )
        assert copyright_obj.release_status == all_release_statuses

    def test_release_status_enum_values(self):
        """Test that ReleaseStatusEnum has expected values."""
        expected_values = {
            "Unrestricted_release": "Unrestricted release",
            "Restricted_release": "Restricted release",
            "Paper_Citation_Required": "Paper Citation Required",
            "Academic_Use_Only": "Academic Use Only",
            "Conditions_Apply": "Conditions Apply",
            "Data_Citation_Required": "Data Citation Required",
        }

        for name, value in expected_values.items():
            enum_member = getattr(ReleaseStatusEnum, name)
            assert enum_member.value == value

    def test_string_field_validation(self, basic_citation):
        """Test validation of string fields."""
        # Test that string fields accept valid strings
        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications="Test publication",
            acknowledgement="Test acknowledgement",
            additional_info="Test additional info",
            conditions_of_use="Custom conditions",
        )

        assert copyright_obj.selected_publications == "Test publication"
        assert copyright_obj.acknowledgement == "Test acknowledgement"
        assert copyright_obj.additional_info == "Test additional info"
        assert copyright_obj.conditions_of_use == "Custom conditions"

    def test_invalid_inputs(self, invalid_inputs):
        """Test Copyright with invalid inputs."""
        field = invalid_inputs["field"]
        value = invalid_inputs["value"]
        error_type = invalid_inputs["error_type"]

        # Skip citation=None test since we already test it separately
        if field == "citation" and value is None:
            return

        # Create base valid arguments
        base_args = {
            "citation": Citation(title="Test", doi="http://doi.org/10.1234/test")
        }

        # Override with invalid value
        test_args = {**base_args, field: value}

        with pytest.raises(ValidationError) as excinfo:
            Copyright(**test_args)

        error_str = str(excinfo.value).lower()
        if error_type == "type":
            assert any(keyword in error_str for keyword in ["type", "input should be"])
        elif error_type == "enum":
            assert any(keyword in error_str for keyword in ["input should be", "enum"])


class TestCopyrightReleaseStatusEnum:
    """Test ReleaseStatusEnum functionality."""

    def test_enum_inheritance(self):
        """Test that ReleaseStatusEnum inherits from str and Enum."""
        assert issubclass(ReleaseStatusEnum, str)
        assert hasattr(ReleaseStatusEnum, "__members__")

    def test_enum_string_behavior(self):
        """Test that enum members behave as strings."""
        status = ReleaseStatusEnum.Academic_Use_Only
        # The enum value is the string, not the repr
        assert status.value == "Academic Use Only"
        assert status == "Academic Use Only"

        # Test string operations on the value
        assert "Academic" in status.value
        assert status.value.upper() == "ACADEMIC USE ONLY"

    def test_enum_iteration(self):
        """Test iteration over enum members."""
        statuses = list(ReleaseStatusEnum)
        assert len(statuses) == 6

        expected_names = [
            "Unrestricted_release",
            "Restricted_release",
            "Paper_Citation_Required",
            "Academic_Use_Only",
            "Conditions_Apply",
            "Data_Citation_Required",
        ]

        actual_names = [status.name for status in statuses]
        assert actual_names == expected_names


class TestCopyrightXMLGeneration:
    """Test Copyright XML generation functionality."""

    def test_xml_generation_complete(self, complete_copyright):
        """Test XML generation with complete data."""
        xml_result = complete_copyright.to_xml(string=True)

        assert isinstance(xml_result, str)
        # XML elements are capitalized in this implementation
        assert "<Citation>" in xml_result
        assert "<SelectedPublications>" in xml_result
        assert "<Acknowledgement>" in xml_result
        assert "<ReleaseStatus>" in xml_result
        assert "<ConditionsOfUse>" in xml_result
        assert "<AdditionalInfo>" in xml_result

    def test_xml_generation_minimal(self, minimal_copyright):
        """Test XML generation with minimal data."""
        # Create a copy to avoid modifying the fixture due to the title() bug
        minimal_copy = Copyright(
            citation=minimal_copyright.citation,
            release_status=ReleaseStatusEnum.Unrestricted_release,  # Use the enum directly
        )

        xml_result = minimal_copy.to_xml(string=True)

        assert isinstance(xml_result, str)
        assert "<Citation>" in xml_result
        assert "<ReleaseStatus>" in xml_result
        assert "<ConditionsOfUse>" in xml_result

    def test_xml_generation_parameters(self, complete_copyright):
        """Test XML generation with different parameters."""
        # Test string=True
        result_string = complete_copyright.to_xml(string=True, required=True)
        assert isinstance(result_string, str)

        # Test string=True, required=False
        result_string_optional = complete_copyright.to_xml(string=True, required=False)
        assert isinstance(result_string_optional, str)

    def test_xml_release_status_formatting(self, basic_citation):
        """Test that release_status is properly formatted in XML."""
        # Test with enum that has underscores
        copyright_obj = Copyright(
            citation=basic_citation, release_status=ReleaseStatusEnum.Academic_Use_Only
        )

        xml_result = copyright_obj.to_xml(string=True)
        # The to_xml method calls .title() on release_status
        assert "Academic Use Only" in xml_result

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.to_xml")
    def test_xml_generation_order(self, mock_to_xml, complete_copyright):
        """Test that XML generation uses correct field order."""
        complete_copyright.to_xml()

        # Check that helpers.to_xml was called with correct order
        mock_to_xml.assert_called_once()
        call_args = mock_to_xml.call_args

        # Verify the order parameter
        assert "order" in call_args.kwargs
        expected_order = [
            "citation",
            "selected_publications",
            "acknowledgement",
            "release_status",
            "conditions_of_use",
            "additional_info",
        ]
        assert call_args.kwargs["order"] == expected_order


class TestCopyrightReadDict:
    """Test Copyright read_dict functionality."""

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers._read_element")
    def test_read_dict_calls_helper(self, mock_read_element, basic_copyright):
        """Test that read_dict calls the helper function correctly."""
        test_dict = {"copyright": {"test": "data"}}

        basic_copyright.read_dict(test_dict)

        # Verify that the helper was called with correct arguments
        mock_read_element.assert_called_once_with(
            basic_copyright, test_dict, "copyright"
        )

    def test_read_dict_interface(self, basic_copyright):
        """Test read_dict method interface."""
        # Test with a dict that has the expected structure to avoid the warning
        test_dict = {"copyright": {"test": "data"}}

        # Should not raise an exception (the helper may log a warning but that's expected)
        basic_copyright.read_dict(test_dict)


class TestCopyrightEdgeCases:
    """Test Copyright edge cases and special scenarios."""

    def test_empty_string_fields(self, basic_citation):
        """Test Copyright with empty string fields."""
        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications="",
            acknowledgement="",
            additional_info="",
            conditions_of_use="",
        )

        assert copyright_obj.selected_publications == ""
        assert copyright_obj.acknowledgement == ""
        assert copyright_obj.additional_info == ""
        assert copyright_obj.conditions_of_use == ""

    def test_whitespace_handling(self, basic_citation):
        """Test Copyright with whitespace in fields."""
        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications="  Test Publication  ",
            acknowledgement="\tTest Acknowledgement\n",
            additional_info=" Test Info ",
            conditions_of_use="  Custom conditions  ",
        )

        # Whitespace should be preserved
        assert copyright_obj.selected_publications == "  Test Publication  "
        assert copyright_obj.acknowledgement == "\tTest Acknowledgement\n"
        assert copyright_obj.additional_info == " Test Info "
        assert copyright_obj.conditions_of_use == "  Custom conditions  "

    def test_special_characters(self, basic_citation):
        """Test Copyright with special characters."""
        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications="Smith & Jones (2023): α/β Study",
            acknowledgement="Funded by NSF grant #123-456",
            additional_info="Temperature: 25°C, Depth: 100m",
            conditions_of_use="©2023 All rights reserved",
        )

        assert copyright_obj.selected_publications == "Smith & Jones (2023): α/β Study"
        assert copyright_obj.acknowledgement == "Funded by NSF grant #123-456"
        assert copyright_obj.additional_info == "Temperature: 25°C, Depth: 100m"
        assert copyright_obj.conditions_of_use == "©2023 All rights reserved"

    def test_unicode_characters(self, basic_citation):
        """Test Copyright with Unicode characters."""
        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications="李明 et al. (2023), Müller & Петров (2024)",
            acknowledgement="感谢 NSF 资助项目",
            additional_info="Località: Montañas de España",
            conditions_of_use="Данные доступны для исследований",
        )

        assert (
            copyright_obj.selected_publications
            == "李明 et al. (2023), Müller & Петров (2024)"
        )
        assert copyright_obj.acknowledgement == "感谢 NSF 资助项目"
        assert copyright_obj.additional_info == "Località: Montañas de España"
        assert copyright_obj.conditions_of_use == "Данные доступны для исследований"

    def test_long_field_values(self, basic_citation):
        """Test Copyright with very long field values."""
        long_text = "A" * 2000  # 2000 character string

        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications=long_text,
            acknowledgement=long_text,
            additional_info=long_text,
            conditions_of_use=long_text,
        )

        assert len(copyright_obj.selected_publications) == 2000
        assert len(copyright_obj.acknowledgement) == 2000
        assert len(copyright_obj.additional_info) == 2000
        assert len(copyright_obj.conditions_of_use) == 2000

    def test_none_assignment_optional_fields(self, basic_citation):
        """Test that optional fields can be set to None."""
        copyright_obj = Copyright(
            citation=basic_citation,
            selected_publications="Initial value",
            acknowledgement="Initial acknowledgement",
            additional_info="Initial info",
        )

        # Test that we can set optional fields to None
        copyright_obj.selected_publications = None
        copyright_obj.acknowledgement = None
        copyright_obj.additional_info = None

        assert copyright_obj.selected_publications is None
        assert copyright_obj.acknowledgement is None
        assert copyright_obj.additional_info is None


class TestCopyrightPerformance:
    """Test Copyright performance characteristics."""

    def test_bulk_creation_performance(self, basic_citation):
        """Test creating many Copyright instances."""
        copyrights = []
        for i in range(100):
            copyright_obj = Copyright(
                citation=basic_citation,
                selected_publications=f"Publication {i}",
                acknowledgement=f"Acknowledgement {i}",
                additional_info=f"Additional info {i}",
            )
            copyrights.append(copyright_obj)

        assert len(copyrights) == 100
        assert all(isinstance(c, Copyright) for c in copyrights)

    def test_xml_generation_performance(self, complete_copyright):
        """Test XML generation performance."""
        # Generate XML multiple times to test performance
        xml_results = []
        for _ in range(50):
            xml_result = complete_copyright.to_xml(string=True)
            xml_results.append(xml_result)

        assert len(xml_results) == 50
        assert all(isinstance(xml, str) for xml in xml_results)


class TestCopyrightIntegration:
    """Test Copyright integration with other components."""

    def test_citation_integration(self, complete_citation):
        """Test integration with Citation objects."""
        copyright_obj = Copyright(citation=complete_citation)

        # Test that Citation object is properly embedded
        assert copyright_obj.citation == complete_citation
        assert copyright_obj.citation.title == "Comprehensive MT Study"
        assert (
            copyright_obj.citation.authors == "Alice Johnson, Bob Williams, Carol Davis"
        )

    def test_field_assignment_after_creation(self, basic_copyright):
        """Test field assignment after Copyright creation."""
        # Test assigning to string fields
        basic_copyright.selected_publications = "Updated Publications"
        basic_copyright.acknowledgement = "Updated Acknowledgement"
        basic_copyright.additional_info = "Updated Additional Info"
        basic_copyright.conditions_of_use = "Updated Conditions"

        assert basic_copyright.selected_publications == "Updated Publications"
        assert basic_copyright.acknowledgement == "Updated Acknowledgement"
        assert basic_copyright.additional_info == "Updated Additional Info"
        assert basic_copyright.conditions_of_use == "Updated Conditions"

    def test_release_status_assignment(self, basic_copyright):
        """Test release_status field assignment."""
        # Test assigning different enum values
        for status in ReleaseStatusEnum:
            basic_copyright.release_status = status
            assert basic_copyright.release_status == status

    def test_citation_replacement(self, basic_copyright):
        """Test replacing the citation field."""
        new_citation = Citation(
            title="New Citation Title",
            doi="http://doi.org/10.9999/new.citation",
            authors="New Author",
        )

        basic_copyright.citation = new_citation
        assert basic_copyright.citation == new_citation
        assert basic_copyright.citation.title == "New Citation Title"


if __name__ == "__main__":
    pytest.main([__file__])
