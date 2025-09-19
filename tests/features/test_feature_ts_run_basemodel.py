"""
Comprehensive pytest suite for FeatureTSRun class.
Tests cover field validation, inheritance, serialization and performance.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.common import TimePeriod
from mt_metadata.common.comment import Comment
from mt_metadata.features.feature_ts_run import FeatureTSRun


# Test fixtures for data generation
@pytest.fixture
def valid_feature_ts_run_data():
    """Fixture providing valid FeatureTSRun test data."""
    return {
        "id": "test_run_001",
        "sample_rate": 1000.0,
        "comments": "Test time series run",
        "time_period": {
            "start": "2023-01-01T00:00:00+00:00",
            "end": "2023-01-01T23:59:59+00:00",
        },
    }


@pytest.fixture
def feature_ts_run_instance(valid_feature_ts_run_data):
    """Fixture providing a configured FeatureTSRun instance."""
    return FeatureTSRun(**valid_feature_ts_run_data)


@pytest.fixture
def comment_data():
    """Fixture providing Comment test data."""
    return {
        "value": "Sample time series comment",
        "author": "test_author",
        "time_stamp": {"time_stamp": "2023-01-01T12:00:00+00:00"},
    }


@pytest.fixture
def time_period_data():
    """Fixture providing TimePeriod test data."""
    return {
        "start": {"time_stamp": "2023-01-01T00:00:00+00:00"},
        "end": {"time_stamp": "2023-01-01T23:59:59+00:00"},
    }


# Test class for basic functionality
class TestFeatureTSRunBasicFunctionality:
    """Test basic FeatureTSRun functionality."""

    def test_default_initialization(self):
        """Test FeatureTSRun default initialization."""
        feature_ts_run = FeatureTSRun()

        assert feature_ts_run.id == ""
        assert feature_ts_run.sample_rate == 0.0
        assert isinstance(feature_ts_run.comments, Comment)
        assert isinstance(feature_ts_run.time_period, TimePeriod)

    def test_initialization_with_valid_data(self, valid_feature_ts_run_data):
        """Test FeatureTSRun initialization with valid data."""
        feature_ts_run = FeatureTSRun(**valid_feature_ts_run_data)

        assert feature_ts_run.id == "test_run_001"
        assert feature_ts_run.sample_rate == 1000.0
        assert isinstance(feature_ts_run.comments, Comment)
        assert feature_ts_run.comments.value == "Test time series run"
        assert isinstance(feature_ts_run.time_period, TimePeriod)

    def test_inheritance_from_metadata_base(self, feature_ts_run_instance):
        """Test that FeatureTSRun properly inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        assert isinstance(feature_ts_run_instance, MetadataBase)
        assert hasattr(feature_ts_run_instance, "to_dict")
        assert hasattr(feature_ts_run_instance, "from_dict")
        assert hasattr(feature_ts_run_instance, "to_json")
        assert hasattr(feature_ts_run_instance, "from_json")


# Test class for ID field validation
class TestFeatureTSRunIdField:
    """Test FeatureTSRun ID field validation and patterns."""

    @pytest.mark.parametrize(
        "valid_id",
        [
            "test_run_001",
            "TS_RUN_123",
            "run_alpha_beta",
            "ABC123DEF",
            "ts_run_001_final",
            "run123",
            "simple_id",
            "",  # Empty string should be valid
            "a",
            "Z",
            "0",
            "9",
            "_",
            "a_1_b_2_c_3",
        ],
    )
    def test_valid_id_patterns(self, valid_id):
        """Test that valid ID patterns are accepted."""
        feature_ts_run = FeatureTSRun(id=valid_id)
        assert feature_ts_run.id == valid_id

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "test-run",  # Hyphen not allowed
            "test.run",  # Dot not allowed
            "test run",  # Space not allowed
            "test@run",  # Special character not allowed
            "test#run",  # Hash not allowed
            "test$run",  # Dollar sign not allowed
            "test%run",  # Percent not allowed
            "test&run",  # Ampersand not allowed
            "test*run",  # Asterisk not allowed
            "test+run",  # Plus not allowed
            "test=run",  # Equals not allowed
            "test[run]",  # Brackets not allowed
            "test{run}",  # Braces not allowed
            "test|run",  # Pipe not allowed
            "test\\run",  # Backslash not allowed
            "test/run",  # Forward slash not allowed
            "test:run",  # Colon not allowed
            "test;run",  # Semicolon not allowed
            'test"run',  # Quote not allowed
            "test'run",  # Apostrophe not allowed
            "test<run>",  # Angle brackets not allowed
            "test,run",  # Comma not allowed
            "test?run",  # Question mark not allowed
            "test!run",  # Exclamation not allowed
        ],
    )
    def test_invalid_id_patterns(self, invalid_id):
        """Test that invalid ID patterns are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            FeatureTSRun(id=invalid_id)

        assert "String should match pattern" in str(exc_info.value)

    def test_id_none_handling(self):
        """Test handling of None ID value."""
        # None values for ID are not allowed
        with pytest.raises(ValidationError):
            FeatureTSRun(id=None)

    def test_id_numeric_handling(self):
        """Test handling of numeric ID values."""
        # Numeric values get converted to strings by Pydantic, so this actually works
        feature_ts_run = FeatureTSRun(id=123)
        assert feature_ts_run.id == "123"


# Test class for sample_rate field validation
class TestFeatureTSRunSampleRateField:
    """Test FeatureTSRun sample_rate field validation."""

    @pytest.mark.parametrize(
        "valid_sample_rate",
        [0.0, 1.0, 100.0, 1000.0, 44100.0, 0.5, 0.001, 1e6, 3.14159, 999999.999],
    )
    def test_valid_sample_rates(self, valid_sample_rate):
        """Test that valid sample rates are accepted."""
        feature_ts_run = FeatureTSRun(sample_rate=valid_sample_rate)
        assert feature_ts_run.sample_rate == valid_sample_rate

    @pytest.mark.parametrize(
        "invalid_sample_rate",
        [
            "not_a_number",
            None,
            [],
            {},
        ],
    )
    def test_invalid_sample_rates(self, invalid_sample_rate):
        """Test that invalid sample rates are rejected."""
        with pytest.raises(ValidationError):
            FeatureTSRun(sample_rate=invalid_sample_rate)

    def test_sample_rate_string_number_conversion(self):
        """Test that string numbers are converted to float."""
        feature_ts_run = FeatureTSRun(sample_rate="100.0")
        assert feature_ts_run.sample_rate == 100.0
        assert isinstance(feature_ts_run.sample_rate, float)

    def test_sample_rate_integer_conversion(self):
        """Test that integer sample rates are converted to float."""
        feature_ts_run = FeatureTSRun(sample_rate=1000)
        assert feature_ts_run.sample_rate == 1000.0
        assert isinstance(feature_ts_run.sample_rate, float)

    def test_sample_rate_boolean_conversion(self):
        """Test that boolean values are converted to float."""
        feature_ts_run_true = FeatureTSRun(sample_rate=True)
        assert feature_ts_run_true.sample_rate == 1.0

        feature_ts_run_false = FeatureTSRun(sample_rate=False)
        assert feature_ts_run_false.sample_rate == 0.0

    def test_negative_sample_rate(self):
        """Test negative sample rate handling."""
        feature_ts_run = FeatureTSRun(sample_rate=-100.0)
        assert feature_ts_run.sample_rate == -100.0


# Test class for comments field validation
class TestFeatureTSRunCommentsField:
    """Test FeatureTSRun comments field validation and conversion."""

    def test_string_comment_conversion(self):
        """Test that string comments are converted to Comment objects."""
        comment_text = "Test time series comment"
        feature_ts_run = FeatureTSRun(comments=comment_text)

        assert isinstance(feature_ts_run.comments, Comment)
        assert feature_ts_run.comments.value == comment_text

    def test_comment_object_preservation(self, comment_data):
        """Test that Comment objects are preserved as-is."""
        comment_obj = Comment(**comment_data)
        feature_ts_run = FeatureTSRun(comments=comment_obj)

        assert feature_ts_run.comments is comment_obj
        assert feature_ts_run.comments.value == comment_data["value"]
        assert feature_ts_run.comments.author == comment_data["author"]

    def test_dict_comment_conversion(self, comment_data):
        """Test that dictionary comments are converted to Comment objects."""
        feature_ts_run = FeatureTSRun(comments=comment_data)

        assert isinstance(feature_ts_run.comments, Comment)
        assert feature_ts_run.comments.value == comment_data["value"]
        assert feature_ts_run.comments.author == comment_data["author"]

    def test_empty_string_comment(self):
        """Test empty string comment handling."""
        feature_ts_run = FeatureTSRun(comments="")

        assert isinstance(feature_ts_run.comments, Comment)
        assert feature_ts_run.comments.value == ""

    def test_none_comment_conversion(self):
        """Test None comment handling - creates default Comment."""
        feature_ts_run = FeatureTSRun()  # None is default

        assert isinstance(feature_ts_run.comments, Comment)
        assert feature_ts_run.comments.value is None

    @pytest.mark.parametrize("invalid_comment", [123, [], True, False])
    def test_invalid_comment_types(self, invalid_comment):
        """Test handling of invalid comment types."""
        with pytest.raises(ValidationError):
            FeatureTSRun(comments=invalid_comment)


# Test class for time_period field validation
class TestFeatureTSRunTimePeriodField:
    """Test FeatureTSRun time_period field validation."""

    def test_default_time_period_creation(self):
        """Test that default TimePeriod is created when not provided."""
        feature_ts_run = FeatureTSRun()

        assert isinstance(feature_ts_run.time_period, TimePeriod)
        assert hasattr(feature_ts_run.time_period, "start")
        assert hasattr(feature_ts_run.time_period, "end")

    def test_dict_time_period_conversion(self, time_period_data):
        """Test that dictionary time_period is converted to TimePeriod object."""
        feature_ts_run = FeatureTSRun(time_period=time_period_data)

        assert isinstance(feature_ts_run.time_period, TimePeriod)

    def test_time_period_object_preservation(self, time_period_data):
        """Test that TimePeriod objects are preserved as-is."""
        time_period_obj = TimePeriod(**time_period_data)
        feature_ts_run = FeatureTSRun(time_period=time_period_obj)

        assert feature_ts_run.time_period is time_period_obj

    def test_none_time_period_handling(self):
        """Test None time_period handling with default factory."""
        feature_ts_run = FeatureTSRun()  # None is default

        assert isinstance(feature_ts_run.time_period, TimePeriod)


# Test class for serialization and deserialization
class TestFeatureTSRunSerialization:
    """Test FeatureTSRun serialization and deserialization."""

    def test_to_dict_functionality(self, feature_ts_run_instance):
        """Test FeatureTSRun to_dict method."""
        result_dict = feature_ts_run_instance.to_dict()

        assert isinstance(result_dict, dict)
        assert "feature_t_s_run" in result_dict
        assert "id" in result_dict["feature_t_s_run"]
        assert "sample_rate" in result_dict["feature_t_s_run"]
        assert "comments" in result_dict["feature_t_s_run"]

    def test_from_dict_functionality(self, valid_feature_ts_run_data):
        """Test FeatureTSRun from_dict method."""
        # Create nested dictionary structure expected by from_dict
        dict_data = {"feature_t_s_run": valid_feature_ts_run_data}

        reconstructed = FeatureTSRun()
        reconstructed.from_dict(dict_data)

        assert isinstance(reconstructed, FeatureTSRun)
        assert reconstructed.id == valid_feature_ts_run_data["id"]
        assert reconstructed.sample_rate == valid_feature_ts_run_data["sample_rate"]
        assert isinstance(reconstructed.comments, Comment)
        assert isinstance(reconstructed.time_period, TimePeriod)

    def test_to_json_functionality(self, feature_ts_run_instance):
        """Test FeatureTSRun to_json method."""
        json_str = feature_ts_run_instance.to_json()

        assert isinstance(json_str, str)
        parsed_json = json.loads(json_str)
        assert "feature_t_s_run" in parsed_json

    def test_from_json_functionality(self, valid_feature_ts_run_data):
        """Test FeatureTSRun from_json method."""
        # Create nested dictionary structure and convert to JSON
        dict_data = {"feature_t_s_run": valid_feature_ts_run_data}
        json_str = json.dumps(dict_data)

        reconstructed = FeatureTSRun()
        reconstructed.from_json(json_str)

        assert isinstance(reconstructed, FeatureTSRun)
        assert reconstructed.id == valid_feature_ts_run_data["id"]
        assert reconstructed.sample_rate == valid_feature_ts_run_data["sample_rate"]

    def test_round_trip_serialization(self, feature_ts_run_instance):
        """Test complete round-trip serialization."""
        # Dictionary round trip
        dict_data = feature_ts_run_instance.to_dict()
        reconstructed_from_dict = FeatureTSRun()
        reconstructed_from_dict.from_dict(dict_data)

        assert reconstructed_from_dict.id == feature_ts_run_instance.id
        assert (
            reconstructed_from_dict.sample_rate == feature_ts_run_instance.sample_rate
        )

        # JSON round trip
        json_str = feature_ts_run_instance.to_json()
        reconstructed_from_json = FeatureTSRun()
        reconstructed_from_json.from_json(json_str)

        assert reconstructed_from_json.id == feature_ts_run_instance.id
        assert (
            reconstructed_from_json.sample_rate == feature_ts_run_instance.sample_rate
        )


# Test class for edge cases and error handling
class TestFeatureTSRunEdgeCases:
    """Test FeatureTSRun edge cases and error handling."""

    def test_empty_initialization(self):
        """Test FeatureTSRun with no parameters."""
        feature_ts_run = FeatureTSRun()

        assert feature_ts_run.id == ""
        assert feature_ts_run.sample_rate == 0.0
        assert isinstance(feature_ts_run.comments, Comment)
        assert isinstance(feature_ts_run.time_period, TimePeriod)

    def test_partial_initialization(self):
        """Test FeatureTSRun with only some fields provided."""
        feature_ts_run = FeatureTSRun(id="partial_test", sample_rate=500.0)

        assert feature_ts_run.id == "partial_test"
        assert feature_ts_run.sample_rate == 500.0
        assert isinstance(feature_ts_run.comments, Comment)
        assert isinstance(feature_ts_run.time_period, TimePeriod)

    def test_extra_fields_handling(self):
        """Test FeatureTSRun handling of extra fields."""
        # MetadataBase is permissive and allows extra fields
        feature_ts_run = FeatureTSRun(
            id="test", sample_rate=1000.0, extra_field="should_be_allowed"
        )
        assert feature_ts_run.id == "test"
        assert feature_ts_run.sample_rate == 1000.0

    def test_type_coercion_behavior(self):
        """Test FeatureTSRun type coercion for compatible types."""
        # Integer to float conversion for sample_rate
        feature_ts_run = FeatureTSRun(sample_rate=1000)
        assert isinstance(feature_ts_run.sample_rate, float)
        assert feature_ts_run.sample_rate == 1000.0

    def test_field_access_and_modification(self, feature_ts_run_instance):
        """Test field access and modification after creation."""
        # Test field access
        assert hasattr(feature_ts_run_instance, "id")
        assert hasattr(feature_ts_run_instance, "sample_rate")
        assert hasattr(feature_ts_run_instance, "comments")
        assert hasattr(feature_ts_run_instance, "time_period")

        # Test field modification
        feature_ts_run_instance.id = "modified_id"
        assert feature_ts_run_instance.id == "modified_id"

        feature_ts_run_instance.sample_rate = 2000.0
        assert feature_ts_run_instance.sample_rate == 2000.0

    def test_equality_comparison(self, valid_feature_ts_run_data):
        """Test FeatureTSRun equality comparison."""
        feature_ts_run1 = FeatureTSRun(**valid_feature_ts_run_data)
        feature_ts_run2 = FeatureTSRun(**valid_feature_ts_run_data)

        assert feature_ts_run1.id == feature_ts_run2.id
        assert feature_ts_run1.sample_rate == feature_ts_run2.sample_rate

    def test_string_representation(self, feature_ts_run_instance):
        """Test FeatureTSRun string representation."""
        str_repr = str(feature_ts_run_instance)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0


# Test class for performance and integration
class TestFeatureTSRunPerformanceIntegration:
    """Test FeatureTSRun performance and integration scenarios."""

    def test_bulk_creation_performance(self, valid_feature_ts_run_data):
        """Test performance of creating multiple FeatureTSRun instances."""
        import time

        start_time = time.time()
        instances = []

        for i in range(100):
            data = valid_feature_ts_run_data.copy()
            data["id"] = f"test_run_{i:03d}"
            data["sample_rate"] = 1000.0 + i
            instances.append(FeatureTSRun(**data))

        end_time = time.time()
        creation_time = end_time - start_time

        assert len(instances) == 100
        assert creation_time < 1.0  # Should create 100 instances in less than 1 second

        # Verify all instances are properly created
        for i, instance in enumerate(instances):
            assert instance.id == f"test_run_{i:03d}"
            assert instance.sample_rate == 1000.0 + i

    def test_serialization_performance(self, feature_ts_run_instance):
        """Test serialization/deserialization performance."""
        import time

        # Test to_dict performance
        start_time = time.time()
        for _ in range(1000):
            feature_ts_run_instance.to_dict()
        dict_time = time.time() - start_time

        # Test to_json performance
        start_time = time.time()
        for _ in range(1000):
            feature_ts_run_instance.to_json()
        json_time = time.time() - start_time

        assert dict_time < 1.0  # 1000 to_dict calls in less than 1 second
        assert json_time < 2.0  # 1000 to_json calls in less than 2 seconds

    def test_field_validation_performance(self):
        """Test field validation performance."""
        import time

        valid_data = {
            "id": "performance_test_run",
            "sample_rate": 1000.0,
            "comments": "Performance test comment",
        }

        start_time = time.time()
        for i in range(1000):
            data = valid_data.copy()
            data["id"] = f"perf_test_{i}"
            FeatureTSRun(**data)
        validation_time = time.time() - start_time

        assert validation_time < 2.0  # 1000 validations in less than 2 seconds

    def test_memory_efficiency(self, valid_feature_ts_run_data):
        """Test memory efficiency of FeatureTSRun instances."""
        import sys

        # Create single instance and measure size
        instance = FeatureTSRun(**valid_feature_ts_run_data)
        instance_size = sys.getsizeof(instance)

        # Size should be reasonable (less than 1KB per instance)
        assert instance_size < 1024

        # Create multiple instances and verify memory doesn't grow excessively
        instances = []
        for i in range(10):
            data = valid_feature_ts_run_data.copy()
            data["id"] = f"memory_test_{i}"
            instances.append(FeatureTSRun(**data))

        total_size = sum(sys.getsizeof(inst) for inst in instances)
        average_size = total_size / len(instances)

        # Average size should be consistent and reasonable
        assert average_size < 1024
        assert len(instances) == 10


# Integration test for comprehensive validation
class TestFeatureTSRunComprehensiveIntegration:
    """Comprehensive integration tests for FeatureTSRun."""

    def test_complete_workflow_simulation(self):
        """Test complete workflow simulation with FeatureTSRun."""
        # Step 1: Create with minimal data
        feature_ts_run = FeatureTSRun(id="workflow_test")
        assert feature_ts_run.id == "workflow_test"

        # Step 2: Update sample rate
        feature_ts_run.sample_rate = 1000.0
        assert feature_ts_run.sample_rate == 1000.0

        # Step 3: Add comments
        feature_ts_run.comments = "Updated during workflow"
        assert isinstance(feature_ts_run.comments, Comment)
        assert feature_ts_run.comments.value == "Updated during workflow"

        # Step 4: Serialize to dictionary
        dict_data = feature_ts_run.to_dict()
        assert "feature_t_s_run" in dict_data

        # Step 5: Reconstruct from dictionary
        reconstructed = FeatureTSRun()
        reconstructed.from_dict(dict_data)
        assert reconstructed.id == "workflow_test"
        assert reconstructed.sample_rate == 1000.0
        assert reconstructed.comments.value == "Updated during workflow"

        # Step 6: JSON round trip
        json_str = reconstructed.to_json()
        final_instance = FeatureTSRun()
        final_instance.from_json(json_str)
        assert final_instance.id == "workflow_test"
        assert final_instance.sample_rate == 1000.0

    def test_complex_data_handling(self):
        """Test FeatureTSRun with complex nested data."""
        complex_data = {
            "id": "complex_test_run_001",
            "sample_rate": 44100.0,
            "comments": {
                "value": "Complex time series run with detailed metadata",
                "author": "test_researcher",
                "time_stamp": {"time_stamp": "2023-06-15T14:30:00+00:00"},
            },
            "time_period": {
                "start": {"time_stamp": "2023-06-15T10:00:00+00:00"},
                "end": {"time_stamp": "2023-06-15T18:00:00+00:00"},
            },
        }

        feature_ts_run = FeatureTSRun(**complex_data)

        # Verify all fields are properly processed
        assert feature_ts_run.id == "complex_test_run_001"
        assert feature_ts_run.sample_rate == 44100.0
        assert isinstance(feature_ts_run.comments, Comment)
        assert (
            feature_ts_run.comments.value
            == "Complex time series run with detailed metadata"
        )
        assert feature_ts_run.comments.author == "test_researcher"
        assert isinstance(feature_ts_run.time_period, TimePeriod)

        # Test serialization of complex data
        dict_result = feature_ts_run.to_dict()
        assert "feature_t_s_run" in dict_result

        # Test deserialization of complex data
        reconstructed = FeatureTSRun()
        reconstructed.from_dict(dict_result)
        assert reconstructed.id == complex_data["id"]
        assert reconstructed.sample_rate == complex_data["sample_rate"]
        assert reconstructed.comments.value == complex_data["comments"]["value"]
        assert reconstructed.comments.author == complex_data["comments"]["author"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
