# -*- coding: utf-8 -*-
"""
Tests for the HMeasurement base model.

This module tests the HMeasurement class functionality including validation,
computed properties, and serialization methods.
"""

import pytest

from mt_metadata.transfer_functions.io.edi.metadata import HMeasurement

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_hmeasurement():
    """Return a HMeasurement instance with default values."""
    return HMeasurement()


@pytest.fixture(scope="module")
def custom_hmeasurement():
    """Return a HMeasurement instance with custom values."""
    return HMeasurement(
        id=1.0, chtype="hx", x=50.0, y=0.0, z=0.0, azm=90.0, dip=0.0, acqchan="channel1"
    )


@pytest.fixture(scope="module")
def angled_hmeasurement():
    """Return a HMeasurement instance with non-zero dip."""
    return HMeasurement(
        id=2.0, chtype="hz", x=0.0, y=0.0, z=1.0, azm=0.0, dip=90.0, acqchan="ch2"
    )


@pytest.fixture(scope="module")
def htype_variations():
    """Return HMeasurement instances with different variations of h-type sensors."""
    return [
        ("hx", True),
        ("hy", True),
        ("hz", True),
        ("hxy", True),
        ("hxz", True),
        ("bz", True),  # b is also valid
        ("bx", True),
        ("ex", False),  # e is invalid
        ("ax", False),  # a is invalid
        ("h", False),  # needs more than just h
        ("b", False),  # needs more than just b
        ("123", False),  # must start with h or b
    ]


# =============================================================================
# Tests
# =============================================================================


class TestHmeasurementInitialization:
    """Test initialization of the HMeasurement class."""

    def test_default_values(self, default_hmeasurement, subtests):
        """Test the default values of HMeasurement attributes."""
        scalar_attrs = {
            "id": 0.0,
            "chtype": "",
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "azm": 0.0,
            "dip": 0.0,
            "acqchan": "",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"default {attr}"):
                assert getattr(default_hmeasurement, attr) == expected

    def test_custom_values(self, custom_hmeasurement, subtests):
        """Test HMeasurement with custom attribute values."""
        scalar_attrs = {
            "id": 1.0,
            "chtype": "hx",
            "x": 50.0,
            "y": 0.0,
            "z": 0.0,
            "azm": 90.0,
            "dip": 0.0,
            "acqchan": "channel1",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"custom {attr}"):
                assert getattr(custom_hmeasurement, attr) == expected


class TestHmeasurementComputedProperties:
    """Test computed properties of the HMeasurement class."""

    def test_channel_number_extraction_string(self, custom_hmeasurement):
        """Test channel_number extraction from string acqchan."""
        assert custom_hmeasurement.channel_number == 1

    def test_channel_number_extraction_numeric(self):
        """Test channel_number extraction from numeric acqchan."""
        hmeas = HMeasurement(acqchan="3")
        assert hmeas.channel_number == 3

    def test_channel_number_extraction_prefix(self):
        """Test channel_number extraction from prefixed acqchan."""
        hmeas = HMeasurement(acqchan="ch2")
        assert hmeas.channel_number == 2

    def test_channel_number_extraction_default(self, default_hmeasurement):
        """Test channel_number extraction from default acqchan."""
        assert default_hmeasurement.channel_number == 0

    def test_channel_number_extraction_complex(self):
        """Test channel_number extraction from complex acqchan strings."""
        test_cases = [
            ("abc123def456", 123456),  # Concatenates all digits
            ("sensor_42", 42),
            ("no-numbers", 0),
            ("ch_0", 0),
            ("42nd_channel", 42),
        ]

        for acqchan, expected in test_cases:
            hmeas = HMeasurement(acqchan=acqchan)
            assert hmeas.channel_number == expected


class TestHmeasurementMethods:
    """Test methods of the HMeasurement class."""

    def test_string_representation(self, custom_hmeasurement):
        """Test string representation of HMeasurement."""
        str_rep = str(custom_hmeasurement)

        # Check that the string contains all attributes
        assert "id = 1.0" in str_rep
        assert "chtype = hx" in str_rep
        assert "x = 50.0" in str_rep
        assert "azm = 90.0" in str_rep

        # Also check __repr__
        repr_str = repr(custom_hmeasurement)
        assert repr_str == str_rep

    def test_write_meas_line(self, custom_hmeasurement, subtests):
        """Test write_meas_line method."""
        line = custom_hmeasurement.write_meas_line()

        # Check that the line has the expected format
        with subtests.test(msg="line format"):
            assert line.startswith(">HMEAS")
            assert line.endswith("\n")

        # Check that all attributes are present in the expected format
        expected_values = {
            "ID=1.0": True,
            "CHTYPE=hx": True,
            "X=50.00": True,
            "Y=0.00": True,
            "Z=0.00": True,
            "AZM=90.00": True,
            "DIP=0.00": True,
            "ACQCHAN=channel1": True,
        }

        for value, should_exist in expected_values.items():
            with subtests.test(msg=f"contains {value}"):
                if should_exist:
                    assert value in line
                else:
                    assert value not in line

    def test_write_meas_line_error_handling(self):
        """Test error handling in write_meas_line method."""
        # Create an object with a problematic value
        hmeas = HMeasurement()
        hmeas.__dict__["acqchan"] = None  # This will cause a TypeError

        # The method should handle the error and use a default
        line = hmeas.write_meas_line()
        assert "ACQCHAN=0.0" in line

    def test_to_dict_format(self, custom_hmeasurement, subtests):
        """Test to_dict method output format."""
        result = custom_hmeasurement.to_dict(single=True)

        # Check that the dictionary has all expected keys
        expected_keys = ["id", "chtype", "x", "y", "z", "azm", "dip", "acqchan"]
        for key in expected_keys:
            with subtests.test(msg=f"has key {key}"):
                assert key in result

        # Check a few values
        assert result["id"] == 1.0
        assert result["chtype"] == "hx"
        assert result["x"] == 50.0
        assert result["azm"] == 90.0


class TestHmeasurementValidation:
    """Test validation in the HMeasurement class."""

    @pytest.mark.parametrize(
        "chtype,is_valid",
        [
            ("hx", True),
            ("hy", True),
            ("hz", True),
            ("hxy", True),
            ("bz", True),  # b is also valid
            ("bx", True),
            ("ex", False),  # e is invalid
            ("ax", False),  # a is invalid
            ("h", False),  # needs more than just h
            ("b", False),  # needs more than just b
            ("123", False),  # must start with h or b
        ],
    )
    def test_chtype_pattern_validation(self, chtype, is_valid):
        """Test chtype pattern validation."""
        if is_valid:
            # Valid chtype (starts with 'h' or 'b')
            hmeas = HMeasurement(chtype=chtype)
            assert hmeas.chtype == chtype
        else:
            # Invalid chtype
            with pytest.raises(ValueError):
                HMeasurement(chtype=chtype)

    def test_coordinate_validation(self):
        """Test coordinate validation when creating HMeasurement."""
        # All these should be valid
        valid_coordinates = [
            {"x": 0.0, "y": 0.0, "z": 0.0},
            {"x": 100.0, "y": -50.0, "z": 25.0},
            {"x": -50.0, "y": -50.0, "z": -10.0},
        ]

        for coords in valid_coordinates:
            hmeas = HMeasurement(chtype="hx", **coords)
            for key, value in coords.items():
                assert getattr(hmeas, key) == value


class TestHmeasurementModification:
    """Test modification of the HMeasurement class."""

    def test_attribute_updates(self, default_hmeasurement, subtests):
        """Test updating attributes after initialization."""
        updates = {
            "id": 5.0,
            "chtype": "hz",
            "x": 0.0,
            "y": 0.0,
            "z": 10.0,
            "azm": 0.0,
            "dip": 90.0,
            "acqchan": "channel5",
        }

        # Apply updates
        for attr, value in updates.items():
            setattr(default_hmeasurement, attr, value)

        # Verify updates
        for attr, expected in updates.items():
            with subtests.test(msg=f"updated {attr}"):
                assert getattr(default_hmeasurement, attr) == expected

    def test_bulk_update_via_dict(self):
        """Test updating multiple attributes via from_dict."""
        hmeas = HMeasurement()
        update_dict = {
            "hmeasurement": {
                "id": 7.0,
                "chtype": "bx",
                "x": 25.0,
                "y": 25.0,
                "z": 0.0,
                "azm": 45.0,
                "dip": 0.0,
                "acqchan": "magnetometer1",
            }
        }

        hmeas.from_dict(update_dict)

        assert hmeas.id == 7.0
        assert hmeas.chtype == "bx"
        assert hmeas.x == 25.0
        assert hmeas.y == 25.0
        assert hmeas.azm == 45.0
        assert hmeas.acqchan == "magnetometer1"


class TestHmeasurementEdgeCases:
    """Test edge cases and special scenarios for HMeasurement."""

    def test_empty_acqchan_channel_number(self):
        """Test channel_number with empty acqchan."""
        hmeas = HMeasurement(acqchan="")
        assert hmeas.channel_number == 0

    def test_float_acqchan_channel_number(self):
        """Test channel_number with float acqchan."""
        hmeas = HMeasurement(acqchan=3.14)
        assert hmeas.channel_number == 314

    def test_none_acqchan_channel_number(self):
        """Test channel_number with None acqchan."""
        hmeas = HMeasurement()
        hmeas.__dict__["acqchan"] = None
        assert hmeas.channel_number == 0


if __name__ == "__main__":
    pytest.main(["-v", __file__])
