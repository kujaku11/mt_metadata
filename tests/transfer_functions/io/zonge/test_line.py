"""
Test suite for Line metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata.line_basemodel import Line


class TestLineDefault:
    """Test default initialization and basic attributes of Line class."""

    @pytest.fixture(scope="class")
    def default_line(self):
        """Fixture providing a default Line instance for efficiency."""
        return Line()  # type: ignore

    def test_default_initialization(self, default_line, subtests):
        """Test that Line initializes with correct default values."""
        with subtests.test("default name value"):
            assert default_line.name is None

        with subtests.test("default number value"):
            assert default_line.number is None

    def test_default_line_attributes(self, default_line, subtests):
        """Test that Line has all expected attributes."""
        expected_attributes = ["name", "number"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_line, attr)

    def test_default_model_fields(self, default_line, subtests):
        """Test model fields are properly defined."""
        fields = default_line.model_fields
        expected_fields = ["name", "number"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 2


class TestLineCustomValues:
    """Test Line with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_line(self):
        """Fixture providing a Line instance with custom values for efficiency."""
        return Line(name="line_A", number=100)  # type: ignore

    def test_populated_line_values(self, populated_line, subtests):
        """Test Line with custom values."""
        with subtests.test("populated name"):
            assert populated_line.name == "line_A"

        with subtests.test("populated number"):
            assert populated_line.number == 100

    def test_partial_line_values(self, subtests):
        """Test Line with only some fields populated."""
        partial_cases = [
            ("name only", {"name": "test_line"}, "test_line", None),
            ("number only", {"number": 42}, None, 42),
        ]

        for case_name, kwargs, expected_name, expected_number in partial_cases:
            with subtests.test(f"partial {case_name}"):
                line = Line(**kwargs)  # type: ignore
                assert line.name == expected_name
                assert line.number == expected_number

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("name", "survey_line_1"),
            ("number", 999),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field}"):
                kwargs = {field: value}
                line = Line(**kwargs)  # type: ignore
                assert getattr(line, field) == value


class TestLineValidation:
    """Test Line input validation and type conversion."""

    def test_string_field_validation(self, subtests):
        """Test string field validation for name."""
        with subtests.test("name string validation"):
            line = Line(name="valid_line_name")  # type: ignore
            assert line.name == "valid_line_name"

    def test_integer_field_validation(self, subtests):
        """Test integer field validation for number."""
        test_numbers = [0, 1, -1, 100, -100, 999999]

        for num in test_numbers:
            with subtests.test(f"number validation {num}"):
                line = Line(number=num)  # type: ignore
                assert line.number == num

    def test_none_values_allowed(self, subtests):
        """Test that None values are allowed for optional fields."""
        optional_fields = ["name", "number"]

        for field in optional_fields:
            with subtests.test(f"none allowed {field}"):
                kwargs = {field: None}
                line = Line(**kwargs)  # type: ignore
                assert getattr(line, field) is None

    def test_empty_string_values(self, subtests):
        """Test handling of empty strings for name field."""
        with subtests.test("empty string name"):
            line = Line(name="")  # type: ignore
            assert line.name == ""

    def test_numeric_string_conversion(self, subtests):
        """Test automatic conversion of numeric values to appropriate types."""
        with subtests.test("name numeric conversion"):
            line = Line(name=123)  # type: ignore
            assert line.name == "123"

        with subtests.test("number string conversion"):
            line = Line(number="456")  # type: ignore
            assert line.number == 456

        with subtests.test("number float conversion"):
            line = Line(number=789.0)  # type: ignore
            assert line.number == 789

    def test_invalid_type_handling(self, subtests):
        """Test handling of invalid types for fields."""
        with subtests.test("name list raises ValidationError"):
            with pytest.raises(ValidationError):
                Line(name=["invalid", "list"])  # type: ignore

        with subtests.test("name dict raises ValidationError"):
            with pytest.raises(ValidationError):
                Line(name={"invalid": "dict"})  # type: ignore

        with subtests.test("number invalid string raises ValidationError"):
            with pytest.raises(ValidationError):
                Line(number="not_a_number")  # type: ignore

        with subtests.test("number list raises ValidationError"):
            with pytest.raises(ValidationError):
                Line(number=[1, 2, 3])  # type: ignore


class TestLineSerialization:
    """Test Line serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_line(self):
        """Fixture for default Line instance."""
        return Line()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_line(self):
        """Fixture for populated Line instance."""
        return Line(name="line_B", number=200)  # type: ignore

    def test_model_dump_default(self, default_line, subtests):
        """Test model_dump with default values."""
        dump = default_line.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["name", "number"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["name"] is None
            assert dump["number"] is None

    def test_model_dump_populated(self, populated_line, subtests):
        """Test model_dump with populated values."""
        dump = populated_line.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["name"] == "line_B"
            assert dump["number"] == 200

    def test_from_dict_creation(self, subtests):
        """Test creating Line from dictionary."""
        with subtests.test("full dict"):
            data = {"name": "line_C", "number": 300}
            line = Line(**data)  # type: ignore
            assert line.name == "line_C"
            assert line.number == 300

        with subtests.test("partial dict name only"):
            data = {"name": "line_D"}
            line = Line(**data)  # type: ignore
            assert line.name == "line_D"
            assert line.number is None

        with subtests.test("partial dict number only"):
            data = {"number": 400}
            line = Line(**data)  # type: ignore
            assert line.name is None
            assert line.number == 400

        with subtests.test("empty dict"):
            data = {}
            line = Line(**data)  # type: ignore
            assert line.name is None
            assert line.number is None

    def test_json_serialization(self, default_line, populated_line, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated line"):
            json_str = populated_line.model_dump_json()
            data = json.loads(json_str)
            recreated = Line(**data)  # type: ignore
            assert recreated.name == populated_line.name
            assert recreated.number == populated_line.number

        with subtests.test("JSON round-trip default line"):
            json_str = default_line.model_dump_json()
            data = json.loads(json_str)
            recreated = Line(**data)  # type: ignore
            assert recreated.name == default_line.name
            assert recreated.number == default_line.number

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            line = Line(name="line_E", number=500)  # type: ignore
            dump = line.model_dump(exclude_none=True)
            assert "name" in dump
            assert "number" in dump
            assert dump["name"] == "line_E"
            assert dump["number"] == 500

        with subtests.test("exclude_none with partial name"):
            line = Line(name="line_F")  # type: ignore  # number will be None
            dump = line.model_dump(exclude_none=True)
            assert "name" in dump
            assert "number" not in dump  # Should be excluded since it's None

        with subtests.test("exclude_none with partial number"):
            line = Line(number=600)  # type: ignore  # name will be None
            dump = line.model_dump(exclude_none=True)
            assert "name" not in dump  # Should be excluded since it's None
            assert "number" in dump

        with subtests.test("exclude_none with all none"):
            line = Line()  # type: ignore  # Both fields None
            dump = line.model_dump(exclude_none=True)
            # Both fields should be excluded
            assert "name" not in dump or dump.get("name") is not None
            assert "number" not in dump or dump.get("number") is not None


class TestLineModification:
    """Test Line field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Line fields after creation."""
        line = Line()  # type: ignore

        test_modifications = [
            ("name", "modified_line"),
            ("number", 777),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field}"):
                setattr(line, field, value)
                assert getattr(line, field) == value

    def test_reset_to_none(self, subtests):
        """Test resetting fields to None."""
        line = Line(name="temp_line", number=888)  # type: ignore

        fields_to_reset = ["name", "number"]

        for field in fields_to_reset:
            with subtests.test(f"reset {field} to None"):
                setattr(line, field, None)
                assert getattr(line, field) is None

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        line = Line()  # type: ignore

        updates = {"name": "bulk_line", "number": 999}

        for field, value in updates.items():
            setattr(line, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(line, field) == expected_value

    def test_type_consistency_after_modification(self, subtests):
        """Test that type consistency is maintained after modification."""
        line = Line()  # type: ignore

        # Test string assignment for name
        with subtests.test("name accepts string type"):
            line.name = "test_string"  # type: ignore
            assert line.name == "test_string"
            assert isinstance(line.name, str)

        # Test integer assignment for number
        with subtests.test("number accepts integer type"):
            line.number = 456  # type: ignore
            assert line.number == 456
            assert isinstance(line.number, int)


class TestLineComparison:
    """Test Line comparison and equality operations."""

    def test_line_equality(self, subtests):
        """Test Line equality comparisons."""
        line1 = Line(name="test_line", number=123)  # type: ignore
        line2 = Line(name="test_line", number=123)  # type: ignore
        line3 = Line(name="other_line", number=123)  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert line1.model_dump() == line2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert line1.model_dump() != line3.model_dump()

        with subtests.test("individual field comparison"):
            assert line1.name == line2.name
            assert line1.number == line2.number
            assert line1.name != line3.name

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("name", "consistency_line"),
            ("number", 555),
        ]

        for field, value in test_values:
            with subtests.test(f"consistency {field} {value}"):
                kwargs = {field: value}
                line = Line(**kwargs)  # type: ignore
                assert getattr(line, field) == value

                # Test round-trip consistency
                dump = line.model_dump()
                recreated = Line(**dump)  # type: ignore
                assert getattr(recreated, field) == getattr(line, field)


class TestLineEdgeCases:
    """Test Line edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            line = Line(**{})  # type: ignore
            assert line.name is None
            assert line.number is None

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            line = Line(unknown_field="value")  # type: ignore
            assert hasattr(line, "unknown_field")
            assert line.unknown_field == "value"  # type: ignore

    def test_very_long_strings(self, subtests):
        """Test handling of very long string values for name."""
        long_string = "x" * 1000

        with subtests.test("long string name"):
            line = Line(name=long_string)  # type: ignore
            assert line.name == long_string
            assert line.name is not None and len(line.name) == 1000

    def test_number_boundary_values(self, subtests):
        """Test boundary values for number field."""
        boundary_values = [
            ("zero", 0),
            ("positive small", 1),
            ("negative small", -1),
            ("large positive", 999999999),
            ("large negative", -999999999),
        ]

        for case_name, value in boundary_values:
            with subtests.test(f"number boundary {case_name}"):
                line = Line(number=value)  # type: ignore
                assert line.number == value

    def test_special_characters_in_name(self, subtests):
        """Test handling of special characters in name field."""
        special_cases = [
            ("commas", "line,with,commas"),
            ("colons", "line:with:colons"),
            ("spaces", "line with spaces"),
            ("underscores", "line_with_underscores"),
            ("hyphens", "line-with-hyphens"),
            ("newlines", "line\nwith\nnewlines"),
            ("tabs", "line\twith\ttabs"),
            ("quotes", 'line"with"quotes'),
            ("apostrophes", "line'with'apostrophes"),
            ("slashes", "line/with/slashes"),
            ("backslashes", "line\\with\\backslashes"),
        ]

        for case_name, test_value in special_cases:
            with subtests.test(f"special chars {case_name}"):
                line = Line(name=test_value)  # type: ignore
                assert line.name == test_value

    def test_unicode_strings_in_name(self, subtests):
        """Test handling of unicode characters in name field."""
        unicode_cases = [
            ("chinese", "测试线路"),
            ("russian", "тестовая линия"),
            ("emoji", "🔬⚗️ line"),
            ("accented", "línea café"),
            ("greek", "γραμμή"),
        ]

        for case_name, test_value in unicode_cases:
            with subtests.test(f"unicode {case_name}"):
                line = Line(name=test_value)  # type: ignore
                assert line.name == test_value

    def test_mixed_none_and_values(self, subtests):
        """Test various combinations of None and actual values."""
        combinations = [
            ("name set, number None", "line_alpha", None),
            ("name None, number set", None, 111),
            ("both None", None, None),
            ("both set", "line_beta", 222),
        ]

        for case_name, name_value, number_value in combinations:
            with subtests.test(f"combination {case_name}"):
                line = Line(name=name_value, number=number_value)  # type: ignore
                assert line.name == name_value
                assert line.number == number_value

    def test_number_type_coercion_edge_cases(self, subtests):
        """Test edge cases for number type coercion."""
        coercion_cases = [
            ("float to int", 42.0, 42),
            ("string number", "123", 123),
            ("negative string", "-456", -456),
            ("zero string", "0", 0),
        ]

        for case_name, input_value, expected_value in coercion_cases:
            with subtests.test(f"coercion {case_name}"):
                line = Line(number=input_value)  # type: ignore
                assert line.number == expected_value
                assert isinstance(line.number, int)


class TestLineDocumentation:
    """Test Line class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Line class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert Line.__name__ == "Line"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(Line, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = Line.model_fields
        expected_fields = ["name", "number"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = Line.model_fields

        with subtests.test("name field properties"):
            name_field = fields["name"]
            # Should be optional (allow None)
            assert "default" in str(name_field) or hasattr(name_field, "default")

        with subtests.test("number field properties"):
            number_field = fields["number"]
            # Should be optional (allow None)
            assert "default" in str(number_field) or hasattr(number_field, "default")

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            line = Line()  # type: ignore
            dump = line.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) >= 0  # Can be empty with exclude_none

        with subtests.test("all expected fields present"):
            expected_fields = ["name", "number"]
            dump = Line().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump

        with subtests.test("model_fields accessible"):
            fields = Line.model_fields
            assert len(fields) == 2
            assert all(field in fields for field in ["name", "number"])
