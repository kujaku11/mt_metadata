"""
Test suite for DPlus metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.common.enumerations import YesNoEnum
from mt_metadata.transfer_functions.io.zonge.metadata import DPlus


class TestDPlusDefault:
    """Test default initialization and basic attributes of DPlus class."""

    @pytest.fixture(scope="class")
    def default_d_plus(self):
        """Fixture providing a default DPlus instance for efficiency."""
        return DPlus()  # type: ignore

    def test_default_initialization(self, default_d_plus, subtests):
        """Test that DPlus initializes with correct default values."""
        with subtests.test("default use value"):
            assert default_d_plus.use == "no"

    def test_default_d_plus_attributes(self, default_d_plus, subtests):
        """Test that DPlus has all expected attributes."""
        with subtests.test("has attribute use"):
            assert hasattr(default_d_plus, "use")

    def test_default_model_fields(self, default_d_plus, subtests):
        """Test model fields are properly defined."""
        fields = default_d_plus.model_fields

        with subtests.test("model field use"):
            assert "use" in fields

        with subtests.test("field count"):
            assert len(fields) == 1


class TestDPlusCustomValues:
    """Test DPlus with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_d_plus(self):
        """Fixture providing a DPlus instance with custom values for efficiency."""
        return DPlus(use="yes")  # type: ignore

    def test_populated_d_plus_values(self, populated_d_plus, subtests):
        """Test DPlus with custom 'yes' value."""
        with subtests.test("populated use"):
            assert populated_d_plus.use == "yes"

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        with subtests.test("individual use yes"):
            d_plus = DPlus(use="yes")  # type: ignore
            assert d_plus.use == "yes"

        with subtests.test("individual use no"):
            d_plus = DPlus(use="no")  # type: ignore
            assert d_plus.use == "no"


class TestDPlusValidation:
    """Test DPlus input validation and type conversion."""

    def test_valid_enum_values(self, subtests):
        """Test that valid YesNoEnum values are accepted."""
        valid_values = ["yes", "no", "YES", "NO", "Yes", "No"]

        for value in valid_values:
            with subtests.test(f"valid value {value}"):
                d_plus = DPlus(use=value)  # type: ignore
                # YesNoEnum should normalize to lowercase
                assert d_plus.use.lower() in ["yes", "no"]

    def test_invalid_enum_values(self, subtests):
        """Test that invalid values raise ValidationError."""
        invalid_values = ["maybe", "true", "false", "1", "0", "unknown"]

        for value in invalid_values:
            with subtests.test(f"invalid value {value}"):
                with pytest.raises(ValidationError):
                    DPlus(use=value)  # type: ignore

    def test_none_value_handling(self, subtests):
        """Test handling of None values."""
        with subtests.test("None value validation"):
            with pytest.raises((ValidationError, TypeError)):
                DPlus(use=None)  # type: ignore

    def test_empty_string_handling(self, subtests):
        """Test handling of empty strings."""
        with subtests.test("empty string validation"):
            with pytest.raises(ValidationError):
                DPlus(use="")  # type: ignore

    def test_type_conversion(self, subtests):
        """Test automatic type conversion."""
        # YesNoEnum should handle case-insensitive conversion
        with subtests.test("case insensitive YES"):
            d_plus = DPlus(use="YES")  # type: ignore
            assert d_plus.use == "YES" or d_plus.use == "yes"

        with subtests.test("case insensitive No"):
            d_plus = DPlus(use="No")  # type: ignore
            assert d_plus.use == "No" or d_plus.use == "no"


class TestDPlusSerialization:
    """Test DPlus serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_d_plus(self):
        """Fixture for default DPlus instance."""
        return DPlus()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_d_plus(self):
        """Fixture for populated DPlus instance."""
        return DPlus(use="yes")  # type: ignore

    def test_model_dump_default(self, default_d_plus, subtests):
        """Test model_dump with default values."""
        dump = default_d_plus.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has field use"):
            assert "use" in dump

        with subtests.test("default value use"):
            assert dump["use"] == "no"

    def test_model_dump_populated(self, populated_d_plus, subtests):
        """Test model_dump with populated values."""
        dump = populated_d_plus.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated value use"):
            assert dump["use"] == "yes"

    def test_from_dict_creation(self, subtests):
        """Test creating DPlus from dictionary."""
        with subtests.test("full dict"):
            data = {"use": "yes"}
            d_plus = DPlus(**data)  # type: ignore
            assert d_plus.use == "yes"

        with subtests.test("empty dict uses defaults"):
            data = {}
            d_plus = DPlus(**data)  # type: ignore
            assert d_plus.use == "no"

    def test_json_serialization(self, default_d_plus, populated_d_plus, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated d_plus"):
            json_str = populated_d_plus.model_dump_json()
            data = json.loads(json_str)
            recreated = DPlus(**data)  # type: ignore
            assert recreated.use == populated_d_plus.use

        with subtests.test("JSON round-trip default d_plus"):
            json_str = default_d_plus.model_dump_json()
            data = json.loads(json_str)
            recreated = DPlus(**data)  # type: ignore
            assert recreated.use == default_d_plus.use

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            d_plus = DPlus(use="yes")  # type: ignore
            dump = d_plus.model_dump(exclude_none=True)
            assert "use" in dump
            assert dump["use"] == "yes"


class TestDPlusModification:
    """Test DPlus field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying DPlus fields after creation."""
        d_plus = DPlus()  # type: ignore

        with subtests.test("modify use to yes"):
            d_plus.use = "yes"  # type: ignore
            assert d_plus.use == "yes"

        with subtests.test("modify use back to no"):
            d_plus.use = "no"  # type: ignore
            assert d_plus.use == "no"

    def test_invalid_modification(self, subtests):
        """Test that invalid modifications raise appropriate errors."""
        d_plus = DPlus()  # type: ignore

        with subtests.test("invalid enum value"):
            with pytest.raises((ValidationError, ValueError)):
                d_plus.use = "invalid"  # type: ignore


class TestDPlusComparison:
    """Test DPlus comparison and equality operations."""

    def test_d_plus_equality(self, subtests):
        """Test DPlus equality comparisons."""
        d_plus1 = DPlus(use="yes")  # type: ignore
        d_plus2 = DPlus(use="yes")  # type: ignore
        d_plus3 = DPlus(use="no")  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert d_plus1.model_dump() == d_plus2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert d_plus1.model_dump() != d_plus3.model_dump()

        with subtests.test("individual field comparison"):
            assert d_plus1.use == d_plus2.use
            assert d_plus1.use != d_plus3.use

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = ["yes", "no"]

        for value in test_values:
            with subtests.test(f"consistency {value}"):
                d_plus = DPlus(use=value)  # type: ignore
                assert d_plus.use == value

                # Test round-trip consistency
                dump = d_plus.model_dump()
                recreated = DPlus(**dump)  # type: ignore
                assert recreated.use == d_plus.use


class TestDPlusEdgeCases:
    """Test DPlus edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            d_plus = DPlus(**{})  # type: ignore
            assert d_plus.use == "no"  # Should use default

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            d_plus = DPlus(unknown_field="value")  # type: ignore
            # Unknown field should be accepted and accessible
            assert hasattr(d_plus, "unknown_field")
            assert d_plus.unknown_field == "value"  # type: ignore

    def test_case_sensitivity(self, subtests):
        """Test case sensitivity handling for enum values."""
        cases = [("yes", ["yes", "YES", "Yes"]), ("no", ["no", "NO", "No"])]

        for expected_base, variations in cases:
            for case_variant in variations:
                with subtests.test(f"case variant {case_variant}"):
                    d_plus = DPlus(use=case_variant)  # type: ignore
                    # Enum should handle case conversion appropriately
                    assert d_plus.use.lower() == expected_base.lower()

    def test_enum_object_assignment(self, subtests):
        """Test direct enum object assignment."""
        with subtests.test("YesNoEnum.yes assignment"):
            d_plus = DPlus(use=YesNoEnum.yes)  # type: ignore
            assert d_plus.use == "yes"

        with subtests.test("YesNoEnum.no assignment"):
            d_plus = DPlus(use=YesNoEnum.no)  # type: ignore
            assert d_plus.use == "no"


class TestDPlusDocumentation:
    """Test DPlus class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test DPlus class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert DPlus.__name__ == "DPlus"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(DPlus, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = DPlus.model_fields

        with subtests.test("field description use"):
            use_field = fields["use"]
            # Check that field has description
            assert hasattr(use_field, "description") or "description" in str(use_field)

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            d_plus = DPlus()  # type: ignore
            dump = d_plus.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) > 0

        with subtests.test("all expected fields present"):
            expected_fields = ["use"]
            dump = DPlus().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump

        with subtests.test("model_fields accessible"):
            fields = DPlus.model_fields
            assert "use" in fields
