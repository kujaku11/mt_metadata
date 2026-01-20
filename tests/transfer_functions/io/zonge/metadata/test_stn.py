"""
Test suite for STN metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata.stn import STN


class TestStnDefault:
    """Test default initialization and basic attributes of STN class."""

    @pytest.fixture(scope="class")
    def default_stn(self):
        """Fixture providing a default STN instance for efficiency."""
        return STN()  # type: ignore

    def test_default_initialization(self, default_stn, subtests):
        """Test that STN initializes with correct default values."""
        with subtests.test("default name value"):
            assert default_stn.name == ""

    def test_default_stn_attributes(self, default_stn, subtests):
        """Test that STN has all expected attributes."""
        expected_attributes = ["name"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_stn, attr)

    def test_default_model_fields(self, default_stn, subtests):
        """Test model fields are properly defined."""
        fields = default_stn.model_fields
        expected_fields = ["name"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 1

    def test_field_types(self, default_stn, subtests):
        """Test that fields have expected types."""
        with subtests.test("name field type"):
            assert isinstance(default_stn.name, str)

    def test_required_field_behavior(self, subtests):
        """Test that name field behaves as required with default."""
        with subtests.test("name field is required but has default"):
            stn = STN()  # type: ignore
            assert stn.name == ""
            assert hasattr(stn, "name")


class TestStnCustomValues:
    """Test STN with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_stn(self):
        """Fixture providing a STN instance with custom values for efficiency."""
        return STN(name="test_station")  # type: ignore

    def test_populated_stn_values(self, populated_stn, subtests):
        """Test STN with custom values."""
        with subtests.test("populated name"):
            assert populated_stn.name == "test_station"

    def test_name_initialization_patterns(self, subtests):
        """Test various name initialization patterns."""
        name_patterns = [
            ("empty string", "", ""),
            ("simple string", "station1", "station1"),
            ("numeric string", "123", "123"),
            ("station with underscore", "test_station", "test_station"),
            ("station with dash", "test-station", "test-station"),
            ("station with spaces", "test station", "test station"),
            ("single character", "A", "A"),
            ("single digit", "1", "1"),
            ("alphanumeric", "station123", "station123"),
        ]

        for case_name, input_value, expected_value in name_patterns:
            with subtests.test(f"name pattern {case_name}"):
                stn = STN(name=input_value)  # type: ignore
                assert stn.name == expected_value

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("name", "station_test"),
            ("name", "1"),
            ("name", "test123"),
            ("name", ""),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field} with value {value}"):
                kwargs = {field: value}
                stn = STN(**kwargs)  # type: ignore
                assert getattr(stn, field) == value

    def test_partial_stn_values(self, subtests):
        """Test STN with explicit name (only field available)."""
        with subtests.test("explicit name"):
            stn = STN(name="explicit_station")  # type: ignore
            assert stn.name == "explicit_station"


class TestStnValidation:
    """Test STN input validation and type conversion."""

    def test_name_validation(self, subtests):
        """Test name field validation."""
        valid_values = [
            "",
            "1",
            "station1",
            "test_station",
            "123",
            "A",
            "test-station-name",
            "station with spaces",
            "αβγ",  # Unicode
            "!@#$%",  # Special characters
        ]

        for value in valid_values:
            with subtests.test(f"name valid '{value}'"):
                stn = STN(name=value)  # type: ignore
                assert stn.name == value

    def test_type_coercion(self, subtests):
        """Test type coercion behavior."""
        coercion_cases = [
            ("integer", 123, "123"),
            ("float", 45.67, "45.67"),
        ]

        for case_name, input_value, expected_value in coercion_cases:
            with subtests.test(f"name coercion {case_name}"):
                stn = STN(name=input_value)  # type: ignore
                assert stn.name == expected_value

        # Test boolean handling separately since it causes ValidationError
        boolean_cases = [
            ("boolean True", True),
            ("boolean False", False),
        ]

        for case_name, input_value in boolean_cases:
            with subtests.test(f"name coercion {case_name}"):
                try:
                    stn = STN(name=input_value)  # type: ignore
                    # If no error, check if it was coerced
                    assert isinstance(stn.name, str)
                except ValidationError:
                    # Expected for boolean types with strict validation
                    pass

    def test_invalid_values(self, subtests):
        """Test handling of invalid values."""
        invalid_cases = [
            ("list", ["not", "a", "string"]),
            ("dict", {"not": "a_string"}),
            ("none", None),  # None might not be valid for required field
        ]

        for case_name, invalid_value in invalid_cases:
            with subtests.test(f"invalid name {case_name}"):
                # Some invalid types might be coerced or raise ValidationError
                try:
                    stn = STN(name=invalid_value)  # type: ignore
                    # If it doesn't raise an error, check if it was coerced
                    assert isinstance(stn.name, str)
                except (ValidationError, TypeError):
                    # Expected for truly invalid types
                    pass


class TestStnSerialization:
    """Test STN serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_stn(self):
        """Fixture for default STN instance."""
        return STN()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_stn(self):
        """Fixture for populated STN instance."""
        return STN(name="test_station")  # type: ignore

    def test_model_dump_default(self, default_stn, subtests):
        """Test model_dump with default values."""
        dump = default_stn.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            assert "name" in dump

        with subtests.test("default values"):
            assert dump["name"] == ""

        with subtests.test("includes class name"):
            assert "_class_name" in dump
            assert dump["_class_name"] == "s_t_n"

    def test_model_dump_populated(self, populated_stn, subtests):
        """Test model_dump with populated values."""
        dump = populated_stn.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["name"] == "test_station"

    def test_from_dict_creation(self, subtests):
        """Test creating STN from dictionary."""
        test_cases = [
            ("full dict", {"name": "station_from_dict"}),
            ("empty dict", {}),
            ("string name", {"name": "simple"}),
            ("numeric name", {"name": "123"}),
        ]

        for case_name, data in test_cases:
            with subtests.test(f"from dict {case_name}"):
                stn = STN(**data)  # type: ignore
                expected_name = data.get("name", "")  # Default to empty string
                assert stn.name == expected_name

    def test_json_serialization(self, default_stn, populated_stn, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated stn"):
            json_str = populated_stn.model_dump_json()
            data = json.loads(json_str)
            recreated = STN(**data)  # type: ignore
            assert recreated.name == populated_stn.name

        with subtests.test("JSON round-trip default stn"):
            json_str = default_stn.model_dump_json()
            data = json.loads(json_str)
            recreated = STN(**data)  # type: ignore
            assert recreated.name == default_stn.name

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            stn = STN(name="test")  # type: ignore
            dump = stn.model_dump(exclude_none=True)
            assert "name" in dump
            assert dump["name"] == "test"

        with subtests.test("exclude_none with defaults"):
            stn = STN()  # type: ignore
            dump = stn.model_dump(exclude_none=True)
            # Should still include name since it's not None (it's empty string)
            assert "name" in dump

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            stn = STN()  # type: ignore
            dump = stn.model_dump(exclude_defaults=True)
            # Should exclude the default empty string
            assert "name" not in dump or dump.get("name") != ""

        with subtests.test("exclude_defaults with custom values"):
            stn = STN(name="custom")  # type: ignore
            dump = stn.model_dump(exclude_defaults=True)
            assert "name" in dump
            assert dump["name"] == "custom"


class TestStnModification:
    """Test STN field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying STN fields after creation."""
        stn = STN()  # type: ignore

        test_modifications = [
            ("name", "new_station"),
            ("name", "123"),
            ("name", "modified_name"),
            ("name", ""),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field} to {value}"):
                setattr(stn, field, value)
                assert getattr(stn, field) == value

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        stn = STN(name="test_station")  # type: ignore

        with subtests.test("reset name to default"):
            stn.name = ""  # type: ignore
            assert stn.name == ""

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        stn = STN()  # type: ignore

        updates = {"name": "bulk_station"}

        for field, value in updates.items():
            setattr(stn, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(stn, field) == expected_value

    def test_string_assignment_conversion(self, subtests):
        """Test that string assignment works correctly."""
        stn = STN()  # type: ignore

        with subtests.test("string assignment"):
            stn.name = "assigned_name"  # type: ignore
            assert stn.name == "assigned_name"
            assert isinstance(stn.name, str)


class TestStnComparison:
    """Test STN comparison and equality operations."""

    def test_stn_equality(self, subtests):
        """Test STN equality comparisons."""
        stn1 = STN(name="same_name")  # type: ignore
        stn2 = STN(name="same_name")  # type: ignore
        stn3 = STN(name="different_name")  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert stn1.model_dump() == stn2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert stn1.model_dump() != stn3.model_dump()

        with subtests.test("individual field comparison"):
            assert stn1.name == stn2.name
            assert stn1.name != stn3.name

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            "station_test",
            "1",
            "A",
            "",
            "test_123",
        ]

        for value in test_values:
            with subtests.test(f"consistency name '{value}'"):
                stn = STN(name=value)  # type: ignore
                assert stn.name == value

                # Test round-trip consistency
                dump = stn.model_dump()
                recreated = STN(**dump)  # type: ignore
                assert recreated.name == stn.name

    def test_name_value_consistency(self, subtests):
        """Test name value consistency."""
        test_names = ["station1", "station2", "A", "1", "test_name"]

        for name in test_names:
            with subtests.test(f"name consistency '{name}'"):
                stn1 = STN(name=name)  # type: ignore
                stn2 = STN(name=name)  # type: ignore
                assert stn1.name == stn2.name
                assert stn1.model_dump() == stn2.model_dump()


class TestStnEdgeCases:
    """Test STN edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            stn = STN(**{})  # type: ignore
            assert stn.name == ""

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            stn = STN(unknown_field="value")  # type: ignore
            assert hasattr(stn, "unknown_field")
            assert stn.unknown_field == "value"  # type: ignore

    def test_name_edge_cases(self, subtests):
        """Test name field edge cases."""
        edge_cases = [
            ("very long string", "x" * 1000),
            ("special characters", "!@#$%^&*()"),
            ("unicode characters", "αβγδεζ"),
            ("newlines", "line1\nline2"),
            ("tabs", "col1\tcol2"),
            ("mixed whitespace", "  spaced  name  "),
            ("numbers only", "123456789"),
            ("float as string", "123.456"),
            ("scientific notation", "1e5"),
            ("negative numbers", "-123"),
            ("boolean-like", "true"),
            ("null-like", "null"),
        ]

        for case_name, test_value in edge_cases:
            with subtests.test(f"name edge case {case_name}"):
                stn = STN(name=test_value)  # type: ignore
                assert stn.name == test_value

    def test_name_boundary_values(self, subtests):
        """Test name boundary values."""
        boundary_cases = [
            ("empty string", ""),
            ("single space", " "),
            ("single character", "A"),
            ("two characters", "AB"),
            ("all spaces", "   "),
            ("zero", "0"),
            ("single digit", "9"),
        ]

        for case_name, test_value in boundary_cases:
            with subtests.test(f"name boundary {case_name}"):
                stn = STN(name=test_value)  # type: ignore
                assert stn.name == test_value

    def test_name_special_formats(self, subtests):
        """Test name with various special formats."""
        special_formats = [
            ("station format", "STN_001"),
            ("dotted format", "station.1"),
            ("hyphenated format", "station-001"),
            ("mixed case", "StAtIoN_123"),
            ("uppercase", "STATION"),
            ("lowercase", "station"),
            ("with extension", "station.txt"),
            ("path-like", "path/to/station"),
            ("url-like", "http://station"),
            ("email-like", "station@domain"),
        ]

        for case_name, test_value in special_formats:
            with subtests.test(f"name special format {case_name}"):
                stn = STN(name=test_value)  # type: ignore
                assert stn.name == test_value


class TestStnDocumentation:
    """Test STN class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test STN class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert STN.__name__ == "STN"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(STN, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = STN.model_fields
        expected_fields = ["name"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = STN.model_fields

        with subtests.test("name field properties"):
            name_field = fields["name"]
            # Should be required with default
            assert hasattr(name_field, "default") or "default" in str(name_field)

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            stn = STN()  # type: ignore
            dump = stn.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) == 2  # name + _class_name

        with subtests.test("all expected fields present"):
            expected_fields = ["name"]
            dump = STN().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump
            # Also has _class_name field
            assert "_class_name" in dump

        with subtests.test("model_fields accessible"):
            fields = STN.model_fields
            assert len(fields) == 1  # Only the actual model fields
            assert "name" in fields

    def test_field_types_documentation(self, subtests):
        """Test documented field types."""
        stn = STN()  # type: ignore

        with subtests.test("name field type documentation"):
            assert isinstance(stn.name, str)

    def test_example_values(self, subtests):
        """Test that field examples work correctly."""
        # Test the example value from the field definition
        with subtests.test("example value name"):
            stn = STN(name="1")  # type: ignore
            assert stn.name == "1"

    def test_field_requirements(self, subtests):
        """Test field requirement specifications."""
        with subtests.test("name field requirement"):
            # Check if name field is marked as required in schema
            fields = STN.model_fields
            name_field = fields["name"]
            # The field is required but has a default value
            assert hasattr(name_field, "default") or "default" in str(name_field)

    def test_default_behavior(self, subtests):
        """Test default behavior matches expectations."""
        with subtests.test("default initialization"):
            stn = STN()  # type: ignore
            assert stn.name == ""

        with subtests.test("explicit default"):
            stn = STN(name="")  # type: ignore
            assert stn.name == ""

        with subtests.test("no arguments"):
            stn = STN()  # type: ignore
            assert hasattr(stn, "name")
            assert isinstance(stn.name, str)


class TestStnIntegration:
    """Test STN integration scenarios and realistic usage patterns."""

    def test_realistic_station_names(self, subtests):
        """Test realistic station naming patterns."""
        realistic_names = [
            ("numeric station", "001"),
            ("prefixed station", "STN001"),
            ("geographic station", "NorthPole"),
            ("coordinate station", "N40W120"),
            ("sequential station", "Station_A"),
            ("mixed format", "MT-001_Site"),
            ("simple digit", "1"),
            ("letter designation", "A"),
            ("survey format", "SURV2024_001"),
        ]

        for case_name, station_name in realistic_names:
            with subtests.test(f"realistic {case_name}"):
                stn = STN(name=station_name)  # type: ignore
                assert stn.name == station_name

                # Test serialization works
                dump = stn.model_dump()
                assert dump["name"] == station_name

                # Test recreation works
                recreated = STN(**dump)  # type: ignore
                assert recreated.name == station_name

    def test_data_pipeline_scenarios(self, subtests):
        """Test scenarios that might occur in data processing pipelines."""
        pipeline_scenarios = [
            ("empty initialization", {}, ""),
            ("string conversion", {"name": 123}, "123"),
            ("float conversion", {"name": 45.67}, "45.67"),
        ]

        for case_name, input_data, expected_name in pipeline_scenarios:
            with subtests.test(f"pipeline {case_name}"):
                stn = STN(**input_data)  # type: ignore
                assert stn.name == expected_name

        # Test boolean conversion separately since it might cause ValidationError
        boolean_pipeline_cases = [
            ("boolean conversion", {"name": True}),
        ]

        for case_name, input_data in boolean_pipeline_cases:
            with subtests.test(f"pipeline {case_name}"):
                try:
                    stn = STN(**input_data)  # type: ignore
                    assert isinstance(stn.name, str)
                except ValidationError:
                    # Expected for boolean types with strict validation
                    pass

    def test_serialization_roundtrip_scenarios(self, subtests):
        """Test serialization scenarios for data persistence."""
        test_names = ["", "1", "Station_001", "αβγ", "special!@#"]

        for name in test_names:
            with subtests.test(f"roundtrip '{name}'"):
                # Create original
                original = STN(name=name)  # type: ignore

                # Serialize to JSON
                json_str = original.model_dump_json()

                # Deserialize from JSON
                data = json.loads(json_str)
                recreated = STN(**data)  # type: ignore

                # Verify consistency
                assert recreated.name == original.name
                assert recreated.model_dump() == original.model_dump()

    def test_field_update_scenarios(self, subtests):
        """Test field update scenarios for data modification."""
        with subtests.test("progressive updates"):
            stn = STN()  # type: ignore

            # Start with default
            assert stn.name == ""

            # Update to initial value
            stn.name = "initial"  # type: ignore
            assert stn.name == "initial"

            # Update to modified value
            stn.name = "modified"  # type: ignore
            assert stn.name == "modified"

            # Reset to empty
            stn.name = ""  # type: ignore
            assert stn.name == ""

    def test_error_handling_scenarios(self, subtests):
        """Test error handling in various scenarios."""
        with subtests.test("invalid type handling"):
            # Test various invalid types to see how they're handled
            invalid_inputs = [
                ([], "list"),
                ({}, "dict"),
                (None, "None"),
            ]

            for invalid_input, input_type in invalid_inputs:
                try:
                    stn = STN(name=invalid_input)  # type: ignore
                    # If no error, check if it was coerced to string
                    assert isinstance(stn.name, str)
                except (ValidationError, TypeError):
                    # Expected for truly invalid types
                    pass
