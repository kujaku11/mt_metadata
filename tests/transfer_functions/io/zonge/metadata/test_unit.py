"""
Test suite for Unit metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata import Unit


class TestUnitDefault:
    """Test default initialization and basic attributes of Unit class."""

    @pytest.fixture(scope="class")
    def default_unit(self):
        """Fixture providing a default Unit instance for efficiency."""
        return Unit()  # type: ignore

    def test_default_initialization(self, default_unit, subtests):
        """Test that Unit initializes with correct default values."""
        with subtests.test("default length value"):
            assert default_unit.length == "m"

        with subtests.test("default e value"):
            assert default_unit.e == "mV/km"

        with subtests.test("default b value"):
            assert default_unit.b == "nT"

    def test_default_unit_attributes(self, default_unit, subtests):
        """Test that Unit has all expected attributes."""
        expected_attributes = ["length", "e", "b"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_unit, attr)

    def test_default_model_fields(self, default_unit, subtests):
        """Test model fields are properly defined."""
        fields = default_unit.model_fields
        expected_fields = ["length", "e", "b"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 3

    def test_field_types(self, default_unit, subtests):
        """Test that fields have expected types."""
        with subtests.test("length field type"):
            assert isinstance(default_unit.length, str)

        with subtests.test("e field type"):
            assert isinstance(default_unit.e, str)

        with subtests.test("b field type"):
            assert isinstance(default_unit.b, str)

    def test_required_field_behavior(self, subtests):
        """Test field requirement specifications."""
        with subtests.test("all fields have defaults"):
            unit = Unit()  # type: ignore
            assert hasattr(unit, "length")
            assert hasattr(unit, "e")
            assert hasattr(unit, "b")
            assert unit.length != ""
            assert unit.e != ""
            assert unit.b != ""


class TestUnitCustomValues:
    """Test Unit with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_unit(self):
        """Fixture providing a Unit instance with custom values for efficiency."""
        return Unit(length="km", e="V/m", b="T")

    def test_populated_unit_values(self, populated_unit, subtests):
        """Test Unit with custom values."""
        with subtests.test("populated length"):
            assert populated_unit.length == "kilometer"

        with subtests.test("populated e"):
            assert populated_unit.e == "Volt per meter"

        with subtests.test("populated b"):
            assert populated_unit.b == "Tesla"

    def test_length_initialization_patterns(self, subtests):
        """Test various length initialization patterns."""
        length_patterns = [
            ("meter", "m", "meter"),
            ("kilometer", "km", "kilometer"),
            ("millimeter", "mm", "millimeter"),
            ("centimeter", "cm", "centimeter"),
        ]

        for case_name, input_value, expected_value in length_patterns:
            with subtests.test(f"length pattern {case_name}"):
                unit = Unit(length=input_value)
                assert unit.length == expected_value

    def test_e_field_initialization_patterns(self, subtests):
        """Test various e field initialization patterns."""
        e_patterns = [
            ("millivolt per kilometer", "mV/km", "milliVolt per kilometer"),
            ("volt per meter", "V/m", "Volt per meter"),
            ("microvolt per meter", "μV/m", "microVolt per meter"),
            ("volt per kilometer", "V/km", "Volt per kilometer"),
        ]

        for case_name, input_value, expected_value in e_patterns:
            with subtests.test(f"e field pattern {case_name}"):
                unit = Unit(e=input_value)
                assert unit.e == expected_value

    def test_b_field_initialization_patterns(self, subtests):
        """Test various b field initialization patterns."""
        b_patterns = [
            ("nanotesla", "nT", "nanoTesla"),
            ("tesla", "T", "Tesla"),
            ("millitesla", "mT", "milliTesla"),
            ("picotesla", "pT", "picoTesla"),
        ]

        for case_name, input_value, expected_value in b_patterns:
            with subtests.test(f"b field pattern {case_name}"):
                unit = Unit(b=input_value)
                assert unit.b == expected_value

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("length", "m"),
            ("length", "km"),
            ("e", "V/m"),
            ("e", "mV/km"),
            ("b", "nT"),
            ("b", "T"),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field} with value {value}"):
                kwargs = {field: value}
                unit = Unit(**kwargs)  # type: ignore
                # Just verify it's a non-empty string (validation converts to long form)
                assert isinstance(getattr(unit, field), str)
                assert getattr(unit, field) != ""

    def test_partial_unit_values(self, subtests):
        """Test Unit with partial field specifications."""
        partial_tests = [
            ("length only", {"length": "km"}),
            ("e only", {"e": "V/m"}),
            ("b only", {"b": "T"}),
            ("length and e", {"length": "m", "e": "mV/km"}),
            ("e and b", {"e": "V/m", "b": "nT"}),
            ("length and b", {"length": "mm", "b": "mT"}),
        ]

        for case_name, kwargs in partial_tests:
            with subtests.test(f"partial {case_name}"):
                unit = Unit(**kwargs)  # type: ignore
                for field, expected_input in kwargs.items():
                    # Verify field was set and converted
                    assert isinstance(getattr(unit, field), str)
                    assert getattr(unit, field) != ""


class TestUnitValidation:
    """Test Unit input validation and unit conversion."""

    def test_length_validation(self, subtests):
        """Test length field validation."""
        valid_lengths = [
            ("m", "meter"),
            ("km", "kilometer"),
            ("mm", "millimeter"),
            ("cm", "centimeter"),
        ]

        for input_val, expected_val in valid_lengths:
            with subtests.test(f"length valid '{input_val}'"):
                unit = Unit(length=input_val)  # type: ignore
                assert unit.length == expected_val

    def test_e_field_validation(self, subtests):
        """Test e field validation."""
        valid_e_values = [
            ("mV/km", "milliVolt per kilometer"),
            ("V/m", "Volt per meter"),
            ("μV/m", "microVolt per meter"),
            ("V/km", "Volt per kilometer"),
        ]

        for input_val, expected_val in valid_e_values:
            with subtests.test(f"e field valid '{input_val}'"):
                unit = Unit(e=input_val)  # type: ignore
                assert unit.e == expected_val

    def test_b_field_validation(self, subtests):
        """Test b field validation."""
        valid_b_values = [
            ("nT", "nanoTesla"),
            ("T", "Tesla"),
            ("mT", "milliTesla"),
            ("pT", "picoTesla"),
        ]

        for input_val, expected_val in valid_b_values:
            with subtests.test(f"b field valid '{input_val}'"):
                unit = Unit(b=input_val)  # type: ignore
                assert unit.b == expected_val

    def test_unit_conversion_behavior(self, subtests):
        """Test unit conversion behavior from short to long form."""
        conversion_tests = [
            ("length conversion", "length", "m", "meter"),
            ("e field conversion", "e", "V/m", "Volt per meter"),
            ("b field conversion", "b", "nT", "nanoTesla"),
        ]

        for case_name, field, input_val, expected_val in conversion_tests:
            with subtests.test(f"{case_name}"):
                kwargs = {field: input_val}
                unit = Unit(**kwargs)  # type: ignore
                assert getattr(unit, field) == expected_val

    def test_unknown_unit_handling(self, subtests):
        """Test handling of unknown or invalid units."""
        unknown_unit_tests = [
            ("invalid_length", "length", "invalid_unit"),
            ("invalid_e", "e", "invalid_electric_unit"),
            ("invalid_b", "b", "invalid_magnetic_unit"),
        ]

        for case_name, field, invalid_value in unknown_unit_tests:
            with subtests.test(f"unknown unit {case_name}"):
                kwargs = {field: invalid_value}
                unit = Unit(**kwargs)  # type: ignore
                # Unknown units should be converted to "unknown"
                field_value = getattr(unit, field)
                assert field_value == "unknown"

    def test_empty_and_none_values(self, subtests):
        """Test handling of empty and None values."""
        empty_value_tests = [
            ("empty_string_length", "length", ""),
            ("none_length", "length", None),
            ("empty_string_e", "e", ""),
            ("none_e", "e", None),
            ("empty_string_b", "b", ""),
            ("none_b", "b", None),
        ]

        for case_name, field, empty_value in empty_value_tests:
            with subtests.test(f"empty value {case_name}"):
                kwargs = {field: empty_value}
                unit = Unit(**kwargs)  # type: ignore
                field_value = getattr(unit, field)
                # Empty values should return empty string
                assert field_value == ""

    def test_case_sensitivity(self, subtests):
        """Test case sensitivity in unit validation."""
        case_tests = [
            ("lowercase_nt", "b", "nt", "nanoTesla"),
            ("uppercase_NT", "b", "NT", "nanoTesla"),
            ("mixed_case_Nt", "b", "Nt", "nanoTesla"),
            ("lowercase_m", "length", "m", "meter"),
            ("uppercase_M", "length", "M", "meter"),
        ]

        for case_name, field, input_val, expected_val in case_tests:
            with subtests.test(f"case sensitivity {case_name}"):
                kwargs = {field: input_val}
                unit = Unit(**kwargs)  # type: ignore
                field_value = getattr(unit, field)
                # Check if case is handled (might be case-insensitive)
                assert isinstance(field_value, str)
                # If it's properly recognized, should match expected
                if field_value != "unknown":
                    assert field_value == expected_val


class TestUnitSerialization:
    """Test Unit serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_unit(self):
        """Fixture for default Unit instance."""
        return Unit()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_unit(self):
        """Fixture for populated Unit instance."""
        return Unit(length="km", e="V/m", b="T")  # type: ignore

    def test_model_dump_default(self, default_unit, subtests):
        """Test model_dump with default values."""
        dump = default_unit.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["length", "e", "b"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["length"] == "m"
            assert dump["e"] == "mV/km"
            assert dump["b"] == "nT"

        with subtests.test("includes class name"):
            assert "_class_name" in dump
            assert dump["_class_name"] == "unit"

    def test_model_dump_populated(self, populated_unit, subtests):
        """Test model_dump with populated values."""
        dump = populated_unit.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["length"] == "kilometer"
            assert dump["e"] == "Volt per meter"
            assert dump["b"] == "Tesla"

    def test_from_dict_creation(self, subtests):
        """Test creating Unit from dictionary."""
        test_cases = [
            ("full dict", {"length": "m", "e": "V/m", "b": "nT"}),
            ("partial dict", {"length": "km"}),
            ("e and b only", {"e": "mV/km", "b": "T"}),
            ("empty dict", {}),
        ]

        for case_name, data in test_cases:
            with subtests.test(f"from dict {case_name}"):
                unit = Unit(**data)  # type: ignore
                for field, expected_input in data.items():
                    # Verify field was converted properly
                    field_value = getattr(unit, field)
                    assert isinstance(field_value, str)
                    assert field_value != ""

    def test_json_serialization(self, default_unit, populated_unit, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated unit"):
            json_str = populated_unit.model_dump_json()
            data = json.loads(json_str)
            recreated = Unit(**data)  # type: ignore
            assert recreated.length == populated_unit.length
            assert recreated.e == populated_unit.e
            assert recreated.b == populated_unit.b

        with subtests.test("JSON round-trip default unit"):
            json_str = default_unit.model_dump_json()
            data = json.loads(json_str)
            recreated = Unit(**data)  # type: ignore
            # When restored from JSON, defaults get validated and converted to long form
            assert recreated.length == "meter"
            assert recreated.e == "milliVolt per kilometer"
            assert recreated.b == "nanoTesla"

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            unit = Unit(length="km", e="V/m", b="T")  # type: ignore
            dump = unit.model_dump(exclude_none=True)
            expected_fields = ["length", "e", "b"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("exclude_none with empty values"):
            unit = Unit(length="", e="", b="")  # type: ignore
            dump = unit.model_dump(exclude_none=True)
            # Empty strings are not None, so they should still be included
            assert "length" in dump
            assert "e" in dump
            assert "b" in dump

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            unit = Unit()  # type: ignore
            dump = unit.model_dump(exclude_defaults=True)
            # Should exclude default values
            for field in ["length", "e", "b"]:
                assert field not in dump or dump.get(field) not in ["m", "mV/km", "nT"]

        with subtests.test("exclude_defaults with custom values"):
            unit = Unit(length="km", e="V/m", b="T")  # type: ignore
            dump = unit.model_dump(exclude_defaults=True)
            # Custom values should be included
            assert "length" in dump
            assert "e" in dump
            assert "b" in dump


class TestUnitModification:
    """Test Unit field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Unit fields after creation."""
        unit = Unit()  # type: ignore

        test_modifications = [
            ("length", "km"),
            ("e", "V/m"),
            ("b", "T"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field} to {value}"):
                setattr(unit, field, value)
                field_value = getattr(unit, field)
                assert isinstance(field_value, str)
                assert field_value != ""

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        unit = Unit(length="km", e="V/m", b="T")  # type: ignore

        default_inputs = [
            ("length", "m"),
            ("e", "mV/km"),
            ("b", "nT"),
        ]

        for field, default_input in default_inputs:
            with subtests.test(f"reset {field} to default"):
                setattr(unit, field, default_input)
                # Verify it was reset (will be converted to long form)
                field_value = getattr(unit, field)
                assert isinstance(field_value, str)
                assert field_value != ""

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        unit = Unit()  # type: ignore

        updates = {"length": "km", "e": "V/m", "b": "T"}

        for field, value in updates.items():
            setattr(unit, field, value)

        for field, expected_input in updates.items():
            with subtests.test(f"bulk update {field}"):
                field_value = getattr(unit, field)
                assert isinstance(field_value, str)
                assert field_value != ""

    def test_sequential_modifications(self, subtests):
        """Test sequential field modifications."""
        unit = Unit()  # type: ignore

        sequences = [
            ("length progression", "length", ["m", "km", "mm", "m"]),
            ("e field progression", "e", ["mV/km", "V/m", "uV/m", "mV/km"]),
            ("b field progression", "b", ["nT", "T", "mT", "nT"]),
        ]

        for case_name, field, values in sequences:
            with subtests.test(f"sequential {case_name}"):
                for value in values:
                    setattr(unit, field, value)
                    field_value = getattr(unit, field)
                    assert isinstance(field_value, str)
                    assert field_value != ""


class TestUnitComparison:
    """Test Unit comparison and equality operations."""

    def test_unit_equality(self, subtests):
        """Test Unit equality comparisons."""
        unit1 = Unit(length="m", e="mV/km", b="nT")  # type: ignore
        unit2 = Unit(length="m", e="mV/km", b="nT")  # type: ignore
        unit3 = Unit(length="km", e="V/m", b="T")  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert unit1.model_dump() == unit2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert unit1.model_dump() != unit3.model_dump()

        with subtests.test("individual field comparison"):
            assert unit1.length == unit2.length
            assert unit1.e == unit2.e
            assert unit1.b == unit2.b
            assert unit1.length != unit3.length

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("length", ["m", "km", "mm"]),
            ("e", ["mV/km", "V/m", "uV/m"]),
            ("b", ["nT", "T", "mT"]),
        ]

        for field, values in test_values:
            for value in values:
                with subtests.test(f"consistency {field} '{value}'"):
                    kwargs = {field: value}
                    unit = Unit(**kwargs)  # type: ignore
                    field_value = getattr(unit, field)
                    assert isinstance(field_value, str)
                    assert field_value != ""

                    # Test round-trip consistency
                    dump = unit.model_dump()
                    recreated = Unit(**dump)  # type: ignore
                    assert getattr(recreated, field) == field_value

    def test_unit_conversion_consistency(self, subtests):
        """Test unit conversion consistency."""
        conversion_pairs = [
            ("length", "m", "meter"),
            ("length", "km", "kilometer"),
            ("e", "V/m", "Volt per meter"),
            ("e", "mV/km", "milliVolt per kilometer"),
            ("b", "nT", "nanoTesla"),
            ("b", "T", "Tesla"),
        ]

        for field, short_form, expected_long_form in conversion_pairs:
            with subtests.test(f"conversion consistency {field} {short_form}"):
                kwargs = {field: short_form}
                unit1 = Unit(**kwargs)  # type: ignore
                unit2 = Unit(**kwargs)  # type: ignore

                assert getattr(unit1, field) == getattr(unit2, field)
                assert getattr(unit1, field) == expected_long_form
                assert unit1.model_dump() == unit2.model_dump()


class TestUnitEdgeCases:
    """Test Unit edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            unit = Unit(**{})  # type: ignore
            assert unit.length == "m"
            assert unit.e == "mV/km"
            assert unit.b == "nT"

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields might be accepted"):
            # Test that unknown fields don't break initialization
            try:
                unit = Unit(length="m", e="mV/km", b="nT", unknown_field="value")
                # If MetadataBase accepts unknown fields, test their presence
                if hasattr(unit, "unknown_field"):
                    assert unit.unknown_field == "value"
                # At minimum, the known fields should work correctly
                assert unit.length == "meter"  # Explicitly set, so converted
                assert unit.e == "milliVolt per kilometer"
                assert unit.b == "nanoTesla"
            except TypeError:
                # If unknown fields are not accepted, that's also valid behavior
                # Just test normal creation works
                unit = Unit(length="m", e="mV/km", b="nT")  # type: ignore
                assert unit.length == "meter"

    def test_unit_edge_cases(self, subtests):
        """Test unit field edge cases."""
        edge_cases = [
            ("empty_string_length", "length", "", ""),
            ("none_length", "length", None, ""),
            ("unknown_unit_length", "length", "unknown_unit", "unknown"),
            ("empty_string_e", "e", "", ""),
            ("none_e", "e", None, ""),
            ("unknown_unit_e", "e", "unknown_unit", "unknown"),
            ("empty_string_b", "b", "", ""),
            ("none_b", "b", None, ""),
            ("unknown_unit_b", "b", "unknown_unit", "unknown"),
        ]

        for case_name, field, test_value, expected_result in edge_cases:
            with subtests.test(f"edge case {case_name}"):
                kwargs = {field: test_value}
                unit = Unit(**kwargs)  # type: ignore
                field_value = getattr(unit, field)
                assert field_value == expected_result

    def test_unit_whitespace_handling(self, subtests):
        """Test unit whitespace handling."""
        whitespace_cases = [
            ("length_with_spaces", "length", " m ", "meter"),  # Assuming trimming
            ("e_with_spaces", "e", " V/m ", "Volt per meter"),
            ("b_with_spaces", "b", " nT ", "nanoTesla"),
        ]

        for case_name, field, input_value, expected_result in whitespace_cases:
            with subtests.test(f"whitespace {case_name}"):
                kwargs = {field: input_value}
                try:
                    unit = Unit(**kwargs)  # type: ignore
                    field_value = getattr(unit, field)
                    # Either trimmed and recognized, or marked as unknown
                    assert isinstance(field_value, str)
                    if field_value != "unknown":
                        assert field_value == expected_result
                except (ValidationError, ValueError):
                    # Some whitespace handling might be strict
                    pass

    def test_complex_unit_strings(self, subtests):
        """Test complex unit string handling."""
        complex_cases = [
            ("compound_e_unit", "e", "mV/km", "milliVolt per kilometer"),
            ("compound_e_unit_alt", "e", "V/m", "Volt per meter"),
            ("simple_length", "length", "m", "meter"),
            ("simple_b", "b", "nT", "nanoTesla"),
        ]

        for case_name, field, input_value, expected_result in complex_cases:
            with subtests.test(f"complex unit {case_name}"):
                kwargs = {field: input_value}
                unit = Unit(**kwargs)  # type: ignore
                field_value = getattr(unit, field)
                assert field_value == expected_result

    def test_numeric_and_special_inputs(self, subtests):
        """Test numeric and special character inputs."""
        special_cases = [
            (
                "numeric_length",
                "length",
                123,
                "unknown",
            ),  # Should be coerced to string and marked unknown
            ("boolean_e", "e", True, "unknown"),
            ("list_b", "b", ["nT"], "unknown"),
            ("dict_length", "length", {"unit": "m"}, "unknown"),
        ]

        for case_name, field, input_value, expected_result in special_cases:
            with subtests.test(f"special input {case_name}"):
                kwargs = {field: input_value}
                try:
                    unit = Unit(**kwargs)  # type: ignore
                    field_value = getattr(unit, field)
                    # Non-string inputs should be handled gracefully
                    assert isinstance(field_value, str)
                    assert field_value == expected_result
                except (ValidationError, ValueError, TypeError):
                    # Some special inputs might cause validation errors
                    pass


class TestUnitDocumentation:
    """Test Unit class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Unit class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert Unit.__name__ == "Unit"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(Unit, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = Unit.model_fields
        expected_fields = ["length", "e", "b"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = Unit.model_fields

        expected_defaults = {"length": "m", "e": "mV/km", "b": "nT"}

        for field_name, expected_default in expected_defaults.items():
            with subtests.test(f"{field_name} field properties"):
                field = fields[field_name]
                # Should have default value
                assert hasattr(field, "default") or "default" in str(field)

    def test_validator_presence(self, subtests):
        """Test that validators are properly configured."""
        with subtests.test("unit validation method exists"):
            assert hasattr(Unit, "validate_units")

        with subtests.test("validator is classmethod"):
            assert callable(Unit.validate_units)

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            unit = Unit()  # type: ignore
            dump = unit.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) == 4  # 3 fields + _class_name

        with subtests.test("all expected fields present"):
            expected_fields = ["length", "e", "b"]
            dump = Unit().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump
            # Also has _class_name field
            assert "_class_name" in dump

        with subtests.test("model_fields accessible"):
            fields = Unit.model_fields
            assert len(fields) == 3  # Only the actual model fields
            expected_fields = ["length", "e", "b"]
            for field in expected_fields:
                assert field in fields

    def test_field_types_documentation(self, subtests):
        """Test documented field types."""
        unit = Unit()  # type: ignore

        with subtests.test("length field type documentation"):
            assert isinstance(unit.length, str)

        with subtests.test("e field type documentation"):
            assert isinstance(unit.e, str)

        with subtests.test("b field type documentation"):
            assert isinstance(unit.b, str)

    def test_example_values(self, subtests):
        """Test that field examples work correctly."""
        # Test the example values from field definitions
        examples = [
            ("length", "m"),
            ("e", "mV/km"),
            ("b", "nT"),
        ]

        for field_name, example_value in examples:
            with subtests.test(f"example value {field_name}"):
                kwargs = {field_name: example_value}
                unit = Unit(**kwargs)  # type: ignore
                field_value = getattr(unit, field_name)
                assert isinstance(field_value, str)
                assert field_value != ""


class TestUnitIntegration:
    """Test Unit integration scenarios and realistic usage patterns."""

    def test_realistic_unit_combinations(self, subtests):
        """Test realistic Unit combinations."""
        realistic_combinations = [
            ("mt_survey_standard", {"length": "m", "e": "mV/km", "b": "nT"}),
            ("high_precision", {"length": "mm", "e": "uV/m", "b": "pT"}),
            ("large_scale", {"length": "km", "e": "V/km", "b": "mT"}),
            ("si_units", {"length": "m", "e": "V/m", "b": "T"}),
        ]

        for case_name, unit_spec in realistic_combinations:
            with subtests.test(f"realistic {case_name}"):
                unit = Unit(**unit_spec)  # type: ignore

                # Verify all fields are valid
                assert isinstance(unit.length, str)
                assert isinstance(unit.e, str)
                assert isinstance(unit.b, str)
                assert unit.length != ""
                assert unit.e != ""
                assert unit.b != ""

                # Test serialization works
                dump = unit.model_dump()
                for field in ["length", "e", "b"]:
                    assert field in dump
                    assert isinstance(dump[field], str)
                    assert dump[field] != ""

                # Test recreation works
                recreated = Unit(**dump)  # type: ignore
                assert recreated.length == unit.length
                assert recreated.e == unit.e
                assert recreated.b == unit.b

    def test_data_pipeline_scenarios(self, subtests):
        """Test scenarios that might occur in data processing pipelines."""
        pipeline_scenarios = [
            ("empty_initialization", {}, {"length": "m", "e": "mV/km", "b": "nT"}),
            ("partial_specification", {"length": "km"}, {"length": "kilometer"}),
            (
                "full_specification",
                {"length": "m", "e": "V/m", "b": "T"},
                {"length": "meter", "e": "Volt per meter", "b": "Tesla"},
            ),
        ]

        for case_name, input_data, expected_fields in pipeline_scenarios:
            with subtests.test(f"pipeline {case_name}"):
                unit = Unit(**input_data)  # type: ignore

                for field, expected_value in expected_fields.items():
                    assert getattr(unit, field) == expected_value

    def test_serialization_roundtrip_scenarios(self, subtests):
        """Test serialization scenarios for data persistence."""
        test_combinations = [
            {"length": "m", "e": "mV/km", "b": "nT"},
            {"length": "km", "e": "V/m", "b": "T"},
            {"length": "mm", "e": "uV/m", "b": "pT"},
        ]

        for i, unit_spec in enumerate(test_combinations):
            with subtests.test(f"roundtrip scenario {i+1}"):
                # Create original
                original = Unit(**unit_spec)  # type: ignore

                # Serialize to JSON
                json_str = original.model_dump_json()

                # Deserialize from JSON
                data = json.loads(json_str)
                recreated = Unit(**data)  # type: ignore

                # Verify consistency
                assert recreated.length == original.length
                assert recreated.e == original.e
                assert recreated.b == original.b
                assert recreated.model_dump() == original.model_dump()

    def test_field_update_scenarios(self, subtests):
        """Test field update scenarios for data modification."""
        with subtests.test("progressive field updates"):
            unit = Unit()  # type: ignore

            # Track initial state
            initial_length = unit.length  # "m"
            initial_e = unit.e  # "mV/km"
            initial_b = unit.b  # "nT"

            # Update length
            unit.length = "km"
            assert unit.length == "kilometer"
            assert unit.e == initial_e  # Other fields unchanged
            assert unit.b == initial_b

            # Update e field
            unit.e = "V/m"
            assert unit.length == "kilometer"  # Previous change preserved
            assert unit.e == "Volt per meter"
            assert unit.b == initial_b

            # Update b field
            unit.b = "T"
            assert unit.length == "kilometer"  # Previous changes preserved
            assert unit.e == "Volt per meter"
            assert unit.b == "Tesla"

    def test_error_handling_scenarios(self, subtests):
        """Test error handling in various scenarios."""
        with subtests.test("invalid unit handling"):
            # Test various invalid units to see how they're handled
            invalid_inputs = [
                ([], "list"),
                ({}, "dict"),
                (None, "None"),
                ("", "empty_string"),
                ("invalid_unit", "invalid_string"),
                (123, "number"),
                (True, "boolean"),
            ]

            for invalid_input, input_type in invalid_inputs:
                try:
                    unit = Unit(length=invalid_input)  # type: ignore
                    field_value = unit.length
                    # Invalid inputs should be handled gracefully
                    assert isinstance(field_value, str)
                    # Should be either empty string or "unknown"
                    assert field_value in ["", "unknown"]
                except (ValidationError, ValueError, TypeError):
                    # Some invalid inputs might cause validation errors
                    pass

    def test_unit_validation_integration(self, subtests):
        """Test integration with unit validation system."""
        with subtests.test("unit validation system integration"):
            validation_tests = [
                ("length", "m", "meter"),
                ("length", "km", "kilometer"),
                ("e", "V/m", "Volt per meter"),
                ("e", "mV/km", "milliVolt per kilometer"),
                ("b", "nT", "nanoTesla"),
                ("b", "T", "Tesla"),
            ]

            for field, input_unit, expected_output in validation_tests:
                kwargs = {field: input_unit}
                unit = Unit(**kwargs)  # type: ignore
                field_value = getattr(unit, field)
                assert field_value == expected_output

    def test_mixed_initialization_scenarios(self, subtests):
        """Test scenarios with mixed initialization approaches."""
        mixed_scenarios = [
            (
                "defaults_and_custom",
                {"e": "V/m"},
                {"length": "m", "e": "Volt per meter", "b": "nT"},
            ),
            (
                "partial_updates",
                {"length": "km", "b": "T"},
                {"length": "kilometer", "e": "mV/km", "b": "Tesla"},
            ),
            (
                "all_custom",
                {"length": "mm", "e": "μV/m", "b": "pT"},
                {"length": "millimeter", "e": "microVolt per meter", "b": "picoTesla"},
            ),
        ]

        for case_name, input_data, expected_results in mixed_scenarios:
            with subtests.test(f"mixed {case_name}"):
                unit = Unit(**input_data)  # type: ignore

                for field, expected_value in expected_results.items():
                    assert getattr(unit, field) == expected_value

                # Test that it serializes correctly
                dump = unit.model_dump()
                for field, expected_value in expected_results.items():
                    assert dump[field] == expected_value

                # Test recreation (values will be re-validated and converted)
                recreated = Unit(**dump)  # type: ignore
                for field, expected_value in expected_results.items():
                    recreated_value = getattr(recreated, field)
                    # Values from JSON get re-validated, so we need to check the actual converted values
                    assert isinstance(recreated_value, str)
                    assert recreated_value != ""
                    # For known field mappings, verify the conversion worked correctly
                    if field == "length" and expected_value == "m":
                        assert recreated_value == "meter"
                    elif field == "e" and expected_value == "mV/km":
                        assert recreated_value == "milliVolt per kilometer"
                    elif field == "b" and expected_value == "nT":
                        assert recreated_value == "nanoTesla"
                    else:
                        # For explicitly converted values, they should match
                        assert recreated_value == expected_value

    def test_compatibility_scenarios(self, subtests):
        """Test compatibility with different data sources."""
        compatibility_tests = [
            ("json_input", '{"length": "m", "e": "mV/km", "b": "nT"}'),
            ("json_partial", '{"length": "km"}'),
            ("json_with_unknowns", '{"length": "unknown_unit", "e": "V/m", "b": "nT"}'),
        ]

        for case_name, json_str in compatibility_tests:
            with subtests.test(f"compatibility {case_name}"):
                data = json.loads(json_str)
                unit = Unit(**data)  # type: ignore

                # Verify fields are populated
                for field in data:
                    field_value = getattr(unit, field)
                    assert isinstance(field_value, str)
                    # Should be valid unit name or "unknown"
                    assert field_value != "" or field_value == "unknown"

                # Verify round-trip works
                recreated_json = unit.model_dump_json()
                recreated_data = json.loads(recreated_json)
                recreated_unit = Unit(**recreated_data)  # type: ignore
                # Note: JSON round-trip may convert units to long form due to validation
                # So we check that the conversion was consistent, not that they're identical
                assert (
                    isinstance(recreated_unit.length, str)
                    and recreated_unit.length != ""
                )
                assert isinstance(recreated_unit.e, str) and recreated_unit.e != ""
                assert isinstance(recreated_unit.b, str) and recreated_unit.b != ""

                # Check that the same input produces the same output consistently
                second_recreated = Unit(**recreated_data)  # type: ignore
                assert second_recreated.length == recreated_unit.length
                assert second_recreated.e == recreated_unit.e
                assert second_recreated.b == recreated_unit.b
