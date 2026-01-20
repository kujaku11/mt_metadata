# -*- coding: utf-8 -*-
"""
Test suite for Estimate basemodel
"""

from unittest.mock import patch

import pytest
from pydantic import ValidationError

from mt_metadata.common.enumerations import ArrayDTypeEnum, EstimateIntentionEnum
from mt_metadata.transfer_functions.io.emtfxml.metadata import Estimate


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def basic_estimate_data():
    """Basic estimate data for testing."""
    return {
        "name": "variance",
        "type": ArrayDTypeEnum.real_type,
        "description": "Error variance estimate",
        "external_url": "http://www.iris.edu/dms/products/emtf/variance.html",
        "intention": EstimateIntentionEnum.error_estimate,
        "tag": "tipper",
    }


@pytest.fixture
def minimal_estimate_data():
    """Minimal estimate data for testing."""
    return {
        "name": "test_estimate",
        "type": ArrayDTypeEnum.complex_type,
        "description": "Test description",
        "external_url": "https://example.com",
        "intention": EstimateIntentionEnum.signal_coherence,
        "tag": "test",
    }


@pytest.fixture
def empty_estimate():
    """Empty estimate instance."""
    return Estimate()


@pytest.fixture
def basic_estimate(basic_estimate_data):
    """Basic estimate instance."""
    return Estimate(**basic_estimate_data)


@pytest.fixture
def minimal_estimate(minimal_estimate_data):
    """Minimal estimate instance."""
    return Estimate(**minimal_estimate_data)


# =============================================================================
# Test Class: Estimate Instantiation
# =============================================================================
class TestEstimateInstantiation:
    """Test estimate instantiation scenarios."""

    def test_empty_estimate_creation(self, empty_estimate):
        """Test creating an empty estimate."""
        assert empty_estimate.name == ""
        assert empty_estimate.type == ""
        assert empty_estimate.description == ""
        assert empty_estimate.external_url == ""
        assert empty_estimate.intention == ""
        assert empty_estimate.tag == ""

    def test_basic_estimate_creation(self, basic_estimate, basic_estimate_data):
        """Test creating a basic estimate with valid data."""
        assert basic_estimate.name == basic_estimate_data["name"]
        assert basic_estimate.type == basic_estimate_data["type"]
        assert basic_estimate.description == basic_estimate_data["description"]
        assert str(basic_estimate.external_url) == basic_estimate_data["external_url"]
        assert basic_estimate.intention == basic_estimate_data["intention"]
        assert basic_estimate.tag == basic_estimate_data["tag"]

    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("name", "test_name", "test_name"),
            ("name", "", ""),
            ("description", "Test description", "Test description"),
            ("description", "", ""),
            ("tag", "test_tag", "test_tag"),
            ("tag", "", ""),
        ],
    )
    def test_string_field_assignment(self, empty_estimate, field, value, expected):
        """Test individual string field assignment."""
        setattr(empty_estimate, field, value)
        assert getattr(empty_estimate, field) == expected

    @pytest.mark.parametrize(
        "type_value",
        [
            ArrayDTypeEnum.real_type,
            ArrayDTypeEnum.complex_type,
            "real",
            "complex",
        ],
    )
    def test_type_enum_assignment(self, empty_estimate, type_value):
        """Test type enum assignment."""
        empty_estimate.type = type_value
        assert empty_estimate.type == type_value

    @pytest.mark.parametrize(
        "intention_value",
        [
            EstimateIntentionEnum.error_estimate,
            EstimateIntentionEnum.signal_coherence,
            EstimateIntentionEnum.signal_power_estimate,
            EstimateIntentionEnum.primary_data_type,
            "error estimate",
            "signal coherence",
        ],
    )
    def test_intention_enum_assignment(self, empty_estimate, intention_value):
        """Test intention enum assignment."""
        empty_estimate.intention = intention_value
        assert empty_estimate.intention == intention_value

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("http://example.com", "http://example.com/"),
            ("https://example.com", "https://example.com/"),
            (
                "https://www.iris.edu/dms/products/emtf/variance.html",
                "https://www.iris.edu/dms/products/emtf/variance.html",
            ),
            ("http://localhost:8080/path", "http://localhost:8080/path"),
        ],
    )
    def test_external_url_assignment(self, empty_estimate, url, expected):
        """Test external URL assignment."""
        empty_estimate.external_url = url
        assert str(empty_estimate.external_url) == expected

    def test_invalid_url_assignment(self, empty_estimate):
        """Test that invalid URLs raise validation errors."""
        with pytest.raises(ValidationError):
            empty_estimate.external_url = "not-a-valid-url"

    def test_invalid_type_enum(self, empty_estimate):
        """Test that invalid type enum raises validation error."""
        with pytest.raises(ValidationError):
            empty_estimate.type = "invalid_type"

    def test_invalid_intention_enum(self, empty_estimate):
        """Test that invalid intention enum raises validation error."""
        with pytest.raises(ValidationError):
            empty_estimate.intention = "invalid intention"


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization functionality."""

    def test_to_xml_empty_estimate(self, empty_estimate):
        """Test XML serialization of empty estimate."""
        xml_element = empty_estimate.to_xml()

        assert xml_element.tag == "Estimate"
        assert xml_element.attrib["name"] == ""
        assert xml_element.attrib["type"] == ""

        # Check child elements
        children = {child.tag: child for child in xml_element}
        assert "Description" in children
        assert children["Description"].text == ""
        assert "ExternalUrl" in children
        assert children["ExternalUrl"].text == ""
        assert "Intention" in children
        assert children["Intention"].text == ""
        assert "tag" in children
        assert children["tag"].text == ""

    def test_to_xml_basic_estimate(self, basic_estimate):
        """Test XML serialization of basic estimate."""
        xml_element = basic_estimate.to_xml()

        assert xml_element.tag == "Estimate"
        assert xml_element.attrib["name"] == "VARIANCE"  # uppercase
        assert xml_element.attrib["type"] == "real"

        # Check child elements
        children = {child.tag: child for child in xml_element}
        assert children["Description"].text == "Error variance estimate"
        assert (
            children["ExternalUrl"].text
            == "http://www.iris.edu/dms/products/emtf/variance.html"
        )
        assert children["Intention"].text == "error estimate"
        assert children["tag"].text == "tipper"

    def test_to_xml_name_uppercase(self, empty_estimate):
        """Test that name is converted to uppercase in XML."""
        empty_estimate.name = "test_name"
        empty_estimate.type = ArrayDTypeEnum.real_type

        xml_element = empty_estimate.to_xml()
        assert xml_element.attrib["name"] == "TEST_NAME"

    def test_to_xml_with_complex_type(self, minimal_estimate):
        """Test XML serialization with complex type."""
        xml_element = minimal_estimate.to_xml()

        assert xml_element.tag == "Estimate"
        assert xml_element.attrib["type"] == "complex"

    def test_to_xml_string_output(self, basic_estimate):
        """Test XML string output."""
        with patch(
            "mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.element_to_string"
        ) as mock_element_to_string:
            mock_element_to_string.return_value = "<Estimate>test</Estimate>"

            xml_string = basic_estimate.to_xml(string=True)

            mock_element_to_string.assert_called_once()
            assert xml_string == "<Estimate>test</Estimate>"

    @pytest.mark.parametrize(
        "field,value,expected_xml_text",
        [
            ("description", "Test description", "Test description"),
            ("description", "", ""),
            ("tag", "test_tag", "test_tag"),
            ("tag", "", ""),
        ],
    )
    def test_to_xml_field_values(self, empty_estimate, field, value, expected_xml_text):
        """Test XML field value serialization."""
        setattr(empty_estimate, field, value)
        empty_estimate.name = "test"
        empty_estimate.type = ArrayDTypeEnum.real_type
        empty_estimate.external_url = "http://example.com"
        empty_estimate.intention = EstimateIntentionEnum.error_estimate

        xml_element = empty_estimate.to_xml()

        # Map field names to XML element names
        xml_field_map = {
            "description": "Description",
            "tag": "tag",
        }

        xml_field_name = xml_field_map.get(field, field)
        child = xml_element.find(xml_field_name)
        assert child is not None
        assert child.text == expected_xml_text


# =============================================================================
# Test Class: Serialization and Deserialization
# =============================================================================
class TestSerialization:
    """Test serialization and deserialization methods."""

    def test_to_dict_empty_estimate(self, empty_estimate):
        """Test dictionary serialization of empty estimate."""
        result = empty_estimate.to_dict()

        assert isinstance(result, dict)
        assert "estimate" in result
        estimate_data = result["estimate"]
        # Check that all required fields are present with empty values
        assert estimate_data["name"] == ""
        assert estimate_data["type"] == ""
        assert estimate_data["description"] == ""
        assert estimate_data["external_url"] == ""
        assert estimate_data["intention"] == ""
        assert estimate_data["tag"] == ""

    def test_to_dict_basic_estimate(self, basic_estimate, basic_estimate_data):
        """Test dictionary serialization of basic estimate."""
        result = basic_estimate.to_dict()

        assert isinstance(result, dict)
        assert "estimate" in result
        estimate_data = result["estimate"]

        assert estimate_data["name"] == basic_estimate_data["name"]
        assert estimate_data["type"] == basic_estimate_data["type"]
        assert estimate_data["description"] == basic_estimate_data["description"]
        assert estimate_data["external_url"] == basic_estimate_data["external_url"]
        assert estimate_data["intention"] == basic_estimate_data["intention"]
        assert estimate_data["tag"] == basic_estimate_data["tag"]

    def test_from_dict_round_trip(self, basic_estimate_data):
        """Test round-trip serialization via dictionary."""
        original_estimate = Estimate(**basic_estimate_data)
        estimate_dict = original_estimate.to_dict()

        # Reconstruct from the nested dict structure
        reconstructed_estimate = Estimate(**estimate_dict["estimate"])

        assert original_estimate.name == reconstructed_estimate.name
        assert original_estimate.type == reconstructed_estimate.type
        assert original_estimate.description == reconstructed_estimate.description
        assert str(original_estimate.external_url) == str(
            reconstructed_estimate.external_url
        )
        assert original_estimate.intention == reconstructed_estimate.intention
        assert original_estimate.tag == reconstructed_estimate.tag

    def test_read_dict_method(self, empty_estimate):
        """Test read_dict method."""
        input_dict = {
            "estimate": {
                "name": "test_name",
                "type": "real",
                "description": "test description",
                "external_url": "http://example.com",
                "intention": "error estimate",
                "tag": "test_tag",
            }
        }

        with patch(
            "mt_metadata.transfer_functions.io.emtfxml.metadata.helpers._read_element"
        ) as mock_read_element:
            empty_estimate.read_dict(input_dict)
            mock_read_element.assert_called_once_with(
                empty_estimate, input_dict, "estimate"
            )

    def test_json_schema_extra_metadata(self, empty_estimate):
        """Test that json_schema_extra metadata is preserved."""
        schema = empty_estimate.model_json_schema()

        # Check that each field has the expected json_schema_extra properties
        for field_name in [
            "name",
            "type",
            "description",
            "external_url",
            "intention",
            "tag",
        ]:
            field_schema = schema["properties"][field_name]
            assert "units" in field_schema
            assert "required" in field_schema


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_very_long_strings(self, empty_estimate):
        """Test handling of very long strings."""
        long_string = "x" * 1000

        empty_estimate.name = long_string
        assert empty_estimate.name == long_string

        empty_estimate.description = long_string
        assert empty_estimate.description == long_string

        empty_estimate.tag = long_string
        assert empty_estimate.tag == long_string

    def test_unicode_strings(self, empty_estimate):
        """Test handling of unicode strings."""
        unicode_string = "测试中文字符🌍🔬"

        empty_estimate.name = unicode_string
        assert empty_estimate.name == unicode_string

        empty_estimate.description = unicode_string
        assert empty_estimate.description == unicode_string

    def test_special_characters_in_name_xml(self, empty_estimate):
        """Test XML generation with special characters in name."""
        empty_estimate.name = "test-name_with.special&chars"
        empty_estimate.type = ArrayDTypeEnum.real_type
        empty_estimate.external_url = "http://example.com"
        empty_estimate.intention = EstimateIntentionEnum.error_estimate

        xml_element = empty_estimate.to_xml()
        # Name should be uppercase in XML
        assert xml_element.attrib["name"] == "TEST-NAME_WITH.SPECIAL&CHARS"

    def test_empty_url_handling(self, empty_estimate):
        """Test handling of empty URL in default instance."""
        # Default empty estimate starts with empty string for external_url
        assert empty_estimate.external_url == ""

        # Test assignment of valid URL
        empty_estimate.external_url = "https://example.com"
        assert str(empty_estimate.external_url) == "https://example.com/"

        # Test that empty string assignment after creation raises validation error
        with pytest.raises(ValidationError):
            empty_estimate.external_url = ""

    @pytest.mark.parametrize(
        "invalid_input",
        [
            True,
            [],
            {},
        ],
    )
    def test_invalid_string_field_types(self, empty_estimate, invalid_input):
        """Test that invalid types for string fields raise validation errors."""
        with pytest.raises((ValidationError, TypeError)):
            empty_estimate.name = invalid_input


# =============================================================================
# Test Class: Enum Tests
# =============================================================================
class TestEnums:
    """Test enum functionality."""

    def test_type_enum_values(self):
        """Test ArrayDTypeEnum values."""
        assert ArrayDTypeEnum.real_type == "real"
        assert ArrayDTypeEnum.complex_type == "complex"
        # Test that these types are in the enum
        assert ArrayDTypeEnum.real_type in list(ArrayDTypeEnum)
        assert ArrayDTypeEnum.complex_type in list(ArrayDTypeEnum)

    def test_intention_enum_values(self):
        """Test EstimateIntentionEnum values."""
        assert EstimateIntentionEnum.error_estimate == "error estimate"
        assert EstimateIntentionEnum.signal_coherence == "signal coherence"
        assert EstimateIntentionEnum.signal_power_estimate == "signal power estimate"
        assert EstimateIntentionEnum.primary_data_type == "primary data type"

    def test_enum_string_conversion(self):
        """Test that enums can be converted to strings."""
        # Note: These enums use their full class name in string representation
        assert str(ArrayDTypeEnum.real_type) == "ArrayDTypeEnum.real_type"
        assert (
            str(EstimateIntentionEnum.error_estimate)
            == "EstimateIntentionEnum.error_estimate"
        )

    def test_enum_equality_with_strings(self):
        """Test that enums are equal to their string values."""
        assert ArrayDTypeEnum.real_type == "real"
        assert EstimateIntentionEnum.signal_coherence == "signal coherence"


# =============================================================================
# Test Class: Integration Tests
# =============================================================================
class TestIntegration:
    """Test integration scenarios."""

    def test_complete_estimate_workflow(self):
        """Test complete estimate creation and serialization workflow."""
        # Create estimate with all fields
        estimate = Estimate(
            name="coherence_estimate",
            type=ArrayDTypeEnum.complex_type,
            description="Signal coherence between components",
            external_url="https://earthscope.org/mt/coherence",
            intention=EstimateIntentionEnum.signal_coherence,
            tag="coherence",
        )

        # Test XML serialization
        xml_element = estimate.to_xml()
        assert xml_element.tag == "Estimate"
        assert xml_element.attrib["name"] == "COHERENCE_ESTIMATE"
        assert xml_element.attrib["type"] == "complex"

        # Test dictionary serialization
        estimate_dict = estimate.to_dict()
        assert "estimate" in estimate_dict

        # Test round-trip
        reconstructed = Estimate(**estimate_dict["estimate"])
        assert reconstructed.name == estimate.name
        assert reconstructed.type == estimate.type

    def test_estimate_with_minimal_data(self):
        """Test estimate with only required fields."""
        estimate = Estimate()

        # Should work with empty values
        xml_element = estimate.to_xml()
        assert xml_element.tag == "Estimate"

        # Should serialize to dict
        result = estimate.to_dict()
        assert "estimate" in result

    def test_multiple_estimates_different_types(self):
        """Test creating multiple estimates with different configurations."""
        estimates = []

        # Real estimate
        estimates.append(
            Estimate(
                name="variance",
                type=ArrayDTypeEnum.real_type,
                description="Error variance",
                external_url="http://example.com/variance",
                intention=EstimateIntentionEnum.error_estimate,
                tag="error",
            )
        )

        # Complex estimate
        estimates.append(
            Estimate(
                name="coherence",
                type=ArrayDTypeEnum.complex_type,
                description="Signal coherence",
                external_url="http://example.com/coherence",
                intention=EstimateIntentionEnum.signal_coherence,
                tag="coherence",
            )
        )

        # Test all can be serialized
        for i, estimate in enumerate(estimates):
            xml_element = estimate.to_xml()
            assert xml_element.tag == "Estimate"

            estimate_dict = estimate.to_dict()
            assert "estimate" in estimate_dict


# =============================================================================
# Test Class: Performance Tests
# =============================================================================
class TestPerformance:
    """Test performance aspects."""

    def test_repeated_field_access(self, basic_estimate):
        """Test repeated field access performance."""
        # Repeated access should be fast
        for _ in range(1000):
            _ = basic_estimate.name
            _ = basic_estimate.type
            _ = basic_estimate.description
            _ = basic_estimate.external_url
            _ = basic_estimate.intention
            _ = basic_estimate.tag

    def test_xml_generation_performance(self, basic_estimate):
        """Test XML generation performance."""
        # Should generate XML without significant delay
        for _ in range(100):
            xml_element = basic_estimate.to_xml()
            assert xml_element is not None

    def test_dict_serialization_performance(self, basic_estimate):
        """Test dictionary serialization performance."""
        # Should serialize to dict without significant delay
        for _ in range(100):
            result = basic_estimate.to_dict()
            assert isinstance(result, dict)


# =============================================================================
# Test Class: Boundary Value Tests
# =============================================================================
class TestBoundaryValues:
    """Test boundary value scenarios."""

    def test_empty_string_fields(self, empty_estimate):
        """Test empty string handling."""
        empty_estimate.name = ""
        empty_estimate.description = ""
        empty_estimate.tag = ""

        assert empty_estimate.name == ""
        assert empty_estimate.description == ""
        assert empty_estimate.tag == ""

        # XML should handle empty strings
        xml_element = empty_estimate.to_xml()
        assert xml_element.attrib["name"] == ""

    def test_url_edge_cases(self, empty_estimate):
        """Test URL edge cases."""
        # Very long URL
        long_url = "http://example.com/" + "a" * 1000
        empty_estimate.external_url = long_url
        assert str(empty_estimate.external_url) == long_url

        # URL with special characters
        special_url = "https://example.com/path?query=value&other=123#fragment"
        empty_estimate.external_url = special_url
        assert str(empty_estimate.external_url) == special_url

    def test_name_case_sensitivity_in_xml(self, empty_estimate):
        """Test that name case conversion works correctly."""
        test_cases = [
            ("lowercase", "LOWERCASE"),
            ("UPPERCASE", "UPPERCASE"),
            ("MixedCase", "MIXEDCASE"),
            ("with_underscores", "WITH_UNDERSCORES"),
            ("with-dashes", "WITH-DASHES"),
        ]

        for input_name, expected_xml_name in test_cases:
            empty_estimate.name = input_name
            empty_estimate.type = ArrayDTypeEnum.real_type
            xml_element = empty_estimate.to_xml()
            assert xml_element.attrib["name"] == expected_xml_name
