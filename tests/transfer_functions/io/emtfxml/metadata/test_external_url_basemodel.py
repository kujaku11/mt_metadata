# -*- coding: utf-8 -*-
"""
Test suite for ExternalUrl basemodel
"""
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.emtfxml.metadata.external_url_basemodel import (
    ExternalUrl,
)


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def basic_external_url_data():
    """Basic external URL data for testing."""
    return {
        "description": "IRIS DMC Metadata",
        "url": "http://www.iris.edu/mda/EM/NVS11",
    }


@pytest.fixture
def minimal_external_url_data():
    """Minimal external URL data for testing."""
    return {
        "description": "Test external reference",
        "url": "https://example.com/data",
    }


@pytest.fixture
def empty_external_url():
    """Empty external URL instance."""
    return ExternalUrl()


@pytest.fixture
def basic_external_url(basic_external_url_data):
    """Basic external URL instance."""
    return ExternalUrl(**basic_external_url_data)


@pytest.fixture
def minimal_external_url(minimal_external_url_data):
    """Minimal external URL instance."""
    return ExternalUrl(**minimal_external_url_data)


# =============================================================================
# Test Class: ExternalUrl Instantiation
# =============================================================================
class TestExternalUrlInstantiation:
    """Test external URL instantiation scenarios."""

    def test_empty_external_url_creation(self, empty_external_url):
        """Test creating an empty external URL."""
        assert empty_external_url.description == ""
        assert empty_external_url.url == ""

    def test_basic_external_url_creation(
        self, basic_external_url, basic_external_url_data
    ):
        """Test creating a basic external URL with valid data."""
        assert basic_external_url.description == basic_external_url_data["description"]
        assert str(basic_external_url.url) == basic_external_url_data["url"]

    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("description", "Test description", "Test description"),
            ("description", "", ""),
            (
                "description",
                "IRIS DMC Metadata Repository",
                "IRIS DMC Metadata Repository",
            ),
        ],
    )
    def test_description_field_assignment(
        self, empty_external_url, field, value, expected
    ):
        """Test description field assignment."""
        setattr(empty_external_url, field, value)
        assert getattr(empty_external_url, field) == expected

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("http://example.com", "http://example.com/"),
            ("https://example.com", "https://example.com/"),
            ("https://www.iris.edu/mda/EM/NVS11", "https://www.iris.edu/mda/EM/NVS11"),
            ("http://localhost:8080/data", "http://localhost:8080/data"),
        ],
    )
    def test_url_assignment(self, empty_external_url, url, expected):
        """Test URL assignment with normalization."""
        empty_external_url.url = url
        assert str(empty_external_url.url) == expected

    def test_invalid_url_assignment(self, empty_external_url):
        """Test that invalid URLs raise validation errors."""
        with pytest.raises(ValidationError):
            empty_external_url.url = "not-a-valid-url"

    def test_url_type_after_assignment(self, empty_external_url):
        """Test that URL becomes HttpUrl object after valid assignment."""
        # Initially a string
        assert isinstance(empty_external_url.url, str)

        # After assignment becomes HttpUrl
        empty_external_url.url = "https://example.com"
        assert (
            str(type(empty_external_url.url)) == "<class 'pydantic.networks.HttpUrl'>"
        )

    def test_empty_url_assignment_after_creation(self, empty_external_url):
        """Test that empty URL assignment after valid URL raises validation error."""
        empty_external_url.url = "https://example.com"

        # Cannot assign empty string to HttpUrl field after creation
        with pytest.raises(ValidationError):
            empty_external_url.url = ""


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization functionality."""

    def test_to_xml_empty_external_url(self, empty_external_url):
        """Test XML serialization of empty external URL."""
        xml_element = empty_external_url.to_xml()

        assert xml_element.tag == "external_url"
        assert xml_element.attrib == {}

        # Check child elements
        children = {child.tag: child for child in xml_element}
        assert children["description"].text == ""
        assert children["url"].text == ""

    def test_to_xml_basic_external_url(self, basic_external_url):
        """Test XML serialization of basic external URL."""
        xml_element = basic_external_url.to_xml()

        assert xml_element.tag == "external_url"
        assert xml_element.attrib == {}

        # Check child elements
        children = {child.tag: child for child in xml_element}
        assert children["description"].text == "IRIS DMC Metadata"
        assert children["url"].text == "http://www.iris.edu/mda/EM/NVS11"

    def test_to_xml_string_output(self, basic_external_url):
        """Test XML string serialization."""
        xml_string = basic_external_url.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_string
        assert "<external_url>" in xml_string
        assert "<description>IRIS DMC Metadata</description>" in xml_string
        assert "<url>http://www.iris.edu/mda/EM/NVS11</url>" in xml_string
        assert "</external_url>" in xml_string

    @pytest.mark.parametrize(
        "field,value,expected_xml_text",
        [
            ("description", "Test description", "Test description"),
            ("description", "", ""),
            ("description", "External data source", "External data source"),
        ],
    )
    def test_to_xml_field_values(
        self, empty_external_url, field, value, expected_xml_text
    ):
        """Test XML field value serialization."""
        setattr(empty_external_url, field, value)
        empty_external_url.url = "http://example.com"

        xml_element = empty_external_url.to_xml()

        child_element = xml_element.find(field)
        assert child_element is not None
        assert child_element.text == expected_xml_text

    def test_to_xml_url_normalization(self, empty_external_url):
        """Test that URL normalization is reflected in XML output."""
        empty_external_url.description = "Test"
        empty_external_url.url = "https://example.com"

        xml_element = empty_external_url.to_xml()
        url_element = xml_element.find("url")
        assert url_element.text == "https://example.com/"


# =============================================================================
# Test Class: Dictionary Operations
# =============================================================================
class TestDictionaryOperations:
    """Test dictionary serialization and read_dict functionality."""

    def test_to_dict_basic_external_url(self, basic_external_url):
        """Test dictionary serialization of basic external URL."""
        external_url_dict = basic_external_url.to_dict()

        assert "external_url" in external_url_dict
        data = external_url_dict["external_url"]

        assert data["description"] == "IRIS DMC Metadata"
        assert data["url"] == "http://www.iris.edu/mda/EM/NVS11"

    def test_to_dict_empty_external_url(self, empty_external_url):
        """Test dictionary serialization of empty external URL."""
        external_url_dict = empty_external_url.to_dict()

        assert "external_url" in external_url_dict
        data = external_url_dict["external_url"]

        assert data["description"] == ""
        assert data["url"] == ""

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers._read_element")
    def test_read_dict_method(self, mock_read_element, empty_external_url):
        """Test read_dict method calls helper correctly."""
        test_dict = {"description": "Test", "url": "https://example.com"}

        empty_external_url.read_dict(test_dict)

        mock_read_element.assert_called_once_with(
            empty_external_url, test_dict, "external_url"
        )


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def test_url_with_special_characters(self, empty_external_url):
        """Test URL with special characters and parameters."""
        test_urls = [
            "https://example.com/path?param=value&other=test",
            "https://example.com:8080/path/to/resource",
            "http://subdomain.example.com/data",
            "https://example.com/path/with-dashes_and_underscores",
        ]

        for url in test_urls:
            empty_external_url.url = url
            assert str(empty_external_url.url) == url

    def test_description_with_special_characters(self, empty_external_url):
        """Test description with special characters."""
        special_descriptions = [
            "Description with 'quotes' and \"double quotes\"",
            "Description with & ampersand",
            "Description with <brackets>",
            "Description with unicode: café naïve résumé",
            "Multi-line\ndescription\nwith\nbreaks",
        ]

        for desc in special_descriptions:
            empty_external_url.description = desc
            assert empty_external_url.description == desc

    @pytest.mark.parametrize(
        "invalid_input",
        [
            None,
            123,
            [],
            {},
        ],
    )
    def test_invalid_description_types(self, empty_external_url, invalid_input):
        """Test that invalid types for description field are handled."""
        # Pydantic should convert these to strings
        empty_external_url.description = invalid_input
        assert isinstance(empty_external_url.description, str)

    def test_very_long_url(self, empty_external_url):
        """Test handling of very long URLs."""
        # Create a very long but valid URL
        long_path = "a" * 1000
        long_url = f"https://example.com/{long_path}"

        empty_external_url.url = long_url
        assert str(empty_external_url.url) == long_url

    def test_very_long_description(self, empty_external_url):
        """Test handling of very long descriptions."""
        long_description = "x" * 10000

        empty_external_url.description = long_description
        assert empty_external_url.description == long_description

    def test_xml_with_empty_fields(self, empty_external_url):
        """Test XML generation with empty fields."""
        xml_element = empty_external_url.to_xml()

        # Should still generate valid XML structure
        assert xml_element.tag == "external_url"
        children = {child.tag: child for child in xml_element}
        assert "description" in children
        assert "url" in children
        assert children["description"].text == ""
        assert children["url"].text == ""


# =============================================================================
# Test Class: Boundary Value Testing
# =============================================================================
class TestBoundaryValues:
    """Test boundary values and limits."""

    def test_empty_string_fields(self, empty_external_url):
        """Test empty string handling."""
        empty_external_url.description = ""

        assert empty_external_url.description == ""

        # XML should handle empty strings
        xml_element = empty_external_url.to_xml()
        desc_element = xml_element.find("description")
        assert desc_element.text == ""

    def test_whitespace_handling(self, empty_external_url):
        """Test whitespace handling in fields."""
        whitespace_cases = [
            "   leading spaces",
            "trailing spaces   ",
            "   both sides   ",
            "\t\ttabs\t\t",
            "\n\nnewlines\n\n",
        ]

        for case in whitespace_cases:
            empty_external_url.description = case
            assert empty_external_url.description == case

    def test_url_schemes(self, empty_external_url):
        """Test different URL schemes."""
        schemes = [
            "http://example.com",
            "https://example.com",
            "ftp://example.com",  # This might fail - HttpUrl might only accept http/https
        ]

        for scheme in schemes[:2]:  # Test only http/https for now
            empty_external_url.url = scheme
            assert str(empty_external_url.url).startswith(scheme.split("://")[0])


# =============================================================================
# Test Class: Integration Tests
# =============================================================================
class TestIntegration:
    """Test integration scenarios and workflows."""

    def test_external_url_with_minimal_data(self):
        """Test external URL with only required fields."""
        external_url = ExternalUrl()

        # Should work with empty values
        xml_element = external_url.to_xml()
        assert xml_element.tag == "external_url"

        # Should serialize to dict
        external_url_dict = external_url.to_dict()
        assert "external_url" in external_url_dict

    def test_complete_external_url_workflow(self):
        """Test complete external URL creation and serialization workflow."""
        # Create external URL with all fields
        external_url = ExternalUrl(
            description="IRIS DMC Magnetotelluric Data",
            url="https://www.iris.edu/mda/EM/NVS11",
        )

        # Test XML serialization
        xml_element = external_url.to_xml()
        assert xml_element.tag == "external_url"

        # Test dictionary serialization
        external_url_dict = external_url.to_dict()
        assert "external_url" in external_url_dict

        # Verify data integrity
        data = external_url_dict["external_url"]
        assert data["description"] == "IRIS DMC Magnetotelluric Data"
        assert data["url"] == "https://www.iris.edu/mda/EM/NVS11"

    def test_external_url_modification_workflow(self):
        """Test modifying external URL after creation."""
        external_url = ExternalUrl()

        # Initial state
        assert external_url.description == ""
        assert external_url.url == ""

        # Modify fields
        external_url.description = "Updated description"
        external_url.url = "https://updated.example.com"

        # Verify changes
        assert external_url.description == "Updated description"
        assert str(external_url.url) == "https://updated.example.com/"

        # Test XML reflects changes
        xml_element = external_url.to_xml()
        children = {child.tag: child for child in xml_element}
        assert children["description"].text == "Updated description"
        assert children["url"].text == "https://updated.example.com/"

    def test_multiple_external_urls(self):
        """Test creating multiple external URL instances."""
        external_urls = []

        # Create different external URLs
        external_urls.append(
            ExternalUrl(description="IRIS DMC", url="https://www.iris.edu/mda/EM/NVS11")
        )

        external_urls.append(
            ExternalUrl(
                description="EMTF Data Repository", url="https://earthscope.org/mt/data"
            )
        )

        # Test all can be serialized
        for i, external_url in enumerate(external_urls):
            xml_element = external_url.to_xml()
            assert xml_element.tag == "external_url"

            external_url_dict = external_url.to_dict()
            assert "external_url" in external_url_dict


# =============================================================================
# Test Class: Performance and Memory
# =============================================================================
class TestPerformance:
    """Test performance characteristics."""

    def test_large_batch_creation(self):
        """Test creating many external URL instances."""
        external_urls = []

        for i in range(100):
            external_url = ExternalUrl(
                description=f"External URL {i}", url=f"https://example{i}.com"
            )
            external_urls.append(external_url)

        assert len(external_urls) == 100

        # Test they all work
        for external_url in external_urls[:5]:  # Test first 5
            xml_element = external_url.to_xml()
            assert xml_element.tag == "external_url"

    def test_xml_serialization_performance(self, basic_external_url):
        """Test XML serialization performance."""
        # This should complete quickly
        for _ in range(100):
            xml_element = basic_external_url.to_xml()
            assert xml_element.tag == "external_url"

    def test_dict_serialization_performance(self, basic_external_url):
        """Test dictionary serialization performance."""
        # This should complete quickly
        for _ in range(100):
            external_url_dict = basic_external_url.to_dict()
            assert "external_url" in external_url_dict
