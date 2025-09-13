"""
Test module for base_feature_basemodel.py
Comprehensive pytest suite using fixtures and subtests for efficiency.
"""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import xarray as xr
from pydantic import ValidationError

from mt_metadata.common import Comment
from mt_metadata.features.base_feature_basemodel import DomainEnum, Feature


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
def basic_feature():
    """Basic Feature instance with default values."""
    return Feature()


@pytest.fixture
def configured_feature():
    """Feature instance with configured values."""
    return Feature(
        name="test_feature",
        description="A test feature for unit testing",
        domain="time",
        comments=Comment(value="Test comment"),
    )


@pytest.fixture(
    params=[
        {"name": "coherence_feature", "domain": "frequency"},
        {"name": "time_feature", "domain": "time"},
        {"name": "fc_feature", "domain": "fc"},
    ]
)
def parametrized_feature_data(request):
    """Parametrized feature data for testing multiple configurations."""
    return request.param


@pytest.fixture
def invalid_data_types():
    """Invalid data types for testing data validation."""
    return [
        "string_data",
        123,
        [1, 2, 3],
        {"key": "value"},
        object(),
    ]


@pytest.fixture
def valid_comment_inputs():
    """Valid input types for comment validation."""
    return [
        "Simple string comment",
        Comment(value="Comment object"),
        Comment(value="Another comment", author="test_author"),
    ]


# ============================================================================
# TEST CLASSES
# ============================================================================


@pytest.mark.basics
class TestFeatureInstantiation:
    """Test Feature class instantiation and basic properties."""

    def test_default_instantiation(self, basic_feature):
        """Test Feature can be instantiated with default values."""
        assert isinstance(basic_feature, Feature)
        assert basic_feature.name == ""
        assert basic_feature.description == ""
        assert basic_feature.domain == DomainEnum.frequency
        assert basic_feature.data is None
        assert isinstance(basic_feature.comments, Comment)

    def test_configured_instantiation(self, configured_feature):
        """Test Feature instantiation with configured values."""
        assert configured_feature.name == "test_feature"
        assert configured_feature.description == "A test feature for unit testing"
        assert configured_feature.domain == DomainEnum.time
        assert isinstance(configured_feature.comments, Comment)

    def test_model_validate_instantiation(self):
        """Test Feature instantiation using model_validate."""
        data = {
            "name": "validated_feature",
            "description": "Feature created via model_validate",
            "domain": "frequency",
            "comments": "Test comment",
        }
        feature = Feature.model_validate(data)
        assert feature.name == "validated_feature"
        assert feature.domain == DomainEnum.frequency
        assert isinstance(feature.comments, Comment)

    @pytest.mark.parametrize(
        "domain_value", ["time", "frequency", "fc", "ts", "fourier"]
    )
    def test_domain_enum_values(self, domain_value):
        """Test all valid domain enum values."""
        feature = Feature(domain=domain_value)
        assert feature.domain.value == domain_value


@pytest.mark.validation
class TestFeatureValidation:
    """Test Feature field validation."""

    @pytest.mark.parametrize(
        "comment_input",
        [
            "Simple string",
            Comment(value="Comment object"),
        ],
    )
    def test_comments_validation_valid(self, comment_input):
        """Test valid comment input types."""
        feature = Feature(comments=comment_input)
        assert isinstance(feature.comments, Comment)
        if isinstance(comment_input, str):
            assert feature.comments.value == comment_input
        else:
            assert feature.comments.value == comment_input.value

    def test_comments_validation_with_subtests(self, valid_comment_inputs, subtests):
        """Test comment validation using subtests for efficiency."""
        for comment_input in valid_comment_inputs:
            with subtests.test(comment_input=comment_input):
                feature = Feature(comments=comment_input)
                assert isinstance(feature.comments, Comment)

    def test_data_validation_none(self):
        """Test data validation with None value."""
        feature = Feature(data=None)
        assert feature.data is None

    def test_data_validation_numpy(self, sample_numpy_data):
        """Test data validation with numpy array."""
        feature = Feature(data=sample_numpy_data)
        assert isinstance(feature.data, np.ndarray)
        np.testing.assert_array_equal(feature.data, sample_numpy_data)

    def test_data_validation_xarray_dataarray(self, sample_xr_dataarray):
        """Test data validation with xarray DataArray."""
        feature = Feature(data=sample_xr_dataarray)
        assert isinstance(feature.data, xr.DataArray)
        xr.testing.assert_equal(feature.data, sample_xr_dataarray)

    def test_data_validation_xarray_dataset(self, sample_xr_dataset):
        """Test data validation with xarray Dataset."""
        feature = Feature(data=sample_xr_dataset)
        assert isinstance(feature.data, xr.Dataset)
        xr.testing.assert_equal(feature.data, sample_xr_dataset)

    def test_data_validation_invalid_types(self, invalid_data_types, subtests):
        """Test data validation with invalid types using subtests."""
        for invalid_data in invalid_data_types:
            with subtests.test(invalid_data=invalid_data):
                with pytest.raises(
                    TypeError, match="Data must be a numpy array, xarray, or None"
                ):
                    Feature(data=invalid_data)

    def test_invalid_domain_value(self):
        """Test validation error for invalid domain value."""
        with pytest.raises(ValidationError):
            Feature(domain="invalid_domain")


@pytest.mark.data_handling
class TestFeatureDataHandling:
    """Test Feature data handling and manipulation."""

    def test_data_assignment_after_instantiation(
        self, basic_feature, sample_numpy_data
    ):
        """Test data assignment after Feature instantiation."""
        basic_feature.data = sample_numpy_data
        assert isinstance(basic_feature.data, np.ndarray)
        np.testing.assert_array_equal(basic_feature.data, sample_numpy_data)

    def test_data_replacement(
        self, configured_feature, sample_xr_dataarray, sample_numpy_data
    ):
        """Test replacing data with different types."""
        # Start with xarray
        configured_feature.data = sample_xr_dataarray
        assert isinstance(configured_feature.data, xr.DataArray)

        # Replace with numpy
        configured_feature.data = sample_numpy_data
        assert isinstance(configured_feature.data, np.ndarray)

        # Replace with None
        configured_feature.data = None
        assert configured_feature.data is None

    @pytest.mark.parametrize(
        "data_shape",
        [
            (5,),
            (3, 4),
            (2, 3, 4),
            (1, 2, 3, 4),
        ],
    )
    def test_numpy_data_shapes(self, data_shape):
        """Test Feature with numpy arrays of different shapes."""
        data = np.random.rand(*data_shape)
        feature = Feature(data=data)
        assert feature.data.shape == data_shape

    def test_xarray_with_coordinates(self):
        """Test Feature with xarray DataArray containing coordinates."""
        import pandas as pd

        times = pd.date_range("2023-01-01", periods=3, freq="H")
        freqs = np.logspace(0, 2, 4)
        data = np.random.rand(3, 4)

        da = xr.DataArray(
            data,
            coords={"time": times, "frequency": freqs},
            dims=["time", "frequency"],
            attrs={"units": "coherence", "method": "welch"},
        )

        feature = Feature(data=da)
        assert "time" in feature.data.coords
        assert "frequency" in feature.data.coords
        assert feature.data.attrs["units"] == "coherence"


@pytest.mark.factory
class TestFeatureFactory:
    """Test Feature factory methods."""

    def test_from_feature_id_missing_key(self):
        """Test from_feature_id with missing feature_id key."""
        meta_dict = {"name": "test", "description": "test feature"}
        with pytest.raises(
            KeyError, match="Feature metadata must include 'feature_id'"
        ):
            Feature.from_feature_id(meta_dict)

    def test_from_feature_id_unknown_id(self):
        """Test from_feature_id with unknown feature_id."""
        meta_dict = {"feature_id": "unknown_feature"}
        with pytest.raises(KeyError, match="Unknown feature_id 'unknown_feature'"):
            Feature.from_feature_id(meta_dict)

    @patch("mt_metadata.features.SUPPORTED_FEATURE_DICT", {"test_feature": MagicMock})
    def test_from_feature_id_success(self):
        """Test successful from_feature_id with mocked supported features."""
        # Create a mock feature class
        mock_feature_cls = MagicMock()
        mock_instance = MagicMock()
        mock_feature_cls.return_value = mock_instance

        meta_dict = {
            "feature_id": "test_feature",
            "name": "Test Feature",
            "description": "A test feature",
        }

        # Patch the SUPPORTED_FEATURE_DICT directly in the module
        with patch(
            "mt_metadata.features.base_feature_basemodel.SUPPORTED_FEATURE_DICT",
            {"test_feature": mock_feature_cls},
        ):
            result = Feature.from_feature_id(meta_dict)

            # Verify the factory worked correctly
            mock_feature_cls.assert_called_once()
            mock_instance.from_dict.assert_called_once_with(meta_dict)
            assert result == mock_instance

    def test_supported_features_dict_access(self, basic_feature):
        """Test access to supported features dictionary."""
        supported = basic_feature._supported_features
        assert isinstance(supported, dict)
        # Since SUPPORTED_FEATURE_DICT is empty in the test environment
        assert len(supported) == 0


@pytest.mark.properties
class TestFeatureProperties:
    """Test Feature properties and attributes."""

    def test_name_property(self, configured_feature):
        """Test name property access and modification."""
        assert configured_feature.name == "test_feature"
        configured_feature.name = "modified_name"
        assert configured_feature.name == "modified_name"

    def test_description_property(self, configured_feature):
        """Test description property access and modification."""
        original_desc = configured_feature.description
        assert original_desc == "A test feature for unit testing"

        new_desc = "Modified description"
        configured_feature.description = new_desc
        assert configured_feature.description == new_desc

    def test_domain_property(self, configured_feature):
        """Test domain property access and modification."""
        assert configured_feature.domain == DomainEnum.time
        configured_feature.domain = DomainEnum.frequency
        assert configured_feature.domain == DomainEnum.frequency

    def test_comments_property(self, basic_feature):
        """Test comments property access and modification."""
        assert isinstance(basic_feature.comments, Comment)

        new_comment = Comment(value="New comment")
        basic_feature.comments = new_comment
        assert basic_feature.comments.value == "New comment"


@pytest.mark.serialization
class TestFeatureSerialization:
    """Test Feature serialization and deserialization."""

    def test_model_dump(self, configured_feature):
        """Test model serialization to dictionary."""
        data = configured_feature.model_dump()
        assert isinstance(data, dict)
        assert data["name"] == "test_feature"
        assert data["domain"] == "time"
        assert "comments" in data

    def test_model_dump_exclude_none(self, basic_feature):
        """Test model serialization excluding None values."""
        data = basic_feature.model_dump(exclude_none=True)
        assert "data" not in data or data["data"] is None

    def test_roundtrip_serialization(self, configured_feature, sample_numpy_data):
        """Test roundtrip serialization: Feature -> dict -> Feature."""
        # Add some data
        configured_feature.data = sample_numpy_data

        # Serialize to dict (excluding data which can't be JSON serialized easily)
        data = configured_feature.model_dump(exclude={"data"})

        # Create new Feature from dict
        new_feature = Feature.model_validate(data)

        # Verify properties match
        assert new_feature.name == configured_feature.name
        assert new_feature.description == configured_feature.description
        assert new_feature.domain == configured_feature.domain

    def test_json_schema(self):
        """Test JSON schema generation."""
        schema = Feature.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "name" in schema["properties"]
        assert "domain" in schema["properties"]
        assert "data" in schema["properties"]
        assert "comments" in schema["properties"]


@pytest.mark.edge_cases
class TestFeatureEdgeCases:
    """Test Feature edge cases and error conditions."""

    def test_empty_string_values(self):
        """Test Feature with empty string values."""
        feature = Feature(name="", description="")
        assert feature.name == ""
        assert feature.description == ""

    def test_unicode_strings(self):
        """Test Feature with unicode strings."""
        feature = Feature(
            name="测试特征", description="A feature with émojis 🧪 and ñoñó characters"
        )
        assert "测试" in feature.name
        assert "émojis" in feature.description

    def test_very_large_numpy_array(self):
        """Test Feature with large numpy array."""
        large_data = np.zeros((1000, 1000))
        feature = Feature(data=large_data)
        assert feature.data.shape == (1000, 1000)
        assert feature.data.dtype == np.float64

    def test_mixed_data_types_in_dataset(self):
        """Test Feature with xarray Dataset containing mixed data types."""
        coords = {"time": range(3), "location": ["A", "B"]}

        dataset = xr.Dataset(
            {
                "temperature": (["time", "location"], np.random.rand(3, 2)),
                "humidity": (["time", "location"], np.random.randint(0, 100, (3, 2))),
                "status": (["location"], ["active", "inactive"]),
            },
            coords=coords,
        )

        feature = Feature(data=dataset)
        assert isinstance(feature.data, xr.Dataset)
        assert "temperature" in feature.data.data_vars
        assert "humidity" in feature.data.data_vars
        assert "status" in feature.data.data_vars


@pytest.mark.integration
class TestFeatureIntegration:
    """Integration tests for Feature class."""

    def test_complete_workflow(self, sample_numpy_data):
        """Test complete Feature workflow from creation to data assignment."""
        # Create Feature
        feature = Feature(
            name="integration_test",
            description="Feature for integration testing",
            domain="frequency",
        )

        # Verify initial state
        assert feature.name == "integration_test"
        assert feature.domain == DomainEnum.frequency
        assert feature.data is None

        # Add data
        feature.data = sample_numpy_data
        assert isinstance(feature.data, np.ndarray)

        # Modify properties
        feature.comments = Comment(value="Integration test completed")
        assert feature.comments.value == "Integration test completed"

        # Serialize and verify
        serialized = feature.model_dump(exclude={"data"})
        assert serialized["name"] == "integration_test"
        assert serialized["domain"] == "frequency"

    def test_feature_with_all_data_types(
        self, sample_numpy_data, sample_xr_dataarray, sample_xr_dataset
    ):
        """Test Feature with all supported data types in sequence."""
        feature = Feature(name="multi_data_test")

        # Test with numpy
        feature.data = sample_numpy_data
        assert isinstance(feature.data, np.ndarray)

        # Test with xarray DataArray
        feature.data = sample_xr_dataarray
        assert isinstance(feature.data, xr.DataArray)

        # Test with xarray Dataset
        feature.data = sample_xr_dataset
        assert isinstance(feature.data, xr.Dataset)

        # Test with None
        feature.data = None
        assert feature.data is None

    @pytest.mark.parametrize("domain", list(DomainEnum))
    def test_all_domain_values_integration(self, domain):
        """Integration test with all domain enum values."""
        feature = Feature(
            name=f"test_{domain.value}",
            description=f"Feature in {domain.value} domain",
            domain=domain,
        )
        assert feature.domain == domain
        assert feature.name == f"test_{domain.value}"


# ============================================================================
# UTILITY TESTS
# ============================================================================


@pytest.mark.utils
class TestDomainEnum:
    """Test DomainEnum utility class."""

    def test_domain_enum_values(self):
        """Test all domain enum values are accessible."""
        expected_values = ["time", "frequency", "fc", "ts", "fourier"]
        actual_values = [domain.value for domain in DomainEnum]
        assert set(actual_values) == set(expected_values)

    def test_domain_enum_string_representation(self):
        """Test domain enum string representation."""
        assert DomainEnum.frequency.value == "frequency"
        assert DomainEnum.time.value == "time"

    @pytest.mark.parametrize("enum_value", list(DomainEnum))
    def test_domain_enum_equality(self, enum_value):
        """Test domain enum equality with string values."""
        assert enum_value.value in ["time", "frequency", "fc", "ts", "fourier"]


# ============================================================================
# NOTE: Performance tests would require pytest-benchmark plugin
# Uncomment when pytest-benchmark is available in the environment
# ============================================================================

# @pytest.mark.performance
# class TestFeaturePerformance:
#     """Performance tests for Feature class."""
#
#     def test_instantiation_performance(self, benchmark):
#         """Benchmark Feature instantiation performance."""
#         def create_feature():
#             return Feature(
#                 name="performance_test",
#                 description="Testing performance",
#                 domain="frequency"
#             )
#
#         result = benchmark(create_feature)
#         assert isinstance(result, Feature)
#
#     def test_data_assignment_performance(self, benchmark, basic_feature):
#         """Benchmark data assignment performance."""
#         large_data = np.random.rand(1000, 100)
#
#         def assign_data():
#             basic_feature.data = large_data
#             return basic_feature.data
#
#         result = benchmark(assign_data)
#         assert isinstance(result, np.ndarray)
#
#     def test_serialization_performance(self, benchmark, configured_feature):
#         """Benchmark serialization performance."""
#         def serialize_feature():
#             return configured_feature.model_dump()
#
#         result = benchmark(serialize_feature)
#         assert isinstance(result, dict)
