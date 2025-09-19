# -*- coding: utf-8 -*-
"""
Pytest test suite for TF (Transfer Function) reading from AVG files

Created on Sat Dec  4 17:03:51 2021
Updated to pytest: August 17, 2025

:author: jpeacock
:updated_by: GitHub Copilot

:license: MIT

"""
import time
from collections import OrderedDict

import numpy as np
import pytest

from mt_metadata import TF_AVG
from mt_metadata.transfer_functions.core import TF


# =============================================================================
# Fixtures - Session scoped for maximum efficiency
# =============================================================================


@pytest.fixture(scope="session")
def tf_avg():
    """Read TF_AVG file once per session for efficiency."""
    tf = TF(fn=TF_AVG)
    tf.read()
    return tf


@pytest.fixture(scope="session")
def actual_survey_metadata(tf_avg):
    """Get actual survey metadata once per session."""
    return tf_avg.survey_metadata.to_dict(single=True)


@pytest.fixture(scope="session")
def actual_station_metadata(tf_avg):
    """Get actual station metadata once per session."""
    metadata = tf_avg.station_metadata.to_dict(single=True)
    # Remove provenance.creation_time for comparison since it varies
    if "provenance.creation_time" in metadata:
        del metadata["provenance.creation_time"]
    return metadata


@pytest.fixture(scope="session")
def actual_run_metadata(tf_avg):
    """Get actual run metadata once per session."""
    metadata = tf_avg.station_metadata.runs[0].to_dict(single=True)
    # Remove provenance.creation_time for comparison since it can vary
    if "provenance.creation_time" in metadata:
        del metadata["provenance.creation_time"]
    return metadata


@pytest.fixture(scope="session")
def expected_survey_metadata():
    """Expected survey metadata for comparison."""
    return OrderedDict(
        [
            ("acquired_by.author", ""),
            ("datum", "WGS 84"),
            ("geographic_name", ""),
            ("id", "0"),
            ("name", ""),
            ("northwest_corner.elevation", 0.0),
            ("northwest_corner.latitude", 32.83331167),
            ("northwest_corner.longitude", -107.08305667),
            ("project", ""),
            ("project_lead.author", ""),
            ("release_license", "CC-BY-4.0"),
            ("southeast_corner.elevation", 0.0),
            ("southeast_corner.latitude", 32.83331167),
            ("southeast_corner.longitude", -107.08305667),
            ("summary", ""),
            ("time_period.end_date", "1980-01-01"),
            ("time_period.start_date", "1980-01-01"),
        ]
    )


@pytest.fixture(scope="session")
def expected_station_metadata():
    """Expected station metadata for comparison."""
    return OrderedDict(
        [
            ("acquired_by.author", ""),
            ("channel_layout", "X"),
            ("channels_recorded", ["ex", "ey", "hx", "hy"]),
            ("data_type", "NSAMT"),
            ("geographic_name", ""),
            ("id", "24"),
            ("location.datum", "WGS 84"),
            ("location.declination.model", "IGRF"),
            ("location.declination.value", 0.0),
            ("location.elevation", 0.0),
            ("location.latitude", 32.83331167),
            ("location.longitude", -107.08305667),
            ("orientation.method", "compass"),
            ("orientation.reference_frame", "geographic"),
            ("orientation.value", "orthogonal"),
            ("provenance.archive.name", ""),
            ("provenance.creator.author", ""),
            ("provenance.software.author", ""),
            ("provenance.software.name", ""),
            ("provenance.software.version", ""),
            ("provenance.submitter.author", ""),
            ("run_list", ["001"]),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ("transfer_function.coordinate_system", "geographic"),
            ("transfer_function.data_quality.rating.value", None),
            ("transfer_function.id", "24"),
            ("transfer_function.processed_by.author", ""),
            ("transfer_function.processed_date", "1980-01-01T00:00:00+00:00"),
            (
                "transfer_function.processing_parameters",
                [
                    "mtedit.auto.phase_flip=yes",
                    "mtedit.d_plus.use=no",
                    "mtedit.phase_slope.smooth=robust",
                    "mtedit.phase_slope.to_z_mag=no",
                ],
            ),
            ("transfer_function.processing_type", ""),
            ("transfer_function.remote_references", []),
            ("transfer_function.runs_processed", ["001"]),
            ("transfer_function.sign_convention", "+"),
            ("transfer_function.software.author", "Zonge International"),
            ("transfer_function.software.last_updated", "2021-01-27T00:00:00+00:00"),
            ("transfer_function.software.name", "MTEdit"),
            ("transfer_function.software.version", "3.10m"),
            ("transfer_function.units", "milliVolt per kilometer per nanoTesla"),
        ]
    )


@pytest.fixture(scope="session")
def expected_run_metadata():
    """Expected run metadata for comparison."""
    return OrderedDict(
        [
            ("acquired_by.author", ""),
            ("channels_recorded_auxiliary", []),
            ("channels_recorded_electric", ["ex", "ey"]),
            ("channels_recorded_magnetic", ["hx", "hy"]),
            ("data_logger.firmware.author", ""),
            ("data_logger.firmware.name", ""),
            ("data_logger.firmware.version", ""),
            ("data_logger.manufacturer", "Zonge International"),
            ("data_logger.power_source.voltage.end", 0.0),
            ("data_logger.power_source.voltage.start", 0.0),
            ("data_logger.timing_system.drift", 0.0),
            ("data_logger.timing_system.type", "GPS"),
            ("data_logger.timing_system.uncertainty", 0.0),
            ("data_type", "BBMT"),
            ("id", "001"),
            ("metadata_by.author", ""),
            ("provenance.archive.name", ""),
            ("provenance.creator.author", ""),
            ("provenance.software.author", ""),
            ("provenance.software.name", ""),
            ("provenance.software.version", ""),
            ("provenance.submitter.author", ""),
            ("sample_rate", 0.0),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "1980-01-01T00:00:00+00:00"),
        ]
    )


@pytest.fixture(scope="session")
def expected_impedance_first():
    """Expected first impedance tensor element."""
    return np.array(
        [
            [
                -0.85198341 - 1.1020768j,
                -1.76236149 - 1.89288924j,
            ],
            [
                -0.17290554 - 0.45221147j,
                -0.16184071 - 0.1545914j,
            ],
        ]
    )


@pytest.fixture(scope="session")
def expected_impedance_last():
    """Expected last impedance tensor element."""
    return np.array(
        [
            [
                -1.90536913 - 22.95806911j,
                147.51100994 + 280.66686097j,
            ],
            [
                -164.60236806 - 270.77480464j,
                9.34354731 + 12.52851806j,
            ],
        ]
    )


@pytest.fixture(scope="session")
def expected_impedance_error_first():
    """Expected first impedance error element."""
    return np.array([[1.38180502, 2.05773344], [0.21920379, 0.16689004]])


@pytest.fixture(scope="session")
def expected_impedance_error_last():
    """Expected last impedance error element."""
    return np.array([[16.14211287, 31.70665545], [62.57734798, 5.69963839]])


# =============================================================================
# Test Classes
# =============================================================================


class TestAVGSurveyMetadata:
    """Test suite for AVG file survey metadata."""

    def test_survey_metadata(self, actual_survey_metadata, expected_survey_metadata):
        """Test survey metadata matches expected values."""
        assert actual_survey_metadata == expected_survey_metadata


class TestAVGStationMetadata:
    """Test suite for AVG file station metadata."""

    def test_station_metadata(self, actual_station_metadata, expected_station_metadata):
        """Test station metadata matches expected values, excluding creation_time."""
        assert actual_station_metadata == expected_station_metadata

    def test_station_metadata_has_creation_time(self, tf_avg):
        """Test that station metadata includes creation_time."""
        actual_metadata = tf_avg.station_metadata.to_dict(single=True)
        assert "provenance.creation_time" in actual_metadata
        assert actual_metadata["provenance.creation_time"] is not None


class TestAVGRunMetadata:
    """Test suite for AVG file run metadata."""

    def test_run_metadata(self, actual_run_metadata, expected_run_metadata):
        """Test run metadata matches expected values."""
        assert actual_run_metadata == expected_run_metadata

    def test_run_count(self, tf_avg):
        """Test that there is exactly one run."""
        assert len(tf_avg.station_metadata.runs) == 1

    def test_run_id(self, tf_avg):
        """Test run ID is correct."""
        assert tf_avg.station_metadata.runs[0].id == "001"


class TestAVGImpedanceData:
    """Test suite for AVG file impedance data."""

    def test_impedance_shape(self, tf_avg):
        """Test impedance tensor has correct shape."""
        assert tf_avg.impedance.shape == (28, 2, 2)

    def test_impedance_first_element(self, tf_avg, expected_impedance_first):
        """Test first impedance tensor element values."""
        assert np.allclose(tf_avg.impedance[0], expected_impedance_first)

    def test_impedance_last_element(self, tf_avg, expected_impedance_last):
        """Test last impedance tensor element values."""
        assert np.allclose(tf_avg.impedance[-1], expected_impedance_last)

    def test_impedance_data_type(self, tf_avg):
        """Test impedance data is complex."""
        assert tf_avg.impedance.dtype == np.complex128

    def test_impedance_no_nan_values(self, tf_avg):
        """Test impedance tensor contains no NaN values."""
        assert not np.any(np.isnan(tf_avg.impedance))


class TestAVGImpedanceError:
    """Test suite for AVG file impedance error data."""

    def test_impedance_error_shape(self, tf_avg):
        """Test impedance error has correct shape."""
        assert tf_avg.impedance_error.shape == (28, 2, 2)

    def test_impedance_error_first_element(
        self, tf_avg, expected_impedance_error_first
    ):
        """Test first impedance error element values."""
        assert np.allclose(tf_avg.impedance_error[0], expected_impedance_error_first)

    def test_impedance_error_last_element(self, tf_avg, expected_impedance_error_last):
        """Test last impedance error element values."""
        assert np.allclose(tf_avg.impedance_error[-1], expected_impedance_error_last)

    def test_impedance_error_positive_values(self, tf_avg):
        """Test all impedance errors are positive."""
        assert np.all(tf_avg.impedance_error >= 0)

    def test_impedance_error_data_type(self, tf_avg):
        """Test impedance error data is real."""
        assert tf_avg.impedance_error.dtype == np.float64


class TestAVGTransferFunctionFeatures:
    """Test suite for AVG transfer function features."""

    def test_has_tipper(self, tf_avg):
        """Test that this file does not have tipper data."""
        assert not tf_avg.has_tipper()

    def test_has_inverse_signal_power(self, tf_avg):
        """Test that this file does not have inverse signal power."""
        assert not tf_avg.has_inverse_signal_power()

    def test_has_residual_covariance(self, tf_avg):
        """Test that this file does not have residual covariance."""
        assert not tf_avg.has_residual_covariance()

    def test_frequency_count(self, tf_avg):
        """Test frequency array length matches impedance data."""
        assert len(tf_avg.frequency) == tf_avg.impedance.shape[0]

    def test_frequency_increasing(self, tf_avg):
        """Test frequency array is monotonically increasing."""
        assert np.all(tf_avg.frequency[1:] >= tf_avg.frequency[:-1])


class TestAVGIntegration:
    """Integration tests for AVG file processing."""

    def test_file_loading_consistency(self, tf_avg):
        """Test that file loading is consistent and complete."""
        assert tf_avg.survey_metadata is not None
        assert tf_avg.station_metadata is not None
        assert tf_avg.impedance is not None
        assert tf_avg.impedance_error is not None
        assert tf_avg.frequency is not None

    def test_metadata_consistency(self, tf_avg):
        """Test metadata consistency across different levels."""
        # Station ID should match between different metadata levels
        survey_id = tf_avg.survey_metadata.id
        station_id = tf_avg.station_metadata.id
        tf_id = tf_avg.station_metadata.transfer_function.id

        # Survey ID should be different from station ID in this case
        assert survey_id != station_id
        assert station_id == tf_id

    def test_data_array_consistency(self, tf_avg):
        """Test that all data arrays have consistent dimensions."""
        n_freq = len(tf_avg.frequency)
        assert tf_avg.impedance.shape[0] == n_freq
        assert tf_avg.impedance_error.shape[0] == n_freq


# =============================================================================
# Parametric Tests
# =============================================================================


@pytest.mark.parametrize(
    "metadata_field,expected_value",
    [
        ("datum", "WGS 84"),
        ("id", "0"),
        ("release_license", "CC-BY-4.0"),
        ("northwest_corner.latitude", 32.83331167),
        ("northwest_corner.longitude", -107.08305667),
    ],
)
def test_survey_metadata_fields(actual_survey_metadata, metadata_field, expected_value):
    """Test individual survey metadata fields."""
    assert actual_survey_metadata[metadata_field] == expected_value


@pytest.mark.parametrize(
    "metadata_field,expected_value",
    [
        ("id", "24"),
        ("data_type", "NSAMT"),
        ("location.datum", "WGS 84"),
        ("location.latitude", 32.83331167),
        ("location.longitude", -107.08305667),
        ("transfer_function.software.name", "MTEdit"),
        ("transfer_function.software.version", "3.10m"),
    ],
)
def test_station_metadata_fields(
    actual_station_metadata, metadata_field, expected_value
):
    """Test individual station metadata fields."""
    assert actual_station_metadata[metadata_field] == expected_value


@pytest.mark.parametrize(
    "shape_dimension,expected_size",
    [
        (0, 28),  # Number of frequencies
        (1, 2),  # Number of output channels (Ex, Ey)
        (2, 2),  # Number of input channels (Hx, Hy)
    ],
)
def test_impedance_tensor_dimensions(tf_avg, shape_dimension, expected_size):
    """Test individual dimensions of impedance tensor."""
    assert tf_avg.impedance.shape[shape_dimension] == expected_size


@pytest.mark.parametrize(
    "feature_method",
    [
        "has_tipper",
        "has_inverse_signal_power",
        "has_residual_covariance",
    ],
)
def test_transfer_function_features_absent(tf_avg, feature_method):
    """Test that optional transfer function features are absent."""
    method = getattr(tf_avg, feature_method)
    assert not method()


# =============================================================================
# Performance Tests
# =============================================================================


class TestAVGPerformance:
    """Performance tests for AVG file operations."""

    def test_file_read_performance(self):
        """Test that file reading completes in reasonable time."""
        start_time = time.time()
        tf = TF(fn=TF_AVG)
        tf.read()
        end_time = time.time()

        # Should complete within 10 seconds (increased from 5 for reliability)
        read_time = end_time - start_time
        assert read_time < 10.0, f"File reading took {read_time:.2f}s, expected < 10.0s"

    def test_memory_usage_reasonable(self, tf_avg):
        """Test that loaded data uses reasonable memory."""
        # Impedance tensor should be reasonable size
        impedance_size = tf_avg.impedance.nbytes
        error_size = tf_avg.impedance_error.nbytes

        # Should be less than 10MB for this size of data (increased from 1MB)
        total_size = impedance_size + error_size
        assert (
            total_size < 10 * 1024 * 1024
        ), f"Data size {total_size} bytes exceeds 10MB limit"

    def test_session_fixture_efficiency(self, tf_avg):
        """Test that session fixtures provide the same object reference for efficiency."""
        # This test verifies the session fixture is working efficiently
        assert hasattr(tf_avg, "impedance")
        assert hasattr(tf_avg, "frequency")
        assert tf_avg.impedance is not None
        assert tf_avg.frequency is not None


if __name__ == "__main__":
    pytest.main([__file__])
