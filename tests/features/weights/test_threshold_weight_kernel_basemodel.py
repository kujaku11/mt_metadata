"""
Test threshold_weight_kernel_basemodel.py - Comprehensive test suite for ThresholdWeightKernel basemodel

Tests the ThresholdWeightKernel class from the basemodel module using fixtures and subtests
for optimal efficiency.

This module contains the ThresholdWeightKernel class which is a special case of
TaperMonotonicWeightKernel where the transition region is a single value, resulting in
a hard threshold (step function).
"""

import numpy as np
import pytest

from mt_metadata.features.weights.base_basemodel import Base
from mt_metadata.features.weights.monotonic_weight_kernel_basemodel import (
    MonotonicWeightKernel,
)
from mt_metadata.features.weights.taper_monotonic_weight_kernel_basemodel import (
    TaperMonotonicWeightKernel,
)
from mt_metadata.features.weights.threshold_weight_kernel_basemodel import (
    ThresholdWeightKernel,
)


# Fixtures at module level for optimal efficiency
@pytest.fixture
def default_threshold_kernel():
    """Basic ThresholdWeightKernel with default values"""
    return ThresholdWeightKernel()


@pytest.fixture
def low_cut_threshold_kernel():
    """ThresholdWeightKernel configured for low cut threshold"""
    return ThresholdWeightKernel(
        threshold_type="low cut",
        threshold="low cut",
        half_window_style="rectangle",
        transition_lower_bound=0.5,
        transition_upper_bound=0.5,
    )


@pytest.fixture
def high_cut_threshold_kernel():
    """ThresholdWeightKernel configured for high cut threshold"""
    return ThresholdWeightKernel(
        threshold_type="high cut",
        threshold="high cut",
        half_window_style="rectangle",
        transition_lower_bound=0.7,
        transition_upper_bound=0.7,
    )


@pytest.fixture
def sample_threshold_values():
    """Sample numpy array for testing threshold operations"""
    return np.array([0.1, 0.3, 0.5, 0.7, 0.9])


@pytest.fixture
def large_sample_values():
    """Larger sample array for performance testing"""
    return np.linspace(0, 1, 1000)


@pytest.fixture
def edge_case_values():
    """Edge case values including infinity and NaN"""
    return np.array(
        [
            float("-inf"),
            -1e10,
            -1.0,
            0.0,
            0.5,
            1.0,
            1e10,
            float("inf"),
            float("nan"),
        ]
    )


# Class 1: Inheritance Tests
class TestThresholdWeightKernelInheritance:
    """Test inheritance relationships and base class integration"""

    def test_inheritance_from_taper_monotonic_weight_kernel(self):
        """Test that ThresholdWeightKernel inherits from TaperMonotonicWeightKernel"""
        kernel = ThresholdWeightKernel()
        assert isinstance(kernel, TaperMonotonicWeightKernel)
        assert isinstance(kernel, MonotonicWeightKernel)
        assert isinstance(kernel, Base)
        assert isinstance(kernel, ThresholdWeightKernel)

    def test_method_resolution_order(self):
        """Test method resolution order includes all parent classes"""
        mro = ThresholdWeightKernel.__mro__
        base_classes = [cls.__name__ for cls in mro]
        assert "ThresholdWeightKernel" in base_classes
        assert "TaperMonotonicWeightKernel" in base_classes
        assert "MonotonicWeightKernel" in base_classes
        assert "Base" in base_classes

    def test_inherited_fields_from_parents(self):
        """Test that fields from parent classes are accessible"""
        kernel = ThresholdWeightKernel()

        # From Base
        assert hasattr(kernel, "weight_type")
        assert hasattr(kernel, "description")
        assert hasattr(kernel, "active")

        # From MonotonicWeightKernel
        assert hasattr(kernel, "threshold")
        assert hasattr(kernel, "style")
        assert hasattr(kernel, "transition_lower_bound")
        assert hasattr(kernel, "transition_upper_bound")

        # From TaperMonotonicWeightKernel
        assert hasattr(kernel, "half_window_style")

        # From ThresholdWeightKernel
        assert hasattr(kernel, "threshold_type")

    def test_parent_methods_available(self):
        """Test that parent class methods are available"""
        kernel = ThresholdWeightKernel()

        # Check for parent methods
        assert hasattr(kernel, "evaluate")
        assert hasattr(kernel, "_normalize")
        assert hasattr(kernel, "_has_finite_transition_bounds")

        # Ensure methods are callable
        assert callable(getattr(kernel, "evaluate"))
        assert callable(getattr(kernel, "_normalize"))


# Class 2: Field Tests
class TestThresholdWeightKernelFields:
    """Test field definitions and validation"""

    def test_threshold_type_field_default(self):
        """Test threshold_type field has correct default value"""
        kernel = ThresholdWeightKernel()
        assert kernel.threshold_type == "low cut"

    def test_threshold_type_field_assignment(self):
        """Test threshold_type field can be assigned valid values"""
        valid_values = ["low cut", "high cut"]

        for value in valid_values:
            kernel = ThresholdWeightKernel(threshold_type=value)
            assert kernel.threshold_type == value

    def test_threshold_type_field_validation(self):
        """Test threshold_type field validation for invalid values"""
        # Note: Since this is a string field, it accepts any string
        # Validation might happen at a higher level
        kernel = ThresholdWeightKernel(threshold_type="invalid_type")
        assert kernel.threshold_type == "invalid_type"

    def test_field_descriptions_exist(self):
        """Test that field descriptions are properly defined"""
        # Get the field info from the model
        field_info = ThresholdWeightKernel.model_fields

        assert "threshold_type" in field_info
        assert field_info["threshold_type"].description is not None
        assert (
            "threshold should be downweighted"
            in field_info["threshold_type"].description.lower()
        )


# Class 3: Instantiation Tests
class TestThresholdWeightKernelInstantiation:
    """Test various instantiation scenarios"""

    def test_default_instantiation(self, default_threshold_kernel):
        """Test default instantiation with fixtures"""
        assert isinstance(default_threshold_kernel, ThresholdWeightKernel)
        assert default_threshold_kernel.threshold_type == "low cut"

    def test_custom_instantiation(self):
        """Test instantiation with custom parameters"""
        kernel = ThresholdWeightKernel(
            threshold_type="high cut",
            threshold="high cut",
            half_window_style="rectangle",
            transition_lower_bound=0.8,
            transition_upper_bound=0.8,
        )

        assert kernel.threshold_type == "high cut"
        assert kernel.threshold == "high cut"
        assert kernel.half_window_style == "rectangle"
        assert kernel.transition_lower_bound == 0.8
        assert kernel.transition_upper_bound == 0.8

    def test_inheritance_field_defaults(self):
        """Test that inherited field defaults work correctly"""
        kernel = ThresholdWeightKernel()

        # Test Base defaults
        assert kernel.weight_type == "monotonic"
        assert kernel.description is None
        assert kernel.active is None

        # Test MonotonicWeightKernel defaults
        assert kernel.threshold == "low cut"
        assert kernel.style == "taper"

        # Test TaperMonotonicWeightKernel defaults
        assert kernel.half_window_style == "rectangle"

    def test_equal_bounds_instantiation(self):
        """Test instantiation with equal transition bounds (threshold behavior)"""
        threshold_value = 0.6
        kernel = ThresholdWeightKernel(
            transition_lower_bound=threshold_value,
            transition_upper_bound=threshold_value,
        )

        assert kernel.transition_lower_bound == threshold_value
        assert kernel.transition_upper_bound == threshold_value
        assert kernel.transition_lower_bound == kernel.transition_upper_bound


# Class 4: Method Tests
class TestThresholdWeightKernelMethods:
    """Test class methods and their behavior"""

    def test_normalize_raises_not_implemented(self):
        """Test that _normalize method raises NotImplementedError"""
        kernel = ThresholdWeightKernel()
        values = np.array([0.1, 0.5, 0.9])

        with pytest.raises(NotImplementedError, match="Normalization not implemented"):
            kernel._normalize(values)

    def test_normalize_with_different_input_types(self):
        """Test _normalize with different input types all raise NotImplementedError"""
        kernel = ThresholdWeightKernel()

        test_inputs = [
            np.array([0.1, 0.5, 0.9]),
            [0.1, 0.5, 0.9],
            (0.1, 0.5, 0.9),
            0.5,
            np.array([]),
        ]

        for values in test_inputs:
            with pytest.raises(NotImplementedError):
                kernel._normalize(values)

    def test_evaluate_method_inherited_raises_error(self):
        """Test that evaluate method raises NotImplementedError due to _normalize"""
        kernel = ThresholdWeightKernel(
            threshold="low cut",
            half_window_style="rectangle",
            transition_lower_bound=0.5,
            transition_upper_bound=0.5,
        )

        # This should raise NotImplementedError because _normalize is not implemented
        values = np.array([0.1, 0.5, 0.9])
        with pytest.raises(NotImplementedError, match="Normalization not implemented"):
            kernel.evaluate(values)

    def test_has_finite_transition_bounds_inherited(self):
        """Test that _has_finite_transition_bounds computed field works"""
        # Test with finite bounds
        kernel1 = ThresholdWeightKernel(
            transition_lower_bound=0.3,
            transition_upper_bound=0.7,
        )
        assert bool(kernel1._has_finite_transition_bounds) is True

        # Test with infinite bounds
        kernel2 = ThresholdWeightKernel(
            transition_lower_bound=float("-inf"),
            transition_upper_bound=float("inf"),
        )
        assert bool(kernel2._has_finite_transition_bounds) is False


# Class 5: Threshold Behavior Tests
class TestThresholdWeightKernelBehavior:
    """Test threshold-specific behavior - Note: evaluate() not fully implemented in basemodel"""

    def test_threshold_type_field_behavior(self):
        """Test threshold_type field affects kernel configuration"""
        # Test low cut
        low_cut_kernel = ThresholdWeightKernel(threshold_type="low cut")
        assert low_cut_kernel.threshold_type == "low cut"

        # Test high cut
        high_cut_kernel = ThresholdWeightKernel(threshold_type="high cut")
        assert high_cut_kernel.threshold_type == "high cut"

    def test_threshold_configuration_consistency(self):
        """Test that threshold_type and threshold fields can be set consistently"""
        kernel = ThresholdWeightKernel(
            threshold_type="high cut",
            threshold="high cut",
        )

        assert kernel.threshold_type == "high cut"
        assert kernel.threshold == "high cut"

    def test_equal_bounds_configuration(self):
        """Test configuration with equal transition bounds (threshold behavior)"""
        threshold_val = 0.6
        kernel = ThresholdWeightKernel(
            threshold_type="low cut",
            transition_lower_bound=threshold_val,
            transition_upper_bound=threshold_val,
        )

        assert kernel.transition_lower_bound == threshold_val
        assert kernel.transition_upper_bound == threshold_val
        assert kernel.transition_lower_bound == kernel.transition_upper_bound
        assert kernel.threshold_type == "low cut"


# Class 6: Edge Cases Tests
class TestThresholdWeightKernelEdgeCases:
    """Test edge cases and boundary conditions - focusing on field validation"""

    def test_empty_threshold_type_string(self):
        """Test behavior with empty threshold_type string"""
        kernel = ThresholdWeightKernel(threshold_type="")
        assert kernel.threshold_type == ""

    def test_extreme_transition_bounds(self):
        """Test with extreme transition bound values"""
        extreme_values = [
            -1e10,
            1e10,
        ]

        for thresh in extreme_values:
            kernel = ThresholdWeightKernel(
                transition_lower_bound=thresh,
                transition_upper_bound=thresh,
            )

            assert kernel.transition_lower_bound == thresh
            assert kernel.transition_upper_bound == thresh

    def test_zero_transition_bounds(self):
        """Test with zero transition bounds"""
        kernel = ThresholdWeightKernel(
            transition_lower_bound=0.0,
            transition_upper_bound=0.0,
        )

        assert kernel.transition_lower_bound == 0.0
        assert kernel.transition_upper_bound == 0.0

    def test_negative_transition_bounds(self):
        """Test with negative transition bounds"""
        kernel = ThresholdWeightKernel(
            transition_lower_bound=-1.0,
            transition_upper_bound=-1.0,
        )

        assert kernel.transition_lower_bound == -1.0
        assert kernel.transition_upper_bound == -1.0


# Class 7: Serialization Tests
class TestThresholdWeightKernelSerialization:
    """Test serialization and deserialization"""

    def test_model_dump(self):
        """Test model serialization to dictionary"""
        kernel = ThresholdWeightKernel(
            threshold_type="high cut",
            threshold="high cut",
            transition_lower_bound=0.8,
            transition_upper_bound=0.8,
        )

        kernel_dict = kernel.model_dump()

        assert isinstance(kernel_dict, dict)
        assert kernel_dict["threshold_type"] == "high cut"
        assert kernel_dict["threshold"] == "high cut"
        assert kernel_dict["transition_lower_bound"] == 0.8
        assert kernel_dict["transition_upper_bound"] == 0.8

    def test_model_load_from_dict(self):
        """Test model deserialization from dictionary"""
        data = {
            "threshold_type": "low cut",
            "threshold": "low cut",
            "half_window_style": "rectangle",
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.3,
        }

        kernel = ThresholdWeightKernel(**data)

        assert kernel.threshold_type == "low cut"
        assert kernel.threshold == "low cut"
        assert kernel.transition_lower_bound == 0.3
        assert kernel.transition_upper_bound == 0.3

    def test_serialization_roundtrip(self):
        """Test that serialization and deserialization preserve data"""
        original = ThresholdWeightKernel(
            threshold_type="high cut",
            weight_type="custom",
            description="Test threshold kernel",
            active=True,
        )

        # Serialize to dict
        data = original.model_dump()

        # Deserialize back
        restored = ThresholdWeightKernel(**data)

        assert restored.threshold_type == original.threshold_type
        assert restored.weight_type == original.weight_type
        assert restored.description == original.description
        assert restored.active == original.active

    def test_model_copy(self):
        """Test model copying functionality"""
        original = ThresholdWeightKernel(
            threshold_type="high cut",
            transition_lower_bound=0.6,
            transition_upper_bound=0.6,
        )

        copied = original.model_copy()

        assert isinstance(copied, ThresholdWeightKernel)
        assert copied.threshold_type == original.threshold_type
        assert copied.transition_lower_bound == original.transition_lower_bound
        assert copied.transition_upper_bound == original.transition_upper_bound

        # Ensure they are separate objects
        assert copied is not original


# Class 8: Performance Tests
class TestThresholdWeightKernelPerformance:
    """Test performance characteristics - focusing on instantiation and field access"""

    def test_instantiation_performance(self):
        """Test that instantiation is reasonably fast"""
        import time

        start_time = time.time()

        # Create multiple instances
        kernels = [ThresholdWeightKernel() for _ in range(100)]

        end_time = time.time()
        duration = end_time - start_time

        # Should complete in reasonable time (less than 1 second)
        assert duration < 1.0
        assert len(kernels) == 100
        assert all(isinstance(k, ThresholdWeightKernel) for k in kernels)

    def test_field_access_performance(self):
        """Test that field access is fast"""
        kernel = ThresholdWeightKernel()

        import time

        start_time = time.time()

        # Access fields many times
        for _ in range(1000):
            _ = kernel.threshold_type
            _ = kernel.threshold
            _ = kernel.transition_lower_bound
            _ = kernel.transition_upper_bound

        end_time = time.time()
        duration = end_time - start_time

        # Should be very fast
        assert duration < 0.1


# Class 9: Parametrized Tests
class TestThresholdWeightKernelParametrized:
    """Parametrized tests for comprehensive coverage - focusing on field validation"""

    @pytest.mark.parametrize("threshold_type", ["low cut", "high cut"])
    def test_threshold_type_values(self, threshold_type):
        """Test different threshold_type values"""
        kernel = ThresholdWeightKernel(threshold_type=threshold_type)
        assert kernel.threshold_type == threshold_type

    @pytest.mark.parametrize("threshold_value", [0.0, 0.25, 0.5, 0.75, 1.0])
    def test_different_threshold_bound_values(self, threshold_value):
        """Test different threshold bound values"""
        kernel = ThresholdWeightKernel(
            threshold="low cut",
            transition_lower_bound=threshold_value,
            transition_upper_bound=threshold_value,
        )

        assert kernel.transition_lower_bound == threshold_value
        assert kernel.transition_upper_bound == threshold_value

    @pytest.mark.parametrize(
        "threshold_direction",
        ["low cut", "high cut"],
    )
    def test_threshold_consistency(self, threshold_direction):
        """Test that threshold_type and threshold can be set consistently"""
        threshold_val = 0.5
        kernel = ThresholdWeightKernel(
            threshold_type=threshold_direction,
            threshold=threshold_direction,
            transition_lower_bound=threshold_val,
            transition_upper_bound=threshold_val,
        )

        assert kernel.threshold_type == threshold_direction
        assert kernel.threshold == threshold_direction
        assert kernel.transition_lower_bound == threshold_val
        assert kernel.transition_upper_bound == threshold_val
