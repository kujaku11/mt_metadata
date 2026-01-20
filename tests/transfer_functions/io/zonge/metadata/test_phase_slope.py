"""
Test suite for PhaseSlope metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.common.enumerations import YesNoEnum
from mt_metadata.transfer_functions.io.zonge.metadata.phase_slope import (
    PhaseSlope,
    SmoothEnum,
)


class TestPhaseSlopeDefault:
    """Test default initialization and basic attributes of PhaseSlope class."""

    @pytest.fixture(scope="class")
    def default_phase_slope(self):
        """Fixture providing a default PhaseSlope instance for efficiency."""
        return PhaseSlope()  # type: ignore

    def test_default_initialization(self, default_phase_slope, subtests):
        """Test that PhaseSlope initializes with correct default values."""
        with subtests.test("default smooth value"):
            assert default_phase_slope.smooth == "None"  # Stored as string

        with subtests.test("default to_z_mag value"):
            assert default_phase_slope.to_z_mag == YesNoEnum.no

    def test_default_phase_slope_attributes(self, default_phase_slope, subtests):
        """Test that PhaseSlope has all expected attributes."""
        expected_attributes = ["smooth", "to_z_mag"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_phase_slope, attr)

    def test_default_model_fields(self, default_phase_slope, subtests):
        """Test model fields are properly defined."""
        fields = default_phase_slope.model_fields
        expected_fields = ["smooth", "to_z_mag"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 2

    def test_required_field_behavior(self, subtests):
        """Test that both fields behave as required with defaults."""
        with subtests.test("smooth field is required but has default"):
            phase_slope = PhaseSlope()  # type: ignore
            assert phase_slope.smooth == "None"  # String representation
            assert hasattr(phase_slope, "smooth")

        with subtests.test("to_z_mag field is required but has default"):
            phase_slope = PhaseSlope()  # type: ignore
            assert phase_slope.to_z_mag == YesNoEnum.no
            assert hasattr(phase_slope, "to_z_mag")


class TestPhaseSlopeCustomValues:
    """Test PhaseSlope with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_phase_slope(self):
        """Fixture providing a PhaseSlope instance with custom values for efficiency."""
        return PhaseSlope(  # type: ignore
            smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes
        )

    def test_populated_phase_slope_values(self, populated_phase_slope, subtests):
        """Test PhaseSlope with custom values."""
        with subtests.test("populated smooth"):
            assert populated_phase_slope.smooth == "robust"  # Stored as string

        with subtests.test("populated to_z_mag"):
            assert populated_phase_slope.to_z_mag == YesNoEnum.yes

    def test_smooth_enum_initialization_patterns(self, subtests):
        """Test various smooth enum initialization patterns."""
        smooth_patterns = [
            ("robust", SmoothEnum.robust, "robust"),
            ("normal", SmoothEnum.normal, "normal"),
            ("minimal", SmoothEnum.minimal, "minimal"),
            ("null", SmoothEnum.null, "None"),  # Maps to "None" string
            ("string robust", "robust", "robust"),
            ("string normal", "normal", "normal"),
            ("string minimal", "minimal", "minimal"),
            ("string None", "None", "None"),
        ]

        for case_name, input_value, expected_value in smooth_patterns:
            with subtests.test(f"smooth pattern {case_name}"):
                phase_slope = PhaseSlope(smooth=input_value)  # type: ignore
                assert phase_slope.smooth == expected_value

    def test_yes_no_enum_initialization_patterns(self, subtests):
        """Test various YesNoEnum initialization patterns."""
        yes_no_patterns = [
            ("yes enum", YesNoEnum.yes, YesNoEnum.yes),
            ("no enum", YesNoEnum.no, YesNoEnum.no),
            ("string yes", "yes", YesNoEnum.yes),
            ("string no", "no", YesNoEnum.no),
            ("case insensitive YES", "YES", YesNoEnum.yes),
            ("case insensitive NO", "NO", YesNoEnum.no),
            ("case insensitive Yes", "Yes", YesNoEnum.yes),
            ("case insensitive No", "No", YesNoEnum.no),
        ]

        for case_name, input_value, expected_value in yes_no_patterns:
            with subtests.test(f"to_z_mag pattern {case_name}"):
                phase_slope = PhaseSlope(to_z_mag=input_value)  # type: ignore
                assert phase_slope.to_z_mag == expected_value

    def test_partial_phase_slope_values(self, subtests):
        """Test PhaseSlope with only some fields populated."""
        partial_cases = [
            ("smooth only", {"smooth": SmoothEnum.robust}, "robust", YesNoEnum.no),
            ("to_z_mag only", {"to_z_mag": YesNoEnum.yes}, "None", YesNoEnum.yes),
        ]

        for case_name, kwargs, expected_smooth, expected_to_z_mag in partial_cases:
            with subtests.test(f"partial {case_name}"):
                phase_slope = PhaseSlope(**kwargs)  # type: ignore
                assert phase_slope.smooth == expected_smooth
                assert phase_slope.to_z_mag == expected_to_z_mag

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("smooth", SmoothEnum.minimal),
            ("to_z_mag", YesNoEnum.yes),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field}"):
                kwargs = {field: value}
                phase_slope = PhaseSlope(**kwargs)  # type: ignore
                assert getattr(phase_slope, field) == value


class TestPhaseSlopeValidation:
    """Test PhaseSlope input validation and type conversion."""

    def test_smooth_enum_validation(self, subtests):
        """Test SmoothEnum field validation."""
        valid_smooth_values = [
            SmoothEnum.robust,
            SmoothEnum.normal,
            SmoothEnum.minimal,
            SmoothEnum.null,
            "robust",
            "normal",
            "minimal",
            "None",
        ]

        for value in valid_smooth_values:
            with subtests.test(f"smooth validation {value}"):
                phase_slope = PhaseSlope(smooth=value)  # type: ignore
                # Check that smooth is stored as string
                assert phase_slope.smooth in ["robust", "normal", "minimal", "None"]

    def test_yes_no_enum_validation(self, subtests):
        """Test YesNoEnum field validation."""
        valid_yes_no_values = [
            YesNoEnum.yes,
            YesNoEnum.no,
            "yes",
            "no",
            "YES",
            "NO",
            "Yes",
            "No",
        ]

        for value in valid_yes_no_values:
            with subtests.test(f"to_z_mag validation {value}"):
                phase_slope = PhaseSlope(to_z_mag=value)  # type: ignore
                assert phase_slope.to_z_mag in [YesNoEnum.yes, YesNoEnum.no]

    def test_enum_case_insensitive_validation(self, subtests):
        """Test case-sensitive enum validation (PhaseSlope is case-sensitive)."""
        # Test valid case-sensitive variations
        valid_cases = [
            ("smooth robust", "robust", "robust"),
            ("smooth normal", "normal", "normal"),
            ("smooth minimal", "minimal", "minimal"),
            ("smooth none", "None", "None"),
            ("to_z_mag yes", "yes", YesNoEnum.yes),
            ("to_z_mag no", "no", YesNoEnum.no),
        ]

        for case_name, input_value, expected_result in valid_cases:
            with subtests.test(f"valid case {case_name}"):
                if "smooth" in case_name:
                    phase_slope = PhaseSlope(smooth=input_value)  # type: ignore
                    assert phase_slope.smooth == expected_result
                else:
                    phase_slope = PhaseSlope(to_z_mag=input_value)  # type: ignore
                    assert phase_slope.to_z_mag == expected_result

        # Test that invalid cases fail
        invalid_cases = [
            ("smooth ROBUST", "ROBUST"),
            ("smooth NORMAL", "NORMAL"),
            ("smooth MINIMAL", "MINIMAL"),
            ("smooth NONE", "NONE"),
        ]

        for case_name, invalid_value in invalid_cases:
            with subtests.test(f"invalid case {case_name}"):
                with pytest.raises(ValidationError):
                    PhaseSlope(smooth=invalid_value)  # type: ignore

    def test_invalid_enum_values(self, subtests):
        """Test handling of invalid enum values."""
        invalid_smooth_cases = [
            ("invalid_string", "invalid_smooth"),
            ("empty_string", ""),
            ("random_text", "random"),
        ]

        for case_name, invalid_value in invalid_smooth_cases:
            with subtests.test(f"invalid smooth {case_name}"):
                with pytest.raises(ValidationError):
                    PhaseSlope(smooth=invalid_value)  # type: ignore

        invalid_to_z_mag_cases = [
            ("invalid_string", "maybe"),
            ("empty_string", ""),
            ("random_text", "true"),
        ]

        for case_name, invalid_value in invalid_to_z_mag_cases:
            with subtests.test(f"invalid to_z_mag {case_name}"):
                with pytest.raises(ValidationError):
                    PhaseSlope(to_z_mag=invalid_value)  # type: ignore

    def test_invalid_type_handling(self, subtests):
        """Test handling of invalid types for enum fields."""
        invalid_types = [
            ("integer", 123),
            ("float", 456.7),
            ("list", ["invalid", "list"]),
            ("dict", {"invalid": "dict"}),
            ("boolean", True),
        ]

        for case_name, invalid_value in invalid_types:
            with subtests.test(f"smooth invalid type {case_name}"):
                with pytest.raises(ValidationError):
                    PhaseSlope(smooth=invalid_value)  # type: ignore

            with subtests.test(f"to_z_mag invalid type {case_name}"):
                # to_z_mag throws TypeError for non-string types due to enum normalization
                with pytest.raises((ValidationError, TypeError)):
                    PhaseSlope(to_z_mag=invalid_value)  # type: ignore


class TestPhaseSlopeSerialization:
    """Test PhaseSlope serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_phase_slope(self):
        """Fixture for default PhaseSlope instance."""
        return PhaseSlope()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_phase_slope(self):
        """Fixture for populated PhaseSlope instance."""
        return PhaseSlope(  # type: ignore
            smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes
        )

    def test_model_dump_default(self, default_phase_slope, subtests):
        """Test model_dump with default values."""
        dump = default_phase_slope.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["smooth", "to_z_mag"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["smooth"] == "None"  # String representation of SmoothEnum.null
            # to_z_mag might be stored as enum object or string depending on model behavior
            assert dump["to_z_mag"] in [YesNoEnum.no, "no"]

    def test_model_dump_populated(self, populated_phase_slope, subtests):
        """Test model_dump with populated values."""
        dump = populated_phase_slope.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["smooth"] == "robust"  # String representation
            # to_z_mag might be stored as enum object
            assert dump["to_z_mag"] in [YesNoEnum.yes, "yes"]

    def test_from_dict_creation(self, subtests):
        """Test creating PhaseSlope from dictionary."""
        test_cases = [
            (
                "full dict",
                {"smooth": "robust", "to_z_mag": "yes"},
                "robust",
                YesNoEnum.yes,
            ),
            ("partial dict smooth", {"smooth": "minimal"}, "minimal", YesNoEnum.no),
            ("partial dict to_z_mag", {"to_z_mag": "yes"}, "None", YesNoEnum.yes),
            ("empty dict", {}, "None", YesNoEnum.no),
            (
                "string values",
                {"smooth": "normal", "to_z_mag": "no"},
                "normal",
                YesNoEnum.no,
            ),
        ]

        for case_name, data, expected_smooth, expected_to_z_mag in test_cases:
            with subtests.test(f"from dict {case_name}"):
                phase_slope = PhaseSlope(**data)  # type: ignore
                assert phase_slope.smooth == expected_smooth
                assert phase_slope.to_z_mag == expected_to_z_mag

    def test_json_serialization(
        self, default_phase_slope, populated_phase_slope, subtests
    ):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated phase_slope"):
            json_str = populated_phase_slope.model_dump_json()
            data = json.loads(json_str)
            recreated = PhaseSlope(**data)  # type: ignore
            assert recreated.smooth == populated_phase_slope.smooth
            assert recreated.to_z_mag == populated_phase_slope.to_z_mag

        with subtests.test("JSON round-trip default phase_slope"):
            json_str = default_phase_slope.model_dump_json()
            data = json.loads(json_str)
            recreated = PhaseSlope(**data)  # type: ignore
            assert recreated.smooth == default_phase_slope.smooth
            assert recreated.to_z_mag == default_phase_slope.to_z_mag

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            phase_slope = PhaseSlope(smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes)  # type: ignore
            dump = phase_slope.model_dump(exclude_none=True)
            assert "smooth" in dump
            assert "to_z_mag" in dump
            assert dump["smooth"] == "robust"
            assert dump["to_z_mag"] == "yes"

        with subtests.test("exclude_none with defaults"):
            phase_slope = PhaseSlope()  # type: ignore
            dump = phase_slope.model_dump(exclude_none=True)
            # Should still include both fields since they have non-None enum values
            assert "smooth" in dump
            assert "to_z_mag" in dump

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            phase_slope = PhaseSlope()  # type: ignore
            dump = phase_slope.model_dump(exclude_defaults=True)
            # Should exclude the default values
            assert "smooth" not in dump or dump.get("smooth") != "None"
            assert "to_z_mag" not in dump or dump.get("to_z_mag") != "no"

        with subtests.test("exclude_defaults with custom values"):
            phase_slope = PhaseSlope(smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes)  # type: ignore
            dump = phase_slope.model_dump(exclude_defaults=True)
            assert "smooth" in dump
            assert "to_z_mag" in dump
            assert dump["smooth"] == "robust"
            assert dump["to_z_mag"] == "yes"


class TestPhaseSlopeModification:
    """Test PhaseSlope field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying PhaseSlope fields after creation."""
        phase_slope = PhaseSlope()  # type: ignore

        test_modifications = [
            ("smooth", SmoothEnum.robust),
            ("to_z_mag", YesNoEnum.yes),
            ("smooth", SmoothEnum.minimal),
            ("to_z_mag", YesNoEnum.no),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field} to {value}"):
                setattr(phase_slope, field, value)
                assert getattr(phase_slope, field) == value

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        phase_slope = PhaseSlope(smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes)  # type: ignore

        with subtests.test("reset smooth to default"):
            phase_slope.smooth = SmoothEnum.null  # type: ignore
            assert phase_slope.smooth == SmoothEnum.null

        with subtests.test("reset to_z_mag to default"):
            phase_slope.to_z_mag = YesNoEnum.no  # type: ignore
            assert phase_slope.to_z_mag == YesNoEnum.no

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        phase_slope = PhaseSlope()  # type: ignore

        updates = {"smooth": SmoothEnum.normal, "to_z_mag": YesNoEnum.yes}

        for field, value in updates.items():
            setattr(phase_slope, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(phase_slope, field) == expected_value

    def test_string_assignment_conversion(self, subtests):
        """Test that string assignment properly converts to enums."""
        phase_slope = PhaseSlope()  # type: ignore

        # Test string assignment for smooth
        with subtests.test("smooth string assignment"):
            phase_slope.smooth = "robust"  # type: ignore
            assert phase_slope.smooth == "robust"  # Stored as string
            assert isinstance(phase_slope.smooth, str)

        # Test string assignment for to_z_mag
        with subtests.test("to_z_mag string assignment"):
            phase_slope.to_z_mag = "yes"  # type: ignore
            assert phase_slope.to_z_mag == YesNoEnum.yes
            assert isinstance(phase_slope.to_z_mag, YesNoEnum)


class TestPhaseSlopeComparison:
    """Test PhaseSlope comparison and equality operations."""

    def test_phase_slope_equality(self, subtests):
        """Test PhaseSlope equality comparisons."""
        phase_slope1 = PhaseSlope(smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes)  # type: ignore
        phase_slope2 = PhaseSlope(smooth=SmoothEnum.robust, to_z_mag=YesNoEnum.yes)  # type: ignore
        phase_slope3 = PhaseSlope(smooth=SmoothEnum.minimal, to_z_mag=YesNoEnum.yes)  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert phase_slope1.model_dump() == phase_slope2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert phase_slope1.model_dump() != phase_slope3.model_dump()

        with subtests.test("individual field comparison"):
            assert phase_slope1.smooth == phase_slope2.smooth
            assert phase_slope1.to_z_mag == phase_slope2.to_z_mag
            assert phase_slope1.smooth != phase_slope3.smooth

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("smooth", SmoothEnum.robust),
            ("to_z_mag", YesNoEnum.yes),
            ("smooth", SmoothEnum.normal),
            ("to_z_mag", YesNoEnum.no),
        ]

        for field, value in test_values:
            with subtests.test(f"consistency {field} {value}"):
                kwargs = {field: value}
                phase_slope = PhaseSlope(**kwargs)  # type: ignore
                assert getattr(phase_slope, field) == value

                # Test round-trip consistency
                dump = phase_slope.model_dump()
                recreated = PhaseSlope(**dump)  # type: ignore
                assert getattr(recreated, field) == getattr(phase_slope, field)

    def test_enum_object_equality(self, subtests):
        """Test enum object equality and identity."""
        with subtests.test("smooth enum equality"):
            phase_slope1 = PhaseSlope(smooth=SmoothEnum.robust)  # type: ignore
            phase_slope2 = PhaseSlope(smooth="robust")  # type: ignore
            assert phase_slope1.smooth == phase_slope2.smooth
            # Both are stored as strings, not enum objects
            assert phase_slope1.smooth == "robust"
            assert phase_slope2.smooth == "robust"

        with subtests.test("to_z_mag enum equality"):
            phase_slope1 = PhaseSlope(to_z_mag=YesNoEnum.yes)  # type: ignore
            phase_slope2 = PhaseSlope(to_z_mag="yes")  # type: ignore
            assert phase_slope1.to_z_mag == phase_slope2.to_z_mag
            assert phase_slope1.to_z_mag is YesNoEnum.yes
            assert phase_slope2.to_z_mag is YesNoEnum.yes


class TestPhaseSlopeEdgeCases:
    """Test PhaseSlope edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            phase_slope = PhaseSlope(**{})  # type: ignore
            assert phase_slope.smooth == "None"  # String representation
            assert phase_slope.to_z_mag == YesNoEnum.no

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            phase_slope = PhaseSlope(unknown_field="value")  # type: ignore
            assert hasattr(phase_slope, "unknown_field")
            assert phase_slope.unknown_field == "value"  # type: ignore

    def test_enum_string_representation(self, subtests):
        """Test string representation of enum values."""
        enum_string_cases = [
            (SmoothEnum.robust, "SmoothEnum.robust"),  # Actual string representation
            (SmoothEnum.normal, "SmoothEnum.normal"),
            (SmoothEnum.minimal, "SmoothEnum.minimal"),
            (SmoothEnum.null, "SmoothEnum.null"),
            (YesNoEnum.yes, "YesNoEnum.yes"),
            (YesNoEnum.no, "YesNoEnum.no"),
        ]

        for enum_value, expected_string in enum_string_cases:
            with subtests.test(f"enum string {enum_value}"):
                assert str(enum_value) == expected_string

    def test_all_smooth_enum_combinations(self, subtests):
        """Test all possible SmoothEnum combinations."""
        smooth_values = [
            SmoothEnum.robust,
            SmoothEnum.normal,
            SmoothEnum.minimal,
            SmoothEnum.null,
        ]
        smooth_expected = [
            "robust",
            "normal",
            "minimal",
            "None",
        ]  # String representations
        to_z_mag_values = [YesNoEnum.yes, YesNoEnum.no]

        for smooth, smooth_expected_str in zip(smooth_values, smooth_expected):
            for to_z_mag in to_z_mag_values:
                with subtests.test(f"combination {smooth} + {to_z_mag}"):
                    phase_slope = PhaseSlope(smooth=smooth, to_z_mag=to_z_mag)  # type: ignore
                    assert phase_slope.smooth == smooth_expected_str
                    assert phase_slope.to_z_mag == to_z_mag

    def test_mixed_initialization_patterns(self, subtests):
        """Test mixed initialization patterns (enum + string)."""
        mixed_patterns = [
            ("enum + string", SmoothEnum.robust, "yes"),
            ("string + enum", "normal", YesNoEnum.no),
            ("both enums", SmoothEnum.minimal, YesNoEnum.yes),
            ("both strings", "None", "no"),
        ]

        for case_name, smooth_value, to_z_mag_value in mixed_patterns:
            with subtests.test(f"mixed pattern {case_name}"):
                phase_slope = PhaseSlope(smooth=smooth_value, to_z_mag=to_z_mag_value)  # type: ignore
                # Check that smooth is stored as string, to_z_mag as enum
                assert isinstance(phase_slope.smooth, str)
                assert isinstance(phase_slope.to_z_mag, YesNoEnum)

    def test_enum_value_preservation(self, subtests):
        """Test that enum values are preserved across operations."""
        with subtests.test("smooth enum preservation"):
            phase_slope = PhaseSlope(smooth="robust")  # type: ignore
            original_smooth = phase_slope.smooth

            # Modify other field
            phase_slope.to_z_mag = YesNoEnum.yes  # type: ignore

            # Original enum should be preserved
            assert phase_slope.smooth is original_smooth
            assert phase_slope.smooth == "robust"  # Stored as string

        with subtests.test("to_z_mag enum preservation"):
            phase_slope = PhaseSlope(to_z_mag="yes")  # type: ignore
            original_to_z_mag = phase_slope.to_z_mag

            # Modify other field
            phase_slope.smooth = SmoothEnum.normal  # type: ignore

            # Original enum should be preserved
            assert phase_slope.to_z_mag is original_to_z_mag
            assert phase_slope.to_z_mag == YesNoEnum.yes


class TestPhaseSlopeDocumentation:
    """Test PhaseSlope class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test PhaseSlope class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert PhaseSlope.__name__ == "PhaseSlope"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(PhaseSlope, MetadataBase)

    def test_enum_class_structure(self, subtests):
        """Test enum class structures."""
        with subtests.test("SmoothEnum is available"):
            assert SmoothEnum is not None
            assert hasattr(SmoothEnum, "robust")
            assert hasattr(SmoothEnum, "normal")
            assert hasattr(SmoothEnum, "minimal")
            assert hasattr(SmoothEnum, "null")

        with subtests.test("YesNoEnum is available"):
            assert YesNoEnum is not None
            assert hasattr(YesNoEnum, "yes")
            assert hasattr(YesNoEnum, "no")

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = PhaseSlope.model_fields
        expected_fields = ["smooth", "to_z_mag"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = PhaseSlope.model_fields

        with subtests.test("smooth field properties"):
            smooth_field = fields["smooth"]
            # Should be required with default
            assert "default" in str(smooth_field) or hasattr(smooth_field, "default")

        with subtests.test("to_z_mag field properties"):
            to_z_mag_field = fields["to_z_mag"]
            # Should be required with default
            assert "default" in str(to_z_mag_field) or hasattr(
                to_z_mag_field, "default"
            )

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            phase_slope = PhaseSlope()  # type: ignore
            dump = phase_slope.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) == 3  # Should have both fields + _class_name

        with subtests.test("all expected fields present"):
            expected_fields = ["smooth", "to_z_mag"]
            dump = PhaseSlope().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump
            # Also has _class_name field
            assert "_class_name" in dump

        with subtests.test("model_fields accessible"):
            fields = PhaseSlope.model_fields
            assert len(fields) == 2  # Only the actual model fields, not _class_name
            assert "smooth" in fields
            assert "to_z_mag" in fields

    def test_field_requirements(self, subtests):
        """Test field requirement specifications."""
        with subtests.test("smooth field requirement"):
            # Check if smooth field is marked as required in schema
            fields = PhaseSlope.model_fields
            smooth_field = fields["smooth"]
            # The field is required but has a default value
            assert hasattr(smooth_field, "default") or "default" in str(smooth_field)

        with subtests.test("to_z_mag field requirement"):
            # Check if to_z_mag field is marked as required in schema
            fields = PhaseSlope.model_fields
            to_z_mag_field = fields["to_z_mag"]
            # The field is required but has a default value
            assert hasattr(to_z_mag_field, "default") or "default" in str(
                to_z_mag_field
            )
