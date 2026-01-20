# -*- coding: utf-8 -*-
"""
Tests for the DataSection base model.

This module tests the DataSection class functionality including
validation, default values, custom values, and methods for reading/writing data.
"""

from unittest.mock import patch

import pytest

from mt_metadata.transfer_functions.io.edi.metadata import DataSection

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_data_section():
    """Return a DataSection instance with default values."""
    return DataSection()


@pytest.fixture(scope="module")
def custom_data_section():
    """Return a DataSection instance with custom values."""
    return DataSection(
        nfreq=16,
        sectid="mt001",
        nchan=7,
        maxblocks=999,
        ex="1",
        ey="2",
        hx="3",
        hy="4",
        hz="5",
        rrhx="6",
        rrhy="7",
    )


@pytest.fixture(scope="module")
def minimal_data_section():
    """Return a DataSection instance with minimal required values."""
    return DataSection(sectid="mt002", nchan=5, maxblocks=50)


@pytest.fixture(scope="module")
def sample_edi_lines():
    """Sample EDI lines for testing read_data method."""
    return [
        "Header Line 1",
        "Header Line 2",
        ">=>=>=>=>=>=>=>=>=>=>=>=>",
        ">=MTSECT",
        "    NFREQ=16",
        "    SECTID=mt003",
        "    NCHAN=5",
        "    MAXBLOCKS=100",
        "    EX=1",
        "    EY=2",
        "    HX=3",
        "    HY=4",
        "    HZ=5",
        "//",
        "1 2 3 4 5",
        ">XXXX",
        "Footer Line 1",
    ]


@pytest.fixture(scope="module")
def spectra_edi_lines():
    """Sample EDI lines with spectra section for testing."""
    return [
        "Header Line 1",
        ">=SPECTRASECT",
        "    NFREQ=32",
        "    SECTID=mt004",
        "    NCHAN=5",
        "    MAXBLOCKS=200",
        "    EX=1",
        "    EY=2",
        "    HX=3",
        "    HY=4",
        "    HZ=5",
        "//",
        "1",
        "2",
        "3",
        "4",
        "5",
        ">XXXX",
    ]


@pytest.fixture(scope="module")
def channel_ids_map():
    """Sample channel IDs map for testing match_channels method."""
    return {"EX": 1, "EY": 2, "HX": 3, "HY": 4, "HZ": 5}


# =============================================================================
# Tests
# =============================================================================


class TestDataSectionInitialization:
    """Test initialization of the DataSection class."""

    def test_default_values(self, default_data_section, subtests):
        """Test the default values of DataSection attributes."""
        scalar_attrs = {
            "nfreq": 0,
            "sectid": "",
            "nchan": 0,
            "maxblocks": 999,
            "ex": None,
            "ey": None,
            "hx": None,
            "hy": None,
            "hz": None,
            "rrhx": None,
            "rrhy": None,
        }

        # Check public attributes
        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"default {attr}"):
                assert getattr(default_data_section, attr) == expected

        # Check private attributes
        with subtests.test(msg="default _line_num"):
            assert default_data_section._line_num == 0

        with subtests.test(msg="default _data_type_out"):
            assert default_data_section._data_type_out == "z"

        with subtests.test(msg="default _data_type_in"):
            assert default_data_section._data_type_in == "z"

        with subtests.test(msg="default _channel_ids"):
            assert default_data_section._channel_ids == []

        with subtests.test(msg="default _kw_list"):
            expected_kw_list = [
                "nfreq",
                "sectid",
                "nchan",
                "maxblocks",
                "ex",
                "ey",
                "hx",
                "hy",
                "hz",
                "rrhx",
                "rrhy",
            ]
            assert default_data_section._kw_list == expected_kw_list

    def test_custom_values(self, custom_data_section, subtests):
        """Test DataSection with custom attribute values."""
        scalar_attrs = {
            "nfreq": 16,
            "sectid": "mt001",
            "nchan": 7,
            "maxblocks": 999,
            "ex": "1",
            "ey": "2",
            "hx": "3",
            "hy": "4",
            "hz": "5",
            "rrhx": "6",
            "rrhy": "7",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"custom {attr}"):
                assert getattr(custom_data_section, attr) == expected


class TestDataSectionMethods:
    """Test methods of the DataSection class."""

    def test_string_representation(self, custom_data_section):
        """Test the string representation of DataSection."""
        with patch.object(
            custom_data_section,
            "write_data",
            return_value=[
                "\n>=MTSECT\n    NFREQ=16\n    SECTID=mt001\n    NCHAN=7\n    MAXBLOCKS=999\n    EX=1\n    EY=2\n    HX=3\n    HY=4\n    HZ=5\n    RRHX=6\n    RRHY=7\n\n"
            ],
        ):
            result = str(custom_data_section)
            assert (
                result
                == "\n>=MTSECT\n    NFREQ=16\n    SECTID=mt001\n    NCHAN=7\n    MAXBLOCKS=999\n    EX=1\n    EY=2\n    HX=3\n    HY=4\n    HZ=5\n    RRHX=6\n    RRHY=7\n\n"
            )

            # Also test __repr__
            assert (
                repr(custom_data_section)
                == "\n>=MTSECT\n    NFREQ=16\n    SECTID=mt001\n    NCHAN=7\n    MAXBLOCKS=999\n    EX=1\n    EY=2\n    HX=3\n    HY=4\n    HZ=5\n    RRHX=6\n    RRHY=7\n\n"
            )

    def test_get_data_z_type(self, sample_edi_lines):
        """Test get_data method with impedance data."""
        data_section = DataSection()
        data_lines = data_section.get_data(sample_edi_lines)

        assert data_section._data_type_in == "z"
        assert data_section._line_num == 15
        assert len(data_lines) == 10
        assert "NFREQ=16" in data_lines

    def test_get_data_spectra_type(self, spectra_edi_lines):
        """Test get_data method with spectra data."""
        data_section = DataSection()
        data_lines = data_section.get_data(spectra_edi_lines)

        assert data_section._data_type_in == "spectra"
        assert data_section._line_num == 17
        assert len(data_lines) == 9
        assert "NFREQ=32" in data_lines

    def test_read_data_impedance(self, sample_edi_lines, subtests):
        """Test read_data method with impedance data."""
        data_section = DataSection()
        data_section.read_data(sample_edi_lines)

        expected_values = {
            "nfreq": 16,
            "sectid": "mt003",
            "nchan": 5,
            "maxblocks": 100,
            "ex": "1",
            "ey": "2",
            "hx": "3",
            "hy": "4",
            "hz": "5",
        }

        for attr, expected in expected_values.items():
            with subtests.test(msg=f"read {attr}"):
                assert getattr(data_section, attr) == expected

        with subtests.test(msg="read channel_ids property"):
            assert data_section._channel_ids == ["1", "2", "3", "4", "5"]

    def test_read_data_spectra(self, spectra_edi_lines, subtests):
        """Test read_data method with spectra data."""
        data_section = DataSection()
        data_section.read_data(spectra_edi_lines)

        expected_values = {
            "nfreq": 32,
            "sectid": "mt004",
            "nchan": 5,
            "maxblocks": 200,
            "ex": "1",
            "ey": "2",
            "hx": "3",
            "hy": "4",
            "hz": "5",
        }

        for attr, expected in expected_values.items():
            with subtests.test(msg=f"read spectra {attr}"):
                assert getattr(data_section, attr) == expected

        with subtests.test(msg="read spectra _channel_ids"):
            assert len(data_section._channel_ids) == 5
            assert "1" in data_section._channel_ids
            assert "5" in data_section._channel_ids

    def test_read_data_with_no_channels_section(self, subtests):
        """Test read_data method when there's no channels section."""
        edi_lines = [
            ">=MTSECT",
            "    NFREQ=8",
            "    SECTID=mt005",
            "    NCHAN=3",
            "    MAXBLOCKS=50",
            "    EX=10",
            "    EY=11",
            "    HX=12",
        ]

        data_section = DataSection()
        data_section.read_data(edi_lines)

        with subtests.test(msg="channel_ids from attrs"):
            # Should extract channel IDs from attributes when no explicit channels section
            assert data_section._channel_ids == ["10", "11", "12"]

    def test_write_data_impedance(self, custom_data_section, subtests):
        """Test write_data method with impedance data."""
        custom_data_section._data_type_out = "z"
        lines = custom_data_section.write_data()

        with subtests.test(msg="write header"):
            assert ">=MTSECT" in lines[0]

        attrs_to_check = ["NFREQ", "SECTID", "NCHAN", "MAXBLOCKS"]
        for i, attr in enumerate(attrs_to_check, 1):
            with subtests.test(msg=f"write {attr}"):
                assert attr in lines[i]

        # Check that all channels are written
        channel_attrs = ["EX", "EY", "HX", "HY", "HZ", "RRHX", "RRHY"]
        written_lines = "".join(lines)
        for attr in channel_attrs:
            with subtests.test(msg=f"write channel {attr}"):
                assert attr in written_lines

    def test_write_data_spectra(self, custom_data_section, subtests):
        """Test write_data method with spectra data."""
        custom_data_section._data_type_out = "spectra"
        lines = custom_data_section.write_data()

        with subtests.test(msg="write spectra header"):
            assert ">SPECTRASECT" in lines[0]

        attrs_to_check = ["NFREQ", "SECTID", "NCHAN", "MAXBLOCKS"]
        for i, attr in enumerate(attrs_to_check, 1):
            with subtests.test(msg=f"write spectra {attr}"):
                assert attr in lines[i]

    def test_write_data_with_override(self, default_data_section):
        """Test write_data method with override dictionary."""
        override = {"nfreq": 64, "nchan": 10, "sectid": "override_test"}
        lines = default_data_section.write_data(over_dict=override)

        # Check that overridden values are used
        written_text = "".join(lines)
        assert "NFREQ=64" in written_text
        assert "NCHAN=10" in written_text
        assert "SECTID=override_test" in written_text

    def test_write_data_sorting(self, subtests):
        """Test that write_data sorts channels in ascending order."""
        data_section = DataSection(
            ex="3", ey="1", hx="5", hy="2", hz="4", rrhx="7", rrhy="6"
        )

        lines = data_section.write_data()
        written_text = "".join(lines)

        # Check that channels appear in sorted order by their values
        channel_positions = {}
        for ch in ["EX", "EY", "HX", "HY", "HZ", "RRHX", "RRHY"]:
            pos = written_text.find(ch)
            if pos != -1:
                channel_positions[ch] = pos

        # The channel positions should be in ascending order of channel values
        # (EY(1), HY(2), EX(3), HZ(4), HX(5), RRHY(6), RRHX(7))
        expected_order = ["EY", "HY", "EX", "HZ", "HX", "RRHY", "RRHX"]

        current_pos = -1
        for ch in expected_order:
            with subtests.test(msg=f"channel {ch} position"):
                assert channel_positions[ch] > current_pos
                current_pos = channel_positions[ch]

    def test_match_channels(self, default_data_section, channel_ids_map, subtests):
        """Test match_channels method."""
        # Set up test data
        default_data_section._channel_ids = ["1", "2", "3", "4", "5"]

        # Call the method
        default_data_section.match_channels(channel_ids_map)

        # Check results
        channel_attrs = {"ex": 1, "ey": 2, "hx": 3, "hy": 4, "hz": 5}

        for attr, expected in channel_attrs.items():
            with subtests.test(msg=f"matched {attr}"):
                assert getattr(default_data_section, attr) == str(expected)

    def test_match_channels_with_ch_prefix(self, default_data_section, subtests):
        """Test match_channels method with channels that have 'ch' prefix."""
        # Set up test data
        default_data_section._channel_ids = ["ch1", "ch2", "ch3"]
        channel_map = {"EX": 1, "EY": 2, "HX": 3}

        # Call the method
        default_data_section.match_channels(channel_map)

        # Check results
        channel_attrs = {"ex": 1, "ey": 2, "hx": 3}

        for attr, expected in channel_attrs.items():
            with subtests.test(msg=f"matched ch prefix {attr}"):
                assert getattr(default_data_section, attr) == str(expected)

    def test_match_channels_with_invalid_id(self, default_data_section):
        """Test match_channels method with invalid channel ID."""
        # Set up test data
        default_data_section._channel_ids = ["invalid"]
        channel_map = {"EX": 1}

        # Mock the logger to avoid actual warnings
        with patch(
            "mt_metadata.transfer_functions.io.edi.metadata.data_section.logger.warning"
        ) as mock_warning:
            default_data_section.match_channels(channel_map)
            # Check that warning was logged
            mock_warning.assert_called_with("Could not match channel invalid")


class TestDataSectionModification:
    """Test modification of the DataSection class."""

    def test_attribute_updates(self, default_data_section, subtests):
        """Test updating attributes after initialization."""
        updates = {
            "nfreq": 24,
            "sectid": "updated",
            "nchan": 6,
            "maxblocks": 500,
            "ex": "10",
            "ey": "11",
            "hx": "12",
            "hy": "13",
            "hz": "14",
        }

        # Apply updates
        for attr, value in updates.items():
            setattr(default_data_section, attr, value)

        # Verify updates
        for attr, expected in updates.items():
            with subtests.test(msg=f"updated {attr}"):
                assert getattr(default_data_section, attr) == expected

    def test_channel_ids_property(self, subtests):
        """Test the channel_ids property setter and getter."""
        data_section = DataSection()

        # Test setter
        test_ids = ["101", "102", "103"]
        data_section._channel_ids = test_ids

        with subtests.test(msg="channel_ids getter"):
            assert data_section._channel_ids == test_ids

        with subtests.test(msg="_channel_ids internal"):
            assert data_section._channel_ids == test_ids


if __name__ == "__main__":
    pytest.main(["-v", __file__])
