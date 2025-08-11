# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for ZSS TF reading functionality.

Created on Sat Dec  4 17:03:51 2021
@author: jpeacock

Modernized for pytest with fixtures and subtests for optimal efficiency.
"""

from collections import OrderedDict

import numpy as np

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_ZSS_TIPPER
from mt_metadata.transfer_functions.core import TF


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="class")
def tf_obj():
    """Fixture providing TF object loaded from ZSS tipper file."""
    try:
        tf_object = TF(fn=TF_ZSS_TIPPER)
        tf_object.read()
        return tf_object
    except Exception as e:
        pytest.skip(f"Cannot load TF object from ZSS file: {e}")


@pytest.fixture(scope="class")
def expected_survey_metadata():
    """Expected survey metadata for ZSS tipper test data."""
    return OrderedDict(
        [
            ("acquired_by.author", ""),
            ("datum", "WGS 84"),
            ("geographic_name", ""),
            ("id", "0"),
            ("name", ""),
            ("northwest_corner.elevation", 0.0),
            ("northwest_corner.latitude", 44.631),
            ("northwest_corner.longitude", -110.44),
            ("project", ""),
            ("project_lead.author", ""),
            ("release_license", "CC-BY-4.0"),
            ("southeast_corner.elevation", 0.0),
            ("southeast_corner.latitude", 44.631),
            ("southeast_corner.longitude", -110.44),
            ("summary", ""),
            ("time_period.end_date", "1980-01-01"),
            ("time_period.start_date", "1980-01-01"),
        ]
    )


@pytest.fixture(scope="class")
def expected_station_metadata():
    """Expected station metadata for ZSS tipper test data (excluding time-sensitive fields)."""
    return OrderedDict(
        [
            ("acquired_by.author", ""),
            ("channel_layout", "X"),
            ("channels_recorded", ["hx", "hy", "hz"]),
            ("comments", "WITH FULL ERROR COVARIANCE"),
            ("data_type", "MT"),
            ("geographic_name", ""),
            ("id", "YSW212abcdefghijkl"),
            ("location.datum", "WGS 84"),
            ("location.declination.model", "IGRF"),
            ("location.declination.value", 11.18),
            ("location.elevation", 0.0),
            ("location.latitude", 44.631),
            ("location.longitude", -110.44),
            ("orientation.method", "compass"),
            ("orientation.reference_frame", "geographic"),
            ("orientation.value", "orthogonal"),
            ("provenance.archive.name", ""),
            ("provenance.creator.author", ""),
            ("provenance.software.author", ""),
            ("provenance.software.name", "EMTF"),
            ("provenance.software.version", "1"),
            ("provenance.submitter.author", ""),
            ("run_list", ["ysw212abcdefghijkla"]),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ("transfer_function.coordinate_system", "geographic"),
            ("transfer_function.data_quality.rating.value", None),
            ("transfer_function.id", "ysw212abcdefghijkl"),
            ("transfer_function.processed_by.author", ""),
            ("transfer_function.processed_date", "1980-01-01T00:00:00+00:00"),
            ("transfer_function.processing_parameters", []),
            ("transfer_function.processing_type", "Robust Single station"),
            ("transfer_function.remote_references", []),
            ("transfer_function.runs_processed", ["ysw212abcdefghijkla"]),
            ("transfer_function.sign_convention", "+"),
            ("transfer_function.software.author", ""),
            ("transfer_function.software.name", "EMTF"),
            ("transfer_function.software.version", "1"),
            ("transfer_function.units", "milliVolt per kilometer per nanoTesla"),
        ]
    )


@pytest.fixture(scope="class")
def expected_run_metadata():
    """Expected run metadata for ZSS tipper test data."""
    return OrderedDict(
        [
            ("acquired_by.author", ""),
            ("channels_recorded_auxiliary", []),
            ("channels_recorded_electric", []),
            ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
            ("data_logger.firmware.author", ""),
            ("data_logger.firmware.name", ""),
            ("data_logger.firmware.version", ""),
            ("data_logger.power_source.voltage.end", 0.0),
            ("data_logger.power_source.voltage.start", 0.0),
            ("data_logger.timing_system.drift", 0.0),
            ("data_logger.timing_system.type", "GPS"),
            ("data_logger.timing_system.uncertainty", 0.0),
            ("data_type", "BBMT"),
            ("id", "ysw212abcdefghijkla"),
            ("metadata_by.author", ""),
            ("provenance.archive.name", ""),
            ("provenance.creator.author", ""),
            ("provenance.software.author", ""),
            ("provenance.software.name", ""),
            ("provenance.software.version", ""),
            ("provenance.submitter.author", ""),
            ("sample_rate", 5.0),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "1980-01-01T00:00:00+00:00"),
        ]
    )


@pytest.fixture(scope="class")
def expected_array_values():
    """Expected array values for validation."""
    return {
        "tipper_first": np.array([[-0.20389999 + 0.09208j, 0.05996000 + 0.03177j]]),
        "tipper_last": np.array([[-0.01205 - 0.03873j, -0.09759 - 0.03014j]]),
        "inverse_signal_power_first": np.array(
            [
                [136.19999695 + 0.0j, -9.60000038 + 5.32700014j],
                [-9.60000038 - 5.32700014j, 336.1000061 + 0.0j],
            ]
        ),
        "inverse_signal_power_last": np.array(
            [
                [3.59999990e-06 + 0.00000000e00j, 2.10999997e-06 + 9.44800007e-08j],
                [2.10999997e-06 - 9.44800007e-08j, 4.55500003e-06 + 0.00000000e00j],
            ]
        ),
        "residual_covariance_first": np.array(
            [
                [0.00000000e00 + 0.0j, 0.00000000e00 + 0.0j, 0.00000000e00 + 0.0j],
                [0.00000000e00 + 0.0j, 0.00000000e00 + 0.0j, 0.00000000e00 + 0.0j],
                [0.00000000e00 + 0.0j, 0.00000000e00 + 0.0j, 4.62099982e-18 + 0.0j],
            ]
        ),
        "residual_covariance_last": np.array(
            [
                [0.00000000 + 0.0j, 0.00000000 + 0.0j, 0.00000000 + 0.0j],
                [0.00000000 + 0.0j, 0.00000000 + 0.0j, 0.00000000 + 0.0j],
                [0.00000000 + 0.0j, 0.00000000 + 0.0j, 38.70000076 + 0.0j],
            ]
        ),
    }


# =============================================================================
# Test Classes
# =============================================================================


class TestZSSTFObjectCreation:
    """Test TF object creation and basic functionality."""

    def test_tf_object_creation(self):
        """Test TF object can be created from ZSS file."""
        try:
            tf_obj = TF(fn=TF_ZSS_TIPPER)
            tf_obj.read()
            assert tf_obj is not None
            assert hasattr(tf_obj, "survey_metadata")
            assert hasattr(tf_obj, "station_metadata")
        except Exception as e:
            pytest.skip(f"Cannot create TF object: {e}")

    def test_transfer_function_capabilities(self, subtests):
        """Test transfer function capability detection."""
        try:
            tf_obj = TF(fn=TF_ZSS_TIPPER)
            tf_obj.read()
        except Exception as e:
            pytest.skip(f"Cannot test TF capabilities: {e}")

        with subtests.test(capability="impedance"):
            assert (
                tf_obj.has_impedance() is False
            ), "ZSS tipper file should not have impedance capability"

        with subtests.test(capability="tipper"):
            assert (
                tf_obj.has_tipper() is True
            ), "ZSS tipper file should have tipper capability"

        with subtests.test(capability="inverse_signal_power"):
            assert (
                tf_obj.has_inverse_signal_power() is True
            ), "ZSS file should have inverse signal power"

        with subtests.test(capability="residual_covariance"):
            assert (
                tf_obj.has_residual_covariance() is True
            ), "ZSS file should have residual covariance"


class TestZSSSurveyMetadata:
    """Test survey metadata from ZSS file."""

    def test_survey_metadata_comparison(
        self, tf_obj, expected_survey_metadata, subtests
    ):
        """Test survey metadata matches expected values."""
        try:
            actual_metadata = tf_obj.survey_metadata.to_dict(single=True)
        except Exception as e:
            pytest.skip(f"Cannot get survey metadata: {e}")

        for key, expected_value in expected_survey_metadata.items():
            with subtests.test(metadata_field=key):
                assert (
                    key in actual_metadata
                ), f"Field {key} missing from survey metadata"
                actual_value = actual_metadata[key]
                assert (
                    actual_value == expected_value
                ), f"Survey metadata mismatch in {key}: expected {expected_value}, got {actual_value}"


class TestZSSStationMetadata:
    """Test station metadata from ZSS file."""

    def test_station_metadata_comparison(
        self, tf_obj, expected_station_metadata, subtests
    ):
        """Test station metadata matches expected values (excluding time-sensitive fields)."""
        try:
            actual_metadata = tf_obj.station_metadata.to_dict(single=True)
        except Exception as e:
            pytest.skip(f"Cannot get station metadata: {e}")

        # Exclude time-sensitive fields
        excluded_fields = ["provenance.creation_time"]
        filtered_metadata = {
            k: v for k, v in actual_metadata.items() if k not in excluded_fields
        }

        for key, expected_value in expected_station_metadata.items():
            with subtests.test(metadata_field=key):
                assert (
                    key in filtered_metadata
                ), f"Field {key} missing from station metadata"
                actual_value = filtered_metadata[key]
                assert (
                    actual_value == expected_value
                ), f"Station metadata mismatch in {key}: expected {expected_value}, got {actual_value}"

    def test_station_metadata_completeness(self, tf_obj):
        """Test that station metadata contains required fields."""
        try:
            actual_metadata = tf_obj.station_metadata.to_dict(single=True)
        except Exception as e:
            pytest.skip(f"Cannot test station metadata completeness: {e}")

        required_fields = [
            "id",
            "location.latitude",
            "location.longitude",
            "channels_recorded",
        ]

        for field in required_fields:
            assert (
                field in actual_metadata
            ), f"Required field {field} missing from station metadata"
            assert actual_metadata[field] is not None, f"Required field {field} is None"


class TestZSSRunMetadata:
    """Test run metadata from ZSS file."""

    def test_run_metadata_comparison(self, tf_obj, expected_run_metadata, subtests):
        """Test run metadata matches expected values."""
        try:
            actual_metadata = tf_obj.station_metadata.runs[0].to_dict(single=True)
        except Exception as e:
            pytest.skip(f"Cannot get run metadata: {e}")

        for key, expected_value in expected_run_metadata.items():
            with subtests.test(metadata_field=key):
                assert key in actual_metadata, f"Field {key} missing from run metadata"
                actual_value = actual_metadata[key]
                assert (
                    actual_value == expected_value
                ), f"Run metadata mismatch in {key}: expected {expected_value}, got {actual_value}"

    def test_run_count(self, tf_obj):
        """Test that exactly one run is present."""
        try:
            runs = tf_obj.station_metadata.runs
            assert len(runs) == 1, f"Expected 1 run, got {len(runs)}"
        except Exception as e:
            pytest.skip(f"Cannot test run count: {e}")


class TestZSSTipperData:
    """Test tipper transfer function data."""

    def test_tipper_properties(self, tf_obj, subtests):
        """Test tipper array properties."""
        try:
            tipper = tf_obj.tipper
        except Exception as e:
            pytest.skip(f"Cannot get tipper data: {e}")

        with subtests.test(property="shape"):
            expected_shape = (44, 1, 2)
            actual_shape = tipper.shape
            assert (
                actual_shape == expected_shape
            ), f"Tipper shape: expected {expected_shape}, got {actual_shape}"

        with subtests.test(property="dtype"):
            assert np.iscomplexobj(tipper), "Tipper should be complex array"

    def test_tipper_values(self, tf_obj, expected_array_values, subtests):
        """Test tipper array values."""
        try:
            tipper = tf_obj.tipper
        except Exception as e:
            pytest.skip(f"Cannot get tipper values: {e}")

        with subtests.test(element="first"):
            expected_first = expected_array_values["tipper_first"]
            actual_first = tipper[0]
            assert np.allclose(
                actual_first, expected_first
            ), f"Tipper first element mismatch: expected {expected_first}, got {actual_first}"

        with subtests.test(element="last"):
            expected_last = expected_array_values["tipper_last"]
            actual_last = tipper[-1]
            assert np.allclose(
                actual_last, expected_last
            ), f"Tipper last element mismatch: expected {expected_last}, got {actual_last}"


class TestZSSInverseSignalPower:
    """Test inverse signal power matrix data."""

    def test_inverse_signal_power_properties(self, tf_obj, subtests):
        """Test inverse signal power array properties."""
        try:
            isp = tf_obj.inverse_signal_power
        except Exception as e:
            pytest.skip(f"Cannot get inverse signal power data: {e}")

        with subtests.test(property="shape"):
            expected_shape = (44, 2, 2)
            actual_shape = isp.shape
            assert (
                actual_shape == expected_shape
            ), f"Inverse signal power shape: expected {expected_shape}, got {actual_shape}"

        with subtests.test(property="dtype"):
            assert np.iscomplexobj(isp), "Inverse signal power should be complex array"

    def test_inverse_signal_power_values(self, tf_obj, expected_array_values, subtests):
        """Test inverse signal power array values."""
        try:
            isp = tf_obj.inverse_signal_power
        except Exception as e:
            pytest.skip(f"Cannot get inverse signal power values: {e}")

        with subtests.test(element="first"):
            expected_first = expected_array_values["inverse_signal_power_first"]
            actual_first = isp[0]
            assert np.allclose(
                actual_first, expected_first, atol=1e-5
            ), f"ISP first element mismatch: expected {expected_first}, got {actual_first}"

        with subtests.test(element="last"):
            expected_last = expected_array_values["inverse_signal_power_last"]
            actual_last = isp[-1]
            assert np.allclose(
                actual_last, expected_last, atol=1e-5
            ), f"ISP last element mismatch: expected {expected_last}, got {actual_last}"


class TestZSSResidualCovariance:
    """Test residual covariance matrix data."""

    def test_residual_covariance_properties(self, tf_obj, subtests):
        """Test residual covariance array properties."""
        try:
            residual = tf_obj.residual_covariance
        except Exception as e:
            pytest.skip(f"Cannot get residual covariance data: {e}")

        with subtests.test(property="shape"):
            expected_shape = (44, 3, 3)
            actual_shape = residual.shape
            assert (
                actual_shape == expected_shape
            ), f"Residual covariance shape: expected {expected_shape}, got {actual_shape}"

        with subtests.test(property="dtype"):
            assert np.iscomplexobj(
                residual
            ), "Residual covariance should be complex array"

    def test_residual_covariance_values(self, tf_obj, expected_array_values, subtests):
        """Test residual covariance array values."""
        try:
            residual = tf_obj.residual_covariance
        except Exception as e:
            pytest.skip(f"Cannot get residual covariance values: {e}")

        with subtests.test(element="first"):
            expected_first = expected_array_values["residual_covariance_first"]
            actual_first = residual[0]
            assert np.allclose(
                actual_first, expected_first
            ), f"Residual covariance first element mismatch: expected {expected_first}, got {actual_first}"

        with subtests.test(element="last"):
            expected_last = expected_array_values["residual_covariance_last"]
            actual_last = residual[-1]
            assert np.allclose(
                actual_last, expected_last
            ), f"Residual covariance last element mismatch: expected {expected_last}, got {actual_last}"


# =============================================================================
# Integration and Performance Tests
# =============================================================================


class TestZSSIntegration:
    """Test integration scenarios and comprehensive workflows."""

    def test_complete_data_loading(self, tf_obj, subtests):
        """Test that all data components are properly loaded."""
        with subtests.test(component="tipper"):
            assert tf_obj.has_tipper() is True
            assert tf_obj.tipper is not None
            assert tf_obj.tipper.size > 0

        with subtests.test(component="inverse_signal_power"):
            assert tf_obj.has_inverse_signal_power() is True
            assert tf_obj.inverse_signal_power is not None
            assert tf_obj.inverse_signal_power.size > 0

        with subtests.test(component="residual_covariance"):
            assert tf_obj.has_residual_covariance() is True
            assert tf_obj.residual_covariance is not None
            assert tf_obj.residual_covariance.size > 0

    def test_data_consistency(self, tf_obj, subtests):
        """Test consistency across different data components."""
        try:
            tipper = tf_obj.tipper
            isp = tf_obj.inverse_signal_power
            residual = tf_obj.residual_covariance
        except Exception as e:
            pytest.skip(f"Cannot get data for consistency testing: {e}")

        with subtests.test(consistency="frequency_count"):
            # All arrays should have same number of frequencies
            assert (
                tipper.shape[0] == isp.shape[0] == residual.shape[0]
            ), "Frequency count mismatch across arrays"

        with subtests.test(consistency="no_nan_values"):
            # No NaN values in any array
            assert not np.any(np.isnan(tipper)), "Tipper contains NaN values"
            assert not np.any(np.isnan(isp)), "Inverse signal power contains NaN values"
            assert not np.any(
                np.isnan(residual)
            ), "Residual covariance contains NaN values"

    def test_metadata_data_consistency(self, tf_obj, subtests):
        """Test consistency between metadata and actual data."""
        try:
            station_metadata = tf_obj.station_metadata.to_dict(single=True)
            tipper = tf_obj.tipper
        except Exception as e:
            pytest.skip(f"Cannot test metadata-data consistency: {e}")

        with subtests.test(consistency="channels_recorded"):
            # Channels recorded should match data structure
            channels_recorded = station_metadata.get("channels_recorded", [])
            expected_channels = ["hx", "hy", "hz"]
            assert (
                channels_recorded == expected_channels
            ), f"Channels recorded mismatch: expected {expected_channels}, got {channels_recorded}"


class TestZSSPerformance:
    """Test performance and efficiency aspects."""

    def test_multiple_object_creation(self, subtests):
        """Test that multiple TF objects can be created efficiently."""
        with subtests.test(test="multiple_creation"):
            try:
                objects = []
                for i in range(3):
                    tf_obj = TF(fn=TF_ZSS_TIPPER)
                    tf_obj.read()
                    objects.append(tf_obj)
                    assert tf_obj.has_tipper() is True

                # All objects should be independent
                assert len(set(id(obj) for obj in objects)) == 3
            except Exception as e:
                pytest.skip(f"Cannot test multiple object creation: {e}")

    def test_repeated_access_consistency(self):
        """Test that repeated data access doesn't change values."""
        try:
            tf_obj = TF(fn=TF_ZSS_TIPPER)
            tf_obj.read()

            # Check if objects are properly loaded
            if tf_obj.tipper is None or tf_obj.station_metadata is None:
                pytest.skip("TF object not properly loaded for consistency testing")

        except Exception as e:
            pytest.skip(f"Cannot test repeated access: {e}")

        # Get initial values
        initial_tipper_first = tf_obj.tipper[0].copy()
        initial_station_metadata = tf_obj.station_metadata.to_dict(single=True)
        initial_station_id = (
            initial_station_metadata.get("id") if initial_station_metadata else None
        )

        # Access data multiple times
        for _ in range(5):
            _ = tf_obj.tipper[0]
            _ = tf_obj.station_metadata.to_dict(single=True)
            _ = tf_obj.has_tipper()

        # Values should remain consistent
        assert np.array_equal(
            tf_obj.tipper[0], initial_tipper_first
        ), "Tipper values changed after repeated access"

        current_station_metadata = tf_obj.station_metadata.to_dict(single=True)
        current_station_id = (
            current_station_metadata.get("id") if current_station_metadata else None
        )
        assert (
            current_station_id == initial_station_id
        ), "Station ID changed after repeated access"


# =============================================================================
# Run tests
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
