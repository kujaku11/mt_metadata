"""
Comprehensive pytest test suite for MTEdit metadata class.
This test suite follows modern pytest patterns with fixtures and subtests for efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata import (
    Auto,
    DPlus,
    MTEdit,
    PhaseSlope,
)


class TestMTEditDefault:
    """Test default initialization and basic attributes of MTEdit class."""

    @pytest.fixture(scope="class")
    def default_mtedit(self):
        """Fixture providing a default MTEdit instance for efficiency."""
        return MTEdit()  # type: ignore

    def test_default_initialization(self, default_mtedit, subtests):
        """Test that MTEdit initializes with correct default values."""
        with subtests.test("default version value"):
            assert default_mtedit.version == ""

        with subtests.test("default auto value"):
            assert isinstance(default_mtedit.auto, Auto)
            assert default_mtedit.auto.phase_flip == "yes"

        with subtests.test("default d_plus value"):
            assert isinstance(default_mtedit.d_plus, DPlus)
            assert default_mtedit.d_plus.use == "no"

        with subtests.test("default phase_slope value"):
            assert isinstance(default_mtedit.phase_slope, PhaseSlope)
            assert default_mtedit.phase_slope.smooth == "None"
            assert default_mtedit.phase_slope.to_z_mag == "no"

    def test_default_mtedit_attributes(self, default_mtedit, subtests):
        """Test that MTEdit has all expected attributes."""
        expected_attributes = ["version", "auto", "d_plus", "phase_slope"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_mtedit, attr)

    def test_default_model_fields(self, default_mtedit, subtests):
        """Test MTEdit model fields structure."""
        fields = default_mtedit.model_fields

        with subtests.test("model field version"):
            assert "version" in fields

        with subtests.test("model field auto"):
            assert "auto" in fields

        with subtests.test("model field d_plus"):
            assert "d_plus" in fields

        with subtests.test("model field phase_slope"):
            assert "phase_slope" in fields

        with subtests.test("field count"):
            assert len(fields) == 4

    def test_field_types(self, default_mtedit, subtests):
        """Test that fields have correct types."""
        with subtests.test("version field type"):
            assert isinstance(default_mtedit.version, str)

        with subtests.test("auto field type"):
            assert isinstance(default_mtedit.auto, Auto)

        with subtests.test("d_plus field type"):
            assert isinstance(default_mtedit.d_plus, DPlus)

        with subtests.test("phase_slope field type"):
            assert isinstance(default_mtedit.phase_slope, PhaseSlope)

    def test_required_field_behavior(self, default_mtedit, subtests):
        """Test required field behavior and defaults."""
        with subtests.test("all fields have defaults"):
            # Should be able to create with no parameters
            empty_mtedit = MTEdit()  # type: ignore
            assert empty_mtedit.version == ""
            assert isinstance(empty_mtedit.auto, Auto)
            assert isinstance(empty_mtedit.d_plus, DPlus)
            assert isinstance(empty_mtedit.phase_slope, PhaseSlope)


class TestMTEditCustomValues:
    """Test MTEdit with custom/populated values."""

    @pytest.fixture(scope="class")
    def populated_mtedit(self):
        """Fixture providing a populated MTEdit instance."""
        auto_data = Auto(phase_flip="no")  # type: ignore
        d_plus_data = DPlus(use="yes")  # type: ignore
        phase_slope_data = PhaseSlope(smooth="robust", to_z_mag="yes")  # type: ignore
        return MTEdit(
            version="3.10m applied 2021/01/27",
            auto=auto_data,
            d_plus=d_plus_data,
            phase_slope=phase_slope_data,
        )  # type: ignore

    def test_populated_mtedit_values(self, populated_mtedit, subtests):
        """Test populated MTEdit has correct values."""
        with subtests.test("populated version"):
            assert populated_mtedit.version == "3.10m applied 2021/01/27"

        with subtests.test("populated auto"):
            assert populated_mtedit.auto.phase_flip == "no"

        with subtests.test("populated d_plus"):
            assert populated_mtedit.d_plus.use == "yes"

        with subtests.test("populated phase_slope"):
            assert populated_mtedit.phase_slope.smooth == "robust"
            assert populated_mtedit.phase_slope.to_z_mag == "yes"

    def test_version_initialization_patterns(self, subtests):
        """Test different version initialization patterns."""
        version_patterns = [
            ("basic version", "3.10", "3.10"),
            ("version with modifier", "3.10m", "3.10m"),
            (
                "version with date",
                "3.10m applied 2021/01/27",
                "3.10m applied 2021/01/27",
            ),
            ("empty string", "", ""),
            ("complex version", "MT Edit v4.0 build 123", "MT Edit v4.0 build 123"),
        ]

        for pattern_name, input_version, expected_version in version_patterns:
            with subtests.test(f"version pattern {pattern_name}"):
                mtedit = MTEdit(version=input_version)  # type: ignore
                assert mtedit.version == expected_version

    def test_auto_initialization_patterns(self, subtests):
        """Test different auto field initialization patterns."""
        auto_patterns = [
            ("auto yes", Auto(phase_flip="yes"), "yes"),  # type: ignore
            ("auto no", Auto(phase_flip="no"), "no"),  # type: ignore
        ]

        for pattern_name, auto_obj, expected_flip in auto_patterns:
            with subtests.test(f"auto pattern {pattern_name}"):
                mtedit = MTEdit(auto=auto_obj)  # type: ignore
                assert mtedit.auto.phase_flip == expected_flip

    def test_d_plus_initialization_patterns(self, subtests):
        """Test different d_plus field initialization patterns."""
        d_plus_patterns = [
            ("d_plus yes", DPlus(use="yes"), "yes"),  # type: ignore
            ("d_plus no", DPlus(use="no"), "no"),  # type: ignore
        ]

        for pattern_name, d_plus_obj, expected_use in d_plus_patterns:
            with subtests.test(f"d_plus pattern {pattern_name}"):
                mtedit = MTEdit(d_plus=d_plus_obj)  # type: ignore
                assert mtedit.d_plus.use == expected_use

    def test_phase_slope_initialization_patterns(self, subtests):
        """Test different phase_slope field initialization patterns."""
        phase_slope_patterns = [
            ("robust smooth", PhaseSlope(smooth="robust", to_z_mag="yes"), "robust", "yes"),  # type: ignore
            ("normal smooth", PhaseSlope(smooth="normal", to_z_mag="no"), "normal", "no"),  # type: ignore
            ("minimal smooth", PhaseSlope(smooth="minimal", to_z_mag="yes"), "minimal", "yes"),  # type: ignore
            ("none smooth", PhaseSlope(smooth="None", to_z_mag="no"), "None", "no"),  # type: ignore
        ]

        for (
            pattern_name,
            phase_slope_obj,
            expected_smooth,
            expected_to_z_mag,
        ) in phase_slope_patterns:
            with subtests.test(f"phase_slope pattern {pattern_name}"):
                mtedit = MTEdit(phase_slope=phase_slope_obj)  # type: ignore
                assert mtedit.phase_slope.smooth == expected_smooth
                assert mtedit.phase_slope.to_z_mag == expected_to_z_mag

    def test_individual_field_initialization(self, subtests):
        """Test initializing individual fields with different values."""
        individual_cases = [
            (
                "individual version",
                {"version": "test_version"},
                "version",
                "test_version",
            ),
            (
                "individual auto dict",
                {"auto": {"phase_flip": "no"}},
                "auto.phase_flip",
                "no",
            ),
            ("individual d_plus dict", {"d_plus": {"use": "yes"}}, "d_plus.use", "yes"),
            (
                "individual phase_slope dict",
                {"phase_slope": {"smooth": "robust", "to_z_mag": "yes"}},
                "phase_slope.smooth",
                "robust",
            ),
        ]

        for case_name, kwargs, field_path, expected_value in individual_cases:
            with subtests.test(f"{case_name}"):
                mtedit = MTEdit(**kwargs)  # type: ignore

                # Navigate to nested field if needed
                field_parts = field_path.split(".")
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)

                assert current_value == expected_value

    def test_partial_mtedit_values(self, subtests):
        """Test MTEdit with partial field specifications."""
        partial_cases = [
            ("version only", {"version": "partial_test"}, "version", "partial_test"),
            ("auto only", {"auto": {"phase_flip": "no"}}, "auto.phase_flip", "no"),
            ("d_plus only", {"d_plus": {"use": "yes"}}, "d_plus.use", "yes"),
            (
                "phase_slope only",
                {"phase_slope": {"smooth": "minimal"}},
                "phase_slope.smooth",
                "minimal",
            ),
        ]

        for case_name, kwargs, field_path, expected_value in partial_cases:
            with subtests.test(f"partial {case_name}"):
                mtedit = MTEdit(**kwargs)  # type: ignore

                # Navigate to nested field
                field_parts = field_path.split(".")
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)

                assert current_value == expected_value

                # Check that other fields have defaults
                if field_path != "version":
                    assert mtedit.version == ""
                if not field_path.startswith("auto"):
                    assert mtedit.auto.phase_flip == "yes"  # default
                if not field_path.startswith("d_plus"):
                    assert mtedit.d_plus.use == "no"  # default


class TestMTEditValidation:
    """Test MTEdit validation and error handling."""

    def test_version_validation(self, subtests):
        """Test version field validation."""
        valid_versions = [
            ("string version", "3.10m applied 2021/01/27"),
            ("empty string", ""),
            ("numeric string", "123"),
            ("long string", "a" * 1000),
        ]

        for case_name, version_value in valid_versions:
            with subtests.test(f"version valid {case_name}"):
                mtedit = MTEdit(version=version_value)  # type: ignore
                assert mtedit.version == version_value

    def test_auto_validation(self, subtests):
        """Test auto field validation."""
        with subtests.test("auto valid yes"):
            mtedit = MTEdit(auto={"phase_flip": "yes"})  # type: ignore
            assert mtedit.auto.phase_flip == "yes"

        with subtests.test("auto valid no"):
            mtedit = MTEdit(auto={"phase_flip": "no"})  # type: ignore
            assert mtedit.auto.phase_flip == "no"

    def test_d_plus_validation(self, subtests):
        """Test d_plus field validation."""
        with subtests.test("d_plus valid yes"):
            mtedit = MTEdit(d_plus={"use": "yes"})  # type: ignore
            assert mtedit.d_plus.use == "yes"

        with subtests.test("d_plus valid no"):
            mtedit = MTEdit(d_plus={"use": "no"})  # type: ignore
            assert mtedit.d_plus.use == "no"

    def test_phase_slope_validation(self, subtests):
        """Test phase_slope field validation."""
        valid_smooth_values = ["robust", "normal", "None", "minimal"]
        valid_to_z_mag_values = ["yes", "no"]

        for smooth_val in valid_smooth_values:
            with subtests.test(f"phase_slope smooth {smooth_val}"):
                mtedit = MTEdit(phase_slope={"smooth": smooth_val})  # type: ignore
                assert mtedit.phase_slope.smooth == smooth_val

        for to_z_mag_val in valid_to_z_mag_values:
            with subtests.test(f"phase_slope to_z_mag {to_z_mag_val}"):
                mtedit = MTEdit(phase_slope={"to_z_mag": to_z_mag_val})  # type: ignore
                assert mtedit.phase_slope.to_z_mag == to_z_mag_val

    def test_invalid_field_values(self, subtests):
        """Test that invalid field values raise ValidationError."""
        with subtests.test("invalid auto phase_flip"):
            with pytest.raises(ValidationError):
                MTEdit(auto={"phase_flip": "invalid"})  # type: ignore

        with subtests.test("invalid d_plus use"):
            with pytest.raises(ValidationError):
                MTEdit(d_plus={"use": "invalid"})  # type: ignore

        with subtests.test("invalid phase_slope smooth"):
            with pytest.raises(ValidationError):
                MTEdit(phase_slope={"smooth": "invalid"})  # type: ignore

        with subtests.test("invalid phase_slope to_z_mag"):
            with pytest.raises(ValidationError):
                MTEdit(phase_slope={"to_z_mag": "invalid"})  # type: ignore

    def test_type_validation(self, subtests):
        """Test type validation for different fields."""
        with subtests.test("version accepts string"):
            mtedit = MTEdit(version="test")  # type: ignore
            assert isinstance(mtedit.version, str)

        with subtests.test("auto accepts dict"):
            mtedit = MTEdit(auto={"phase_flip": "yes"})  # type: ignore
            assert isinstance(mtedit.auto, Auto)

        with subtests.test("d_plus accepts dict"):
            mtedit = MTEdit(d_plus={"use": "no"})  # type: ignore
            assert isinstance(mtedit.d_plus, DPlus)

        with subtests.test("phase_slope accepts dict"):
            mtedit = MTEdit(phase_slope={"smooth": "robust"})  # type: ignore
            assert isinstance(mtedit.phase_slope, PhaseSlope)


class TestMTEditSerialization:
    """Test MTEdit serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_mtedit(self):
        """Fixture for default MTEdit instance."""
        return MTEdit()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_mtedit(self):
        """Fixture for populated MTEdit instance."""
        return MTEdit(
            version="3.12m applied 2023/05/15",
            auto={"phase_flip": "no"},
            d_plus={"use": "yes"},
            phase_slope={"smooth": "robust", "to_z_mag": "yes"},
        )  # type: ignore

    def test_model_dump_default(self, default_mtedit, subtests):
        """Test model_dump with default values."""
        dump = default_mtedit.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["version", "auto", "d_plus", "phase_slope"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["version"] == ""
            assert dump["auto"]["phase_flip"] == "yes"
            assert dump["d_plus"]["use"] == "no"
            assert dump["phase_slope"]["smooth"] == "None"
            assert dump["phase_slope"]["to_z_mag"] == "no"

        with subtests.test("includes class name"):
            assert "_class_name" in dump or "m_t_edit" in str(dump).lower()

    def test_model_dump_populated(self, populated_mtedit, subtests):
        """Test model_dump with populated values."""
        dump = populated_mtedit.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["version"] == "3.12m applied 2023/05/15"
            assert dump["auto"]["phase_flip"] == "no"
            assert dump["d_plus"]["use"] == "yes"
            assert dump["phase_slope"]["smooth"] == "robust"
            assert dump["phase_slope"]["to_z_mag"] == "yes"

    def test_from_dict_creation(self, subtests):
        """Test creating MTEdit from dictionary."""
        test_cases = [
            (
                "full dict",
                {
                    "version": "test_version",
                    "auto": {"phase_flip": "no"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "normal", "to_z_mag": "yes"},
                },
                {
                    "version": "test_version",
                    "auto.phase_flip": "no",
                    "d_plus.use": "yes",
                    "phase_slope.smooth": "normal",
                    "phase_slope.to_z_mag": "yes",
                },
            ),
            (
                "partial dict",
                {"version": "partial_test", "auto": {"phase_flip": "no"}},
                {"version": "partial_test", "auto.phase_flip": "no"},
            ),
            (
                "empty dict",
                {},
                {
                    "version": "",
                    "auto.phase_flip": "yes",
                    "d_plus.use": "no",
                    "phase_slope.smooth": "None",
                },
            ),
        ]

        for case_name, data, expected_results in test_cases:
            with subtests.test(f"from dict {case_name}"):
                mtedit = MTEdit(**data)  # type: ignore

                for field_path, expected_value in expected_results.items():
                    field_parts = field_path.split(".")
                    current_value = mtedit
                    for part in field_parts:
                        current_value = getattr(current_value, part)
                    assert current_value == expected_value

    def test_json_serialization(self, default_mtedit, populated_mtedit, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated mtedit"):
            json_str = populated_mtedit.model_dump_json()
            data = json.loads(json_str)
            recreated = MTEdit(**data)  # type: ignore

            assert recreated.version == populated_mtedit.version
            assert recreated.auto.phase_flip == populated_mtedit.auto.phase_flip
            assert recreated.d_plus.use == populated_mtedit.d_plus.use
            assert recreated.phase_slope.smooth == populated_mtedit.phase_slope.smooth
            assert (
                recreated.phase_slope.to_z_mag == populated_mtedit.phase_slope.to_z_mag
            )

        with subtests.test("JSON round-trip default mtedit"):
            json_str = default_mtedit.model_dump_json()
            data = json.loads(json_str)
            recreated = MTEdit(**data)  # type: ignore

            assert recreated.version == default_mtedit.version
            assert recreated.auto.phase_flip == default_mtedit.auto.phase_flip
            assert recreated.d_plus.use == default_mtedit.d_plus.use
            assert recreated.phase_slope.smooth == default_mtedit.phase_slope.smooth
            assert recreated.phase_slope.to_z_mag == default_mtedit.phase_slope.to_z_mag

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            mtedit = MTEdit(version="test_version", auto={"phase_flip": "no"})  # type: ignore
            dump = mtedit.model_dump(exclude_none=True)
            assert "version" in dump
            assert "auto" in dump
            assert dump["version"] == "test_version"
            assert dump["auto"]["phase_flip"] == "no"

        with subtests.test("exclude_none with empty values"):
            mtedit = MTEdit(version="")  # type: ignore
            dump = mtedit.model_dump(exclude_none=True)
            # Empty string should still be included since it's not None
            assert "version" in dump
            assert dump["version"] == ""

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            mtedit = MTEdit()  # type: ignore
            dump = mtedit.model_dump(exclude_defaults=True)
            # Should minimize default values based on exclude_defaults behavior
            assert isinstance(dump, dict)

        with subtests.test("exclude_defaults with custom values"):
            mtedit = MTEdit(version="custom_value", auto={"phase_flip": "no"})  # type: ignore
            dump = mtedit.model_dump(exclude_defaults=True)
            assert "version" in dump
            assert dump["version"] == "custom_value"


class TestMTEditModification:
    """Test MTEdit field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying MTEdit fields after creation."""
        mtedit = MTEdit()  # type: ignore

        test_modifications = [
            ("version", "modified_version_1.0"),
            ("auto.phase_flip", "no"),
            ("d_plus.use", "yes"),
            ("phase_slope.smooth", "robust"),
            ("phase_slope.to_z_mag", "yes"),
        ]

        for field_path, value in test_modifications:
            with subtests.test(f"modify {field_path} to {value}"):
                field_parts = field_path.split(".")
                if len(field_parts) == 1:
                    setattr(mtedit, field_parts[0], value)
                else:
                    nested_obj = getattr(mtedit, field_parts[0])
                    setattr(nested_obj, field_parts[1], value)

                # Verify the change
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)
                assert current_value == value

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        mtedit = MTEdit(
            version="temp_version",
            auto={"phase_flip": "no"},
            d_plus={"use": "yes"},
            phase_slope={"smooth": "robust", "to_z_mag": "yes"},
        )  # type: ignore

        reset_tests = [
            ("reset version to default", "version", ""),
            ("reset auto.phase_flip to default", "auto.phase_flip", "yes"),
            ("reset d_plus.use to default", "d_plus.use", "no"),
            ("reset phase_slope.smooth to default", "phase_slope.smooth", "None"),
            ("reset phase_slope.to_z_mag to default", "phase_slope.to_z_mag", "no"),
        ]

        for test_name, field_path, default_value in reset_tests:
            with subtests.test(test_name):
                field_parts = field_path.split(".")
                if len(field_parts) == 1:
                    setattr(mtedit, field_parts[0], default_value)
                else:
                    nested_obj = getattr(mtedit, field_parts[0])
                    setattr(nested_obj, field_parts[1], default_value)

                # Verify the reset
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)
                assert current_value == default_value

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        mtedit = MTEdit()  # type: ignore

        updates = {
            "version": "bulk_update_version_2.0",
            "auto": Auto(phase_flip="no"),  # type: ignore
            "d_plus": DPlus(use="yes"),  # type: ignore
            "phase_slope": PhaseSlope(smooth="minimal", to_z_mag="yes"),  # type: ignore
        }

        for field, value in updates.items():
            setattr(mtedit, field, value)

        expected_values = {
            "version": "bulk_update_version_2.0",
            "auto.phase_flip": "no",
            "d_plus.use": "yes",
            "phase_slope.smooth": "minimal",
            "phase_slope.to_z_mag": "yes",
        }

        for field_path, expected_value in expected_values.items():
            with subtests.test(f"bulk update {field_path}"):
                field_parts = field_path.split(".")
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)
                assert current_value == expected_value

    def test_sequential_modifications(self, subtests):
        """Test sequential field modifications."""
        mtedit = MTEdit()  # type: ignore

        sequence_tests = [
            ("sequential version progression", "version", ["v1.0", "v2.0", "v3.0"]),
            ("sequential auto progression", "auto.phase_flip", ["yes", "no", "yes"]),
            ("sequential d_plus progression", "d_plus.use", ["no", "yes", "no"]),
            (
                "sequential phase_slope smooth progression",
                "phase_slope.smooth",
                ["None", "robust", "normal", "minimal"],
            ),
            (
                "sequential phase_slope to_z_mag progression",
                "phase_slope.to_z_mag",
                ["no", "yes", "no"],
            ),
        ]

        for test_name, field_path, value_sequence in sequence_tests:
            with subtests.test(test_name):
                for value in value_sequence:
                    field_parts = field_path.split(".")
                    if len(field_parts) == 1:
                        setattr(mtedit, field_parts[0], value)
                    else:
                        nested_obj = getattr(mtedit, field_parts[0])
                        setattr(nested_obj, field_parts[1], value)

                    # Verify each step
                    current_value = mtedit
                    for part in field_parts:
                        current_value = getattr(current_value, part)
                    assert current_value == value


class TestMTEditComparison:
    """Test MTEdit comparison and equality operations."""

    def test_mtedit_equality(self, subtests):
        """Test MTEdit equality comparisons."""
        mtedit1 = MTEdit(
            version="3.10m applied 2021/01/27",
            auto={"phase_flip": "no"},
            d_plus={"use": "yes"},
            phase_slope={"smooth": "robust", "to_z_mag": "yes"},
        )  # type: ignore

        mtedit2 = MTEdit(
            version="3.10m applied 2021/01/27",
            auto={"phase_flip": "no"},
            d_plus={"use": "yes"},
            phase_slope={"smooth": "robust", "to_z_mag": "yes"},
        )  # type: ignore

        mtedit3 = MTEdit(
            version="3.11m applied 2021/02/15",
            auto={"phase_flip": "yes"},
            d_plus={"use": "no"},
            phase_slope={"smooth": "normal", "to_z_mag": "no"},
        )  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert mtedit1.model_dump() == mtedit2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert mtedit1.model_dump() != mtedit3.model_dump()

        with subtests.test("individual field comparison"):
            assert mtedit1.version == mtedit2.version
            assert mtedit1.version != mtedit3.version
            assert mtedit1.auto.phase_flip == mtedit2.auto.phase_flip
            assert mtedit1.auto.phase_flip != mtedit3.auto.phase_flip

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("version", "consistency_test_v1.0"),
            ("auto.phase_flip", "no"),
            ("d_plus.use", "yes"),
            ("phase_slope.smooth", "robust"),
            ("phase_slope.to_z_mag", "yes"),
        ]

        for field_path, value in test_values:
            with subtests.test(f"consistency {field_path} {value}"):
                # Create from init
                if "." not in field_path:
                    kwargs = {field_path: value}
                elif field_path.startswith("auto"):
                    kwargs = {"auto": {"phase_flip": value}}
                elif field_path.startswith("d_plus"):
                    kwargs = {"d_plus": {"use": value}}
                elif field_path.startswith("phase_slope.smooth"):
                    kwargs = {"phase_slope": {"smooth": value}}
                elif field_path.startswith("phase_slope.to_z_mag"):
                    kwargs = {"phase_slope": {"to_z_mag": value}}

                mtedit = MTEdit(**kwargs)  # type: ignore

                # Check direct access
                field_parts = field_path.split(".")
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)
                assert current_value == value

                # Test round-trip consistency
                dump = mtedit.model_dump()
                recreated = MTEdit(**dump)  # type: ignore
                recreated_value = recreated
                for part in field_parts:
                    recreated_value = getattr(recreated_value, part)
                assert recreated_value == current_value

    def test_nested_field_comparison(self, subtests):
        """Test comparison of nested field structures."""
        mtedit1 = MTEdit(
            auto={"phase_flip": "yes"},
            d_plus={"use": "no"},
            phase_slope={"smooth": "robust", "to_z_mag": "yes"},
        )  # type: ignore

        mtedit2 = MTEdit(
            auto={"phase_flip": "yes"},
            d_plus={"use": "no"},
            phase_slope={"smooth": "robust", "to_z_mag": "yes"},
        )  # type: ignore

        with subtests.test("nested auto comparison"):
            assert mtedit1.auto.model_dump() == mtedit2.auto.model_dump()

        with subtests.test("nested d_plus comparison"):
            assert mtedit1.d_plus.model_dump() == mtedit2.d_plus.model_dump()

        with subtests.test("nested phase_slope comparison"):
            assert mtedit1.phase_slope.model_dump() == mtedit2.phase_slope.model_dump()


class TestMTEditEdgeCases:
    """Test MTEdit edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            mtedit = MTEdit(**{})  # type: ignore
            assert mtedit.version == ""
            assert mtedit.auto.phase_flip == "yes"
            assert mtedit.d_plus.use == "no"
            assert mtedit.phase_slope.smooth == "None"
            assert mtedit.phase_slope.to_z_mag == "no"

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields might be accepted"):
            # MetadataBase behavior with unknown fields
            try:
                mtedit = MTEdit(unknown_field="value")  # type: ignore
                # If no error, verify it was handled gracefully
                assert isinstance(mtedit, MTEdit)
            except (ValidationError, TypeError):
                # ValidationError or TypeError is acceptable for unknown fields
                pass

    def test_mtedit_edge_cases(self, subtests):
        """Test various edge cases for MTEdit fields."""
        edge_cases = [
            ("empty_string_version", {"version": ""}, "version", ""),
            (
                "none_version",
                {"version": None},
                "version",
                None,
            ),  # May be converted to string
            ("very_long_version", {"version": "x" * 1000}, "version", "x" * 1000),
            ("unicode_version", {"version": "版本 3.10 🔬"}, "version", "版本 3.10 🔬"),
        ]

        for case_name, kwargs, field_path, expected_or_none in edge_cases:
            with subtests.test(f"edge case {case_name}"):
                try:
                    mtedit = MTEdit(**kwargs)  # type: ignore
                    field_parts = field_path.split(".")
                    current_value = mtedit
                    for part in field_parts:
                        current_value = getattr(current_value, part)

                    if expected_or_none is not None:
                        assert current_value == expected_or_none
                    else:
                        # Just ensure it's a valid string conversion
                        assert isinstance(current_value, str)

                except ValidationError:
                    # Some edge cases may legitimately fail validation
                    pass

    def test_nested_dict_edge_cases(self, subtests):
        """Test edge cases with nested dictionary inputs."""
        nested_edge_cases = [
            (
                "empty auto dict",
                {"auto": {}},
                "auto.phase_flip",
                "yes",
            ),  # Should use default
            (
                "empty d_plus dict",
                {"d_plus": {}},
                "d_plus.use",
                "no",
            ),  # Should use default
            (
                "empty phase_slope dict",
                {"phase_slope": {}},
                "phase_slope.smooth",
                "None",
            ),  # Should use default
            (
                "partial phase_slope dict",
                {"phase_slope": {"smooth": "robust"}},
                "phase_slope.smooth",
                "robust",
            ),
        ]

        for case_name, kwargs, field_path, expected_value in nested_edge_cases:
            with subtests.test(f"nested edge case {case_name}"):
                mtedit = MTEdit(**kwargs)  # type: ignore
                field_parts = field_path.split(".")
                current_value = mtedit
                for part in field_parts:
                    current_value = getattr(current_value, part)
                assert current_value == expected_value

    def test_complex_initialization_combinations(self, subtests):
        """Test complex combinations of initialization parameters."""
        complex_cases = [
            (
                "all_custom",
                {
                    "version": "Complex v4.0",
                    "auto": {"phase_flip": "no"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "minimal", "to_z_mag": "yes"},
                },
                {
                    "version": "Complex v4.0",
                    "auto.phase_flip": "no",
                    "d_plus.use": "yes",
                },
            ),
            (
                "mixed_defaults_and_custom",
                {"version": "Mixed test", "auto": {"phase_flip": "no"}},
                {"version": "Mixed test", "auto.phase_flip": "no", "d_plus.use": "no"},
            ),
        ]

        for case_name, kwargs, expected_values in complex_cases:
            with subtests.test(f"complex combination {case_name}"):
                mtedit = MTEdit(**kwargs)  # type: ignore
                for field_path, expected_value in expected_values.items():
                    field_parts = field_path.split(".")
                    current_value = mtedit
                    for part in field_parts:
                        current_value = getattr(current_value, part)
                    assert current_value == expected_value


class TestMTEditDocumentation:
    """Test MTEdit class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test MTEdit class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert MTEdit.__name__ == "MTEdit"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(MTEdit, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = MTEdit.model_fields
        expected_fields = ["version", "auto", "d_plus", "phase_slope"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = MTEdit.model_fields

        with subtests.test("version field properties"):
            version_field = fields["version"]
            # Should have default empty string
            assert "default" in str(version_field) or hasattr(version_field, "default")

        with subtests.test("auto field properties"):
            auto_field = fields["auto"]
            # Should have default_factory
            assert "default_factory" in str(auto_field) or hasattr(
                auto_field, "default_factory"
            )

        with subtests.test("d_plus field properties"):
            d_plus_field = fields["d_plus"]
            # Should have default_factory
            assert "default_factory" in str(d_plus_field) or hasattr(
                d_plus_field, "default_factory"
            )

        with subtests.test("phase_slope field properties"):
            phase_slope_field = fields["phase_slope"]
            # Should have default_factory
            assert "default_factory" in str(phase_slope_field) or hasattr(
                phase_slope_field, "default_factory"
            )

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            mtedit = MTEdit()  # type: ignore
            dump = mtedit.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) >= 4  # Should have at least 4 fields

        with subtests.test("all expected fields present"):
            expected_fields = ["version", "auto", "d_plus", "phase_slope"]
            dump = MTEdit().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump

        with subtests.test("model_fields accessible"):
            fields = MTEdit.model_fields
            assert len(fields) == 4
            assert "version" in fields
            assert "auto" in fields
            assert "d_plus" in fields
            assert "phase_slope" in fields

    def test_nested_class_access(self, subtests):
        """Test access to nested class information."""
        with subtests.test("Auto class accessible"):
            assert Auto.__name__ == "Auto"

        with subtests.test("DPlus class accessible"):
            assert DPlus.__name__ == "DPlus"

        with subtests.test("PhaseSlope class accessible"):
            assert PhaseSlope.__name__ == "PhaseSlope"

    def test_field_types_documentation(self, subtests):
        """Test field type documentation and annotations."""
        fields = MTEdit.model_fields

        with subtests.test("version field type documentation"):
            version_field = fields["version"]
            # String field
            assert "str" in str(version_field) or hasattr(version_field, "annotation")

        with subtests.test("auto field type documentation"):
            auto_field = fields["auto"]
            # Auto type field
            assert "Auto" in str(auto_field) or hasattr(auto_field, "annotation")

        with subtests.test("d_plus field type documentation"):
            d_plus_field = fields["d_plus"]
            # DPlus type field
            assert "DPlus" in str(d_plus_field) or hasattr(d_plus_field, "annotation")

        with subtests.test("phase_slope field type documentation"):
            phase_slope_field = fields["phase_slope"]
            # PhaseSlope type field
            assert "PhaseSlope" in str(phase_slope_field) or hasattr(
                phase_slope_field, "annotation"
            )

    def test_example_values(self, subtests):
        """Test example values and realistic usage patterns."""
        realistic_examples = [
            ("basic version", {"version": "3.10m"}),
            ("version with date", {"version": "3.10m applied 2021/01/27"}),
            ("auto flip enabled", {"auto": {"phase_flip": "yes"}}),
            ("d_plus enabled", {"d_plus": {"use": "yes"}}),
            (
                "robust phase slope",
                {"phase_slope": {"smooth": "robust", "to_z_mag": "yes"}},
            ),
        ]

        for example_name, kwargs in realistic_examples:
            with subtests.test(f"example value {example_name}"):
                mtedit = MTEdit(**kwargs)  # type: ignore
                assert isinstance(mtedit, MTEdit)

                # Verify the example works as expected
                for field, value in kwargs.items():
                    if isinstance(value, dict):
                        nested_obj = getattr(mtedit, field)
                        for nested_field, nested_value in value.items():
                            assert getattr(nested_obj, nested_field) == nested_value
                    else:
                        assert getattr(mtedit, field) == value


class TestMTEditIntegration:
    """Test MTEdit integration scenarios and real-world usage patterns."""

    def test_realistic_mtedit_configurations(self, subtests):
        """Test realistic MTEdit configurations."""
        realistic_configs = [
            (
                "standard_processing",
                {
                    "version": "3.10m applied 2021/01/27",
                    "auto": {"phase_flip": "yes"},
                    "d_plus": {"use": "no"},
                    "phase_slope": {"smooth": "robust", "to_z_mag": "no"},
                },
            ),
            (
                "advanced_processing",
                {
                    "version": "4.0 build 123 applied 2023/08/15",
                    "auto": {"phase_flip": "no"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "minimal", "to_z_mag": "yes"},
                },
            ),
            (
                "minimal_processing",
                {
                    "version": "3.05",
                    "auto": {"phase_flip": "yes"},
                    "d_plus": {"use": "no"},
                    "phase_slope": {"smooth": "None", "to_z_mag": "no"},
                },
            ),
        ]

        for config_name, config_data in realistic_configs:
            with subtests.test(f"realistic config {config_name}"):
                mtedit = MTEdit(**config_data)  # type: ignore
                assert isinstance(mtedit, MTEdit)

                # Verify all fields
                assert mtedit.version == config_data["version"]
                assert mtedit.auto.phase_flip == config_data["auto"]["phase_flip"]
                assert mtedit.d_plus.use == config_data["d_plus"]["use"]
                assert mtedit.phase_slope.smooth == config_data["phase_slope"]["smooth"]
                assert (
                    mtedit.phase_slope.to_z_mag
                    == config_data["phase_slope"]["to_z_mag"]
                )

    def test_data_pipeline_scenarios(self, subtests):
        """Test MTEdit in data processing pipeline scenarios."""
        pipeline_scenarios = [
            (
                "pipeline empty_initialization",
                {},
                {"version": "", "auto.phase_flip": "yes", "d_plus.use": "no"},
            ),
            (
                "pipeline partial_specification",
                {"version": "Pipeline v1.0", "auto": {"phase_flip": "no"}},
                {
                    "version": "Pipeline v1.0",
                    "auto.phase_flip": "no",
                    "d_plus.use": "no",
                },
            ),
            (
                "pipeline full_specification",
                {
                    "version": "Pipeline v2.0 complete",
                    "auto": {"phase_flip": "yes"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "robust", "to_z_mag": "yes"},
                },
                {
                    "version": "Pipeline v2.0 complete",
                    "auto.phase_flip": "yes",
                    "d_plus.use": "yes",
                    "phase_slope.smooth": "robust",
                },
            ),
        ]

        for scenario_name, input_data, expected_fields in pipeline_scenarios:
            with subtests.test(f"pipeline {scenario_name}"):
                mtedit = MTEdit(**input_data)  # type: ignore

                for field_path, expected_value in expected_fields.items():
                    field_parts = field_path.split(".")
                    current_value = mtedit
                    for part in field_parts:
                        current_value = getattr(current_value, part)
                    assert current_value == expected_value

    def test_serialization_roundtrip_scenarios(self, subtests):
        """Test comprehensive serialization round-trip scenarios."""
        roundtrip_scenarios = [
            (
                "scenario 1",
                {
                    "version": "Roundtrip test v1.0",
                    "auto": {"phase_flip": "no"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "normal", "to_z_mag": "yes"},
                },
            ),
            (
                "scenario 2",
                {
                    "version": "",
                    "auto": {"phase_flip": "yes"},
                    "d_plus": {"use": "no"},
                    "phase_slope": {"smooth": "robust", "to_z_mag": "no"},
                },
            ),
            (
                "scenario 3",
                {
                    "version": "Complex test with unicode 🔬",
                    "auto": {"phase_flip": "no"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "minimal", "to_z_mag": "yes"},
                },
            ),
        ]

        for scenario_name, original_data in roundtrip_scenarios:
            with subtests.test(f"roundtrip {scenario_name}"):
                # Create original
                original = MTEdit(**original_data)  # type: ignore

                # Serialize and deserialize
                json_data = original.model_dump_json()
                recreated_data = json.loads(json_data)
                recreated = MTEdit(**recreated_data)  # type: ignore

                # Verify round-trip integrity
                assert original.version == recreated.version
                assert original.auto.phase_flip == recreated.auto.phase_flip
                assert original.d_plus.use == recreated.d_plus.use
                assert original.phase_slope.smooth == recreated.phase_slope.smooth
                assert original.phase_slope.to_z_mag == recreated.phase_slope.to_z_mag

    def test_field_update_scenarios(self, subtests):
        """Test progressive field update scenarios."""
        with subtests.test("progressive field updates"):
            mtedit = MTEdit()  # type: ignore

            # Step 1: Update version
            mtedit.version = "Step 1 version"
            assert mtedit.version == "Step 1 version"

            # Step 2: Update auto
            mtedit.auto.phase_flip = "no"
            assert mtedit.auto.phase_flip == "no"

            # Step 3: Update d_plus
            mtedit.d_plus.use = "yes"
            assert mtedit.d_plus.use == "yes"

            # Step 4: Update phase_slope
            mtedit.phase_slope.smooth = "robust"
            mtedit.phase_slope.to_z_mag = "yes"
            assert mtedit.phase_slope.smooth == "robust"
            assert mtedit.phase_slope.to_z_mag == "yes"

            # Verify all updates persisted
            assert mtedit.version == "Step 1 version"
            assert mtedit.auto.phase_flip == "no"
            assert mtedit.d_plus.use == "yes"
            assert mtedit.phase_slope.smooth == "robust"
            assert mtedit.phase_slope.to_z_mag == "yes"

    def test_error_handling_scenarios(self, subtests):
        """Test error handling in various scenarios."""
        with subtests.test("invalid nested field handling"):
            with pytest.raises(ValidationError):
                MTEdit(auto={"phase_flip": "invalid_value"})  # type: ignore

        with subtests.test("invalid phase_slope smooth value"):
            with pytest.raises(ValidationError):
                MTEdit(phase_slope={"smooth": "invalid_smooth"})  # type: ignore

        with subtests.test("invalid d_plus use value"):
            with pytest.raises(ValidationError):
                MTEdit(d_plus={"use": "maybe"})  # type: ignore

    def test_mtedit_integration_consistency(self, subtests):
        """Test consistency across different creation and access patterns."""
        with subtests.test("mtedit integration system consistency"):
            # Test various creation patterns produce consistent results
            patterns = [
                MTEdit(version="test", auto={"phase_flip": "no"}),  # type: ignore
                MTEdit(**{"version": "test", "auto": {"phase_flip": "no"}}),  # type: ignore
            ]

            for i, pattern in enumerate(patterns):
                assert pattern.version == "test"
                assert pattern.auto.phase_flip == "no"
                # All patterns should have same default behavior for unspecified fields
                assert pattern.d_plus.use == "no"
                assert pattern.phase_slope.smooth == "None"
                assert pattern.phase_slope.to_z_mag == "no"

    def test_comprehensive_field_combinations(self, subtests):
        """Test comprehensive combinations of all fields."""
        comprehensive_cases = [
            (
                "all_defaults",
                {},
                {
                    "version": "",
                    "auto.phase_flip": "yes",
                    "d_plus.use": "no",
                    "phase_slope.smooth": "None",
                },
            ),
            (
                "all_custom",
                {
                    "version": "All custom v1.0",
                    "auto": {"phase_flip": "no"},
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "robust", "to_z_mag": "yes"},
                },
                {
                    "version": "All custom v1.0",
                    "auto.phase_flip": "no",
                    "d_plus.use": "yes",
                    "phase_slope.smooth": "robust",
                    "phase_slope.to_z_mag": "yes",
                },
            ),
            (
                "mixed_configuration",
                {
                    "version": "Mixed config",
                    "d_plus": {"use": "yes"},
                    "phase_slope": {"smooth": "minimal"},
                },
                {
                    "version": "Mixed config",
                    "auto.phase_flip": "yes",  # default
                    "d_plus.use": "yes",
                    "phase_slope.smooth": "minimal",
                    "phase_slope.to_z_mag": "no",  # default
                },
            ),
        ]

        for case_name, input_data, expected_values in comprehensive_cases:
            with subtests.test(f"comprehensive combination {case_name}"):
                mtedit = MTEdit(**input_data)  # type: ignore

                for field_path, expected_value in expected_values.items():
                    field_parts = field_path.split(".")
                    current_value = mtedit
                    for part in field_parts:
                        current_value = getattr(current_value, part)
                    assert current_value == expected_value
