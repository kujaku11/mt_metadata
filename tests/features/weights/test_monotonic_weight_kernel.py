"""
Test monotonic_weight_kernel_basemodel.py - Comprehensive test suite for MonotonicWeightKernel basemodel

Tests the MonotonicWeightKernel class, ThresholdEnum, and StyleEnum from the
basemodel module using fixtures and subtests for optimal efficiency.

This module contains the base classes and enumerations for monotonic weight kernels
used in MT metadata processing.
"""

import numpy as np
import pytest

from mt_metadata.features.weights.base import Base, WeightTypeEnum
from mt_metadata.features.weights.monotonic_weight_kernel import (
    MonotonicWeightKernel,
    StyleEnum,
    ThresholdEnum,
)


# Fixtures at module level for optimal efficiency
@pytest.fixture
def default_kernel():
    """Basic MonotonicWeightKernel with default values"""
    return MonotonicWeightKernel()


@pytest.fixture
def finite_bounds_kernel():
    """MonotonicWeightKernel with finite transition bounds"""
    return MonotonicWeightKernel(
        threshold="low cut",
        style="taper",
        transition_lower_bound=0.3,
        transition_upper_bound=0.8,
    )


@pytest.fixture
def infinite_bounds_kernel():
    """MonotonicWeightKernel with infinite transition bounds"""
    return MonotonicWeightKernel(
        threshold="high cut",
        style="activation",
        transition_lower_bound=float("-inf"),
        transition_upper_bound=float("inf"),
    )


@pytest.fixture
def mixed_bounds_kernel():
    """MonotonicWeightKernel with one finite and one infinite bound"""
    return MonotonicWeightKernel(
        threshold="low cut",
        style="activation",
        transition_lower_bound=0.5,
        transition_upper_bound=float("inf"),
    )


@pytest.fixture
def sample_values():
    """Sample numpy array for testing normalization"""
    return np.array([0.1, 0.3, 0.5, 0.8, 1.0])


@pytest.fixture
def large_sample_values():
    """Larger sample array for performance testing"""
    return np.linspace(0, 1, 1000)


# Class 1: Inheritance Tests
class TestMonotonicWeightKernelInheritance:
    """Test inheritance relationships and base class integration"""

    def test_inheritance_from_base(self):
        """Test that MonotonicWeightKernel inherits from Base"""
        kernel = MonotonicWeightKernel()
        assert isinstance(kernel, Base)
        assert isinstance(kernel, MonotonicWeightKernel)

    def test_method_resolution_order(self):
        """Test method resolution order includes Base"""
        mro = MonotonicWeightKernel.__mro__
        base_classes = [cls.__name__ for cls in mro]
        assert "Base" in base_classes
        assert "MonotonicWeightKernel" in base_classes

    def test_inherited_fields_from_base(self):
        """Test that fields from Base are accessible"""
        kernel = MonotonicWeightKernel()

        # Test inherited fields exist
        assert hasattr(kernel, "weight_type")
        assert hasattr(kernel, "description")
        assert hasattr(kernel, "active")

        # Test default values from Base
        assert kernel.weight_type == "monotonic"  # default from Base
        assert kernel.description is None  # default from Base
        assert kernel.active is None  # default from Base

    def test_base_weight_type_enum_integration(self):
        """Test that WeightTypeEnum from base works correctly"""
        # Test that we can create a kernel with different weight types
        kernel = MonotonicWeightKernel(weight_type="custom")
        assert kernel.weight_type == "custom"

        # Test that the enum values work
        kernel = MonotonicWeightKernel(weight_type=WeightTypeEnum.learned)
        assert kernel.weight_type == "learned"

        # Test default value
        kernel = MonotonicWeightKernel()
        assert kernel.weight_type == WeightTypeEnum.monotonic

    def test_inherited_evaluate_method(self):
        """Test that evaluate method is properly inherited/overridden"""
        kernel = MonotonicWeightKernel()

        # Base class evaluate should raise NotImplementedError
        # MonotonicWeightKernel should override this
        # For now just test that method exists
        assert hasattr(kernel, "evaluate")
        assert callable(getattr(kernel, "evaluate"))

    def test_base_class_integration(self):
        """Test integration with base class functionality"""
        kernel = MonotonicWeightKernel(
            weight_type="monotonic",
            description="Test kernel for inheritance",
            active=True,
        )

        assert kernel.weight_type == "monotonic"
        assert kernel.description == "Test kernel for inheritance"
        assert kernel.active is True


# Class 2: Enumeration Tests
class TestEnumerations:
    """Test enumeration classes"""

    def test_threshold_enum_values(self):
        """Test ThresholdEnum has correct values"""
        assert ThresholdEnum.low_cut == "low cut"
        assert ThresholdEnum.high_cut == "high cut"

        # Test all enum values
        expected_values = {"low cut", "high cut"}
        actual_values = {item.value for item in ThresholdEnum}
        assert actual_values == expected_values

    def test_style_enum_values(self):
        """Test StyleEnum has correct values"""
        assert StyleEnum.taper == "taper"
        assert StyleEnum.activation == "activation"

        # Test all enum values
        expected_values = {"taper", "activation"}
        actual_values = {item.value for item in StyleEnum}
        assert actual_values == expected_values

    def test_threshold_enum_membership(self):
        """Test ThresholdEnum membership"""
        members = [item.value for item in ThresholdEnum]
        assert "low cut" in members
        assert "high cut" in members
        assert "invalid" not in members

    def test_style_enum_membership(self):
        """Test StyleEnum membership"""
        members = [item.value for item in StyleEnum]
        assert "taper" in members
        assert "activation" in members
        assert "invalid" not in members


class TestMonotonicWeightKernelFixtures:
    """Test that fixtures work correctly"""

    def test_fixtures_work(self, default_kernel, finite_bounds_kernel, sample_values):
        """Test that all fixtures are properly created"""
        assert isinstance(default_kernel, MonotonicWeightKernel)
        assert isinstance(finite_bounds_kernel, MonotonicWeightKernel)
        assert isinstance(sample_values, np.ndarray)

        # Test fixture values
        assert finite_bounds_kernel.transition_lower_bound == 0.3
        assert finite_bounds_kernel.transition_upper_bound == 0.8
        assert len(sample_values) == 5


class TestMonotonicWeightKernelInstantiation:
    """Test MonotonicWeightKernel instantiation and initialization"""

    def test_default_instantiation(self):
        """Test default MonotonicWeightKernel creation"""
        kernel = MonotonicWeightKernel()

        assert isinstance(kernel, MonotonicWeightKernel)
        assert kernel.threshold == ThresholdEnum.low_cut
        assert kernel.style == StyleEnum.taper
        assert kernel.transition_lower_bound == -1000000000.0
        assert kernel.transition_upper_bound == 1000000000.0

    def test_custom_instantiation(self):
        """Test MonotonicWeightKernel with custom parameters"""
        kernel = MonotonicWeightKernel(
            threshold="high cut",
            style="activation",
            transition_lower_bound=0.2,
            transition_upper_bound=0.9,
        )

        assert kernel.threshold == ThresholdEnum.high_cut
        assert kernel.style == StyleEnum.activation
        assert kernel.transition_lower_bound == 0.2
        assert kernel.transition_upper_bound == 0.9

    def test_string_enum_conversion(self):
        """Test that string values are properly converted to enums"""
        kernel = MonotonicWeightKernel(threshold="low cut", style="taper")

        assert isinstance(kernel.threshold, ThresholdEnum)
        assert isinstance(kernel.style, StyleEnum)
        assert kernel.threshold == ThresholdEnum.low_cut
        assert kernel.style == StyleEnum.taper

    def test_invalid_threshold_value(self):
        """Test validation error for invalid threshold"""
        with pytest.raises(ValueError):
            MonotonicWeightKernel(threshold="invalid_threshold")

    def test_invalid_style_value(self):
        """Test validation error for invalid style"""
        with pytest.raises(ValueError):
            MonotonicWeightKernel(style="invalid_style")

    def test_bound_types(self):
        """Test that bounds accept various numeric types"""
        # Test integer bounds
        kernel1 = MonotonicWeightKernel(
            transition_lower_bound=1, transition_upper_bound=10
        )
        assert kernel1.transition_lower_bound == 1.0
        assert kernel1.transition_upper_bound == 10.0

        # Test float bounds
        kernel2 = MonotonicWeightKernel(
            transition_lower_bound=1.5, transition_upper_bound=10.7
        )
        assert kernel2.transition_lower_bound == 1.5
        assert kernel2.transition_upper_bound == 10.7

        # Test infinite bounds
        kernel3 = MonotonicWeightKernel(
            transition_lower_bound=float("-inf"), transition_upper_bound=float("inf")
        )
        assert np.isinf(kernel3.transition_lower_bound)
        assert np.isinf(kernel3.transition_upper_bound)


class TestMonotonicWeightKernelComputedFields:
    """Test computed fields and properties"""

    def test_has_finite_transition_bounds_finite(self, finite_bounds_kernel):
        """Test _has_finite_transition_bounds with finite bounds"""
        assert finite_bounds_kernel._has_finite_transition_bounds == True

    def test_has_finite_transition_bounds_infinite(self, infinite_bounds_kernel):
        """Test _has_finite_transition_bounds with infinite bounds"""
        assert infinite_bounds_kernel._has_finite_transition_bounds == False

    def test_has_finite_transition_bounds_mixed(self, mixed_bounds_kernel):
        """Test _has_finite_transition_bounds with mixed bounds"""
        assert mixed_bounds_kernel._has_finite_transition_bounds == False

    def test_has_finite_transition_bounds_edge_cases(self):
        """Test _has_finite_transition_bounds with edge cases"""
        # Test very large but finite numbers
        kernel1 = MonotonicWeightKernel(
            transition_lower_bound=-1e100, transition_upper_bound=1e100
        )
        assert kernel1._has_finite_transition_bounds == True

        # Test NaN values
        kernel2 = MonotonicWeightKernel(
            transition_lower_bound=float("nan"), transition_upper_bound=1.0
        )
        assert kernel2._has_finite_transition_bounds == False

    def test_computed_field_is_read_only(self, finite_bounds_kernel):
        """Test that computed field cannot be modified"""
        # Computed fields should be read-only
        with pytest.raises(AttributeError):
            finite_bounds_kernel._has_finite_transition_bounds = False


class TestMonotonicWeightKernelNormalization:
    """Test normalization functionality"""

    def test_normalize_finite_bounds(self, finite_bounds_kernel, sample_values):
        """Test normalization with finite bounds"""
        normalized = finite_bounds_kernel._normalize(sample_values)

        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == len(sample_values)

        # Check normalization formula: (x - lb) / (ub - lb)
        expected = (sample_values - 0.3) / (0.8 - 0.3)
        np.testing.assert_array_almost_equal(normalized, expected)

    def test_normalize_range_validation(self, finite_bounds_kernel):
        """Test normalization produces values in expected range"""
        # Test values that should normalize to 0 and 1
        test_values = np.array([0.3, 0.55, 0.8])  # lower_bound, middle, upper_bound
        normalized = finite_bounds_kernel._normalize(test_values)

        assert normalized[0] == 0.0  # lower bound -> 0
        assert normalized[2] == 1.0  # upper bound -> 1
        assert 0 < normalized[1] < 1  # middle value between 0 and 1

    def test_normalize_infinite_bounds_error(
        self, infinite_bounds_kernel, sample_values
    ):
        """Test that normalization with infinite bounds raises error"""
        with pytest.raises(ValueError, match="only supports finite transition bounds"):
            infinite_bounds_kernel._normalize(sample_values)

    def test_normalize_mixed_bounds_error(self, mixed_bounds_kernel, sample_values):
        """Test that normalization with mixed bounds raises error"""
        with pytest.raises(ValueError, match="only supports finite transition bounds"):
            mixed_bounds_kernel._normalize(sample_values)

    def test_normalize_different_input_types(self, finite_bounds_kernel):
        """Test normalization with different input types"""
        # Test list input
        list_input = [0.3, 0.5, 0.8]
        normalized_list = finite_bounds_kernel._normalize(list_input)
        assert isinstance(normalized_list, np.ndarray)

        # Test scalar input
        scalar_input = 0.5
        normalized_scalar = finite_bounds_kernel._normalize(scalar_input)
        # Scalar input may return a scalar, which is acceptable
        assert np.isscalar(normalized_scalar) or isinstance(
            normalized_scalar, np.ndarray
        )

        # Test tuple input
        tuple_input = (0.3, 0.5, 0.8)
        normalized_tuple = finite_bounds_kernel._normalize(tuple_input)
        assert isinstance(normalized_tuple, np.ndarray)

    def test_normalize_empty_array(self, finite_bounds_kernel):
        """Test normalization with empty array"""
        empty_array = np.array([])
        normalized = finite_bounds_kernel._normalize(empty_array)

        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == 0

    def test_normalize_single_value(self, finite_bounds_kernel):
        """Test normalization with single value"""
        single_value = np.array([0.5])
        normalized = finite_bounds_kernel._normalize(single_value)

        assert isinstance(normalized, np.ndarray)
        assert len(normalized) == 1
        expected = (0.5 - 0.3) / (0.8 - 0.3)
        assert normalized[0] == expected


class TestMonotonicWeightKernelValidation:
    """Test validation functionality"""

    def test_threshold_enum_validation(self):
        """Test threshold field accepts valid enum values"""
        for threshold in ThresholdEnum:
            kernel = MonotonicWeightKernel(threshold=threshold)
            assert kernel.threshold == threshold

    def test_style_enum_validation(self):
        """Test style field accepts valid enum values"""
        for style in StyleEnum:
            kernel = MonotonicWeightKernel(style=style)
            assert kernel.style == style

    def test_bounds_ordering_allowed(self):
        """Test that lower bound can be greater than upper bound (unusual but valid)"""
        # This might be valid for certain use cases
        kernel = MonotonicWeightKernel(
            transition_lower_bound=0.8, transition_upper_bound=0.3
        )
        assert kernel.transition_lower_bound == 0.8
        assert kernel.transition_upper_bound == 0.3

    def test_equal_bounds(self):
        """Test equal lower and upper bounds"""
        kernel = MonotonicWeightKernel(
            transition_lower_bound=0.5, transition_upper_bound=0.5
        )
        assert kernel.transition_lower_bound == 0.5
        assert kernel.transition_upper_bound == 0.5

        # This should still be considered finite bounds
        assert kernel._has_finite_transition_bounds == True


class TestMonotonicWeightKernelSerialization:
    """Test serialization functionality"""

    def test_to_dict(self, finite_bounds_kernel):
        """Test conversion to dictionary"""
        kernel_dict = finite_bounds_kernel.to_dict()

        assert isinstance(kernel_dict, dict)
        # The to_dict wraps content in a key
        assert "monotonic_weight_kernel" in kernel_dict
        content = kernel_dict["monotonic_weight_kernel"]
        assert content["threshold"] == "low cut"
        assert content["style"] == "taper"
        assert content["transition_lower_bound"] == 0.3
        assert content["transition_upper_bound"] == 0.8

    def test_from_dict(self):
        """Test creation from dictionary"""
        kernel_dict = {
            "threshold": "high cut",
            "style": "activation",
            "transition_lower_bound": 0.2,
            "transition_upper_bound": 0.9,
        }

        kernel = MonotonicWeightKernel()
        kernel.from_dict(kernel_dict)

        assert kernel.threshold == ThresholdEnum.high_cut
        assert kernel.style == StyleEnum.activation
        assert kernel.transition_lower_bound == 0.2
        assert kernel.transition_upper_bound == 0.9

    def test_serialization_roundtrip(self, finite_bounds_kernel):
        """Test serialization roundtrip preserves data"""
        # Convert to dict and back
        kernel_dict = finite_bounds_kernel.to_dict()
        new_kernel = MonotonicWeightKernel()
        new_kernel.from_dict(kernel_dict)

        assert new_kernel.threshold == finite_bounds_kernel.threshold
        assert new_kernel.style == finite_bounds_kernel.style
        assert (
            new_kernel.transition_lower_bound
            == finite_bounds_kernel.transition_lower_bound
        )
        assert (
            new_kernel.transition_upper_bound
            == finite_bounds_kernel.transition_upper_bound
        )

    def test_model_copy(self, finite_bounds_kernel):
        """Test model copying"""
        copied = finite_bounds_kernel.model_copy(deep=True)

        assert isinstance(copied, MonotonicWeightKernel)
        assert copied.threshold == finite_bounds_kernel.threshold
        assert copied.style == finite_bounds_kernel.style
        assert (
            copied.transition_lower_bound == finite_bounds_kernel.transition_lower_bound
        )
        assert (
            copied.transition_upper_bound == finite_bounds_kernel.transition_upper_bound
        )

        # Verify it's a deep copy
        copied.transition_lower_bound = 999.0
        assert finite_bounds_kernel.transition_lower_bound != 999.0


class TestMonotonicWeightKernelPerformance:
    """Test performance characteristics"""

    def test_instantiation_performance(self):
        """Test kernel instantiation performance"""
        import time

        start_time = time.time()

        for _ in range(1000):
            kernel = MonotonicWeightKernel()

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete quickly
        assert execution_time < 1.0

    def test_normalization_performance(self, finite_bounds_kernel, large_sample_values):
        """Test normalization performance with large arrays"""
        import time

        start_time = time.time()

        for _ in range(100):
            _ = finite_bounds_kernel._normalize(large_sample_values)

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete in reasonable time
        assert execution_time < 5.0

    def test_computed_field_performance(self, finite_bounds_kernel):
        """Test computed field access performance"""
        import time

        start_time = time.time()

        for _ in range(10000):
            _ = finite_bounds_kernel._has_finite_transition_bounds

        end_time = time.time()
        execution_time = end_time - start_time

        # Computed field should be fast to access
        assert execution_time < 1.0


class TestMonotonicWeightKernelEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_very_large_bounds(self):
        """Test with very large but finite bounds"""
        kernel = MonotonicWeightKernel(
            transition_lower_bound=-1e308, transition_upper_bound=1e308
        )

        assert kernel._has_finite_transition_bounds == True

        # Test normalization with large bounds
        test_values = np.array([0.0])
        normalized = kernel._normalize(test_values)
        assert np.isfinite(normalized[0])

    def test_zero_bounds(self):
        """Test with zero bounds"""
        kernel = MonotonicWeightKernel(
            transition_lower_bound=0.0, transition_upper_bound=0.0
        )

        assert kernel._has_finite_transition_bounds == True

        # Normalization with zero-width bounds should handle division by zero
        test_values = np.array([0.0])
        with pytest.warns(RuntimeWarning, match="invalid value encountered in divide"):
            normalized = kernel._normalize(test_values)
            # Should return NaN due to 0/0 division
            assert np.isnan(normalized[0])

    def test_negative_bounds(self):
        """Test with negative bounds"""
        kernel = MonotonicWeightKernel(
            transition_lower_bound=-1.0, transition_upper_bound=-0.5
        )

        assert kernel._has_finite_transition_bounds == True

        test_values = np.array([-0.8, -0.7, -0.6])
        normalized = kernel._normalize(test_values)
        assert all(np.isfinite(normalized))

    def test_mixed_sign_bounds(self):
        """Test with bounds spanning zero"""
        kernel = MonotonicWeightKernel(
            transition_lower_bound=-0.5, transition_upper_bound=0.5
        )

        assert kernel._has_finite_transition_bounds == True

        test_values = np.array([-0.5, 0.0, 0.5])
        normalized = kernel._normalize(test_values)

        assert normalized[0] == 0.0  # lower bound
        assert normalized[1] == 0.5  # middle
        assert normalized[2] == 1.0  # upper bound


class TestMonotonicWeightKernelParametrized:
    """Parametrized tests for various scenarios"""

    @pytest.mark.parametrize(
        "threshold,expected",
        [
            ("low cut", ThresholdEnum.low_cut),
            ("high cut", ThresholdEnum.high_cut),
        ],
    )
    def test_threshold_values(self, threshold, expected):
        """Test various threshold values"""
        kernel = MonotonicWeightKernel(threshold=threshold)
        assert kernel.threshold == expected

    @pytest.mark.parametrize(
        "style,expected",
        [
            ("taper", StyleEnum.taper),
            ("activation", StyleEnum.activation),
        ],
    )
    def test_style_values(self, style, expected):
        """Test various style values"""
        kernel = MonotonicWeightKernel(style=style)
        assert kernel.style == expected

    @pytest.mark.parametrize(
        "lower,upper,expected_finite",
        [
            (0.0, 1.0, True),
            (-np.inf, 1.0, False),
            (0.0, np.inf, False),
            (-np.inf, np.inf, False),
            (np.nan, 1.0, False),
            (0.0, np.nan, False),
            (-1e10, 1e10, True),
        ],
    )
    def test_finite_bounds_detection(self, lower, upper, expected_finite):
        """Test finite bounds detection with various values"""
        kernel = MonotonicWeightKernel(
            transition_lower_bound=lower, transition_upper_bound=upper
        )
        assert kernel._has_finite_transition_bounds == expected_finite

    @pytest.mark.parametrize(
        "bound_pairs",
        [
            (0.0, 1.0),
            (-1.0, 1.0),
            (0.5, 0.6),
            (-10.0, -5.0),
            (100.0, 200.0),
        ],
    )
    def test_normalization_consistency(self, bound_pairs):
        """Test normalization consistency across different bound pairs"""
        lower, upper = bound_pairs
        kernel = MonotonicWeightKernel(
            transition_lower_bound=lower, transition_upper_bound=upper
        )

        # Test that bounds normalize to 0 and 1
        test_values = np.array([lower, upper])
        normalized = kernel._normalize(test_values)

        np.testing.assert_array_almost_equal(normalized, [0.0, 1.0])

    @pytest.mark.parametrize("array_size", [1, 10, 100, 1000])
    def test_normalization_array_sizes(self, finite_bounds_kernel, array_size):
        """Test normalization with different array sizes"""
        test_values = np.linspace(0.2, 0.9, array_size)
        normalized = finite_bounds_kernel._normalize(test_values)

        assert len(normalized) == array_size
        assert all(np.isfinite(normalized))
