"""
Test module for feature_fc.py
Comprehensive pytest suite using fixtures and subtests for efficiency.
"""

import numpy as np
import pytest
import xarray as xr

from mt_metadata.common import Comment
from mt_metadata.features.base_feature_basemodel import DomainEnum, Feature
from mt_metadata.features.feature_fc import FeatureFC


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
def default_feature_fc():
    """Default FeatureFC instance for testing."""
    return FeatureFC()


@pytest.fixture
def custom_comment():
    """Custom Comment object for testing."""
    return Comment(value="Test comment", author="Test Author")


@pytest.fixture
def feature_fc_config():
    """Complete FeatureFC configuration for testing."""
    return {
        "name": "custom_fc",
        "description": "Custom FC feature description",
        "domain": "time",
        "comments": "Custom comment",
        "data": np.array([1, 2, 3, 4, 5]),
    }


# ============================================================================
# TEST CLASSES
# ============================================================================


class TestFeatureFCInitialization:
    """Test class for FeatureFC initialization and default behavior."""

    def test_default_initialization(self, default_feature_fc):
        """Test FeatureFC default initialization."""
        assert isinstance(default_feature_fc, FeatureFC)
        assert isinstance(default_feature_fc, Feature)

    def test_model_validator_sets_defaults(self, default_feature_fc):
        """Test that model validator sets correct default values."""
        assert default_feature_fc.name == "feature_fc"
        assert (
            default_feature_fc.description
            == "A feature for storing feature_fc information."
        )
        assert default_feature_fc.domain == DomainEnum.frequency

    def test_inheritance_from_feature(self, default_feature_fc):
        """Test that FeatureFC properly inherits from Feature class."""
        # Check that all Feature fields are present
        assert hasattr(default_feature_fc, "name")
        assert hasattr(default_feature_fc, "description")
        assert hasattr(default_feature_fc, "domain")
        assert hasattr(default_feature_fc, "comments")
        assert hasattr(default_feature_fc, "data")

    def test_default_field_values(self, default_feature_fc):
        """Test that default field values are properly set."""
        assert default_feature_fc.name == "feature_fc"
        assert (
            default_feature_fc.description
            == "A feature for storing feature_fc information."
        )
        assert default_feature_fc.domain == DomainEnum.frequency
        assert isinstance(default_feature_fc.comments, Comment)
        assert default_feature_fc.data is None


class TestFeatureFCModelValidator:
    """Test class for FeatureFC model validator functionality."""

    def test_set_defaults_validator(self):
        """Test the set_defaults model validator."""
        # Test with empty dict
        fc = FeatureFC()
        assert fc.name == "feature_fc"
        assert fc.description == "A feature for storing feature_fc information."
        assert fc.domain == DomainEnum.frequency

    def test_set_defaults_with_custom_values(self):
        """Test set_defaults validator with custom input values."""
        # Custom values should be overridden by the validator
        fc = FeatureFC(
            name="custom_name", description="custom description", domain="time"
        )
        assert fc.name == "feature_fc"  # Should be overridden
        assert (
            fc.description == "A feature for storing feature_fc information."
        )  # Should be overridden
        assert fc.domain == DomainEnum.frequency  # Should be overridden

    def test_validator_preserves_other_fields(self):
        """Test that validator preserves non-default fields."""
        fc = FeatureFC(comments="Custom comment", data=np.array([1, 2, 3]))
        assert fc.name == "feature_fc"
        assert fc.description == "A feature for storing feature_fc information."
        assert fc.domain == DomainEnum.frequency
        assert isinstance(fc.data, np.ndarray) and np.array_equal(
            fc.data, np.array([1, 2, 3])
        )


class TestFeatureFCFieldValidation:
    """Test class for FeatureFC field validation functionality."""

    def test_comments_field_validation(self):
        """Test comments field validator converts string to Comment."""
        fc = FeatureFC(comments="Test comment string")
        assert isinstance(fc.comments, Comment)
        assert fc.comments.value == "Test comment string"

    def test_comments_object_validation(self, custom_comment):
        """Test comments field accepts Comment objects."""
        fc = FeatureFC(comments=custom_comment)
        assert isinstance(fc.comments, Comment)
        assert fc.comments.value == "Test comment"
        assert fc.comments.author == "Test Author"

    def test_data_field_numpy_validation(self, sample_numpy_data):
        """Test data field accepts numpy arrays."""
        fc = FeatureFC(data=sample_numpy_data)
        assert isinstance(fc.data, np.ndarray)
        assert np.array_equal(fc.data, sample_numpy_data)

    def test_data_field_xarray_dataarray_validation(self, sample_xr_dataarray):
        """Test data field accepts xarray DataArray."""
        fc = FeatureFC(data=sample_xr_dataarray)
        assert isinstance(fc.data, xr.DataArray)
        assert fc.data.equals(sample_xr_dataarray)

    def test_data_field_xarray_dataset_validation(self, sample_xr_dataset):
        """Test data field accepts xarray Dataset."""
        fc = FeatureFC(data=sample_xr_dataset)
        assert isinstance(fc.data, xr.Dataset)
        assert fc.data.equals(sample_xr_dataset)

    def test_data_field_none_validation(self):
        """Test data field accepts None values."""
        fc = FeatureFC(data=None)
        assert fc.data is None

    def test_data_field_invalid_type_rejection(self):
        """Test data field rejects invalid types."""
        with pytest.raises(TypeError) as exc_info:
            FeatureFC(data="invalid_string_data")
        assert "Data must be a numpy array, xarray, or None" in str(exc_info.value)

        with pytest.raises(TypeError) as exc_info:
            FeatureFC(data=[1, 2, 3])  # List is not allowed
        assert "Data must be a numpy array, xarray, or None" in str(exc_info.value)


class TestFeatureFCDomainEnum:
    """Test class for domain field enum validation."""

    @pytest.mark.parametrize(
        "domain_value,expected",
        [
            ("time", DomainEnum.time),
            ("frequency", DomainEnum.frequency),
            ("fc", DomainEnum.fc),
            ("ts", DomainEnum.ts),
            ("fourier", DomainEnum.fourier),
        ],
    )
    def test_valid_domain_values(self, domain_value, expected):
        """Test valid domain enum values."""
        # Test that the enum itself accepts these values
        assert DomainEnum(domain_value) == expected

    def test_invalid_domain_value_rejection(self):
        """Test invalid domain values are rejected."""
        with pytest.raises(ValueError):
            DomainEnum("invalid_domain")


class TestFeatureFCIntegration:
    """Test class for FeatureFC integration and comprehensive functionality."""

    def test_full_configuration(self, feature_fc_config):
        """Test FeatureFC with full configuration."""
        fc = FeatureFC(**feature_fc_config)
        # Model validator should override name, description, domain
        assert fc.name == "feature_fc"
        assert fc.description == "A feature for storing feature_fc information."
        assert fc.domain == DomainEnum.frequency
        assert fc.comments.value == "Custom comment"
        assert isinstance(fc.data, np.ndarray) and np.array_equal(
            fc.data, np.array([1, 2, 3, 4, 5])
        )

    def test_serialization_deserialization(self, default_feature_fc):
        """Test FeatureFC serialization and deserialization."""
        # Test to_dict
        fc_dict = default_feature_fc.to_dict()
        assert isinstance(fc_dict, dict)
        assert fc_dict["feature_f_c"]["name"] == "feature_fc"
        assert (
            fc_dict["feature_f_c"]["description"]
            == "A feature for storing feature_fc information."
        )
        assert fc_dict["feature_f_c"]["domain"] == "frequency"

        # Test from_dict
        new_fc = FeatureFC()
        new_fc.from_dict(fc_dict)
        assert new_fc.name == default_feature_fc.name
        assert new_fc.description == default_feature_fc.description
        assert new_fc.domain == default_feature_fc.domain

    def test_copy_and_modification(self, default_feature_fc):
        """Test copying and modifying FeatureFC instances."""
        fc_copy = default_feature_fc.model_copy()
        assert fc_copy.name == default_feature_fc.name
        assert fc_copy.description == default_feature_fc.description
        assert fc_copy.domain == default_feature_fc.domain

        # Modify copy
        fc_copy.comments = Comment(value="Modified comment")
        assert fc_copy.comments.value == "Modified comment"
        assert default_feature_fc.comments.value is None  # Original unchanged

    def test_equality_comparison(self):
        """Test FeatureFC equality comparison."""
        fc1 = FeatureFC()
        fc2 = FeatureFC()

        # Default instances should be equal
        assert fc1.name == fc2.name
        assert fc1.description == fc2.description
        assert fc1.domain == fc2.domain

        # Modify one instance
        fc2.comments = Comment(value="Different comment")
        assert fc1.comments.value != fc2.comments.value

    def test_comprehensive_validation(self, sample_numpy_data, custom_comment):
        """Test comprehensive FeatureFC validation with all fields."""
        fc = FeatureFC(comments=custom_comment, data=sample_numpy_data)

        # Verify all fields
        assert fc.name == "feature_fc"
        assert fc.description == "A feature for storing feature_fc information."
        assert fc.domain == DomainEnum.frequency
        assert fc.comments.value == "Test comment"
        assert fc.comments.author == "Test Author"
        assert isinstance(fc.data, np.ndarray) and np.array_equal(
            fc.data, sample_numpy_data
        )

    def test_error_handling_and_edge_cases(self):
        """Test error handling and edge cases."""
        # Test with empty comment string
        fc = FeatureFC(comments="")
        assert fc.comments.value == ""

        # Test with whitespace comment
        fc = FeatureFC(comments="   ")
        assert fc.comments.value == "   "

        # Test with unicode comment
        fc = FeatureFC(comments="测试评论")
        assert fc.comments.value == "测试评论"


class TestFeatureFCFactoryMethods:
    """Test class for FeatureFC factory methods and class methods."""

    def test_from_feature_id_method(self):
        """Test from_feature_id factory method."""
        # This tests the inherited factory method
        meta_dict = {
            "feature_id": "feature_fc",
            "name": "test_feature",
            "description": "test description",
            "domain": "time",
        }

        # Mock the SUPPORTED_FEATURE_DICT to include feature_fc
        with pytest.raises(KeyError):
            # Should raise KeyError if feature_fc not in supported dict
            FeatureFC.from_feature_id(meta_dict)

    def test_from_feature_id_missing_id(self):
        """Test from_feature_id with missing feature_id."""
        meta_dict = {"name": "test_feature", "description": "test description"}

        with pytest.raises(KeyError) as exc_info:
            FeatureFC.from_feature_id(meta_dict)
        assert "Feature metadata must include 'feature_id'" in str(exc_info.value)

    def test_supported_features_attribute(self, default_feature_fc):
        """Test _supported_features private attribute."""
        # This tests the inherited private attribute
        assert hasattr(default_feature_fc, "_supported_features")
        assert isinstance(default_feature_fc._supported_features, dict)


class TestFeatureFCEdgeCases:
    """Test class for FeatureFC edge cases and boundary conditions."""

    def test_large_numpy_array_data(self):
        """Test with large numpy array data."""
        large_data = np.random.rand(1000, 1000)
        fc = FeatureFC(data=large_data)
        assert isinstance(fc.data, np.ndarray)
        assert fc.data.shape == (1000, 1000)

    def test_complex_numpy_array_data(self):
        """Test with complex numpy array data."""
        complex_data = np.random.rand(10, 5) + 1j * np.random.rand(10, 5)
        fc = FeatureFC(data=complex_data)
        assert isinstance(fc.data, np.ndarray)
        assert fc.data.dtype == complex

    def test_empty_numpy_array_data(self):
        """Test with empty numpy array data."""
        empty_data = np.array([])
        fc = FeatureFC(data=empty_data)
        assert isinstance(fc.data, np.ndarray)
        assert fc.data.size == 0

    def test_multidimensional_xarray_data(self):
        """Test with multidimensional xarray data."""
        data = np.random.rand(5, 4, 3, 2)
        coords = {
            "time": range(5),
            "frequency": range(4),
            "channel": range(3),
            "component": range(2),
        }
        da = xr.DataArray(
            data, coords=coords, dims=["time", "frequency", "channel", "component"]
        )

        fc = FeatureFC(data=da)
        assert isinstance(fc.data, xr.DataArray)
        assert fc.data.dims == ("time", "frequency", "channel", "component")

    def test_very_long_comment_string(self):
        """Test with very long comment string."""
        long_comment = "a" * 10000  # 10,000 character comment
        fc = FeatureFC(comments=long_comment)
        assert fc.comments.value == long_comment
        assert len(fc.comments.value) == 10000

    def test_special_characters_in_comment(self):
        """Test comment with special characters."""
        special_comment = "Comment with 🔬 emojis and special chars: àáâãäåæç ñ ø"
        fc = FeatureFC(comments=special_comment)
        assert fc.comments.value == special_comment
