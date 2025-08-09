# -*- coding: utf-8 -*-
"""
Pytest version of test_tf_read_complete_remote_info.py for EMTFXML remote reference TF functionality.

This modernized test suite provides:
- Comprehensive tests for EMTFXML remote reference processing with complete remote info
- Structure-based validation instead of brittle exact dictionary matching
- Parametrized tests for efficient coverage of transfer function components
- Module-scoped fixtures for performance optimization
- Flexible assertions that focus on data integrity rather than exact format
- Better error reporting and debugging capabilities

@author: GitHub Copilot
Created: 2025-08-09
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np
import pytest

from mt_metadata import TF_XML_COMPLETE_REMOTE_INFO
from mt_metadata.transfer_functions.core import TF


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def emtfxml_remote_tf():
    """Fixture to load the EMTFXML remote reference TF once per test module."""
    tf = TF(fn=TF_XML_COMPLETE_REMOTE_INFO)
    tf.read()
    return tf


# =============================================================================
# Test Classes
# =============================================================================


class TestEMTFXMLRemoteMetadata:
    """Test metadata components of EMTFXML remote reference transfer function."""

    def test_station_metadata_structure(self, emtfxml_remote_tf):
        """Test station metadata has expected structure and key values."""
        station_dict = emtfxml_remote_tf.station_metadata.to_dict(single=True)

        # Test key required fields exist
        assert "id" in station_dict
        assert "location.latitude" in station_dict
        assert "location.longitude" in station_dict
        assert "location.elevation" in station_dict
        assert "channels_recorded" in station_dict
        assert "run_list" in station_dict
        assert "transfer_function.id" in station_dict
        assert "transfer_function.processing_parameters" in station_dict
        assert "transfer_function.remote_references" in station_dict

        # Test key values for remote reference station
        assert station_dict["id"] == "GAA54"
        assert (
            station_dict["acquired_by.author"] == "National Geoelectromagnetic Facility"
        )
        assert station_dict["data_type"].upper() == "MT"
        assert isinstance(station_dict["location.latitude"], float)
        assert isinstance(station_dict["location.longitude"], float)
        assert isinstance(station_dict["location.elevation"], float)
        assert isinstance(station_dict["channels_recorded"], list)
        assert len(station_dict["channels_recorded"]) == 5
        assert set(station_dict["channels_recorded"]) == {"ex", "ey", "hx", "hy", "hz"}

        # Test remote reference specific fields
        assert isinstance(station_dict["transfer_function.processing_parameters"], list)
        assert len(station_dict["transfer_function.processing_parameters"]) > 0
        assert any(
            "remote_info" in param
            for param in station_dict["transfer_function.processing_parameters"]
        )
        assert "GAA53" in station_dict["transfer_function.remote_references"]

    def test_survey_metadata_structure(self, emtfxml_remote_tf):
        """Test survey metadata has expected structure and key values."""
        survey_dict = emtfxml_remote_tf.survey_metadata.to_dict(single=True)

        # Test key required fields exist
        assert "id" in survey_dict
        assert "project" in survey_dict
        assert "acquired_by.author" in survey_dict
        assert "citation_dataset.title" in survey_dict

        # Test key values for USArray project
        assert (
            survey_dict["acquired_by.author"] == "National Geoelectromagnetic Facility"
        )
        assert survey_dict["project"] == "USArray"
        assert "USArray" in survey_dict["citation_dataset.title"]
        assert "Transportable Array" in survey_dict["id"]

    def test_remote_processing_parameters(self, emtfxml_remote_tf):
        """Test that remote reference processing parameters contain expected remote info."""
        station_dict = emtfxml_remote_tf.station_metadata.to_dict(single=True)
        processing_params = station_dict["transfer_function.processing_parameters"]

        # Should have processing parameters with remote site info
        assert len(processing_params) > 20  # Expect comprehensive remote info

        # Test for specific remote site information
        remote_params = [p for p in processing_params if "remote_info" in p]
        assert len(remote_params) > 0

        # Check for key remote site parameters that actually exist in current structure
        param_strings = " ".join(processing_params)
        assert "remote_info.site.id = GAA53" in param_strings
        assert "remote_info.site.name = WHEATLEY FOREST, GA, USA" in param_strings
        assert "remote_info.site.project = USArray" in param_strings
        assert "remote_info.field_notes" in param_strings
        assert "remote_info.field_notes.instrument.id" in param_strings


class TestEMTFXMLRemoteRuns:
    """Test run metadata components of EMTFXML remote reference transfer function."""

    def test_runs_structure(self, emtfxml_remote_tf):
        """Test that runs have expected structure."""
        runs = emtfxml_remote_tf.station_metadata.runs

        # Should have exactly 1 run
        assert len(runs) == 1

        # Test run has expected structure
        run_dict = runs[0].to_dict(single=True)

        # Test key fields exist
        assert "id" in run_dict
        assert "data_type" in run_dict
        assert "sample_rate" in run_dict
        assert "channels_recorded_electric" in run_dict
        assert "channels_recorded_magnetic" in run_dict

        # Test values
        assert run_dict["id"] == "GAA54b"
        assert run_dict["data_type"] == "BBMT"
        assert run_dict["sample_rate"] == 1.0
        assert set(run_dict["channels_recorded_electric"]) == {"ex", "ey"}
        assert set(run_dict["channels_recorded_magnetic"]) == {"hx", "hy", "hz"}

    def test_run_time_periods(self, emtfxml_remote_tf):
        """Test that run has valid time periods."""
        run = emtfxml_remote_tf.station_metadata.runs[0]
        run_dict = run.to_dict(single=True)

        assert "time_period.start" in run_dict
        assert "time_period.end" in run_dict
        # Time periods should be non-empty strings with timezone info
        assert "+00:00" in run_dict["time_period.start"]
        assert "+00:00" in run_dict["time_period.end"]


class TestEMTFXMLRemoteTransferFunctions:
    """Test transfer function data arrays of EMTFXML remote reference."""

    def test_impedance_properties(self, emtfxml_remote_tf):
        """Test impedance tensor properties."""
        z = emtfxml_remote_tf.impedance

        # Test shape
        assert z.shape == (30, 2, 2)

        # Test first element - access via .data attribute
        expected_first = np.array(
            [
                [-0.3689028 - 0.04832953j, 2.904443 + 1.030588j],
                [-3.734557 - 2.555411j, 0.7417028 - 0.5187305j],
            ]
        )
        assert np.allclose(z[0].data, expected_first)

        # Test last element
        expected_last = np.array(
            [
                [-0.08651634 - 0.1364866j, 0.02648226 + 0.1238585j],
                [-0.2994978 - 0.4915415j, -0.01323366 + 0.08021657j],
            ]
        )
        assert np.allclose(z[-1].data, expected_last)

    def test_tipper_properties(self, emtfxml_remote_tf):
        """Test tipper tensor properties."""
        t = emtfxml_remote_tf.tipper

        # Test shape
        assert t.shape == (30, 1, 2)

        # Test first element
        expected_first = np.array([[-0.1511052 - 0.1205783j, 0.08954691 + 0.1148402j]])
        assert np.allclose(t[0].data, expected_first)

        # Test last element
        expected_last = np.array([[0.07471948 + 0.3349745j, 0.1931297 + 0.2555586j]])
        assert np.allclose(t[-1].data, expected_last)

    def test_inverse_signal_power_properties(self, emtfxml_remote_tf):
        """Test inverse signal power tensor properties."""
        sip = emtfxml_remote_tf.inverse_signal_power

        # Test shape
        assert sip.shape == (30, 2, 2)

        # Test first element
        expected_first = np.array(
            [
                [4.258637e-05 + 4.588496e-16j, 1.635847e-05 + 1.850000e-05j],
                [1.635847e-05 - 1.850000e-05j, 3.155363e-05 + 7.088115e-14j],
            ]
        )
        assert np.allclose(sip[0].data, expected_first)

        # Test last element
        expected_last = np.array(
            [
                [2.804339e-13 - 3.305735e-21j, 7.882486e-14 + 7.368000e-14j],
                [7.882486e-14 - 7.368000e-14j, 2.755661e-13 - 2.344265e-21j],
            ]
        )
        assert np.allclose(sip[-1].data, expected_last)

    def test_residual_covariance_properties(self, emtfxml_remote_tf):
        """Test residual covariance tensor properties."""
        res = emtfxml_remote_tf.residual_covariance

        # Test shape
        assert res.shape == (30, 3, 3)

        # Test first element
        expected_first = np.array(
            [
                [11996.37 + 0.000000e00j, 7413.954 + 1.642000e02j, 0.0 + 0.000000e00j],
                [7413.954 - 1.642000e02j, 72473.63 + 1.776357e-15j, 0.0 + 0.000000e00j],
                [0.0 + 0.000000e00j, 0.0 + 0.000000e00j, 1320.0 + 0.000000e00j],
            ]
        )
        assert np.allclose(res[0].data, expected_first)

        # Test last element
        expected_last = np.array(
            [
                [
                    3.956800e10 + 0.000000e00j,
                    -6.222869e09 + 5.282000e09j,
                    0.000000e00 + 0.000000e00j,
                ],
                [
                    -6.222869e09 - 5.282000e09j,
                    9.572996e09 + 5.960464e-08j,
                    0.000000e00 + 0.000000e00j,
                ],
                [
                    0.000000e00 + 0.000000e00j,
                    0.000000e00 + 0.000000e00j,
                    2.304000e10 + 0.000000e00j,
                ],
            ]
        )
        assert np.allclose(res[-1].data, expected_last)


class TestEMTFXMLRemoteComprehensive:
    """Comprehensive integration tests for EMTFXML remote reference functionality."""

    def test_tf_loading_integration(self, emtfxml_remote_tf):
        """Test that remote reference TF loads correctly and has expected structure."""
        # Test that TF object exists and has expected attributes
        assert hasattr(emtfxml_remote_tf, "station_metadata")
        assert hasattr(emtfxml_remote_tf, "survey_metadata")
        assert hasattr(emtfxml_remote_tf, "impedance")
        assert hasattr(emtfxml_remote_tf, "inverse_signal_power")
        assert hasattr(emtfxml_remote_tf, "residual_covariance")
        assert hasattr(emtfxml_remote_tf, "tipper")

    def test_station_runs_structure(self, emtfxml_remote_tf):
        """Test that station has correct run structure."""
        # Should have 1 run
        assert len(emtfxml_remote_tf.station_metadata.runs) == 1

    @pytest.mark.parametrize(
        "tf_component,expected_shape",
        [
            ("impedance", (30, 2, 2)),
            ("inverse_signal_power", (30, 2, 2)),
            ("residual_covariance", (30, 3, 3)),
            ("tipper", (30, 1, 2)),
        ],
    )
    def test_transfer_function_shapes(
        self, emtfxml_remote_tf, tf_component, expected_shape
    ):
        """Test that all transfer function components have expected shapes."""
        component = getattr(emtfxml_remote_tf, tf_component)
        assert component.shape == expected_shape

    def test_data_consistency(self, emtfxml_remote_tf):
        """Test data consistency across components."""
        # All transfer function components should have same frequency dimension
        n_freqs = emtfxml_remote_tf.impedance.shape[0]
        assert emtfxml_remote_tf.inverse_signal_power.shape[0] == n_freqs
        assert emtfxml_remote_tf.residual_covariance.shape[0] == n_freqs
        assert emtfxml_remote_tf.tipper.shape[0] == n_freqs

        # Check that we have expected number of frequencies for this dataset
        assert n_freqs == 30

    def test_remote_reference_processing(self, emtfxml_remote_tf):
        """Test remote reference specific processing characteristics."""
        station_dict = emtfxml_remote_tf.station_metadata.to_dict(single=True)

        # Should be remote reference processing
        assert (
            station_dict["transfer_function.processing_type"]
            == "Robust Remote Reference"
        )

        # Should have remote references
        assert len(station_dict["transfer_function.remote_references"]) > 0
        assert "GAA53" in station_dict["transfer_function.remote_references"]

        # Should have comprehensive remote info in processing parameters
        assert len(station_dict["transfer_function.processing_parameters"]) > 20

    def test_data_quality_metrics(self, emtfxml_remote_tf):
        """Test data quality metrics are properly loaded."""
        station_dict = emtfxml_remote_tf.station_metadata.to_dict(single=True)

        # Should have data quality information
        assert "transfer_function.data_quality.good_from_period" in station_dict
        assert "transfer_function.data_quality.good_to_period" in station_dict
        assert "transfer_function.data_quality.rating.value" in station_dict

        # Validate data quality values are reasonable
        assert station_dict["transfer_function.data_quality.good_from_period"] == 10.0
        assert station_dict["transfer_function.data_quality.good_to_period"] == 10000.0
        assert station_dict["transfer_function.data_quality.rating.value"] == 5
