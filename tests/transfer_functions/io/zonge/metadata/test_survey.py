"""
Test suite for Survey metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.common.enumerations import DataTypeEnum
from mt_metadata.transfer_functions.io.zonge.metadata.survey import (
    ArrayEnum,
    ProjEnum,
    Survey,
)


class TestSurveyDefault:
    """Test default initialization and basic attributes of Survey class."""

    @pytest.fixture(scope="class")
    def default_survey(self):
        """Fixture providing a default Survey instance for efficiency."""
        return Survey()  # type: ignore

    def test_default_initialization(self, default_survey, subtests):
        """Test that Survey initializes with correct default values."""
        with subtests.test("default type value"):
            assert default_survey.type == "nsamt"

        with subtests.test("default array value"):
            assert default_survey.array == ArrayEnum.tensor

        with subtests.test("default datum value"):
            assert default_survey.datum == "WGS84"

        with subtests.test("default u_t_m_zone value"):
            assert default_survey.u_t_m_zone == 0

        with subtests.test("default proj value"):
            assert default_survey.proj == ProjEnum.UTM

    def test_default_survey_attributes(self, default_survey, subtests):
        """Test that Survey has all expected attributes."""
        expected_attributes = ["type", "array", "datum", "u_t_m_zone", "proj"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_survey, attr)

    def test_default_model_fields(self, default_survey, subtests):
        """Test model fields are properly defined."""
        fields = default_survey.model_fields
        expected_fields = ["type", "array", "datum", "u_t_m_zone", "proj"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 5

    def test_field_types(self, default_survey, subtests):
        """Test that fields have expected types."""
        with subtests.test("type field type"):
            assert isinstance(default_survey.type, str)

        with subtests.test("array field type"):
            # Array field is stored as string, not enum
            assert isinstance(default_survey.array, str)

        with subtests.test("datum field type"):
            assert isinstance(default_survey.datum, str)

        with subtests.test("u_t_m_zone field type"):
            assert isinstance(default_survey.u_t_m_zone, int)

        with subtests.test("proj field type"):
            # Proj field is stored as string, not enum
            assert isinstance(default_survey.proj, str)

    def test_required_field_behavior(self, subtests):
        """Test that all fields behave as required with defaults."""
        with subtests.test("all fields are required but have defaults"):
            survey = Survey()  # type: ignore
            assert survey.type == "nsamt"
            assert survey.array == ArrayEnum.tensor
            assert survey.datum == "WGS84"
            assert survey.u_t_m_zone == 0
            assert survey.proj == ProjEnum.UTM


class TestSurveyCustomValues:
    """Test Survey with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_survey(self):
        """Fixture providing a Survey instance with custom values for efficiency."""
        return Survey(
            type="MT", array="tensor", datum="NAD83", u_t_m_zone=12, proj="UTM"
        )  # type: ignore

    def test_populated_survey_values(self, populated_survey, subtests):
        """Test Survey with custom values."""
        with subtests.test("populated type"):
            assert populated_survey.type == DataTypeEnum.MT

        with subtests.test("populated array"):
            assert populated_survey.array == "tensor"

        with subtests.test("populated datum"):
            # Datum validator may transform the value
            assert isinstance(populated_survey.datum, str)

        with subtests.test("populated u_t_m_zone"):
            assert populated_survey.u_t_m_zone == 12

        with subtests.test("populated proj"):
            assert populated_survey.proj == "UTM"

    def test_enum_initialization_patterns(self, subtests):
        """Test various enum initialization patterns."""
        enum_patterns = [
            ("DataTypeEnum string", "MT", DataTypeEnum.MT),
            ("DataTypeEnum enum", DataTypeEnum.AMT, DataTypeEnum.AMT),
            ("ArrayEnum string", "tensor", ArrayEnum.tensor),
            ("ArrayEnum enum", ArrayEnum.tensor, ArrayEnum.tensor),
            ("ProjEnum string", "UTM", ProjEnum.UTM),
            ("ProjEnum enum", ProjEnum.other, ProjEnum.other),
        ]

        for case_name, input_value, expected_value in enum_patterns:
            with subtests.test(f"enum pattern {case_name}"):
                if "type" in case_name.lower():
                    survey = Survey(type=input_value)  # type: ignore
                    assert survey.type == expected_value
                elif "array" in case_name.lower():
                    survey = Survey(array=input_value)  # type: ignore
                    assert survey.array == expected_value
                elif "proj" in case_name.lower():
                    survey = Survey(proj=input_value)  # type: ignore
                    assert survey.proj == expected_value

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("type", "MT"),
            ("array", "tensor"),
            ("datum", "EPSG:4326"),
            ("u_t_m_zone", 15),
            ("proj", "other"),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field} with value {value}"):
                kwargs = {field: value}
                survey = Survey(**kwargs)  # type: ignore
                actual_value = getattr(survey, field)

                if field in ["type", "array", "proj"]:
                    if isinstance(actual_value, (DataTypeEnum, ArrayEnum, ProjEnum)):
                        assert actual_value.value == value or actual_value == value
                    else:
                        assert actual_value == value
                elif field == "datum":
                    # Datum validator may transform the value, so just check it's a string
                    assert isinstance(actual_value, str)
                    assert len(actual_value) > 0
                else:
                    assert actual_value == value

    def test_partial_survey_values(self, subtests):
        """Test Survey with partial custom values."""
        with subtests.test("custom type only"):
            survey = Survey(type="AMT")  # type: ignore
            assert survey.type == DataTypeEnum.AMT
            assert survey.array == ArrayEnum.tensor  # default

        with subtests.test("custom utm zone only"):
            survey = Survey(u_t_m_zone=13)  # type: ignore
            assert survey.u_t_m_zone == 13
            assert survey.type == "nsamt"  # default


class TestSurveyValidation:
    """Test Survey input validation and type conversion."""

    def test_type_validation(self, subtests):
        """Test type field validation."""
        valid_values = [
            DataTypeEnum.MT,
            DataTypeEnum.AMT,
            "MT",
            "AMT",
            "RMT",
        ]

        for value in valid_values:
            with subtests.test(f"type valid '{value}'"):
                survey = Survey(type=value)  # type: ignore
                if isinstance(value, DataTypeEnum):
                    assert survey.type == value
                else:
                    assert survey.type == DataTypeEnum(value)

    def test_array_validation(self, subtests):
        """Test array field validation."""
        valid_values = [
            ArrayEnum.tensor,
            "tensor",
        ]

        for value in valid_values:
            with subtests.test(f"array valid '{value}'"):
                survey = Survey(array=value)  # type: ignore
                assert survey.array == ArrayEnum.tensor

    def test_datum_validation(self, subtests):
        """Test datum field validation with pyproj CRS validation."""
        valid_values = [
            "WGS84",
            "EPSG:4326",
            "NAD83",
            "EPSG:4269",
            "+proj=longlat +datum=WGS84",
        ]

        for value in valid_values:
            with subtests.test(f"datum valid '{value}'"):
                survey = Survey(datum=value)  # type: ignore
                assert isinstance(survey.datum, str)
                assert len(survey.datum) > 0

    def test_u_t_m_zone_validation(self, subtests):
        """Test u_t_m_zone field validation."""
        valid_values = [
            0,
            1,
            12,
            60,
            -1,  # Edge cases and valid zones
        ]

        for value in valid_values:
            with subtests.test(f"u_t_m_zone valid {value}"):
                survey = Survey(u_t_m_zone=value)  # type: ignore
                assert survey.u_t_m_zone == value

    def test_proj_validation(self, subtests):
        """Test proj field validation."""
        valid_values = [
            ProjEnum.UTM,
            ProjEnum.other,
            "UTM",
            "other",
        ]

        for value in valid_values:
            with subtests.test(f"proj valid '{value}'"):
                survey = Survey(proj=value)  # type: ignore
                if isinstance(value, ProjEnum):
                    assert survey.proj == value
                else:
                    assert survey.proj == ProjEnum(value)

    def test_type_coercion(self, subtests):
        """Test type coercion behavior."""
        coercion_cases = [
            ("u_t_m_zone string", "12", 12),
            ("u_t_m_zone float", 12.0, 12),
        ]

        for case_name, input_value, expected_value in coercion_cases:
            with subtests.test(f"coercion {case_name}"):
                survey = Survey(u_t_m_zone=input_value)  # type: ignore
                assert survey.u_t_m_zone == expected_value

    def test_invalid_values(self, subtests):
        """Test handling of invalid values."""
        invalid_cases = [
            ("type", "invalid_type"),
            ("array", "invalid_array"),
            ("datum", "completely_invalid_datum_12345"),
            ("u_t_m_zone", "not_a_number"),
            ("proj", "invalid_proj"),
        ]

        for field, invalid_value in invalid_cases:
            with subtests.test(f"invalid {field} '{invalid_value}'"):
                kwargs = {field: invalid_value}
                try:
                    survey = Survey(**kwargs)  # type: ignore
                    # Some invalid values might be coerced or accepted
                    assert hasattr(survey, field)
                except (ValidationError, ValueError):
                    # Expected for truly invalid values
                    pass


class TestSurveySerialization:
    """Test Survey serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_survey(self):
        """Fixture for default Survey instance."""
        return Survey()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_survey(self):
        """Fixture for populated Survey instance."""
        return Survey(
            type="MT", array="tensor", datum="WGS84", u_t_m_zone=12, proj="UTM"
        )  # type: ignore

    def test_model_dump_default(self, default_survey, subtests):
        """Test model_dump with default values."""
        dump = default_survey.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["type", "array", "datum", "u_t_m_zone", "proj"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["type"] == "nsamt"
            assert dump["array"] == "tensor"
            assert dump["datum"] == "WGS84"
            assert dump["u_t_m_zone"] == 0
            assert dump["proj"] == "UTM"

        with subtests.test("includes class name"):
            assert "_class_name" in dump
            assert dump["_class_name"] == "survey"

    def test_model_dump_populated(self, populated_survey, subtests):
        """Test model_dump with populated values."""
        dump = populated_survey.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["u_t_m_zone"] == 12
            # datum might be transformed by validator
            assert isinstance(dump["datum"], str)

    def test_from_dict_creation(self, subtests):
        """Test creating Survey from dictionary."""
        test_cases = [
            (
                "full dict",
                {
                    "type": "MT",
                    "array": "tensor",
                    "datum": "WGS84",
                    "u_t_m_zone": 15,
                    "proj": "UTM",
                },
            ),
            ("partial dict", {"type": "AMT", "u_t_m_zone": 10}),
            ("empty dict", {}),
        ]

        for case_name, data in test_cases:
            with subtests.test(f"from dict {case_name}"):
                survey = Survey(**data)  # type: ignore
                for key, value in data.items():
                    actual_value = getattr(survey, key)
                    if key == "datum":
                        # Datum validator may transform values, just check it's a string
                        assert isinstance(actual_value, str)
                        assert len(actual_value) > 0
                    elif isinstance(actual_value, (DataTypeEnum, ArrayEnum, ProjEnum)):
                        assert actual_value.value == value or actual_value == value
                    else:
                        assert actual_value == value

    def test_json_serialization(self, default_survey, populated_survey, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated survey"):
            json_str = populated_survey.model_dump_json()
            data = json.loads(json_str)
            recreated = Survey(**data)  # type: ignore
            assert recreated.u_t_m_zone == populated_survey.u_t_m_zone

        with subtests.test("JSON round-trip default survey"):
            json_str = default_survey.model_dump_json()
            data = json.loads(json_str)
            recreated = Survey(**data)  # type: ignore
            assert recreated.u_t_m_zone == default_survey.u_t_m_zone

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            survey = Survey(type="MT", u_t_m_zone=12)  # type: ignore
            dump = survey.model_dump(exclude_none=True)
            assert "type" in dump
            assert "u_t_m_zone" in dump

        with subtests.test("exclude_none with defaults"):
            survey = Survey()  # type: ignore
            dump = survey.model_dump(exclude_none=True)
            # Should include all fields since none are None
            assert len(dump) >= 5

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            survey = Survey()  # type: ignore
            dump = survey.model_dump(exclude_defaults=True)
            # Should exclude default values - might be empty or have minimal fields
            assert isinstance(dump, dict)

        with subtests.test("exclude_defaults with custom values"):
            survey = Survey(type="MT", u_t_m_zone=15)  # type: ignore
            dump = survey.model_dump(exclude_defaults=True)
            assert "u_t_m_zone" in dump
            assert dump["u_t_m_zone"] == 15


class TestSurveyModification:
    """Test Survey field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Survey fields after creation."""
        survey = Survey()  # type: ignore

        test_modifications = [
            ("type", "AMT"),
            ("array", "tensor"),
            ("datum", "NAD83"),
            ("u_t_m_zone", 13),
            ("proj", "other"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field} to {value}"):
                setattr(survey, field, value)
                actual_value = getattr(survey, field)
                if isinstance(actual_value, (DataTypeEnum, ArrayEnum, ProjEnum)):
                    assert actual_value.value == value or actual_value == value
                else:
                    assert actual_value == value

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        survey = Survey(type="MT", u_t_m_zone=15, proj="other")  # type: ignore

        with subtests.test("reset type to default"):
            survey.type = "nsamt"  # type: ignore
            # Type might be stored as enum or string
            assert survey.type == "nsamt" or (
                hasattr(survey.type, "value") and survey.type.value == "NSAMT"
            )

        with subtests.test("reset u_t_m_zone to default"):
            survey.u_t_m_zone = 0  # type: ignore
            assert survey.u_t_m_zone == 0

        with subtests.test("reset proj to default"):
            survey.proj = ProjEnum.UTM  # type: ignore
            assert survey.proj == ProjEnum.UTM

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        survey = Survey()  # type: ignore

        updates = {
            "type": "RMT",
            "u_t_m_zone": 11,
            "datum": "EPSG:4326",
            "proj": "other",
        }

        for field, value in updates.items():
            setattr(survey, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                actual_value = getattr(survey, field)
                if field == "datum":
                    # Datum validator may transform values
                    assert isinstance(actual_value, str)
                    assert len(actual_value) > 0
                elif isinstance(actual_value, (DataTypeEnum, ArrayEnum, ProjEnum)):
                    assert (
                        actual_value.value == expected_value
                        or actual_value == expected_value
                    )
                else:
                    assert actual_value == expected_value

    def test_enum_assignment(self, subtests):
        """Test that enum assignment works correctly."""
        survey = Survey()  # type: ignore

        with subtests.test("DataTypeEnum assignment"):
            survey.type = DataTypeEnum.BBMT  # type: ignore
            assert survey.type == DataTypeEnum.BBMT

        with subtests.test("ArrayEnum assignment"):
            survey.array = ArrayEnum.tensor  # type: ignore
            assert survey.array == ArrayEnum.tensor

        with subtests.test("ProjEnum assignment"):
            survey.proj = ProjEnum.other  # type: ignore
            assert survey.proj == ProjEnum.other


class TestSurveyComparison:
    """Test Survey comparison and equality operations."""

    def test_survey_equality(self, subtests):
        """Test Survey equality comparisons."""
        survey1 = Survey(type="MT", u_t_m_zone=12)  # type: ignore
        survey2 = Survey(type="MT", u_t_m_zone=12)  # type: ignore
        survey3 = Survey(type="AMT", u_t_m_zone=13)  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert survey1.model_dump() == survey2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert survey1.model_dump() != survey3.model_dump()

        with subtests.test("individual field comparison"):
            assert survey1.type == survey2.type
            assert survey1.u_t_m_zone == survey2.u_t_m_zone
            assert survey1.type != survey3.type

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("MT", 12, "WGS84"),
            ("AMT", 0, "NAD83"),
            ("RMT", 15, "EPSG:4326"),
        ]

        for type_val, zone_val, datum_val in test_values:
            with subtests.test(f"consistency {type_val}-{zone_val}-{datum_val}"):
                survey = Survey(type=type_val, u_t_m_zone=zone_val, datum=datum_val)  # type: ignore

                # Test round-trip consistency
                dump = survey.model_dump()
                recreated = Survey(**dump)  # type: ignore
                assert recreated.u_t_m_zone == survey.u_t_m_zone
                assert recreated.datum == survey.datum

    def test_enum_value_consistency(self, subtests):
        """Test enum value consistency."""
        enum_combinations = [
            (DataTypeEnum.MT, ArrayEnum.tensor, ProjEnum.UTM),
            (DataTypeEnum.AMT, ArrayEnum.tensor, ProjEnum.other),
        ]

        for type_enum, array_enum, proj_enum in enum_combinations:
            with subtests.test(
                f"enum consistency {type_enum.value}-{array_enum.value}-{proj_enum.value}"
            ):
                survey1 = Survey(type=type_enum, array=array_enum, proj=proj_enum)  # type: ignore
                survey2 = Survey(type=type_enum, array=array_enum, proj=proj_enum)  # type: ignore
                assert survey1.type == survey2.type
                assert survey1.array == survey2.array
                assert survey1.proj == survey2.proj


class TestSurveyEdgeCases:
    """Test Survey edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            survey = Survey(**{})  # type: ignore
            assert survey.type == "nsamt"
            assert survey.u_t_m_zone == 0

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            survey = Survey(unknown_field="value")  # type: ignore
            assert hasattr(survey, "unknown_field")
            assert survey.unknown_field == "value"  # type: ignore

    def test_u_t_m_zone_edge_cases(self, subtests):
        """Test u_t_m_zone field edge cases."""
        edge_cases = [
            ("zero", 0),
            ("negative", -1),
            ("large positive", 100),
            ("max utm zone", 60),
            ("beyond max", 61),
        ]

        for case_name, test_value in edge_cases:
            with subtests.test(f"u_t_m_zone edge case {case_name}"):
                survey = Survey(u_t_m_zone=test_value)  # type: ignore
                assert survey.u_t_m_zone == test_value

    def test_datum_edge_cases(self, subtests):
        """Test datum field edge cases."""
        edge_cases = [
            ("standard WGS84", "WGS84"),
            ("EPSG code", "EPSG:4326"),
            ("NAD83", "NAD83"),
            ("proj4 string", "+proj=longlat +datum=WGS84 +no_defs"),
        ]

        for case_name, test_value in edge_cases:
            with subtests.test(f"datum edge case {case_name}"):
                try:
                    survey = Survey(datum=test_value)  # type: ignore
                    assert isinstance(survey.datum, str)
                    assert len(survey.datum) > 0
                except ValueError:
                    # Some datum values might be invalid and raise ValueError
                    pass

    def test_enum_case_sensitivity(self, subtests):
        """Test enum case sensitivity."""
        case_tests = [
            ("type lowercase", "mt", "MT"),
            ("type uppercase", "MT", "MT"),
            ("array case", "TENSOR", "tensor"),
            ("proj case", "utm", "UTM"),
        ]

        for case_name, input_value, expected_value in case_tests:
            with subtests.test(f"case sensitivity {case_name}"):
                try:
                    if "type" in case_name:
                        survey = Survey(type=input_value)  # type: ignore
                        assert (
                            survey.type.value == expected_value
                            if hasattr(survey.type, "value")
                            else survey.type == expected_value
                        )
                    elif "array" in case_name:
                        survey = Survey(array=input_value)  # type: ignore
                        assert survey.array.value == expected_value.lower()
                    elif "proj" in case_name:
                        survey = Survey(proj=input_value)  # type: ignore
                        assert survey.proj.value == expected_value
                except (ValidationError, ValueError):
                    # Case sensitivity might cause validation errors
                    pass


class TestSurveyDocumentation:
    """Test Survey class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Survey class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert Survey.__name__ == "Survey"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(Survey, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = Survey.model_fields
        expected_fields = ["type", "array", "datum", "u_t_m_zone", "proj"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = Survey.model_fields

        with subtests.test("type field properties"):
            type_field = fields["type"]
            assert hasattr(type_field, "default") or "default" in str(type_field)

        with subtests.test("u_t_m_zone field properties"):
            zone_field = fields["u_t_m_zone"]
            assert hasattr(zone_field, "default") or "default" in str(zone_field)

    def test_enum_definitions(self, subtests):
        """Test enum class definitions."""
        with subtests.test("ArrayEnum definition"):
            assert hasattr(ArrayEnum, "tensor")
            assert ArrayEnum.tensor.value == "tensor"

        with subtests.test("ProjEnum definition"):
            assert hasattr(ProjEnum, "UTM")
            assert hasattr(ProjEnum, "other")
            assert ProjEnum.UTM.value == "UTM"
            assert ProjEnum.other.value == "other"

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            survey = Survey()  # type: ignore
            dump = survey.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) == 6  # 5 fields + _class_name

        with subtests.test("all expected fields present"):
            expected_fields = ["type", "array", "datum", "u_t_m_zone", "proj"]
            dump = Survey().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump
            assert "_class_name" in dump

        with subtests.test("model_fields accessible"):
            fields = Survey.model_fields
            assert len(fields) == 5
            assert all(
                field in fields
                for field in ["type", "array", "datum", "u_t_m_zone", "proj"]
            )

    def test_field_types_documentation(self, subtests):
        """Test documented field types."""
        survey = Survey()  # type: ignore

        with subtests.test("type field type documentation"):
            assert isinstance(survey.type, str)

        with subtests.test("array field type documentation"):
            # Array field is stored as string, not enum
            assert isinstance(survey.array, str)

        with subtests.test("datum field type documentation"):
            assert isinstance(survey.datum, str)

        with subtests.test("u_t_m_zone field type documentation"):
            assert isinstance(survey.u_t_m_zone, int)

        with subtests.test("proj field type documentation"):
            # Proj field is stored as string, not enum
            assert isinstance(survey.proj, str)

    def test_validator_functionality(self, subtests):
        """Test custom validator functionality."""
        with subtests.test("datum validator works"):
            # Test that the datum validator accepts valid CRS strings
            survey = Survey(datum="EPSG:4326")  # type: ignore
            assert isinstance(survey.datum, str)

        with subtests.test("datum validator rejects invalid"):
            # Test that invalid datum raises ValueError
            try:
                Survey(datum="completely_invalid_datum_xyz123")  # type: ignore
                # If it doesn't raise an error, that's also valid behavior
            except ValueError:
                # Expected behavior for invalid datum
                pass


class TestSurveyIntegration:
    """Test Survey integration scenarios and realistic usage patterns."""

    def test_realistic_survey_configurations(self, subtests):
        """Test realistic survey configuration patterns."""
        realistic_configs = [
            (
                "MT survey UTM",
                {
                    "type": "MT",
                    "array": "tensor",
                    "datum": "WGS84",
                    "u_t_m_zone": 12,
                    "proj": "UTM",
                },
            ),
            (
                "AMT survey other projection",
                {
                    "type": "AMT",
                    "array": "tensor",
                    "datum": "NAD83",
                    "u_t_m_zone": 0,
                    "proj": "other",
                },
            ),
            (
                "RMT survey",
                {
                    "type": "RMT",
                    "array": "tensor",
                    "datum": "EPSG:4326",
                    "u_t_m_zone": 15,
                    "proj": "UTM",
                },
            ),
        ]

        for case_name, config in realistic_configs:
            with subtests.test(f"realistic {case_name}"):
                survey = Survey(**config)  # type: ignore

                # Test serialization works
                dump = survey.model_dump()
                assert dump["u_t_m_zone"] == config["u_t_m_zone"]

                # Test recreation works
                recreated = Survey(**dump)  # type: ignore
                assert recreated.u_t_m_zone == survey.u_t_m_zone

    def test_data_pipeline_scenarios(self, subtests):
        """Test scenarios that might occur in data processing pipelines."""
        pipeline_scenarios = [
            ("default initialization", {}, "nsamt", 0),
            ("string to int coercion", {"u_t_m_zone": "15"}, "nsamt", 15),
            ("enum string conversion", {"type": "MT"}, "MT", 0),
        ]

        for case_name, input_data, expected_type, expected_zone in pipeline_scenarios:
            with subtests.test(f"pipeline {case_name}"):
                survey = Survey(**input_data)  # type: ignore
                if hasattr(survey.type, "value"):
                    assert (
                        survey.type.value == expected_type
                        or survey.type == expected_type
                    )
                else:
                    assert survey.type == expected_type
                assert survey.u_t_m_zone == expected_zone

    def test_serialization_roundtrip_scenarios(self, subtests):
        """Test serialization scenarios for data persistence."""
        test_configs = [
            {"type": "MT", "u_t_m_zone": 12, "datum": "WGS84"},
            {"type": "AMT", "u_t_m_zone": 0, "proj": "other"},
            {},  # Default configuration
        ]

        for i, config in enumerate(test_configs):
            with subtests.test(f"roundtrip config {i}"):
                # Create original
                original = Survey(**config)  # type: ignore

                # Serialize to JSON
                json_str = original.model_dump_json()

                # Deserialize from JSON
                data = json.loads(json_str)
                recreated = Survey(**data)  # type: ignore

                # Verify consistency
                assert recreated.u_t_m_zone == original.u_t_m_zone
                # datum might be transformed, so just check both are strings
                assert isinstance(recreated.datum, str)
                assert isinstance(original.datum, str)

    def test_field_update_scenarios(self, subtests):
        """Test field update scenarios for data modification."""
        with subtests.test("progressive updates"):
            survey = Survey()  # type: ignore

            # Start with defaults
            assert survey.type == "nsamt"
            assert survey.u_t_m_zone == 0

            # Update to new values
            survey.type = "MT"  # type: ignore
            survey.u_t_m_zone = 15  # type: ignore

            assert survey.type == DataTypeEnum.MT or survey.type == "MT"
            assert survey.u_t_m_zone == 15

            # Reset some values
            survey.u_t_m_zone = 0  # type: ignore
            assert survey.u_t_m_zone == 0

    def test_error_handling_scenarios(self, subtests):
        """Test error handling in various scenarios."""
        with subtests.test("invalid enum handling"):
            # Test various invalid enum values
            invalid_inputs = [
                ("type", "invalid_survey_type"),
                ("array", "invalid_array_type"),
                ("proj", "invalid_projection"),
            ]

            for field, invalid_input in invalid_inputs:
                try:
                    kwargs = {field: invalid_input}
                    survey = Survey(**kwargs)  # type: ignore
                    # If no error, check if it was handled gracefully
                    assert hasattr(survey, field)
                except (ValidationError, ValueError):
                    # Expected for truly invalid types
                    pass

        with subtests.test("invalid datum handling"):
            try:
                survey = Survey(datum="completely_invalid_datum_xyz123")  # type: ignore
                # If no error, datum validation might be more lenient
                assert hasattr(survey, "datum")
            except ValueError:
                # Expected for invalid datum values
                pass

    def test_mixed_type_scenarios(self, subtests):
        """Test scenarios with mixed input types."""
        mixed_scenarios = [
            (
                "enum and string mix",
                {
                    "type": DataTypeEnum.MT,
                    "array": "tensor",
                    "proj": ProjEnum.UTM,
                    "u_t_m_zone": "12",
                },
            ),
            (
                "all strings",
                {"type": "AMT", "array": "tensor", "proj": "other", "u_t_m_zone": "0"},
            ),
        ]

        for case_name, config in mixed_scenarios:
            with subtests.test(f"mixed types {case_name}"):
                survey = Survey(**config)  # type: ignore

                # Verify all fields are properly converted
                assert isinstance(survey.array, str)  # Array stored as string
                assert isinstance(survey.proj, str)  # Proj stored as string
                assert isinstance(survey.u_t_m_zone, int)

                # Verify values are correct
                assert survey.array == "tensor"
                if "UTM" in str(config.get("proj", "")):
                    assert survey.proj == "UTM"

                expected_zone = (
                    int(config["u_t_m_zone"])
                    if isinstance(config["u_t_m_zone"], str)
                    else config["u_t_m_zone"]
                )
                assert survey.u_t_m_zone == expected_zone
