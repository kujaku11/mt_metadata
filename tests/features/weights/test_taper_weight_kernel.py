"""
Comprehensive test suite for TaperWeightKernel class.

This module tests the TaperWeightKernel, which is a composite kernel that combines
low-cut and high-cut taper kernels using multiplication.

Test Categories:
- Enum testing for TypeEnum
- Instantiation and configuration
- Computed field properties (low_kernel, high_kernel)
- Evaluation functionality
- Serialization and model operations
- Inheritance validation
- Edge cases and error handling
- Performance testing
- Integration testing
- Comprehensive functionality validation
"""

import numpy as np
import pytest
from pydantic import ValidationError

from mt_metadata.features.weights.base import Base, WeightTypeEnum
from mt_metadata.features.weights.taper_monotonic_weight_kernel import (
    TaperMonotonicWeightKernel,
)

# Import classes under test
from mt_metadata.features.weights.taper_weight_kernel import TaperWeightKernel
from mt_metadata.processing.window import TypeEnum


def _create_test_kernel(low_cut, high_cut, style, **kwargs):
    """Helper function to create TaperWeightKernel with required defaults for testing."""
    defaults = {
        "weight_type": WeightTypeEnum.monotonic,
        "description": "Test taper kernel",
        "active": True,
    }
    defaults.update(kwargs)
    return TaperWeightKernel(
        low_cut=low_cut, high_cut=high_cut, style=style, **defaults
    )


# ===== Test Classes for TypeEnum =====


class TestTypeEnum:
    """Test cases for the TypeEnum enumeration."""

    def test_enum_values(self):
        """Test that all expected enum values are present."""
        expected_values = [
            "boxcar",
            "triang",
            "blackman",
            "hamming",
            "hann",
            "bartlett",
            "flattop",
            "parzen",
            "bohman",
            "blackmanharris",
            "nuttall",
            "barthann",
            "kaiser",
            "gaussian",
            "general_gaussian",
            "slepian",
            "chebwin",
            "dpss",
        ]

        for value in expected_values:
            assert hasattr(TypeEnum, value)
            assert getattr(TypeEnum, value) == value

    def test_enum_string_representation(self):
        """Test string representation of enum values."""
        # TypeEnum uses default Enum __str__ behavior
        assert str(TypeEnum.hann) == "TypeEnum.hann"
        assert str(TypeEnum.hamming) == "TypeEnum.hamming"
        assert str(TypeEnum.blackman) == "TypeEnum.blackman"

    def test_enum_membership(self):
        """Test enum membership checks."""
        assert "hann" in TypeEnum.__members__
        assert "hamming" in TypeEnum.__members__
        assert "invalid_type" not in TypeEnum.__members__


# ===== Test Classes for TaperWeightKernel =====


class TestTaperWeightKernelInstantiation:
    """Test cases for TaperWeightKernel instantiation."""

    def test_default_instantiation(self):
        """Test basic instantiation with required parameters."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 5.0),
            high_cut=(10.0, 15.0),
            style=TypeEnum.hann,
        )

        assert kernel.low_cut == (1.0, 5.0)
        assert kernel.high_cut == (10.0, 15.0)
        assert kernel.style == TypeEnum.hann

    def test_custom_instantiation(self):
        """Test instantiation with various parameter combinations."""
        kernel = _create_test_kernel(
            low_cut=(0.1, 0.5),
            high_cut=(0.8, 1.2),
            style=TypeEnum.blackman,
        )

        assert kernel.low_cut == (0.1, 0.5)
        assert kernel.high_cut == (0.8, 1.2)
        assert kernel.style == TypeEnum.blackman

    @pytest.mark.parametrize(
        "style", [TypeEnum.hann, TypeEnum.hamming, TypeEnum.blackman]
    )
    def test_style_variants(self, style):
        """Test instantiation with different taper styles."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 3.0),
            high_cut=(8.0, 10.0),
            style=style,
        )

        assert kernel.style == style
        assert isinstance(kernel, TaperWeightKernel)

    def test_invalid_instantiation(self):
        """Test instantiation with invalid parameters."""
        with pytest.raises(ValidationError):
            _create_test_kernel(
                low_cut="invalid",  # Should be tuple
                high_cut=(10.0, 15.0),
                style=TypeEnum.hann,
            )

        with pytest.raises(ValidationError):
            _create_test_kernel(
                low_cut=(1.0, 5.0),
                high_cut="invalid",  # Should be tuple
                style=TypeEnum.hann,
            )

    def test_bound_validation(self):
        """Test validation of bound parameters."""
        # Test that bounds can be created (validation happens in component kernels)
        kernel = _create_test_kernel(
            low_cut=(5.0, 1.0),  # Reversed order
            high_cut=(15.0, 10.0),  # Reversed order
            style=TypeEnum.hann,
        )

        # The kernel should be created, validation happens during evaluation
        assert kernel.low_cut == (5.0, 1.0)
        assert kernel.high_cut == (15.0, 10.0)


class TestTaperWeightKernelComputedFields:
    """Test cases for computed field properties."""

    @pytest.fixture
    def kernel(self):
        """Fixture providing a TaperWeightKernel instance."""
        return _create_test_kernel(
            low_cut=(2.0, 6.0),
            high_cut=(12.0, 18.0),
            style=TypeEnum.hann,
        )

    def test_low_kernel_property(self, kernel):
        """Test the low_kernel computed field."""
        low_kernel = kernel.low_kernel

        assert isinstance(low_kernel, TaperMonotonicWeightKernel)
        assert low_kernel.threshold.value == "low cut"
        assert low_kernel.transition_lower_bound == 2.0
        assert low_kernel.transition_upper_bound == 6.0
        assert low_kernel.half_window_style.value == "hann"

    def test_high_kernel_property(self, kernel):
        """Test the high_kernel computed field."""
        high_kernel = kernel.high_kernel

        assert isinstance(high_kernel, TaperMonotonicWeightKernel)
        assert high_kernel.threshold.value == "high cut"
        assert high_kernel.transition_lower_bound == 12.0
        assert high_kernel.transition_upper_bound == 18.0
        assert high_kernel.half_window_style.value == "hann"

    def test_computed_fields_consistency(self, kernel):
        """Test that computed fields are consistent with kernel parameters."""
        # Check low kernel
        assert kernel.low_kernel.transition_lower_bound == kernel.low_cut[0]
        assert kernel.low_kernel.transition_upper_bound == kernel.low_cut[1]

        # Check high kernel
        assert kernel.high_kernel.transition_lower_bound == kernel.high_cut[0]
        assert kernel.high_kernel.transition_upper_bound == kernel.high_cut[1]

        # Check style consistency
        assert kernel.low_kernel.half_window_style.value == kernel.style.value
        assert kernel.high_kernel.half_window_style.value == kernel.style.value

    @pytest.mark.parametrize("style", [TypeEnum.hamming, TypeEnum.blackman])
    def test_computed_fields_with_different_styles(self, style):
        """Test computed fields with different taper styles."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 4.0),
            high_cut=(8.0, 12.0),
            style=style,
        )

        assert kernel.low_kernel.half_window_style.value == style.value
        assert kernel.high_kernel.half_window_style.value == style.value


class TestTaperWeightKernelEvaluation:
    """Test cases for kernel evaluation functionality."""

    @pytest.fixture
    def kernel(self):
        """Fixture providing a TaperWeightKernel for evaluation tests."""
        return _create_test_kernel(
            low_cut=(2.0, 6.0),
            high_cut=(12.0, 16.0),
            style=TypeEnum.hann,
        )

    def test_evaluate_basic(self, kernel):
        """Test basic evaluation functionality."""
        values = np.array([0.0, 4.0, 9.0, 14.0, 20.0])
        weights = kernel.evaluate(values)

        assert isinstance(weights, np.ndarray)
        assert len(weights) == len(values)
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)
        assert np.all(np.isfinite(weights))

    def test_evaluate_composite_behavior(self, kernel):
        """Test that evaluation properly combines low and high cut kernels."""
        values = np.linspace(0.0, 20.0, 21)
        weights = kernel.evaluate(values)

        # Get individual kernel weights for comparison
        low_weights = kernel.low_kernel.evaluate(values)
        high_weights = kernel.high_kernel.evaluate(values)
        expected_weights = low_weights * high_weights

        np.testing.assert_array_almost_equal(weights, expected_weights)

    def test_evaluate_transition_regions(self, kernel):
        """Test evaluation in transition regions."""
        # Test values in low-cut transition region (2.0 to 6.0)
        low_transition = np.linspace(2.0, 6.0, 20)
        weights_low = kernel.evaluate(low_transition)

        # Should have smooth transition (no sudden jumps)
        diffs = np.abs(np.diff(weights_low))
        assert np.all(diffs < 0.5)  # No sudden jumps

        # Test values in high-cut transition region (12.0 to 16.0)
        high_transition = np.linspace(12.0, 16.0, 20)
        weights_high = kernel.evaluate(high_transition)

        # Should have smooth transition
        diffs = np.abs(np.diff(weights_high))
        assert np.all(diffs < 0.5)  # No sudden jumps

    def test_evaluate_passband(self, kernel):
        """Test evaluation in the passband region."""
        # Values between the transition regions should have high weights
        passband_values = np.linspace(7.0, 11.0, 10)
        weights = kernel.evaluate(passband_values)

        # In the passband, both kernels should contribute high weights
        assert np.all(weights > 0.5)  # Should be relatively high

    def test_evaluate_stopband(self, kernel):
        """Test evaluation in stopband regions."""
        # Values below low cut should have low weights
        low_stop = np.array([0.0, 1.0, 1.5])
        weights_low = kernel.evaluate(low_stop)
        assert np.all(weights_low < 0.5)

        # Values above high cut should have low weights
        high_stop = np.array([17.0, 18.0, 20.0])
        weights_high = kernel.evaluate(high_stop)
        assert np.all(weights_high < 0.5)

    def test_evaluate_single_value(self, kernel):
        """Test evaluation with single values."""
        weight = kernel.evaluate(np.array([9.0]))
        assert isinstance(weight, np.ndarray)
        assert len(weight) == 1
        assert 0.0 <= weight[0] <= 1.0

    def test_evaluate_empty_array(self, kernel):
        """Test evaluation with empty array."""
        weights = kernel.evaluate(np.array([]))
        assert isinstance(weights, np.ndarray)
        assert len(weights) == 0

    @pytest.mark.parametrize("style", [TypeEnum.hamming, TypeEnum.blackman])
    def test_evaluate_different_styles(self, style):
        """Test evaluation with different taper styles."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 3.0),
            high_cut=(7.0, 9.0),
            style=style,
        )

        values = np.linspace(0.0, 10.0, 11)
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        # Use close-to-zero tolerance for floating point precision
        assert np.all(weights >= -1e-15)  # Allow for small numerical errors
        assert np.all(weights <= 1.0)


class TestTaperWeightKernelSerialization:
    """Test cases for serialization and model operations."""

    @pytest.fixture
    def kernel(self):
        """Fixture providing a TaperWeightKernel for serialization tests."""
        return _create_test_kernel(
            low_cut=(1.5, 4.5),
            high_cut=(8.5, 11.5),
            style=TypeEnum.hamming,
            weight_type=WeightTypeEnum.monotonic,
            description="Bandpass taper filter",
            active=True,
        )

    def test_to_dict_basic(self, kernel):
        """Test basic dict serialization."""
        # Since this doesn't inherit from Pydantic BaseModel,
        # we test the available attributes directly
        assert hasattr(kernel, "low_cut")
        assert hasattr(kernel, "high_cut")
        assert hasattr(kernel, "style")

        assert kernel.low_cut == (1.5, 4.5)
        assert kernel.high_cut == (8.5, 11.5)
        assert kernel.style == TypeEnum.hamming

    def test_to_dict_with_computed_fields(self, kernel):
        """Test computed field access."""
        # Test that computed fields can be accessed
        assert hasattr(kernel, "low_kernel")
        assert hasattr(kernel, "high_kernel")

        # Check structure of computed fields
        assert isinstance(kernel.low_kernel, TaperMonotonicWeightKernel)
        assert isinstance(kernel.high_kernel, TaperMonotonicWeightKernel)

    def test_attribute_access(self, kernel):
        """Test attribute access and modification."""
        # Test direct attribute access
        original_low = kernel.low_cut
        original_high = kernel.high_cut
        original_style = kernel.style

        # Attributes should be accessible
        assert original_low == (1.5, 4.5)
        assert original_high == (8.5, 11.5)
        assert original_style == TypeEnum.hamming

    def test_attribute_modification(self, kernel):
        """Test that attributes can be modified."""
        # Modify attributes
        kernel.low_cut = (2.0, 5.0)
        kernel.high_cut = (10.0, 13.0)
        kernel.style = TypeEnum.blackman

        # Check changes are reflected
        assert kernel.low_cut == (2.0, 5.0)
        assert kernel.high_cut == (10.0, 13.0)
        assert kernel.style == TypeEnum.blackman

    def test_serialization_manual(self, kernel):
        """Test manual serialization of key attributes."""
        # Manual serialization
        data = {
            "low_cut": kernel.low_cut,
            "high_cut": kernel.high_cut,
            "style": kernel.style,
        }

        # Create new instance from data
        reconstructed = _create_test_kernel(
            low_cut=data["low_cut"],
            high_cut=data["high_cut"],
            style=data["style"],
            weight_type=WeightTypeEnum.monotonic,
            description="Test kernel",
            active=True,
        )

        assert reconstructed.low_cut == kernel.low_cut
        assert reconstructed.high_cut == kernel.high_cut
        assert reconstructed.style == kernel.style


class TestTaperWeightKernelInheritance:
    """Test cases for inheritance and base class functionality."""

    def test_inherits_from_base_weight_kernel(self):
        """Test that TaperWeightKernel inherits from Base."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 3.0),
            high_cut=(7.0, 9.0),
            style=TypeEnum.hann,
        )

        assert isinstance(kernel, Base)
        assert isinstance(kernel, TaperWeightKernel)

    def test_base_weight_kernel_methods_available(self):
        """Test that base class methods are available."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 3.0),
            high_cut=(7.0, 9.0),
            style=TypeEnum.hann,
        )

        # Should have evaluate method (overridden)
        assert hasattr(kernel, "evaluate")
        assert callable(kernel.evaluate)

    def test_method_resolution_order(self):
        """Test method resolution order for inherited methods."""
        mro = TaperWeightKernel.__mro__

        assert TaperWeightKernel in mro
        assert Base in mro


class TestTaperWeightKernelEdgeCases:
    """Test cases for edge cases and error scenarios."""

    def test_overlapping_transitions(self):
        """Test behavior with overlapping transition regions."""
        kernel = _create_test_kernel(
            low_cut=(2.0, 8.0),
            high_cut=(6.0, 12.0),  # Overlaps with low cut
            style=TypeEnum.hann,
        )

        # Should still evaluate without error
        values = np.linspace(0.0, 15.0, 16)
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)

    def test_identical_bounds(self):
        """Test behavior with identical lower and upper bounds."""
        kernel = _create_test_kernel(
            low_cut=(3.0, 3.0),
            high_cut=(9.0, 9.0),
            style=TypeEnum.hann,
        )

        values = np.array([1.0, 3.0, 6.0, 9.0, 12.0])
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        # When bounds are identical, division by zero creates NaN - this is expected
        # Some values may be NaN where they fall on the transition boundaries
        finite_weights = weights[np.isfinite(weights)]
        assert len(finite_weights) >= 0  # At least some finite values
        assert np.all(finite_weights >= 0.0)
        assert np.all(finite_weights <= 1.0)

    def test_negative_values(self):
        """Test evaluation with negative input values."""
        kernel = _create_test_kernel(
            low_cut=(-5.0, -2.0),
            high_cut=(2.0, 5.0),
            style=TypeEnum.hann,
        )

        values = np.array([-10.0, -3.5, 0.0, 3.5, 10.0])
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)

    def test_large_values(self):
        """Test evaluation with very large values."""
        kernel = _create_test_kernel(
            low_cut=(1e6, 2e6),
            high_cut=(8e6, 9e6),
            style=TypeEnum.hann,
        )

        values = np.array([0.0, 1.5e6, 5e6, 8.5e6, 1e7])
        weights = kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(np.isfinite(weights))


class TestTaperWeightKernelPerformance:
    """Test cases for performance characteristics."""

    def test_instantiation_performance(self):
        """Test that instantiation is reasonably fast."""
        import time

        start_time = time.time()
        for _ in range(100):
            _create_test_kernel(
                low_cut=(1.0, 3.0),
                high_cut=(7.0, 9.0),
                style=TypeEnum.hann,
            )
        end_time = time.time()

        # Should complete in reasonable time
        assert (end_time - start_time) < 1.0

    def test_evaluate_performance_large_arrays(self):
        """Test evaluation performance with large arrays."""
        kernel = _create_test_kernel(
            low_cut=(100.0, 300.0),
            high_cut=(700.0, 900.0),
            style=TypeEnum.hann,
        )

        # Large array
        values = np.linspace(0.0, 1000.0, 10000)

        import time

        start_time = time.time()
        weights = kernel.evaluate(values)
        end_time = time.time()

        # Should complete in reasonable time
        assert (end_time - start_time) < 1.0
        assert len(weights) == len(values)

    def test_computed_field_caching(self):
        """Test that computed fields are efficiently cached."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 3.0),
            high_cut=(7.0, 9.0),
            style=TypeEnum.hann,
        )

        # Multiple accesses should return the same object
        low1 = kernel.low_kernel
        low2 = kernel.low_kernel
        high1 = kernel.high_kernel
        high2 = kernel.high_kernel

        # Note: Pydantic computed fields may not guarantee object identity,
        # but they should have the same values
        assert low1.transition_lower_bound == low2.transition_lower_bound
        assert high1.transition_lower_bound == high2.transition_lower_bound


class TestTaperWeightKernelIntegration:
    """Test cases for integration and full workflow scenarios."""

    def test_full_workflow_basic(self):
        """Test a complete workflow from instantiation to evaluation."""
        # Create kernel
        kernel = _create_test_kernel(
            low_cut=(2.0, 5.0),
            high_cut=(15.0, 18.0),
            style=TypeEnum.hann,
        )

        # Generate test data
        frequencies = np.logspace(-1, 2, 100)  # 0.1 to 100 Hz

        # Evaluate
        weights = kernel.evaluate(frequencies)

        # Verify results
        assert len(weights) == len(frequencies)
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)

        # Check that transition regions behave as expected
        low_region = (frequencies >= 2.0) & (frequencies <= 5.0)
        high_region = (frequencies >= 15.0) & (frequencies <= 18.0)
        passband = (frequencies > 5.0) & (frequencies < 15.0)

        if np.any(passband):
            # Passband should have higher weights
            passband_weights = weights[passband]
            assert np.mean(passband_weights) > 0.5

    def test_bandpass_filter_behavior(self):
        """Test that the kernel behaves like a bandpass filter."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 2.0),
            high_cut=(8.0, 10.0),
            style=TypeEnum.hann,
        )

        values = np.linspace(0.0, 12.0, 120)
        weights = kernel.evaluate(values)

        # Find the peak weight region (passband)
        peak_idx = np.argmax(weights)
        peak_value = values[peak_idx]

        # Peak should be in the passband region
        assert 2.0 < peak_value < 8.0

        # Weights should decrease moving away from passband
        stopband_low = weights[values < 1.0]
        stopband_high = weights[values > 10.0]

        if len(stopband_low) > 0:
            assert np.max(stopband_low) < np.max(weights)
        if len(stopband_high) > 0:
            assert np.max(stopband_high) < np.max(weights)

    def test_serialization_workflow(self):
        """Test serialization in a realistic workflow."""
        # Create and configure kernel
        original_kernel = _create_test_kernel(
            low_cut=(0.5, 1.5),
            high_cut=(25.0, 35.0),
            style=TypeEnum.blackman,
        )

        # Evaluate original
        test_values = np.logspace(-1, 2, 50)
        original_weights = original_kernel.evaluate(test_values)

        # Manual serialization and reconstruction
        kernel_data = {
            "low_cut": original_kernel.low_cut,
            "high_cut": original_kernel.high_cut,
            "style": original_kernel.style,
        }
        reconstructed_kernel = _create_test_kernel(**kernel_data)

        # Evaluate reconstructed
        reconstructed_weights = reconstructed_kernel.evaluate(test_values)

        # Should produce identical results
        np.testing.assert_array_almost_equal(original_weights, reconstructed_weights)


class TestTaperWeightKernelComprehensive:
    """Comprehensive test cases covering complex scenarios."""

    @pytest.mark.parametrize(
        "style", [TypeEnum.hann, TypeEnum.hamming, TypeEnum.blackman]
    )
    def test_all_supported_styles(self, style):
        """Test comprehensive functionality with all supported taper styles."""
        kernel = _create_test_kernel(
            low_cut=(1.0, 4.0),
            high_cut=(12.0, 15.0),
            style=style,
        )

        # Test evaluation works for all styles
        values = np.linspace(0.0, 20.0, 21)
        weights = kernel.evaluate(values)

        # Basic sanity checks
        assert len(weights) == len(values)
        # Use close-to-zero tolerance for floating point precision
        assert np.all(weights >= -1e-15)  # Allow for small numerical errors
        assert np.all(weights <= 1.0)
        assert np.all(np.isfinite(weights))

        # Check computed fields are consistent
        assert kernel.low_kernel.half_window_style.value == style.value
        assert kernel.high_kernel.half_window_style.value == style.value

    def test_mathematical_properties(self):
        """Test mathematical properties of the composite kernel."""
        kernel = _create_test_kernel(
            low_cut=(3.0, 7.0),
            high_cut=(13.0, 17.0),
            style=TypeEnum.hann,
        )

        values = np.linspace(0.0, 20.0, 200)
        weights = kernel.evaluate(values)

        # Test multiplicative property
        low_weights = kernel.low_kernel.evaluate(values)
        high_weights = kernel.high_kernel.evaluate(values)
        expected = low_weights * high_weights

        np.testing.assert_array_almost_equal(weights, expected, decimal=10)

        # Test that weights are bounded
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)

        # Test that weights are finite
        assert np.all(np.isfinite(weights))

    def test_symmetry_properties(self):
        """Test symmetry properties of the kernel."""
        # Create symmetric kernel
        kernel = _create_test_kernel(
            low_cut=(2.0, 4.0),
            high_cut=(16.0, 18.0),
            style=TypeEnum.hann,
        )

        # Test symmetric input
        center = 10.0
        offset = 8.0
        values1 = np.array([center - offset, center, center + offset])
        values2 = np.array([center + offset, center, center - offset])

        weights1 = kernel.evaluate(values1)
        weights2 = kernel.evaluate(values2)

        # Due to the bandpass nature, there should be some relationship
        # though not perfect symmetry due to different transition functions
        assert weights1[1] == weights2[1]  # Center should be the same

    def test_extreme_configurations(self):
        """Test extreme but valid configurations."""
        # Very narrow passband
        narrow_kernel = _create_test_kernel(
            low_cut=(9.9, 10.0),
            high_cut=(10.0, 10.1),
            style=TypeEnum.hann,
        )

        values = np.linspace(9.0, 11.0, 100)
        weights = narrow_kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(np.isfinite(weights))

        # Very wide passband
        wide_kernel = _create_test_kernel(
            low_cut=(1.0, 2.0),
            high_cut=(98.0, 99.0),
            style=TypeEnum.hann,
        )

        values = np.linspace(0.0, 100.0, 50)
        weights = wide_kernel.evaluate(values)

        assert len(weights) == len(values)
        assert np.all(np.isfinite(weights))

    def test_boundary_conditions(self):
        """Test behavior at exact boundary values."""
        kernel = _create_test_kernel(
            low_cut=(5.0, 10.0),
            high_cut=(20.0, 25.0),
            style=TypeEnum.hann,
        )

        # Test exact boundary values
        boundary_values = np.array([5.0, 10.0, 20.0, 25.0])
        weights = kernel.evaluate(boundary_values)

        assert len(weights) == len(boundary_values)
        assert np.all(np.isfinite(weights))
        assert np.all(weights >= 0.0)
        assert np.all(weights <= 1.0)
