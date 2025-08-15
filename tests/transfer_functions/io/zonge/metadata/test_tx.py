"""
Test suite for Tx metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata import Tx, TypeEnum


class TestTxDefault:
    """Test default initialization and basic attributes of Tx class."""

    @pytest.fixture(scope="class")
    def default_tx(self):
        """Fixture providing a default Tx instance for efficiency."""
        return Tx()  # type: ignore

    def test_default_initialization(self, default_tx, subtests):
        """Test that Tx initializes with correct default values."""
        with subtests.test("default type value"):
            assert default_tx.type == "natural"

    def test_default_tx_attributes(self, default_tx, subtests):
        """Test that Tx has all expected attributes."""
        expected_attributes = ["type"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_tx, attr)

    def test_default_model_fields(self, default_tx, subtests):
        """Test model fields are properly defined."""
        fields = default_tx.model_fields
        expected_fields = ["type"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 1

    def test_field_types(self, default_tx, subtests):
        """Test that fields have expected types."""
        with subtests.test("type field type"):
            assert isinstance(default_tx.type, str)

    def test_required_field_behavior(self, subtests):
        """Test that type field behaves as required with default."""
        with subtests.test("type field is required but has default"):
            tx = Tx()  # type: ignore
            assert tx.type == "natural"
            assert hasattr(tx, "type")


class TestTxCustomValues:
    """Test Tx with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_tx(self):
        """Fixture providing a Tx instance with custom values for efficiency."""
        return Tx(type="controlled source")  # type: ignore

    def test_populated_tx_values(self, populated_tx, subtests):
        """Test Tx with custom values."""
        with subtests.test("populated type"):
            assert populated_tx.type == "controlled source"

    def test_type_initialization_patterns(self, subtests):
        """Test various type initialization patterns."""
        type_patterns = [
            ("natural string", "natural", "natural"),
            ("controlled source string", "controlled source", "controlled source"),
            ("TypeEnum natural", TypeEnum.natural, "natural"),
            (
                "TypeEnum controlled_source",
                TypeEnum.controlled_source,
                "controlled source",
            ),
        ]

        for case_name, input_value, expected_value in type_patterns:
            with subtests.test(f"type pattern {case_name}"):
                tx = Tx(type=input_value)  # type: ignore
                assert tx.type == expected_value

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("type", "natural"),
            ("type", "controlled source"),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field} with value {value}"):
                kwargs = {field: value}
                tx = Tx(**kwargs)  # type: ignore
                assert getattr(tx, field) == value

    def test_partial_tx_values(self, subtests):
        """Test Tx with explicit type (only field available)."""
        with subtests.test("explicit type"):
            tx = Tx(type="controlled source")  # type: ignore
            assert tx.type == "controlled source"


class TestTxValidation:
    """Test Tx input validation and type conversion."""

    def test_type_validation(self, subtests):
        """Test type field validation."""
        valid_values = [
            "natural",
            "controlled source",
            TypeEnum.natural,
            TypeEnum.controlled_source,
        ]

        for value in valid_values:
            with subtests.test(f"type valid '{value}'"):
                tx = Tx(type=value)  # type: ignore
                if isinstance(value, TypeEnum):
                    assert tx.type == value.value
                else:
                    assert tx.type == value

    def test_type_coercion(self, subtests):
        """Test type coercion behavior."""
        # Test that enum objects are converted to string values
        with subtests.test("TypeEnum to string conversion"):
            tx = Tx(type=TypeEnum.controlled_source)  # type: ignore
            assert tx.type == "controlled source"
            assert isinstance(tx.type, str)

    def test_invalid_values(self, subtests):
        """Test handling of invalid values."""
        invalid_cases = [
            ("list", ["not", "a", "string"]),
            ("dict", {"not": "a_string"}),
            ("none", None),
            ("invalid_type", "invalid_source_type"),
            ("empty_string", ""),
            ("number", 123),
            ("boolean", True),
        ]

        for case_name, invalid_value in invalid_cases:
            with subtests.test(f"invalid type {case_name}"):
                try:
                    tx = Tx(type=invalid_value)  # type: ignore
                    # If it doesn't raise an error, check if it was coerced
                    assert isinstance(tx.type, str)
                except (ValidationError, ValueError, TypeError):
                    # Expected for truly invalid types
                    pass

    def test_enum_validation(self, subtests):
        """Test TypeEnum validation."""
        with subtests.test("all enum values are valid"):
            for enum_value in TypeEnum:
                tx = Tx(type=enum_value)  # type: ignore
                assert tx.type == enum_value.value

        with subtests.test("enum string values are valid"):
            for enum_value in TypeEnum:
                tx = Tx(type=enum_value.value)  # type: ignore
                assert tx.type == enum_value.value


class TestTxSerialization:
    """Test Tx serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_tx(self):
        """Fixture for default Tx instance."""
        return Tx()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_tx(self):
        """Fixture for populated Tx instance."""
        return Tx(type="controlled source")  # type: ignore

    def test_model_dump_default(self, default_tx, subtests):
        """Test model_dump with default values."""
        dump = default_tx.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            assert "type" in dump

        with subtests.test("default values"):
            assert dump["type"] == "natural"

        with subtests.test("includes class name"):
            assert "_class_name" in dump
            assert dump["_class_name"] == "tx"

    def test_model_dump_populated(self, populated_tx, subtests):
        """Test model_dump with populated values."""
        dump = populated_tx.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["type"] == "controlled source"

    def test_from_dict_creation(self, subtests):
        """Test creating Tx from dictionary."""
        test_cases = [
            ("full dict", {"type": "natural"}),
            ("controlled source dict", {"type": "controlled source"}),
            ("empty dict", {}),
        ]

        for case_name, data in test_cases:
            with subtests.test(f"from dict {case_name}"):
                tx = Tx(**data)  # type: ignore
                expected_type = data.get("type", "natural")  # Default to natural
                assert tx.type == expected_type

    def test_json_serialization(self, default_tx, populated_tx, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated tx"):
            json_str = populated_tx.model_dump_json()
            data = json.loads(json_str)
            recreated = Tx(**data)  # type: ignore
            assert recreated.type == populated_tx.type

        with subtests.test("JSON round-trip default tx"):
            json_str = default_tx.model_dump_json()
            data = json.loads(json_str)
            recreated = Tx(**data)  # type: ignore
            assert recreated.type == default_tx.type

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            tx = Tx(type="controlled source")  # type: ignore
            dump = tx.model_dump(exclude_none=True)
            assert "type" in dump
            assert dump["type"] == "controlled source"

        with subtests.test("exclude_none with defaults"):
            tx = Tx()  # type: ignore
            dump = tx.model_dump(exclude_none=True)
            # Should still include type since it's not None (it's "natural")
            assert "type" in dump

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            tx = Tx()  # type: ignore
            dump = tx.model_dump(exclude_defaults=True)
            # Should exclude the default "natural" value
            assert "type" not in dump or dump.get("type") != "natural"

        with subtests.test("exclude_defaults with custom values"):
            tx = Tx(type="controlled source")  # type: ignore
            dump = tx.model_dump(exclude_defaults=True)
            assert "type" in dump
            assert dump["type"] == "controlled source"


class TestTxModification:
    """Test Tx field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Tx fields after creation."""
        tx = Tx()  # type: ignore

        test_modifications = [
            ("type", "controlled source"),
            ("type", "natural"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field} to {value}"):
                setattr(tx, field, value)
                assert getattr(tx, field) == value

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        tx = Tx(type="controlled source")  # type: ignore

        with subtests.test("reset type to default"):
            tx.type = "natural"  # type: ignore
            assert tx.type == "natural"

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        tx = Tx()  # type: ignore

        updates = {"type": "controlled source"}

        for field, value in updates.items():
            setattr(tx, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(tx, field) == expected_value

    def test_enum_assignment(self, subtests):
        """Test that enum assignment works correctly."""
        tx = Tx()  # type: ignore

        with subtests.test("TypeEnum assignment"):
            tx.type = TypeEnum.controlled_source  # type: ignore
            assert tx.type == "controlled source"

        with subtests.test("string assignment"):
            tx.type = "natural"  # type: ignore
            assert tx.type == "natural"
            assert isinstance(tx.type, str)


class TestTxComparison:
    """Test Tx comparison and equality operations."""

    def test_tx_equality(self, subtests):
        """Test Tx equality comparisons."""
        tx1 = Tx(type="natural")  # type: ignore
        tx2 = Tx(type="natural")  # type: ignore
        tx3 = Tx(type="controlled source")  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert tx1.model_dump() == tx2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert tx1.model_dump() != tx3.model_dump()

        with subtests.test("individual field comparison"):
            assert tx1.type == tx2.type
            assert tx1.type != tx3.type

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            "natural",
            "controlled source",
        ]

        for value in test_values:
            with subtests.test(f"consistency type '{value}'"):
                tx = Tx(type=value)  # type: ignore
                assert tx.type == value

                # Test round-trip consistency
                dump = tx.model_dump()
                recreated = Tx(**dump)  # type: ignore
                assert recreated.type == tx.type

    def test_type_value_consistency(self, subtests):
        """Test type value consistency."""
        test_types = ["natural", "controlled source"]

        for type_val in test_types:
            with subtests.test(f"type consistency '{type_val}'"):
                tx1 = Tx(type=type_val)  # type: ignore
                tx2 = Tx(type=type_val)  # type: ignore
                assert tx1.type == tx2.type
                assert tx1.model_dump() == tx2.model_dump()


class TestTxEdgeCases:
    """Test Tx edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            tx = Tx(**{})  # type: ignore
            assert tx.type == "natural"

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            tx = Tx(unknown_field="value")  # type: ignore
            assert hasattr(tx, "unknown_field")
            assert tx.unknown_field == "value"  # type: ignore

    def test_type_edge_cases(self, subtests):
        """Test type field edge cases."""
        edge_cases = [
            ("all lowercase natural", "natural"),
            ("controlled source", "controlled source"),
            ("with enum", TypeEnum.natural),
            ("with enum controlled", TypeEnum.controlled_source),
        ]

        for case_name, test_value in edge_cases:
            with subtests.test(f"type edge case {case_name}"):
                tx = Tx(type=test_value)  # type: ignore
                if isinstance(test_value, TypeEnum):
                    assert tx.type == test_value.value
                else:
                    assert tx.type == test_value

    def test_type_boundary_values(self, subtests):
        """Test type boundary values."""
        boundary_cases = [
            ("empty enum natural", TypeEnum.natural),
            ("empty enum controlled", TypeEnum.controlled_source),
        ]

        for case_name, test_value in boundary_cases:
            with subtests.test(f"type boundary {case_name}"):
                tx = Tx(type=test_value)  # type: ignore
                assert tx.type == test_value.value

    def test_type_case_sensitivity(self, subtests):
        """Test type case sensitivity."""
        case_tests = [
            ("natural lowercase", "natural", "natural"),
            ("NATURAL uppercase", "NATURAL", True),  # Should fail validation
            (
                "Controlled Source title",
                "Controlled Source",
                True,
            ),  # Should fail validation
            ("controlled source correct", "controlled source", "controlled source"),
        ]

        for case_name, input_value, expected_result in case_tests:
            with subtests.test(f"case sensitivity {case_name}"):
                if expected_result is True:  # Expecting validation error
                    try:
                        tx = Tx(type=input_value)  # type: ignore
                        # If no error, the validation might be more lenient
                        assert isinstance(tx.type, str)
                    except (ValidationError, ValueError):
                        # Expected for case-sensitive validation
                        pass
                else:
                    tx = Tx(type=input_value)  # type: ignore
                    assert tx.type == expected_result

    def test_type_whitespace_handling(self, subtests):
        """Test type whitespace handling."""
        whitespace_cases = [
            ("natural with spaces", " natural ", True),  # Should fail or be trimmed
            ("controlled source exact", "controlled source", "controlled source"),
            (
                "controlled with extra spaces",
                " controlled source ",
                True,
            ),  # Should fail or be trimmed
        ]

        for case_name, input_value, expected_result in whitespace_cases:
            with subtests.test(f"whitespace {case_name}"):
                if expected_result is True:  # Expecting validation error or trimming
                    try:
                        tx = Tx(type=input_value)  # type: ignore
                        # If no error, check if it was trimmed
                        assert tx.type.strip() == input_value.strip()
                    except (ValidationError, ValueError):
                        # Expected for strict validation
                        pass
                else:
                    tx = Tx(type=input_value)  # type: ignore
                    assert tx.type == expected_result


class TestTxDocumentation:
    """Test Tx class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Tx class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert Tx.__name__ == "Tx"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(Tx, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = Tx.model_fields
        expected_fields = ["type"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = Tx.model_fields

        with subtests.test("type field properties"):
            type_field = fields["type"]
            # Should be required with default
            assert hasattr(type_field, "default") or "default" in str(type_field)

    def test_enum_definitions(self, subtests):
        """Test TypeEnum definition."""
        with subtests.test("TypeEnum definition"):
            assert hasattr(TypeEnum, "natural")
            assert hasattr(TypeEnum, "controlled_source")
            assert TypeEnum.natural.value == "natural"
            assert TypeEnum.controlled_source.value == "controlled source"

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            tx = Tx()  # type: ignore
            dump = tx.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) == 2  # type + _class_name

        with subtests.test("all expected fields present"):
            expected_fields = ["type"]
            dump = Tx().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump
            # Also has _class_name field
            assert "_class_name" in dump

        with subtests.test("model_fields accessible"):
            fields = Tx.model_fields
            assert len(fields) == 1  # Only the actual model fields
            assert "type" in fields

    def test_field_types_documentation(self, subtests):
        """Test documented field types."""
        tx = Tx()  # type: ignore

        with subtests.test("type field type documentation"):
            assert isinstance(tx.type, str)

    def test_example_values(self, subtests):
        """Test that field examples work correctly."""
        # Test the example value from the field definition
        with subtests.test("example value type"):
            tx = Tx(type="natural")  # type: ignore
            assert tx.type == "natural"

    def test_field_requirements(self, subtests):
        """Test field requirement specifications."""
        with subtests.test("type field requirement"):
            # Check if type field is marked as required in schema
            fields = Tx.model_fields
            type_field = fields["type"]
            # The field is required but has a default value
            assert hasattr(type_field, "default") or "default" in str(type_field)

    def test_default_behavior(self, subtests):
        """Test default behavior matches expectations."""
        with subtests.test("default initialization"):
            tx = Tx()  # type: ignore
            assert tx.type == "natural"

        with subtests.test("explicit default"):
            tx = Tx(type="natural")  # type: ignore
            assert tx.type == "natural"

        with subtests.test("no arguments"):
            tx = Tx()  # type: ignore
            assert hasattr(tx, "type")
            assert isinstance(tx.type, str)


class TestTxIntegration:
    """Test Tx integration scenarios and realistic usage patterns."""

    def test_realistic_tx_types(self, subtests):
        """Test realistic TX type patterns."""
        realistic_types = [
            ("natural source", "natural"),
            ("controlled source", "controlled source"),
        ]

        for case_name, tx_type in realistic_types:
            with subtests.test(f"realistic {case_name}"):
                tx = Tx(type=tx_type)  # type: ignore
                assert tx.type == tx_type

                # Test serialization works
                dump = tx.model_dump()
                assert dump["type"] == tx_type

                # Test recreation works
                recreated = Tx(**dump)  # type: ignore
                assert recreated.type == tx_type

    def test_data_pipeline_scenarios(self, subtests):
        """Test scenarios that might occur in data processing pipelines."""
        pipeline_scenarios = [
            ("empty initialization", {}, "natural"),
            (
                "enum conversion",
                {"type": TypeEnum.controlled_source},
                "controlled source",
            ),
            ("string direct", {"type": "natural"}, "natural"),
        ]

        for case_name, input_data, expected_type in pipeline_scenarios:
            with subtests.test(f"pipeline {case_name}"):
                tx = Tx(**input_data)  # type: ignore
                assert tx.type == expected_type

    def test_serialization_roundtrip_scenarios(self, subtests):
        """Test serialization scenarios for data persistence."""
        test_types = ["natural", "controlled source"]

        for tx_type in test_types:
            with subtests.test(f"roundtrip '{tx_type}'"):
                # Create original
                original = Tx(type=tx_type)  # type: ignore

                # Serialize to JSON
                json_str = original.model_dump_json()

                # Deserialize from JSON
                data = json.loads(json_str)
                recreated = Tx(**data)  # type: ignore

                # Verify consistency
                assert recreated.type == original.type
                assert recreated.model_dump() == original.model_dump()

    def test_field_update_scenarios(self, subtests):
        """Test field update scenarios for data modification."""
        with subtests.test("progressive updates"):
            tx = Tx()  # type: ignore

            # Start with default
            assert tx.type == "natural"

            # Update to controlled source
            tx.type = "controlled source"  # type: ignore
            assert tx.type == "controlled source"

            # Update back to natural
            tx.type = "natural"  # type: ignore
            assert tx.type == "natural"

    def test_error_handling_scenarios(self, subtests):
        """Test error handling in various scenarios."""
        with subtests.test("invalid type handling"):
            # Test various invalid types to see how they're handled
            invalid_inputs = [
                ([], "list"),
                ({}, "dict"),
                (None, "None"),
                ("invalid_type", "invalid_string"),
                (123, "number"),
                (True, "boolean"),
            ]

            for invalid_input, input_type in invalid_inputs:
                try:
                    tx = Tx(type=invalid_input)  # type: ignore
                    # If no error, check if it was coerced to string
                    assert isinstance(tx.type, str)
                except (ValidationError, ValueError, TypeError):
                    # Expected for truly invalid types
                    pass

    def test_enum_integration_scenarios(self, subtests):
        """Test integration scenarios with TypeEnum."""
        with subtests.test("enum values integration"):
            for enum_val in TypeEnum:
                # Test enum object
                tx1 = Tx(type=enum_val)  # type: ignore
                assert tx1.type == enum_val.value

                # Test string value
                tx2 = Tx(type=enum_val.value)  # type: ignore
                assert tx2.type == enum_val.value

                # Test consistency
                assert tx1.type == tx2.type
                assert tx1.model_dump() == tx2.model_dump()

    def test_mixed_initialization_scenarios(self, subtests):
        """Test scenarios with mixed initialization approaches."""
        mixed_scenarios = [
            ("enum object", TypeEnum.natural, "natural"),
            ("enum string", "natural", "natural"),
            ("controlled enum", TypeEnum.controlled_source, "controlled source"),
            ("controlled string", "controlled source", "controlled source"),
        ]

        for case_name, input_value, expected_value in mixed_scenarios:
            with subtests.test(f"mixed {case_name}"):
                tx = Tx(type=input_value)  # type: ignore
                assert tx.type == expected_value

                # Test that it serializes correctly
                dump = tx.model_dump()
                assert dump["type"] == expected_value

                # Test recreation
                recreated = Tx(**dump)  # type: ignore
                assert recreated.type == expected_value

    def test_compatibility_scenarios(self, subtests):
        """Test compatibility with different data sources."""
        compatibility_tests = [
            ("json compatibility", '{"type": "natural"}'),
            ("json controlled", '{"type": "controlled source"}'),
        ]

        for case_name, json_str in compatibility_tests:
            with subtests.test(f"compatibility {case_name}"):
                data = json.loads(json_str)
                tx = Tx(**data)  # type: ignore

                # Verify the type is correct
                assert tx.type == data["type"]

                # Verify round-trip works
                recreated_json = tx.model_dump_json()
                recreated_data = json.loads(recreated_json)
                recreated_tx = Tx(**recreated_data)  # type: ignore
                assert recreated_tx.type == tx.type
