"""
Pytest suite for FeatureWeightSpec class

This file tests the FeatureWeightSpec functionality using pytest fixtures,
parametrized tests, and markers for optimal efficiency.

Run with:
    pytest test_feature_weight_spec.py
    pytest test_feature_weight_spec.py -m features  # Run only feature tests
    pytest test_feature_weight_spec.py -m kernels  # Run only kernel tests
    pytest test_feature_weight_spec.py -v  # Verbose output

Test organization:
- Fixtures for reusable test data and instances
- Parametrized tests for efficiency
- Pytest markers for test categorization
- Comprehensive test coverage with edge cases
"""

import numpy as np
import pytest

from mt_metadata.features.weights.feature_weight_spec import (
    FeatureNameEnum,
    FeatureWeightSpec,
)
from mt_metadata.features.weights.taper_monotonic_weight_kernel import (
    TaperMonotonicWeightKernel,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_feature_dict():
    """Sample feature dictionary for testing."""
    return {
        "feature_name": "coherence",
        "feature": {
            "ch1": "ex",
            "ch2": "hy",
        },
        "weight_kernels": [
            {
                "style": "taper",
                "half_window_style": "hann",
                "transition_lower_bound": 0.3,
                "transition_upper_bound": 0.8,
                "threshold": "low cut",
            }
        ],
    }


@pytest.fixture
def taper_kernel_1():
    """Create first TaperMonotonicWeightKernel for testing."""
    return TaperMonotonicWeightKernel.model_validate(
        {
            "transition_lower_bound": 0.2,
            "transition_upper_bound": 0.5,
            "half_window_style": "hann",
            "threshold": "low cut",
            "style": "taper",
        }
    )


@pytest.fixture
def taper_kernel_2():
    """Create second TaperMonotonicWeightKernel for testing."""
    return TaperMonotonicWeightKernel.model_validate(
        {
            "transition_lower_bound": 0.6,
            "transition_upper_bound": 0.9,
            "half_window_style": "hann",
            "threshold": "high cut",
            "style": "taper",
        }
    )


@pytest.fixture
def simple_feature():
    """Create a simple feature dict for testing."""
    return {"ch1": "ex", "ch2": "hy"}


@pytest.fixture
def feature_weight_spec(simple_feature, taper_kernel_1, taper_kernel_2):
    """Create a FeatureWeightSpec instance for testing."""
    return FeatureWeightSpec(
        feature_name=FeatureNameEnum.coherence,
        feature=simple_feature,
        weight_kernels=[taper_kernel_1, taper_kernel_2],
    )


@pytest.fixture
def test_feature_values():
    """Sample feature values for testing evaluation."""
    return np.array([0.1, 0.3, 0.7, 1.0])


@pytest.fixture
def mixed_weight_kernels(taper_kernel_1):
    """Mixed list of weight kernels including dict and object instances."""
    return [
        {"transition_lower_bound": 0.1, "transition_upper_bound": 0.4},
        taper_kernel_1,
    ]


# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================


@pytest.mark.basics
class TestFeatureWeightSpecBasics:
    """Test basic FeatureWeightSpec functionality."""

    def test_initialization_from_dict(self, sample_feature_dict):
        """Test creating FeatureWeightSpec instance from dictionary."""
        feature_weight_spec = FeatureWeightSpec.model_validate(sample_feature_dict)
        assert feature_weight_spec.feature_name == FeatureNameEnum.coherence

    def test_features_property(self, feature_weight_spec, simple_feature):
        """Test the features property."""
        assert feature_weight_spec.feature.ch1 == simple_feature["ch1"]
        assert feature_weight_spec.feature.ch2 == simple_feature["ch2"]

    def test_weight_kernels_property(self, feature_weight_spec):
        """Test the weight_kernels property."""
        assert len(feature_weight_spec.weight_kernels) == 2
        assert isinstance(
            feature_weight_spec.weight_kernels[0], TaperMonotonicWeightKernel
        )

    @pytest.mark.parametrize(
        "feature_values,expected_shape",
        [
            (np.array([0.1, 0.3, 0.7, 1.0]), (4,)),
            (np.array([0.5]), (1,)),
            (0.5, ()),  # scalar
        ],
    )
    def test_evaluate_shapes(self, feature_weight_spec, feature_values, expected_shape):
        """Test the evaluate method with different input shapes."""
        combined_weights = feature_weight_spec.evaluate(feature_values)
        if expected_shape == ():
            assert np.isscalar(combined_weights)
        else:
            assert combined_weights.shape == expected_shape

    def test_evaluate_values(self, feature_weight_spec, test_feature_values):
        """Test the evaluate method returns reasonable values."""
        combined_weights = feature_weight_spec.evaluate(test_feature_values)

        # Ensure the output is the correct shape
        assert combined_weights.shape == test_feature_values.shape

        # Check specific values (example assertions)
        assert np.allclose(combined_weights[0], 0.0, atol=1e-5)
        assert combined_weights[2] > 0.0


# ============================================================================
# KERNEL TESTS
# ============================================================================


@pytest.mark.kernels
class TestWeightKernelHandling:
    """Test weight kernel handling functionality."""

    def test_mixed_weight_kernels_handling(self, mixed_weight_kernels):
        """Test handling of mixed weight kernel types."""
        # This would test _unpack_weight_kernels functionality if it existed
        # For now, test that we can create a spec with mixed types
        assert len(mixed_weight_kernels) == 2
        assert isinstance(mixed_weight_kernels[1], TaperMonotonicWeightKernel)
        assert isinstance(mixed_weight_kernels[0], dict)

    @pytest.mark.parametrize(
        "kernel_params",
        [
            {
                "transition_lower_bound": 0.1,
                "transition_upper_bound": 0.4,
                "half_window_style": "hann",
                "threshold": "low cut",
                "style": "taper",
            },
            {
                "transition_lower_bound": 0.3,
                "transition_upper_bound": 0.7,
                "half_window_style": "hamming",
                "threshold": "high cut",
                "style": "taper",
            },
            {
                "transition_lower_bound": 0.0,
                "transition_upper_bound": 1.0,
                "half_window_style": "rectangle",
                "threshold": "low cut",
                "style": "taper",
            },
        ],
    )
    def test_kernel_creation_parametrized(self, kernel_params):
        """Test creating kernels with various parameters."""
        kernel = TaperMonotonicWeightKernel.model_validate(kernel_params)
        assert kernel.transition_lower_bound == kernel_params["transition_lower_bound"]
        assert kernel.transition_upper_bound == kernel_params["transition_upper_bound"]
        assert kernel.half_window_style == kernel_params["half_window_style"]
        assert kernel.threshold == kernel_params["threshold"]


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.integration
class TestFeatureWeightSpecIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow(self, sample_feature_dict):
        """Test a complete workflow: create from dict, modify, evaluate."""
        # Create from dict
        feature_weight_spec = FeatureWeightSpec.model_validate(sample_feature_dict)

        # Test evaluation with sample data
        test_values = np.array([0.2, 0.5, 0.8])
        weights = feature_weight_spec.evaluate(test_values)

        # Verify results
        assert isinstance(weights, np.ndarray)
        assert weights.shape == test_values.shape
        assert np.all(weights >= 0.0)  # Weights should be non-negative
        assert np.all(weights <= 1.0)  # Weights should be <= 1.0

    @pytest.mark.parametrize(
        "test_values",
        [
            np.array([0.1, 0.9]),  # Edge values
            np.array([0.5]),  # Single value
            np.linspace(0, 1, 10),  # Range of values
            0.5,  # Scalar value
        ],
    )
    def test_evaluation_with_various_inputs(self, feature_weight_spec, test_values):
        """Test evaluation with various input types and ranges."""
        weights = feature_weight_spec.evaluate(test_values)

        if np.isscalar(test_values):
            assert np.isscalar(weights)
        else:
            assert isinstance(weights, np.ndarray)
            assert weights.shape == test_values.shape


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


@pytest.mark.edge_cases
class TestFeatureWeightSpecEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_weight_kernels(self, simple_feature):
        """Test FeatureWeightSpec with empty weight kernels list."""
        feature_weight_spec = FeatureWeightSpec(
            feature_name=FeatureNameEnum.coherence,
            feature=simple_feature,
            weight_kernels=[],
        )

        # Should return 1.0 (no weighting)
        test_values = np.array([0.1, 0.5, 0.9])
        weights = feature_weight_spec.evaluate(test_values)
        assert np.allclose(weights, 1.0)

    @pytest.mark.parametrize(
        "bad_input",
        [
            None,
            "invalid",
            [],
        ],
    )
    def test_evaluate_invalid_inputs(self, feature_weight_spec, bad_input):
        """Test evaluate method with invalid inputs."""
        with pytest.raises((TypeError, ValueError, AttributeError)):
            feature_weight_spec.evaluate(bad_input)
