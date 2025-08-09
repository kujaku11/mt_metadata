# -*- coding: utf-8 -*-
"""
Comprehensive pytest suite for EMTFXML derived quantities testing.

Created on Sat Dec  4 17:03:51 2021
@author: jpeacock

Converted to pytest suite for enhanced testing with fixtures and parametrization.
Tests EMTFXML functionality with derived quantities data from South Chile.
"""


import numpy as np

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_XML_WITH_DERIVED_QUANTITIES
from mt_metadata.transfer_functions.core import TF


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def tf_derived_quantities():
    """Load transfer function with derived quantities for testing."""
    tf = TF(fn=TF_XML_WITH_DERIVED_QUANTITIES)
    tf.read()
    return tf


# =============================================================================
# Test Classes
# =============================================================================
class TestEMTFXMLDerivedMetadata:
    """Test metadata structure for EMTFXML with derived quantities."""

    def test_station_basic_info(self, tf_derived_quantities):
        """Test basic station information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["id"] == "SMG1"
        assert station_dict["geographic_name"] == "South Chile"
        assert station_dict["acquired_by.author"] == "Freie Universitaet Berlin"
        assert station_dict["data_type"] == "MT"
        assert station_dict["fdsn.id"] == "FU-BERLIN.SMG1.2003"

    def test_station_location(self, tf_derived_quantities):
        """Test station location parameters."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["location.latitude"] == -38.41
        assert station_dict["location.longitude"] == -73.904722
        assert station_dict["location.elevation"] == 10.0
        assert station_dict["location.datum"] == "WGS 84"
        assert station_dict["location.declination.model"] == "IGRF"
        assert station_dict["location.declination.value"] == 0.0

    def test_station_channels(self, tf_derived_quantities):
        """Test recorded channels information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        expected_channels = ["ex", "ey", "hx", "hy", "hz"]
        assert station_dict["channels_recorded"] == expected_channels

    def test_station_orientation(self, tf_derived_quantities):
        """Test station orientation parameters."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["orientation.angle_to_geographic_north"] == 0.0
        assert station_dict["orientation.reference_frame"] == "geographic"
        assert station_dict["orientation.method"] == "compass"

    def test_station_provenance(self, tf_derived_quantities):
        """Test station provenance information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["provenance.creator.author"] == "Heinrich Brasse"
        assert (
            station_dict["provenance.creator.email"] == "heinrich.brasse@fu-berlin.de"
        )
        assert station_dict["provenance.creation_time"] == "2020-06-05T12:06:27+00:00"

        # Note: organization fields not present in current data structure

    def test_station_submitter_info(self, tf_derived_quantities):
        """Test submitter information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["provenance.submitter.author"] == "Anna Kelbert"
        assert station_dict["provenance.submitter.email"] == "akelbert@usgs.gov"

        # Note: organization and URL fields not present in current data structure

    def test_station_transfer_function_info(self, tf_derived_quantities):
        """Test transfer function metadata."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["transfer_function.id"] == "SMG1"
        assert (
            station_dict["transfer_function.processed_by.author"] == "Heinrich Brasse"
        )
        assert station_dict["transfer_function.sign_convention"] == "exp(+ i\\omega t)"
        assert station_dict["transfer_function.coordinate_system"] == "geographic"
        assert station_dict["transfer_function.data_quality.rating.value"] == 0

    def test_station_software_info(self, tf_derived_quantities):
        """Test software information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert (
            station_dict["provenance.software.name"]
            == "EMTF File Conversion Utilities 4.0"
        )
        assert station_dict["transfer_function.software.author"] == "Randie Mackie"
        assert station_dict["transfer_function.software.name"] == "WINGLINK EDI 1.0.22"
        assert (
            station_dict["transfer_function.software.last_updated"]
            == "2002-04-23T00:00:00+00:00"
        )

    def test_station_time_period(self, tf_derived_quantities):
        """Test time period information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        assert station_dict["time_period.start"] == "2003-01-02T00:00:00+00:00"
        assert station_dict["time_period.end"] == "2003-01-02T00:00:00+00:00"
        assert station_dict["run_list"] == ["SMG1a"]


class TestEMTFXMLDerivedSurvey:
    """Test survey metadata for EMTFXML with derived quantities."""

    def test_survey_basic_info(self, tf_derived_quantities):
        """Test basic survey information."""
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        assert survey_dict["id"] == "South Chile"
        assert survey_dict["geographic_name"] == "South Chile"
        assert survey_dict["project"] == "FU-BERLIN"
        assert survey_dict["acquired_by.author"] == "Freie Universitaet Berlin"
        assert survey_dict["summary"] == "Magnetotelluric Transfer Functions"

    def test_survey_citation(self, tf_derived_quantities):
        """Test survey citation information."""
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        assert survey_dict["citation_dataset.authors"] == "Heinrich Brasse"
        assert (
            survey_dict["citation_dataset.doi"]
            == "https://doi.org/10.17611/DP/EMTF/FU-BERLIN/SOUTHCHILE"
        )
        assert (
            survey_dict["citation_dataset.title"]
            == "Magnetotelluric Transfer Functions in South Chile by Freie Universitaet, Berlin"
        )
        assert survey_dict["citation_dataset.year"] == "2003-2005"

    def test_survey_geographic_bounds(self, tf_derived_quantities):
        """Test survey geographic boundaries."""
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        assert survey_dict["northwest_corner.latitude"] == -38.41
        assert survey_dict["northwest_corner.longitude"] == -73.904722
        assert survey_dict["southeast_corner.latitude"] == -38.41
        assert survey_dict["southeast_corner.longitude"] == -73.904722
        assert survey_dict["datum"] == "WGS 84"
        assert survey_dict["country"] == ["Chile"]

    def test_survey_time_period(self, tf_derived_quantities):
        """Test survey time period."""
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        assert survey_dict["time_period.start_date"] == "2003-01-02"
        assert survey_dict["time_period.end_date"] == "2003-01-02"

    def test_survey_licensing(self, tf_derived_quantities):
        """Test survey licensing information."""
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        assert survey_dict["release_license"] == "CC-BY-4.0"

        # Note: project_lead fields not present in current data structure

    def test_survey_comments_structure(self, tf_derived_quantities):
        """Test that comments field is properly structured."""
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        comments = survey_dict["comments"]
        assert isinstance(comments, str)
        assert len(comments) > 0
        # Check for key copyright and publication information
        assert "copyright.conditions_of_use:" in comments
        assert "ReleaseStatusEnum.Paper_Citation_Required" in comments
        assert "Brasse, H." in comments  # Publication reference


class TestEMTFXMLDerivedRuns:
    """Test run metadata for EMTFXML with derived quantities."""

    def test_run_basic_info(self, tf_derived_quantities):
        """Test basic run information."""
        run_dict = tf_derived_quantities.station_metadata.runs[0].to_dict(single=True)

        assert run_dict["id"] == "SMG1a"
        assert run_dict["data_type"] == "BBMT"
        assert run_dict["sample_rate"] == 0.0

    def test_run_channels(self, tf_derived_quantities):
        """Test run channel configuration."""
        run_dict = tf_derived_quantities.station_metadata.runs[0].to_dict(single=True)

        assert run_dict["channels_recorded_electric"] == ["ex", "ey"]
        assert run_dict["channels_recorded_magnetic"] == ["hx", "hy", "hz"]
        assert run_dict["channels_recorded_auxiliary"] == []

    def test_run_data_logger(self, tf_derived_quantities):
        """Test data logger information."""
        run_dict = tf_derived_quantities.station_metadata.runs[0].to_dict(single=True)

        assert run_dict["data_logger.timing_system.type"] == "GPS"
        assert run_dict["data_logger.timing_system.drift"] == 0.0
        assert run_dict["data_logger.timing_system.uncertainty"] == 0.0

        # Test power source fields (present in current structure)
        assert run_dict["data_logger.power_source.voltage.start"] == 0.0
        assert run_dict["data_logger.power_source.voltage.end"] == 0.0

    def test_run_firmware(self, tf_derived_quantities):
        """Test firmware information."""
        run_dict = tf_derived_quantities.station_metadata.runs[0].to_dict(single=True)

        assert run_dict["data_logger.firmware.author"] == ""
        assert run_dict["data_logger.firmware.name"] == ""
        assert run_dict["data_logger.firmware.version"] == ""

    def test_run_time_period(self, tf_derived_quantities):
        """Test run time period (default values)."""
        run_dict = tf_derived_quantities.station_metadata.runs[0].to_dict(single=True)

        assert run_dict["time_period.start"] == "1980-01-01T00:00:00+00:00"
        assert run_dict["time_period.end"] == "1980-01-01T00:00:00+00:00"


class TestEMTFXMLDerivedTransferFunctions:
    """Test transfer function data for EMTFXML with derived quantities."""

    def test_impedance_shape(self, tf_derived_quantities):
        """Test impedance tensor shape."""
        assert tf_derived_quantities.impedance.shape == (20, 2, 2)

    @pytest.mark.parametrize(
        "index,expected",
        [
            (
                0,
                np.array(
                    [
                        [-8.089973e-03 - 0.04293998j, 9.217000e-01 + 0.3741j],
                        [-6.215000e-01 - 0.4342j, -4.668272e-04 - 0.00064572j],
                    ]
                ),
            ),
            (
                -1,
                np.array(
                    [
                        [7.610000e-02 + 0.06188j, 1.069000e-01 + 0.1594j],
                        [-6.638000e-02 - 0.05362j, -4.141902e-06 + 0.004022j],
                    ]
                ),
            ),
        ],
    )
    def test_impedance_values(self, tf_derived_quantities, index, expected):
        """Test specific impedance tensor values."""
        actual = tf_derived_quantities.impedance[index].data
        np.testing.assert_allclose(actual, expected, rtol=1e-5)

    def test_impedance_first_element(self, tf_derived_quantities):
        """Test first impedance element (alternative validation)."""
        first_z = tf_derived_quantities.impedance[0].data
        assert first_z.shape == (2, 2)
        assert np.isclose(first_z[0, 0], -8.089973e-03 - 0.04293998j)
        assert np.isclose(first_z[0, 1], 9.217000e-01 + 0.3741j)
        assert np.isclose(first_z[1, 0], -6.215000e-01 - 0.4342j)
        assert np.isclose(first_z[1, 1], -4.668272e-04 - 0.00064572j)

    def test_impedance_last_element(self, tf_derived_quantities):
        """Test last impedance element (alternative validation)."""
        last_z = tf_derived_quantities.impedance[-1].data
        assert last_z.shape == (2, 2)
        assert np.isclose(last_z[0, 0], 7.610000e-02 + 0.06188j)
        assert np.isclose(last_z[0, 1], 1.069000e-01 + 0.1594j)
        assert np.isclose(last_z[1, 0], -6.638000e-02 - 0.05362j)
        assert np.isclose(last_z[1, 1], -4.141902e-06 + 0.004022j)

    def test_tipper_shape(self, tf_derived_quantities):
        """Test tipper shape."""
        assert tf_derived_quantities.tipper.shape == (20, 1, 2)

    @pytest.mark.parametrize(
        "index,expected",
        [
            (0, np.array([[0.06982 + 0.01516j, -0.1876 + 0.0135j]])),
            (-1, np.array([[1.0e32 + 1.0e32j, 1.0e32 + 1.0e32j]])),
        ],
    )
    def test_tipper_values(self, tf_derived_quantities, index, expected):
        """Test specific tipper values."""
        actual = tf_derived_quantities.tipper[index].data
        np.testing.assert_allclose(actual, expected, rtol=1e-7)

    def test_tipper_first_element(self, tf_derived_quantities):
        """Test first tipper element (alternative validation)."""
        first_t = tf_derived_quantities.tipper[0].data
        assert first_t.shape == (1, 2)
        assert np.isclose(first_t[0, 0], 0.06982 + 0.01516j)
        assert np.isclose(first_t[0, 1], -0.1876 + 0.0135j)

    def test_tipper_last_element_special(self, tf_derived_quantities):
        """Test last tipper element (special high values)."""
        last_t = tf_derived_quantities.tipper[-1].data
        assert last_t.shape == (1, 2)
        # These are special high values indicating no data
        assert np.isclose(last_t[0, 0], 1.0e32 + 1.0e32j)
        assert np.isclose(last_t[0, 1], 1.0e32 + 1.0e32j)


class TestEMTFXMLDerivedComprehensive:
    """Comprehensive tests for EMTFXML derived quantities functionality."""

    def test_data_consistency(self, tf_derived_quantities):
        """Test consistency between impedance and tipper data."""
        # Both should have same number of frequency points
        assert (
            tf_derived_quantities.impedance.shape[0]
            == tf_derived_quantities.tipper.shape[0]
        )
        assert tf_derived_quantities.impedance.shape[0] == 20

    def test_impedance_data_types(self, tf_derived_quantities):
        """Test that impedance data are complex numbers."""
        z_data = tf_derived_quantities.impedance[0].data
        assert np.iscomplexobj(z_data)
        assert z_data.dtype == complex

    def test_tipper_data_types(self, tf_derived_quantities):
        """Test that tipper data are complex numbers."""
        t_data = tf_derived_quantities.tipper[0].data
        assert np.iscomplexobj(t_data)
        assert t_data.dtype == complex

    def test_non_empty_data_validation(self, tf_derived_quantities):
        """Test that key data fields are not empty."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        # Essential fields should not be None or empty
        essential_fields = [
            "id",
            "geographic_name",
            "acquired_by.author",
            "location.latitude",
            "location.longitude",
            "channels_recorded",
        ]

        for field in essential_fields:
            assert field in station_dict
            assert station_dict[field] is not None
            if isinstance(station_dict[field], (list, str)):
                assert len(station_dict[field]) > 0

    def test_derived_quantities_presence(self, tf_derived_quantities):
        """Test that derived quantities are properly loaded."""
        # Both impedance and tipper should be available
        assert hasattr(tf_derived_quantities, "impedance")
        assert hasattr(tf_derived_quantities, "tipper")

        # Check that they contain data
        assert tf_derived_quantities.impedance is not None
        assert tf_derived_quantities.tipper is not None

        # Check data access
        assert hasattr(tf_derived_quantities.impedance[0], "data")
        assert hasattr(tf_derived_quantities.tipper[0], "data")

    def test_transfer_function_processing_info(self, tf_derived_quantities):
        """Test transfer function processing information."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)

        # Processing information should be present but may be empty for this dataset
        assert "transfer_function.processing_parameters" in station_dict
        assert "transfer_function.processing_type" in station_dict
        assert "transfer_function.remote_references" in station_dict
        assert "transfer_function.runs_processed" in station_dict

        # These should be lists (even if empty)
        assert isinstance(station_dict["transfer_function.processing_parameters"], list)
        assert isinstance(station_dict["transfer_function.remote_references"], list)
        assert isinstance(station_dict["transfer_function.runs_processed"], list)


# =============================================================================
# Integration Tests
# =============================================================================
class TestEMTFXMLDerivedIntegration:
    """Integration tests for the complete EMTFXML derived quantities workflow."""

    def test_complete_metadata_structure(self, tf_derived_quantities):
        """Test that all major metadata components are present and accessible."""
        # Station metadata
        assert hasattr(tf_derived_quantities, "station_metadata")
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)
        assert len(station_dict) > 0

        # Survey metadata
        assert hasattr(tf_derived_quantities, "survey_metadata")
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)
        assert len(survey_dict) > 0

        # Run metadata
        assert len(tf_derived_quantities.station_metadata.runs) == 1
        run_dict = tf_derived_quantities.station_metadata.runs[0].to_dict(single=True)
        assert len(run_dict) > 0

    def test_south_chile_specific_validation(self, tf_derived_quantities):
        """Test South Chile specific data validation."""
        station_dict = tf_derived_quantities.station_metadata.to_dict(single=True)
        survey_dict = tf_derived_quantities.survey_metadata.to_dict(single=True)

        # Location should be in Chile
        assert station_dict["location.latitude"] < 0  # Southern hemisphere
        assert station_dict["location.longitude"] < 0  # Western hemisphere
        assert survey_dict["country"] == ["Chile"]

        # Should be from Freie Universitaet Berlin
        assert "Berlin" in station_dict["acquired_by.author"]

        # Project identification
        assert survey_dict["project"] == "FU-BERLIN"
        assert station_dict["fdsn.id"].startswith("FU-BERLIN")

    def test_derived_quantities_data_integrity(self, tf_derived_quantities):
        """Test data integrity of derived quantities."""
        # Check that impedance tensor has reasonable values (not all zeros or infinities)
        z_data = tf_derived_quantities.impedance[5].data  # Use middle frequency
        assert not np.all(z_data == 0)
        assert np.all(np.isfinite(z_data))

        # Check that tipper has reasonable values for most frequencies
        # (last element has special high values indicating no data)
        t_data = tf_derived_quantities.tipper[5].data  # Use middle frequency
        assert not np.all(t_data == 0)
        assert np.all(np.isfinite(t_data))

        # Verify that some tipper values are reasonable (not the 1e32 no-data markers)
        assert np.all(np.abs(t_data) < 1e10)


if __name__ == "__main__":
    pytest.main([__file__])
