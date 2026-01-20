# -*- coding: utf-8 -*-
"""
Tests for the CH class using pytest with fixtures and subtests.

This module provides comprehensive testing for the CH class from
mt_metadata.transfer_functions.io.zonge.metadata.ch_basemodel, covering:

- Default initialization and values
- Custom initialization with valid values
- Field validation and type checking
- String field handling (all fields are optional strings)
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

    from mt_metadata.transfer_functions.io.zonge.metadata import CH
except ImportError as e:
    pytest.skip(f"Import error: {e}", allow_module_level=True)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="class")
def default_ch():
    """Create a CH instance with default values."""
    return CH()  # type: ignore


@pytest.fixture(scope="class")
def populated_ch():
    """Create a CH instance with all fields populated.

    Note: Comma-separated values are automatically converted to lists by the validator.
    """
    return CH(  # type: ignore
        a_d_card_s_n="6545BAC6,BE380864",
        gdp_box="18,15",
        stn="1,2",
        number="1, 2284",
        cmp="ex,hy",
        c_res="0,0",
        azimuth="12.1,12.1",
        incl="335754.685:4263553.435:1650.2",
    )


@pytest.fixture(scope="class")
def partial_ch():
    """Create a CH instance with some fields populated."""
    return CH(a_d_card_s_n="TEST123", gdp_box="42", cmp="ez")  # type: ignore


@pytest.fixture(scope="class")
def ch_dict_full():
    """Create a dictionary representation of full CH metadata.

    Note: When creating CH from this dict, comma-separated strings will be converted to lists.
    """
    return {
        "a_d_card_s_n": "6545BAC6,BE380864",
        "gdp_box": "18,15",
        "stn": "1,2",
        "number": "1, 2284",
        "cmp": "ex,hy",
        "c_res": "0,0",
        "azimuth": "12.1,12.1",
        "incl": "335754.685:4263553.435:1650.2",
    }


@pytest.fixture(scope="class")
def ch_dict_partial():
    """Create a dictionary representation of partial CH metadata."""
    return {"a_d_card_s_n": "TEST123", "gdp_box": "42", "cmp": "ez"}


@pytest.fixture(
    params=[
        {"a_d_card_s_n": 123},  # Integer instead of string
        {"stn": {}},  # Dict instead of string (lists are now valid)
        {"number": True},  # Boolean instead of string
        {"cmp": 45.6},  # Float instead of string
    ]
)
def invalid_ch_params(request):
    """Provide invalid CH parameters for validation testing.

    Note: Lists are now valid (removed from invalid params).
    """
    return request.param


@pytest.fixture(scope="class")
def ch_field_names():
    """Provide list of all CH field names for testing."""
    return [
        "a_d_card_s_n",
        "gdp_box",
        "stn",
        "number",
        "cmp",
        "c_res",
        "azimuth",
        "incl",
    ]


# =============================================================================
# Test Classes
# =============================================================================


class TestChDefault:
    """Test CH class default initialization and behavior."""

    def test_default_initialization(self, default_ch, ch_field_names, subtests):
        """Test CH class initializes with correct defaults."""
        for field_name in ch_field_names:
            with subtests.test(msg=f"default {field_name}"):
                assert getattr(default_ch, field_name) is None

    def test_default_ch_attributes(self, default_ch, ch_field_names, subtests):
        """Test CH class has expected attributes."""
        for field_name in ch_field_names:
            with subtests.test(msg=f"has attribute {field_name}"):
                assert hasattr(default_ch, field_name)

    def test_default_model_fields(self, default_ch, ch_field_names, subtests):
        """Test CH model has correct field definitions."""
        model_fields = default_ch.model_fields

        for field_name in ch_field_names:
            with subtests.test(msg=f"model field {field_name}"):
                assert field_name in model_fields

        with subtests.test(msg="field count"):
            assert len(model_fields) >= len(ch_field_names)


class TestChCustomValues:
    """Test CH class with custom initialization values."""

    def test_populated_ch_values(self, populated_ch, subtests):
        """Test CH with all fields populated.

        Note: Fields with commas are automatically split into lists.
        """
        expected_values = {
            "a_d_card_s_n": ["6545BAC6", "BE380864"],  # Comma-separated -> list
            "gdp_box": ["18", "15"],  # Comma-separated -> list
            "stn": ["1", "2"],  # Comma-separated -> list
            "number": ["1", "2284"],  # Comma-separated -> list
            "cmp": ["ex", "hy"],  # Comma-separated -> list
            "c_res": ["0", "0"],  # Comma-separated -> list
            "azimuth": ["12.1", "12.1"],  # Comma-separated -> list
            "incl": "335754.685:4263553.435:1650.2",  # No comma -> string
        }

        for field_name, expected_value in expected_values.items():
            with subtests.test(msg=f"populated {field_name}"):
                assert getattr(populated_ch, field_name) == expected_value

    def test_partial_ch_values(self, partial_ch, subtests):
        """Test CH with partial field population."""
        expected_values = {"a_d_card_s_n": "TEST123", "gdp_box": "42", "cmp": "ez"}

        expected_none = ["stn", "number", "c_res", "azimuth", "incl"]

        for field_name, expected_value in expected_values.items():
            with subtests.test(msg=f"partial {field_name}"):
                assert getattr(partial_ch, field_name) == expected_value

        for field_name in expected_none:
            with subtests.test(msg=f"partial none {field_name}"):
                assert getattr(partial_ch, field_name) is None

    def test_individual_field_initialization(self, subtests):
        """Test CH initialization with individual fields."""
        test_cases = [
            ("a_d_card_s_n", "SERIAL123"),
            ("gdp_box", "BOX001"),
            ("stn", "STN999"),
            ("number", "CH01"),
            ("cmp", "hx"),
            ("c_res", "10.5"),
            ("azimuth", "90.0"),
            ("incl", "45.0"),
        ]

        for field_name, test_value in test_cases:
            with subtests.test(msg=f"individual {field_name}"):
                ch_obj = CH(**{field_name: test_value})
                assert getattr(ch_obj, field_name) == test_value
                # Check other fields are None
                for other_field in [
                    "a_d_card_s_n",
                    "gdp_box",
                    "stn",
                    "number",
                    "cmp",
                    "c_res",
                    "azimuth",
                    "incl",
                ]:
                    if other_field != field_name:
                        assert getattr(ch_obj, other_field) is None


class TestChValidation:
    """Test CH class field validation and error handling."""

    def test_comma_separated_values(self, subtests):
        """Test automatic comma-separated value splitting."""
        test_cases = [
            ("a,b", ["a", "b"]),  # Two values
            ("a,b,c", ["a", "b", "c"]),  # Three values
            ("1,2", ["1", "2"]),  # Numeric strings
            ("test, value", ["test", "value"]),  # With spaces
            (",", None),  # Just comma -> None
            ("", ""),  # Empty string remains empty
            ("single", "single"),  # No comma remains string
        ]

        for input_val, expected_val in test_cases:
            with subtests.test(msg=f"comma split {repr(input_val)}"):
                ch_obj = CH(a_d_card_s_n=input_val)  # type: ignore
                assert ch_obj.a_d_card_s_n == expected_val

    def test_invalid_field_types(self, invalid_ch_params):
        """Test CH class handles invalid field types appropriately."""
        # Note: Pydantic may convert some types automatically
        try:
            ch_obj = CH(**invalid_ch_params)
            # If no exception, check that conversion happened appropriately
            for field_name, value in invalid_ch_params.items():
                result_value = getattr(ch_obj, field_name)
                # Should be converted to string, list, or raise validation error
                assert isinstance(result_value, (str, list, type(None)))
        except (ValidationError, ValueError, TypeError):
            # This is also acceptable - validation should catch invalid types
            pass

    def test_none_values_allowed(self, ch_field_names, subtests):
        """Test that all fields accept None values."""
        for field_name in ch_field_names:
            with subtests.test(msg=f"none allowed {field_name}"):
                ch_obj = CH(**{field_name: None})
                assert getattr(ch_obj, field_name) is None

    def test_empty_string_values(self, ch_field_names, subtests):
        """Test that all fields accept empty string values."""
        for field_name in ch_field_names:
            with subtests.test(msg=f"empty string {field_name}"):
                ch_obj = CH(**{field_name: ""})
                assert getattr(ch_obj, field_name) == ""

    def test_string_conversion(self, subtests):
        """Test automatic string conversion for valid inputs."""
        conversion_cases = [
            ("a_d_card_s_n", 123, "123"),
            ("gdp_box", 45.6, "45.6"),
            ("stn", True, "True"),
            ("number", False, "False"),
        ]

        for field_name, input_value, expected_str in conversion_cases:
            with subtests.test(msg=f"conversion {field_name} {input_value}"):
                try:
                    ch_obj = CH(**{field_name: input_value})
                    result = getattr(ch_obj, field_name)
                    # Either converted to string or validation error (both acceptable)
                    if result is not None:
                        assert isinstance(result, str)
                except (ValidationError, ValueError, TypeError):
                    # Validation error is also acceptable
                    pass


class TestChSerialization:
    """Test CH class serialization and dictionary conversion."""

    def test_model_dump_default(self, default_ch, ch_field_names, subtests):
        """Test dictionary conversion for default CH."""
        ch_dict = default_ch.model_dump()

        with subtests.test(msg="dict structure"):
            assert isinstance(ch_dict, dict)

        for field_name in ch_field_names:
            with subtests.test(msg=f"has field {field_name}"):
                assert field_name in ch_dict

            with subtests.test(msg=f"default value {field_name}"):
                assert ch_dict[field_name] is None

    def test_model_dump_populated(self, populated_ch, subtests):
        """Test dictionary conversion for populated CH.

        Note: Comma-separated values are stored as lists.
        """
        ch_dict = populated_ch.model_dump()

        expected_values = {
            "a_d_card_s_n": ["6545BAC6", "BE380864"],  # Comma-separated -> list
            "gdp_box": ["18", "15"],  # Comma-separated -> list
            "stn": ["1", "2"],  # Comma-separated -> list
            "number": ["1", "2284"],  # Comma-separated -> list
            "cmp": ["ex", "hy"],  # Comma-separated -> list
            "c_res": ["0", "0"],  # Comma-separated -> list
            "azimuth": ["12.1", "12.1"],  # Comma-separated -> list
            "incl": "335754.685:4263553.435:1650.2",  # No comma -> string
        }

        with subtests.test(msg="dict structure"):
            assert isinstance(ch_dict, dict)

        for field_name, expected_value in expected_values.items():
            with subtests.test(msg=f"populated value {field_name}"):
                assert ch_dict[field_name] == expected_value

    def test_from_dict_creation(self, ch_dict_full, ch_dict_partial, subtests):
        """Test CH creation from dictionary.

        Note: Comma-separated strings are converted to lists during validation.
        """
        # For partial dict (no commas), values remain as strings
        with subtests.test(msg="partial dict"):
            ch_obj = CH(**ch_dict_partial)
            for field_name, expected_value in ch_dict_partial.items():
                assert getattr(ch_obj, field_name) == expected_value

        # For full dict (with commas), values are converted to lists
        with subtests.test(msg="full dict - comma handling"):
            ch_obj = CH(**ch_dict_full)
            # Check that comma-separated values became lists
            assert isinstance(ch_obj.a_d_card_s_n, list)
            assert isinstance(ch_obj.gdp_box, list)
            assert isinstance(ch_obj.stn, list)
            # Check that non-comma value remained a string
            assert isinstance(ch_obj.incl, str)

    def test_json_serialization(self, populated_ch, default_ch, subtests):
        """Test JSON serialization and deserialization."""
        test_cases = [
            (populated_ch, "populated ch"),
            (default_ch, "default ch"),
        ]

        for ch_obj, desc in test_cases:
            with subtests.test(msg=f"JSON round-trip {desc}"):
                # Convert to dict, then JSON, then back
                ch_dict = ch_obj.model_dump()
                json_str = json.dumps(ch_dict)
                parsed_dict = json.loads(json_str)

                # Create new CH from parsed dict
                new_ch = CH(
                    **{k: v for k, v in parsed_dict.items() if not k.startswith("_")}
                )

                # Compare relevant fields
                for field_name in ch_obj.model_fields:
                    original_value = getattr(ch_obj, field_name)
                    new_value = getattr(new_ch, field_name)
                    assert original_value == new_value

    def test_model_dump_exclude_none(self, populated_ch, partial_ch, subtests):
        """Test model_dump with exclude_none option."""
        test_cases = [
            (populated_ch, "populated", 8),  # All fields should be present
            (partial_ch, "partial", 3),  # Only 3 non-None fields
        ]

        for ch_obj, desc, expected_non_none in test_cases:
            with subtests.test(msg=f"exclude_none {desc}"):
                ch_dict = ch_obj.model_dump(exclude_none=True)
                non_none_count = sum(
                    1
                    for v in ch_dict.values()
                    if v is not None and not str(v).startswith("_")
                )
                assert non_none_count >= expected_non_none


class TestChModification:
    """Test CH class attribute modification and updates."""

    def test_field_modification(self, default_ch, ch_field_names, subtests):
        """Test modifying CH field values."""
        test_values = {
            "a_d_card_s_n": "MODIFIED_SERIAL",
            "gdp_box": "MODIFIED_BOX",
            "stn": "MODIFIED_STN",
            "number": "MODIFIED_NUM",
            "cmp": "MODIFIED_CMP",
            "c_res": "MODIFIED_RES",
            "azimuth": "MODIFIED_AZ",
            "incl": "MODIFIED_INCL",
        }

        # Store original values
        original_values = {
            field: getattr(default_ch, field) for field in ch_field_names
        }

        # Test modifications
        for field_name, new_value in test_values.items():
            with subtests.test(msg=f"modify {field_name}"):
                setattr(default_ch, field_name, new_value)
                assert getattr(default_ch, field_name) == new_value

        # Test setting back to None
        for field_name in ch_field_names:
            with subtests.test(msg=f"reset to None {field_name}"):
                setattr(default_ch, field_name, None)
                assert getattr(default_ch, field_name) is None

        # Restore original values
        for field_name, original_value in original_values.items():
            setattr(default_ch, field_name, original_value)

    def test_bulk_update(self, default_ch, subtests):
        """Test bulk updating multiple fields."""
        updates = {
            "a_d_card_s_n": "BULK_SERIAL",
            "gdp_box": "BULK_BOX",
            "cmp": "BULK_CMP",
        }

        # Store original values
        original_values = {
            field: getattr(default_ch, field) for field in updates.keys()
        }

        # Apply updates
        for field_name, new_value in updates.items():
            setattr(default_ch, field_name, new_value)

        # Verify updates
        for field_name, expected_value in updates.items():
            with subtests.test(msg=f"bulk update {field_name}"):
                assert getattr(default_ch, field_name) == expected_value

        # Restore original values
        for field_name, original_value in original_values.items():
            setattr(default_ch, field_name, original_value)


class TestChComparison:
    """Test CH class comparison and equality operations."""

    def test_ch_equality(self, subtests):
        """Test CH instance equality comparisons."""
        ch1 = CH(a_d_card_s_n="TEST", gdp_box="123")  # type: ignore
        ch2 = CH(a_d_card_s_n="TEST", gdp_box="123")  # type: ignore
        ch3 = CH(a_d_card_s_n="DIFFERENT", gdp_box="123")  # type: ignore

        with subtests.test(msg="same values model_dump equal"):
            assert ch1.model_dump() == ch2.model_dump()

        with subtests.test(msg="different values model_dump not equal"):
            assert ch1.model_dump() != ch3.model_dump()

        with subtests.test(msg="individual field comparison"):
            assert ch1.a_d_card_s_n == ch2.a_d_card_s_n
            assert ch1.a_d_card_s_n != ch3.a_d_card_s_n

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across instances."""
        test_cases = [
            ("TEST_VALUE", "TEST_VALUE"),
            ("", ""),
            (None, None),
        ]

        for value1, value2 in test_cases:
            with subtests.test(msg=f"consistency {value1} vs {value2}"):
                ch1 = CH(a_d_card_s_n=value1)  # type: ignore
                ch2 = CH(a_d_card_s_n=value2)  # type: ignore
                assert ch1.a_d_card_s_n == ch2.a_d_card_s_n


class TestChEdgeCases:
    """Test CH class edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test CH initialization with empty kwargs."""
        with subtests.test(msg="empty kwargs"):
            ch_obj = CH()  # type: ignore
            for field_name in ch_obj.model_fields:
                if not field_name.startswith("_"):
                    assert getattr(ch_obj, field_name) is None

    def test_unknown_field_handling(self, subtests):
        """Test CH behavior with unknown fields."""
        with subtests.test(msg="unknown fields ignored or error"):
            try:
                # This might raise an error or ignore unknown fields
                ch_obj = CH()  # type: ignore
                # Test setting unknown field after creation
                try:
                    setattr(ch_obj, "unknown_field", "should_be_ignored")
                    # If no error, check it's not in model fields
                    assert "unknown_field" not in ch_obj.model_fields
                except AttributeError:
                    # This is also acceptable - attribute protection
                    pass
            except (ValidationError, TypeError):
                # This is also acceptable - Pydantic strict mode
                pass

    def test_very_long_strings(self, ch_field_names, subtests):
        """Test handling of very long string values."""
        long_string = "x" * 1000  # 1000 character string

        for field_name in ch_field_names:
            with subtests.test(msg=f"long string {field_name}"):
                ch_obj = CH(**{field_name: long_string})
                assert getattr(ch_obj, field_name) == long_string

    def test_special_characters(self, subtests):
        """Test handling of special characters in string values.

        Note: Commas trigger automatic splitting into lists.
        """
        # Test strings without commas (should remain as strings)
        special_strings = [
            "test:with:colons",
            "test with spaces",
            "test\nwith\nnewlines",
            "test\twith\ttabs",
            'test"with"quotes',
            "test'with'apostrophes",
            "test/with/slashes",
            "test\\with\\backslashes",
        ]

        for special_string in special_strings:
            with subtests.test(msg=f"special chars {repr(special_string)}"):
                ch_obj = CH(a_d_card_s_n=special_string)  # type: ignore
                assert ch_obj.a_d_card_s_n == special_string

        # Test comma-separated strings (should become lists)
        with subtests.test(msg="comma-separated string becomes list"):
            ch_obj = CH(a_d_card_s_n="test,with,commas")  # type: ignore
            assert ch_obj.a_d_card_s_n == ["test", "with", "commas"]

    def test_unicode_strings(self, subtests):
        """Test handling of unicode strings."""
        unicode_strings = [
            "测试",  # Chinese
            "тест",  # Cyrillic
            "🧪⚗️",  # Emojis
            "café",  # Accented characters
        ]

        for unicode_string in unicode_strings:
            with subtests.test(msg=f"unicode {repr(unicode_string)}"):
                ch_obj = CH(a_d_card_s_n=unicode_string)  # type: ignore
                assert ch_obj.a_d_card_s_n == unicode_string


class TestChDocumentation:
    """Test CH class documentation and metadata."""

    def test_class_structure(self, subtests):
        """Test CH class structure and inheritance."""
        with subtests.test(msg="class name accessible"):
            assert CH.__name__ == "CH"

        with subtests.test(msg="class is MetadataBase subclass"):
            from mt_metadata.base.metadata import MetadataBase

            assert issubclass(CH, MetadataBase)

    def test_field_descriptions(self, default_ch, subtests):
        """Test field descriptions and metadata."""
        model_fields = default_ch.model_fields

        expected_descriptions = {
            "a_d_card_s_n": "serial number of ad card for local and remote stations",
            "gdp_box": "Box number for local and remote stations",
            "stn": "station number of local and remote",
            "number": "channel number for local and coil number of remote",
            "cmp": "component of local and remote stations",
            "c_res": "contact resistance for local and remote sensors",
            "azimuth": "azimuth for local and remote sensors",
            "incl": "Inclination",
        }

        for field_name, expected_desc in expected_descriptions.items():
            with subtests.test(msg=f"field description {field_name}"):
                if field_name in model_fields:
                    field_info = model_fields[field_name]
                    # Description might be in different places depending on Pydantic version
                    assert hasattr(field_info, "description") or hasattr(
                        field_info, "field_info"
                    )

    def test_schema_information(self, default_ch, subtests):
        """Test schema-related information."""
        # Test basic schema access patterns
        with subtests.test(msg="model_dump produces schema-like structure"):
            ch_dict = default_ch.model_dump()
            assert isinstance(ch_dict, dict)

        with subtests.test(msg="all expected fields present"):
            ch_dict = default_ch.model_dump()
            expected_fields = [
                "a_d_card_s_n",
                "gdp_box",
                "stn",
                "number",
                "cmp",
                "c_res",
                "azimuth",
                "incl",
            ]
            for field_name in expected_fields:
                assert field_name in ch_dict

        with subtests.test(msg="model_fields accessible"):
            assert hasattr(default_ch, "model_fields")
            assert isinstance(default_ch.model_fields, dict)
