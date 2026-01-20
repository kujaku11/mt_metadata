"""
Test activation_monotonic_weight_kernel_basemodel.py - Comprehensive test suite for ActivationMonotonicWeightKernel basemodel

Tests the ActivationMonotonicWeightKernel class, ThresholdEnum, and ActivationStyleEnum from the
basemodel module using fixtures and subtests for optimal efficiency.

This module contains the activation-based classes and enumerations for monotonic weight kernels
used in MT metadata processing with sigmoid, tanh, and hard activation functions.
"""

import time
from unittest.mock import patch

import numpy as np
import pytest

from mt_metadata.features.weights.activation_monotonic_weight_kernel import (
    ActivationMonotonicWeightKernel,
    ActivationStyleEnum,
    ThresholdEnum,
)
from mt_metadata.features.weights.monotonic_weight_kernel import StyleEnum

# =====================================================
# Fixtures for optimal efficiency
# =====================================================


@pytest.fixture
def default_activation_kernel():
    """Basic ActivationMonotonicWeightKernel with default values"""
    return ActivationMonotonicWeightKernel(
        threshold=ThresholdEnum.low_cut,
        style=StyleEnum.activation,
        activation_style=ActivationStyleEnum.sigmoid,
        steepness=1.0,
        transition_lower_bound=0.0,
        transition_upper_bound=1.0,
    )


@pytest.fixture
def sigmoid_kernel():
    """ActivationMonotonicWeightKernel with sigmoid activation"""
    return ActivationMonotonicWeightKernel(
        threshold=ThresholdEnum.low_cut,
        style=StyleEnum.activation,
        activation_style=ActivationStyleEnum.sigmoid,
        steepness=2.0,
        transition_lower_bound=0.0,
        transition_upper_bound=1.0,
    )


@pytest.fixture
def tanh_kernel():
    """ActivationMonotonicWeightKernel with tanh activation"""
    return ActivationMonotonicWeightKernel(
        threshold=ThresholdEnum.high_cut,
        style=StyleEnum.activation,
        activation_style=ActivationStyleEnum.tanh,
        steepness=5.0,
        transition_lower_bound=-1.0,
        transition_upper_bound=1.0,
    )


@pytest.fixture
def hard_sigmoid_kernel():
    """ActivationMonotonicWeightKernel with hard_sigmoid activation"""
    return ActivationMonotonicWeightKernel(
        threshold=ThresholdEnum.low_cut,
        style=StyleEnum.activation,
        activation_style=ActivationStyleEnum.hard_sigmoid,
        steepness=1.0,
        transition_lower_bound=0.2,
        transition_upper_bound=0.8,
    )


@pytest.fixture
def hard_tanh_kernel():
    """ActivationMonotonicWeightKernel with hard_tanh activation"""
    return ActivationMonotonicWeightKernel(
        threshold=ThresholdEnum.high_cut,
        style=StyleEnum.activation,
        activation_style=ActivationStyleEnum.hard_tanh,
        steepness=3.0,
        transition_lower_bound=-0.5,
        transition_upper_bound=0.5,
    )


@pytest.fixture
def infinite_bounds_kernel():
    """ActivationMonotonicWeightKernel with infinite bounds for testing fallback"""
    return ActivationMonotonicWeightKernel(
        threshold=ThresholdEnum.low_cut,
        style=StyleEnum.activation,
        activation_style=ActivationStyleEnum.sigmoid,
        steepness=1.0,
        transition_lower_bound=float("-inf"),
        transition_upper_bound=float("inf"),
    )


@pytest.fixture
def test_values_simple():
    """Simple test values for normalization and evaluation"""
    return np.array([0.0, 0.25, 0.5, 0.75, 1.0])


@pytest.fixture
def test_values_extended():
    """Extended test values including edge cases"""
    return np.array([-1.0, -0.5, 0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0])


@pytest.fixture
def large_test_array():
    """Large array for performance testing"""
    return np.linspace(-2.0, 2.0, 1000)


# =====================================================
# Test Classes
# =====================================================


class TestEnumerations:
    """Test ThresholdEnum and ActivationStyleEnum values and behavior"""

    def test_threshold_enum_values(self):
        """Test that ThresholdEnum has expected values"""
        expected_values = ["low cut", "high cut"]
        actual_values = [e.value for e in ThresholdEnum]
        assert actual_values == expected_values

    def test_activation_style_enum_values(self):
        """Test that ActivationStyleEnum has expected values"""
        expected_values = ["sigmoid", "hard_sigmoid", "tanh", "hard_tanh"]
        actual_values = [e.value for e in ActivationStyleEnum]
        assert actual_values == expected_values

    def test_threshold_enum_membership(self):
        """Test enum membership for threshold values"""
        assert "low cut" in [e.value for e in ThresholdEnum]
        assert "high cut" in [e.value for e in ThresholdEnum]
        assert "invalid" not in [e.value for e in ThresholdEnum]

    def test_activation_style_enum_membership(self):
        """Test enum membership for activation style values"""
        assert "sigmoid" in [e.value for e in ActivationStyleEnum]
        assert "tanh" in [e.value for e in ActivationStyleEnum]
        assert "hard_sigmoid" in [e.value for e in ActivationStyleEnum]
        assert "hard_tanh" in [e.value for e in ActivationStyleEnum]
        assert "invalid" not in [e.value for e in ActivationStyleEnum]


class TestActivationMonotonicWeightKernelFixtures:
    """Test that all fixtures work correctly"""

    def test_fixtures_work(
        self,
        default_activation_kernel,
        sigmoid_kernel,
        tanh_kernel,
        hard_sigmoid_kernel,
        hard_tanh_kernel,
        infinite_bounds_kernel,
    ):
        """Verify all fixtures create valid instances"""
        assert isinstance(default_activation_kernel, ActivationMonotonicWeightKernel)
        assert isinstance(sigmoid_kernel, ActivationMonotonicWeightKernel)
        assert isinstance(tanh_kernel, ActivationMonotonicWeightKernel)
        assert isinstance(hard_sigmoid_kernel, ActivationMonotonicWeightKernel)
        assert isinstance(hard_tanh_kernel, ActivationMonotonicWeightKernel)
        assert isinstance(infinite_bounds_kernel, ActivationMonotonicWeightKernel)


class TestActivationMonotonicWeightKernelInstantiation:
    """Test various ways to instantiate ActivationMonotonicWeightKernel"""

    def test_default_instantiation(self):
        """Test creating with default values"""
        kernel = ActivationMonotonicWeightKernel(
            threshold=ThresholdEnum.low_cut,
            style=StyleEnum.activation,
            activation_style=ActivationStyleEnum.sigmoid,
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        assert kernel.threshold == "low cut"
        assert kernel.activation_style == "sigmoid"
        assert kernel.steepness == 1.0
        assert kernel.transition_lower_bound == 0.0
        assert kernel.transition_upper_bound == 1.0

    def test_custom_instantiation(self):
        """Test creating with custom values"""
        kernel = ActivationMonotonicWeightKernel(
            threshold=ThresholdEnum.high_cut,
            style=StyleEnum.activation,
            activation_style=ActivationStyleEnum.tanh,
            steepness=3.5,
            transition_lower_bound=0.1,
            transition_upper_bound=0.9,
        )

        assert kernel.threshold == "high cut"
        assert kernel.activation_style == "tanh"
        assert kernel.steepness == 3.5
        assert kernel.transition_lower_bound == 0.1
        assert kernel.transition_upper_bound == 0.9

    def test_string_enum_conversion(self):
        """Test that string values are properly converted to enums"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="hard_sigmoid",
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        assert isinstance(kernel.threshold, str)
        assert isinstance(kernel.activation_style, str)
        assert kernel.threshold == "low cut"
        assert kernel.activation_style == "hard_sigmoid"

    def test_invalid_threshold_value(self):
        """Test that invalid threshold values raise ValidationError"""
        with pytest.raises(ValueError):
            ActivationMonotonicWeightKernel(
                threshold="invalid_threshold",
                style="activation",
                activation_style="sigmoid",
                steepness=1.0,
                transition_lower_bound=0.0,
                transition_upper_bound=1.0,
            )

    def test_invalid_activation_style_value(self):
        """Test that invalid activation style values raise ValidationError"""
        with pytest.raises(ValueError):
            ActivationMonotonicWeightKernel(
                threshold="low cut",
                style="activation",
                activation_style="invalid_style",
                steepness=1.0,
                transition_lower_bound=0.0,
                transition_upper_bound=1.0,
            )

    def test_steepness_types(self):
        """Test different steepness value types"""
        # Float steepness
        kernel1 = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=2.5,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )
        assert kernel1.steepness == 2.5

        # Integer steepness (should convert to float)
        kernel2 = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=3,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )
        assert kernel2.steepness == 3.0
        assert isinstance(kernel2.steepness, float)


class TestActivationMonotonicWeightKernelNormalization:
    """Test the _normalize method behavior"""

    def test_normalize_finite_bounds_low_cut(self, test_values_simple):
        """Test normalization with finite bounds and low cut threshold"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        normalized = kernel._normalize(test_values_simple)
        expected = np.array([0.0, 0.25, 0.5, 0.75, 1.0])

        np.testing.assert_array_almost_equal(normalized, expected)

    def test_normalize_finite_bounds_high_cut(self, test_values_simple):
        """Test normalization with finite bounds and high cut threshold"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="high cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        normalized = kernel._normalize(test_values_simple)
        expected = np.array([1.0, 0.75, 0.5, 0.25, 0.0])  # Reversed for high cut

        np.testing.assert_array_almost_equal(normalized, expected)

    def test_normalize_infinite_bounds_fallback(self, test_values_simple):
        """Test normalization fallback behavior with infinite bounds"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=float("-inf"),
            transition_upper_bound=float("inf"),
        )

        with patch(
            "mt_metadata.features.weights.activation_monotonic_weight_kernel.logger.warning"
        ) as mock_warning:
            normalized = kernel._normalize(test_values_simple)
            expected = np.full_like(test_values_simple, 0.5)

            np.testing.assert_array_almost_equal(normalized, expected)
            mock_warning.assert_called_once()

    def test_normalize_clipping_behavior(self):
        """Test that normalization properly clips values outside bounds"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=0.2,
            transition_upper_bound=0.8,
        )

        test_values = np.array([-1.0, 0.0, 0.5, 1.0, 2.0])
        normalized = kernel._normalize(test_values)

        # All values should be clipped to [0, 1]
        assert np.all(normalized >= 0.0)
        assert np.all(normalized <= 1.0)

    def test_normalize_empty_array(self):
        """Test normalization with empty array"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        empty_array = np.array([])
        normalized = kernel._normalize(empty_array)

        assert len(normalized) == 0
        assert normalized.shape == empty_array.shape

    def test_normalize_single_value(self):
        """Test normalization with single value"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=2.0,
        )

        single_value = np.array([1.0])
        normalized = kernel._normalize(single_value)
        expected = np.array([0.5])

        np.testing.assert_array_almost_equal(normalized, expected)


class TestActivationMonotonicWeightKernelEvaluation:
    """Test the evaluate method for different activation functions"""

    def test_sigmoid_evaluation(self, sigmoid_kernel, test_values_simple):
        """Test sigmoid activation evaluation"""
        evaluated = sigmoid_kernel.evaluate(test_values_simple)

        # Sigmoid should return values between 0 and 1
        assert np.all(evaluated >= 0.0)
        assert np.all(evaluated <= 1.0)

        # Sigmoid should be monotonic for normalized input
        normalized = sigmoid_kernel._normalize(test_values_simple)
        sorted_indices = np.argsort(normalized)
        assert np.all(np.diff(evaluated[sorted_indices]) >= 0)

    def test_tanh_evaluation(self, tanh_kernel, test_values_simple):
        """Test tanh activation evaluation"""
        evaluated = tanh_kernel.evaluate(test_values_simple)

        # Tanh should return values between 0 and 1
        assert np.all(evaluated >= 0.0)
        assert np.all(evaluated <= 1.0)

    def test_hard_sigmoid_evaluation(self, hard_sigmoid_kernel, test_values_simple):
        """Test hard_sigmoid activation evaluation"""
        evaluated = hard_sigmoid_kernel.evaluate(test_values_simple)

        # Hard sigmoid should return values between 0 and 1
        assert np.all(evaluated >= 0.0)
        assert np.all(evaluated <= 1.0)

    def test_hard_tanh_evaluation(self, hard_tanh_kernel, test_values_simple):
        """Test hard_tanh activation evaluation"""
        evaluated = hard_tanh_kernel.evaluate(test_values_simple)

        # Hard tanh should return values between 0 and 1
        assert np.all(evaluated >= 0.0)
        assert np.all(evaluated <= 1.0)

    def test_invalid_activation_style_error(self):
        """Test that invalid activation styles raise ValueError"""
        # Create a kernel with valid parameters first
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            style="activation",
            activation_style="sigmoid",
            steepness=1.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        # Test by directly modifying the internal activation_style
        # This simulates what would happen if an invalid style was somehow set
        original_style = kernel.activation_style

        # Temporarily modify for testing
        kernel.__dict__["activation_style"] = "invalid_style"

        with pytest.raises(ValueError, match="Unsupported activation style"):
            kernel.evaluate(np.array([0.5]))

        # Restore original style
        kernel.__dict__["activation_style"] = original_style

    def test_steepness_effect_sigmoid(self):
        """Test that steepness affects sigmoid transition sharpness"""
        test_values = np.array([0.4, 0.5, 0.6])

        # Low steepness - gradual transition
        kernel_low = ActivationMonotonicWeightKernel(
            activation_style="sigmoid",
            steepness=0.5,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        # High steepness - sharp transition
        kernel_high = ActivationMonotonicWeightKernel(
            activation_style="sigmoid",
            steepness=10.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        eval_low = kernel_low.evaluate(test_values)
        eval_high = kernel_high.evaluate(test_values)

        # High steepness should have sharper transition (greater difference between edges)
        diff_low = eval_low[2] - eval_low[0]
        diff_high = eval_high[2] - eval_high[0]
        assert diff_high > diff_low

    def test_steepness_effect_tanh(self):
        """Test that steepness affects tanh transition sharpness"""
        test_values = np.array([0.4, 0.5, 0.6])

        # Low steepness - gradual transition
        kernel_low = ActivationMonotonicWeightKernel(
            activation_style="tanh",
            steepness=0.5,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        # High steepness - sharp transition
        kernel_high = ActivationMonotonicWeightKernel(
            activation_style="tanh",
            steepness=10.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        eval_low = kernel_low.evaluate(test_values)
        eval_high = kernel_high.evaluate(test_values)

        # High steepness should have sharper transition
        diff_low = eval_low[2] - eval_low[0]
        diff_high = eval_high[2] - eval_high[0]
        assert diff_high > diff_low


class TestActivationMonotonicWeightKernelValidation:
    """Test Pydantic validation behaviors"""

    def test_threshold_enum_validation(self):
        """Test threshold enum validation"""
        for threshold_value in ["low cut", "high cut"]:
            kernel = ActivationMonotonicWeightKernel(threshold=threshold_value)
            assert kernel.threshold == threshold_value

    def test_activation_style_enum_validation(self):
        """Test activation style enum validation"""
        for style_value in ["sigmoid", "hard_sigmoid", "tanh", "hard_tanh"]:
            kernel = ActivationMonotonicWeightKernel(activation_style=style_value)
            assert kernel.activation_style == style_value

    def test_steepness_validation(self):
        """Test steepness field validation"""
        # Valid steepness values
        for steepness in [0.1, 1.0, 5.0, 10.0]:
            kernel = ActivationMonotonicWeightKernel(steepness=steepness)
            assert kernel.steepness == steepness

    def test_bounds_validation(self):
        """Test bounds validation"""
        # Valid bounds
        kernel = ActivationMonotonicWeightKernel(
            transition_lower_bound=0.0, transition_upper_bound=1.0
        )
        assert kernel.transition_lower_bound == 0.0
        assert kernel.transition_upper_bound == 1.0


class TestActivationMonotonicWeightKernelSerialization:
    """Test serialization and deserialization"""

    def test_to_dict(self, sigmoid_kernel):
        """Test serialization to dictionary"""
        kernel_dict = sigmoid_kernel.to_dict()

        assert isinstance(kernel_dict, dict)
        assert "activation_monotonic_weight_kernel" in kernel_dict

        inner_dict = kernel_dict["activation_monotonic_weight_kernel"]
        assert inner_dict["threshold"] == "low cut"
        assert inner_dict["activation_style"] == "sigmoid"
        assert inner_dict["steepness"] == 2.0

    def test_model_copy(self, hard_sigmoid_kernel):
        """Test Pydantic model copy functionality"""
        copied_kernel = hard_sigmoid_kernel.model_copy()

        assert copied_kernel.threshold == hard_sigmoid_kernel.threshold
        assert copied_kernel.activation_style == hard_sigmoid_kernel.activation_style
        assert copied_kernel.steepness == hard_sigmoid_kernel.steepness
        assert copied_kernel is not hard_sigmoid_kernel  # Different instances


class TestActivationMonotonicWeightKernelPerformance:
    """Test performance characteristics"""

    def test_instantiation_performance(self):
        """Test that instantiation is reasonably fast"""
        start_time = time.time()

        for _ in range(100):
            ActivationMonotonicWeightKernel(
                threshold="low cut", activation_style="sigmoid", steepness=1.0
            )

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Should complete 100 instantiations in less than 1 second
        assert elapsed_time < 1.0

    def test_evaluation_performance(self, sigmoid_kernel, large_test_array):
        """Test that evaluation is reasonably fast for large arrays"""
        start_time = time.time()

        result = sigmoid_kernel.evaluate(large_test_array)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Should complete evaluation of 1000 values in less than 0.1 seconds
        assert elapsed_time < 0.1
        assert len(result) == len(large_test_array)

    def test_normalization_performance(self, tanh_kernel, large_test_array):
        """Test that normalization is reasonably fast for large arrays"""
        start_time = time.time()

        result = tanh_kernel._normalize(large_test_array)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Should complete normalization of 1000 values in less than 0.1 seconds
        assert elapsed_time < 0.1
        assert len(result) == len(large_test_array)


class TestActivationMonotonicWeightKernelEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_zero_steepness_sigmoid(self):
        """Test sigmoid behavior with very small steepness"""
        kernel = ActivationMonotonicWeightKernel(
            activation_style="sigmoid",
            steepness=0.001,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        test_values = np.array([0.0, 0.5, 1.0])
        result = kernel.evaluate(test_values)

        # With very low steepness, sigmoid should be nearly flat around 0.5
        assert np.all(np.abs(result - 0.5) < 0.1)

    def test_high_steepness_sigmoid(self):
        """Test sigmoid behavior with very high steepness"""
        kernel = ActivationMonotonicWeightKernel(
            activation_style="sigmoid",
            steepness=100.0,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        test_values = np.array([0.0, 0.5, 1.0])
        result = kernel.evaluate(test_values)

        # With high steepness, sigmoid should be step-like
        assert result[0] < 0.1  # Near 0
        assert 0.4 < result[1] < 0.6  # Near 0.5
        assert result[2] > 0.9  # Near 1

    def test_extreme_bounds(self):
        """Test with very large but finite bounds"""
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            activation_style="tanh",
            steepness=1.0,
            transition_lower_bound=-1e6,
            transition_upper_bound=1e6,
        )

        test_values = np.array([-1e5, 0.0, 1e5])
        result = kernel.evaluate(test_values)

        assert np.all(np.isfinite(result))
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)

    def test_nan_and_inf_input_values(self):
        """Test behavior with NaN and infinite input values"""
        kernel = ActivationMonotonicWeightKernel(
            transition_lower_bound=0.0, transition_upper_bound=1.0
        )

        test_values = np.array([np.nan, np.inf, -np.inf, 0.5])

        # Should handle gracefully - might produce NaN for invalid inputs
        result = kernel.evaluate(test_values)

        # At least the valid input should produce valid output
        assert np.isfinite(result[3])
        assert 0.0 <= result[3] <= 1.0


class TestActivationMonotonicWeightKernelParametrized:
    """Parametrized tests for comprehensive coverage"""

    @pytest.mark.parametrize("threshold", ["low cut", "high cut"])
    def test_threshold_values(self, threshold):
        """Test all threshold enum values"""
        kernel = ActivationMonotonicWeightKernel(threshold=threshold)
        assert kernel.threshold == threshold

    @pytest.mark.parametrize(
        "activation_style", ["sigmoid", "hard_sigmoid", "tanh", "hard_tanh"]
    )
    def test_activation_style_values(self, activation_style):
        """Test all activation style enum values"""
        kernel = ActivationMonotonicWeightKernel(activation_style=activation_style)
        assert kernel.activation_style == activation_style

    @pytest.mark.parametrize("steepness", [0.1, 1.0, 5.0, 10.0])
    def test_steepness_values(self, steepness):
        """Test various steepness values"""
        kernel = ActivationMonotonicWeightKernel(steepness=steepness)
        assert kernel.steepness == steepness

    @pytest.mark.parametrize(
        "activation_style,expected_range",
        [
            ("sigmoid", (0.0, 1.0)),
            ("hard_sigmoid", (0.0, 1.0)),
            ("tanh", (0.0, 1.0)),
            ("hard_tanh", (0.0, 1.0)),
        ],
    )
    def test_activation_output_ranges(self, activation_style, expected_range):
        """Test that all activation functions return values in expected range"""
        kernel = ActivationMonotonicWeightKernel(
            activation_style=activation_style,
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        test_values = np.linspace(-1.0, 2.0, 100)
        result = kernel.evaluate(test_values)

        assert np.all(result >= expected_range[0])
        assert np.all(result <= expected_range[1])

    @pytest.mark.parametrize(
        "bound_pairs", [(-1.0, 1.0), (0.0, 1.0), (0.2, 0.8), (-10.0, 10.0), (-0.5, 0.5)]
    )
    def test_normalization_consistency(self, bound_pairs):
        """Test normalization consistency across different bound pairs"""
        lower, upper = bound_pairs
        kernel = ActivationMonotonicWeightKernel(
            threshold="low cut",
            transition_lower_bound=lower,
            transition_upper_bound=upper,
        )

        # Test boundary values
        boundary_values = np.array([lower, (lower + upper) / 2, upper])
        normalized = kernel._normalize(boundary_values)

        np.testing.assert_array_almost_equal(normalized, [0.0, 0.5, 1.0], decimal=10)

    @pytest.mark.parametrize("array_size", [1, 10, 100, 1000])
    def test_evaluation_array_sizes(self, array_size):
        """Test evaluation with different array sizes"""
        kernel = ActivationMonotonicWeightKernel(
            activation_style="sigmoid",
            transition_lower_bound=0.0,
            transition_upper_bound=1.0,
        )

        test_values = np.linspace(0.0, 1.0, array_size)
        result = kernel.evaluate(test_values)

        assert len(result) == array_size
        assert np.all(np.isfinite(result))
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)
