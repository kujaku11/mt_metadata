"""
Test channel_weight_spec_basemodel.py - Comprehensive test suite for ChannelWeightSpec

Tests the ChannelWeightSpec class and CombinationStyleEnum from the basemodel module
using fixtures and subtests for optimal efficiency.

This module contains channel weight specification classes used in MT metadata processing,
providing structured weighting strategies for transfer function estimation.
"""

import time
from unittest.mock import Mock, patch

import numpy as np
import pytest
import xarray as xr

from mt_metadata.features.weights.channel_weight_spec import (
    ChannelWeightSpec,
    CombinationStyleEnum,
)
from mt_metadata.features.weights.feature_weight_spec import FeatureWeightSpec
from mt_metadata.processing.aurora.band import Band


# =====================================================
# Fixtures for optimal efficiency
# =====================================================


@pytest.fixture
def default_channel_weight_spec():
    """Basic ChannelWeightSpec with default values"""
    return ChannelWeightSpec()


@pytest.fixture
def multiplication_channel_weight_spec():
    """ChannelWeightSpec configured for multiplication combination"""
    return ChannelWeightSpec(
        combination_style=CombinationStyleEnum.multiplication,
        output_channels=["ex", "ey"],
        feature_weight_specs=[],
    )


@pytest.fixture
def mean_channel_weight_spec():
    """ChannelWeightSpec configured for mean combination"""
    return ChannelWeightSpec(
        combination_style=CombinationStyleEnum.mean,
        output_channels=["hz"],
        feature_weight_specs=[],
    )


@pytest.fixture
def minimum_channel_weight_spec():
    """ChannelWeightSpec configured for minimum combination"""
    return ChannelWeightSpec(
        combination_style=CombinationStyleEnum.minimum,
        output_channels=["ex", "ey", "hz"],
        feature_weight_specs=[],
    )


@pytest.fixture
def maximum_channel_weight_spec():
    """ChannelWeightSpec configured for maximum combination"""
    return ChannelWeightSpec(
        combination_style=CombinationStyleEnum.maximum,
        output_channels=["ex"],
        feature_weight_specs=[],
    )


@pytest.fixture
def sample_feature_weight_spec():
    """Mock FeatureWeightSpec for testing purposes"""
    mock_spec = Mock(spec=FeatureWeightSpec)
    mock_spec.feature = Mock()
    mock_spec.feature.name = "coherence"
    mock_spec.evaluate = Mock(return_value=0.8)
    return mock_spec


@pytest.fixture
def multiple_feature_weight_specs():
    """List of mock FeatureWeightSpecs for testing"""
    specs = []
    for i, name in enumerate(["coherence", "multiple_coherence", "power"]):
        mock_spec = Mock(spec=FeatureWeightSpec)
        mock_spec.feature = Mock()
        mock_spec.feature.name = name
        mock_spec.evaluate = Mock(return_value=0.7 + i * 0.1)
        specs.append(mock_spec)
    return specs


@pytest.fixture
def sample_xarray_weights():
    """Sample xarray DataArray with frequency dimension"""
    freqs = np.logspace(0, 3, 50)  # 1 Hz to 1000 Hz
    times = np.arange(100)
    data = np.random.random((50, 100))
    return xr.DataArray(
        data,
        coords={"frequency": freqs, "time": times},
        dims=["frequency", "time"],
    )


@pytest.fixture
def sample_numpy_weights():
    """Sample numpy array weights"""
    return np.random.random((50, 100))


@pytest.fixture
def sample_band():
    """Sample Band object for testing"""
    return Band(
        decimation_level=0,
        index_max=100,
        index_min=10,
        center_frequency=50.0,
    )


@pytest.fixture
def feature_values_dict():
    """Sample feature values dictionary"""
    return {
        "coherence": np.array([0.8, 0.9, 0.7]),
        "multiple_coherence": np.array([0.75, 0.85, 0.65]),
        "power": np.array([0.9, 0.95, 0.88]),
    }


# =====================================================
# Test Classes organized by functionality
# =====================================================


class TestCombinationStyleEnum:
    """Test CombinationStyleEnum enumeration"""

    def test_enum_values(self):
        """Test all enum values are properly defined"""
        assert CombinationStyleEnum.multiplication == "multiplication"
        assert CombinationStyleEnum.minimum == "minimum"
        assert CombinationStyleEnum.maximum == "maximum"
        assert CombinationStyleEnum.mean == "mean"

    def test_enum_string_representation(self):
        """Test enum string representation"""
        assert str(CombinationStyleEnum.multiplication.value) == "multiplication"
        assert str(CombinationStyleEnum.minimum.value) == "minimum"
        assert str(CombinationStyleEnum.maximum.value) == "maximum"
        assert str(CombinationStyleEnum.mean.value) == "mean"

    def test_enum_membership(self):
        """Test enum membership validation"""
        valid_values = ["multiplication", "minimum", "maximum", "mean"]
        for value in valid_values:
            assert value in [e.value for e in CombinationStyleEnum]


class TestChannelWeightSpecInstantiation:
    """Test ChannelWeightSpec instantiation and basic properties"""

    def test_default_instantiation(self, default_channel_weight_spec):
        """Test default instantiation"""
        cws = default_channel_weight_spec
        assert cws.combination_style == CombinationStyleEnum.multiplication
        assert cws.output_channels == []
        assert cws.feature_weight_specs == []
        assert cws.weights is None

    def test_custom_instantiation(self):
        """Test instantiation with custom parameters"""
        cws = ChannelWeightSpec(
            combination_style=CombinationStyleEnum.mean,
            output_channels=["ex", "ey", "hz"],
            feature_weight_specs=[],
        )
        assert cws.combination_style == CombinationStyleEnum.mean
        assert cws.output_channels == ["ex", "ey", "hz"]
        assert cws.feature_weight_specs == []
        assert cws.weights is None

    @pytest.mark.parametrize(
        "combination_style",
        [
            CombinationStyleEnum.multiplication,
            CombinationStyleEnum.minimum,
            CombinationStyleEnum.maximum,
            CombinationStyleEnum.mean,
        ],
    )
    def test_combination_style_variants(self, combination_style):
        """Test different combination style configurations"""
        cws = ChannelWeightSpec(combination_style=combination_style)
        assert cws.combination_style == combination_style

    @pytest.mark.parametrize(
        "output_channels",
        [
            [],
            ["ex"],
            ["ex", "ey"],
            ["ex", "ey", "hz"],
            ["hx", "hy"],
        ],
    )
    def test_output_channels_variants(self, output_channels):
        """Test different output channel configurations"""
        cws = ChannelWeightSpec(output_channels=output_channels)
        assert cws.output_channels == output_channels


class TestChannelWeightSpecFieldValidation:
    """Test ChannelWeightSpec field validation"""

    def test_feature_weight_specs_validation_empty_list(self):
        """Test feature_weight_specs validation with empty list"""
        cws = ChannelWeightSpec(feature_weight_specs=[])
        assert cws.feature_weight_specs == []

    def test_weights_validation_none(self):
        """Test weights validation with None"""
        cws = ChannelWeightSpec(weights=None)
        assert cws.weights is None

    def test_weights_validation_numpy_array(self, sample_numpy_weights):
        """Test weights validation with numpy array"""
        cws = ChannelWeightSpec(weights=sample_numpy_weights)
        assert isinstance(cws.weights, np.ndarray)
        np.testing.assert_array_equal(cws.weights, sample_numpy_weights)

    def test_weights_validation_xarray(self, sample_xarray_weights):
        """Test weights validation with xarray DataArray"""
        cws = ChannelWeightSpec(weights=sample_xarray_weights)
        assert isinstance(cws.weights, xr.DataArray)
        xr.testing.assert_equal(cws.weights, sample_xarray_weights)

    def test_weights_validation_invalid_type(self):
        """Test weights validation with invalid type"""
        with pytest.raises(TypeError, match="Data must be a numpy array or xarray"):
            ChannelWeightSpec(weights="invalid_type")

    def test_weights_validation_list_rejected(self):
        """Test weights validation rejects list"""
        with pytest.raises(TypeError, match="Data must be a numpy array or xarray"):
            ChannelWeightSpec(weights=[1, 2, 3])


class TestChannelWeightSpecEvaluateMethod:
    """Test ChannelWeightSpec evaluate method"""

    def test_evaluate_empty_feature_specs(self, default_channel_weight_spec):
        """Test evaluate with no feature weight specs returns 1.0"""
        result = default_channel_weight_spec.evaluate({})
        assert result == 1.0

    def test_evaluate_single_feature_multiplication(
        self, multiplication_channel_weight_spec, sample_feature_weight_spec
    ):
        """Test evaluate with single feature using multiplication"""
        multiplication_channel_weight_spec.feature_weight_specs = [
            sample_feature_weight_spec
        ]
        feature_values = {"coherence": np.array([0.8, 0.9, 0.7])}

        result = multiplication_channel_weight_spec.evaluate(feature_values)
        # Verify the evaluate method was called once (without comparing numpy arrays directly)
        sample_feature_weight_spec.evaluate.assert_called_once()
        # Check that the result matches the mocked return value
        assert result == 0.8

    def test_evaluate_multiple_features_multiplication(
        self, multiplication_channel_weight_spec, multiple_feature_weight_specs
    ):
        """Test evaluate with multiple features using multiplication"""
        multiplication_channel_weight_spec.feature_weight_specs = (
            multiple_feature_weight_specs
        )
        feature_values = {
            "coherence": np.array([0.8, 0.9, 0.7]),
            "multiple_coherence": np.array([0.75, 0.85, 0.65]),
            "power": np.array([0.9, 0.95, 0.88]),
        }

        with patch("numpy.prod") as mock_prod:
            mock_prod.return_value = 0.6
            result = multiplication_channel_weight_spec.evaluate(feature_values)
            mock_prod.assert_called_once()
            assert result == 0.6

    def test_evaluate_multiple_features_mean(
        self, mean_channel_weight_spec, multiple_feature_weight_specs
    ):
        """Test evaluate with multiple features using mean"""
        mean_channel_weight_spec.feature_weight_specs = multiple_feature_weight_specs
        feature_values = {
            "coherence": np.array([0.8, 0.9, 0.7]),
            "multiple_coherence": np.array([0.75, 0.85, 0.65]),
            "power": np.array([0.9, 0.95, 0.88]),
        }

        with patch("numpy.mean") as mock_mean:
            mock_mean.return_value = 0.8
            result = mean_channel_weight_spec.evaluate(feature_values)
            mock_mean.assert_called_once()
            assert result == 0.8

    def test_evaluate_multiple_features_minimum(
        self, minimum_channel_weight_spec, multiple_feature_weight_specs
    ):
        """Test evaluate with multiple features using minimum"""
        minimum_channel_weight_spec.feature_weight_specs = multiple_feature_weight_specs
        feature_values = {
            "coherence": np.array([0.8, 0.9, 0.7]),
            "multiple_coherence": np.array([0.75, 0.85, 0.65]),
            "power": np.array([0.9, 0.95, 0.88]),
        }

        with patch("numpy.min") as mock_min:
            mock_min.return_value = 0.7
            result = minimum_channel_weight_spec.evaluate(feature_values)
            mock_min.assert_called_once()
            assert result == 0.7

    def test_evaluate_multiple_features_maximum(
        self, maximum_channel_weight_spec, multiple_feature_weight_specs
    ):
        """Test evaluate with multiple features using maximum"""
        maximum_channel_weight_spec.feature_weight_specs = multiple_feature_weight_specs
        feature_values = {
            "coherence": np.array([0.8, 0.9, 0.7]),
            "multiple_coherence": np.array([0.75, 0.85, 0.65]),
            "power": np.array([0.9, 0.95, 0.88]),
        }

        with patch("numpy.max") as mock_max:
            mock_max.return_value = 0.9
            result = maximum_channel_weight_spec.evaluate(feature_values)
            mock_max.assert_called_once()
            assert result == 0.9

    def test_evaluate_missing_feature_raises_keyerror(
        self, multiplication_channel_weight_spec, sample_feature_weight_spec
    ):
        """Test evaluate raises KeyError for missing feature"""
        multiplication_channel_weight_spec.feature_weight_specs = [
            sample_feature_weight_spec
        ]
        feature_values = {"power": np.array([0.9, 0.95, 0.88])}

        with pytest.raises(KeyError, match="Feature values missing for 'coherence'"):
            multiplication_channel_weight_spec.evaluate(feature_values)

    def test_evaluate_invalid_combination_style(self, default_channel_weight_spec):
        """Test evaluate with invalid combination style"""
        # Manually set combination_style to bypass validation during assignment
        object.__setattr__(
            default_channel_weight_spec, "combination_style", "invalid_style"
        )
        # Create a minimal mock feature spec to trigger the evaluation path
        mock_spec = Mock()
        mock_spec.feature = Mock()
        mock_spec.feature.name = "test"
        mock_spec.evaluate = Mock(return_value=0.5)
        # Manually set the feature_weight_specs to bypass validation
        object.__setattr__(
            default_channel_weight_spec, "feature_weight_specs", [mock_spec]
        )

        with pytest.raises(
            ValueError, match="Unknown combination style: invalid_style"
        ):
            default_channel_weight_spec.evaluate({"test": 0.5})


class TestChannelWeightSpecGetWeightsForBand:
    """Test ChannelWeightSpec get_weights_for_band method"""

    def test_get_weights_for_band_no_weights_raises_error(
        self, default_channel_weight_spec, sample_band
    ):
        """Test get_weights_for_band raises error when no weights set"""
        with pytest.raises(ValueError, match="No weights have been set"):
            default_channel_weight_spec.get_weights_for_band(sample_band)

    def test_get_weights_for_band_xarray_with_frequency_dim(
        self, default_channel_weight_spec, sample_xarray_weights, sample_band
    ):
        """Test get_weights_for_band with xarray having frequency dimension"""
        default_channel_weight_spec.weights = sample_xarray_weights

        with patch("numpy.argmin") as mock_argmin:
            mock_argmin.return_value = 25  # Mock index
            result = default_channel_weight_spec.get_weights_for_band(sample_band)
            mock_argmin.assert_called_once()
            assert isinstance(result, xr.DataArray)

    def test_get_weights_for_band_xarray_no_frequency_dim(
        self, default_channel_weight_spec, sample_band
    ):
        """Test get_weights_for_band with xarray without frequency dimension"""
        # Create xarray without frequency dimension
        data = np.random.random((50, 100))
        weights_no_freq = xr.DataArray(
            data,
            coords={"time": np.arange(50), "channel": np.arange(100)},
            dims=["time", "channel"],
        )
        default_channel_weight_spec.weights = weights_no_freq

        with pytest.raises(ValueError, match="Could not find frequency dimension"):
            default_channel_weight_spec.get_weights_for_band(sample_band)

    def test_get_weights_for_band_numpy_array(
        self, default_channel_weight_spec, sample_numpy_weights, sample_band
    ):
        """Test get_weights_for_band with numpy array"""
        default_channel_weight_spec.weights = sample_numpy_weights

        with patch("numpy.argmin") as mock_argmin:
            mock_argmin.return_value = 25  # Mock index
            result = default_channel_weight_spec.get_weights_for_band(sample_band)
            mock_argmin.assert_called_once()
            assert isinstance(result, np.ndarray)

    def test_get_weights_for_band_invalid_weights_type(
        self, default_channel_weight_spec, sample_band
    ):
        """Test get_weights_for_band with invalid weights type"""
        # Manually set weights to invalid type bypassing validation
        object.__setattr__(default_channel_weight_spec, "weights", "invalid_type")

        with pytest.raises(TypeError, match="Weights must be an xarray.DataArray"):
            default_channel_weight_spec.get_weights_for_band(sample_band)


class TestChannelWeightSpecSerialization:
    """Test ChannelWeightSpec serialization and deserialization"""

    def test_to_dict_basic(self, default_channel_weight_spec):
        """Test basic to_dict serialization"""
        result = default_channel_weight_spec.to_dict()
        expected_keys = {
            "combination_style",
            "output_channels",
            "feature_weight_specs",
        }
        assert "channel_weight_spec" in result
        channel_data = result["channel_weight_spec"]
        assert expected_keys.issubset(set(channel_data.keys()))
        assert channel_data["combination_style"] == "multiplication"
        assert channel_data["output_channels"] == []
        assert channel_data["feature_weight_specs"] == []

    def test_to_dict_with_data(self, multiplication_channel_weight_spec):
        """Test to_dict with actual data"""
        result = multiplication_channel_weight_spec.to_dict()
        assert "channel_weight_spec" in result
        channel_data = result["channel_weight_spec"]
        assert channel_data["combination_style"] == "multiplication"
        assert channel_data["output_channels"] == ["ex", "ey"]
        assert channel_data["feature_weight_specs"] == []

    def test_model_copy(self, multiplication_channel_weight_spec):
        """Test model_copy functionality"""
        copied = multiplication_channel_weight_spec.model_copy()
        assert (
            copied.combination_style
            == multiplication_channel_weight_spec.combination_style
        )
        assert (
            copied.output_channels == multiplication_channel_weight_spec.output_channels
        )
        assert copied is not multiplication_channel_weight_spec

    def test_model_copy_deep(self, multiplication_channel_weight_spec):
        """Test deep model_copy functionality"""
        copied = multiplication_channel_weight_spec.model_copy(deep=True)
        assert (
            copied.combination_style
            == multiplication_channel_weight_spec.combination_style
        )
        assert (
            copied.output_channels == multiplication_channel_weight_spec.output_channels
        )
        assert (
            copied.output_channels
            is not multiplication_channel_weight_spec.output_channels
        )


class TestChannelWeightSpecJsonSchema:
    """Test ChannelWeightSpec JSON schema generation"""

    @pytest.mark.skip(
        reason="FeatureWeightSpec not compatible with JSON schema generation"
    )
    def test_json_schema_generation(self):
        """Test JSON schema can be generated"""
        schema = ChannelWeightSpec.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "combination_style" in schema["properties"]
        assert "output_channels" in schema["properties"]
        assert "feature_weight_specs" in schema["properties"]
        assert "weights" in schema["properties"]

    @pytest.mark.skip(
        reason="FeatureWeightSpec not compatible with JSON schema generation"
    )
    def test_json_schema_field_types(self):
        """Test JSON schema field type definitions"""
        schema = ChannelWeightSpec.model_json_schema()
        properties = schema["properties"]

        # Check combination_style field
        assert "enum" in properties["combination_style"]
        expected_enum = ["multiplication", "minimum", "maximum", "mean"]
        assert set(properties["combination_style"]["enum"]) == set(expected_enum)

        # Check output_channels is array
        assert properties["output_channels"]["type"] == "array"
        assert properties["output_channels"]["items"]["type"] == "string"


class TestChannelWeightSpecInheritance:
    """Test ChannelWeightSpec inheritance from MetadataBase"""

    def test_inherits_from_metadata_base(self):
        """Test ChannelWeightSpec inherits from MetadataBase"""
        from mt_metadata.base import MetadataBase

        assert issubclass(ChannelWeightSpec, MetadataBase)

    def test_metadata_base_methods_available(self, default_channel_weight_spec):
        """Test MetadataBase methods are available"""
        # Test common MetadataBase methods
        assert hasattr(default_channel_weight_spec, "to_dict")
        assert hasattr(default_channel_weight_spec, "model_copy")
        assert callable(getattr(default_channel_weight_spec, "to_dict"))
        assert callable(getattr(default_channel_weight_spec, "model_copy"))


class TestChannelWeightSpecEdgeCases:
    """Test ChannelWeightSpec edge cases and error conditions"""

    def test_evaluate_with_scalar_values(self, multiplication_channel_weight_spec):
        """Test evaluate with scalar feature values"""
        mock_spec = Mock(spec=FeatureWeightSpec)
        mock_spec.feature = Mock()
        mock_spec.feature.name = "coherence"
        mock_spec.evaluate = Mock(return_value=0.8)

        multiplication_channel_weight_spec.feature_weight_specs = [mock_spec]
        result = multiplication_channel_weight_spec.evaluate({"coherence": 0.9})
        assert result == 0.8

    def test_evaluate_with_mixed_types(self, mean_channel_weight_spec):
        """Test evaluate with mixed numpy arrays and scalars"""
        specs = []
        for i, (name, return_val) in enumerate(
            [("coherence", np.array([0.8, 0.9])), ("power", 0.7)]
        ):
            mock_spec = Mock(spec=FeatureWeightSpec)
            mock_spec.feature = Mock()
            mock_spec.feature.name = name
            mock_spec.evaluate = Mock(return_value=return_val)
            specs.append(mock_spec)

        mean_channel_weight_spec.feature_weight_specs = specs
        feature_values = {"coherence": np.array([0.8, 0.9]), "power": 0.7}

        with patch("numpy.mean") as mock_mean:
            mock_mean.return_value = 0.75
            result = mean_channel_weight_spec.evaluate(feature_values)
            assert result == 0.75

    def test_large_output_channels_list(self):
        """Test with large output channels list"""
        large_channels = [f"channel_{i}" for i in range(100)]
        cws = ChannelWeightSpec(output_channels=large_channels)
        assert len(cws.output_channels) == 100
        assert cws.output_channels == large_channels

    def test_empty_string_in_output_channels(self):
        """Test empty string in output channels"""
        cws = ChannelWeightSpec(output_channels=["ex", "", "ey"])
        assert "" in cws.output_channels
        assert len(cws.output_channels) == 3


class TestChannelWeightSpecPerformance:
    """Test ChannelWeightSpec performance characteristics"""

    def test_instantiation_performance(self):
        """Test instantiation performance"""
        start_time = time.time()
        instances = []
        for _ in range(100):
            instances.append(ChannelWeightSpec())
        end_time = time.time()

        # Should complete quickly (less than 1 second for 100 instances)
        assert end_time - start_time < 1.0
        assert len(instances) == 100

    def test_evaluate_performance_large_arrays(
        self, multiplication_channel_weight_spec
    ):
        """Test evaluate performance with large arrays"""
        # Create mock spec with large array
        mock_spec = Mock(spec=FeatureWeightSpec)
        mock_spec.feature = Mock()
        mock_spec.feature.name = "coherence"
        large_array = np.random.random(10000)
        mock_spec.evaluate = Mock(return_value=large_array)

        multiplication_channel_weight_spec.feature_weight_specs = [mock_spec]
        feature_values = {"coherence": large_array}

        start_time = time.time()
        result = multiplication_channel_weight_spec.evaluate(feature_values)
        end_time = time.time()

        # Should complete quickly
        assert end_time - start_time < 1.0
        np.testing.assert_array_equal(result, large_array)

    def test_to_dict_performance(self, multiplication_channel_weight_spec):
        """Test to_dict performance"""
        start_time = time.time()
        for _ in range(100):
            multiplication_channel_weight_spec.to_dict()
        end_time = time.time()

        # Should complete quickly
        assert end_time - start_time < 1.0


class TestChannelWeightSpecIntegration:
    """Test ChannelWeightSpec integration scenarios"""

    def test_full_workflow_multiplication(
        self, multiplication_channel_weight_spec, feature_values_dict
    ):
        """Test full workflow with multiplication combination"""
        # Setup mock feature weight specs
        specs = []
        expected_values = [0.8, 0.75, 0.9]
        for i, name in enumerate(["coherence", "multiple_coherence", "power"]):
            mock_spec = Mock(spec=FeatureWeightSpec)
            mock_spec.feature = Mock()
            mock_spec.feature.name = name
            mock_spec.evaluate = Mock(return_value=expected_values[i])
            specs.append(mock_spec)

        multiplication_channel_weight_spec.feature_weight_specs = specs

        # Test evaluation
        result = multiplication_channel_weight_spec.evaluate(feature_values_dict)

        # Verify all specs were called
        for spec in specs:
            spec.evaluate.assert_called_once()

        # Result should be product of all values
        expected_result = np.prod(expected_values)
        assert result == expected_result

    def test_workflow_with_weights_setting(
        self, default_channel_weight_spec, sample_xarray_weights, sample_band
    ):
        """Test workflow including setting and retrieving weights"""
        # Set weights
        default_channel_weight_spec.weights = sample_xarray_weights

        # Get weights for band
        with patch("numpy.argmin", return_value=25):
            weights_for_band = default_channel_weight_spec.get_weights_for_band(
                sample_band
            )
            assert isinstance(weights_for_band, xr.DataArray)

    def test_serialization_roundtrip(self, multiplication_channel_weight_spec):
        """Test serialization and deserialization roundtrip"""
        # Convert to dict
        data_dict = multiplication_channel_weight_spec.to_dict()

        # Create new instance from dict
        new_instance = ChannelWeightSpec(**data_dict)

        # Verify they match
        assert (
            new_instance.combination_style
            == multiplication_channel_weight_spec.combination_style
        )
        assert (
            new_instance.output_channels
            == multiplication_channel_weight_spec.output_channels
        )
        assert (
            new_instance.feature_weight_specs
            == multiplication_channel_weight_spec.feature_weight_specs
        )


# =====================================================
# Integration and Comprehensive Tests
# =====================================================


class TestChannelWeightSpecComprehensive:
    """Comprehensive tests covering multiple aspects simultaneously"""

    def test_comprehensive_functionality(self):
        """Test multiple functionality aspects together"""
        # Create instance with all parameters
        cws = ChannelWeightSpec(
            combination_style=CombinationStyleEnum.mean,
            output_channels=["ex", "ey", "hz"],
            feature_weight_specs=[],
        )

        # Test basic properties
        assert cws.combination_style == CombinationStyleEnum.mean
        assert len(cws.output_channels) == 3
        assert cws.weights is None

        # Test serialization
        data_dict = cws.to_dict()
        assert "channel_weight_spec" in data_dict
        channel_data = data_dict["channel_weight_spec"]
        assert channel_data["combination_style"] == "mean"
        assert len(channel_data["output_channels"]) == 3

        # Test copy
        copied = cws.model_copy()
        assert copied.combination_style == cws.combination_style
        assert copied is not cws

    @pytest.mark.parametrize(
        "combo_style,expected_func",
        [
            (CombinationStyleEnum.multiplication, "prod"),
            (CombinationStyleEnum.mean, "mean"),
            (CombinationStyleEnum.minimum, "min"),
            (CombinationStyleEnum.maximum, "max"),
        ],
    )
    def test_all_combination_styles_with_mocking(self, combo_style, expected_func):
        """Test all combination styles with proper mocking"""
        cws = ChannelWeightSpec(
            combination_style=combo_style,
            output_channels=["ex"],
            feature_weight_specs=[],
        )

        # Create mock feature weight specs
        mock_spec = Mock(spec=FeatureWeightSpec)
        mock_spec.feature = Mock()
        mock_spec.feature.name = "test_feature"
        mock_spec.evaluate = Mock(return_value=0.8)
        cws.feature_weight_specs = [mock_spec]

        feature_values = {"test_feature": np.array([0.8, 0.9, 0.7])}

        with patch(f"numpy.{expected_func}") as mock_func:
            mock_func.return_value = 0.8
            result = cws.evaluate(feature_values)
            if len(cws.feature_weight_specs) > 1 or expected_func != "prod":
                mock_func.assert_called_once()
            assert result == 0.8
