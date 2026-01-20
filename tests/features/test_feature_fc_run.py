#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test suite for feature_fc_run.py

Tests for the FeatureFCRun class with fixtures and subtests optimized for efficiency.

Created on: September 13, 2025
Author: GitHub Copilot
"""

# =====================================================
# Imports
# =====================================================
import pytest
from pydantic import ValidationError

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment, TimePeriod

# Import the class under test
from mt_metadata.features.feature_fc_run import FeatureFCRun


# =====================================================
# Fixtures
# =====================================================


@pytest.fixture
def default_fc_run():
    """Fixture providing a default FeatureFCRun instance."""
    return FeatureFCRun()


@pytest.fixture
def sample_time_period():
    """Fixture providing a sample TimePeriod for testing."""
    return TimePeriod(start="2020-01-01T00:00:00", end="2020-01-02T00:00:00")


@pytest.fixture
def sample_comment():
    """Fixture providing a sample Comment for testing."""
    return Comment(value="Test comment for FC run")


@pytest.fixture
def valid_fc_run_configurations():
    """Fixture providing various valid FC run configurations."""
    return [
        {
            "id": "001",
            "sample_rate": 100.0,
            "comments": "Processed with standard parameters",
            "time_period": {
                "start": "2020-01-01T00:00:00",
                "end": "2020-01-02T00:00:00",
            },
        },
        {
            "id": "sr256_001",  # Now valid with underscores allowed
            "sample_rate": 256.0,
            "comments": Comment(value="High frequency sampling"),
            "time_period": TimePeriod(
                start="2021-06-15T10:00:00", end="2021-06-15T12:00:00"
            ),
        },
        {
            "id": "LF_01",
            "sample_rate": 1.0,
            "comments": Comment(value="Low frequency decimation"),
            "time_period": {
                "start": "2019-03-01T00:00:00",
                "end": "2019-03-10T00:00:00",
            },
        },
    ]


@pytest.fixture
def invalid_id_patterns():
    """Fixture providing invalid ID patterns for testing."""
    return [
        "001-A",  # Contains hyphen
        "test!",  # Contains special character
        "sr 256",  # Contains space
        "001@home",  # Contains @ symbol
        "test.run",  # Contains period
        "run#01",  # Contains hash
        "test|run",  # Contains pipe
    ]


@pytest.fixture
def valid_id_patterns():
    """Fixture providing valid ID patterns for testing."""
    return [
        "001",
        "sr256",
        "ABC123",
        "a1b2c3",
        "RUN001",
        "1",
        "a",
        "123ABC456",
        "test_run_001",  # Now valid with underscores
        "sr256_001",  # Now valid with underscores
        "low_freq_01",  # Now valid with underscores
        "_start_underscore",  # Valid with underscores
        "end_underscore_",  # Valid with underscores
    ]


@pytest.fixture
def configured_fc_run(sample_time_period, sample_comment):
    """Fixture providing a fully configured FeatureFCRun instance."""
    return FeatureFCRun(
        id="test_run_001",  # Now valid with underscores allowed
        sample_rate=256.0,
        comments=sample_comment,
        time_period=sample_time_period,
    )


# =====================================================
# Test Classes
# =====================================================


class TestFeatureFCRunInitialization:
    """Test class for FeatureFCRun initialization and basic functionality."""

    def test_default_initialization(self, default_fc_run):
        """Test default initialization sets correct default values."""
        assert default_fc_run.id == ""
        assert default_fc_run.sample_rate == 0.0
        assert isinstance(default_fc_run.comments, Comment)
        assert isinstance(default_fc_run.time_period, TimePeriod)

    def test_inheritance_from_metadata_base(self, default_fc_run):
        """Test that FeatureFCRun properly inherits from MetadataBase."""
        assert isinstance(default_fc_run, MetadataBase)
        assert hasattr(default_fc_run, "model_dump")
        assert hasattr(default_fc_run, "model_validate")

    @pytest.mark.parametrize("config", [0, 1, 2])
    def test_custom_initialization(self, valid_fc_run_configurations, config):
        """Test custom initialization with various valid configurations."""
        config_data = valid_fc_run_configurations[config]
        fc_run = FeatureFCRun(**config_data)

        assert fc_run.id == config_data["id"]
        assert fc_run.sample_rate == config_data["sample_rate"]

        # Test comments field
        if isinstance(config_data["comments"], str):
            assert fc_run.comments.value == config_data["comments"]
        else:
            assert fc_run.comments.value == config_data["comments"].value

        # Test time_period field
        if isinstance(config_data["time_period"], dict):
            assert (
                "2020" in str(fc_run.time_period.start)
                or "2021" in str(fc_run.time_period.start)
                or "2019" in str(fc_run.time_period.start)
            )
        else:
            assert fc_run.time_period == config_data["time_period"]

    def test_initialization_with_time_period(self, sample_time_period):
        """Test initialization with TimePeriod object."""
        fc_run = FeatureFCRun(time_period=sample_time_period)
        assert fc_run.time_period == sample_time_period
        assert "2020-01-01" in str(fc_run.time_period.start)

    def test_field_types_validation(self, configured_fc_run):
        """Test that field types are correctly validated."""
        assert isinstance(configured_fc_run.id, str)
        assert isinstance(configured_fc_run.sample_rate, float)
        assert isinstance(configured_fc_run.comments, Comment)
        assert isinstance(configured_fc_run.time_period, TimePeriod)


class TestFeatureFCRunIdValidation:
    """Test class for ID field pattern validation."""

    @pytest.mark.parametrize(
        "valid_id",
        [
            "001",
            "sr256",
            "ABC123",
            "a1b2c3",
            "RUN001",
            "1",
            "a",
            "123ABC456",
            "test_run_001",
            "sr256_001",
            "low_freq_01",  # Now valid with underscores
        ],
    )
    def test_valid_id_patterns(self, valid_id):
        """Test that valid ID patterns are accepted."""
        fc_run = FeatureFCRun(id=valid_id)
        assert fc_run.id == valid_id

    @pytest.mark.parametrize(
        "invalid_id",
        ["001-A", "test!", "sr 256", "001@home", "test.run", "run#01", "test|run"],
    )
    def test_invalid_id_patterns_rejection(self, invalid_id):
        """Test that invalid ID patterns are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            FeatureFCRun(id=invalid_id)
        assert "String should match pattern" in str(exc_info.value)

    def test_empty_id_allowed(self):
        """Test that empty string ID is allowed (default)."""
        fc_run = FeatureFCRun(id="")
        assert fc_run.id == ""

    def test_id_pattern_comprehensive(self):
        """Test comprehensive ID pattern validation."""
        # Test alphanumeric and underscore - should pass
        valid_ids = [
            "123",
            "abc",
            "ABC",
            "123abc",
            "ABC123",
            "a1B2c3",
            "test_run",
            "sr256_001",
            "_underscore",
        ]
        for valid_id in valid_ids:
            fc_run = FeatureFCRun(id=valid_id)
            assert fc_run.id == valid_id

        # Test invalid characters - should fail (note: underscore is now valid)
        invalid_chars = [
            "-",
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "+",
            "=",
            "[",
            "]",
            "{",
            "}",
            "|",
            "\\",
            ":",
            ";",
            "'",
            '"',
            "<",
            ">",
            ",",
            ".",
            "?",
            "/",
            "~",
            "`",
            " ",
        ]
        for char in invalid_chars[:5]:  # Test subset for efficiency
            with pytest.raises(ValidationError):
                FeatureFCRun(id=f"test{char}id")


class TestFeatureFCRunSampleRateValidation:
    """Test class for sample_rate field validation."""

    @pytest.mark.parametrize(
        "sample_rate,expected",
        [
            (100.0, 100.0),
            (256.0, 256.0),
            (1.0, 1.0),
            (0.1, 0.1),
            (1024.0, 1024.0),
            (0, 0.0),
            (1, 1.0),  # Test int to float conversion
        ],
    )
    def test_valid_sample_rates(self, sample_rate, expected):
        """Test valid sample rate values."""
        fc_run = FeatureFCRun(sample_rate=sample_rate)
        assert fc_run.sample_rate == expected

    @pytest.mark.parametrize(
        "invalid_rate",
        [
            -1.0,  # Negative values should be accepted by pydantic (no constraints)
            -100.0,
        ],
    )
    def test_negative_sample_rates_allowed(self, invalid_rate):
        """Test that negative sample rates are allowed (no field constraints)."""
        fc_run = FeatureFCRun(sample_rate=invalid_rate)
        assert fc_run.sample_rate == invalid_rate

    def test_string_to_float_conversion(self):
        """Test automatic string to float conversion."""
        fc_run = FeatureFCRun(sample_rate="256.0")
        assert fc_run.sample_rate == 256.0
        assert isinstance(fc_run.sample_rate, float)

    def test_extreme_sample_rate_values(self):
        """Test extreme sample rate values."""
        # Very small positive value
        fc_run = FeatureFCRun(sample_rate=1e-10)
        assert fc_run.sample_rate == 1e-10

        # Very large value
        fc_run = FeatureFCRun(sample_rate=1e6)
        assert fc_run.sample_rate == 1e6

    def test_invalid_sample_rate_types(self):
        """Test invalid sample rate types."""
        with pytest.raises(ValidationError) as exc_info:
            FeatureFCRun(sample_rate="invalid")
        assert "Input should be a valid number" in str(exc_info.value)


class TestFeatureFCRunCommentsValidation:
    """Test class for comments field validation and Comment integration."""

    def test_string_comment_validation(self):
        """Test comments field validator with string input."""
        fc_run = FeatureFCRun(comments="Test comment string")
        assert isinstance(fc_run.comments, Comment)
        assert fc_run.comments.value == "Test comment string"

    def test_comment_object_validation(self, sample_comment):
        """Test comments field validator with Comment object input."""
        fc_run = FeatureFCRun(comments=sample_comment)
        assert fc_run.comments == sample_comment
        assert fc_run.comments.value == sample_comment.value

    def test_default_comment_creation(self, default_fc_run):
        """Test that default Comment object is created properly."""
        assert isinstance(default_fc_run.comments, Comment)
        # Default Comment should have empty/None value
        assert default_fc_run.comments.value in ["", None]

    def test_empty_string_comment(self):
        """Test comments field with empty string."""
        fc_run = FeatureFCRun(comments="")
        assert isinstance(fc_run.comments, Comment)
        assert fc_run.comments.value == ""

    def test_comment_with_special_characters(self):
        """Test comments field with special characters."""
        special_comment = "Comment with émojis 🔬 and special chars: @#$%^&*()!"
        fc_run = FeatureFCRun(comments=special_comment)
        assert fc_run.comments.value == special_comment

    def test_long_comment_string(self):
        """Test comments field with very long string."""
        long_comment = "This is a very long comment " * 50
        fc_run = FeatureFCRun(comments=long_comment)
        assert fc_run.comments.value == long_comment

    def test_none_comment_behavior(self):
        """Test comments field with None value."""
        # None is not accepted - should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            FeatureFCRun(comments=None)
        assert "comments" in str(exc_info.value)
        assert "Input should be a valid dictionary or instance of Comment" in str(
            exc_info.value
        )


class TestFeatureFCRunTimePeriodIntegration:
    """Test class for TimePeriod field functionality."""

    def test_default_time_period_creation(self, default_fc_run):
        """Test that default TimePeriod is created with default factory."""
        assert isinstance(default_fc_run.time_period, TimePeriod)
        # Default TimePeriod should have default start/end times
        assert "1980" in str(default_fc_run.time_period.start)

    def test_custom_time_period_assignment(self, sample_time_period):
        """Test custom TimePeriod assignment."""
        fc_run = FeatureFCRun(time_period=sample_time_period)
        assert fc_run.time_period == sample_time_period
        assert "2020-01-01" in str(fc_run.time_period.start)

    def test_time_period_dict_initialization(self):
        """Test TimePeriod initialization with dictionary."""
        time_dict = {"start": "2021-05-01T10:00:00", "end": "2021-05-01T12:00:00"}
        fc_run = FeatureFCRun(time_period=time_dict)
        assert isinstance(fc_run.time_period, TimePeriod)
        assert "2021-05-01" in str(fc_run.time_period.start)

    def test_time_period_modification(self, configured_fc_run):
        """Test modifying time_period after initialization."""
        new_time_period = TimePeriod(
            start="2022-01-01T00:00:00", end="2022-01-02T00:00:00"
        )
        configured_fc_run.time_period = new_time_period

        assert configured_fc_run.time_period == new_time_period
        assert "2022-01-01" in str(configured_fc_run.time_period.start)


class TestFeatureFCRunValidation:
    """Test class for field validation and error conditions."""

    def test_required_fields_behavior(self):
        """Test behavior with required vs optional fields."""
        # All fields have defaults, so no required field validation errors expected
        fc_run = FeatureFCRun()
        assert fc_run.id == ""
        assert fc_run.sample_rate == 0.0
        assert isinstance(fc_run.comments, Comment)
        assert isinstance(fc_run.time_period, TimePeriod)

    def test_field_constraint_validation(self):
        """Test field constraints and validation."""
        # id field has pattern constraint
        with pytest.raises(ValidationError):
            FeatureFCRun(id="invalid-id-with-hyphen")

        # sample_rate must be numeric
        with pytest.raises(ValidationError):
            FeatureFCRun(sample_rate="not_a_number")

    def test_type_coercion_behavior(self):
        """Test automatic type coercion for fields."""
        # Integer to float for sample_rate
        fc_run = FeatureFCRun(sample_rate=100)
        assert fc_run.sample_rate == 100.0
        assert isinstance(fc_run.sample_rate, float)

        # String to Comment for comments
        fc_run = FeatureFCRun(comments="test")
        assert isinstance(fc_run.comments, Comment)
        assert fc_run.comments.value == "test"

    def test_edge_case_values(self):
        """Test edge case values for all fields."""
        # Minimum values
        fc_run = FeatureFCRun(
            id="",  # Empty string
            sample_rate=0.0,  # Zero
            comments="",  # Empty comment
        )
        assert fc_run.id == ""
        assert fc_run.sample_rate == 0.0
        assert fc_run.comments.value == ""

    def test_unicode_and_special_characters(self):
        """Test Unicode and special character handling."""
        # Unicode in comments
        fc_run = FeatureFCRun(comments="Überprüfung mit Umlauten")
        assert fc_run.comments.value == "Überprüfung mit Umlauten"

        # Unicode not allowed in id due to pattern constraint
        with pytest.raises(ValidationError):
            FeatureFCRun(id="über")


class TestFeatureFCRunIntegration:
    """Test class for integration scenarios and comprehensive functionality."""

    def test_full_workflow_integration(self, configured_fc_run):
        """Test complete workflow from initialization to usage."""
        # Verify initial state
        assert configured_fc_run.id == "test_run_001"
        assert configured_fc_run.sample_rate == 256.0
        assert configured_fc_run.comments.value == "Test comment for FC run"

        # Modify values
        configured_fc_run.sample_rate = 512.0
        configured_fc_run.comments = "Updated comment"

        # Verify modifications
        assert configured_fc_run.sample_rate == 512.0
        assert configured_fc_run.comments.value == "Updated comment"

    def test_serialization_deserialization(self, configured_fc_run):
        """Test model serialization and deserialization."""
        # Serialize to dict
        fc_run_dict = configured_fc_run.model_dump()

        # Verify dict structure
        assert "id" in fc_run_dict
        assert "sample_rate" in fc_run_dict
        assert "comments" in fc_run_dict
        assert "time_period" in fc_run_dict

        # Deserialize back to object
        new_fc_run = FeatureFCRun(**fc_run_dict)

        # Verify equality of key fields
        assert new_fc_run.id == configured_fc_run.id
        assert new_fc_run.sample_rate == configured_fc_run.sample_rate
        assert new_fc_run.comments.value == configured_fc_run.comments.value

    def test_copy_and_modification(self, configured_fc_run):
        """Test copying and modifying FC run instances."""
        # Create copy using model_dump
        fc_run_copy = FeatureFCRun(**configured_fc_run.model_dump())

        # Verify copy
        assert fc_run_copy.id == configured_fc_run.id
        assert fc_run_copy.sample_rate == configured_fc_run.sample_rate

        # Modify copy
        fc_run_copy.id = "modified_copy"
        fc_run_copy.sample_rate = 1024.0

        # Verify original unchanged
        assert configured_fc_run.id == "test_run_001"
        assert configured_fc_run.sample_rate == 256.0

    def test_equality_comparison(self):
        """Test equality comparison between FC run instances."""
        fc_run1 = FeatureFCRun(id="test", sample_rate=100.0)
        fc_run2 = FeatureFCRun(id="test", sample_rate=100.0)

        # Note: MetadataBase instances may not have == operator overridden
        # So we test field-by-field equality
        assert fc_run1.id == fc_run2.id
        assert fc_run1.sample_rate == fc_run2.sample_rate

    def test_comprehensive_configuration(self):
        """Test comprehensive configuration with all field types."""
        comprehensive_config = {
            "id": "comprehensive001",
            "sample_rate": 256.0,
            "comments": Comment(
                value="Comprehensive test configuration",
                author="Test Author",
                date="2020-01-01T00:00:00",
            ),
            "time_period": TimePeriod(
                start="2020-06-01T00:00:00", end="2020-06-30T23:59:59"
            ),
        }

        fc_run = FeatureFCRun(**comprehensive_config)

        # Verify all fields
        assert fc_run.id == "comprehensive001"
        assert fc_run.sample_rate == 256.0
        assert fc_run.comments.value == "Comprehensive test configuration"
        assert fc_run.comments.author == "Test Author"
        assert "2020-06-01" in str(fc_run.time_period.start)
        assert "2020-06-30" in str(fc_run.time_period.end)

    def test_error_propagation_and_handling(self):
        """Test error propagation and proper error handling."""
        # Test multiple validation errors
        with pytest.raises(ValidationError) as exc_info:
            FeatureFCRun(
                id="invalid-id!",  # Invalid pattern
                sample_rate="not_a_number",  # Invalid type
            )

        # Should have multiple validation errors
        errors = exc_info.value.errors()
        assert len(errors) >= 2

        # Check for specific error types
        error_types = [error["type"] for error in errors]
        assert (
            "string_pattern_mismatch" in error_types or "string_parsing" in error_types
        )

    def test_model_validation_comprehensive(self):
        """Test comprehensive model validation scenarios."""
        # Valid minimal configuration
        minimal_fc_run = FeatureFCRun()
        assert minimal_fc_run.model_validate(minimal_fc_run.model_dump())

        # Valid maximal configuration
        maximal_config = {
            "id": "maximal123ABC",
            "sample_rate": 2048.0,
            "comments": "Detailed comments with all information",
            "time_period": {
                "start": "2020-01-01T00:00:00",
                "end": "2020-12-31T23:59:59",
            },
        }
        maximal_fc_run = FeatureFCRun(**maximal_config)
        assert maximal_fc_run.id == "maximal123ABC"
        assert maximal_fc_run.sample_rate == 2048.0
