"""
Test module for feature_weighting_window.py
"""

import numpy as np
import pytest
from pydantic import ValidationError

from mt_metadata.features.feature_weighting_window import (
    FeatureWeightingWindow,
    HalfWindowStyleEnum,
    ThresholdEnum,
)


# ============================================================================
# TEST THRESHOLD ENUM
# ============================================================================


class TestThresholdEnum:
    """Test ThresholdEnum enumeration."""

    def test_threshold_enum_values(self):
        """Test that all threshold enum values are accessible."""
        assert ThresholdEnum.low_cut == "low cut"
        assert ThresholdEnum.high_cut == "high cut"

    def test_threshold_enum_all_values(self):
        """Test that enum contains all expected values."""
        values = [e.value for e in ThresholdEnum]
        assert "low cut" in values
        assert "high cut" in values
        assert len(values) == 2


# ============================================================================
# TEST HALF WINDOW STYLE ENUM
# ============================================================================


class TestHalfWindowStyleEnum:
    """Test HalfWindowStyleEnum enumeration."""

    def test_half_window_style_enum_values(self):
        """Test that all half window style enum values are accessible."""
        assert HalfWindowStyleEnum.hamming == "hamming"
        assert HalfWindowStyleEnum.hann == "hann"
        assert HalfWindowStyleEnum.rectangle == "rectangle"

    def test_half_window_style_enum_all_values(self):
        """Test that enum contains all expected values."""
        values = [e.value for e in HalfWindowStyleEnum]
        assert "hamming" in values
        assert "hann" in values
        assert "rectangle" in values
        assert len(values) == 3


# ============================================================================
# TEST FEATURE WEIGHTING WINDOW
# ============================================================================


class TestFeatureWeightingWindowDefaults:
    """Test FeatureWeightingWindow default values."""

    def test_default_initialization(self):
        """Test that FeatureWeightingWindow initializes with default values."""
        window = FeatureWeightingWindow()
        assert window.threshold == "low cut"
        assert window.half_window_style == "hann"
        assert window.transition_lower_bound == -np.inf
        assert window.transition_upper_bound == np.inf

    def test_default_types(self):
        """Test that default values have correct types."""
        window = FeatureWeightingWindow()
        assert isinstance(window.threshold, str)
        assert isinstance(window.half_window_style, str)
        assert isinstance(window.transition_lower_bound, float)
        assert isinstance(window.transition_upper_bound, float)


class TestFeatureWeightingWindowThreshold:
    """Test FeatureWeightingWindow threshold parameter."""

    @pytest.mark.parametrize(
        "threshold",
        ["low cut", "high cut"],
    )
    def test_valid_threshold_values(self, threshold):
        """Test setting valid threshold values."""
        window = FeatureWeightingWindow(threshold=threshold)
        assert window.threshold == threshold

    def test_threshold_enum_direct(self):
        """Test setting threshold with enum directly."""
        window = FeatureWeightingWindow(threshold=ThresholdEnum.low_cut)
        assert window.threshold == "low cut"

    def test_invalid_threshold_raises_error(self):
        """Test that invalid threshold value raises ValidationError."""
        with pytest.raises(ValidationError):
            FeatureWeightingWindow(threshold="invalid_threshold")


class TestFeatureWeightingWindowHalfWindowStyle:
    """Test FeatureWeightingWindow half_window_style parameter."""

    @pytest.mark.parametrize(
        "style",
        ["hamming", "hann", "rectangle"],
    )
    def test_valid_half_window_style_values(self, style):
        """Test setting valid half_window_style values."""
        window = FeatureWeightingWindow(half_window_style=style)
        assert window.half_window_style == style

    def test_half_window_style_enum_direct(self):
        """Test setting half_window_style with enum directly."""
        window = FeatureWeightingWindow(half_window_style=HalfWindowStyleEnum.hamming)
        assert window.half_window_style == "hamming"

    def test_invalid_half_window_style_raises_error(self):
        """Test that invalid half_window_style value raises ValidationError."""
        with pytest.raises(ValidationError):
            FeatureWeightingWindow(half_window_style="invalid_style")


class TestFeatureWeightingWindowBounds:
    """Test FeatureWeightingWindow transition bounds."""

    def test_set_transition_lower_bound(self):
        """Test setting transition_lower_bound."""
        window = FeatureWeightingWindow(transition_lower_bound=0.3)
        assert window.transition_lower_bound == 0.3

    def test_set_transition_upper_bound(self):
        """Test setting transition_upper_bound."""
        window = FeatureWeightingWindow(transition_upper_bound=0.999)
        assert window.transition_upper_bound == 0.999

    def test_set_both_bounds(self):
        """Test setting both transition bounds."""
        window = FeatureWeightingWindow(
            transition_lower_bound=0.2, transition_upper_bound=0.8
        )
        assert window.transition_lower_bound == 0.2
        assert window.transition_upper_bound == 0.8

    @pytest.mark.parametrize(
        "lower, upper",
        [
            (0.0, 1.0),
            (-1.0, 1.0),
            (0.1, 0.9),
            (-np.inf, np.inf),
            (0.0, np.inf),
            (-np.inf, 0.0),
        ],
    )
    def test_various_bound_combinations(self, lower, upper):
        """Test various combinations of transition bounds."""
        window = FeatureWeightingWindow(
            transition_lower_bound=lower, transition_upper_bound=upper
        )
        assert window.transition_lower_bound == lower
        assert window.transition_upper_bound == upper

    def test_negative_bounds(self):
        """Test setting negative bounds."""
        window = FeatureWeightingWindow(
            transition_lower_bound=-10.0, transition_upper_bound=-5.0
        )
        assert window.transition_lower_bound == -10.0
        assert window.transition_upper_bound == -5.0


class TestFeatureWeightingWindowCombinations:
    """Test FeatureWeightingWindow with various parameter combinations."""

    def test_full_initialization(self):
        """Test initializing with all parameters."""
        window = FeatureWeightingWindow(
            threshold="high cut",
            half_window_style="hamming",
            transition_lower_bound=0.1,
            transition_upper_bound=0.9,
        )
        assert window.threshold == "high cut"
        assert window.half_window_style == "hamming"
        assert window.transition_lower_bound == 0.1
        assert window.transition_upper_bound == 0.9

    @pytest.mark.parametrize(
        "threshold, style, lower, upper",
        [
            ("low cut", "hann", 0.0, 1.0),
            ("high cut", "hamming", 0.2, 0.8),
            ("low cut", "rectangle", -1.0, 1.0),
            ("high cut", "hann", 0.3, 0.999),
        ],
    )
    def test_parameter_combinations(self, threshold, style, lower, upper):
        """Test various parameter combinations."""
        window = FeatureWeightingWindow(
            threshold=threshold,
            half_window_style=style,
            transition_lower_bound=lower,
            transition_upper_bound=upper,
        )
        assert window.threshold == threshold
        assert window.half_window_style == style
        assert window.transition_lower_bound == lower
        assert window.transition_upper_bound == upper


class TestFeatureWeightingWindowSerialization:
    """Test FeatureWeightingWindow serialization methods."""

    def test_to_dict(self):
        """Test converting to dictionary."""
        window = FeatureWeightingWindow(
            threshold="high cut",
            half_window_style="hamming",
            transition_lower_bound=0.5,
            transition_upper_bound=0.9,
        )
        data = window.model_dump()
        assert data["threshold"] == "high cut"
        assert data["half_window_style"] == "hamming"
        assert data["transition_lower_bound"] == 0.5
        assert data["transition_upper_bound"] == 0.9

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "threshold": "low cut",
            "half_window_style": "rectangle",
            "transition_lower_bound": 0.2,
            "transition_upper_bound": 0.7,
        }
        window = FeatureWeightingWindow(**data)
        assert window.threshold == "low cut"
        assert window.half_window_style == "rectangle"
        assert window.transition_lower_bound == 0.2
        assert window.transition_upper_bound == 0.7

    def test_round_trip_serialization(self):
        """Test round-trip serialization to/from dict."""
        original = FeatureWeightingWindow(
            threshold="high cut",
            half_window_style="hann",
            transition_lower_bound=0.1,
            transition_upper_bound=0.9,
        )
        data = original.model_dump()
        restored = FeatureWeightingWindow(**data)
        assert restored.threshold == original.threshold
        assert restored.half_window_style == original.half_window_style
        assert restored.transition_lower_bound == original.transition_lower_bound
        assert restored.transition_upper_bound == original.transition_upper_bound

    def test_to_json(self):
        """Test JSON serialization."""
        window = FeatureWeightingWindow(
            threshold="low cut",
            half_window_style="hamming",
            transition_lower_bound=0.3,
            transition_upper_bound=0.8,
        )
        json_str = window.model_dump_json()
        assert "low cut" in json_str
        assert "hamming" in json_str
        assert isinstance(json_str, str)
