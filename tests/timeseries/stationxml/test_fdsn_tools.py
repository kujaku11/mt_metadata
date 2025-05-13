# -*- coding: utf-8 -*-
"""
Tests for FDSN tools using pytest.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import pytest


try:
    from mt_metadata.timeseries.stationxml import fdsn_tools
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)


# --- Fixtures ---


@pytest.fixture(scope="module")
def orientation_angles():
    """Define test angles for different orientations."""
    return {
        "north_angles": [-14, -10, -5, 0, 5, 10, 14],
        "east_angles": [76, 80, 85, 91, 95, 100, 104],
        "vertical_angles": [-14, -10, -5, 0, 3, 5, 10, 14],
        "one": -16,
        "two": 134,
        "three": 20,
    }


@pytest.fixture(scope="module")
def channel_codes():
    """Define test channel codes."""
    return {"h_channel_code": "LFN", "e_channel_code": "EQE", "aux_channel_code": "LKZ"}


# --- Test Functions for Orientation Code ---


class TestOrientationCode:
    """Test getting orientation code from azimuth."""

    def test_north(self, orientation_angles, subtests):
        """Test north orientation codes."""
        for angle in orientation_angles["north_angles"]:
            with subtests.test(msg=f"testing angle {angle}"):
                assert fdsn_tools.get_orientation_code(angle) == "N"

    def test_east(self, orientation_angles, subtests):
        """Test east orientation codes."""
        for angle in orientation_angles["east_angles"]:
            with subtests.test(msg=f"testing angle {angle}"):
                assert fdsn_tools.get_orientation_code(angle) == "E"

    def test_vertical(self, orientation_angles, subtests):
        """Test vertical orientation codes."""
        for angle in orientation_angles["vertical_angles"]:
            with subtests.test(msg=f"Testing angle {angle}"):
                assert (
                    fdsn_tools.get_orientation_code(angle, orientation="vertical")
                    == "Z"
                )

    def test_numbered_orientations(self, orientation_angles, subtests):
        """Test numbered orientation codes."""
        with subtests.test(msg="one code"):
            assert fdsn_tools.get_orientation_code(orientation_angles["one"]) == "1"

        with subtests.test(msg="two code"):
            assert fdsn_tools.get_orientation_code(orientation_angles["two"]) == "2"

        with subtests.test(msg="three code"):
            assert (
                fdsn_tools.get_orientation_code(
                    orientation_angles["three"], orientation="vertical"
                )
                == "3"
            )

    def test_direction_codes(self, subtests):
        """Test orientation codes from direction strings."""
        with subtests.test(msg="x direction"):
            assert fdsn_tools.get_orientation_code(direction="x") == "N"

        with subtests.test(msg="y direction"):
            assert fdsn_tools.get_orientation_code(direction="y") == "E"

        with subtests.test(msg="z direction"):
            assert fdsn_tools.get_orientation_code(direction="z") == "Z"

    def test_direction_fail(self):
        """Test invalid direction raises ValueError."""
        with pytest.raises(ValueError):
            fdsn_tools.get_orientation_code(None, "k")


# --- Test Functions for Channel Code ---


class TestChannelCode:
    """Test making and reading channel codes."""

    def test_orientation_code(self, subtests):
        """Test specific orientation codes."""
        with subtests.test(msg="0 to Z"):
            assert fdsn_tools.get_orientation_code(0, orientation="vertical") == "Z"

        with subtests.test(msg="16 to 1"):
            assert fdsn_tools.get_orientation_code(16) == "1"

        with subtests.test(msg="50 to 2"):
            assert fdsn_tools.get_orientation_code(50) == "2"

    def test_read_h_channel(self, channel_codes, subtests):
        """Test reading horizontal magnetic channel code."""
        ch_dict = fdsn_tools.read_channel_code(channel_codes["h_channel_code"])

        with subtests.test(msg="period range"):
            assert ch_dict["period"] == {"min": 0.95, "max": 1.05}

        with subtests.test(msg="measurement type"):
            assert ch_dict["measurement"] == "magnetic"

        with subtests.test(msg="orientation"):
            assert ch_dict["orientation"] == {"angle": 0, "variance": 15}

    def test_read_e_channel(self, channel_codes, subtests):
        """Test reading electric channel code."""
        ch_dict = fdsn_tools.read_channel_code(channel_codes["e_channel_code"])

        with subtests.test(msg="period range"):
            assert ch_dict["period"] == {"min": 80, "max": 250}

        with subtests.test(msg="measurement type"):
            assert ch_dict["measurement"] == "electric"

        with subtests.test(msg="orientation"):
            assert ch_dict["orientation"] == {"angle": 90, "variance": 15}

    def test_read_aux_channel(self, channel_codes, subtests):
        """Test reading auxiliary channel code."""
        ch_dict = fdsn_tools.read_channel_code(channel_codes["aux_channel_code"])

        with subtests.test(msg="period range"):
            assert ch_dict["period"] == {"min": 0.95, "max": 1.05}

        with subtests.test(msg="measurement type"):
            assert ch_dict["measurement"] == "temperature"

        with subtests.test(msg="orientation"):
            assert ch_dict["orientation"] == {"angle": 0, "variance": 15}

    def test_make_channels(self, channel_codes, subtests):
        """Test making different channel codes."""
        with subtests.test(msg="make_h_channel"):
            ch_code = fdsn_tools.make_channel_code(1, "magnetic", 0)
            assert ch_code == channel_codes["h_channel_code"]

        with subtests.test(msg="make_h_channel_direction"):
            ch_code = fdsn_tools.make_channel_code(1, "magnetic", "x")
            assert ch_code == channel_codes["h_channel_code"]

        with subtests.test(msg="make_e_channel"):
            ch_code = fdsn_tools.make_channel_code(100, "electric", 87)
            assert ch_code == channel_codes["e_channel_code"]

        with subtests.test(msg="make_e_channel_direction"):
            ch_code = fdsn_tools.make_channel_code(100, "electric", "y")
            assert ch_code == channel_codes["e_channel_code"]

        with subtests.test(msg="make_aux_channel"):
            ch_code = fdsn_tools.make_channel_code(
                1, "temperature", 4, orientation="vertical"
            )
            assert ch_code == channel_codes["aux_channel_code"]

        with subtests.test(msg="make_aux_channel_direction"):
            ch_code = fdsn_tools.make_channel_code(1, "temperature", "z")
            assert ch_code == channel_codes["aux_channel_code"]
