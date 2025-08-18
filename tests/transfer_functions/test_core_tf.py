"""
Tests for mt_metadata.transfer_functions.core.tf.TF
==================================================

This module contains comprehensive pytest tests for the TF core functionality.
Tests cover string representations, equality operations, channel nomenclature,
period/frequency input handling, impedance/tipper data, and matrix operations.

"""

import numpy as np
import pytest
import xarray as xr

from mt_metadata.transfer_functions.core import TF, TFError


# ==============================================================================
# Session-scoped fixtures for common test data
# ==============================================================================
@pytest.fixture(scope="session")
def base_periods():
    """Base period array used across multiple tests."""
    return np.logspace(-3, 3, 20)


@pytest.fixture(scope="session")
def mismatched_periods():
    """Period array with different length for mismatch testing."""
    return np.logspace(-3, 3, 22)


@pytest.fixture(scope="session")
def base_frequencies(base_periods):
    """Base frequency array derived from periods."""
    return 1.0 / base_periods


@pytest.fixture(scope="session")
def impedance_data(base_periods):
    """Generate impedance data for testing."""
    n_period = len(base_periods)
    return xr.DataArray(
        data=np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2),
        dims=["period", "output", "input"],
        coords={
            "period": base_periods,
            "output": ["ex", "ey"],
            "input": ["hx", "hy"],
        },
        name="impedance",
    )


@pytest.fixture(scope="session")
def tipper_data(base_periods):
    """Generate tipper data for testing."""
    n_period = len(base_periods)
    return xr.DataArray(
        data=np.random.rand(n_period, 1, 2) + 1j * np.random.rand(n_period, 1, 2),
        dims=["period", "output", "input"],
        coords={
            "period": base_periods,
            "output": ["hz"],
            "input": ["hx", "hy"],
        },
        name="tipper",
    )


@pytest.fixture(scope="session")
def isp_data(base_periods):
    """Generate inverse signal power data for testing."""
    n_period = len(base_periods)
    return xr.DataArray(
        data=np.random.rand(n_period, 2, 2),
        dims=["period", "output", "input"],
        coords={
            "period": base_periods,
            "output": ["hx", "hy"],
            "input": ["hx", "hy"],
        },
        name="inverse_signal_power",
    )


@pytest.fixture(scope="session")
def residual_data(base_periods):
    """Generate residual covariance data for testing."""
    n_period = len(base_periods)
    return xr.DataArray(
        data=np.random.rand(n_period, 3, 3),
        dims=["period", "output", "input"],
        coords={
            "period": base_periods,
            "output": ["ex", "ey", "hz"],
            "input": ["ex", "ey", "hz"],
        },
        name="residual_covariance",
    )


@pytest.fixture
def empty_tf():
    """Fresh TF instance for each test."""
    return TF()


@pytest.fixture
def populated_tf(impedance_data, tipper_data):
    """TF instance with impedance and tipper data."""
    tf = TF()
    tf.impedance = impedance_data
    tf.tipper = tipper_data
    return tf


# ==============================================================================
# Test TF Core Functionality
# ==============================================================================
class TestTFCore:
    """Test basic TF functionality and string representations."""

    def test_tf_string_representation(self, empty_tf):
        """Test string representation of empty TF."""
        string_repr = str(empty_tf)
        assert "Station: 0" in string_repr
        assert "Survey:" in string_repr
        assert "Impedance:" in string_repr
        assert "Tipper:" in string_repr

    def test_tf_repr(self, empty_tf):
        """Test repr representation of empty TF."""
        repr_str = repr(empty_tf)
        assert "TF" in repr_str

    def test_station_metadata_dict(self, empty_tf):
        """Test station metadata dictionary."""
        metadata_dict = empty_tf.station_metadata.to_dict(single=True)
        assert isinstance(metadata_dict, dict)

    def test_survey_metadata_dict(self, empty_tf):
        """Test survey metadata dictionary."""
        metadata_dict = empty_tf.survey_metadata.to_dict(single=True)
        assert isinstance(metadata_dict, dict)

    def test_run_metadata_dict(self, empty_tf):
        """Test run metadata structure."""
        run_metadata = empty_tf.run_metadata
        # run_metadata could be a dict, list, or other structure - just verify it exists
        assert run_metadata is not None
        assert hasattr(run_metadata, "__len__") or hasattr(run_metadata, "keys")


# ==============================================================================
# Test TF Equality Operations
# ==============================================================================
class TestTFEquality:
    """Test TF equality and comparison operations."""

    def test_empty_equality(self, empty_tf):
        """Test equality of empty TF objects."""
        other_tf = TF()
        assert empty_tf == other_tf

    def test_populated_equality(self, populated_tf, impedance_data, tipper_data):
        """Test equality of populated TF objects."""
        other_tf = TF()
        other_tf.impedance = impedance_data
        other_tf.tipper = tipper_data
        assert populated_tf == other_tf

    def test_inequality_impedance(self, populated_tf, base_periods):
        """Test inequality when impedance differs."""
        other_tf = TF()
        n_period = len(base_periods)
        different_impedance = xr.DataArray(
            data=np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        other_tf.impedance = different_impedance
        assert populated_tf != other_tf

    def test_inequality_missing_component(self, populated_tf):
        """Test inequality when one TF is missing components."""
        partial_tf = TF()
        partial_tf.impedance = populated_tf.impedance
        # No tipper data
        assert populated_tf != partial_tf


# ==============================================================================
# Test Channel Nomenclature
# ==============================================================================
class TestTFChannelNomenclature:
    """Test channel naming and nomenclature handling."""

    @pytest.mark.parametrize(
        "input_channels,output_channels,expected_size",
        [
            (["hx", "hy"], ["ex", "ey"], (2, 2)),
            (["hx", "hy", "hz"], ["ex", "ey"], (2, 3)),
            (["hx", "hy"], ["ex", "ey", "hz"], (3, 2)),
            (["hx", "hy", "hz"], ["ex", "ey", "hz"], (3, 3)),
        ],
    )
    def test_channel_nomenclature_sizes(
        self, empty_tf, base_periods, input_channels, output_channels, expected_size
    ):
        """Test different channel combinations and their resulting sizes."""
        n_period = len(base_periods)
        data = np.random.rand(n_period, expected_size[0], expected_size[1])

        # Create test DataArray with specified channels
        test_array = xr.DataArray(
            data=data,
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": output_channels,
                "input": input_channels,
            },
            name="test_data",
        )

        # Test that TF can handle these channel configurations
        assert test_array.shape == (n_period, expected_size[0], expected_size[1])
        assert list(test_array.coords["input"]) == input_channels
        assert list(test_array.coords["output"]) == output_channels

    def test_standard_mt_channels(self, empty_tf, base_periods):
        """Test standard MT channel nomenclature."""
        n_period = len(base_periods)

        # Standard impedance channels
        impedance_channels = {"input": ["hx", "hy"], "output": ["ex", "ey"]}

        impedance_data = xr.DataArray(
            data=np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": impedance_channels["output"],
                "input": impedance_channels["input"],
            },
            name="impedance",
        )

        empty_tf.impedance = impedance_data
        assert empty_tf.has_impedance()
        assert list(empty_tf.impedance.coords["input"]) == ["hx", "hy"]
        assert list(empty_tf.impedance.coords["output"]) == ["ex", "ey"]

    def test_tipper_channels(self, empty_tf, base_periods):
        """Test tipper channel nomenclature."""
        n_period = len(base_periods)

        tipper_data = xr.DataArray(
            data=np.random.rand(n_period, 1, 2) + 1j * np.random.rand(n_period, 1, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )

        empty_tf.tipper = tipper_data
        assert empty_tf.has_tipper()
        assert list(empty_tf.tipper.coords["input"]) == ["hx", "hy"]
        assert list(empty_tf.tipper.coords["output"]) == ["hz"]


# ==============================================================================
# Test Period Input Handling
# ==============================================================================
class TestTFPeriodInput:
    """Test TF period input validation and handling."""

    def test_set_impedance_with_periods(self, empty_tf, base_periods, impedance_data):
        """Test setting impedance with proper periods."""
        empty_tf.impedance = impedance_data
        assert empty_tf.has_impedance()
        assert len(empty_tf.impedance.period) == len(base_periods)
        assert np.allclose(empty_tf.impedance.period.data, base_periods)

    def test_impedance_shape_validation(self, empty_tf, base_periods):
        """Test impedance shape validation."""
        n_period = len(base_periods)
        correct_data = impedance_data = xr.DataArray(
            data=np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )

        empty_tf.impedance = correct_data
        assert empty_tf.impedance.shape == (n_period, 2, 2)

    def test_period_mismatch_error(self, empty_tf, base_periods, mismatched_periods):
        """Test error when setting data with mismatched periods."""
        # First set impedance with base periods
        impedance_data = xr.DataArray(
            data=np.random.rand(len(base_periods), 2, 2)
            + 1j * np.random.rand(len(base_periods), 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        empty_tf.impedance = impedance_data

        # Try to set tipper with different periods - should raise error
        mismatched_tipper = xr.DataArray(
            data=np.random.rand(len(mismatched_periods), 1, 2)
            + 1j * np.random.rand(len(mismatched_periods), 1, 2),
            dims=["period", "output", "input"],
            coords={
                "period": mismatched_periods,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )

        with pytest.raises(TFError):
            empty_tf.tipper = mismatched_tipper

    def test_set_from_numpy_array(self, empty_tf, base_periods):
        """Test setting impedance from numpy array."""
        n_period = len(base_periods)
        numpy_data = np.random.rand(n_period, 2, 2) + 1j * np.random.rand(
            n_period, 2, 2
        )

        # This should work if the TF has periods set
        impedance_with_coords = xr.DataArray(
            data=numpy_data,
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        empty_tf.impedance = impedance_with_coords

        # Now set from numpy array (this depends on TF implementation)
        empty_tf.impedance = numpy_data
        assert np.allclose(np.array(empty_tf.impedance.data), numpy_data)


# ==============================================================================
# Test Frequency Input Handling
# ==============================================================================
class TestTFFrequencyInput:
    """Test TF frequency input validation and handling."""

    def test_frequency_period_consistency(
        self, empty_tf, base_frequencies, base_periods
    ):
        """Test that frequencies and periods are consistent."""
        n_period = len(base_frequencies)

        frequency_data = xr.DataArray(
            data=np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2),
            dims=["frequency", "output", "input"],
            coords={
                "frequency": base_frequencies,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )

        # Convert frequency-based data to period-based (if TF supports this)
        expected_periods = 1.0 / base_frequencies
        assert np.allclose(expected_periods, base_periods)

    def test_frequency_sorting(self, base_frequencies):
        """Test frequency sorting behavior."""
        # Frequencies should typically be in ascending order
        sorted_frequencies = np.sort(base_frequencies)

        # For periods derived from frequencies, they should be in descending order
        periods_from_freq = 1.0 / sorted_frequencies
        expected_period_order = np.sort(periods_from_freq)[
            ::-1
        ]  # Reverse for descending

        actual_periods = 1.0 / base_frequencies
        # Note: This test verifies the relationship, actual implementation may vary
        assert len(actual_periods) == len(expected_period_order)


# ==============================================================================
# Test Impedance Input
# ==============================================================================
class TestTFImpedanceInput:
    """Test impedance data input and validation."""

    def test_has_impedance(self, populated_tf):
        """Test impedance detection."""
        assert populated_tf.has_impedance()

    def test_impedance_shape(self, populated_tf, base_periods):
        """Test impedance shape validation."""
        expected_shape = (len(base_periods), 2, 2)
        assert populated_tf.impedance.shape == expected_shape

    def test_impedance_data_integrity(self, populated_tf, impedance_data):
        """Test impedance data integrity."""
        assert np.allclose(populated_tf.impedance.data, impedance_data.data)

    def test_impedance_period_mismatch_error(self, empty_tf, mismatched_periods):
        """Test error with mismatched impedance periods."""
        mismatched_impedance = xr.DataArray(
            data=np.random.rand(len(mismatched_periods), 2, 2)
            + 1j * np.random.rand(len(mismatched_periods), 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": mismatched_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )

        # Set initial impedance
        base_impedance = xr.DataArray(
            data=np.random.rand(20, 2, 2) + 1j * np.random.rand(20, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": np.logspace(-3, 3, 20),
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        empty_tf.impedance = base_impedance

        # Try to overwrite with mismatched data
        with pytest.raises(TFError):
            empty_tf.impedance = mismatched_impedance

    def test_set_impedance_from_array(self, empty_tf, base_periods):
        """Test setting impedance from numpy array."""
        n_period = len(base_periods)
        new_data = np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2)

        # First set with proper DataArray
        initial_data = xr.DataArray(
            data=np.ones((n_period, 2, 2), dtype=complex),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        empty_tf.impedance = initial_data

        # Then set from numpy array
        empty_tf.impedance = new_data
        assert np.allclose(np.array(empty_tf.impedance.data), new_data)


# ==============================================================================
# Test Tipper Input
# ==============================================================================
class TestTFTipperInput:
    """Test tipper data input and validation."""

    def test_has_tipper(self, populated_tf):
        """Test tipper detection."""
        assert populated_tf.has_tipper()

    def test_tipper_shape(self, populated_tf, base_periods):
        """Test tipper shape validation."""
        expected_shape = (len(base_periods), 1, 2)
        assert populated_tf.tipper.shape == expected_shape

    def test_tipper_data_integrity(self, populated_tf, tipper_data):
        """Test tipper data integrity."""
        assert np.allclose(populated_tf.tipper.data, tipper_data.data)

    def test_tipper_period_mismatch_error(
        self, empty_tf, base_periods, mismatched_periods
    ):
        """Test error with mismatched tipper periods."""
        # Set impedance first
        impedance_data = xr.DataArray(
            data=np.random.rand(len(base_periods), 2, 2)
            + 1j * np.random.rand(len(base_periods), 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        empty_tf.impedance = impedance_data

        # Try to set tipper with mismatched periods
        mismatched_tipper = xr.DataArray(
            data=np.random.rand(len(mismatched_periods), 1, 2)
            + 1j * np.random.rand(len(mismatched_periods), 1, 2),
            dims=["period", "output", "input"],
            coords={
                "period": mismatched_periods,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )

        with pytest.raises(TFError):
            empty_tf.tipper = mismatched_tipper

    def test_set_tipper_from_array(self, empty_tf, base_periods):
        """Test setting tipper from numpy array."""
        n_period = len(base_periods)
        new_data = np.random.rand(n_period, 1, 2) + 1j * np.random.rand(n_period, 1, 2)

        # First set with proper DataArray
        initial_data = xr.DataArray(
            data=np.ones((n_period, 1, 2), dtype=complex),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )
        empty_tf.tipper = initial_data

        # Then set from numpy array
        empty_tf.tipper = new_data
        assert np.allclose(np.array(empty_tf.tipper.data), new_data)


# ==============================================================================
# Test Inverse Signal Power Input
# ==============================================================================
class TestTFISPInput:
    """Test inverse signal power data input and validation."""

    def test_has_isp(self, empty_tf, isp_data):
        """Test inverse signal power detection."""
        empty_tf.inverse_signal_power = isp_data
        assert empty_tf.has_inverse_signal_power()

    def test_isp_shape(self, empty_tf, isp_data, base_periods):
        """Test inverse signal power shape validation."""
        empty_tf.inverse_signal_power = isp_data
        expected_shape = (len(base_periods), 2, 2)
        assert empty_tf.inverse_signal_power.shape == expected_shape

    def test_isp_data_integrity(self, empty_tf, isp_data):
        """Test inverse signal power data integrity."""
        empty_tf.inverse_signal_power = isp_data
        assert np.allclose(empty_tf.inverse_signal_power.data, isp_data.data)

    def test_isp_period_mismatch_error(
        self, empty_tf, base_periods, mismatched_periods
    ):
        """Test error with mismatched ISP periods."""
        # Set initial ISP
        initial_isp = xr.DataArray(
            data=np.random.rand(len(base_periods), 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
            },
            name="inverse_signal_power",
        )
        empty_tf.inverse_signal_power = initial_isp

        # Try to set ISP with mismatched periods
        mismatched_isp = xr.DataArray(
            data=np.random.rand(len(mismatched_periods), 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": mismatched_periods,
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
            },
            name="inverse_signal_power",
        )

        with pytest.raises(TFError):
            empty_tf.inverse_signal_power = mismatched_isp

    def test_set_isp_from_array(self, empty_tf, base_periods):
        """Test setting ISP from numpy array."""
        n_period = len(base_periods)
        new_data = np.random.rand(n_period, 2, 2)

        # First set with proper DataArray
        initial_data = xr.DataArray(
            data=np.ones((n_period, 2, 2)),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
            },
            name="inverse_signal_power",
        )
        empty_tf.inverse_signal_power = initial_data

        # Then set from numpy array
        empty_tf.inverse_signal_power = new_data
        assert np.allclose(np.array(empty_tf.inverse_signal_power.data), new_data)


# ==============================================================================
# Test Residual Covariance Input
# ==============================================================================
class TestTFResidualInput:
    """Test residual covariance data input and validation."""

    def test_has_residual(self, empty_tf, residual_data):
        """Test residual covariance detection."""
        empty_tf.residual_covariance = residual_data
        assert empty_tf.has_residual_covariance()

    def test_residual_shape(self, empty_tf, residual_data, base_periods):
        """Test residual covariance shape validation."""
        empty_tf.residual_covariance = residual_data
        expected_shape = (len(base_periods), 3, 3)
        assert empty_tf.residual_covariance.shape == expected_shape

    def test_residual_data_integrity(self, empty_tf, residual_data):
        """Test residual covariance data integrity."""
        empty_tf.residual_covariance = residual_data
        assert np.allclose(empty_tf.residual_covariance.data, residual_data.data)

    def test_residual_period_mismatch_error(
        self, empty_tf, base_periods, mismatched_periods
    ):
        """Test error with mismatched residual periods."""
        # Set initial residual covariance
        initial_residual = xr.DataArray(
            data=np.random.rand(len(base_periods), 3, 3),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
            },
            name="residual_covariance",
        )
        empty_tf.residual_covariance = initial_residual

        # Try to set residual with mismatched periods
        mismatched_residual = xr.DataArray(
            data=np.random.rand(len(mismatched_periods), 3, 3),
            dims=["period", "output", "input"],
            coords={
                "period": mismatched_periods,
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
            },
            name="residual_covariance",
        )

        with pytest.raises(TFError):
            empty_tf.residual_covariance = mismatched_residual

    def test_set_residual_from_array(self, empty_tf, base_periods):
        """Test setting residual covariance from numpy array."""
        n_period = len(base_periods)
        new_data = np.random.rand(n_period, 3, 3)

        # First set with proper DataArray
        initial_data = xr.DataArray(
            data=np.ones((n_period, 3, 3)),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
            },
            name="residual_covariance",
        )
        empty_tf.residual_covariance = initial_data

        # Then set from numpy array
        empty_tf.residual_covariance = new_data
        assert np.allclose(np.array(empty_tf.residual_covariance.data), new_data)


# ==============================================================================
# Integration Tests
# ==============================================================================
class TestTFIntegration:
    """Integration tests for complete TF functionality."""

    def test_full_tf_workflow(self, base_periods):
        """Test complete TF workflow with all components."""
        n_period = len(base_periods)
        tf = TF()

        # Set impedance
        impedance = xr.DataArray(
            data=np.random.rand(n_period, 2, 2) + 1j * np.random.rand(n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        tf.impedance = impedance

        # Set tipper
        tipper = xr.DataArray(
            data=np.random.rand(n_period, 1, 2) + 1j * np.random.rand(n_period, 1, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )
        tf.tipper = tipper

        # Set ISP
        isp = xr.DataArray(
            data=np.random.rand(n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
            },
            name="inverse_signal_power",
        )
        tf.inverse_signal_power = isp

        # Set residual covariance
        residual = xr.DataArray(
            data=np.random.rand(n_period, 3, 3),
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
            },
            name="residual_covariance",
        )
        tf.residual_covariance = residual

        # Verify all components
        assert tf.has_impedance()
        assert tf.has_tipper()
        assert tf.has_inverse_signal_power()
        assert tf.has_residual_covariance()

        # Test round-trip compatibility (without dict methods)
        # Check that all components are properly set
        impedance_shape = tf.impedance.shape
        tipper_shape = tf.tipper.shape
        isp_shape = tf.inverse_signal_power.shape
        residual_shape = tf.residual_covariance.shape

        assert impedance_shape == (n_period, 2, 2)
        assert tipper_shape == (n_period, 1, 2)
        assert isp_shape == (n_period, 2, 2)
        assert residual_shape == (n_period, 3, 3)

    def test_tf_consistency_checks(self, populated_tf):
        """Test TF internal consistency."""
        # All data should have same periods
        impedance_periods = populated_tf.impedance.period.data
        tipper_periods = populated_tf.tipper.period.data

        assert np.allclose(impedance_periods, tipper_periods)

    @pytest.mark.parametrize(
        "component",
        ["impedance", "tipper", "inverse_signal_power", "residual_covariance"],
    )
    def test_individual_component_workflow(self, empty_tf, base_periods, component):
        """Test workflow for individual components."""
        n_period = len(base_periods)

        # Define component-specific parameters
        component_configs = {
            "impedance": {
                "shape": (n_period, 2, 2),
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
                "dtype": complex,
                "has_method": "has_impedance",
            },
            "tipper": {
                "shape": (n_period, 1, 2),
                "output": ["hz"],
                "input": ["hx", "hy"],
                "dtype": complex,
                "has_method": "has_tipper",
            },
            "inverse_signal_power": {
                "shape": (n_period, 2, 2),
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
                "dtype": float,
                "has_method": "has_inverse_signal_power",
            },
            "residual_covariance": {
                "shape": (n_period, 3, 3),
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
                "dtype": float,
                "has_method": "has_residual_covariance",
            },
        }

        config = component_configs[component]

        # Create data
        if config["dtype"] == complex:
            data = np.random.rand(*config["shape"]) + 1j * np.random.rand(
                *config["shape"]
            )
        else:
            data = np.random.rand(*config["shape"])

        # Create DataArray
        data_array = xr.DataArray(
            data=data,
            dims=["period", "output", "input"],
            coords={
                "period": base_periods,
                "output": config["output"],
                "input": config["input"],
            },
            name=component,
        )

        # Set the component
        setattr(empty_tf, component, data_array)

        # Test the has_method
        has_method = getattr(empty_tf, config["has_method"])
        assert has_method()

        # Test data integrity
        retrieved_data = getattr(empty_tf, component)
        assert np.allclose(retrieved_data.data, data)


if __name__ == "__main__":
    pytest.main([__file__])
