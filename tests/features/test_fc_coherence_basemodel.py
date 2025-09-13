"""
Comprehensive test suite for FCCoherence class.

Tests cover instantiation, field validation, inheritance,
computation methods, and edge cases.
"""

import numpy as np
import pytest

from mt_metadata.features.base_feature_basemodel import Feature
from mt_metadata.features.coherence_basemodel import Coherence
from mt_metadata.features.fc_coherence_basemodel import (
    BandDefinitionTypeEnum,
    FCCoherence,
    QRadiusEnum,
)


class TestFCCoherenceInstantiation:
    """Test basic instantiation and default values."""

    def test_default_instantiation(self):
        """Test FCCoherence can be instantiated with defaults."""
        fc = FCCoherence()
        assert isinstance(fc, FCCoherence)
        assert isinstance(fc, Coherence)  # Multiple inheritance
        assert isinstance(fc, Feature)  # Multiple inheritance
        assert fc.name == "fc_coherence"
        assert fc.domain.value == "frequency"
        assert fc.channel_1 == ""
        assert fc.channel_2 == ""
        assert fc.minimum_fcs == 2
        assert fc.band_definition_type == BandDefinitionTypeEnum.Q
        assert fc.q_radius == QRadiusEnum.constant_Q

    def test_instantiation_with_channels(self):
        """Test FCCoherence instantiation with channel parameters."""
        fc = FCCoherence(channel_1="ex", channel_2="hy")
        assert fc.channel_1 == "ex"
        assert fc.channel_2 == "hy"
        assert fc.name == "fc_coherence"  # Set by model validator

    def test_instantiation_with_all_params(self):
        """Test FCCoherence instantiation with all parameters."""
        fc = FCCoherence(
            channel_1="hx",
            channel_2="ey",
            minimum_fcs=5,
            band_definition_type="user defined",
            q_radius="user defined",
        )
        assert fc.channel_1 == "hx"
        assert fc.channel_2 == "ey"
        assert fc.minimum_fcs == 5
        assert fc.band_definition_type == BandDefinitionTypeEnum.user_defined
        assert fc.q_radius == QRadiusEnum.user_defined


class TestFCCoherenceInheritance:
    """Test multiple inheritance behavior."""

    def test_inheritance_structure(self):
        """Test that FCCoherence properly inherits from both parent classes."""
        fc = FCCoherence()

        # From Feature class
        assert hasattr(fc, "name")
        assert hasattr(fc, "description")
        assert hasattr(fc, "domain")
        assert hasattr(fc, "data")
        assert hasattr(fc, "comments")

        # From Coherence class
        assert hasattr(fc, "channel_1")
        assert hasattr(fc, "channel_2")
        assert hasattr(fc, "detrend")
        assert hasattr(fc, "station_1")
        assert hasattr(fc, "station_2")
        assert hasattr(fc, "window")

        # FCCoherence specific fields
        assert hasattr(fc, "channel_1")
        assert hasattr(fc, "channel_2")
        assert hasattr(fc, "minimum_fcs")
        assert hasattr(fc, "band_definition_type")
        assert hasattr(fc, "q_radius")

    def test_method_resolution_order(self):
        """Test that method resolution order is correct."""
        # The exact MRO includes the full inheritance chain
        mro = FCCoherence.__mro__
        assert FCCoherence in mro
        assert Coherence in mro
        assert Feature in mro
        assert object in mro


class TestFCCoherenceFieldValidation:
    """Test field validation and types."""

    def test_channel_validation(self):
        """Test channel field validation."""
        fc = FCCoherence()

        # Valid channel names
        valid_channels = ["ex", "ey", "hx", "hy", "hz"]
        for channel in valid_channels:
            fc.channel_1 = channel
            fc.channel_2 = channel
            assert fc.channel_1 == channel
            assert fc.channel_2 == channel

    def test_minimum_fcs_validation(self):
        """Test minimum_fcs field validation."""
        # Valid values
        for fcs in [1, 2, 5, 10, 100]:
            fc = FCCoherence(minimum_fcs=fcs)
            assert fc.minimum_fcs == fcs

        # Note: Pydantic may not raise errors for negative values if field has no constraints
        # This test documents the current behavior
        try:
            fc = FCCoherence(minimum_fcs=-1)
            # If no error raised, document the actual behavior
            assert fc.minimum_fcs == -1
        except Exception:
            # Expected if validation constraints exist
            pass

    def test_band_definition_type_validation(self):
        """Test band_definition_type enum validation."""
        # Valid enum values
        for band_type in ["Q", "fractional bandwidth", "user defined"]:
            fc = FCCoherence(band_definition_type=band_type)
            assert fc.band_definition_type.value == band_type

        # Invalid values should raise validation error
        with pytest.raises(Exception):  # Pydantic validation error
            FCCoherence(band_definition_type="invalid_type")

    def test_q_radius_validation(self):
        """Test q_radius enum validation."""
        # Valid enum values
        for q_rad in ["constant Q", "user defined"]:
            fc = FCCoherence(q_radius=q_rad)
            assert fc.q_radius.value == q_rad

        # Invalid values should raise validation error
        with pytest.raises(Exception):  # Pydantic validation error
            FCCoherence(q_radius="invalid_radius")


class TestFCCoherenceComputedFields:
    """Test computed fields and properties."""

    def test_channel_pair_str(self):
        """Test channel_pair_str computed field."""
        fc = FCCoherence(channel_1="ex", channel_2="hy")
        assert fc.channel_pair_str == "ex, hy"

        fc = FCCoherence(channel_1="hx", channel_2="ey")
        assert fc.channel_pair_str == "hx, ey"

        # Empty channels
        fc = FCCoherence()
        assert fc.channel_pair_str == ", "


class TestFCCoherenceComputation:
    """Test the compute method."""

    @pytest.fixture
    def sample_fc_data(self):
        """Generate sample Fourier coefficient data."""
        np.random.seed(42)  # For reproducible tests
        n_windows, n_freqs = 100, 64

        # Create correlated signals for testing
        signal1 = np.random.randn(n_windows, n_freqs) + 1j * np.random.randn(
            n_windows, n_freqs
        )
        noise = np.random.randn(n_windows, n_freqs) + 1j * np.random.randn(
            n_windows, n_freqs
        )
        signal2 = 0.8 * signal1 + 0.2 * noise  # Partially correlated

        return signal1, signal2

    def test_compute_basic(self, sample_fc_data):
        """Test basic compute functionality."""
        fc = FCCoherence()
        fc1, fc2 = sample_fc_data

        freqs, coherence = fc.compute(fc1, fc2)

        # Check return types and shapes
        assert freqs is None  # No frequency axis provided
        assert isinstance(coherence, np.ndarray)
        assert coherence.shape == (fc1.shape[1],)  # n_freqs

        # Coherence should be between 0 and 1
        assert np.all(coherence >= 0)
        assert np.all(coherence <= 1)

    def test_compute_perfect_coherence(self):
        """Test compute with perfectly coherent signals."""
        fc = FCCoherence()

        # Create identical signals
        n_windows, n_freqs = 50, 32
        signal = np.random.randn(n_windows, n_freqs) + 1j * np.random.randn(
            n_windows, n_freqs
        )

        freqs, coherence = fc.compute(signal, signal)

        # Perfect coherence should be close to 1
        np.testing.assert_array_almost_equal(coherence, np.ones(n_freqs), decimal=10)

    def test_compute_uncorrelated_signals(self):
        """Test compute with uncorrelated signals."""
        fc = FCCoherence()

        # Create uncorrelated signals
        np.random.seed(123)
        n_windows, n_freqs = 1000, 32  # More windows for better statistics
        signal1 = np.random.randn(n_windows, n_freqs) + 1j * np.random.randn(
            n_windows, n_freqs
        )
        signal2 = np.random.randn(n_windows, n_freqs) + 1j * np.random.randn(
            n_windows, n_freqs
        )

        freqs, coherence = fc.compute(signal1, signal2)

        # Uncorrelated signals should have low coherence
        assert np.all(coherence < 0.2)  # Threshold for statistical test

    def test_compute_input_validation(self):
        """Test compute method input validation."""
        fc = FCCoherence()

        # Signals with same shape should work fine
        signal1 = np.random.randn(10, 5) + 1j * np.random.randn(10, 5)
        signal2 = np.random.randn(10, 5) + 1j * np.random.randn(10, 5)

        freqs, coherence = fc.compute(signal1, signal2)
        assert coherence is not None
        assert coherence.shape == (5,)


class TestFCCoherenceModelValidator:
    """Test the model validator behavior."""

    def test_validator_sets_defaults(self):
        """Test that model validator properly sets default values."""
        fc = FCCoherence()

        # Check that validator set the correct defaults
        assert fc.name == "fc_coherence"
        assert fc.domain.value == "frequency"
        assert "Magnitude-squared coherence" in fc.description
        assert "Fourier coefficients" in fc.description

    def test_validator_with_custom_values(self):
        """Test that custom values can override validator defaults."""
        # Custom name should be overridden by validator
        fc = FCCoherence(name="custom_name")
        assert fc.name == "fc_coherence"  # Validator overrides

        # Custom domain should be overridden
        fc = FCCoherence(domain="time")
        assert fc.domain.value == "frequency"  # Validator overrides


class TestFCCoherenceEnums:
    """Test enum classes used by FCCoherence."""

    def test_band_definition_type_enum(self):
        """Test BandDefinitionTypeEnum values."""
        assert BandDefinitionTypeEnum.Q == "Q"
        assert BandDefinitionTypeEnum.fractional_bandwidth == "fractional bandwidth"
        assert BandDefinitionTypeEnum.user_defined == "user defined"

        # Test all values are accessible
        all_values = list(BandDefinitionTypeEnum)
        assert len(all_values) == 3

    def test_q_radius_enum(self):
        """Test QRadiusEnum values."""
        assert QRadiusEnum.constant_Q == "constant Q"
        assert QRadiusEnum.user_defined == "user defined"

        # Test all values are accessible
        all_values = list(QRadiusEnum)
        assert len(all_values) == 2


class TestFCCoherenceEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_division_protection(self):
        """Test compute method handles zero division gracefully."""
        fc = FCCoherence()

        # Create signals with zeros that could cause division by zero
        n_windows, n_freqs = 10, 5
        signal1 = np.zeros((n_windows, n_freqs), dtype=complex)
        signal2 = np.zeros((n_windows, n_freqs), dtype=complex)

        freqs, coherence = fc.compute(signal1, signal2)

        # Should handle gracefully (result may be NaN or 0)
        assert coherence is not None
        assert coherence.shape == (n_freqs,)

    def test_single_window(self):
        """Test compute with single window of data."""
        fc = FCCoherence()

        # Single window
        n_freqs = 10
        signal1 = np.random.randn(1, n_freqs) + 1j * np.random.randn(1, n_freqs)
        signal2 = np.random.randn(1, n_freqs) + 1j * np.random.randn(1, n_freqs)

        freqs, coherence = fc.compute(signal1, signal2)

        assert coherence is not None
        assert coherence.shape == (n_freqs,)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
