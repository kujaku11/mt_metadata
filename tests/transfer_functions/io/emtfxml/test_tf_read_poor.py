# -*- coding: utf-8 -*-
"""
pytest suite for EMTFXML poor data reading tests

Created on Sat Dec  4 17:03:51 2021
Converted to pytest: August 2025

@author: jpeacock
"""

import numpy as np

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_POOR_XML
from mt_metadata.transfer_functions.core import TF

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="session")
def tf_object():
    """TF object loaded from poor quality XML file."""
    tf = TF(fn=TF_POOR_XML)
    tf.read()
    return tf


# =============================================================================
# Test Classes
# =============================================================================


class TestEMTFXMLPoorReading:
    """Test reading poor quality EMTFXML data into TF objects."""

    def test_station_metadata_structure(self, tf_object):
        """Test station metadata structure and key fields."""
        station_dict = tf_object.station_metadata.to_dict(single=True)

        # Test essential keys are present
        essential_keys = [
            "acquired_by.author",
            "channels_recorded",
            "data_type",
            "id",
            "location.latitude",
            "location.longitude",
            "location.elevation",
            "transfer_function.processing_type",
            "transfer_function.remote_references",
        ]

        for key in essential_keys:
            assert key in station_dict, f"Missing essential key: {key}"

        # Test specific known values
        assert (
            station_dict["acquired_by.author"] == "National Geoelectromagnetic Facility"
        )
        assert station_dict["data_type"] == "MT"
        assert station_dict["id"] == "CAS04"
        assert isinstance(station_dict["channels_recorded"], list)
        assert "ex" in station_dict["channels_recorded"]
        assert "ey" in station_dict["channels_recorded"]

    def test_survey_metadata_structure(self, tf_object):
        """Test survey metadata structure and key fields."""
        survey_dict = tf_object.survey_metadata.to_dict(single=True)

        # Test essential keys are present
        essential_keys = [
            "acquired_by.author",
            "id",
            "geographic_name",
            "project",
            "release_license",
        ]

        for key in essential_keys:
            assert key in survey_dict, f"Missing essential key: {key}"

        # Test specific known values
        assert (
            survey_dict["acquired_by.author"] == "National Geoelectromagnetic Facility"
        )
        assert survey_dict["id"] == "CONUS South"
        assert survey_dict["project"] == "USMTArray"
        assert survey_dict["release_license"] == "CC-BY-4.0"

    def test_run_metadata_structure(self, tf_object):
        """Test run metadata structure and key fields."""
        run_dict = tf_object.station_metadata.runs[0].to_dict(single=True)

        # Test essential keys are present
        essential_keys = [
            "channels_recorded_electric",
            "channels_recorded_magnetic",
            "data_type",
            "id",
            "data_logger.timing_system.type",
        ]

        for key in essential_keys:
            assert key in run_dict, f"Missing essential key: {key}"

        # Test specific known values
        assert run_dict["data_type"] == "BBMT"
        assert run_dict["id"] == "CAS04a"
        assert run_dict["data_logger.timing_system.type"] == "GPS"
        assert isinstance(run_dict["channels_recorded_electric"], list)
        assert isinstance(run_dict["channels_recorded_magnetic"], list)


class TestEMTFXMLPoorImpedanceData:
    """Test impedance data extraction from poor quality EMTFXML."""

    def test_impedance_shape(self, tf_object):
        """Test impedance tensor shape."""
        assert tf_object.impedance.shape == (33, 2, 2)

    def test_impedance_first_element(self, tf_object):
        """Test first impedance tensor element values."""
        expected = np.array(
            [
                [0.05218971 - 0.493787j, 1.004782 + 1.873659j],
                [-0.8261183 + 1.226159j, 1.36161 - 1.376113j],
            ]
        )
        assert np.allclose(tf_object.impedance[0], expected)

    def test_impedance_last_element(self, tf_object):
        """Test last impedance tensor element values."""
        expected = np.array(
            [
                [0.03680307 + 0.00131353j, 0.06559774 + 0.00177508j],
                [-0.05877226 - 0.02631392j, -0.01419307 - 0.03934453j],
            ]
        )
        assert np.allclose(tf_object.impedance[-1], expected)

    def test_inverse_signal_power(self, tf_object):
        """Test inverse signal power (should be None for poor data)."""
        assert tf_object.inverse_signal_power is None

    def test_residual_covariance(self, tf_object):
        """Test residual covariance (should be None for poor data)."""
        assert tf_object.residual_covariance is None


class TestEMTFXMLPoorTipperData:
    """Test tipper data extraction from poor quality EMTFXML."""

    def test_tipper_shape(self, tf_object):
        """Test tipper tensor shape."""
        assert tf_object.tipper.shape == (33, 1, 2)

    def test_tipper_first_element(self, tf_object):
        """Test first tipper tensor element values."""
        expected = np.array([[-0.5953611 - 1.984346j, -1.313187 + 1.159378j]])
        assert np.allclose(tf_object.tipper[0], expected)

    def test_tipper_last_element(self, tf_object):
        """Test last tipper tensor element values."""
        expected = np.array([[-0.02102757 - 0.06664169j, 0.5568553 + 0.1630035j]])
        assert np.allclose(tf_object.tipper[-1], expected)


class TestEMTFXMLPoorIntegration:
    """Integration tests for poor quality EMTFXML reading."""

    def test_tf_object_creation(self, tf_object):
        """Test that TF object is properly created from poor XML."""
        assert tf_object is not None
        assert hasattr(tf_object, "station_metadata")
        assert hasattr(tf_object, "survey_metadata")
        assert hasattr(tf_object, "impedance")
        assert hasattr(tf_object, "tipper")

    def test_period_consistency(self, tf_object):
        """Test that period arrays are consistent across different components."""
        assert len(tf_object.period) == tf_object.impedance.shape[0]
        assert len(tf_object.period) == tf_object.tipper.shape[0]

    def test_data_completeness(self, tf_object):
        """Test that essential data components are present."""
        assert tf_object.impedance is not None
        assert tf_object.tipper is not None
        assert tf_object.period is not None
        assert len(tf_object.period) > 0


class TestEMTFXMLPoorDataQuality:
    """Test data quality characteristics of poor EMTFXML data."""

    def test_missing_covariance_data(self, tf_object):
        """Test that covariance matrices are None for poor quality data."""
        assert tf_object.inverse_signal_power is None
        assert tf_object.residual_covariance is None

    def test_impedance_data_quality(self, tf_object):
        """Test impedance data quality characteristics."""
        # Check for finite values in impedance data
        assert np.all(np.isfinite(tf_object.impedance))

        # Check that impedance values are reasonable (not all zeros)
        assert not np.allclose(tf_object.impedance, 0.0)

    def test_tipper_data_quality(self, tf_object):
        """Test tipper data quality characteristics."""
        # Check for finite values in tipper data
        assert np.all(np.isfinite(tf_object.tipper))

        # Check that tipper values are reasonable (not all zeros)
        assert not np.allclose(tf_object.tipper, 0.0)

    def test_metadata_completeness(self, tf_object):
        """Test metadata completeness for poor quality data."""
        # Check essential station metadata fields
        assert tf_object.station_metadata.id is not None
        assert tf_object.station_metadata.location.latitude is not None
        assert tf_object.station_metadata.location.longitude is not None

        # Check survey metadata is present
        assert tf_object.survey_metadata.id is not None


class TestEMTFXMLPoorDataTypes:
    """Test data type handling for poor quality EMTFXML data."""

    def test_impedance_dtype(self, tf_object):
        """Test impedance data type."""
        assert tf_object.impedance.dtype == np.complex128

    def test_tipper_dtype(self, tf_object):
        """Test tipper data type."""
        assert tf_object.tipper.dtype == np.complex128

    def test_period_dtype(self, tf_object):
        """Test period data type."""
        assert tf_object.period.dtype == np.float64

    def test_variance_handling(self, tf_object):
        """Test variance data handling for poor quality data."""
        # Check that variance attributes exist even if they might be None/empty
        assert hasattr(tf_object, "impedance_error")
        assert hasattr(tf_object, "tipper_error")


class TestEMTFXMLPoorEdgeCases:
    """Test edge cases for poor quality EMTFXML data processing."""

    def test_remote_reference_processing(self, tf_object):
        """Test remote reference information processing."""
        processing_params = (
            tf_object.station_metadata.transfer_function.processing_parameters
        )
        assert isinstance(processing_params, list)

        # Check that remote reference parameters are properly parsed
        remote_params = [p for p in processing_params if "remote_info" in p]
        assert len(remote_params) > 0

    def test_coordinate_system_handling(self, tf_object):
        """Test coordinate system handling."""
        coord_system = tf_object.station_metadata.transfer_function.coordinate_system
        assert coord_system is not None

    def test_data_quality_rating(self, tf_object):
        """Test data quality rating extraction."""
        rating = tf_object.station_metadata.transfer_function.data_quality.rating.value
        assert isinstance(rating, (int, float))
        assert rating > 0


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
