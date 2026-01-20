"""
Test module for weight_kernel.py
Note: weight_kernel.py appears to be identical to feature_weighting_window.py
"""

import numpy as np
import pytest
from pydantic import ValidationError

from mt_metadata.features.weight_kernel import (
    FeatureWeightingWindow,
    HalfWindowStyleEnum,
    ThresholdEnum,
)

# ============================================================================
# TEST THRESHOLD ENUM
# ============================================================================


class TestWeightKernelThresholdEnum:
    """Test ThresholdEnum enumeration."""

    def test_threshold_enum_values(self):
        """Test that all threshold enum values are accessible."""
        assert ThresholdEnum.low_cut == "low cut"
        assert ThresholdEnum.high_cut == "high cut"

    def test_threshold_enum_iteration(self):
        """Test iterating over enum values."""
        values = [e.value for e in ThresholdEnum]
        assert "low cut" in values
        assert "high cut" in values


# ============================================================================
# TEST HALF WINDOW STYLE ENUM
# ============================================================================


class TestWeightKernelHalfWindowStyleEnum:
    """Test HalfWindowStyleEnum enumeration."""

    def test_half_window_style_enum_values(self):
        """Test that all half window style enum values are accessible."""
        assert HalfWindowStyleEnum.hamming == "hamming"
        assert HalfWindowStyleEnum.hann == "hann"
        assert HalfWindowStyleEnum.rectangle == "rectangle"

    def test_half_window_style_enum_iteration(self):
        """Test iterating over enum values."""
        values = [e.value for e in HalfWindowStyleEnum]
        assert len(values) == 3
        assert all(v in ["hamming", "hann", "rectangle"] for v in values)


# ============================================================================
# TEST WEIGHT KERNEL FEATURE WEIGHTING WINDOW
# ============================================================================


class TestWeightKernelDefaults:
    """Test weight kernel default initialization."""

    def test_default_values(self):
        """Test default values match specifications."""
        window = FeatureWeightingWindow()
        assert window.threshold == "low cut"
        assert window.half_window_style == "hann"
        assert window.transition_lower_bound == -np.inf
        assert window.transition_upper_bound == np.inf


class TestWeightKernelThresholdParameter:
    """Test weight kernel threshold parameter."""

    def test_low_cut_threshold(self):
        """Test setting low cut threshold."""
        window = FeatureWeightingWindow(threshold="low cut")
        assert window.threshold == "low cut"

    def test_high_cut_threshold(self):
        """Test setting high cut threshold."""
        window = FeatureWeightingWindow(threshold="high cut")
        assert window.threshold == "high cut"

    def test_invalid_threshold(self):
        """Test that invalid threshold raises error."""
        with pytest.raises(ValidationError):
            FeatureWeightingWindow(threshold="medium cut")


class TestWeightKernelWindowStyle:
    """Test weight kernel half window style parameter."""

    @pytest.mark.parametrize(
        "style",
        ["hamming", "hann", "rectangle"],
    )
    def test_all_window_styles(self, style):
        """Test all valid window styles."""
        window = FeatureWeightingWindow(half_window_style=style)
        assert window.half_window_style == style

    def test_invalid_window_style(self):
        """Test that invalid window style raises error."""
        with pytest.raises(ValidationError):
            FeatureWeightingWindow(half_window_style="kaiser")


class TestWeightKernelTransitionBounds:
    """Test weight kernel transition bounds."""

    def test_finite_bounds(self):
        """Test setting finite transition bounds."""
        window = FeatureWeightingWindow(
            transition_lower_bound=0.25, transition_upper_bound=0.75
        )
        assert window.transition_lower_bound == 0.25
        assert window.transition_upper_bound == 0.75

    def test_infinite_bounds(self):
        """Test setting infinite bounds."""
        window = FeatureWeightingWindow(
            transition_lower_bound=-np.inf, transition_upper_bound=np.inf
        )
        assert np.isinf(window.transition_lower_bound)
        assert np.isinf(window.transition_upper_bound)

    def test_mixed_bounds(self):
        """Test mixing finite and infinite bounds."""
        window = FeatureWeightingWindow(
            transition_lower_bound=0.0, transition_upper_bound=np.inf
        )
        assert window.transition_lower_bound == 0.0
        assert np.isinf(window.transition_upper_bound)


class TestWeightKernelConfiguration:
    """Test complete weight kernel configuration."""

    def test_full_configuration(self):
        """Test setting all parameters together."""
        window = FeatureWeightingWindow(
            threshold="high cut",
            half_window_style="rectangle",
            transition_lower_bound=0.1,
            transition_upper_bound=0.95,
        )
        assert window.threshold == "high cut"
        assert window.half_window_style == "rectangle"
        assert window.transition_lower_bound == 0.1
        assert window.transition_upper_bound == 0.95

    def test_serialization_deserialization(self):
        """Test round-trip serialization."""
        original = FeatureWeightingWindow(
            threshold="low cut",
            half_window_style="hamming",
            transition_lower_bound=0.2,
            transition_upper_bound=0.8,
        )
        data = original.model_dump()
        restored = FeatureWeightingWindow(**data)

        assert restored.threshold == original.threshold
        assert restored.half_window_style == original.half_window_style
        assert restored.transition_lower_bound == original.transition_lower_bound
        assert restored.transition_upper_bound == original.transition_upper_bound
