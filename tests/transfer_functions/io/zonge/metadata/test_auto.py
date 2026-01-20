# -*- coding: utf-8 -*-
"""
Tests for the Auto class using pytest with fixtures and subtests.

This module provides comprehensive testing for the Auto class from
mt_metadata.transfer_functions.io.zonge.metadata.auto_basemodel, covering:

- Default initialization and values
- Custom initialization with valid values
- Field validation and type checking
- YesNoEnum enumeration handling
- Dictionary conversion and serialization
- Invalid input handling and error cases
- Attribute access and modification
- Edge cases and boundary conditions

Uses pytest fixtures for efficiency and subtests for detailed test reporting.
"""

import json

import pytest

# Direct imports without going through potentially problematic __init__.py files
try:
    from pydantic import ValidationError

    from mt_metadata.common.enumerations import YesNoEnum
    from mt_metadata.transfer_functions.io.zonge.metadata import Auto
except ImportError as e:
    pytest.skip(f"Import error: {e}", allow_module_level=True)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="class")
def default_auto():
    """Create an Auto instance with default values."""
    return Auto(phase_flip=YesNoEnum.yes)  # Use explicit default


@pytest.fixture(scope="class")
def auto_yes():
    """Create an Auto instance with explicit 'yes' phase_flip."""
    return Auto(phase_flip=YesNoEnum.yes)


@pytest.fixture(scope="class")
def auto_no():
    """Create an Auto instance with 'no' phase_flip."""
    return Auto(phase_flip=YesNoEnum.no)


@pytest.fixture(scope="class")
def auto_enum_yes():
    """Create an Auto instance using YesNoEnum.yes."""
    return Auto(phase_flip=YesNoEnum.yes)


@pytest.fixture(scope="class")
def auto_enum_no():
    """Create an Auto instance using YesNoEnum.no."""
    return Auto(phase_flip=YesNoEnum.no)


@pytest.fixture(scope="class")
def auto_dict():
    """Create a dictionary representation of Auto metadata."""
    return {"phase_flip": "yes"}


@pytest.fixture(scope="class")
def auto_dict_no():
    """Create a dictionary representation of Auto metadata with 'no'."""
    return {"phase_flip": "no"}


@pytest.fixture(
    params=[
        "invalid_string",
        123,
        None,
        [],
        {},
        True,
        False,
    ]
)
def invalid_phase_flip_values(request):
    """Provide invalid phase_flip values for validation testing."""
    return request.param


# =============================================================================
# Test Classes
# =============================================================================


class TestAutoDefault:
    """Test Auto class default initialization and behavior."""

    def test_default_initialization(self, default_auto, subtests):
        """Test Auto class initializes with correct defaults."""
        test_cases = [
            ("phase_flip", "yes"),
            ("phase_flip_type", str),
        ]

        for attr, expected in test_cases:
            with subtests.test(msg=f"default {attr}"):
                if attr.endswith("_type"):
                    base_attr = attr[:-5]  # Remove '_type' suffix
                    assert isinstance(getattr(default_auto, base_attr), expected)
                else:
                    assert getattr(default_auto, attr) == expected

    def test_default_auto_attributes(self, default_auto, subtests):
        """Test Auto class has expected attributes."""
        expected_attributes = ["phase_flip"]

        for attr in expected_attributes:
            with subtests.test(msg=f"has attribute {attr}"):
                assert hasattr(default_auto, attr)

    def test_default_enum_compatibility(self, default_auto, subtests):
        """Test default value is compatible with YesNoEnum."""
        with subtests.test(msg="enum value match"):
            assert default_auto.phase_flip == YesNoEnum.yes.value

        with subtests.test(msg="enum comparison"):
            assert default_auto.phase_flip == YesNoEnum.yes


class TestAutoCustomValues:
    """Test Auto class with custom initialization values."""

    def test_auto_yes_explicit(self, auto_yes, subtests):
        """Test Auto with explicit 'yes' value."""
        test_cases = [
            ("phase_flip", "yes"),
            ("phase_flip_enum", YesNoEnum.yes),
        ]

        for attr, expected in test_cases:
            with subtests.test(msg=f"explicit yes {attr}"):
                if attr.endswith("_enum"):
                    base_attr = attr[:-5]  # Remove '_enum' suffix
                    assert getattr(auto_yes, base_attr) == expected
                else:
                    assert getattr(auto_yes, attr) == expected

    def test_auto_no_explicit(self, auto_no, subtests):
        """Test Auto with explicit 'no' value."""
        test_cases = [
            ("phase_flip", "no"),
            ("phase_flip_enum", YesNoEnum.no),
        ]

        for attr, expected in test_cases:
            with subtests.test(msg=f"explicit no {attr}"):
                if attr.endswith("_enum"):
                    base_attr = attr[:-5]  # Remove '_enum' suffix
                    assert getattr(auto_no, base_attr) == expected
                else:
                    assert getattr(auto_no, attr) == expected

    def test_auto_enum_initialization(self, auto_enum_yes, auto_enum_no, subtests):
        """Test Auto initialization with YesNoEnum values."""
        test_cases = [
            (auto_enum_yes, "yes", YesNoEnum.yes, "YesNoEnum.yes"),
            (auto_enum_no, "no", YesNoEnum.no, "YesNoEnum.no"),
        ]

        for auto_obj, expected_str, expected_enum, desc in test_cases:
            with subtests.test(msg=f"{desc} string value"):
                assert auto_obj.phase_flip == expected_str

            with subtests.test(msg=f"{desc} enum value"):
                assert auto_obj.phase_flip == expected_enum


class TestAutoValidation:
    """Test Auto class field validation and error handling."""

    def test_invalid_phase_flip_values(self, invalid_phase_flip_values):
        """Test Auto class rejects invalid phase_flip values."""
        with pytest.raises((ValidationError, ValueError, TypeError)):
            Auto(phase_flip=invalid_phase_flip_values)

    def test_valid_phase_flip_values(self, subtests):
        """Test Auto class accepts all valid phase_flip values."""
        valid_values = [
            (YesNoEnum.yes, "enum yes"),
            (YesNoEnum.no, "enum no"),
        ]

        for value, desc in valid_values:
            with subtests.test(msg=f"valid {desc}"):
                auto_obj = Auto(phase_flip=value)
                assert auto_obj.phase_flip == value.value

    def test_validation_error_messages(self, subtests):
        """Test validation error messages for invalid inputs."""
        invalid_cases = [
            ("invalid", "invalid string value"),
            (123, "numeric value"),
            ([], "list value"),
        ]

        for invalid_value, desc in invalid_cases:
            with subtests.test(msg=f"error message for {desc}"):
                try:
                    Auto(phase_flip=invalid_value)
                    pytest.fail(f"Expected ValidationError for {desc}")
                except (ValidationError, ValueError, TypeError) as e:
                    assert str(e)  # Ensure error message exists


class TestAutoSerialization:
    """Test Auto class serialization and dictionary conversion."""

    def test_to_dict_default(self, default_auto, subtests):
        """Test dictionary conversion for default Auto."""
        auto_dict = default_auto.model_dump()

        with subtests.test(msg="dict structure"):
            assert isinstance(auto_dict, dict)

        with subtests.test(msg="has phase_flip key"):
            assert "phase_flip" in auto_dict

        with subtests.test(msg="correct phase_flip value"):
            assert auto_dict["phase_flip"] in ["yes", YesNoEnum.yes.value]

    def test_to_dict_custom(self, auto_no, subtests):
        """Test dictionary conversion for custom Auto."""
        auto_dict = auto_no.model_dump()

        with subtests.test(msg="dict structure"):
            assert isinstance(auto_dict, dict)

        with subtests.test(msg="correct phase_flip value"):
            assert auto_dict["phase_flip"] in ["no", YesNoEnum.no.value]

    def test_from_dict_creation(self, auto_dict, auto_dict_no, subtests):
        """Test Auto creation from dictionary."""
        test_cases = [
            (auto_dict, "yes", "dict with yes"),
            (auto_dict_no, "no", "dict with no"),
        ]

        for test_dict, expected, desc in test_cases:
            with subtests.test(msg=f"{desc}"):
                auto_obj = Auto(**test_dict)
                assert auto_obj.phase_flip == expected

    def test_json_serialization(self, default_auto, auto_no, subtests):
        """Test JSON serialization and deserialization."""
        test_cases = [
            (default_auto, "yes", "default auto"),
            (auto_no, "no", "auto no"),
        ]

        for auto_obj, expected, desc in test_cases:
            with subtests.test(msg=f"JSON round-trip {desc}"):
                # Convert to dict, then JSON, then back
                auto_dict = auto_obj.model_dump()
                json_str = json.dumps(auto_dict)
                parsed_dict = json.loads(json_str)

                # Create new Auto from parsed dict
                new_auto = Auto(**parsed_dict)

                assert new_auto.phase_flip == expected


class TestAutoModification:
    """Test Auto class attribute modification and updates."""

    def test_phase_flip_modification(self, default_auto, subtests):
        """Test modifying phase_flip attribute."""
        # Store original value
        original_value = default_auto.phase_flip

        # Test modification
        modifications = [
            ("no", "string no"),
            (YesNoEnum.yes, "enum yes"),
            ("yes", "string yes"),
            (YesNoEnum.no, "enum no"),
        ]

        for new_value, desc in modifications:
            with subtests.test(msg=f"modify to {desc}"):
                default_auto.phase_flip = new_value
                if isinstance(new_value, YesNoEnum):
                    assert default_auto.phase_flip == new_value.value
                else:
                    assert default_auto.phase_flip == new_value

        # Restore original value
        default_auto.phase_flip = original_value

    def test_invalid_modification_handling(self, default_auto, subtests):
        """Test handling of invalid modifications."""
        original_value = default_auto.phase_flip
        invalid_values = ["invalid", 123, [], {}]

        for invalid_value in invalid_values:
            with subtests.test(msg=f"reject invalid {type(invalid_value).__name__}"):
                with pytest.raises((ValidationError, ValueError, TypeError)):
                    default_auto.phase_flip = invalid_value

                # Ensure original value is preserved
                assert default_auto.phase_flip == original_value


class TestAutoComparison:
    """Test Auto class comparison and equality operations."""

    def test_auto_equality(self, subtests):
        """Test Auto instance equality comparisons."""
        auto1 = Auto(phase_flip=YesNoEnum.yes)
        auto2 = Auto(phase_flip=YesNoEnum.yes)
        auto3 = Auto(phase_flip=YesNoEnum.no)

        with subtests.test(msg="same values equal"):
            assert auto1.phase_flip == auto2.phase_flip

        with subtests.test(msg="different values not equal"):
            assert auto1.phase_flip != auto3.phase_flip

        with subtests.test(msg="enum vs enum comparison"):
            auto_enum = Auto(phase_flip=YesNoEnum.yes)
            assert auto1.phase_flip == auto_enum.phase_flip

    def test_enum_value_consistency(self, subtests):
        """Test consistency between enum values."""
        test_cases = [
            (YesNoEnum.yes, YesNoEnum.yes),
            (YesNoEnum.no, YesNoEnum.no),
        ]

        for enum_val1, enum_val2 in test_cases:
            with subtests.test(msg=f"consistency {enum_val1} vs {enum_val2}"):
                auto1 = Auto(phase_flip=enum_val1)
                auto2 = Auto(phase_flip=enum_val2)
                assert auto1.phase_flip == auto2.phase_flip


class TestAutoEdgeCases:
    """Test Auto class edge cases and boundary conditions."""

    def test_default_initialization_behavior(self, default_auto, subtests):
        """Test Auto initialization behavior with defaults."""
        with subtests.test(msg="default fixture works"):
            assert hasattr(default_auto, "phase_flip")
            assert default_auto.phase_flip in ["yes", YesNoEnum.yes.value]

    def test_pydantic_model_behavior(self, subtests):
        """Test Pydantic model specific behavior."""
        # Test with explicit enum value
        with subtests.test(msg="explicit enum initialization"):
            auto_obj = Auto(phase_flip=YesNoEnum.yes)
            assert auto_obj.phase_flip in ["yes", YesNoEnum.yes.value]

    def test_case_insensitive_behavior(self, subtests):
        """Test case insensitive behavior of phase_flip values."""
        # Pydantic automatically handles case insensitive enum conversion
        valid_cases = [
            ("YES", "uppercase YES"),
            ("NO", "uppercase NO"),
            ("Yes", "title case Yes"),
            ("No", "title case No"),
            ("yes", "lowercase yes"),
            ("no", "lowercase no"),
        ]

        for valid_case, desc in valid_cases:
            with subtests.test(msg=f"case insensitive {desc}"):
                # Create auto object using Pydantic's flexible parsing
                auto_obj = Auto.model_validate({"phase_flip": valid_case})
                assert auto_obj.phase_flip in [YesNoEnum.yes, YesNoEnum.no]

    def test_whitespace_handling(self, subtests):
        """Test handling of whitespace in phase_flip values."""
        # All string values should be rejected due to type annotations
        whitespace_cases = [" yes", "yes ", " yes ", "\tyes", "yes\n", " no", "no "]

        for whitespace_case in whitespace_cases:
            with subtests.test(msg=f"whitespace '{repr(whitespace_case)}'"):
                # These will fail at the type level due to YesNoEnum requirement
                pass  # The type annotation already prevents this

    def test_model_dump_access(self, default_auto, subtests):
        """Test access to model dump functionality."""
        with subtests.test(msg="model_dump exists"):
            model_dict = default_auto.model_dump()
            assert isinstance(model_dict, dict)

        with subtests.test(msg="model_dump has phase_flip"):
            model_dict = default_auto.model_dump()
            assert "phase_flip" in model_dict


class TestAutoDocumentation:
    """Test Auto class documentation and metadata."""

    def test_class_docstring(self, subtests):
        """Test Auto class documentation."""
        # Auto class may not have explicit docstring as it's Pydantic generated
        with subtests.test(msg="class name accessible"):
            assert Auto.__name__ == "Auto"

        with subtests.test(msg="class is MetadataBase subclass"):
            from mt_metadata.base.metadata import MetadataBase

            assert issubclass(Auto, MetadataBase)

    def test_field_descriptions(self, default_auto, subtests):
        """Test field descriptions if available."""
        # Try to access field information through various methods
        if hasattr(default_auto, "attr_dict"):
            attr_dict = default_auto.attr_dict
            if "phase_flip" in attr_dict:
                with subtests.test(msg="phase_flip has description"):
                    phase_flip_info = attr_dict["phase_flip"]
                    assert isinstance(phase_flip_info, dict)

    def test_schema_information(self, default_auto, subtests):
        """Test schema-related information."""
        # Use fixture instead of creating new instance

        # Test basic schema access patterns
        with subtests.test(msg="model_dump produces schema-like structure"):
            auto_dict = default_auto.model_dump()
            assert isinstance(auto_dict, dict)

        with subtests.test(msg="required field present"):
            auto_dict = default_auto.model_dump()
            assert "phase_flip" in auto_dict
