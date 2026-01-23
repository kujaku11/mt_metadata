"""
Test module for feature.py
Comprehensive pytest suite using fixtures and subtests for efficiency.
"""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import xarray as xr
from pydantic import ValidationError

from mt_metadata.common import Comment
from mt_metadata.features.cross_powers import CrossPowers
from mt_metadata.features.feature import DomainEnum, Feature

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
    # Return factory functions instead of objects to avoid serialization issues
    return [
        "string_data",
        123,
        [1, 2, 3],
        {"key": "value"},
        "object_placeholder",  # Will be replaced with object() in tests
    ]


@pytest.fixture
def valid_comment_inputs():
    """Valid input types for comment validation."""
    # Return data to create Comment objects in tests to avoid serialization issues
    return [
        "Simple string comment",
        {"type": "comment", "value": "Comment object"},
        {"type": "comment", "value": "Another comment", "author": "test_author"},
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
        for comment_data in valid_comment_inputs:
            # Create Comment objects locally to avoid serialization issues
            if isinstance(comment_data, dict) and comment_data.get("type") == "comment":
                comment_input = Comment(
                    value=comment_data["value"], author=comment_data.get("author")
                )
                test_key = f"Comment({comment_data['value'][:20]}...)"
            else:
                comment_input = comment_data
                test_key = str(comment_data)

            with subtests.test(comment_input=test_key):
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
            # Create object() locally to avoid serialization issues
            if invalid_data == "object_placeholder":
                invalid_data = object()
            with subtests.test(invalid_data=str(type(invalid_data).__name__)):
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

        times = pd.date_range("2023-01-01", periods=3, freq="h")
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

    @patch(
        "mt_metadata.features.registry.SUPPORTED_FEATURE_DICT",
        {"test_feature": MagicMock},
    )
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

        # Patch the SUPPORTED_FEATURE_DICT directly in the registry module
        with patch(
            "mt_metadata.features.registry.SUPPORTED_FEATURE_DICT",
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


# ============================================================================
# CROSS POWERS SPECIFIC FIXTURES
# ============================================================================


@pytest.fixture
def basic_cross_powers():
    """Basic CrossPowers instance with default values."""
    return CrossPowers()


@pytest.fixture
def configured_cross_powers():
    """CrossPowers instance with configured values."""
    return CrossPowers(
        name="cross_powers_test",
        description="Cross power feature for testing",
        domain="frequency",
        comments=Comment(value="Test cross powers"),
    )


@pytest.fixture
def cross_powers_with_data(sample_numpy_data):
    """CrossPowers instance with sample data."""
    return CrossPowers(
        name="data_cross_powers",
        description="Cross powers with data",
        domain="frequency",
        data=sample_numpy_data,
    )


@pytest.fixture(scope="session")
def complex_cross_power_data():
    """Sample complex numpy array representing cross power spectra."""
    # Cross power spectra are typically complex
    real_part = np.random.rand(5, 10)
    imag_part = np.random.rand(5, 10)
    return real_part + 1j * imag_part


@pytest.fixture(scope="session")
def cross_power_xarray():
    """Sample xarray DataArray with cross power data structure."""
    frequencies = np.logspace(0, 3, 50)  # 1 to 1000 Hz
    channels = ["Hx_Hy", "Hx_Ex", "Hy_Ex", "Hy_Ey", "Ex_Ey"]

    # Create complex cross power data
    data = np.random.rand(len(frequencies), len(channels)) + 1j * np.random.rand(
        len(frequencies), len(channels)
    )

    return xr.DataArray(
        data,
        coords={"frequency": frequencies, "channel_pair": channels},
        dims=["frequency", "channel_pair"],
        attrs={
            "units": "cross_power",
            "description": "Cross power spectra between field components",
            "method": "multitaper",
        },
    )


@pytest.fixture(
    params=[
        {"domain": "frequency", "channels": ["Hx_Hy", "Ex_Ey"]},
        {"domain": "time", "channels": ["Hx_Ex", "Hy_Ey"]},
        {"domain": "fc", "channels": ["all_pairs"]},
    ]
)
def parametrized_cross_powers_data(request):
    """Parametrized cross powers data for testing multiple configurations."""
    return request.param


# ============================================================================
# CROSS POWERS SPECIFIC TESTS
# ============================================================================


@pytest.mark.cross_powers
class TestCrossPowersInstantiation:
    """Test CrossPowers class instantiation and inheritance."""

    def test_default_instantiation(self, basic_cross_powers):
        """Test CrossPowers can be instantiated with default values."""
        assert isinstance(basic_cross_powers, CrossPowers)
        assert isinstance(basic_cross_powers, Feature)  # Inheritance check
        assert basic_cross_powers.name == "cross_powers"  # Default from Field
        assert basic_cross_powers.description == ""
        assert basic_cross_powers.domain == DomainEnum.frequency
        assert basic_cross_powers.data is None

    def test_configured_instantiation(self, configured_cross_powers):
        """Test CrossPowers instantiation with configured values."""
        assert configured_cross_powers.name == "cross_powers_test"
        assert configured_cross_powers.description == "Cross power feature for testing"
        assert configured_cross_powers.domain == DomainEnum.frequency
        assert isinstance(configured_cross_powers.comments, Comment)

    def test_inheritance_properties(self, basic_cross_powers):
        """Test that CrossPowers inherits all Feature properties."""
        # Test that all Feature fields are accessible
        assert hasattr(basic_cross_powers, "name")
        assert hasattr(basic_cross_powers, "description")
        assert hasattr(basic_cross_powers, "domain")
        assert hasattr(basic_cross_powers, "data")
        assert hasattr(basic_cross_powers, "comments")

    def test_default_name_field(self):
        """Test that the default name field is properly set."""
        cp = CrossPowers()
        assert cp.name == "cross_powers"

        # Test that we can override the default
        cp_custom = CrossPowers(name="custom_cross_powers")
        assert cp_custom.name == "custom_cross_powers"

    def test_model_validate_instantiation(self):
        """Test CrossPowers instantiation using model_validate."""
        data = {
            "name": "validated_cross_powers",
            "description": "Cross powers created via model_validate",
            "domain": "frequency",
            "comments": "Validation test",
        }
        cp = CrossPowers.model_validate(data)
        assert cp.name == "validated_cross_powers"
        assert cp.domain == DomainEnum.frequency
        assert isinstance(cp.comments, Comment)


@pytest.mark.cross_powers
class TestCrossPowersDataHandling:
    """Test CrossPowers-specific data handling."""

    def test_complex_data_assignment(
        self, basic_cross_powers, complex_cross_power_data
    ):
        """Test assignment of complex cross power data."""
        basic_cross_powers.data = complex_cross_power_data
        assert isinstance(basic_cross_powers.data, np.ndarray)
        assert basic_cross_powers.data.dtype == np.complex128
        np.testing.assert_array_equal(basic_cross_powers.data, complex_cross_power_data)

    def test_xarray_cross_power_data(self, basic_cross_powers, cross_power_xarray):
        """Test assignment of xarray cross power data."""
        basic_cross_powers.data = cross_power_xarray
        assert isinstance(basic_cross_powers.data, xr.DataArray)
        assert "frequency" in basic_cross_powers.data.coords
        assert "channel_pair" in basic_cross_powers.data.coords
        assert basic_cross_powers.data.attrs["units"] == "cross_power"

    def test_cross_power_data_shapes(self, subtests):
        """Test CrossPowers with various data shapes using subtests."""
        test_shapes = [
            (10,),  # 1D frequency spectrum
            (50, 5),  # frequency x channel pairs
            (100, 10, 5),  # time x frequency x channel pairs
            (24, 60, 50, 5),  # day x time x frequency x channel pairs
        ]

        for shape in test_shapes:
            with subtests.test(shape=shape):
                data = np.random.rand(*shape) + 1j * np.random.rand(*shape)
                cp = CrossPowers(data=data)
                assert cp.data.shape == shape
                assert cp.data.dtype == np.complex128

    def test_real_valued_cross_powers(self, basic_cross_powers):
        """Test cross powers with real-valued data (e.g., power spectral density)."""
        real_data = np.random.rand(50, 5)
        basic_cross_powers.data = real_data
        assert isinstance(basic_cross_powers.data, np.ndarray)
        assert basic_cross_powers.data.dtype == np.float64
        np.testing.assert_array_equal(basic_cross_powers.data, real_data)

    def test_cross_power_with_coordinates(self):
        """Test CrossPowers with detailed coordinate information."""
        import pandas as pd

        # Create realistic MT cross power coordinates
        frequencies = np.logspace(-3, 3, 50)  # 0.001 to 1000 Hz
        times = pd.date_range("2023-01-01", periods=24, freq="h")
        channels = ["Hx_Hy", "Hx_Ex", "Hx_Ey", "Hy_Ex", "Hy_Ey", "Ex_Ey"]

        # 3D cross power data: time x frequency x channel_pairs
        data = np.random.rand(
            len(times), len(frequencies), len(channels)
        ) + 1j * np.random.rand(len(times), len(frequencies), len(channels))

        da = xr.DataArray(
            data,
            coords={
                "time": times,
                "frequency": frequencies,
                "channel_pair": channels,
            },
            dims=["time", "frequency", "channel_pair"],
            attrs={
                "units": "cross_power_spectral_density",
                "method": "multitaper",
                "taper_length": 512,
                "overlap": 0.5,
            },
        )

        cp = CrossPowers(
            name="mt_cross_powers",
            description="Magnetotelluric cross power spectra",
            domain="frequency",
            data=da,
        )

        assert isinstance(cp.data, xr.DataArray)
        assert cp.data.shape == (24, 50, 6)
        assert "method" in cp.data.attrs


@pytest.mark.cross_powers
class TestCrossPowersValidation:
    """Test CrossPowers field validation and constraints."""

    def test_domain_constraint_frequency(self):
        """Test that cross powers work best in frequency domain."""
        cp = CrossPowers(domain="frequency")
        assert cp.domain == DomainEnum.frequency

    def test_domain_constraint_other_domains(self, subtests):
        """Test cross powers in other domains using subtests."""
        other_domains = ["time", "fc", "ts", "fourier"]

        for domain in other_domains:
            with subtests.test(domain=domain):
                cp = CrossPowers(domain=domain)
                assert cp.domain.value == domain

    def test_name_field_validation(self):
        """Test name field validation and constraints."""
        # Test default name
        cp = CrossPowers()
        assert cp.name == "cross_powers"

        # Test custom name
        cp_custom = CrossPowers(name="custom_name")
        assert cp_custom.name == "custom_name"

        # Test empty name override
        cp_empty = CrossPowers(name="")
        assert cp_empty.name == ""

    def test_comments_validation_cross_powers(self, subtests):
        """Test comment validation specific to cross powers."""
        test_comments = [
            "Computed using Welch method",
            "Cross powers between H and E field components",
        ]
        # Create Comment object locally to avoid serialization issues
        comment_obj = Comment(value="Multitaper cross power estimation")
        test_comments.append(comment_obj)

        for comment in test_comments:
            # Use string representation for subtest key to avoid serialization
            test_key = (
                str(comment)
                if not isinstance(comment, Comment)
                else f"Comment({comment.value})"
            )
            with subtests.test(comment=test_key):
                cp = CrossPowers(comments=comment)
                assert isinstance(cp.comments, Comment)

    def test_invalid_data_types_cross_powers(self, subtests):
        """Test invalid data types for cross powers."""
        invalid_data = [
            "string_data",
            {"dict": "data"},
            [1, 2, 3],
            12345,
        ]

        for invalid in invalid_data:
            # Use string representation for subtest key
            test_key = (
                str(type(invalid).__name__)
                if not isinstance(invalid, (str, int))
                else str(invalid)
            )
            with subtests.test(invalid=test_key):
                with pytest.raises(
                    TypeError, match="Data must be a numpy array, xarray, or None"
                ):
                    CrossPowers(data=invalid)


@pytest.mark.cross_powers
class TestCrossPowersSpecialized:
    """Test CrossPowers specialized functionality and use cases."""

    def test_magnetotelluric_cross_powers(self, complex_cross_power_data):
        """Test cross powers for magnetotelluric applications."""
        cp = CrossPowers(
            name="mt_cross_powers",
            description="Magnetotelluric cross power spectra for impedance estimation",
            domain="frequency",
            data=complex_cross_power_data,
            comments=Comment(value="Computed for impedance tensor estimation"),
        )

        assert cp.name == "mt_cross_powers"
        assert "impedance" in cp.description
        assert cp.domain == DomainEnum.frequency
        assert isinstance(cp.data, np.ndarray)
        assert cp.data.dtype == np.complex128

    def test_audio_magnetotelluric_cross_powers(self):
        """Test cross powers for audio magnetotelluric frequency range."""
        # AMT typically covers 1 Hz to 10 kHz
        frequencies = np.logspace(0, 4, 100)  # 1 to 10,000 Hz
        channels = ["Hx_Hy", "Hx_Ex", "Hx_Ey", "Hy_Ex", "Hy_Ey", "Ex_Ey"]

        data = np.random.rand(len(frequencies), len(channels)) + 1j * np.random.rand(
            len(frequencies), len(channels)
        )

        da = xr.DataArray(
            data,
            coords={"frequency": frequencies, "channel_pair": channels},
            dims=["frequency", "channel_pair"],
            attrs={"frequency_range": "amt", "units": "cross_power"},
        )

        cp = CrossPowers(
            name="amt_cross_powers",
            description="Audio magnetotelluric cross power spectra",
            domain="frequency",
            data=da,
        )

        assert cp.data.attrs["frequency_range"] == "amt"
        assert cp.data.coords["frequency"].values.min() >= 1.0
        assert cp.data.coords["frequency"].values.max() <= 10000.0

    def test_broadband_mt_cross_powers(self):
        """Test cross powers for broadband magnetotelluric applications."""
        # BBM typically covers 0.001 Hz to 1000 Hz
        frequencies = np.logspace(-3, 3, 200)  # 0.001 to 1000 Hz
        channels = ["Hx_Hy", "Hx_Ex", "Hx_Ey", "Hy_Ex", "Hy_Ey", "Ex_Ey"]

        # Simulate realistic cross power magnitudes
        data = (
            np.random.rand(len(frequencies), len(channels)) * 1e-6
            + 1j * np.random.rand(len(frequencies), len(channels)) * 1e-6
        )

        da = xr.DataArray(
            data,
            coords={"frequency": frequencies, "channel_pair": channels},
            dims=["frequency", "channel_pair"],
            attrs={
                "frequency_range": "broadband",
                "units": "cross_power_spectral_density",
                "method": "robust_processing",
            },
        )

        cp = CrossPowers(
            name="bbmt_cross_powers",
            description="Broadband magnetotelluric cross power spectra",
            domain="frequency",
            data=da,
            comments=Comment(value="Processed with robust statistics"),
        )

        assert cp.data.attrs["frequency_range"] == "broadband"
        assert cp.data.coords["frequency"].values.min() <= 0.001
        assert cp.data.coords["frequency"].values.max() >= 1000.0

    @pytest.mark.parametrize(
        "processing_params",
        [
            {"method": "welch", "nperseg": 1024, "overlap": 0.5},
            {"method": "multitaper", "bandwidth": 4, "n_tapers": 7},
            {"method": "periodogram", "window": "hann"},
        ],
    )
    def test_cross_powers_processing_methods(self, processing_params):
        """Test cross powers with different processing methods."""
        data = np.random.rand(50, 5) + 1j * np.random.rand(50, 5)

        da = xr.DataArray(
            data,
            coords={"frequency": np.logspace(0, 2, 50), "channel_pair": range(5)},
            dims=["frequency", "channel_pair"],
            attrs=processing_params,
        )

        cp = CrossPowers(
            name=f"cross_powers_{processing_params['method']}",
            description=f"Cross powers using {processing_params['method']} method",
            domain="frequency",
            data=da,
        )

        assert cp.data.attrs["method"] == processing_params["method"]
        assert processing_params["method"] in cp.name


@pytest.mark.cross_powers
class TestCrossPowersSerialization:
    """Test CrossPowers serialization and deserialization."""

    def test_model_dump_cross_powers(self, configured_cross_powers):
        """Test CrossPowers serialization to dictionary."""
        data = configured_cross_powers.model_dump()
        assert isinstance(data, dict)
        assert data["name"] == "cross_powers_test"
        assert data["domain"] == "frequency"
        assert "comments" in data

    def test_roundtrip_serialization_cross_powers(self, cross_powers_with_data):
        """Test roundtrip serialization: CrossPowers -> dict -> CrossPowers."""
        # Serialize (excluding data for JSON compatibility)
        data = cross_powers_with_data.model_dump(exclude={"data"})

        # Create new CrossPowers from dict
        new_cp = CrossPowers.model_validate(data)

        # Verify properties match
        assert new_cp.name == cross_powers_with_data.name
        assert new_cp.description == cross_powers_with_data.description
        assert new_cp.domain == cross_powers_with_data.domain

    def test_json_schema_cross_powers(self):
        """Test JSON schema generation for CrossPowers."""
        schema = CrossPowers.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "name" in schema["properties"]

        # Check that name field has the proper default
        name_field = schema["properties"]["name"]
        assert "default" in name_field


@pytest.mark.cross_powers
class TestCrossPowersIntegration:
    """Integration tests for CrossPowers class."""

    def test_complete_cross_powers_workflow(self, complex_cross_power_data):
        """Test complete CrossPowers workflow."""
        # Create CrossPowers
        cp = CrossPowers(
            name="workflow_test",
            description="Complete workflow test for cross powers",
            domain="frequency",
        )

        # Verify initial state
        assert cp.name == "workflow_test"
        assert cp.domain == DomainEnum.frequency
        assert cp.data is None

        # Add data
        cp.data = complex_cross_power_data
        assert isinstance(cp.data, np.ndarray)
        assert cp.data.dtype == np.complex128

        # Modify properties
        cp.comments = Comment(value="Workflow test completed successfully")
        assert "successfully" in cp.comments.value

        # Serialize and verify
        serialized = cp.model_dump(exclude={"data"})
        assert serialized["name"] == "workflow_test"
        assert serialized["domain"] == "frequency"

    def test_cross_powers_inheritance_methods(self, basic_cross_powers):
        """Test that CrossPowers inherits all Feature methods."""
        # Test that inherited methods work
        assert hasattr(basic_cross_powers, "model_dump")
        assert hasattr(basic_cross_powers, "model_validate")
        assert callable(getattr(basic_cross_powers, "model_dump"))

        # Test serialization works
        dumped = basic_cross_powers.model_dump()
        assert isinstance(dumped, dict)
        assert "name" in dumped

    def test_parametrized_cross_powers_configurations(
        self, parametrized_cross_powers_data, subtests
    ):
        """Test cross powers with parametrized configurations."""
        config = parametrized_cross_powers_data

        with subtests.test(config=config):
            cp = CrossPowers(
                name=f"cross_powers_{config['domain']}",
                description=f"Cross powers in {config['domain']} domain",
                domain=config["domain"],
                comments=Comment(value=f"Channels: {', '.join(config['channels'])}"),
            )

            assert cp.domain.value == config["domain"]
            assert config["domain"] in cp.name
            assert any(channel in cp.comments.value for channel in config["channels"])


@pytest.mark.cross_powers
class TestCrossPowersEdgeCases:
    """Test CrossPowers edge cases and error conditions."""

    def test_very_large_cross_power_array(self):
        """Test CrossPowers with large data arrays."""
        large_data = np.zeros((1000, 1000), dtype=np.complex128)
        cp = CrossPowers(
            name="large_cross_powers",
            data=large_data,
        )
        assert cp.data.shape == (1000, 1000)
        assert cp.data.dtype == np.complex128

    def test_single_channel_cross_power(self):
        """Test CrossPowers with single channel (auto-power)."""
        # Single channel auto-power
        auto_power = np.random.rand(100) + 1j * np.zeros(100)  # Real-valued auto-power

        cp = CrossPowers(
            name="auto_power",
            description="Auto-power spectrum of a single channel",
            data=auto_power,
        )

        assert cp.data.shape == (100,)
        assert np.all(cp.data.imag == 0)  # Auto-power should be real

    def test_empty_cross_powers(self):
        """Test CrossPowers with empty data."""
        empty_data = np.array([], dtype=np.complex128)
        cp = CrossPowers(data=empty_data)
        assert cp.data.size == 0
        assert cp.data.dtype == np.complex128

    def test_unicode_in_cross_powers_metadata(self):
        """Test CrossPowers with unicode characters in metadata."""
        cp = CrossPowers(
            name="测试交叉功率",
            description="Cross powers with émojis 📊 and special chars ñ",
            comments=Comment(value="Unicode test: α, β, γ frequencies"),
        )

        assert "测试" in cp.name
        assert "émojis" in cp.description
        assert "α" in cp.comments.value
