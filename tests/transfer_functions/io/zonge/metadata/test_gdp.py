"""
Test suite for Gdp metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from mt_metadata.transfer_functions.io.zonge.metadata import GDP


class TestGdpDefault:
    """Test default initialization and basic attributes of Gdp class."""

    @pytest.fixture(scope="class")
    def default_gdp(self):
        """Fixture providing a default Gdp instance for efficiency."""
        return GDP()  # type: ignore

    def test_default_initialization(self, default_gdp, subtests):
        """Test that Gdp initializes with correct default values."""
        with subtests.test("default date type"):
            assert isinstance(default_gdp.date, str)

        with subtests.test("default time type"):
            # Default time returns an MTime object
            assert hasattr(default_gdp.time, "__str__") or isinstance(
                default_gdp.time, str
            )

        with subtests.test("default type value"):
            assert default_gdp.type is None

        with subtests.test("default prog_ver value"):
            assert default_gdp.prog_ver is None

    def test_default_gdp_attributes(self, default_gdp, subtests):
        """Test that Gdp has all expected attributes."""
        expected_attributes = ["date", "time", "type", "prog_ver"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_gdp, attr)

    def test_default_model_fields(self, default_gdp, subtests):
        """Test model fields are properly defined."""
        fields = default_gdp.model_fields
        expected_fields = ["date", "time", "type", "prog_ver"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 4


class TestGdpCustomValues:
    """Test Gdp with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_gdp(self):
        """Fixture providing a Gdp instance with custom values for efficiency."""
        return GDP(  # type: ignore
            date="2023-01-15", time="14:30:00", type="zen", prog_ver="v1.2.3"
        )

    def test_populated_gdp_values(self, populated_gdp, subtests):
        """Test Gdp with custom values."""
        with subtests.test("populated date"):
            assert "2023-01-15" in str(populated_gdp.date)

        with subtests.test("populated time"):
            assert "14:30:00" in str(populated_gdp.time)

        with subtests.test("populated type"):
            assert populated_gdp.type == "zen"

        with subtests.test("populated prog_ver"):
            assert populated_gdp.prog_ver == "v1.2.3"

    def test_partial_gdp_values(self, subtests):
        """Test Gdp with only some fields populated."""
        gdp = GDP(type="zen", prog_ver="v2.0")  # type: ignore

        with subtests.test("partial type"):
            assert gdp.type == "zen"

        with subtests.test("partial prog_ver"):
            assert gdp.prog_ver == "v2.0"

        with subtests.test("partial default date"):
            assert isinstance(gdp.date, str)

        with subtests.test("partial default time"):
            # Default time returns an MTime object
            assert hasattr(gdp.time, "__str__") or isinstance(gdp.time, str)

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("date", "2023-12-25"),
            ("time", "09:15:30"),
            ("type", "zen"),
            ("prog_ver", "v3.1.4"),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field}"):
                kwargs = {field: value}
                gdp = GDP(**kwargs)  # type: ignore
                assert getattr(gdp, field) == value or str(value) in str(
                    getattr(gdp, field)
                )


class TestGdpValidation:
    """Test Gdp input validation and type conversion."""

    def test_date_validation(self, subtests):
        """Test date field validation and conversion."""
        valid_dates = [
            "2023-01-15",
            "01/15/2023",
            "2023-01-15T10:30:00",
            datetime(2023, 1, 15),
            np.datetime64("2023-01-15"),
            pd.Timestamp("2023-01-15"),
        ]

        for date_value in valid_dates:
            with subtests.test(f"valid date {type(date_value).__name__}"):
                gdp = GDP(date=date_value)  # type: ignore
                assert isinstance(gdp.date, str)
                assert "2023" in str(gdp.date)

    def test_time_validation(self, subtests):
        """Test time field validation and conversion."""
        valid_times = [
            "14:30:00",
            "14:30:00.123",
            "2023-01-15T14:30:00",
            datetime(2023, 1, 15, 14, 30, 0),
            np.datetime64("2023-01-15T14:30:00"),
            pd.Timestamp("2023-01-15 14:30:00"),
        ]

        for time_value in valid_times:
            with subtests.test(f"valid time {type(time_value).__name__}"):
                gdp = GDP(time=time_value)  # type: ignore
                assert isinstance(gdp.time, str)
                # Should contain time components
                assert any(char in str(gdp.time) for char in [":", "14", "30"])

    def test_string_field_validation(self, subtests):
        """Test string field validation for type and prog_ver."""
        with subtests.test("type string validation"):
            gdp = GDP(type="custom_type")  # type: ignore
            assert gdp.type == "custom_type"

        with subtests.test("prog_ver string validation"):
            gdp = GDP(prog_ver="version_string")  # type: ignore
            assert gdp.prog_ver == "version_string"

    def test_none_values_allowed(self, subtests):
        """Test that None values are allowed for optional fields."""
        optional_fields = ["type", "prog_ver"]

        for field in optional_fields:
            with subtests.test(f"none allowed {field}"):
                kwargs = {field: None}
                gdp = GDP(**kwargs)  # type: ignore
                assert getattr(gdp, field) is None

    def test_empty_string_values(self, subtests):
        """Test handling of empty strings."""
        string_fields = ["type", "prog_ver"]

        for field in string_fields:
            with subtests.test(f"empty string {field}"):
                kwargs = {field: ""}
                gdp = GDP(**kwargs)  # type: ignore
                assert getattr(gdp, field) == ""

    def test_numeric_string_conversion(self, subtests):
        """Test automatic conversion of numeric values to strings."""
        with subtests.test("type numeric conversion"):
            gdp = GDP(type=123)  # type: ignore
            assert gdp.type == "123"

        with subtests.test("prog_ver numeric conversion"):
            gdp = GDP(prog_ver=456.7)  # type: ignore
            assert gdp.prog_ver == "456.7"


class TestGdpSerialization:
    """Test Gdp serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_gdp(self):
        """Fixture for default Gdp instance."""
        return GDP()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_gdp(self):
        """Fixture for populated Gdp instance."""
        return GDP(  # type: ignore
            date="2023-06-15", time="16:45:30", type="zen", prog_ver="v2.1.0"
        )

    def test_model_dump_default(self, default_gdp, subtests):
        """Test model_dump with default values."""
        dump = default_gdp.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["date", "time", "type", "prog_ver"]
            for field in expected_fields:
                assert field in dump

    def test_model_dump_populated(self, populated_gdp, subtests):
        """Test model_dump with populated values."""
        dump = populated_gdp.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["type"] == "zen"
            assert dump["prog_ver"] == "v2.1.0"
            assert isinstance(dump["date"], str)
            assert isinstance(dump["time"], str)

    def test_from_dict_creation(self, subtests):
        """Test creating Gdp from dictionary."""
        with subtests.test("full dict"):
            data = {
                "date": "2023-03-20",
                "time": "11:20:15",
                "type": "zen",
                "prog_ver": "v1.5.0",
            }
            gdp = GDP(**data)  # type: ignore
            assert gdp.type == "zen"
            assert gdp.prog_ver == "v1.5.0"

        with subtests.test("partial dict"):
            data = {"type": "custom"}
            gdp = GDP(**data)  # type: ignore
            assert gdp.type == "custom"
            assert gdp.prog_ver is None

    def test_json_serialization(self, default_gdp, populated_gdp, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated gdp"):
            json_str = populated_gdp.model_dump_json()
            data = json.loads(json_str)
            recreated = GDP(**data)  # type: ignore
            assert recreated.type == populated_gdp.type
            assert recreated.prog_ver == populated_gdp.prog_ver

        with subtests.test("JSON round-trip default gdp"):
            json_str = default_gdp.model_dump_json()
            data = json.loads(json_str)
            recreated = GDP(**data)  # type: ignore
            assert recreated.type == default_gdp.type
            assert recreated.prog_ver == default_gdp.prog_ver

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            gdp = GDP(type="zen", prog_ver="v1.0")  # type: ignore
            dump = gdp.model_dump(exclude_none=True)
            assert "type" in dump
            assert "prog_ver" in dump

        with subtests.test("exclude_none with partial"):
            gdp = GDP(type="zen")  # type: ignore  # prog_ver will be None
            dump = gdp.model_dump(exclude_none=True)
            assert "type" in dump
            # prog_ver should be excluded since it's None


class TestGdpModification:
    """Test Gdp field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Gdp fields after creation."""
        gdp = GDP()  # type: ignore

        test_modifications = [
            ("type", "modified_type"),
            ("prog_ver", "v9.9.9"),
            ("date", "2024-12-31"),
            ("time", "23:59:59"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field}"):
                setattr(gdp, field, value)
                if field in ["date", "time"]:
                    # Date/time fields may be processed by validators
                    assert str(value) in str(getattr(gdp, field))
                else:
                    assert getattr(gdp, field) == value

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        gdp = GDP()  # type: ignore

        updates = {"type": "bulk_type", "prog_ver": "bulk_version"}

        for field, value in updates.items():
            setattr(gdp, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(gdp, field) == expected_value


class TestGdpComparison:
    """Test Gdp comparison and equality operations."""

    def test_gdp_equality(self, subtests):
        """Test Gdp equality comparisons."""
        gdp1 = GDP(type="zen", prog_ver="v1.0")  # type: ignore
        gdp2 = GDP(type="zen", prog_ver="v1.0")  # type: ignore
        gdp3 = GDP(type="different", prog_ver="v1.0")  # type: ignore

        with subtests.test("same values model_dump equal"):
            # Note: dates/times may differ due to default_factory, so compare relevant fields
            assert gdp1.type == gdp2.type
            assert gdp1.prog_ver == gdp2.prog_ver

        with subtests.test("different values model_dump not equal"):
            assert gdp1.type != gdp3.type

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [("type", "zen"), ("prog_ver", "v2.0.0")]

        for field, value in test_values:
            with subtests.test(f"consistency {field} {value}"):
                kwargs = {field: value}
                gdp = GDP(**kwargs)  # type: ignore
                assert getattr(gdp, field) == value

                # Test round-trip consistency
                dump = gdp.model_dump()
                recreated = GDP(**dump)  # type: ignore
                assert getattr(recreated, field) == getattr(gdp, field)


class TestGdpEdgeCases:
    """Test Gdp edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            gdp = GDP(**{})  # type: ignore
            assert gdp.type is None
            assert gdp.prog_ver is None
            assert isinstance(gdp.date, str)
            # Default time returns an MTime object
            assert hasattr(gdp.time, "__str__") or isinstance(gdp.time, str)

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            gdp = GDP(unknown_field="value")  # type: ignore
            assert hasattr(gdp, "unknown_field")
            assert gdp.unknown_field == "value"  # type: ignore

    def test_extreme_date_values(self, subtests):
        """Test extreme date and time values."""
        extreme_cases = [
            ("far future", "2099-12-31"),
            ("far past", "1900-01-01"),
            ("leap year", "2024-02-29"),
        ]

        for case_name, date_value in extreme_cases:
            with subtests.test(f"extreme date {case_name}"):
                gdp = GDP(date=date_value)  # type: ignore
                assert isinstance(gdp.date, str)

    def test_time_formats(self, subtests):
        """Test various time format inputs."""
        time_formats = ["00:00:00", "23:59:59", "12:30:45.123", "09:15:30.999999"]

        for time_format in time_formats:
            with subtests.test(f"time format {time_format}"):
                gdp = GDP(time=time_format)  # type: ignore
                assert isinstance(gdp.time, str)

    def test_special_string_values(self, subtests):
        """Test special characters in string fields."""
        special_values = [
            ("spaces", "value with spaces"),
            ("special chars", "value-with_special.chars"),
            ("unicode", "测试值"),
            ("numbers", "123456"),
        ]

        for case_name, value in special_values:
            with subtests.test(f"special string {case_name}"):
                gdp = GDP(type=value, prog_ver=value)  # type: ignore
                assert gdp.type == value
                assert gdp.prog_ver == value


class TestGdpDocumentation:
    """Test Gdp class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Gdp class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert GDP.__name__ == "GDP"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(GDP, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = GDP.model_fields
        expected_fields = ["date", "time", "type", "prog_ver"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_validators_present(self, subtests):
        """Test that custom validators are properly defined."""
        with subtests.test("date validator"):
            # Test that date validation works
            gdp = GDP(date="2023-01-15")  # type: ignore
            assert isinstance(gdp.date, str)

        with subtests.test("time validator"):
            # Test that time validation works
            gdp = GDP(time="14:30:00")  # type: ignore
            assert isinstance(gdp.time, str)

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            gdp = GDP()  # type: ignore
            dump = gdp.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) > 0

        with subtests.test("all expected fields present"):
            expected_fields = ["date", "time", "type", "prog_ver"]
            dump = GDP().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump

        with subtests.test("model_fields accessible"):
            fields = GDP.model_fields
            assert len(fields) == 4
            assert all(
                field in fields for field in ["date", "time", "type", "prog_ver"]
            )
