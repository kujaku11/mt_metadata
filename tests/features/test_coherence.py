"""
Comprehensive pytest suite for Coherence class.

Tests cover instantiation, field validation, model validation,
station ID validation, computation methods, and edge cases.
"""

from unittest.mock import patch

import numpy as np
import pytest

from mt_metadata.features.coherence import Coherence, DetrendEnum
from mt_metadata.features.feature import Feature
from mt_metadata.processing.window import Window


class TestCoherenceInstantiation:
    """Test basic instantiation and default values."""

    def test_default_instantiation(self):
        """Test Coherence can be instantiated with defaults."""
        coh = Coherence()
        assert isinstance(coh, Coherence)
        assert isinstance(coh, Feature)  # Inheritance
        assert coh.name == "coherence"
        assert coh.domain.value == "frequency"
        assert coh.channel_1 == ""
        assert coh.channel_2 == ""
        assert coh.detrend == DetrendEnum.linear
        assert coh.station_1 is None
        assert coh.station_2 is None
        assert isinstance(coh.window, Window)

    def test_instantiation_with_channels(self):
        """Test Coherence instantiation with channel parameters."""
        coh = Coherence(channel_1="ex", channel_2="hy")
        assert coh.channel_1 == "ex"
        assert coh.channel_2 == "hy"
        assert coh.name == "coherence"  # Set by model validator

    def test_instantiation_with_all_params(self):
        """Test Coherence instantiation with all parameters."""
        window = Window(num_samples=512, overlap=256, type="hann")
        coh = Coherence(
            channel_1="hx",
            channel_2="ey",
            detrend="constant",
            station_1="PKD",
            station_2="SAO",
            window=window,
        )
        assert coh.channel_1 == "hx"
        assert coh.channel_2 == "ey"
        assert coh.detrend == DetrendEnum.constant
        assert coh.station_1 == "PKD"
        assert coh.station_2 == "SAO"
        assert coh.window.num_samples == 512
        assert coh.window.overlap == 256
        assert coh.window.type == "hann"


class TestCoherenceInheritance:
    """Test inheritance from Feature class."""

    def test_inheritance_structure(self):
        """Test that Coherence properly inherits from Feature."""
        coh = Coherence()

        # From Feature class
        assert hasattr(coh, "name")
        assert hasattr(coh, "description")
        assert hasattr(coh, "domain")
        assert hasattr(coh, "data")
        assert hasattr(coh, "comments")

        # Coherence specific fields
        assert hasattr(coh, "channel_1")
        assert hasattr(coh, "channel_2")
        assert hasattr(coh, "detrend")
        assert hasattr(coh, "station_1")
        assert hasattr(coh, "station_2")
        assert hasattr(coh, "window")

    def test_method_resolution_order(self):
        """Test that method resolution order is correct."""
        mro = Coherence.__mro__
        assert Coherence in mro
        assert Feature in mro
        assert object in mro


class TestCoherenceFieldValidation:
    """Test field validation and types."""

    @pytest.mark.parametrize(
        "channel_name", ["ex", "ey", "hx", "hy", "hz", "rx", "ry", "Ex", "EY"]
    )
    def test_channel_validation(self, channel_name):
        """Test channel field validation with valid channel names."""
        coh = Coherence(channel_1=channel_name, channel_2="hy")
        assert coh.channel_1 == channel_name
        assert coh.channel_2 == "hy"

    @pytest.mark.parametrize("detrend_type", ["linear", "constant"])
    def test_detrend_validation(self, detrend_type):
        """Test detrend enum validation."""
        coh = Coherence(detrend=detrend_type)
        assert coh.detrend.value == detrend_type

    def test_invalid_detrend_validation(self):
        """Test invalid detrend enum raises validation error."""
        with pytest.raises(Exception):  # Pydantic validation error
            Coherence(detrend="invalid_type")

    @pytest.mark.parametrize("station_name", ["PKD", "SAO", "TEST_STATION", None, ""])
    def test_station_validation(self, station_name):
        """Test station field validation."""
        coh = Coherence(station_1=station_name, station_2=station_name)
        assert coh.station_1 == station_name
        assert coh.station_2 == station_name


class TestCoherenceWindow:
    """Test Window object integration."""

    @pytest.fixture
    def sample_windows(self):
        """Sample window configurations for testing."""
        return [
            Window(num_samples=256, overlap=128, type="hamming"),
            Window(num_samples=512, overlap=256, type="hann"),
            Window(num_samples=1024, overlap=512, type="blackman"),
        ]

    def test_default_window(self):
        """Test default window configuration."""
        coh = Coherence()
        assert isinstance(coh.window, Window)
        assert coh.window.num_samples == 256
        assert coh.window.overlap == 128
        assert coh.window.type == "hamming"

    def test_custom_window(self, sample_windows):
        """Test custom window configurations."""
        for window in sample_windows:
            coh = Coherence(window=window)
            assert coh.window.num_samples == window.num_samples
            assert coh.window.overlap == window.overlap
            assert coh.window.type == window.type

    def test_window_from_dict(self):
        """Test window creation from dictionary."""
        window_dict = {"num_samples": 1024, "overlap": 512, "type": "blackman"}
        window = Window(**window_dict)
        coh = Coherence(window=window)
        assert coh.window.num_samples == 1024
        assert coh.window.overlap == 512
        assert coh.window.type == "blackman"


class TestCoherenceComputedFields:
    """Test computed fields and properties."""

    def test_channel_pair_str(self):
        """Test channel_pair_str computed field."""
        coh = Coherence(channel_1="ex", channel_2="hy")
        assert coh.channel_pair_str == "ex, hy"

        coh = Coherence(channel_1="hx", channel_2="ey")
        assert coh.channel_pair_str == "hx, ey"

        # Empty channels
        coh = Coherence()
        assert coh.channel_pair_str == ", "


class TestCoherenceModelValidator:
    """Test the model validator behavior."""

    def test_validator_sets_defaults(self):
        """Test that model validator properly sets default values."""
        coh = Coherence()

        # Check that validator set the correct defaults
        assert coh.name == "coherence"
        assert coh.domain.value == "frequency"
        assert "Simple coherence" in coh.description
        assert "scipy.signal.coherence" in coh.description

    def test_validator_with_custom_values(self):
        """Test that custom values can override validator defaults."""
        # Custom name should be overridden by validator
        coh = Coherence(name="custom_name")
        assert coh.name == "coherence"  # Validator overrides

        # Custom domain should be overridden
        coh = Coherence(domain="time")
        assert coh.domain.value == "frequency"  # Validator overrides


class TestCoherenceStationValidation:
    """Test station ID validation logic."""

    @pytest.fixture
    def coherence_with_channels(self):
        """Coherence instance with channel setup for testing."""
        return Coherence(channel_1="ex", channel_2="hy")

    def test_validate_station_ids_local_only(self, coherence_with_channels):
        """Test station validation with local station only."""
        coh = coherence_with_channels
        coh.validate_station_ids("LOCAL_STN")

        # Both channels should be assigned to local station
        assert coh.station_1 == "LOCAL_STN"
        assert coh.station_2 == "LOCAL_STN"

    def test_validate_station_ids_with_remote(self, coherence_with_channels):
        """Test station validation with local and remote stations."""
        coh = coherence_with_channels
        coh.validate_station_ids("LOCAL_STN", "REMOTE_STN")

        # Non-remote channels should be assigned to local
        assert coh.station_1 == "LOCAL_STN"  # ex -> local
        assert coh.station_2 == "LOCAL_STN"  # hy -> local

    def test_validate_station_ids_with_remote_channels(self):
        """Test station validation with remote channels."""
        coh = Coherence(channel_1="rx", channel_2="ry")
        coh.validate_station_ids("LOCAL_STN", "REMOTE_STN")

        # Remote channels should be assigned to remote station
        assert coh.station_1 == "REMOTE_STN"  # rx -> remote
        assert coh.station_2 == "REMOTE_STN"  # ry -> remote

    def test_validate_station_ids_mixed_channels(self):
        """Test station validation with mixed local/remote channels."""
        coh = Coherence(channel_1="ex", channel_2="ry")
        coh.validate_station_ids("LOCAL_STN", "REMOTE_STN")

        assert coh.station_1 == "LOCAL_STN"  # ex -> local
        assert coh.station_2 == "REMOTE_STN"  # ry -> remote

    def test_validate_station_ids_preset_stations(self):
        """Test validation with pre-set station IDs."""
        coh = Coherence(
            channel_1="ex", channel_2="hy", station_1="PRESET_1", station_2="PRESET_2"
        )
        coh.validate_station_ids("PRESET_1", "PRESET_2")

        # Pre-set valid stations should be preserved
        assert coh.station_1 == "PRESET_1"
        assert coh.station_2 == "PRESET_2"

    def test_validate_station_ids_invalid_preset(self):
        """Test validation with invalid pre-set station IDs."""
        coh = Coherence(
            channel_1="ex",
            channel_2="hy",
            station_1="INVALID_STN",
            station_2="ANOTHER_INVALID",
        )

        with patch("mt_metadata.features.coherence.logger") as mock_logger:
            coh.validate_station_ids("LOCAL_STN")

            # Should log warnings and reset to None, then assign
            assert mock_logger.warning.call_count >= 2
            assert coh.station_1 == "LOCAL_STN"  # Reset and assigned
            assert coh.station_2 == "LOCAL_STN"  # Reset and assigned

    def test_validate_station_ids_method_exists(self):
        """Test that validate_station_ids method exists and is callable."""
        coh = Coherence()
        assert hasattr(coh, "validate_station_ids")
        assert callable(coh.validate_station_ids)

        # Test the method signature accepts the expected parameters
        import inspect

        sig = inspect.signature(coh.validate_station_ids)
        params = list(sig.parameters.keys())
        assert "local_station_id" in params
        assert "remote_station_id" in params


class TestCoherenceComputation:
    """Test the compute method using scipy.signal.coherence."""

    @pytest.fixture
    def sample_time_series(self):
        """Generate sample time series data for testing."""
        np.random.seed(42)  # For reproducible tests
        fs = 1000  # Sampling frequency
        t = np.linspace(0, 1, fs)

        # Create correlated signals
        signal1 = np.sin(2 * np.pi * 50 * t) + 0.1 * np.random.randn(len(t))
        signal2 = (
            0.8 * signal1
            + 0.2 * np.sin(2 * np.pi * 120 * t)
            + 0.1 * np.random.randn(len(t))
        )

        return signal1, signal2

    @patch("mt_metadata.features.coherence.ssig.coherence")
    def test_compute_calls_scipy(self, mock_coherence, sample_time_series):
        """Test that compute method properly calls scipy.signal.coherence."""
        ts1, ts2 = sample_time_series
        mock_coherence.return_value = (np.array([1, 2, 3]), np.array([0.5, 0.7, 0.9]))

        coh = Coherence()
        freqs, coherence = coh.compute(ts1, ts2)

        # Verify scipy.coherence was called with correct parameters
        mock_coherence.assert_called_once_with(
            ts1,
            ts2,
            window=coh.window.type,
            nperseg=coh.window.num_samples,
            noverlap=coh.window.overlap,
            detrend=coh.detrend,
        )

        # Verify return values
        np.testing.assert_array_equal(freqs, [1, 2, 3])
        np.testing.assert_array_equal(coherence, [0.5, 0.7, 0.9])

    def test_compute_with_real_data(self, sample_time_series):
        """Test compute method with real scipy computation."""
        ts1, ts2 = sample_time_series
        coh = Coherence()

        freqs, coherence_vals = coh.compute(ts1, ts2)

        # Basic validation of outputs
        assert isinstance(freqs, np.ndarray)
        assert isinstance(coherence_vals, np.ndarray)
        assert len(freqs) == len(coherence_vals)
        assert all(0 <= c <= 1 for c in coherence_vals)  # Coherence should be [0,1]
        assert all(f >= 0 for f in freqs)  # Frequencies should be positive

    @pytest.mark.parametrize(
        "window_config",
        [
            {"num_samples": 128, "overlap": 64, "type": "hamming"},
            {"num_samples": 256, "overlap": 128, "type": "hann"},
            {"num_samples": 512, "overlap": 256, "type": "blackman"},
        ],
    )
    def test_compute_different_windows(self, sample_time_series, window_config):
        """Test compute method with different window configurations."""
        ts1, ts2 = sample_time_series

        window = Window(**window_config)
        coh = Coherence(window=window)

        freqs, coherence_vals = coh.compute(ts1, ts2)

        # Should successfully compute with different window settings
        assert isinstance(freqs, np.ndarray)
        assert isinstance(coherence_vals, np.ndarray)
        assert len(freqs) > 0
        assert len(coherence_vals) > 0

    @pytest.mark.parametrize("detrend_type", ["linear", "constant"])
    def test_compute_different_detrend(self, sample_time_series, detrend_type):
        """Test compute method with different detrend options."""
        ts1, ts2 = sample_time_series

        coh = Coherence(detrend=detrend_type)
        freqs, coherence_vals = coh.compute(ts1, ts2)

        # Should successfully compute with different detrend settings
        assert isinstance(freqs, np.ndarray)
        assert isinstance(coherence_vals, np.ndarray)
        assert all(0 <= c <= 1 for c in coherence_vals)


class TestCoherenceDetrendEnum:
    """Test DetrendEnum enumeration."""

    def test_detrend_enum_values(self):
        """Test DetrendEnum has correct values."""
        assert DetrendEnum.linear == "linear"
        assert DetrendEnum.constant == "constant"

        # Test all values are accessible
        all_values = list(DetrendEnum)
        assert len(all_values) == 2
        assert "linear" in [v.value for v in all_values]
        assert "constant" in [v.value for v in all_values]


class TestCoherenceEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_time_series(self):
        """Test compute with empty time series."""
        coh = Coherence()

        # Empty arrays should not crash but may produce empty output
        ts1 = np.array([])
        ts2 = np.array([])

        try:
            freqs, coherence_vals = coh.compute(ts1, ts2)
            # If no exception, verify output structure
            assert isinstance(freqs, np.ndarray)
            assert isinstance(coherence_vals, np.ndarray)
        except Exception:
            # Some configurations may raise exceptions with empty data
            pass

    def test_mismatched_time_series_length(self):
        """Test compute with mismatched time series lengths."""
        coh = Coherence()

        ts1 = np.random.randn(1000)
        ts2 = np.random.randn(500)  # Different length

        try:
            freqs, coherence_vals = coh.compute(ts1, ts2)
            # scipy may handle this or raise an exception
            assert isinstance(freqs, np.ndarray)
            assert isinstance(coherence_vals, np.ndarray)
        except Exception:
            # Expected if scipy doesn't handle length mismatch
            pass

    def test_single_sample_time_series(self):
        """Test compute with very short time series."""
        coh = Coherence(window=Window(num_samples=2, overlap=0, type="boxcar"))

        ts1 = np.array([1.0, 2.0, 3.0])
        ts2 = np.array([2.0, 3.0, 4.0])

        try:
            freqs, coherence_vals = coh.compute(ts1, ts2)
            assert isinstance(freqs, np.ndarray)
            assert isinstance(coherence_vals, np.ndarray)
        except Exception:
            # Very short time series may not be suitable for coherence
            pass

    def test_identical_time_series(self):
        """Test compute with identical time series (perfect coherence)."""
        coh = Coherence()

        ts = np.random.randn(1000)
        freqs, coherence_vals = coh.compute(ts, ts)

        # Identical signals should have high coherence
        assert isinstance(freqs, np.ndarray)
        assert isinstance(coherence_vals, np.ndarray)
        # Most frequencies should have high coherence (close to 1)
        assert np.mean(coherence_vals) > 0.8


class TestCoherenceIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow(self):
        """Test complete workflow from instantiation to computation."""
        # Create coherence with custom configuration
        window = Window(num_samples=512, overlap=256, type="hann")
        coh = Coherence(
            channel_1="ex",
            channel_2="hy",
            detrend="linear",
            station_1="TEST_STN",
            station_2="TEST_STN",
            window=window,
        )

        # Validate station IDs
        coh.validate_station_ids("TEST_STN")

        # Generate test data
        np.random.seed(123)
        fs = 1000
        t = np.linspace(0, 2, 2 * fs)
        ts1 = np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn(len(t))
        ts2 = np.sin(2 * np.pi * 10 * t + np.pi / 4) + 0.1 * np.random.randn(len(t))

        # Compute coherence
        freqs, coherence_vals = coh.compute(ts1, ts2)

        # Validate results
        assert isinstance(freqs, np.ndarray)
        assert isinstance(coherence_vals, np.ndarray)
        assert len(freqs) == len(coherence_vals)
        assert all(0 <= c <= 1 for c in coherence_vals)
        assert coh.channel_pair_str == "ex, hy"
        assert coh.station_1 == "TEST_STN"
        assert coh.station_2 == "TEST_STN"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
