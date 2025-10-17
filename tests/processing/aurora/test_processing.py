#!/usr/bin/env python3
"""
Pytest suite for processing_basemodel.py

This file tests the Processing class and BandSpecificationStyleEnum functionality
using pytest fixtures, parametrized tests, and markers for optimal efficiency.

Run with:
    pytest test_processing.py
    pytest test_processing.py -m enum  # Run only enum tests
    pytest test_processing.py -m integration  # Run only integration tests
    pytest test_processing.py -v  # Verbose output

Test organization:
- Fixtures for reusable test data and instances
- Parametrized tests for efficiency
- Pytest markers for test categorization
- Integration tests for complete workflows
"""

import pytest

from mt_metadata.processing.aurora.processing import (
    BandSpecificationStyleEnum,
    Processing,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def processing_instance():
    """Create a basic Processing instance with default values."""
    return Processing()


@pytest.fixture
def populated_processing():
    """Create a Processing instance with populated values."""
    processing = Processing()
    processing.id = "test_config"
    processing.band_specification_style = BandSpecificationStyleEnum.EMTF
    processing.band_setup_file = "/test/path/setup.cfg"
    return processing


@pytest.fixture
def sample_processing_data():
    """Sample data for creating Processing instances from dictionaries."""
    return {
        "id": "dict_test_config",
        "band_specification_style": "EMTF",
        "band_setup_file": "/test/path/setup.cfg",
    }


@pytest.fixture
def enum_test_values():
    """Test values for enum testing."""
    return {
        "valid_strings": ["EMTF", "band_edges"],
        "invalid_strings": ["invalid_value", "", "random_text"],
        "invalid_types": [123, [], {}],
    }


# ============================================================================
# ENUM TESTS
# ============================================================================


@pytest.mark.enum
class TestBandSpecificationStyleEnum:
    """Test BandSpecificationStyleEnum functionality."""

    def test_enum_values(self):
        """Test that enum has expected string representations."""
        assert "EMTF" in str(BandSpecificationStyleEnum.EMTF)
        assert "band_edges" in str(BandSpecificationStyleEnum.band_edges)

    def test_enum_string_inheritance(self):
        """Test that enum inherits from string."""
        assert isinstance(BandSpecificationStyleEnum.EMTF, str)
        assert isinstance(BandSpecificationStyleEnum.band_edges, str)

    @pytest.mark.parametrize(
        "enum_value,expected",
        [
            ("EMTF", BandSpecificationStyleEnum.EMTF),
            ("band_edges", BandSpecificationStyleEnum.band_edges),
        ],
    )
    def test_enum_from_string(self, enum_value, expected):
        """Test creating enum instances from string values."""
        result = BandSpecificationStyleEnum(enum_value)
        assert result == expected

    def test_enum_comparison(self):
        """Test enum comparison operations."""
        emtf1 = BandSpecificationStyleEnum.EMTF
        emtf2 = BandSpecificationStyleEnum("EMTF")
        band_edges = BandSpecificationStyleEnum.band_edges

        # Test equality
        assert emtf1 == emtf2
        assert emtf1 != band_edges

        # Test identity
        assert emtf1 is BandSpecificationStyleEnum.EMTF

    @pytest.mark.parametrize("invalid_value", ["invalid_value", "", 123])
    def test_enum_error_cases(self, invalid_value):
        """Test enum error handling for invalid values."""
        with pytest.raises((ValueError, TypeError)):
            BandSpecificationStyleEnum(invalid_value)


# ============================================================================
# PROCESSING BASIC TESTS
# ============================================================================


@pytest.mark.basics
class TestProcessingBasics:
    """Test BandSpecificationStyleEnum functionality."""

    def test_enum_values(self):
        """Test basic Processing class functionality."""

    def test_default_instantiation(self, processing_instance):
        """Test creating Processing instance with defaults."""
        # Check default values
        assert isinstance(processing_instance.decimations, list)
        assert len(processing_instance.decimations) == 0
        assert processing_instance.band_specification_style is None
        assert processing_instance.band_setup_file is None
        assert processing_instance.id == ""

    @pytest.mark.parametrize(
        "field_name,input_value,expected_value",
        [
            ("id", "test_processing_config", "test_processing_config"),
            ("band_setup_file", "/path/to/band_setup.cfg", "/path/to/band_setup.cfg"),
        ],
    )
    def test_field_assignment(
        self, processing_instance, field_name, input_value, expected_value
    ):
        """Test assigning values to Processing fields using parametrized tests."""
        setattr(processing_instance, field_name, input_value)
        assert getattr(processing_instance, field_name) == expected_value

    def test_enum_field_assignment(self, processing_instance):
        """Test enum field assignment separately due to type complexity."""
        processing_instance.band_specification_style = BandSpecificationStyleEnum.EMTF
        assert (
            processing_instance.band_specification_style
            == BandSpecificationStyleEnum.EMTF
        )

    @pytest.mark.parametrize(
        "enum_value,expected_type",
        [
            (BandSpecificationStyleEnum.EMTF, BandSpecificationStyleEnum),
            (BandSpecificationStyleEnum.band_edges, BandSpecificationStyleEnum),
            (None, type(None)),
        ],
    )
    def test_enum_assignment_types(
        self, processing_instance, enum_value, expected_type
    ):
        """Test enum assignment with various types."""
        processing_instance.band_specification_style = enum_value
        assert type(processing_instance.band_specification_style) == expected_type

    def test_enum_string_assignment(self, processing_instance):
        """Test assigning enum via string (should convert automatically)."""
        # String assignment should convert to enum
        processing_instance.band_specification_style = (
            BandSpecificationStyleEnum.band_edges
        )
        assert (
            processing_instance.band_specification_style
            == BandSpecificationStyleEnum.band_edges
        )

        # None assignment should work
        processing_instance.band_specification_style = None
        assert processing_instance.band_specification_style is None

    def test_from_dict_creation(self, sample_processing_data):
        """Test creating Processing instance from dictionary."""
        processing = Processing.model_validate(sample_processing_data)

        assert processing.id == "dict_test_config"
        assert processing.band_specification_style == BandSpecificationStyleEnum.EMTF
        assert processing.band_setup_file == "/test/path/setup.cfg"


# ============================================================================
# VALIDATION TESTS
# ============================================================================


@pytest.mark.validation
class TestProcessingValidation:
    """Test Processing field validation."""

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "invalid_enum_value",
            12345,
            [],
            {},
        ],
    )
    def test_invalid_enum_assignment(self, processing_instance, invalid_value):
        """Test that invalid enum values raise errors."""
        with pytest.raises((ValueError, TypeError)):
            processing_instance.band_specification_style = invalid_value


# ============================================================================
# DECIMATION TESTS
# ============================================================================


@pytest.mark.decimations
class TestProcessingDecimations:
    """Test decimation-related functionality."""

    @pytest.mark.parametrize(
        "property_name,expected_type,expected_value",
        [
            ("decimations", list, 0),  # Check length
            ("num_decimation_levels", int, 0),
        ],
    )
    def test_empty_decimations_properties(
        self, processing_instance, property_name, expected_type, expected_value
    ):
        """Test decimation-related properties with empty decimations."""
        value = getattr(processing_instance, property_name)
        if property_name == "decimations":
            assert isinstance(value, expected_type)
            assert len(value) == expected_value
        else:
            assert isinstance(value, expected_type)
            assert value == expected_value

    def test_decimations_dict_property(self, processing_instance):
        """Test decimations_dict computed property."""
        decimations_dict = processing_instance.decimations_dict

        assert isinstance(decimations_dict, dict)
        assert len(decimations_dict) == 0


# ============================================================================
# UTILITY TESTS
# ============================================================================


@pytest.mark.utilities
class TestProcessingUtilities:
    """Test utility methods of Processing class."""

    @pytest.mark.parametrize(
        "config_id,expected_filename",
        [
            ("my_config", "my_config_processing_config.json"),
            ("", "_processing_config.json"),
            ("test-123", "test-123_processing_config.json"),
        ],
    )
    def test_json_filename_generation(
        self, processing_instance, config_id, expected_filename
    ):
        """Test JSON filename generation with various IDs."""
        processing_instance.id = config_id
        assert processing_instance.json_fn() == expected_filename

    @pytest.mark.parametrize(
        "channel_list",
        [
            ["ex", "ey"],
            ["hx", "hy", "hz"],
            ["rrhx", "rrhy"],
            [],
        ],
    )
    def test_channel_management_methods(self, processing_instance, channel_list):
        """Test channel management methods work without errors."""
        # These should work without error even with empty decimations
        processing_instance.drop_reference_channels()
        processing_instance.set_input_channels(channel_list)
        processing_instance.set_output_channels(channel_list)
        processing_instance.set_reference_channels(channel_list)

        # Should not have added any decimations
        assert len(processing_instance.decimations) == 0


# ============================================================================
# SERIALIZATION TESTS
# ============================================================================


@pytest.mark.serialization
class TestProcessingSerialization:
    """Test JSON serialization and deserialization."""

    def test_json_serialization_roundtrip(self, populated_processing):
        """Test JSON serialization and deserialization preserves data."""
        # Serialize to JSON
        json_str = populated_processing.model_dump_json()
        assert isinstance(json_str, str)
        assert "test_config" in json_str

        # Deserialize from JSON
        processing_restored = Processing.model_validate_json(json_str)

        # Verify data integrity
        assert processing_restored.id == "test_config"
        assert (
            processing_restored.band_specification_style
            == BandSpecificationStyleEnum.EMTF
        )
        assert processing_restored.band_setup_file == "/test/path/setup.cfg"

    @pytest.mark.parametrize(
        "test_data",
        [
            {"id": "dict_conversion_test", "band_specification_style": "EMTF"},
            {"id": "minimal_test"},
            {
                "id": "full_test",
                "band_specification_style": "band_edges",
                "band_setup_file": "/test.cfg",
            },
        ],
    )
    def test_dict_conversion_parametrized(self, test_data):
        """Test dictionary conversion with various configurations."""
        processing = Processing.model_validate(test_data)

        # Convert to dictionary
        processing_dict = processing.model_dump()

        assert isinstance(processing_dict, dict)
        assert "id" in processing_dict
        assert "decimations" in processing_dict
        assert processing_dict["id"] == test_data["id"]

        # Verify specific fields if they were set
        if "band_specification_style" in test_data:
            assert (
                processing_dict["band_specification_style"]
                == test_data["band_specification_style"]
            )

    def test_minimal_dict_creation(self):
        """Test creating Processing from minimal dictionary."""
        minimal_data = {"id": "minimal_test"}

        processing = Processing.model_validate(minimal_data)

        assert processing.id == "minimal_test"
        assert processing.band_specification_style is None
        assert len(processing.decimations) == 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.integration
class TestProcessingIntegration:
    """Integration tests that test multiple components together."""

    def test_complete_workflow(self, sample_processing_data):
        """Test a complete workflow: create, modify, serialize, deserialize."""
        # Create from dict
        processing = Processing.model_validate(sample_processing_data)

        # Modify
        processing.id = "workflow_test"
        processing.band_specification_style = BandSpecificationStyleEnum.band_edges

        # Serialize
        json_str = processing.model_dump_json()

        # Deserialize
        restored = Processing.model_validate_json(json_str)

        # Verify
        assert restored.id == "workflow_test"
        assert (
            restored.band_specification_style == BandSpecificationStyleEnum.band_edges
        )
        assert restored.band_setup_file == sample_processing_data["band_setup_file"]

    @pytest.mark.parametrize(
        "enum_style",
        [
            BandSpecificationStyleEnum.EMTF,
            BandSpecificationStyleEnum.band_edges,
            None,
        ],
    )
    def test_enum_serialization_roundtrip(self, processing_instance, enum_style):
        """Test enum serialization roundtrip with different values."""
        processing_instance.band_specification_style = enum_style
        processing_instance.id = "enum_test"

        # Serialize and deserialize
        json_str = processing_instance.model_dump_json()
        restored = Processing.model_validate_json(json_str)

        # Verify enum is preserved
        assert restored.band_specification_style == enum_style
