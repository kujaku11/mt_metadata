# -*- coding: utf-8 -*-
"""
Pytest test suite for JFile class.

This module contains comprehensive tests for the JFile class functionality,
including header parsing, BIRRP parameters, data blocks, and impedance data.
"""

import json
from collections import OrderedDict
from pathlib import Path

import numpy as np
import pytest

from mt_metadata import TF_JFILE
from mt_metadata.transfer_functions.io.jfiles import JFile


class TestJFile:
    """Test suite for JFile class with pytest fixtures and subtests."""

    @pytest.fixture(scope="class")
    def jfile_obj(self):
        """Fixture to create a JFile object from test data."""
        return JFile(fn=TF_JFILE)

    @pytest.fixture(scope="class")
    def expected_birrp_params(self):
        """Fixture containing expected BIRRP parameters for validation."""
        return OrderedDict(
            [
                ("ainlin", -999.0),
                ("ainuin", 0.999),
                ("c2threshe", 0.7),
                ("c2threshe1", 0.0),
                ("deltat", 0.1),
                ("imode", 2),
                ("inputs", 2),
                ("jmode", 0),
                ("nar", 3),
                ("ncomp", None),
                ("nf1", 4),
                ("nfft", 5164.0),
                ("nfinc", 2),
                ("nfsect", 2),
                ("npcs", 1),
                ("nsctinc", 2.0),
                ("nsctmax", 7.0),
                ("nz", 0),
                ("outputs", 2),
                ("references", 2),
                ("tbw", 2.0),
                ("uin", 0.0),
            ]
        )

    @pytest.fixture(scope="class")
    def expected_data_blocks(self):
        """Fixture containing expected data blocks for validation."""
        return [
            OrderedDict(
                [
                    (
                        "filnam",
                        "/data/mtpy/examples/birrp_processing/birrp_wd/birrp_data_3.txt",
                    ),
                    ("indices", [1]),
                    ("ncomp", 4),
                    ("nread", 38750),
                    ("nskip", 0),
                ]
            ),
            OrderedDict(
                [
                    (
                        "filnam",
                        "/data/mtpy/examples/birrp_processing/birrp_wd/birrp_data_3.txt",
                    ),
                    ("indices", [3]),
                    ("ncomp", 4),
                    ("nread", 38750),
                    ("nskip", 0),
                ]
            ),
        ]

    def test_jfile_initialization_from_file(self, jfile_obj):
        """Test that JFile initializes properly from a file."""
        assert jfile_obj.fn is not None
        assert jfile_obj.header is not None
        assert jfile_obj.z is not None
        assert jfile_obj.z_err is not None

    def test_jfile_initialization_empty(self):
        """Test that JFile initializes properly without a file."""
        jfile = JFile()
        assert jfile.fn is None
        assert jfile.header is not None
        assert jfile.z is None
        assert jfile.z_err is None

    def test_header_title(self, jfile_obj):
        """Test that header title is parsed correctly."""
        expected_title = "BIRRP Version 5 basic mode output"
        assert jfile_obj.header.title == expected_title

    def test_header_station(self, jfile_obj):
        """Test that header station is parsed correctly."""
        expected_station = "BP05"
        assert jfile_obj.header.station == expected_station

    def test_header_azimuth(self, jfile_obj):
        """Test that header azimuth is parsed correctly."""
        # Based on the j-file data, azimuth should be 0.0
        assert jfile_obj.header.azimuth == 0.0

    def test_birrp_parameters_complete(self, jfile_obj, expected_birrp_params):
        """Test that all BIRRP parameters are parsed correctly."""
        actual_params = jfile_obj.header.birrp_parameters.to_dict(single=True)
        assert actual_params == expected_birrp_params

    @pytest.mark.parametrize(
        "param_name,expected_value",
        [
            ("ainlin", -999.0),
            ("ainuin", 0.999),
            ("c2threshe", 0.7),
            ("deltat", 0.1),
            ("imode", 2),
            ("inputs", 2),
            ("outputs", 2),
            ("references", 2),
        ],
    )
    def test_birrp_parameters_individual(self, jfile_obj, param_name, expected_value):
        """Test individual BIRRP parameters using parametrization."""
        actual_value = getattr(jfile_obj.header.birrp_parameters, param_name)
        assert actual_value == expected_value

    def test_data_blocks_count(self, jfile_obj):
        """Test that correct number of data blocks are parsed."""
        assert len(jfile_obj.header.data_blocks) == 2

    def test_data_blocks_content(self, jfile_obj, expected_data_blocks):
        """Test that data blocks contain expected content."""
        for i, expected_block in enumerate(expected_data_blocks):
            actual_block = jfile_obj.header.data_blocks[i].to_dict(single=True)
            assert actual_block == expected_block, f"Data block {i} mismatch"

    @pytest.mark.parametrize("block_index", [0, 1])
    def test_data_blocks_individual_fields(self, jfile_obj, block_index):
        """Test individual data block fields using parametrization."""
        block = jfile_obj.header.data_blocks[block_index]

        # Common assertions for both blocks
        assert block.ncomp == 4
        assert block.nread == 38750
        assert block.nskip == 0
        assert (
            "/data/mtpy/examples/birrp_processing/birrp_wd/birrp_data_3.txt"
            in block.filnam
        )

        # Block-specific assertions
        if block_index == 0:
            assert block.indices == [1]
        else:
            assert block.indices == [3]

    def test_impedance_data_shape(self, jfile_obj):
        """Test that impedance tensor has correct shape."""
        expected_shape = (12, 2, 2)
        assert jfile_obj.z.shape == expected_shape

    def test_impedance_error_shape(self, jfile_obj):
        """Test that impedance error tensor has correct shape."""
        expected_shape = (12, 2, 2)
        assert jfile_obj.z_err.shape == expected_shape

    def test_impedance_data_type(self, jfile_obj):
        """Test that impedance data is complex."""
        assert jfile_obj.z.dtype == complex

    def test_impedance_error_data_type(self, jfile_obj):
        """Test that impedance error data is real."""
        assert np.isrealobj(jfile_obj.z_err)

    def test_impedance_not_empty(self, jfile_obj):
        """Test that impedance data is not empty and contains finite values."""
        # Check that we have non-NaN values (excluding -999 fill values)
        valid_mask = jfile_obj.z != -999.0
        assert np.any(valid_mask), "No valid impedance data found"

        # Check that valid data is finite
        valid_z = jfile_obj.z[valid_mask]
        assert np.all(np.isfinite(valid_z)), "Invalid values in impedance data"

    def test_impedance_error_not_empty(self, jfile_obj):
        """Test that impedance error data is not empty and contains valid values."""
        # Check that we have non-NaN values (excluding -999 fill values)
        valid_mask = jfile_obj.z_err != -999.0
        assert np.any(valid_mask), "No valid impedance error data found"

        # Check that valid data is finite and non-negative
        valid_z_err = jfile_obj.z_err[valid_mask]
        assert np.all(
            np.isfinite(valid_z_err)
        ), "Invalid values in impedance error data"
        assert np.all(valid_z_err >= 0), "Negative values in impedance error data"

    def test_frequency_data(self, jfile_obj):
        """Test that frequency data is available and valid."""
        assert jfile_obj.frequency is not None
        assert len(jfile_obj.frequency) == jfile_obj.z.shape[0]
        assert np.all(jfile_obj.frequency > 0), "Invalid frequency values"
        assert np.all(np.isfinite(jfile_obj.frequency)), "Non-finite frequency values"

    def test_header_location_fields(self, jfile_obj):
        """Test that inherited location fields are available."""
        # Test that location fields are accessible (from BasicLocation inheritance)
        assert hasattr(jfile_obj.header, "latitude")
        assert hasattr(jfile_obj.header, "longitude")
        assert hasattr(jfile_obj.header, "elevation")
        assert hasattr(jfile_obj.header, "datum")

    def test_header_serialization(self, jfile_obj):
        """Test that header can be serialized to dict and JSON."""
        # Test dictionary serialization
        header_dict = jfile_obj.header.to_dict()
        assert isinstance(header_dict, dict)
        assert "header" in header_dict

        # Test JSON serialization
        header_json = jfile_obj.header.to_json()
        assert isinstance(header_json, str)

        # Verify JSON is valid
        json_data = json.loads(header_json)
        assert isinstance(json_data, dict)

    def test_file_path_handling(self):
        """Test that JFile handles different path types correctly."""
        # Test with string path
        jfile1 = JFile(fn=str(TF_JFILE))
        assert jfile1.header.station == "BP05"

        # Test with Path object
        jfile2 = JFile(fn=Path(TF_JFILE))
        assert jfile2.header.station == "BP05"

    def test_jfile_string_representation(self, jfile_obj):
        """Test that JFile has a proper string representation."""
        str_repr = str(jfile_obj)
        assert "Station: BP05" in str_repr
        assert isinstance(str_repr, str)

    @pytest.mark.parametrize(
        "component",
        ["z", "z_err", "frequency"],
    )
    def test_impedance_components_not_none(self, jfile_obj, component):
        """Test that all impedance-related components are not None."""
        assert getattr(jfile_obj, component) is not None

    def test_birrp_parameters_type_consistency(self, jfile_obj):
        """Test that BIRRP parameters have consistent types."""
        params = jfile_obj.header.birrp_parameters

        # Float parameters
        float_params = [
            "ainlin",
            "ainuin",
            "c2threshe",
            "c2threshe1",
            "deltat",
            "nfft",
            "nsctinc",
            "nsctmax",
            "tbw",
            "uin",
        ]
        for param in float_params:
            if hasattr(params, param):
                value = getattr(params, param)
                assert isinstance(value, (int, float)), f"{param} should be numeric"

        # Integer parameters
        int_params = [
            "imode",
            "inputs",
            "jmode",
            "nar",
            "ncomp",
            "nf1",
            "nfinc",
            "nfsect",
            "npcs",
            "nz",
            "outputs",
            "references",
        ]
        for param in int_params:
            if hasattr(params, param):
                value = getattr(params, param)
                # Handle None values which are valid for some parameters
                if value is not None:
                    assert isinstance(value, int), f"{param} should be integer"

    def test_data_consistency(self, jfile_obj):
        """Test consistency between different data arrays."""
        # All arrays should have the same number of frequencies
        n_freq = jfile_obj.z.shape[0]
        assert jfile_obj.z_err.shape[0] == n_freq
        assert len(jfile_obj.frequency) == n_freq

        # Impedance tensor should be square 2x2 matrices
        assert jfile_obj.z.shape[1:] == (2, 2)
        assert jfile_obj.z_err.shape[1:] == (2, 2)


class TestJFileEdgeCases:
    """Test edge cases and error conditions for JFile."""

    def test_nonexistent_file(self):
        """Test behavior with non-existent file."""
        with pytest.raises(NameError):  # JFile raises NameError, not FileNotFoundError
            JFile(fn="nonexistent_file.j")

    def test_invalid_file_type(self):
        """Test behavior with invalid file type."""
        # This should be handled gracefully or raise appropriate exception
        with pytest.raises((ValueError, FileNotFoundError, IOError)):
            JFile(fn=__file__)  # Use this Python file as invalid J-file

    def test_empty_filename(self):
        """Test behavior with empty filename."""
        with pytest.raises(
            ValueError
        ):  # JFile raises ValueError for invalid file extension
            JFile(fn="")


class TestJFileAttributes:
    """Test JFile attribute access and modification."""

    @pytest.fixture
    def jfile_obj(self):
        """Fixture for attribute tests."""
        return JFile(fn=TF_JFILE)

    def test_header_attribute_access(self, jfile_obj):
        """Test that header attributes are accessible."""
        assert hasattr(jfile_obj, "header")
        assert hasattr(jfile_obj.header, "title")
        assert hasattr(jfile_obj.header, "station")
        assert hasattr(jfile_obj.header, "birrp_parameters")
        assert hasattr(jfile_obj.header, "data_blocks")

    def test_impedance_attribute_access(self, jfile_obj):
        """Test that impedance attributes are accessible."""
        assert hasattr(jfile_obj, "z")
        assert hasattr(jfile_obj, "z_err")
        assert hasattr(jfile_obj, "t")
        assert hasattr(jfile_obj, "t_err")
        assert hasattr(jfile_obj, "frequency")

    def test_file_attribute_access(self, jfile_obj):
        """Test that file-related attributes are accessible."""
        assert hasattr(jfile_obj, "fn")
        assert hasattr(jfile_obj, "_jfn")


# Test configuration for performance
class TestJFilePerformance:
    """Performance and efficiency tests."""

    def test_repeated_instantiation_performance(self):
        """Test that repeated JFile instantiation is reasonably fast."""
        import time

        start_time = time.time()
        for _ in range(10):
            jfile = JFile(fn=TF_JFILE)
            assert jfile.header.station == "BP05"
        end_time = time.time()

        # Should complete 10 instantiations in reasonable time (< 10 seconds)
        assert (end_time - start_time) < 10, "JFile instantiation too slow"


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
