# -*- coding: utf-8 -*-
"""
Created on December 15, 2024

@author: GitHub Copilot

Comprehensive pytest test suite for StridingWindowCoherence basemodel using fixtures and subtests
whilst optimizing for efficiency.
"""
# =============================================================================
# Imports
# =============================================================================

from unittest.mock import patch

import numpy as np
import pytest
from pydantic import ValidationError

from mt_metadata.features.coherence_basemodel import Coherence
from mt_metadata.features.striding_window_coherence_basemodel import (
    StridingWindowCoherence,
)
from mt_metadata.processing.window import TypeEnum, Window


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_striding_coherence():
    """Create a default StridingWindowCoherence instance for testing."""
    return StridingWindowCoherence()


@pytest.fixture
def sample_time_series():
    """Generate sample time series data for coherence testing."""
    np.random.seed(42)  # For reproducible tests
    n_samples = 1000
    fs = 100.0
    t = np.linspace(0, n_samples / fs, n_samples, endpoint=False)

    # Create two correlated signals with some noise
    f1, f2 = 10.0, 15.0
    signal1 = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)
    signal2 = 0.8 * signal1 + 0.3 * np.random.randn(n_samples)

    return signal1, signal2, fs


@pytest.fixture
def window_configurations():
    """Different window configurations for testing."""
    return [
        {"num_samples": 256, "overlap": 128, "type": TypeEnum.hann},
        {"num_samples": 512, "overlap": 256, "type": TypeEnum.hamming},
        {"num_samples": 128, "overlap": 64, "type": TypeEnum.blackman},
        {"num_samples": 1024, "overlap": 512, "type": TypeEnum.kaiser},
    ]


@pytest.fixture
def subwindow_configurations():
    """Different subwindow configurations for striding."""
    return [
        {"num_samples": 64, "overlap": 32, "type": TypeEnum.hann},
        {"num_samples": 128, "overlap": 64, "type": TypeEnum.hamming},
        {"num_samples": 32, "overlap": 16, "type": TypeEnum.blackman},
        {"num_samples": 256, "overlap": 128, "type": TypeEnum.boxcar},
    ]


@pytest.fixture
def configured_striding_coherence(window_configurations, subwindow_configurations):
    """Create a StridingWindowCoherence with configured windows."""
    coherence = StridingWindowCoherence(
        window=Window(**window_configurations[0]),
        subwindow=Window(**subwindow_configurations[0]),
        station_1="MT001",
        station_2="MT002",
        channel_1="hx",
        channel_2="hy",
    )
    return coherence


@pytest.fixture
def invalid_striding_data():
    """Invalid data for testing validation errors."""
    return [
        {"subwindow": "not_a_window"},  # String instead of Window
        {"subwindow": 123},  # Number instead of Window
        {"subwindow": None, "window": None},  # Both None
        {
            "window": {"num_samples": 128},
            "subwindow": {"num_samples": 256},
        },  # Subwindow larger than window
    ]


@pytest.fixture
def edge_case_windows():
    """Edge case window configurations."""
    return [
        {"num_samples": 1, "overlap": 0, "type": TypeEnum.boxcar},  # Minimal window
        {
            "num_samples": 2,
            "overlap": 1,
            "type": TypeEnum.hann,
        },  # Small window with overlap
        {"num_samples": 1000, "overlap": 999, "type": TypeEnum.hamming},  # High overlap
    ]


# =============================================================================
# Test Classes
# =============================================================================


class TestStridingWindowCoherenceInitialization:
    """Test StridingWindowCoherence initialization and inheritance."""

    def test_default_initialization(self, default_striding_coherence):
        """Test StridingWindowCoherence creation with default values."""
        assert isinstance(default_striding_coherence, StridingWindowCoherence)
        assert isinstance(default_striding_coherence, Coherence)
        assert isinstance(default_striding_coherence.subwindow, Window)
        assert default_striding_coherence.subwindow.type == TypeEnum.boxcar

    def test_inheritance_from_coherence(self, default_striding_coherence):
        """Test that StridingWindowCoherence properly inherits from Coherence."""
        # Check inherited attributes exist
        assert hasattr(default_striding_coherence, "station_1")
        assert hasattr(default_striding_coherence, "station_2")
        assert hasattr(default_striding_coherence, "channel_1")
        assert hasattr(default_striding_coherence, "channel_2")
        assert hasattr(default_striding_coherence, "window")
        assert hasattr(default_striding_coherence, "detrend")

        # Check new attribute
        assert hasattr(default_striding_coherence, "subwindow")

    def test_custom_initialization_with_subwindow(
        self, window_configurations, subwindow_configurations
    ):
        """Test initialization with custom subwindow configuration."""
        window_config = window_configurations[0]
        subwindow_config = subwindow_configurations[0]

        coherence = StridingWindowCoherence(
            window=Window(**window_config),
            subwindow=Window(**subwindow_config),
            station_1="MT001",
            station_2="MT002",
        )

        assert coherence.window.num_samples == window_config["num_samples"]
        assert coherence.subwindow.num_samples == subwindow_config["num_samples"]
        assert coherence.window.type == window_config["type"]
        assert coherence.subwindow.type == subwindow_config["type"]

    @pytest.mark.parametrize(
        "window_config",
        [
            {"num_samples": 256, "overlap": 128, "type": TypeEnum.hann},
            {"num_samples": 512, "overlap": 256, "type": TypeEnum.hamming},
            {"num_samples": 1024, "overlap": 512, "type": TypeEnum.blackman},
        ],
    )
    def test_initialization_with_different_windows(self, window_config):
        """Test initialization with different window configurations."""
        coherence = StridingWindowCoherence(
            window=Window(**window_config), station_1="TEST1", station_2="TEST2"
        )
        assert coherence.window.num_samples == window_config["num_samples"]
        assert coherence.window.type == window_config["type"]

    def test_model_validator_sets_subwindow_from_window(self):
        """Test that model validator sets subwindow from window when not provided."""
        window = Window(num_samples=256, overlap=128, type=TypeEnum.hann)
        coherence = StridingWindowCoherence(
            window=window, station_1="TEST1", station_2="TEST2"
        )

        # Should have called set_subwindow_from_window
        assert coherence.subwindow is not None
        assert isinstance(coherence.subwindow, Window)


class TestStridingWindowCoherenceSubwindowManagement:
    """Test subwindow management functionality."""

    def test_set_subwindow_from_window_method(self):
        """Test the set_subwindow_from_window method."""
        coherence = StridingWindowCoherence()
        window = Window(num_samples=256, overlap=128, type=TypeEnum.hann)
        coherence.window = window

        coherence.set_subwindow_from_window()

        assert coherence.subwindow is not None
        assert isinstance(coherence.subwindow, Window)
        assert coherence.subwindow.type == window.type

    def test_subwindow_inherits_window_properties(self):
        """Test that subwindow inherits appropriate properties from main window."""
        window = Window(
            num_samples=512, overlap=256, type=TypeEnum.hamming, normalized=False
        )
        coherence = StridingWindowCoherence(
            window=window, station_1="TEST1", station_2="TEST2"
        )

        # Call the method to set subwindow from window
        coherence.set_subwindow_from_window()

        # Only type is inherited; other properties use Window defaults
        assert coherence.subwindow.type == window.type.value  # Compare string values
        assert coherence.subwindow.num_samples == int(
            window.num_samples * 0.2
        )  # 20% of 512 = 102
        assert coherence.subwindow.overlap == int(
            coherence.subwindow.num_samples // 2
        )  # Half of num_samples

    @pytest.mark.parametrize(
        "subwindow_config",
        [
            {"num_samples": 64, "overlap": 32, "type": TypeEnum.hann},
            {"num_samples": 128, "overlap": 64, "type": TypeEnum.hamming},
            {"num_samples": 32, "overlap": 16, "type": TypeEnum.blackman},
        ],
    )
    def test_explicit_subwindow_configuration(self, subwindow_config):
        """Test setting explicit subwindow configurations."""
        coherence = StridingWindowCoherence(
            window=Window(num_samples=256, overlap=128),
            subwindow=Window(**subwindow_config),
            station_1="TEST1",
            station_2="TEST2",
        )

        assert coherence.subwindow.num_samples == subwindow_config["num_samples"]
        assert coherence.subwindow.overlap == subwindow_config["overlap"]
        assert coherence.subwindow.type == subwindow_config["type"]

    def test_subwindow_smaller_than_window_validation(self):
        """Test that subwindow should be smaller or equal to main window."""
        window = Window(num_samples=128, overlap=64)

        # This should work - subwindow smaller than window
        coherence = StridingWindowCoherence(
            window=window,
            subwindow=Window(num_samples=64, overlap=32),
            station_1="TEST1",
            station_2="TEST2",
        )
        assert coherence.subwindow.num_samples <= coherence.window.num_samples

    def test_subwindow_equal_to_window_allowed(self):
        """Test that subwindow can be equal to main window."""
        window_config = {"num_samples": 128, "overlap": 64, "type": TypeEnum.hann}

        coherence = StridingWindowCoherence(
            window=Window(**window_config),
            subwindow=Window(**window_config),
            station_1="TEST1",
            station_2="TEST2",
        )

        assert coherence.subwindow.num_samples == coherence.window.num_samples


class TestStridingWindowCoherenceComputation:
    """Test the compute method for striding window coherence."""

    def test_compute_returns_frequency_and_coherence_array(
        self, configured_striding_coherence, sample_time_series
    ):
        """Test that compute returns frequency array and 2D coherence array."""
        signal1, signal2, fs = sample_time_series

        with patch(
            "mt_metadata.features.striding_window_coherence_basemodel.ssig.coherence"
        ) as mock_coherence:
            # Mock scipy.signal.coherence to return predictable results
            mock_f = np.linspace(0, fs / 2, 129)
            mock_coh = np.random.rand(129)
            mock_coherence.return_value = (mock_f, mock_coh)

            f, coh_array = configured_striding_coherence.compute(signal1, signal2)

            assert isinstance(f, np.ndarray)
            assert isinstance(coh_array, np.ndarray)
            assert coh_array.ndim == 2  # Should be 2D array
            assert len(f) == coh_array.shape[1]  # Frequency dimension matches

    def test_compute_with_different_window_configurations(
        self, sample_time_series, window_configurations, subwindow_configurations
    ):
        """Test compute with various window configurations."""
        signal1, signal2, fs = sample_time_series
        signal_length = len(signal1)

        for i, (window_config, subwindow_config) in enumerate(
            zip(window_configurations, subwindow_configurations)
        ):
            # Skip configurations where window is larger than signal
            if window_config["num_samples"] > signal_length:
                continue

            coherence = StridingWindowCoherence(
                window=Window(**window_config),
                subwindow=Window(**subwindow_config),
                station_1="TEST1",
                station_2="TEST2",
                channel_1="hx",
                channel_2="hy",
            )

            with patch(
                "mt_metadata.features.striding_window_coherence_basemodel.ssig.coherence"
            ) as mock_coherence:
                mock_f = np.linspace(0, fs / 2, 65)
                mock_coh = np.random.rand(65)
                mock_coherence.return_value = (mock_f, mock_coh)

                f, coh_array = coherence.compute(signal1, signal2)

                assert isinstance(f, np.ndarray)
                assert isinstance(coh_array, np.ndarray)
                assert coh_array.ndim == 2

    def test_compute_calls_scipy_coherence_correctly(
        self, configured_striding_coherence, sample_time_series
    ):
        """Test that compute calls scipy.signal.coherence with correct parameters."""
        signal1, signal2, fs = sample_time_series

        with patch(
            "mt_metadata.features.striding_window_coherence_basemodel.ssig.coherence"
        ) as mock_coherence:
            mock_f = np.linspace(0, fs / 2, 33)
            mock_coh = np.random.rand(33)
            mock_coherence.return_value = (mock_f, mock_coh)

            configured_striding_coherence.compute(signal1, signal2)

            # Verify scipy.signal.coherence was called
            assert mock_coherence.called
            call_args = mock_coherence.call_args

            # Check that correct parameters were passed
            assert "window" in call_args.kwargs
            assert "nperseg" in call_args.kwargs
            assert "noverlap" in call_args.kwargs
            assert "detrend" in call_args.kwargs

            # Note: fs is not passed to scipy coherence in this implementation
            assert (
                call_args.kwargs["window"]
                == configured_striding_coherence.subwindow.type
            )
            assert (
                call_args.kwargs["nperseg"]
                == configured_striding_coherence.subwindow.num_samples
            )
            assert (
                call_args.kwargs["noverlap"]
                == configured_striding_coherence.subwindow.overlap
            )

    def test_compute_with_striding_windows(self, sample_time_series):
        """Test compute with actual striding through the data."""
        signal1, signal2, fs = sample_time_series

        coherence = StridingWindowCoherence(
            window=Window(num_samples=200, overlap=100),
            subwindow=Window(num_samples=64, overlap=32),
            station_1="TEST1",
            station_2="TEST2",
            channel_1="hx",
            channel_2="hy",
        )

        with patch(
            "mt_metadata.features.striding_window_coherence_basemodel.ssig.coherence"
        ) as mock_coherence:
            mock_f = np.linspace(0, fs / 2, 33)
            mock_coh = np.random.rand(33)
            mock_coherence.return_value = (mock_f, mock_coh)

            f, coh_array = coherence.compute(signal1, signal2)

            # Should have multiple calls for different windows
            assert mock_coherence.call_count > 1
            assert coh_array.shape[0] > 1  # Multiple windows processed

    def test_compute_empty_signals_handling(self, configured_striding_coherence):
        """Test compute method with empty or very short signals."""
        empty_signal1 = np.array([])
        empty_signal2 = np.array([])

        # Empty signals cause UnboundLocalError because no windows can be processed
        with pytest.raises(UnboundLocalError):
            configured_striding_coherence.compute(empty_signal1, empty_signal2)

    def test_compute_mismatched_signal_lengths(self, configured_striding_coherence):
        """Test compute method with signals of different lengths."""
        signal1 = np.random.randn(1000)
        signal2 = np.random.randn(500)  # Different length

        with pytest.raises((ValueError, IndexError)):
            configured_striding_coherence.compute(signal1, signal2)


class TestStridingWindowCoherenceValidation:
    """Test validation and error handling."""

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"subwindow": "not_a_window"},
            {"subwindow": 123},
            {"subwindow": None, "window": None},
        ],
    )
    def test_invalid_subwindow_types(self, invalid_data):
        """Test validation with invalid subwindow types."""
        with pytest.raises(ValidationError):
            StridingWindowCoherence(**invalid_data)

    def test_subwindow_field_validation(self):
        """Test that subwindow field accepts only Window instances."""
        coherence = StridingWindowCoherence()

        # Valid assignment
        coherence.subwindow = Window(num_samples=64)
        assert isinstance(coherence.subwindow, Window)

        # Invalid assignment should raise error
        with pytest.raises(ValidationError):
            coherence.subwindow = "not_a_window"

    def test_model_validation_with_no_window(self):
        """Test model validation when no window is provided."""
        # Should still create a default subwindow
        coherence = StridingWindowCoherence(station_1="TEST1", station_2="TEST2")
        assert coherence.subwindow is not None
        assert isinstance(coherence.subwindow, Window)

    @pytest.mark.parametrize(
        "edge_case",
        [
            {"num_samples": 1, "overlap": 0},
            {"num_samples": 2, "overlap": 1},
        ],
    )
    def test_edge_case_window_sizes(self, edge_case):
        """Test with edge case window configurations."""
        window = Window(**edge_case, type=TypeEnum.boxcar)

        # Should not raise error during initialization
        coherence = StridingWindowCoherence(
            window=window, station_1="TEST1", station_2="TEST2"
        )
        assert coherence.window.num_samples == edge_case["num_samples"]

    def test_inheritance_validation_preserved(self):
        """Test that validation from parent Coherence class is preserved."""
        # Since model_validator provides defaults, test that we get a properly initialized object
        # with inheritance from Coherence class intact
        coherence = StridingWindowCoherence()

        # Verify it properly inherits from Coherence
        assert isinstance(coherence, Coherence)
        assert hasattr(coherence, "channel_1")
        assert hasattr(coherence, "channel_2")
        assert hasattr(coherence, "station_1")
        assert hasattr(coherence, "station_2")

        # Verify striding-specific field exists
        assert hasattr(coherence, "subwindow")

    def test_all_coherence_attributes_accessible(self, configured_striding_coherence):
        """Test that all Coherence attributes are accessible."""
        coherence_attrs = [
            "station_1",
            "station_2",
            "channel_1",
            "channel_2",
            "window",
            "detrend",
        ]

        for attr in coherence_attrs:
            assert hasattr(configured_striding_coherence, attr)

    def test_striding_specific_attributes(self, configured_striding_coherence):
        """Test StridingWindowCoherence specific attributes."""
        assert hasattr(configured_striding_coherence, "subwindow")
        assert hasattr(configured_striding_coherence, "set_subwindow_from_window")


class TestStridingWindowCoherenceIntegration:
    """Test integration scenarios and edge cases."""

    def test_full_workflow_integration(self, sample_time_series):
        """Test complete workflow from initialization to computation."""
        signal1, signal2, fs = sample_time_series

        # Create with realistic parameters
        coherence = StridingWindowCoherence(
            window=Window(num_samples=256, overlap=128, type=TypeEnum.hann),
            subwindow=Window(num_samples=64, overlap=32, type=TypeEnum.hann),
            station_1="MT001",
            station_2="MT002",
            channel_1="hx",
            channel_2="hy",
        )

        with patch(
            "mt_metadata.features.striding_window_coherence_basemodel.ssig.coherence"
        ) as mock_coherence:
            mock_f = np.linspace(0, fs / 2, 33)
            mock_coh = np.random.rand(33)
            mock_coherence.return_value = (mock_f, mock_coh)

            f, coh_array = coherence.compute(signal1, signal2)

            assert isinstance(f, np.ndarray)
            assert isinstance(coh_array, np.ndarray)
            assert coh_array.ndim == 2
            assert len(f) == coh_array.shape[1]

    def test_serialization_deserialization(self, configured_striding_coherence):
        """Test that StridingWindowCoherence can be serialized and deserialized."""
        # Test dictionary conversion
        coherence_dict = configured_striding_coherence.model_dump()
        assert "subwindow" in coherence_dict

        # Test recreation from dictionary
        new_coherence = StridingWindowCoherence(**coherence_dict)
        assert isinstance(new_coherence.subwindow, Window)
        assert new_coherence.station_1 == configured_striding_coherence.station_1

    def test_copy_and_modification(self, configured_striding_coherence):
        """Test copying and modifying StridingWindowCoherence instances."""
        # Test model copy
        copied_coherence = configured_striding_coherence.model_copy()
        assert isinstance(copied_coherence, StridingWindowCoherence)
        assert copied_coherence.station_1 == configured_striding_coherence.station_1

        # Modify copy
        copied_coherence.station_1 = "MODIFIED"
        assert copied_coherence.station_1 != configured_striding_coherence.station_1

    def test_equality_comparison(self, window_configurations, subwindow_configurations):
        """Test equality comparison between StridingWindowCoherence instances."""
        config1 = {
            "window": Window(**window_configurations[0]),
            "subwindow": Window(**subwindow_configurations[0]),
            "station_1": "MT001",
            "station_2": "MT002",
        }

        coherence1 = StridingWindowCoherence(**config1)
        coherence2 = StridingWindowCoherence(**config1)

        # Should be equal with same configuration
        assert coherence1.model_dump() == coherence2.model_dump()
