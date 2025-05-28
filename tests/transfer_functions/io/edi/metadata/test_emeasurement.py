# -*- coding: utf-8 -*-
"""
Tests for the Emeasurement base model.

This module tests the Emeasurement class functionality including validation,
computed properties, and serialization methods.
"""

import numpy as np
import pytest

from mt_metadata.transfer_functions.io.edi.metadata.emeasurement_basemodel import (
    Emeasurement,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_emeasurement():
    """Return a Emeasurement instance with default values."""
    return Emeasurement()


@pytest.fixture(scope="module")
def custom_emeasurement():
    """Return a Emeasurement instance with custom values."""
    return Emeasurement(
        id=1.0,
        chtype="ex",
        x=50.0,
        y=0.0,
        z=0.0,
        x2=150.0,
        y2=0.0,
        z2=0.0,
        azm=90.0,
        acqchan="channel1",
    )


@pytest.fixture(scope="module")
def diagonal_emeasurement():
    """Return a Emeasurement instance with diagonal electrode layout."""
    return Emeasurement(
        id=2.0,
        chtype="ey",
        x=0.0,
        y=25.0,
        z=0.0,
        x2=0.0,
        y2=125.0,
        z2=0.0,
        azm=0.0,  # Will be computed from coordinates
        acqchan="ch2",
    )


@pytest.fixture(scope="module")
def depth_emeasurement():
    """Return a Emeasurement instance with depth component."""
    return Emeasurement(
        id=3.0,
        chtype="ez",
        x=0.0,
        y=0.0,
        z=10.0,
        x2=0.0,
        y2=0.0,
        z2=110.0,
        azm=0.0,
        acqchan="3",
    )


@pytest.fixture(scope="module")
def angled_emeasurement():
    """Return a Emeasurement instance with angled orientation."""
    return Emeasurement(
        id=4.0,
        chtype="exy",
        x=10.0,
        y=10.0,
        z=0.0,
        x2=90.0,
        y2=90.0,
        z2=0.0,
        azm=0.0,  # Will be computed from coordinates
        acqchan="chan4",
    )


# =============================================================================
# Tests
# =============================================================================


class TestEmeasurementInitialization:
    """Test initialization of the Emeasurement class."""

    def test_default_values(self, default_emeasurement, subtests):
        """Test the default values of Emeasurement attributes."""
        scalar_attrs = {
            "id": 0.0,
            "chtype": "",
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "x2": 0.0,
            "y2": 0.0,
            "z2": 0.0,
            "azm": 0.0,
            "acqchan": "",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"default {attr}"):
                assert getattr(default_emeasurement, attr) == expected

    def test_custom_values(self, custom_emeasurement, subtests):
        """Test Emeasurement with custom attribute values."""
        scalar_attrs = {
            "id": 1.0,
            "chtype": "ex",
            "x": 50.0,
            "y": 0.0,
            "z": 0.0,
            "x2": 150.0,
            "y2": 0.0,
            "z2": 0.0,
            "azm": 90.0,
            "acqchan": "channel1",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"custom {attr}"):
                assert getattr(custom_emeasurement, attr) == expected


class TestEmeasurementComputedProperties:
    """Test computed properties of the Emeasurement class."""

    def test_dipole_length_horizontal(self, custom_emeasurement):
        """Test dipole_length calculation for horizontal layout."""
        assert custom_emeasurement.dipole_length == 100.0

    def test_dipole_length_vertical(self, depth_emeasurement):
        """Test dipole_length calculation for vertical layout."""
        assert depth_emeasurement.dipole_length == 100.0

    def test_dipole_length_diagonal(self, angled_emeasurement):
        """Test dipole_length calculation for diagonal layout."""
        expected = np.sqrt(80**2 + 80**2)  # Pythagorean theorem
        assert np.isclose(angled_emeasurement.dipole_length, expected)

    def test_dipole_length_default(self, default_emeasurement):
        """Test dipole_length calculation for default values."""
        assert default_emeasurement.dipole_length == 0.0

    def test_azimuth_calculation_east(self, custom_emeasurement):
        """Test azimuth calculation for east-oriented electrode."""
        # Should be 0.0 degrees for east orientation (x-axis)
        assert custom_emeasurement.azimuth == 0.0

    def test_azimuth_calculation_north(self, diagonal_emeasurement):
        """Test azimuth calculation for north-oriented electrode."""
        # Should be 90.0 degrees for north orientation (y-axis)
        assert diagonal_emeasurement.azimuth == 90.0

    def test_azimuth_calculation_diagonal(self, angled_emeasurement):
        """Test azimuth calculation for diagonally oriented electrode."""
        # Should be 45.0 degrees for northeast orientation
        assert np.isclose(angled_emeasurement.azimuth, 45.0)

    def test_azimuth_auto_assignment(
        self, diagonal_emeasurement, angled_emeasurement, subtests
    ):
        """Test automatic azimuth assignment from coordinates."""
        with subtests.test(msg="north direction"):
            assert diagonal_emeasurement.azm == 90.0

        with subtests.test(msg="diagonal direction"):
            assert np.isclose(angled_emeasurement.azm, 45.0)

    def test_channel_number_extraction_string(self, custom_emeasurement):
        """Test channel_number extraction from string acqchan."""
        assert custom_emeasurement.channel_number == 1

    def test_channel_number_extraction_numeric(self, depth_emeasurement):
        """Test channel_number extraction from numeric acqchan."""
        assert depth_emeasurement.channel_number == 3

    def test_channel_number_extraction_prefix(self, diagonal_emeasurement):
        """Test channel_number extraction from prefixed acqchan."""
        assert diagonal_emeasurement.channel_number == 2

    def test_channel_number_extraction_default(self, default_emeasurement):
        """Test channel_number extraction from default acqchan."""
        assert default_emeasurement.channel_number == 0


class TestEmeasurementMethods:
    """Test methods of the Emeasurement class."""

    def test_string_representation(self, custom_emeasurement):
        """Test string representation of Emeasurement."""
        str_rep = str(custom_emeasurement)

        # Check that the string contains all attributes
        assert "id = 1.0" in str_rep
        assert "chtype = ex" in str_rep
        assert "x = 50.0" in str_rep
        assert "x2 = 150.0" in str_rep

        # Also check __repr__
        repr_str = repr(custom_emeasurement)
        assert repr_str == str_rep

    def test_write_meas_line(self, custom_emeasurement):
        """Test write_meas_line method."""
        line = custom_emeasurement.write_meas_line()

        # Check that the line has the expected format
        assert line.startswith(">EMEAS")
        assert "ID=1.0" in line
        assert "CHTYPE=ex" in line
        assert "X=50.00" in line
        assert "X2=150.00" in line
        assert "AZM=90.00" in line
        assert "ACQCHAN=channel1" in line
        assert line.endswith("\n")

    def test_write_meas_line_error_handling(self):
        """Test error handling in write_meas_line method."""
        # Create an object with a problematic value
        emeas = Emeasurement()
        emeas.__dict__["acqchan"] = None  # This will cause a TypeError

        # The method should handle the error and use a default
        line = emeas.write_meas_line()
        assert "ACQCHAN=0.0" in line

    def test_to_dict_format(self, custom_emeasurement):
        """Test to_dict method output format."""
        result = custom_emeasurement.to_dict(single=True)

        # Check that the dictionary has all expected keys
        expected_keys = [
            "id",
            "chtype",
            "x",
            "y",
            "z",
            "x2",
            "y2",
            "z2",
            "azm",
            "acqchan",
        ]
        for key in expected_keys:
            assert key in result

        # Check a few values
        assert result["id"] == 1.0
        assert result["chtype"] == "ex"
        assert result["x"] == 50.0


class TestEmeasurementValidation:
    """Test validation in the Emeasurement class."""

    def test_chtype_pattern_validation(self):
        """Test chtype pattern validation."""
        # Valid chtype (starts with 'e')
        valid_emeas = Emeasurement(chtype="ex")
        assert valid_emeas.chtype == "ex"

        # Invalid chtype (doesn't start with 'e')
        with pytest.raises(ValueError):
            Emeasurement(chtype="hx")

    def test_coordinate_validation(self):
        """Test coordinate validation when creating Emeasurement."""
        # All these should be valid
        valid_coordinates = [
            {"x": 0.0, "y": 0.0, "x2": 100.0, "y2": 0.0},
            {"x": 0.0, "y": 0.0, "x2": 0.0, "y2": 100.0},
            {"x": -50.0, "y": -50.0, "x2": 50.0, "y2": 50.0},
        ]

        for coords in valid_coordinates:
            emeas = Emeasurement(**coords)
            for key, value in coords.items():
                assert getattr(emeas, key) == value


class TestEmeasurementModification:
    """Test modification of the Emeasurement class."""

    def test_attribute_updates(self, default_emeasurement, subtests):
        """Test updating attributes after initialization."""
        updates = {
            "id": 5.0,
            "chtype": "exy",
            "x": -25.0,
            "y": -25.0,
            "z": 0.0,
            "x2": 25.0,
            "y2": 25.0,
            "z2": 0.0,
            "acqchan": "channel5",
        }

        # Apply updates
        for attr, value in updates.items():
            setattr(default_emeasurement, attr, value)

        # Verify updates
        for attr, expected in updates.items():
            with subtests.test(msg=f"updated {attr}"):
                assert getattr(default_emeasurement, attr) == expected

        # Check that azimuth was automatically updated
        with subtests.test(msg="auto-updated azm"):
            assert np.isclose(default_emeasurement.azm, 45.0)

        # Check that dipole_length was updated
        with subtests.test(msg="updated dipole_length"):
            expected_length = np.sqrt(50**2 + 50**2)
            assert np.isclose(default_emeasurement.dipole_length, expected_length)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
