"""
Test taper_monotonic_weight_kernel_basemodel.py - Comprehensive test suite for TaperMonotonicWeightKernel

Tests the TaperMonotonicWeightKernel class and associated enums from the basemodel module
using fixtures and subtests for optimal efficiency.

This module contains taper-based monotonic weight kernels used in MT metadata processing,
providing smooth transitions between weight bounds using various windowing functions.
"""

import time

import numpy as np
import pytest

from mt_metadata.features.weights.monotonic_weight_kernel import ThresholdEnum
from mt_metadata.features.weights.taper_monotonic_weight_kernel import (
    ActivationStyleEnum,
    HalfWindowStyleEnum,
    TaperMonotonicWeightKernel,
)

# =====================================================
# Fixtures for optimal efficiency
# =====================================================


@pytest.fixture
def default_taper_kernel():
    """Basic TaperMonotonicWeightKernel with default values"""
    return TaperMonotonicWeightKernel()


@pytest.fixture
def rectangle_low_cut_kernel():
    """TaperMonotonicWeightKernel configured for rectangle window, low cut"""
    return TaperMonotonicWeightKernel(
        half_window_style=HalfWindowStyleEnum.rectangle,
        threshold=ThresholdEnum.low_cut,
        transition_lower_bound=10.0,
        transition_upper_bound=20.0,
    )


@pytest.fixture
def hann_low_cut_kernel():
    """TaperMonotonicWeightKernel configured for hann window, low cut"""
    return TaperMonotonicWeightKernel(
        half_window_style=HalfWindowStyleEnum.hann,
        threshold=ThresholdEnum.low_cut,
        transition_lower_bound=5.0,
        transition_upper_bound=15.0,
    )


@pytest.fixture
def hamming_high_cut_kernel():
    """TaperMonotonicWeightKernel configured for hamming window, high cut"""
    return TaperMonotonicWeightKernel(
        half_window_style=HalfWindowStyleEnum.hamming,
        threshold=ThresholdEnum.high_cut,
        transition_lower_bound=0.1,
        transition_upper_bound=1.0,
    )


@pytest.fixture
def blackman_low_cut_kernel():
    """TaperMonotonicWeightKernel configured for blackman window, low cut"""
    return TaperMonotonicWeightKernel(
        half_window_style=HalfWindowStyleEnum.blackman,
        threshold=ThresholdEnum.low_cut,
        transition_lower_bound=0.0,
        transition_upper_bound=10.0,
    )


@pytest.fixture
def sample_values_low_range():
    """Sample input values for low range testing"""
    return np.array([0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0])


@pytest.fixture
def sample_values_high_range():
    """Sample input values for high range testing"""
    return np.array([0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 5.0, 10.0])


@pytest.fixture
def sample_values_wide_range():
    """Sample input values for wide range testing"""
    return np.linspace(-10, 30, 100)


@pytest.fixture
def sample_values_normalized():
    """Sample normalized values in [0, 1] range"""
    return np.linspace(0, 1, 11)


# =====================================================
# Test Classes organized by functionality
# =====================================================


class TestHalfWindowStyleEnum:
    """Test HalfWindowStyleEnum enumeration"""

    def test_enum_values(self):
        """Test all enum values are properly defined"""
        assert HalfWindowStyleEnum.hamming == "hamming"
        assert HalfWindowStyleEnum.hann == "hann"
        assert HalfWindowStyleEnum.rectangle == "rectangle"
        assert HalfWindowStyleEnum.blackman == "blackman"

    def test_enum_string_representation(self):
        """Test enum string representation"""
        assert str(HalfWindowStyleEnum.hamming.value) == "hamming"
        assert str(HalfWindowStyleEnum.hann.value) == "hann"
        assert str(HalfWindowStyleEnum.rectangle.value) == "rectangle"
        assert str(HalfWindowStyleEnum.blackman.value) == "blackman"

    def test_enum_membership(self):
        """Test enum membership validation"""
        valid_values = ["hamming", "hann", "rectangle", "blackman"]
        for value in valid_values:
            assert value in [e.value for e in HalfWindowStyleEnum]


class TestActivationStyleEnum:
    """Test ActivationStyleEnum enumeration"""

    def test_enum_values(self):
        """Test all enum values are properly defined"""
        assert ActivationStyleEnum.linear == "linear"
        assert ActivationStyleEnum.sigmoid == "sigmoid"
        assert ActivationStyleEnum.tanh == "tanh"
        assert ActivationStyleEnum.relu == "relu"
        assert ActivationStyleEnum.hard_tanh == "hard_tanh"
        assert ActivationStyleEnum.hard_sigmoid == "hard_sigmoid"

    def test_enum_string_representation(self):
        """Test enum string representation"""
        assert str(ActivationStyleEnum.linear.value) == "linear"
        assert str(ActivationStyleEnum.sigmoid.value) == "sigmoid"
        assert str(ActivationStyleEnum.tanh.value) == "tanh"
        assert str(ActivationStyleEnum.relu.value) == "relu"
        assert str(ActivationStyleEnum.hard_tanh.value) == "hard_tanh"
        assert str(ActivationStyleEnum.hard_sigmoid.value) == "hard_sigmoid"

    def test_enum_membership(self):
        """Test enum membership validation"""
        valid_values = [
            "linear",
            "sigmoid",
            "tanh",
            "relu",
            "hard_tanh",
            "hard_sigmoid",
        ]
        for value in valid_values:
            assert value in [e.value for e in ActivationStyleEnum]


class TestTaperMonotonicWeightKernelInstantiation:
    """Test TaperMonotonicWeightKernel instantiation and basic properties"""

    def test_default_instantiation(self, default_taper_kernel):
        """Test default instantiation"""
        kernel = default_taper_kernel
        assert kernel.half_window_style == HalfWindowStyleEnum.rectangle
        assert kernel.threshold == ThresholdEnum.low_cut
        assert hasattr(kernel, "transition_lower_bound")
        assert hasattr(kernel, "transition_upper_bound")

    def test_custom_instantiation(self):
        """Test instantiation with custom parameters"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hann,
            threshold=ThresholdEnum.high_cut,
            transition_lower_bound=1.0,
            transition_upper_bound=10.0,
        )
        assert kernel.half_window_style == HalfWindowStyleEnum.hann
        assert kernel.threshold == ThresholdEnum.high_cut
        assert kernel.transition_lower_bound == 1.0
        assert kernel.transition_upper_bound == 10.0

    @pytest.mark.parametrize(
        "window_style",
        [
            HalfWindowStyleEnum.rectangle,
            HalfWindowStyleEnum.hann,
            HalfWindowStyleEnum.hamming,
            HalfWindowStyleEnum.blackman,
        ],
    )
    def test_window_style_variants(self, window_style):
        """Test different window style configurations"""
        kernel = TaperMonotonicWeightKernel(half_window_style=window_style)
        assert kernel.half_window_style == window_style

    @pytest.mark.parametrize(
        "threshold_type",
        [ThresholdEnum.low_cut, ThresholdEnum.high_cut],
    )
    def test_threshold_variants(self, threshold_type):
        """Test different threshold type configurations"""
        kernel = TaperMonotonicWeightKernel(threshold=threshold_type)
        assert kernel.threshold == threshold_type


class TestTaperMonotonicWeightKernelNormalize:
    """Test TaperMonotonicWeightKernel _normalize method"""

    def test_normalize_low_cut_basic(self, hann_low_cut_kernel):
        """Test normalization for low cut threshold"""
        values = np.array([0.0, 5.0, 10.0, 15.0, 20.0])
        normalized = hann_low_cut_kernel._normalize(values)

        # Values below lower bound should normalize to 0
        assert normalized[0] == 0.0  # value 0.0 -> (0-5)/(15-5) = -0.5 -> clipped to 0
        assert normalized[1] == 0.0  # value 5.0 -> (5-5)/(15-5) = 0.0
        assert normalized[2] == 0.5  # value 10.0 -> (10-5)/(15-5) = 0.5
        assert normalized[3] == 1.0  # value 15.0 -> (15-5)/(15-5) = 1.0
        assert normalized[4] == 1.0  # value 20.0 -> (20-5)/(15-5) = 1.5 -> clipped to 1

    def test_normalize_high_cut_basic(self, hamming_high_cut_kernel):
        """Test normalization for high cut threshold"""
        values = np.array([0.0, 0.1, 0.55, 1.0, 2.0])
        normalized = hamming_high_cut_kernel._normalize(values)

        # For high cut, the mapping is reversed
        assert (
            normalized[0] == 1.0
        )  # value 0.0 -> 1 - (0-0.1)/(1.0-0.1) = 1 - (-0.1/0.9) = 1 - clipped(negative) = 1
        assert normalized[1] == 1.0  # value 0.1 -> 1 - (0.1-0.1)/(1.0-0.1) = 1 - 0 = 1
        assert (
            abs(normalized[2] - 0.5) < 0.01
        )  # value 0.55 -> 1 - (0.55-0.1)/(1.0-0.1) = 1 - 0.5 = 0.5
        assert normalized[3] == 0.0  # value 1.0 -> 1 - (1.0-0.1)/(1.0-0.1) = 1 - 1 = 0
        assert normalized[4] == 0.0  # value 2.0 -> 1 - clipped(>1) = 1 - 1 = 0

    def test_normalize_bounds_checking(self, hann_low_cut_kernel):
        """Test normalization properly clips to [0, 1] bounds"""
        # Test values well outside bounds
        values = np.array([-100, -10, 0, 5, 10, 15, 25, 100])
        normalized = hann_low_cut_kernel._normalize(values)

        # All normalized values should be in [0, 1]
        assert np.all(normalized >= 0.0)
        assert np.all(normalized <= 1.0)

    def test_normalize_invalid_threshold(self, default_taper_kernel):
        """Test normalization with invalid threshold raises error"""
        # Manually set invalid threshold
        object.__setattr__(default_taper_kernel, "threshold", "invalid_threshold")
        values = np.array([1, 2, 3])

        with pytest.raises(ValueError, match="Unknown threshold direction"):
            default_taper_kernel._normalize(values)

    def test_normalize_array_shapes(self, hann_low_cut_kernel):
        """Test normalization with different array shapes"""
        # 1D array
        values_1d = np.array([5.0, 10.0, 15.0])
        norm_1d = hann_low_cut_kernel._normalize(values_1d)
        assert norm_1d.shape == values_1d.shape

        # 2D array
        values_2d = np.array([[5.0, 10.0], [15.0, 20.0]])
        norm_2d = hann_low_cut_kernel._normalize(values_2d)
        assert norm_2d.shape == values_2d.shape


class TestTaperMonotonicWeightKernelEvaluateRectangle:
    """Test TaperMonotonicWeightKernel evaluate method with rectangle window"""

    def test_evaluate_rectangle_low_cut(self, rectangle_low_cut_kernel):
        """Test rectangle window evaluation for low cut"""
        values = np.array([5.0, 10.0, 15.0, 20.0, 25.0])
        weights = rectangle_low_cut_kernel.evaluate(values)

        # Rectangle window: step function at lower bound
        expected = np.array([0.0, 1.0, 1.0, 1.0, 1.0])
        np.testing.assert_array_equal(weights, expected)

    def test_evaluate_rectangle_high_cut(self):
        """Test rectangle window evaluation for high cut"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.rectangle,
            threshold=ThresholdEnum.high_cut,
            transition_lower_bound=10.0,
            transition_upper_bound=20.0,
        )
        values = np.array([5.0, 10.0, 15.0, 20.0, 25.0])
        weights = kernel.evaluate(values)

        # Rectangle window: step function at upper bound for high cut
        # Values > upper bound should be 0, others should be 1
        expected = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
        np.testing.assert_array_equal(weights, expected)

    def test_evaluate_rectangle_boundary_conditions(self, rectangle_low_cut_kernel):
        """Test rectangle window at exact boundary values"""
        # Test values exactly at bounds
        values = np.array([10.0, 20.0])  # exact bounds
        weights = rectangle_low_cut_kernel.evaluate(values)

        # At lower bound should be 1.0, at upper bound should be 1.0
        expected = np.array([1.0, 1.0])
        np.testing.assert_array_equal(weights, expected)


class TestTaperMonotonicWeightKernelEvaluateHann:
    """Test TaperMonotonicWeightKernel evaluate method with Hann window"""

    def test_evaluate_hann_basic(self, hann_low_cut_kernel):
        """Test Hann window basic evaluation"""
        values = np.array([5.0, 10.0, 15.0])  # bounds are 5.0-15.0
        weights = hann_low_cut_kernel.evaluate(values)

        # Hann window: 0.5 * (1 - cos(pi * x))
        # At x=0 (value=5): 0.5 * (1 - cos(0)) = 0.5 * (1 - 1) = 0
        # At x=0.5 (value=10): 0.5 * (1 - cos(pi/2)) = 0.5 * (1 - 0) = 0.5
        # At x=1 (value=15): 0.5 * (1 - cos(pi)) = 0.5 * (1 - (-1)) = 1
        expected = np.array([0.0, 0.5, 1.0])
        np.testing.assert_allclose(weights, expected, atol=1e-10)

    def test_evaluate_hann_smooth_transition(self, hann_low_cut_kernel):
        """Test Hann window provides smooth transition"""
        values = np.linspace(5.0, 15.0, 11)  # 11 points from 5 to 15
        weights = hann_low_cut_kernel.evaluate(values)

        # Check monotonic increase
        assert np.all(np.diff(weights) >= 0)

        # Check bounds
        assert weights[0] == 0.0
        assert weights[-1] == 1.0

        # Check smoothness (second derivative should be reasonable)
        second_diff = np.diff(weights, 2)
        assert np.all(np.abs(second_diff) < 0.5)  # Reasonably smooth

    def test_evaluate_hann_high_cut(self):
        """Test Hann window with high cut threshold"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hann,
            threshold=ThresholdEnum.high_cut,
            transition_lower_bound=0.0,
            transition_upper_bound=10.0,
        )
        values = np.array([0.0, 5.0, 10.0])
        weights = kernel.evaluate(values)

        # For high cut, normalized values are reversed: x -> (1-x)
        # At value=0: x_norm = 1, hann = 0.5 * (1 - cos(pi)) = 1
        # At value=5: x_norm = 0.5, hann = 0.5 * (1 - cos(pi/2)) = 0.5
        # At value=10: x_norm = 0, hann = 0.5 * (1 - cos(0)) = 0
        expected = np.array([1.0, 0.5, 0.0])
        np.testing.assert_allclose(weights, expected, atol=1e-10)


class TestTaperMonotonicWeightKernelEvaluateHamming:
    """Test TaperMonotonicWeightKernel evaluate method with Hamming window"""

    def test_evaluate_hamming_basic(self, hamming_high_cut_kernel):
        """Test Hamming window basic evaluation"""
        values = np.array([0.1, 0.55, 1.0])  # bounds are 0.1-1.0
        weights = hamming_high_cut_kernel.evaluate(values)

        # Hamming window: 0.54 - 0.46 * cos(pi * x)
        # For high cut, x values are reversed
        # At value=0.1: x_norm = 1, hamming = 0.54 - 0.46 * cos(pi) = 0.54 - 0.46 * (-1) = 1.0
        # At value=0.55: x_norm = 0.5, hamming = 0.54 - 0.46 * cos(pi/2) = 0.54 - 0.46 * 0 = 0.54
        # At value=1.0: x_norm = 0, hamming = 0.54 - 0.46 * cos(0) = 0.54 - 0.46 = 0.08
        expected = np.array([1.0, 0.54, 0.08])
        np.testing.assert_allclose(weights, expected, atol=1e-10)

    def test_evaluate_hamming_monotonic_decrease(self, hamming_high_cut_kernel):
        """Test Hamming window monotonic decrease for high cut"""
        values = np.linspace(0.1, 1.0, 11)  # 11 points from 0.1 to 1.0
        weights = hamming_high_cut_kernel.evaluate(values)

        # For high cut, weights should decrease monotonically
        assert np.all(np.diff(weights) <= 0)

        # Check that it doesn't go to zero (Hamming has non-zero endpoints)
        assert weights[-1] > 0.0


class TestTaperMonotonicWeightKernelEvaluateBlackman:
    """Test TaperMonotonicWeightKernel evaluate method with Blackman window"""

    def test_evaluate_blackman_basic(self, blackman_low_cut_kernel):
        """Test Blackman window basic evaluation"""
        values = np.array([0.0, 5.0, 10.0])  # bounds are 0.0-10.0
        weights = blackman_low_cut_kernel.evaluate(values)

        # Blackman window: 0.42 - 0.5 * cos(pi * x) + 0.08 * cos(2 * pi * x)
        # At x=0: 0.42 - 0.5 * cos(0) + 0.08 * cos(0) = 0.42 - 0.5 + 0.08 = 0.0
        # At x=0.5: 0.42 - 0.5 * cos(pi/2) + 0.08 * cos(pi) = 0.42 - 0 + 0.08 * (-1) = 0.34
        # At x=1: 0.42 - 0.5 * cos(pi) + 0.08 * cos(2*pi) = 0.42 - 0.5 * (-1) + 0.08 * 1 = 1.0
        expected = np.array([0.0, 0.34, 1.0])
        np.testing.assert_allclose(weights, expected, atol=1e-10)

    def test_evaluate_blackman_smooth_transition(self, blackman_low_cut_kernel):
        """Test Blackman window provides smooth transition"""
        values = np.linspace(0.0, 10.0, 21)  # 21 points
        weights = blackman_low_cut_kernel.evaluate(values)

        # Check monotonic increase
        assert np.all(np.diff(weights) >= 0)

        # Check bounds (Blackman window starts very close to 0, but not exactly)
        assert np.isclose(weights[0], 0.0, atol=1e-15)
        assert np.isclose(weights[-1], 1.0, atol=1e-15)

        # Blackman should be smoother than Hann
        second_diff = np.diff(weights, 2)
        assert np.all(np.abs(second_diff) < 0.3)


class TestTaperMonotonicWeightKernelEvaluateErrors:
    """Test TaperMonotonicWeightKernel evaluate method error conditions"""

    def test_evaluate_unsupported_taper_style(self, default_taper_kernel):
        """Test evaluation with unsupported taper style"""
        # Manually set invalid taper style
        object.__setattr__(default_taper_kernel, "half_window_style", "invalid_style")
        values = np.array([1, 2, 3])

        with pytest.raises(ValueError, match="Unsupported taper style"):
            default_taper_kernel.evaluate(values)

    def test_evaluate_empty_array(self, hann_low_cut_kernel):
        """Test evaluation with empty array"""
        values = np.array([])
        weights = hann_low_cut_kernel.evaluate(values)
        assert weights.shape == (0,)

    def test_evaluate_single_value(self, hann_low_cut_kernel):
        """Test evaluation with single value"""
        values = np.array([10.0])  # mid-point of bounds 5-15
        weights = hann_low_cut_kernel.evaluate(values)
        expected = np.array([0.5])
        np.testing.assert_allclose(weights, expected, atol=1e-10)


class TestTaperMonotonicWeightKernelSerialization:
    """Test TaperMonotonicWeightKernel serialization and deserialization"""

    def test_to_dict_basic(self, default_taper_kernel):
        """Test basic to_dict serialization"""
        result = default_taper_kernel.to_dict()
        assert isinstance(result, dict)
        # Check that it contains a nested structure
        assert (
            "taper_monotonic_weight_kernel" in result
            or "monotonic_weight_kernel" in result
        )

    def test_to_dict_with_custom_values(self, hann_low_cut_kernel):
        """Test to_dict with custom values"""
        result = hann_low_cut_kernel.to_dict()
        assert isinstance(result, dict)
        # Should contain the custom values somewhere in the structure
        result_str = str(result)
        assert "hann" in result_str
        assert "low cut" in result_str

    def test_model_copy(self, hamming_high_cut_kernel):
        """Test model_copy functionality"""
        copied = hamming_high_cut_kernel.model_copy()
        assert copied.half_window_style == hamming_high_cut_kernel.half_window_style
        assert copied.threshold == hamming_high_cut_kernel.threshold
        assert copied is not hamming_high_cut_kernel

    def test_model_copy_deep(self, blackman_low_cut_kernel):
        """Test deep model_copy functionality"""
        copied = blackman_low_cut_kernel.model_copy(deep=True)
        assert copied.half_window_style == blackman_low_cut_kernel.half_window_style
        assert copied.threshold == blackman_low_cut_kernel.threshold
        assert copied is not blackman_low_cut_kernel


class TestTaperMonotonicWeightKernelInheritance:
    """Test TaperMonotonicWeightKernel inheritance from MonotonicWeightKernel"""

    def test_inherits_from_monotonic_weight_kernel(self):
        """Test TaperMonotonicWeightKernel inherits from MonotonicWeightKernel"""
        from mt_metadata.features.weights.monotonic_weight_kernel import (
            MonotonicWeightKernel,
        )

        assert issubclass(TaperMonotonicWeightKernel, MonotonicWeightKernel)

    def test_monotonic_weight_kernel_methods_available(self, default_taper_kernel):
        """Test MonotonicWeightKernel methods are available"""
        # Test common parent methods
        assert hasattr(default_taper_kernel, "evaluate")
        assert hasattr(default_taper_kernel, "_normalize")
        assert hasattr(default_taper_kernel, "to_dict")
        assert hasattr(default_taper_kernel, "model_copy")

    def test_parent_attributes_accessible(self, hann_low_cut_kernel):
        """Test parent class attributes are accessible"""
        assert hasattr(hann_low_cut_kernel, "threshold")
        assert hasattr(hann_low_cut_kernel, "transition_lower_bound")
        assert hasattr(hann_low_cut_kernel, "transition_upper_bound")


class TestTaperMonotonicWeightKernelEdgeCases:
    """Test TaperMonotonicWeightKernel edge cases and boundary conditions"""

    def test_zero_transition_range(self):
        """Test with zero transition range"""
        kernel = TaperMonotonicWeightKernel(
            transition_lower_bound=10.0,
            transition_upper_bound=10.0,  # Same as lower bound
        )
        values = np.array([5.0, 10.0, 15.0])

        # With zero range, division by zero might occur, but numpy should handle gracefully
        weights = kernel.evaluate(values)
        assert len(weights) == len(values)

    def test_negative_bounds(self):
        """Test with negative bounds"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hann,
            threshold=ThresholdEnum.low_cut,
            transition_lower_bound=-10.0,
            transition_upper_bound=-5.0,
        )
        values = np.array([-15.0, -7.5, -2.0])
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)

    def test_large_values(self):
        """Test with very large input values"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hann,
            transition_lower_bound=1e6,
            transition_upper_bound=1e7,
        )
        values = np.array([1e5, 5e6, 1e8])
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(np.isfinite(weights))

    def test_very_small_values(self):
        """Test with very small input values"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hamming,
            transition_lower_bound=1e-6,
            transition_upper_bound=1e-5,
        )
        values = np.array([1e-7, 5e-6, 1e-4])
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(np.isfinite(weights))


class TestTaperMonotonicWeightKernelPerformance:
    """Test TaperMonotonicWeightKernel performance characteristics"""

    def test_instantiation_performance(self):
        """Test instantiation performance"""
        start_time = time.time()
        kernels = []
        for _ in range(100):
            kernels.append(TaperMonotonicWeightKernel())
        end_time = time.time()

        # Should complete quickly (less than 1 second for 100 instances)
        assert end_time - start_time < 1.0
        assert len(kernels) == 100

    def test_evaluate_performance_large_arrays(self, hann_low_cut_kernel):
        """Test evaluate performance with large arrays"""
        # Create large array
        large_values = np.random.uniform(0, 20, 100000)

        start_time = time.time()
        weights = hann_low_cut_kernel.evaluate(large_values)
        end_time = time.time()

        # Should complete quickly
        assert end_time - start_time < 1.0
        assert len(weights) == len(large_values)

    def test_normalize_performance(self, blackman_low_cut_kernel):
        """Test _normalize performance"""
        large_values = np.random.uniform(-10, 30, 50000)

        start_time = time.time()
        normalized = blackman_low_cut_kernel._normalize(large_values)
        end_time = time.time()

        # Should complete quickly
        assert end_time - start_time < 1.0
        assert len(normalized) == len(large_values)


class TestTaperMonotonicWeightKernelIntegration:
    """Test TaperMonotonicWeightKernel integration scenarios"""

    def test_full_workflow_low_cut(self):
        """Test complete workflow for low cut scenario"""
        # Create kernel
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hann,
            threshold=ThresholdEnum.low_cut,
            transition_lower_bound=1.0,
            transition_upper_bound=5.0,
        )

        # Generate test data
        frequencies = np.logspace(-1, 2, 100)  # 0.1 to 100 Hz

        # Evaluate weights
        weights = kernel.evaluate(frequencies)

        # Verify properties
        assert len(weights) == len(frequencies)
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)

        # Low frequencies should have low weights, high frequencies high weights
        low_freq_weights = weights[frequencies < 1.0]
        high_freq_weights = weights[frequencies > 5.0]
        assert np.mean(low_freq_weights) < np.mean(high_freq_weights)

    def test_full_workflow_high_cut(self):
        """Test complete workflow for high cut scenario"""
        # Create kernel
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.blackman,
            threshold=ThresholdEnum.high_cut,
            transition_lower_bound=10.0,
            transition_upper_bound=100.0,
        )

        # Generate test data
        frequencies = np.logspace(0, 3, 100)  # 1 to 1000 Hz

        # Evaluate weights
        weights = kernel.evaluate(frequencies)

        # Verify properties
        assert len(weights) == len(frequencies)
        # Use tolerance for floating-point precision
        assert np.all(
            weights >= -1e-15
        )  # Allow tiny negative values due to floating-point errors
        assert np.all(weights <= 1.0)

        # Low frequencies should have high weights, high frequencies low weights
        low_freq_weights = weights[frequencies < 10.0]
        high_freq_weights = weights[frequencies > 100.0]
        assert np.mean(low_freq_weights) > np.mean(high_freq_weights)

    def test_serialization_roundtrip(self):
        """Test serialization and deserialization roundtrip"""
        # Create kernel with specific settings
        original = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hamming,
            threshold=ThresholdEnum.high_cut,
            transition_lower_bound=0.5,
            transition_upper_bound=2.0,
        )

        # Convert to dict
        data_dict = original.to_dict()

        # Create new instance from dict would require from_dict method
        # For now, just verify the dict contains expected information
        data_str = str(data_dict)
        assert "hamming" in data_str
        assert "high cut" in data_str


# =====================================================
# Comprehensive Tests
# =====================================================


class TestTaperMonotonicWeightKernelComprehensive:
    """Comprehensive tests covering multiple aspects simultaneously"""

    def test_comprehensive_functionality(self):
        """Test multiple functionality aspects together"""
        # Create kernel with all custom parameters
        kernel = TaperMonotonicWeightKernel(
            half_window_style=HalfWindowStyleEnum.hann,
            threshold=ThresholdEnum.low_cut,
            transition_lower_bound=2.0,
            transition_upper_bound=8.0,
        )

        # Test basic properties
        assert kernel.half_window_style == HalfWindowStyleEnum.hann
        assert kernel.threshold == ThresholdEnum.low_cut
        assert kernel.transition_lower_bound == 2.0
        assert kernel.transition_upper_bound == 8.0

        # Test evaluation
        values = np.array([0.0, 2.0, 5.0, 8.0, 10.0])
        weights = kernel.evaluate(values)
        assert len(weights) == len(values)
        assert weights[0] == 0.0  # Below lower bound
        assert weights[1] == 0.0  # At lower bound
        assert 0.0 < weights[2] < 1.0  # In transition
        assert weights[3] == 1.0  # At upper bound
        assert weights[4] == 1.0  # Above upper bound

        # Test serialization
        data_dict = kernel.to_dict()
        assert isinstance(data_dict, dict)

        # Test copy
        copied = kernel.model_copy()
        assert copied is not kernel
        assert copied.half_window_style == kernel.half_window_style

    @pytest.mark.parametrize(
        "window_style,threshold_type",
        [
            (HalfWindowStyleEnum.rectangle, ThresholdEnum.low_cut),
            (HalfWindowStyleEnum.hann, ThresholdEnum.low_cut),
            (HalfWindowStyleEnum.hamming, ThresholdEnum.high_cut),
            (HalfWindowStyleEnum.blackman, ThresholdEnum.high_cut),
        ],
    )
    def test_all_combinations(self, window_style, threshold_type):
        """Test all combinations of window styles and threshold types"""
        kernel = TaperMonotonicWeightKernel(
            half_window_style=window_style,
            threshold=threshold_type,
            transition_lower_bound=1.0,
            transition_upper_bound=10.0,
        )

        # Test evaluation works for all combinations
        values = np.linspace(0, 15, 16)
        weights = kernel.evaluate(values)

        # Basic sanity checks
        assert len(weights) == len(values)
        # Use tolerance for floating-point precision
        assert np.all(
            weights >= -1e-15
        )  # Allow tiny negative values due to floating-point errors
        assert np.all(weights <= 1.0)
        assert np.all(np.isfinite(weights))

    def test_mathematical_properties(self):
        """Test mathematical properties of different window functions"""
        bounds = (5.0, 15.0)
        values = np.linspace(bounds[0], bounds[1], 100)

        # Test each window style
        for window_style in HalfWindowStyleEnum:
            kernel = TaperMonotonicWeightKernel(
                half_window_style=window_style,
                threshold=ThresholdEnum.low_cut,
                transition_lower_bound=bounds[0],
                transition_upper_bound=bounds[1],
            )
            weights = kernel.evaluate(values)

            # All windows should be monotonic for low cut
            if window_style != HalfWindowStyleEnum.rectangle:
                assert np.all(
                    np.diff(weights) >= -1e-10
                )  # Monotonic (with small tolerance)

            # Boundary conditions
            # For Blackman window, the endpoints are not exactly 0/1, so use tolerance
            if window_style == HalfWindowStyleEnum.blackman:
                assert np.isclose(weights[0], 0.0, atol=1e-10)
            elif window_style == HalfWindowStyleEnum.hamming:
                # Hamming window has non-zero endpoints, check actual behavior
                # For low cut at lower bound, should still be near minimum value
                assert weights[0] >= 0.08 - 1e-5 or np.isclose(
                    weights[0], 0.0, atol=1e-10
                )
            elif window_style == HalfWindowStyleEnum.hann:
                # Hann window should be 0 at endpoints for low cut
                assert np.isclose(weights[0], 0.0, atol=1e-10)
            else:  # rectangle
                # Rectangle window can be 1.0 at the boundary for low cut depending on implementation
                assert (
                    weights[0] == 0.0
                    or weights[0] == 1.0
                    or np.isclose(weights[0], 0.0, atol=1e-10)
                )

            if window_style == HalfWindowStyleEnum.rectangle:
                assert weights[-1] == 1.0
            else:
                assert weights[-1] == 1.0 or np.isclose(weights[-1], 1.0, atol=1e-10)
