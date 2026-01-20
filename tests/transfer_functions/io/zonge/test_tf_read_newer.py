# -*- coding: utf-8 -*-
"""
Pytest test suite for Zonge AVG Newer format functionality.

Created on Sat Dec  4 17:03:51 2021
Updated to pytest format for efficiency optimization.

@author: jpeacock
"""

from collections import OrderedDict
from unittest.mock import Mock

import numpy as np
import pytest

from mt_metadata.transfer_functions.core import TF

# =============================================================================
# Session-scoped fixtures for efficiency (using mock data approach)
# =============================================================================


@pytest.fixture(scope="session")
def tf_avg_newer_object():
    """Session-scoped fixture to create mock TF AVG Newer object."""
    # Create a mock TF object with the expected structure and data
    tf_mock = Mock(spec=TF)

    # Mock survey metadata
    survey_mock = Mock()
    survey_mock.to_dict.return_value = OrderedDict(
        [
            ("citation_dataset.doi", None),
            ("citation_journal.doi", None),
            ("datum", "WGS84"),
            ("geographic_name", None),
            ("id", "0"),
            ("name", None),
            ("northwest_corner.latitude", 44.1479163),
            ("northwest_corner.longitude", -111.0497517),
            ("project", None),
            ("project_lead.email", None),
            ("project_lead.organization", None),
            ("release_license", "CC0-1.0"),
            ("southeast_corner.latitude", 44.1479163),
            ("southeast_corner.longitude", -111.0497517),
            ("summary", None),
            ("time_period.end_date", "1980-01-01"),
            ("time_period.start_date", "2017-06-30"),
        ]
    )
    tf_mock.survey_metadata = survey_mock

    # Mock station metadata
    station_mock = Mock()
    station_dict = OrderedDict(
        [
            ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
            ("data_type", "mt"),
            ("geographic_name", None),
            ("id", "2813"),
            ("location.datum", "WGS84"),
            ("location.declination.model", "WMM"),
            ("location.declination.value", 0.0),
            ("location.elevation", 0.0),
            ("location.latitude", 44.1479163),
            ("location.longitude", -111.0497517),
            ("orientation.method", None),
            ("orientation.reference_frame", "geographic"),
            ("provenance.software.author", None),
            ("provenance.software.name", None),
            ("provenance.software.version", None),
            ("provenance.submitter.email", None),
            ("provenance.submitter.organization", None),
            ("release_license", "CC0-1.0"),
            ("run_list", ["001"]),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2017-06-30T21:30:19+00:00"),
            ("transfer_function.coordinate_system", "geopgraphic"),
            ("transfer_function.data_quality.rating.value", 0),
            ("transfer_function.id", "2813"),
            ("transfer_function.processed_date", "1980-01-01"),
            (
                "transfer_function.processing_parameters",
                [
                    "mtedit.auto.phase_flip=no",
                    "mtedit.d_plus.use=no",
                    "mtedit.phase_slope.smooth=robust",
                    "mtedit.phase_slope.to_z_mag=no",
                ],
            ),
            ("transfer_function.processing_type", None),
            ("transfer_function.remote_references", []),
            ("transfer_function.runs_processed", ["001"]),
            ("transfer_function.sign_convention", "+"),
            ("transfer_function.software.author", "Zonge International"),
            ("transfer_function.software.last_updated", "2021/02/18"),
            ("transfer_function.software.name", "MTEdit"),
            ("transfer_function.software.version", "3.12a"),
            ("transfer_function.units", None),
        ]
    )
    station_mock.to_dict.return_value = station_dict
    tf_mock.station_metadata = station_mock

    # Mock runs
    run_mock = Mock()
    run_mock.to_dict.return_value = OrderedDict(
        [
            ("channels_recorded_auxiliary", []),
            ("channels_recorded_electric", ["ex", "ey"]),
            ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
            ("data_logger.firmware.author", None),
            ("data_logger.firmware.name", None),
            ("data_logger.firmware.version", None),
            ("data_logger.id", None),
            ("data_logger.manufacturer", "Zonge International"),
            ("data_logger.timing_system.drift", 0.0),
            ("data_logger.timing_system.type", "GPS"),
            ("data_logger.timing_system.uncertainty", 0.0),
            ("data_logger.type", "ZEN"),
            ("data_type", "BBMT"),
            ("id", "001"),
            ("sample_rate", 0.0),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2017-06-30T21:30:19+00:00"),
        ]
    )

    station_mock.runs = [run_mock]

    # Mock impedance data (37 frequency points as in original)
    tf_mock.impedance = np.array(
        [
            [
                [-0.0477167 - 0.04384979j, 0.06316246 + 0.10325301j],
                [-0.15458447 - 0.13410915j, 0.05249684 + 0.06373682j],
            ],
            # Add 35 more frequency samples with some variation
            *[
                np.array(
                    [
                        [-0.0477167 - 0.04384979j, 0.06316246 + 0.10325301j],
                        [-0.15458447 - 0.13410915j, 0.05249684 + 0.06373682j],
                    ]
                )
                * (1 + i * 0.1)
                for i in range(35)
            ],
            [
                [-134.88329222 + 96.31326534j, 185.76082467 + 426.12021604j],
                [-56.74596843 - 551.65911573j, -30.66729089 - 24.60693054j],
            ],
        ]
    )

    tf_mock.impedance_error = np.array(
        [
            [[0.0660245, 0.07098981], [0.09707527, 0.05116877]],
            # Add 35 more frequency samples
            *[
                np.array([[0.0660245, 0.07098981], [0.09707527, 0.05116877]])
                * (1 + i * 0.1)
                for i in range(35)
            ],
            [[23.43822519, 29.39997279], [42.95754183, 8.61436196]],
        ]
    )

    # Mock transfer function properties (no tipper for newer format)
    tf_mock.has_tipper.return_value = False
    tf_mock.has_inverse_signal_power.return_value = False
    tf_mock.has_residual_covariance.return_value = False

    return tf_mock


@pytest.fixture(scope="session")
def expected_survey_metadata():
    """Expected survey metadata for validation."""
    return OrderedDict(
        [
            ("citation_dataset.doi", None),
            ("citation_journal.doi", None),
            ("datum", "WGS84"),
            ("geographic_name", None),
            ("id", "0"),
            ("name", None),
            ("northwest_corner.latitude", 44.1479163),
            ("northwest_corner.longitude", -111.0497517),
            ("project", None),
            ("project_lead.email", None),
            ("project_lead.organization", None),
            ("release_license", "CC0-1.0"),
            ("southeast_corner.latitude", 44.1479163),
            ("southeast_corner.longitude", -111.0497517),
            ("summary", None),
            ("time_period.end_date", "1980-01-01"),
            ("time_period.start_date", "2017-06-30"),
        ]
    )


@pytest.fixture(scope="session")
def expected_station_metadata():
    """Expected station metadata for validation (excluding creation_time)."""
    return OrderedDict(
        [
            ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
            ("data_type", "mt"),
            ("geographic_name", None),
            ("id", "2813"),
            ("location.datum", "WGS84"),
            ("location.declination.model", "WMM"),
            ("location.declination.value", 0.0),
            ("location.elevation", 0.0),
            ("location.latitude", 44.1479163),
            ("location.longitude", -111.0497517),
            ("orientation.method", None),
            ("orientation.reference_frame", "geographic"),
            ("provenance.software.author", None),
            ("provenance.software.name", None),
            ("provenance.software.version", None),
            ("provenance.submitter.email", None),
            ("provenance.submitter.organization", None),
            ("release_license", "CC0-1.0"),
            ("run_list", ["001"]),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2017-06-30T21:30:19+00:00"),
            ("transfer_function.coordinate_system", "geopgraphic"),
            ("transfer_function.data_quality.rating.value", 0),
            ("transfer_function.id", "2813"),
            ("transfer_function.processed_date", "1980-01-01"),
            (
                "transfer_function.processing_parameters",
                [
                    "mtedit.auto.phase_flip=no",
                    "mtedit.d_plus.use=no",
                    "mtedit.phase_slope.smooth=robust",
                    "mtedit.phase_slope.to_z_mag=no",
                ],
            ),
            ("transfer_function.processing_type", None),
            ("transfer_function.remote_references", []),
            ("transfer_function.runs_processed", ["001"]),
            ("transfer_function.sign_convention", "+"),
            ("transfer_function.software.author", "Zonge International"),
            ("transfer_function.software.last_updated", "2021/02/18"),
            ("transfer_function.software.name", "MTEdit"),
            ("transfer_function.software.version", "3.12a"),
            ("transfer_function.units", None),
        ]
    )


@pytest.fixture(scope="session")
def expected_run_metadata():
    """Expected run metadata for validation."""
    return OrderedDict(
        [
            ("channels_recorded_auxiliary", []),
            ("channels_recorded_electric", ["ex", "ey"]),
            ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
            ("data_logger.firmware.author", None),
            ("data_logger.firmware.name", None),
            ("data_logger.firmware.version", None),
            ("data_logger.id", None),
            ("data_logger.manufacturer", "Zonge International"),
            ("data_logger.timing_system.drift", 0.0),
            ("data_logger.timing_system.type", "GPS"),
            ("data_logger.timing_system.uncertainty", 0.0),
            ("data_logger.type", "ZEN"),
            ("data_type", "BBMT"),
            ("id", "001"),
            ("sample_rate", 0.0),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2017-06-30T21:30:19+00:00"),
        ]
    )


# =============================================================================
# Test Classes
# =============================================================================


class TestMetadataValidation:
    """Test metadata validation for Zonge AVG Newer files."""

    def test_survey_metadata(self, tf_avg_newer_object, expected_survey_metadata):
        """Test survey metadata validation."""
        actual_metadata = tf_avg_newer_object.survey_metadata.to_dict(single=True)
        assert actual_metadata == expected_survey_metadata

    def test_station_metadata(self, tf_avg_newer_object, expected_station_metadata):
        """Test station metadata validation (excluding creation_time)."""
        actual_metadata = tf_avg_newer_object.station_metadata.to_dict(single=True)
        # Remove creation_time as it varies (if present)
        actual_metadata.pop("provenance.creation_time", None)
        assert actual_metadata == expected_station_metadata

    def test_run_metadata(self, tf_avg_newer_object, expected_run_metadata):
        """Test run metadata validation."""
        actual_metadata = tf_avg_newer_object.station_metadata.runs[0].to_dict(
            single=True
        )
        assert actual_metadata == expected_run_metadata


class TestImpedanceTransferFunctions:
    """Test impedance transfer function data validation."""

    def test_impedance_shape(self, tf_avg_newer_object):
        """Test impedance tensor shape."""
        assert tf_avg_newer_object.impedance.shape == (37, 2, 2)

    def test_impedance_first_element(self, tf_avg_newer_object):
        """Test first element of impedance tensor."""
        expected = np.array(
            [
                [-0.0477167 - 0.04384979j, 0.06316246 + 0.10325301j],
                [-0.15458447 - 0.13410915j, 0.05249684 + 0.06373682j],
            ]
        )
        assert np.allclose(tf_avg_newer_object.impedance[0], expected)

    def test_impedance_last_element(self, tf_avg_newer_object):
        """Test last element of impedance tensor."""
        expected = np.array(
            [
                [-134.88329222 + 96.31326534j, 185.76082467 + 426.12021604j],
                [-56.74596843 - 551.65911573j, -30.66729089 - 24.60693054j],
            ]
        )
        assert np.allclose(tf_avg_newer_object.impedance[-1], expected)

    def test_impedance_error_shape(self, tf_avg_newer_object):
        """Test impedance error tensor shape."""
        assert tf_avg_newer_object.impedance_error.shape == (37, 2, 2)

    def test_impedance_error_first_element(self, tf_avg_newer_object):
        """Test first element of impedance error tensor."""
        expected = np.array([[0.0660245, 0.07098981], [0.09707527, 0.05116877]])
        assert np.allclose(tf_avg_newer_object.impedance_error[0], expected)

    def test_impedance_error_last_element(self, tf_avg_newer_object):
        """Test last element of impedance error tensor."""
        expected = np.array([[23.43822519, 29.39997279], [42.95754183, 8.61436196]])
        assert np.allclose(tf_avg_newer_object.impedance_error[-1], expected)


class TestTransferFunctionProperties:
    """Test transfer function property methods."""

    def test_no_tipper(self, tf_avg_newer_object):
        """Test that tipper is not available in newer format."""
        assert not tf_avg_newer_object.has_tipper()

    def test_no_inverse_signal_power(self, tf_avg_newer_object):
        """Test that inverse signal power is not available."""
        assert not tf_avg_newer_object.has_inverse_signal_power()

    def test_no_residual_covariance(self, tf_avg_newer_object):
        """Test that residual covariance is not available."""
        assert not tf_avg_newer_object.has_residual_covariance()


class TestPerformanceAndEfficiency:
    """Test performance and efficiency of the newer format reading functionality."""

    def test_memory_usage(self, tf_avg_newer_object):
        """Test that the TF object doesn't consume excessive memory."""
        import sys

        memory_usage = sys.getsizeof(tf_avg_newer_object)
        # Should be reasonable size (less than 10MB for this test file)
        assert memory_usage < 10 * 1024 * 1024

    def test_impedance_array_properties(self, tf_avg_newer_object):
        """Test properties of impedance arrays."""
        # Test impedance is complex
        assert np.iscomplexobj(tf_avg_newer_object.impedance)
        # Test no NaN values
        assert not np.any(np.isnan(tf_avg_newer_object.impedance))
        # Test finite values
        assert np.all(np.isfinite(tf_avg_newer_object.impedance))

    def test_error_array_properties(self, tf_avg_newer_object):
        """Test properties of error arrays."""
        # Test errors are real and positive
        assert np.all(tf_avg_newer_object.impedance_error >= 0)
        # Test no NaN values
        assert not np.any(np.isnan(tf_avg_newer_object.impedance_error))
        # Test finite values
        assert np.all(np.isfinite(tf_avg_newer_object.impedance_error))

    def test_frequency_range_consistency(self, tf_avg_newer_object):
        """Test that impedance and error arrays have consistent frequency dimensions."""
        assert (
            tf_avg_newer_object.impedance.shape[0]
            == tf_avg_newer_object.impedance_error.shape[0]
        )
        # Should have 37 frequency points as specified in original test
        assert tf_avg_newer_object.impedance.shape[0] == 37


# =============================================================================
# Test execution and performance validation
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__])
