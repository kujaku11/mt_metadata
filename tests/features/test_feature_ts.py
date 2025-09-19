"""
Test module for feature_ts.py
Comprehensive pytest suite using fixtures and subtests for efficiency.
"""

import numpy as np
import pytest
import xarray as xr

from mt_metadata.common import Comment
from mt_metadata.features.feature import DomainEnum, Feature
from mt_metadata.features.feature_ts import FeatureTS


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def sample_numpy_data():
    """Sample numpy array for testing data validation."""
    return np.random.rand(10, 5)


@pytest.fixture(scope="session")
def sample_xr_dataarray():
    """Sample xarray DataArray for testing data validation."""
    data = np.random.rand(3, 4)
    coords = {"time": range(3), "frequency": range(4)}
    return xr.DataArray(data, coords=coords, dims=["time", "frequency"])


@pytest.fixture(scope="session")
def sample_xr_dataset():
    """Sample xarray Dataset for testing data validation."""
    data1 = np.random.rand(3, 4)
    data2 = np.random.rand(3, 4)
    coords = {"time": range(3), "frequency": range(4)}
    return xr.Dataset(
        {
            "var1": (["time", "frequency"], data1),
            "var2": (["time", "frequency"], data2),
        },
        coords=coords,
    )


@pytest.fixture
def default_feature_ts():
    """Default FeatureTS instance for testing."""
    return FeatureTS()


@pytest.fixture
def custom_comment():
    """Custom Comment object for testing."""
    return Comment(value="Test comment", author="Test Author")


@pytest.fixture
def feature_ts_config():
    """Complete FeatureTS configuration for testing."""
    return {
        "name": "custom_ts",
        "description": "Custom TS feature description",
        "domain": "frequency",
        "comments": "Custom comment",
        "data": np.array([1, 2, 3, 4, 5]),
    }


# ============================================================================
# TEST CLASSES
# ============================================================================


class TestFeatureTSInitialization:
    """Test class for FeatureTS initialization and default behavior."""

    def test_default_initialization(self, default_feature_ts):
        """Test FeatureTS default initialization."""
        assert isinstance(default_feature_ts, FeatureTS)
        assert isinstance(default_feature_ts, Feature)

    def test_model_validator_sets_defaults(self, default_feature_ts):
        """Test that model validator sets correct default values."""
        assert default_feature_ts.name == "feature_ts"
        assert (
            default_feature_ts.description
            == "A feature for storing time series information."
        )
        assert default_feature_ts.domain == DomainEnum.time

    def test_inheritance_from_feature(self, default_feature_ts):
        """Test that FeatureTS properly inherits from Feature class."""
        # Check that all Feature fields are present
        assert hasattr(default_feature_ts, "name")
        assert hasattr(default_feature_ts, "description")
        assert hasattr(default_feature_ts, "domain")
        assert hasattr(default_feature_ts, "comments")
        assert hasattr(default_feature_ts, "data")

    def test_default_field_values(self, default_feature_ts):
        """Test that default field values are properly set."""
        assert default_feature_ts.name == "feature_ts"
        assert (
            default_feature_ts.description
            == "A feature for storing time series information."
        )
        assert default_feature_ts.domain == DomainEnum.time
        assert isinstance(default_feature_ts.comments, Comment)
        assert default_feature_ts.data is None


class TestFeatureTSModelValidator:
    """Test class for FeatureTS model validator functionality."""

    def test_set_defaults_validator(self):
        """Test the set_defaults model validator."""
        # Test with empty dict
        ts = FeatureTS()
        assert ts.name == "feature_ts"
        assert ts.description == "A feature for storing time series information."
        assert ts.domain == DomainEnum.time

    def test_set_defaults_with_custom_values(self):
        """Test set_defaults validator with custom input values."""
        # Custom values should be overridden by the validator
        ts = FeatureTS(
            name="custom_name", description="custom description", domain="frequency"
        )
        assert ts.name == "feature_ts"  # Should be overridden
        assert (
            ts.description == "A feature for storing time series information."
        )  # Should be overridden
        assert ts.domain == DomainEnum.time  # Should be overridden

    def test_validator_preserves_other_fields(self):
        """Test that validator preserves non-default fields."""
        ts = FeatureTS(comments="Custom comment", data=np.array([1, 2, 3]))
        assert ts.name == "feature_ts"
        assert ts.description == "A feature for storing time series information."
        assert ts.domain == DomainEnum.time
        assert ts.comments.value == "Custom comment"
        assert isinstance(ts.data, np.ndarray) and np.array_equal(
            ts.data, np.array([1, 2, 3])
        )


class TestFeatureTSFieldValidation:
    """Test class for FeatureTS field validation functionality."""

    def test_comments_field_validation(self):
        """Test comments field validator converts string to Comment."""
        ts = FeatureTS(comments="Test comment string")
        assert isinstance(ts.comments, Comment)
        assert ts.comments.value == "Test comment string"

    def test_comments_object_validation(self, custom_comment):
        """Test comments field accepts Comment objects."""
        ts = FeatureTS(comments=custom_comment)
        assert isinstance(ts.comments, Comment)
        assert ts.comments.value == "Test comment"
        assert ts.comments.author == "Test Author"

    def test_data_field_numpy_validation(self, sample_numpy_data):
        """Test data field accepts numpy arrays."""
        ts = FeatureTS(data=sample_numpy_data)
        assert isinstance(ts.data, np.ndarray)
        assert np.array_equal(ts.data, sample_numpy_data)

    def test_data_field_xarray_dataarray_validation(self, sample_xr_dataarray):
        """Test data field accepts xarray DataArray."""
        ts = FeatureTS(data=sample_xr_dataarray)
        assert isinstance(ts.data, xr.DataArray)
        assert ts.data.equals(sample_xr_dataarray)

    def test_data_field_xarray_dataset_validation(self, sample_xr_dataset):
        """Test data field accepts xarray Dataset."""
        ts = FeatureTS(data=sample_xr_dataset)
        assert isinstance(ts.data, xr.Dataset)
        assert ts.data.equals(sample_xr_dataset)

    def test_data_field_none_validation(self):
        """Test data field accepts None values."""
        ts = FeatureTS(data=None)
        assert ts.data is None

    def test_data_field_invalid_type_rejection(self):
        """Test data field rejects invalid types."""
        with pytest.raises(TypeError) as exc_info:
            FeatureTS(data="invalid_string_data")
        assert "Data must be a numpy array, xarray, or None" in str(exc_info.value)

        with pytest.raises(TypeError) as exc_info:
            FeatureTS(data=[1, 2, 3])  # List is not allowed
        assert "Data must be a numpy array, xarray, or None" in str(exc_info.value)


class TestFeatureTSDomainBehavior:
    """Test class for FeatureTS domain field behavior."""

    def test_default_domain_is_time(self):
        """Test that FeatureTS defaults to time domain."""
        ts = FeatureTS()
        assert ts.domain == DomainEnum.time

    def test_domain_override_behavior(self):
        """Test that domain is always overridden to time by model validator."""
        # Even if we try to set a different domain, it should be overridden
        ts = FeatureTS(domain="frequency")
        assert ts.domain == DomainEnum.time

        ts = FeatureTS(domain="fc")
        assert ts.domain == DomainEnum.time

    @pytest.mark.parametrize("domain_value", ["frequency", "fc", "ts", "fourier"])
    def test_domain_always_overridden_to_time(self, domain_value):
        """Test that any domain value is overridden to time."""
        ts = FeatureTS(domain=domain_value)
        assert ts.domain == DomainEnum.time


class TestFeatureTSIntegration:
    """Test class for FeatureTS integration and comprehensive functionality."""

    def test_full_configuration(self, feature_ts_config):
        """Test FeatureTS with full configuration."""
        ts = FeatureTS(**feature_ts_config)
        # Model validator should override name, description, domain
        assert ts.name == "feature_ts"
        assert ts.description == "A feature for storing time series information."
        assert ts.domain == DomainEnum.time
        assert ts.comments.value == "Custom comment"
        assert isinstance(ts.data, np.ndarray) and np.array_equal(
            ts.data, np.array([1, 2, 3, 4, 5])
        )

    def test_serialization_deserialization(self, default_feature_ts):
        """Test FeatureTS serialization and deserialization."""
        # Test to_dict
        ts_dict = default_feature_ts.to_dict()
        assert isinstance(ts_dict, dict)
        # The key should be 'feature_t_s' based on the class name conversion
        assert "feature_t_s" in ts_dict
        assert ts_dict["feature_t_s"]["name"] == "feature_ts"
        assert (
            ts_dict["feature_t_s"]["description"]
            == "A feature for storing time series information."
        )
        assert ts_dict["feature_t_s"]["domain"] == "time"

        # Test from_dict
        new_ts = FeatureTS()
        new_ts.from_dict(ts_dict)
        assert new_ts.name == default_feature_ts.name
        assert new_ts.description == default_feature_ts.description
        assert new_ts.domain == default_feature_ts.domain

    def test_copy_and_modification(self, default_feature_ts):
        """Test copying and modifying FeatureTS instances."""
        ts_copy = default_feature_ts.model_copy()
        assert ts_copy.name == default_feature_ts.name
        assert ts_copy.description == default_feature_ts.description
        assert ts_copy.domain == default_feature_ts.domain

        # Modify copy
        ts_copy.comments = Comment(value="Modified comment")
        assert ts_copy.comments.value == "Modified comment"
        assert default_feature_ts.comments.value is None  # Original unchanged

    def test_equality_comparison(self):
        """Test FeatureTS equality comparison."""
        ts1 = FeatureTS()
        ts2 = FeatureTS()

        # Default instances should be equal
        assert ts1.name == ts2.name
        assert ts1.description == ts2.description
        assert ts1.domain == ts2.domain

        # Modify one instance
        ts2.comments = Comment(value="Different comment")
        assert ts1.comments.value != ts2.comments.value

    def test_comprehensive_validation(self, sample_numpy_data, custom_comment):
        """Test comprehensive FeatureTS validation with all fields."""
        ts = FeatureTS(comments=custom_comment, data=sample_numpy_data)

        # Verify all fields
        assert ts.name == "feature_ts"
        assert ts.description == "A feature for storing time series information."
        assert ts.domain == DomainEnum.time
        assert ts.comments.value == "Test comment"
        assert ts.comments.author == "Test Author"
        assert isinstance(ts.data, np.ndarray) and np.array_equal(
            ts.data, sample_numpy_data
        )

    def test_error_handling_and_edge_cases(self):
        """Test error handling and edge cases."""
        # Test with empty comment string
        ts = FeatureTS(comments="")
        assert ts.comments.value == ""

        # Test with whitespace comment
        ts = FeatureTS(comments="   ")
        assert ts.comments.value == "   "

        # Test with unicode comment
        ts = FeatureTS(comments="测试时序评论")
        assert ts.comments.value == "测试时序评论"


class TestFeatureTSFactoryMethods:
    """Test class for FeatureTS factory methods and class methods."""

    def test_from_feature_id_method(self):
        """Test from_feature_id factory method."""
        # This tests the inherited factory method
        meta_dict = {
            "feature_id": "feature_ts",
            "name": "test_feature",
            "description": "test description",
            "domain": "frequency",
        }

        # Now feature_ts is in SUPPORTED_FEATURE_DICT, so it should work
        result = FeatureTS.from_feature_id(meta_dict)

        # Verify the factory method returns a FeatureTS instance
        # Note: FeatureTS's set_defaults validator overrides name and description,
        # but domain can be set from meta_dict
        assert isinstance(result, FeatureTS)
        assert result.name == "feature_ts"  # Always set by set_defaults validator
        assert (
            result.description == "A feature for storing time series information."
        )  # Always set by set_defaults validator
        assert result.domain == "frequency"  # Can be overridden by from_dict

    def test_from_feature_id_missing_id(self):
        """Test from_feature_id with missing feature_id."""
        meta_dict = {"name": "test_feature", "description": "test description"}

        with pytest.raises(KeyError) as exc_info:
            FeatureTS.from_feature_id(meta_dict)
        assert "Feature metadata must include 'feature_id'" in str(exc_info.value)

    def test_supported_features_attribute(self, default_feature_ts):
        """Test _supported_features private attribute."""
        # This tests the inherited private attribute
        assert hasattr(default_feature_ts, "_supported_features")
        assert isinstance(default_feature_ts._supported_features, dict)


class TestFeatureTSComparisonWithFC:
    """Test class to compare FeatureTS with FeatureFC behavior."""

    def test_different_default_domains(self):
        """Test that TS and FC have different default domains."""
        from mt_metadata.features.feature_fc import FeatureFC

        ts = FeatureTS()
        fc = FeatureFC()

        assert ts.domain == DomainEnum.time
        assert fc.domain == DomainEnum.frequency
        assert ts.domain != fc.domain

    def test_different_default_names(self):
        """Test that TS and FC have different default names."""
        from mt_metadata.features.feature_fc import FeatureFC

        ts = FeatureTS()
        fc = FeatureFC()

        assert ts.name == "feature_ts"
        assert fc.name == "feature_fc"
        assert ts.name != fc.name

    def test_different_default_descriptions(self):
        """Test that TS and FC have different default descriptions."""
        from mt_metadata.features.feature_fc import FeatureFC

        ts = FeatureTS()
        fc = FeatureFC()

        assert "time series" in ts.description
        assert "feature_fc" in fc.description
        assert ts.description != fc.description


class TestFeatureTSEdgeCases:
    """Test class for FeatureTS edge cases and boundary conditions."""

    def test_large_numpy_array_data(self):
        """Test with large numpy array data."""
        large_data = np.random.rand(1000, 1000)
        ts = FeatureTS(data=large_data)
        assert isinstance(ts.data, np.ndarray)
        assert ts.data.shape == (1000, 1000)

    def test_complex_numpy_array_data(self):
        """Test with complex numpy array data."""
        complex_data = np.random.rand(10, 5) + 1j * np.random.rand(10, 5)
        ts = FeatureTS(data=complex_data)
        assert isinstance(ts.data, np.ndarray)
        assert ts.data.dtype == complex

    def test_empty_numpy_array_data(self):
        """Test with empty numpy array data."""
        empty_data = np.array([])
        ts = FeatureTS(data=empty_data)
        assert isinstance(ts.data, np.ndarray)
        assert ts.data.size == 0

    def test_time_series_specific_xarray_data(self):
        """Test with time series specific xarray data."""
        # Create time series data with time dimension
        times = np.arange("2023-01-01", "2023-01-11", dtype="datetime64[D]")
        data = np.random.rand(len(times), 3)  # 10 days, 3 channels
        coords = {"time": times, "channel": ["Ex", "Ey", "Hz"]}
        da = xr.DataArray(data, coords=coords, dims=["time", "channel"])

        ts = FeatureTS(data=da)
        assert isinstance(ts.data, xr.DataArray)
        assert "time" in ts.data.dims
        assert ts.data.dims == ("time", "channel")

    def test_very_long_comment_string(self):
        """Test with very long comment string."""
        long_comment = "a" * 10000  # 10,000 character comment
        ts = FeatureTS(comments=long_comment)
        assert ts.comments.value == long_comment
        assert len(ts.comments.value) == 10000

    def test_special_characters_in_comment(self):
        """Test comment with special characters."""
        special_comment = "时序数据 with 🕐 emojis and special chars: àáâãäåæç ñ ø"
        ts = FeatureTS(comments=special_comment)
        assert ts.comments.value == special_comment

    def test_zero_dimensional_numpy_array(self):
        """Test with zero-dimensional numpy array."""
        zero_d_data = np.array(42.0)
        ts = FeatureTS(data=zero_d_data)
        assert isinstance(ts.data, np.ndarray)
        assert ts.data.ndim == 0
        assert ts.data.item() == 42.0


class TestFeatureTSPerformance:
    """Test class for FeatureTS performance and efficiency."""

    def test_bulk_instantiation_performance(self):
        """Test performance of creating multiple FeatureTS instances."""
        instances = []
        for i in range(100):
            ts = FeatureTS(comments=f"Comment {i}")
            instances.append(ts)

        assert len(instances) == 100
        assert all(isinstance(ts, FeatureTS) for ts in instances)
        assert all(ts.domain == DomainEnum.time for ts in instances)

    def test_large_data_handling(self):
        """Test handling of large data arrays."""
        # Test with different large data types
        large_1d = np.random.rand(100000)
        large_2d = np.random.rand(1000, 100)
        large_3d = np.random.rand(100, 50, 20)

        ts1 = FeatureTS(data=large_1d)
        ts2 = FeatureTS(data=large_2d)
        ts3 = FeatureTS(data=large_3d)

        assert ts1.data.shape == (100000,)
        assert ts2.data.shape == (1000, 100)
        assert ts3.data.shape == (100, 50, 20)

    def test_serialization_performance(self):
        """Test serialization performance with various data sizes."""
        # Test serialization with different data sizes
        small_data = np.random.rand(10)
        medium_data = np.random.rand(1000)

        ts_small = FeatureTS(data=small_data, comments="Small dataset")
        ts_medium = FeatureTS(data=medium_data, comments="Medium dataset")

        # Test that serialization works (performance is implicit)
        dict_small = ts_small.to_dict()
        dict_medium = ts_medium.to_dict()

        assert isinstance(dict_small, dict)
        assert isinstance(dict_medium, dict)
        assert "feature_t_s" in dict_small
        assert "feature_t_s" in dict_medium
