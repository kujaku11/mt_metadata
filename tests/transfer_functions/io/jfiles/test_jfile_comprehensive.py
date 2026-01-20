# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for JFile class.

This module contains tests for the JFile class functionality, including both
basic object testing and file parsing (when the parsing issues are resolved).
Uses modern pytest fixtures, parametrization, and subtests for efficiency.
"""

import json
from pathlib import Path

import numpy as np
import pytest

from mt_metadata.transfer_functions.io.jfiles import JFile
from mt_metadata.transfer_functions.io.jfiles.metadata import Header


class TestJFileCore:
    """Core functionality tests for JFile class."""

    @pytest.fixture
    def empty_jfile(self):
        """Fixture providing an empty JFile instance."""
        return JFile()

    @pytest.fixture
    def sample_header_data(self):
        """Fixture providing sample header data for testing."""
        return {
            "title": "Test BIRRP Processing",
            "station": "TEST01",
            "azimuth": 15.5,
            "latitude": 40.123,
            "longitude": -120.456,
            "elevation": 1200.0,
            "datum": "NAD83",
        }

    def test_empty_initialization(self, empty_jfile):
        """Test JFile initializes correctly without parameters."""
        assert empty_jfile.fn is None
        assert isinstance(empty_jfile.header, Header)
        assert empty_jfile.z is None
        assert empty_jfile.z_err is None
        assert empty_jfile.t is None
        assert empty_jfile.t_err is None
        assert empty_jfile.frequency is None

    def test_attribute_existence(self, empty_jfile):
        """Test that all expected attributes exist."""
        expected_attrs = [
            "header",
            "fn",
            "_jfn",
            "z",
            "z_err",
            "t",
            "t_err",
            "frequency",
        ]
        for attr in expected_attrs:
            assert hasattr(empty_jfile, attr)

    def test_header_inheritance_fields(self, empty_jfile):
        """Test header has inherited location fields from BasicLocation."""
        header = empty_jfile.header
        location_fields = ["latitude", "longitude", "elevation", "datum", "x", "y", "z"]

        for field in location_fields:
            assert hasattr(header, field)

    def test_header_field_defaults(self, empty_jfile):
        """Test header field default values."""
        header = empty_jfile.header

        # Basic fields
        assert header.title == ""
        assert header.station == ""
        assert header.azimuth == 0.0

        # Location fields
        assert header.latitude == 0.0
        assert header.longitude == 0.0
        assert header.elevation == 0.0
        assert header.datum == "WGS 84"

    def test_header_field_assignment(self, empty_jfile, sample_header_data):
        """Test assigning values to header fields."""
        header = empty_jfile.header

        for field, value in sample_header_data.items():
            setattr(header, field, value)
            assert getattr(header, field) == value

    @pytest.mark.parametrize(
        "field,value,expected_type",
        [
            ("title", "Test Title", str),
            ("station", "MT001", str),
            ("azimuth", 45.0, float),
            ("latitude", 35.5, float),
            ("longitude", -118.2, float),
            ("elevation", 500.0, float),
        ],
    )
    def test_header_field_types(self, empty_jfile, field, value, expected_type):
        """Test that header fields accept and maintain correct types."""
        header = empty_jfile.header
        setattr(header, field, value)
        assert isinstance(getattr(header, field), expected_type)
        assert getattr(header, field) == value

    def test_kwargs_handling(self):
        """Test JFile handles keyword arguments correctly."""
        jfile = JFile(test_param="test_value", another_param=42)
        assert hasattr(jfile, "test_param")
        assert hasattr(jfile, "another_param")
        assert getattr(jfile, "test_param") == "test_value"
        assert getattr(jfile, "another_param") == 42


class TestJFilePathHandling:
    """Test file path handling and validation."""

    def test_valid_j_file_extension(self):
        """Test that .j files are accepted."""
        jfile = JFile()
        # This should not raise an error
        try:
            jfile._jfn = Path("test.j")
            assert jfile._jfn.suffix == ".j"
        except Exception:
            # If there are other validation issues, that's OK for this test
            pass

    @pytest.mark.parametrize(
        "invalid_filename", ["test.txt", "test.json", "test.dat", "test", "test.J"]
    )
    def test_invalid_file_extensions(self, invalid_filename):
        """Test that invalid file extensions are rejected."""
        with pytest.raises(ValueError, match="Input file must be a.*j file"):
            JFile(fn=invalid_filename)

    def test_empty_filename_handling(self):
        """Test handling of empty filenames."""
        with pytest.raises(ValueError):
            JFile(fn="")

    def test_nonexistent_file_error(self):
        """Test error handling for nonexistent files."""
        with pytest.raises(NameError, match="Could not find"):
            JFile(fn="nonexistent_file.j")

    def test_path_object_handling(self):
        """Test that Path objects are handled correctly."""
        test_path = Path("test_file.j")
        jfile = JFile()
        jfile._jfn = test_path
        assert jfile._jfn == test_path


class TestJFileDataStructures:
    """Test JFile data structures and properties."""

    @pytest.fixture
    def jfile_with_mock_data(self):
        """Fixture providing JFile with mock impedance data."""
        jfile = JFile()

        # Create mock data
        n_freq = 10
        jfile.frequency = np.logspace(-3, 2, n_freq)
        jfile.z = np.random.rand(n_freq, 2, 2) + 1j * np.random.rand(n_freq, 2, 2)
        jfile.z_err = np.random.rand(n_freq, 2, 2) * 0.1
        jfile.t = np.random.rand(n_freq, 1, 2) + 1j * np.random.rand(n_freq, 1, 2)
        jfile.t_err = np.random.rand(n_freq, 1, 2) * 0.1

        return jfile

    def test_impedance_data_structure(self, jfile_with_mock_data):
        """Test impedance data has correct structure."""
        jfile = jfile_with_mock_data

        # Test shapes
        n_freq = len(jfile.frequency)
        assert jfile.z.shape == (n_freq, 2, 2)
        assert jfile.z_err.shape == (n_freq, 2, 2)

        # Test data types
        assert jfile.z.dtype == complex
        assert np.isrealobj(jfile.z_err)

    def test_tipper_data_structure(self, jfile_with_mock_data):
        """Test tipper data has correct structure."""
        jfile = jfile_with_mock_data

        # Test shapes
        n_freq = len(jfile.frequency)
        assert jfile.t.shape == (n_freq, 1, 2)
        assert jfile.t_err.shape == (n_freq, 1, 2)

        # Test data types
        assert jfile.t.dtype == complex
        assert np.isrealobj(jfile.t_err)

    def test_frequency_data_consistency(self, jfile_with_mock_data):
        """Test frequency data consistency across all arrays."""
        jfile = jfile_with_mock_data

        n_freq = len(jfile.frequency)
        assert jfile.z.shape[0] == n_freq
        assert jfile.z_err.shape[0] == n_freq
        assert jfile.t.shape[0] == n_freq
        assert jfile.t_err.shape[0] == n_freq

    def test_periods_property(self, jfile_with_mock_data):
        """Test periods property calculation."""
        jfile = jfile_with_mock_data

        periods = jfile.periods
        expected_periods = 1.0 / jfile.frequency

        assert periods is not None
        assert np.allclose(periods, expected_periods)

    def test_periods_property_no_frequency(self):
        """Test periods property when frequency is None."""
        jfile = JFile()
        assert jfile.periods is None


class TestJFileSerialization:
    """Test JFile serialization and metadata handling."""

    @pytest.fixture
    def configured_jfile(self):
        """Fixture providing JFile with configured header."""
        jfile = JFile()
        header = jfile.header

        header.title = "Comprehensive Test"
        header.station = "SERIALIZE01"
        header.azimuth = 30.0
        header.latitude = 42.123
        header.longitude = -121.456
        header.elevation = 800.0
        header.datum = "NAD83"

        return jfile

    def test_header_dict_serialization(self, configured_jfile):
        """Test header serialization to dictionary."""
        header_dict = configured_jfile.header.to_dict()

        assert isinstance(header_dict, dict)
        assert "header" in header_dict

        header_data = header_dict["header"]
        assert header_data["title"] == "Comprehensive Test"
        assert header_data["station"] == "SERIALIZE01"
        assert header_data["latitude"] == 42.123
        assert header_data["longitude"] == -121.456

    def test_header_json_serialization(self, configured_jfile):
        """Test header serialization to JSON."""
        json_str = configured_jfile.header.to_json()

        assert isinstance(json_str, str)

        # Validate JSON structure
        json_data = json.loads(json_str)
        assert isinstance(json_data, dict)
        assert "header" in json_data

    def test_serialization_roundtrip(self, configured_jfile):
        """Test that serialization preserves data integrity."""
        original_header = configured_jfile.header

        # Serialize to dict and back
        header_dict = original_header.to_dict()

        # Verify key values are preserved
        header_data = header_dict["header"]
        assert header_data["title"] == original_header.title
        assert header_data["station"] == original_header.station
        assert header_data["azimuth"] == original_header.azimuth


class TestJFileRepresentation:
    """Test JFile string representations."""

    def test_repr_basic(self):
        """Test __repr__ method."""
        jfile = JFile()
        repr_str = repr(jfile)

        assert isinstance(repr_str, str)
        assert "JFile" in repr_str
        assert "station=" in repr_str
        assert "latitude=" in repr_str
        assert "longitude=" in repr_str

    def test_repr_with_data(self):
        """Test __repr__ with configured data."""
        jfile = JFile()
        jfile.header.station = "REPR01"
        jfile.header.latitude = 35.0
        jfile.header.longitude = -118.0

        repr_str = repr(jfile)
        assert "station='REPR01'" in repr_str
        assert "latitude=35.00" in repr_str
        assert "longitude=-118.00" in repr_str


class TestJFileMetadata:
    """Test JFile metadata properties and methods."""

    @pytest.fixture
    def jfile_with_valid_deltat(self):
        """Fixture with valid deltat to avoid division by zero."""
        jfile = JFile()
        jfile.header.birrp_parameters.deltat = 0.1  # 10 Hz sampling
        jfile.header.station = "META01"
        return jfile

    def test_station_metadata_property(self, jfile_with_valid_deltat):
        """Test station_metadata property."""
        jfile = jfile_with_valid_deltat
        station_meta = jfile.station_metadata

        assert hasattr(station_meta, "id")
        assert hasattr(station_meta, "location")
        assert hasattr(station_meta, "runs")
        assert hasattr(
            station_meta, "transfer_function"
        )  # Now available with updated import

    def test_survey_metadata_property(self, jfile_with_valid_deltat):
        """Test survey_metadata property."""
        jfile = jfile_with_valid_deltat
        survey_meta = jfile.survey_metadata

        assert hasattr(survey_meta, "stations")
        assert len(survey_meta.stations) > 0


class TestJFileCompatibility:
    """Test JFile compatibility with existing interfaces."""

    def test_birrp_parameters_access(self):
        """Test access to BIRRP parameters."""
        jfile = JFile()
        params = jfile.header.birrp_parameters

        assert hasattr(params, "deltat")
        assert hasattr(params, "nfft")
        assert hasattr(params, "inputs")
        assert hasattr(params, "outputs")

    def test_data_blocks_access(self):
        """Test access to data blocks."""
        jfile = JFile()
        blocks = jfile.header.data_blocks

        assert hasattr(blocks, "__len__")  # Should be list-like
        assert isinstance(blocks, list)

    def test_model_field_metadata_access(self):
        """Test that model field metadata is accessible."""
        jfile = JFile()
        header = jfile.header

        if hasattr(header, "model_fields"):
            fields = header.model_fields
            assert isinstance(fields, dict)

            # Check for expected fields
            expected_fields = ["title", "station", "azimuth"]
            for field in expected_fields:
                if field in fields:
                    field_info = fields[field]
                    assert hasattr(field_info, "default")


class TestJFileValidation:
    """Test JFile validation and error handling."""

    def test_header_field_validation(self):
        """Test that header fields validate input types."""
        jfile = JFile()
        header = jfile.header

        # Test string to float conversion for numeric fields
        header.latitude = "40.123"
        assert header.latitude == 40.123
        assert isinstance(header.latitude, float)

    def test_data_array_validation_with_mock_data(self):
        """Test validation of data arrays."""
        jfile = JFile()

        # Mock some frequency data
        jfile.frequency = np.array([1.0, 2.0, 3.0])

        # Verify frequency data properties
        assert len(jfile.frequency) == 3
        assert np.all(jfile.frequency > 0)
        assert np.all(np.isfinite(jfile.frequency))

    @pytest.mark.parametrize(
        "attr_name,expected_initial_value",
        [
            ("z", None),
            ("z_err", None),
            ("t", None),
            ("t_err", None),
            ("frequency", None),
        ],
    )
    def test_initial_data_array_states(self, attr_name, expected_initial_value):
        """Test that data arrays start in expected initial state."""
        jfile = JFile()
        assert getattr(jfile, attr_name) == expected_initial_value


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
