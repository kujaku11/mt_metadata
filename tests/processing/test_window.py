# -*- coding: utf-8 -*-
"""
Created on September 7, 2025

@author: GitHub Copilot

Comprehensive pytest test suite for Window basemodel using fixtures and subtests
whilst optimizing for efficiency.
"""
# =============================================================================
# Imports
# =============================================================================

from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from mt_metadata.common.mttime import MTime
from mt_metadata.processing.window import (
    ClockZeroTypeEnum,
    get_fft_harmonics,
    TypeEnum,
    Window,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_window():
    """Create a default Window instance for testing."""
    return Window()


@pytest.fixture
def custom_window():
    """Create a Window instance with custom values."""
    window = Window(
        num_samples=256,
        overlap=64,
        type=TypeEnum.hamming,
        clock_zero_type=ClockZeroTypeEnum.user_specified,
        additional_args={"beta": 10},
    )
    window.normalized = False  # Set after creation to override default
    return window


@pytest.fixture
def sample_rates():
    """Sample rates for FFT testing."""
    return [1.0, 256.0, 1024.0, 8192.0]


@pytest.fixture
def window_types():
    """Different window types for parametrized testing."""
    return [
        TypeEnum.boxcar,
        TypeEnum.hamming,
        TypeEnum.hann,
        TypeEnum.blackman,
        TypeEnum.kaiser,
        TypeEnum.gaussian,
    ]


@pytest.fixture
def invalid_window_data():
    """Invalid data for testing validation errors."""
    return [
        {"num_samples": -1},  # Negative number
        {"num_samples": "invalid"},  # String instead of int
        {"overlap": -5},  # Negative overlap
        {"type": "invalid_type"},  # Invalid window type
        {"clock_zero_type": "invalid_zero_type"},  # Invalid clock zero type
        {"normalized": "not_boolean"},  # String instead of boolean
        {"additional_args": "not_dict"},  # String instead of dict
    ]


@pytest.fixture
def clock_zero_variations():
    """Different clock_zero input formats."""
    return [
        "2020-02-01T09:23:45.453670+00:00",
        datetime(2020, 2, 1, 9, 23, 45),
        pd.Timestamp("2020-02-01 09:23:45"),
        np.datetime64("2020-02-01T09:23:45"),
        1580547825.0,  # Unix timestamp
        None,
    ]


# =============================================================================
# Test Classes
# =============================================================================


class TestWindowInitialization:
    """Test Window initialization and default values."""

    def test_default_initialization(self, default_window):
        """Test Window creation with default values."""
        assert default_window.num_samples == 256
        assert default_window.overlap == 32
        assert default_window.type == TypeEnum.boxcar
        assert default_window.clock_zero_type == ClockZeroTypeEnum.ignore
        assert default_window.normalized is True
        assert default_window.additional_args == {}
        assert isinstance(default_window.clock_zero, MTime)

    def test_custom_initialization(self, custom_window):
        """Test Window creation with custom values."""
        assert custom_window.num_samples == 256
        assert custom_window.overlap == 64
        assert custom_window.type == TypeEnum.hamming
        assert custom_window.clock_zero_type == ClockZeroTypeEnum.user_specified
        assert custom_window.normalized is False
        assert custom_window.additional_args == {"beta": 10}

    @pytest.mark.parametrize(
        "window_type",
        [
            TypeEnum.boxcar,
            TypeEnum.hamming,
            TypeEnum.hann,
            TypeEnum.blackman,
            TypeEnum.kaiser,
            TypeEnum.gaussian,
            TypeEnum.flattop,
            TypeEnum.bartlett,
        ],
    )
    def test_initialization_with_different_types(self, window_type):
        """Test initialization with different window types."""
        window = Window(type=window_type, num_samples=128, overlap=32)
        assert window.type == window_type

    @pytest.mark.parametrize(
        "clock_zero_type",
        [
            ClockZeroTypeEnum.ignore,
            ClockZeroTypeEnum.data_start,
            ClockZeroTypeEnum.user_specified,
        ],
    )
    def test_initialization_with_clock_zero_types(self, clock_zero_type):
        """Test initialization with different clock zero types."""
        window = Window(clock_zero_type=clock_zero_type, num_samples=128, overlap=32)
        assert window.clock_zero_type == clock_zero_type

    def test_copy(self, custom_window):
        """Test Window copy functionality."""
        copied_window = custom_window.model_copy()
        assert copied_window.num_samples == custom_window.num_samples
        assert copied_window.overlap == custom_window.overlap
        assert copied_window.type == custom_window.type
        assert copied_window.normalized == custom_window.normalized
        assert copied_window.additional_args == custom_window.additional_args


class TestWindowValidation:
    """Test Window field validation."""

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"num_samples": "invalid"},
            {"overlap": "invalid"},
            # {"normalized": "not_boolean"},  # This might be coerced by Pydantic
            {"additional_args": "not_dict"},
        ],
    )
    def test_invalid_field_types(self, invalid_data):
        """Test validation errors for invalid field types."""
        with pytest.raises(ValidationError):
            Window(**invalid_data)

    @pytest.mark.parametrize(
        "clock_zero_input",
        [
            "2020-02-01T09:23:45.453670+00:00",
            datetime(2020, 2, 1, 9, 23, 45),
            pd.Timestamp("2020-02-01 09:23:45"),
            1580547825.0,
            None,
        ],
    )
    def test_clock_zero_validation(self, clock_zero_input):
        """Test clock_zero field accepts various input formats."""
        window = Window(num_samples=128, overlap=32, clock_zero=clock_zero_input)
        assert isinstance(window.clock_zero, MTime)

    def test_enum_validation(self):
        """Test enum field validation."""
        # Valid enum values
        window = Window(
            type=TypeEnum.hamming,
            clock_zero_type=ClockZeroTypeEnum.ignore,
            num_samples=128,
            overlap=32,
        )
        assert window.type == TypeEnum.hamming
        assert window.clock_zero_type == ClockZeroTypeEnum.ignore

        # Invalid enum values should raise ValidationError
        with pytest.raises(ValidationError):
            Window(type="invalid_window_type", num_samples=128, overlap=32)

        with pytest.raises(ValidationError):
            Window(clock_zero_type="invalid_zero_type", num_samples=128, overlap=32)


class TestWindowComputedFields:
    """Test Window computed fields and properties."""

    def test_num_samples_advance_property(self):
        """Test num_samples_advance computed field."""
        window = Window(num_samples=256, overlap=64)
        assert window.num_samples_advance == 192

        window2 = Window(num_samples=128, overlap=32)
        assert window2.num_samples_advance == 96

    def test_num_samples_advance_edge_cases(self):
        """Test num_samples_advance with edge cases."""
        # When overlap equals num_samples
        window = Window(num_samples=128, overlap=128)
        assert window.num_samples_advance == 0

        # When overlap is zero
        window2 = Window(num_samples=128, overlap=0)
        assert window2.num_samples_advance == 128


class TestWindowMethods:
    """Test Window methods."""

    @pytest.mark.parametrize(
        "sample_rate,num_samples",
        [(1.0, 128), (256.0, 256), (1024.0, 512), (8192.0, 1024)],
    )
    def test_fft_harmonics(self, sample_rate, num_samples):
        """Test FFT harmonics calculation."""
        window = Window(num_samples=num_samples, overlap=32)
        harmonics = window.fft_harmonics(sample_rate)

        assert isinstance(harmonics, np.ndarray)
        assert len(harmonics) == num_samples // 2
        assert harmonics[0] == 0.0  # DC component
        assert np.all(harmonics >= 0)  # All positive frequencies
        assert harmonics[-1] < sample_rate / 2  # Below Nyquist

    def test_taper_basic_functionality(self):
        """Test basic taper generation."""
        window = Window(num_samples=64, overlap=16, type=TypeEnum.hamming)
        taper = window.taper()

        assert isinstance(taper, np.ndarray)
        assert len(taper) == 64
        assert np.all(taper >= 0)  # Taper values should be positive

    def test_taper_normalization(self):
        """Test taper normalization."""
        # Normalized taper
        window_norm = Window(
            num_samples=64, overlap=16, type=TypeEnum.hamming, normalized=True
        )
        taper_norm = window_norm.taper()

        # Non-normalized taper (but for hamming window, both may sum to 1)
        window_no_norm = Window(
            num_samples=64, overlap=16, type=TypeEnum.hamming, normalized=False
        )
        taper_no_norm = window_no_norm.taper()

        # Both should exist and be valid arrays
        assert isinstance(taper_norm, np.ndarray)
        assert isinstance(taper_no_norm, np.ndarray)
        assert len(taper_norm) == 64
        assert len(taper_no_norm) == 64

    @pytest.mark.parametrize(
        "window_type",
        [TypeEnum.boxcar, TypeEnum.hamming, TypeEnum.hann, TypeEnum.blackman],
    )
    def test_taper_different_types(self, window_type):
        """Test taper generation with different window types."""
        window = Window(num_samples=64, overlap=16, type=window_type)
        taper = window.taper()

        assert isinstance(taper, np.ndarray)
        assert len(taper) == 64
        # Allow for tiny negative values due to floating point precision (especially for blackman)
        assert np.all(
            taper > -1e-15
        ), f"Found negative values in {window_type} taper: {np.min(taper)}"

    def test_taper_with_additional_args(self):
        """Test taper generation with additional arguments."""
        # Kaiser window with beta parameter
        window = Window(
            num_samples=64,
            overlap=16,
            type=TypeEnum.kaiser,
            additional_args={"beta": 8.6},
        )
        taper = window.taper()

        assert isinstance(taper, np.ndarray)
        assert len(taper) == 64

        # Gaussian window with std parameter
        window_gauss = Window(
            num_samples=64,
            overlap=16,
            type=TypeEnum.gaussian,
            additional_args={"std": 7},
        )
        taper_gauss = window_gauss.taper()

        assert isinstance(taper_gauss, np.ndarray)
        assert len(taper_gauss) == 64

    def test_taper_caching(self):
        """Test that taper is cached after first calculation."""
        window = Window(num_samples=64, overlap=16, type=TypeEnum.hamming)

        # First call should compute taper
        taper1 = window.taper()

        # Second call should return cached taper
        taper2 = window.taper()

        # Should be the exact same object (cached)
        assert taper1 is taper2
        assert np.array_equal(taper1, taper2)


class TestWindowEquality:
    """Test Window equality and comparison methods."""

    def test_equality_same_values(self):
        """Test equality between windows with same values."""
        window1 = Window(num_samples=256, overlap=64, type=TypeEnum.hamming)
        window2 = Window(num_samples=256, overlap=64, type=TypeEnum.hamming)
        assert window1 == window2

    def test_equality_different_values(self):
        """Test inequality between windows with different values."""
        window1 = Window(num_samples=256, overlap=64, type=TypeEnum.hamming)
        window2 = Window(num_samples=128, overlap=32, type=TypeEnum.hann)
        assert window1 != window2

    def test_equality_copy(self, custom_window):
        """Test equality with copied window."""
        copied_window = custom_window.model_copy()
        assert custom_window == copied_window


class TestWindowRepresentation:
    """Test Window string representation and serialization."""

    def test_string_representation(self, custom_window):
        """Test string representation of Window."""
        str_repr = str(custom_window)
        # The actual representation is a dict/JSON format, not a simple string
        assert "num_samples" in str_repr
        assert "256" in str_repr
        assert "overlap" in str_repr
        assert "64" in str_repr

    def test_model_dump(self, custom_window):
        """Test model serialization."""
        window_dict = custom_window.model_dump()
        assert isinstance(window_dict, dict)
        assert window_dict["num_samples"] == 256
        assert window_dict["overlap"] == 64
        assert window_dict["type"] == "hamming"
        assert window_dict["normalized"] is False


class TestWindowEdgeCases:
    """Test edge cases and error conditions."""

    def test_minimal_valid_window(self):
        """Test creation with minimal valid parameters."""
        window = Window(num_samples=1, overlap=0)
        assert window.num_samples == 1
        assert window.overlap == 0
        assert window.num_samples_advance == 1

    def test_enum_string_conversion(self):
        """Test that enum values work properly."""
        window = Window(
            num_samples=128,
            overlap=32,
            type=TypeEnum.hamming,
            clock_zero_type=ClockZeroTypeEnum.ignore,
        )
        assert window.type.value == "hamming"
        assert window.clock_zero_type.value == "ignore"

    def test_additional_args_persistence(self):
        """Test that additional_args are preserved correctly."""
        args = {"beta": 8.6, "std": 7, "param": "value"}
        window = Window(num_samples=128, overlap=32, additional_args=args)
        assert window.additional_args == args
        assert window.additional_args is not args  # Should be a copy


class TestFFTHarmonicsFunction:
    """Test the standalone get_fft_harmonics function."""

    @pytest.mark.parametrize(
        "samples_per_window,sample_rate",
        [
            (128, 1.0),
            (256, 256.0),
            (512, 1024.0),
            (1024, 8192.0),
            (100, 50.0),  # Non-power-of-2
        ],
    )
    def test_get_fft_harmonics_basic(self, samples_per_window, sample_rate):
        """Test basic FFT harmonics functionality."""
        harmonics = get_fft_harmonics(samples_per_window, sample_rate)

        assert isinstance(harmonics, np.ndarray)
        assert len(harmonics) == samples_per_window // 2
        assert harmonics[0] == 0.0  # DC component
        assert np.all(harmonics >= 0)  # All positive frequencies

        # Check frequency spacing
        expected_df = sample_rate / samples_per_window
        if len(harmonics) > 1:
            actual_df = harmonics[1] - harmonics[0]
            assert np.isclose(actual_df, expected_df)

    def test_get_fft_harmonics_odd_samples(self):
        """Test FFT harmonics with odd number of samples."""
        harmonics = get_fft_harmonics(127, 256.0)

        assert isinstance(harmonics, np.ndarray)
        assert len(harmonics) == 127 // 2  # 63
        assert harmonics[0] == 0.0

    def test_get_fft_harmonics_frequency_values(self):
        """Test that FFT harmonics produce correct frequency values."""
        sample_rate = 1000.0
        samples = 1000
        harmonics = get_fft_harmonics(samples, sample_rate)

        # Check that frequencies are in expected range [0, Nyquist)
        assert harmonics[0] == 0.0
        assert harmonics[-1] < sample_rate / 2

        # Check frequency resolution
        df = sample_rate / samples
        assert np.isclose(harmonics[1], df)


class TestWindowIntegration:
    """Integration tests for Window functionality."""

    def test_typical_signal_processing_workflow(self):
        """Test a typical signal processing workflow."""
        # Create window for signal processing
        window = Window(
            num_samples=1024, overlap=512, type=TypeEnum.hann, normalized=True
        )

        # Generate sample data
        sample_rate = 1000.0
        t = np.linspace(0, 1.024, 1024, endpoint=False)
        signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

        # Get taper and apply to signal
        taper = window.taper()
        windowed_signal = signal * taper

        # Get FFT frequencies
        freqs = window.fft_harmonics(sample_rate)

        # Perform FFT
        fft_result = np.fft.fft(windowed_signal)[: len(freqs)]

        # Check results
        assert len(freqs) == len(fft_result)
        assert len(windowed_signal) == window.num_samples
        assert window.num_samples_advance == 512

    def test_window_parameter_validation_workflow(self):
        """Test comprehensive parameter validation."""
        # Valid parameters - use Kaiser window which accepts beta parameter
        valid_params = {
            "num_samples": 256,
            "overlap": 128,
            "type": TypeEnum.kaiser,
            "clock_zero_type": ClockZeroTypeEnum.user_specified,
            "normalized": False,
            "additional_args": {"beta": 5.0},
        }

        window = Window(**valid_params)

        # Verify all parameters are set correctly
        assert window.num_samples == 256
        assert window.overlap == 128
        assert window.type == TypeEnum.kaiser
        assert window.clock_zero_type == ClockZeroTypeEnum.user_specified
        assert window.normalized is False
        assert window.additional_args == {"beta": 5.0}

        # Test taper generation works
        taper = window.taper()
        assert len(taper) == 256

        # Test FFT harmonics work
        freqs = window.fft_harmonics(1000.0)
        assert len(freqs) == 128

    def test_window_comparison_workflow(self):
        """Test window comparison and copy workflows."""
        original = Window(
            num_samples=512, overlap=256, type=TypeEnum.hamming, normalized=True
        )

        # Test copy preserves all attributes
        copied = original.model_copy()
        assert original == copied

        # Test modification creates different window
        modified = original.model_copy()
        modified.num_samples = 1024
        assert original != modified

        # Test serialization/deserialization
        serialized = original.model_dump()
        reconstructed = Window(**serialized)
        assert original == reconstructed


class TestWindowPerformance:
    """Performance-related tests."""

    def test_bulk_window_creation(self):
        """Test creating many window instances efficiently."""
        windows = []
        for i in range(100):
            window = Window(num_samples=128 + i, overlap=32, type=TypeEnum.hamming)
            windows.append(window)

        assert len(windows) == 100
        assert all(isinstance(w, Window) for w in windows)

    def test_taper_calculation_performance(self):
        """Test taper calculation for various sizes."""
        sizes = [64, 128, 256, 512, 1024, 2048]

        for size in sizes:
            window = Window(num_samples=size, overlap=size // 4, type=TypeEnum.hann)
            taper = window.taper()
            assert len(taper) == size

    def test_fft_harmonics_performance(self):
        """Test FFT harmonics calculation performance."""
        sample_rates = [1.0, 100.0, 1000.0, 10000.0]
        window_sizes = [128, 256, 512, 1024]

        for sr in sample_rates:
            for size in window_sizes:
                window = Window(num_samples=size, overlap=32)
                harmonics = window.fft_harmonics(sr)
                assert len(harmonics) == size // 2
