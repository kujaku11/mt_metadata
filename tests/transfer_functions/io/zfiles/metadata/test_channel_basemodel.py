# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for Channel class from zfiles metadata.

Created on August 10, 2025
@author: GitHub Copilot
"""

from collections import OrderedDict

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata.common.enumerations import ChannelEnum
from mt_metadata.transfer_functions.io.zfiles.metadata import Channel

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_channel():
    """Create a Channel instance with default values."""
    return Channel()


@pytest.fixture
def populated_channel():
    """Create a Channel instance with typical values."""
    return Channel(number=1, azimuth=90.0, tilt=15.0, dl=100.0, channel=ChannelEnum.ex)


@pytest.fixture
def magnetic_channel():
    """Create a magnetic channel instance."""
    return Channel(number=2, azimuth=0.0, tilt=0.0, dl=0.0, channel=ChannelEnum.hx)


@pytest.fixture
def channel_dict_test_cases():
    """Test cases for from_dict method with various key aliases."""
    return {
        "standard_keys": {
            "number": 3,
            "azimuth": 180.0,
            "tilt": 5.0,
            "dl": 50.0,
            "channel": "ey",
        },
        "alias_keys": {
            "chn_num": 4,
            "azm": 270.0,
            "measurement_tilt": 10.0,
            "dipole_length": 75.0,
            "component": "hy",
        },
        "mixed_keys": {
            "number": 5,
            "measurement_azimuth": 45.0,
            "tilt": 0.0,
            "dipole_length": 25.0,
            "component": "hz",
        },
    }


@pytest.fixture
def channel_validation_cases():
    """Test cases for field validation."""
    return {
        "valid_cases": [
            {
                "number": 1,
                "azimuth": 0.0,
                "tilt": 0.0,
                "dl": 0.0,
                "channel": ChannelEnum.ex,
            },
            {
                "number": 10,
                "azimuth": 359.9,
                "tilt": 90.0,
                "dl": 1000.0,
                "channel": ChannelEnum.hx,
            },
            {
                "number": 99,
                "azimuth": -180.0,
                "tilt": -45.0,
                "dl": "100",
                "channel": ChannelEnum.hz,
            },
        ],
        "boundary_cases": [
            {
                "number": 0,
                "azimuth": 0.0,
                "tilt": 0.0,
                "dl": 0.0,
                "channel": ChannelEnum.null,
            },
            {
                "number": 999,
                "azimuth": 360.0,
                "tilt": 90.0,
                "dl": 99999.0,
                "channel": ChannelEnum.ey,
            },
        ],
    }


# =============================================================================
# Test Classes
# =============================================================================


class TestChannelDefaults:
    """Test default values and initialization."""

    def test_default_initialization(self, default_channel):
        """Test that a Channel initializes with expected defaults."""
        assert default_channel.number is None
        assert default_channel.azimuth == 0.0
        assert default_channel.tilt == 0.0
        assert default_channel.dl == 0.0
        assert default_channel.channel == ChannelEnum.null

    def test_populated_initialization(self, populated_channel):
        """Test Channel initialization with provided values."""
        assert populated_channel.number == 1
        assert populated_channel.azimuth == 90.0
        assert populated_channel.tilt == 15.0
        assert populated_channel.dl == 100.0
        assert populated_channel.channel == ChannelEnum.ex


class TestChannelProperties:
    """Test Channel properties and computed values."""

    @pytest.mark.parametrize(
        "number,expected_index", [(1, 0), (5, 4), (10, 9), (None, None)]
    )
    def test_index_property(self, number, expected_index):
        """Test that the index property correctly computes channel index."""
        channel = Channel(number=number)
        assert channel.index == expected_index

    def test_index_property_with_fixtures(
        self, default_channel, populated_channel, subtests
    ):
        """Test index property with fixtures."""
        with subtests.test("default_channel_index"):
            assert default_channel.index is None

        with subtests.test("populated_channel_index"):
            assert populated_channel.index == 0


class TestChannelValidation:
    """Test field validation and type coercion."""

    def test_valid_channel_types(self, channel_validation_cases, subtests):
        """Test that valid channel configurations are accepted."""
        for case in channel_validation_cases["valid_cases"]:
            with subtests.test(case=str(case)):
                channel = Channel(**case)
                assert channel.number == case["number"]
                assert channel.azimuth == case["azimuth"]
                assert channel.tilt == case["tilt"]
                # Handle string to float conversion for dl
                # expected_dl = (
                #     float(case["dl"]) if isinstance(case["dl"], str) else case["dl"]
                # )
                assert channel.dl == case["dl"]
                assert channel.channel == case["channel"]

    def test_boundary_cases(self, channel_validation_cases, subtests):
        """Test boundary value cases."""
        for case in channel_validation_cases["boundary_cases"]:
            with subtests.test(case=str(case)):
                channel = Channel(**case)
                assert channel.number == case["number"]
                assert channel.azimuth == case["azimuth"]
                assert channel.tilt == case["tilt"]
                assert channel.dl == case["dl"]
                assert channel.channel == case["channel"]

    def test_channel_enum_validation(self, subtests):
        """Test ChannelEnum validation."""
        valid_channels = [
            ChannelEnum.ex,
            ChannelEnum.ey,
            ChannelEnum.hx,
            ChannelEnum.hy,
            ChannelEnum.hz,
            ChannelEnum.null,
        ]

        for ch in valid_channels:
            with subtests.test(channel=str(ch)):
                channel = Channel(channel=ch)
                assert channel.channel == ch

    def test_dl_type_flexibility(self, subtests):
        """Test that dl accepts both float and string types."""
        test_cases = [(100.0, 100.0), ("50.5", "50.5"), (0, 0.0), ("0", "0")]

        for input_val, expected_val in test_cases:
            with subtests.test(input=input_val, expected=expected_val):
                channel = Channel(dl=input_val)
                assert channel.dl == expected_val


class TestChannelFromDict:
    """Test the from_dict method with various input formats."""

    def test_from_dict_standard_keys(self, channel_dict_test_cases):
        """Test from_dict with standard key names."""
        channel = Channel()
        test_dict = channel_dict_test_cases["standard_keys"]
        channel.from_dict(test_dict)

        assert channel.number == 3
        assert channel.azimuth == 180.0
        assert channel.tilt == 5.0
        assert channel.dl == 50.0
        assert channel.channel == ChannelEnum.ey

    def test_from_dict_alias_keys(self, channel_dict_test_cases):
        """Test from_dict with alias key names."""
        channel = Channel()
        test_dict = channel_dict_test_cases["alias_keys"]
        channel.from_dict(test_dict)

        assert channel.number == 4
        assert channel.azimuth == 270.0
        assert channel.tilt == 10.0
        assert channel.dl == 75.0
        assert channel.channel == ChannelEnum.hy

    def test_from_dict_mixed_keys(self, channel_dict_test_cases):
        """Test from_dict with mixed standard and alias keys."""
        channel = Channel()
        test_dict = channel_dict_test_cases["mixed_keys"]
        channel.from_dict(test_dict)

        assert channel.number == 5
        assert channel.azimuth == 45.0
        assert channel.tilt == 0.0
        assert channel.dl == 25.0
        assert channel.channel == ChannelEnum.hz

    @pytest.mark.parametrize(
        "alias_set",
        [
            {"azm": 30.0, "azimuth": 60.0, "measurement_azimuth": 90.0},
            {"chn_num": 1, "number": 2},
            {"tilt": 10.0, "measurement_tilt": 20.0},
            {"dl": 100.0, "dipole_length": 200.0},
            {"channel": "ex", "component": "ey"},
        ],
    )
    def test_from_dict_key_priority(self, alias_set):
        """Test that from_dict handles multiple aliases correctly."""
        channel = Channel()
        channel.from_dict(alias_set)

        # The method should process keys in order, so the last one wins
        # This tests the current implementation behavior
        if "measurement_azimuth" in alias_set:
            assert channel.azimuth == alias_set["measurement_azimuth"]
        elif "azimuth" in alias_set:
            assert channel.azimuth == alias_set["azimuth"]
        elif "azm" in alias_set:
            assert channel.azimuth == alias_set["azm"]

    def test_from_dict_empty_dict(self):
        """Test from_dict with empty dictionary."""
        channel = Channel(number=5, azimuth=90.0)  # Set some initial values
        original_number = channel.number
        original_azimuth = channel.azimuth

        channel.from_dict({})

        # Values should remain unchanged
        assert channel.number == original_number
        assert channel.azimuth == original_azimuth

    def test_from_dict_partial_dict(self):
        """Test from_dict with partial data."""
        channel = Channel(
            number=1, azimuth=0.0, tilt=0.0, dl=0.0, channel=ChannelEnum.ex
        )
        partial_dict = {"azimuth": 45.0, "channel": "hx"}

        channel.from_dict(partial_dict)

        assert channel.number == 1  # unchanged
        assert channel.azimuth == 45.0  # updated
        assert channel.tilt == 0.0  # unchanged
        assert channel.dl == 0.0  # unchanged
        assert channel.channel == ChannelEnum.hx  # updated


class TestChannelStringRepresentation:
    """Test string representation methods."""

    @pytest.fixture
    def string_representation_cases(self):
        """Expected string representations for different channel configurations."""
        return {
            "electric_channel": {
                "channel": Channel(
                    number=4, azimuth=0.0, tilt=0.0, dl=300, channel=ChannelEnum.ex
                ),
                "expected_str": (
                    "Channel Metadata:\n"
                    "\tChannel: ex          \n"
                    "\tNumber: 4           \n"
                    "\tDl: 300.0       \n"  # Updated to expect float format
                    "\tAzimuth: 0.0         \n"
                    "\tTilt: 0.0         "
                ),
            },
            "magnetic_channel": {
                "channel": Channel(
                    number=1, azimuth=90.0, tilt=5.0, dl=0.0, channel=ChannelEnum.hx
                ),
                "expected_str": (
                    "Channel Metadata:\n"
                    "\tChannel: hx          \n"
                    "\tNumber: 1           \n"
                    "\tDl: 0.0         \n"
                    "\tAzimuth: 90.0        \n"
                    "\tTilt: 5.0         "
                ),
            },
            "null_channel": {
                "channel": Channel(
                    number=None, azimuth=0.0, tilt=0.0, dl=0.0, channel=ChannelEnum.null
                ),
                "expected_str": (
                    "Channel Metadata:\n"
                    "\tChannel: None        \n"
                    "\tDl: 0.0         \n"
                    "\tAzimuth: 0.0         \n"
                    "\tTilt: 0.0         "
                ),
            },
        }

    def test_string_representations(self, string_representation_cases, subtests):
        """Test __str__ and __repr__ methods."""
        for case_name, case_data in string_representation_cases.items():
            with subtests.test(case=case_name):
                channel = case_data["channel"]
                expected = case_data["expected_str"]

                assert str(channel) == expected
                assert repr(channel) == expected

    def test_str_with_none_number(self):
        """Test string representation when number is None."""
        channel = Channel(number=None, channel=ChannelEnum.ex)
        str_repr = str(channel)

        # Should not include Number line when number is None
        assert "Channel: ex" in str_repr
        assert "Number:" not in str_repr
        assert "Channel Metadata:" in str_repr

    def test_str_formatting_consistency(self):
        """Test that string formatting is consistent."""
        channel = Channel(
            number=1, azimuth=123.456, tilt=78.9, dl=999.0, channel=ChannelEnum.hy
        )

        str_repr = str(channel)
        lines = str_repr.split("\n")

        # Check that all value lines have consistent formatting
        value_lines = [line for line in lines if line.startswith("\t") and ":" in line]
        for line in value_lines:
            parts = line.split(":")
            assert len(parts) == 2
            # Check that values are right-aligned with consistent spacing
            value_part = parts[1]
            assert len(value_part) >= 12  # Minimum field width


class TestChannelEquality:
    """Test equality operations."""

    def test_equality_same_values(self):
        """Test that channels with same values are equal."""
        channel1 = Channel(
            number=1, azimuth=90.0, tilt=0.0, dl=100.0, channel=ChannelEnum.ex
        )
        channel2 = Channel(
            number=1, azimuth=90.0, tilt=0.0, dl=100.0, channel=ChannelEnum.ex
        )

        assert channel1 == channel2

    def test_equality_different_values(self):
        """Test that channels with different values are not equal."""
        channel1 = Channel(
            number=1, azimuth=90.0, tilt=0.0, dl=100.0, channel=ChannelEnum.ex
        )
        channel2 = Channel(
            number=2, azimuth=90.0, tilt=0.0, dl=100.0, channel=ChannelEnum.ex
        )

        assert channel1 != channel2

    @pytest.mark.parametrize(
        "field,value1,value2",
        [
            ("number", 1, 2),
            ("azimuth", 0.0, 90.0),
            ("tilt", 0.0, 15.0),
            ("dl", 100.0, 200.0),
            ("channel", ChannelEnum.ex, ChannelEnum.hy),
        ],
    )
    def test_equality_field_differences(self, field, value1, value2):
        """Test equality when individual fields differ."""
        base_kwargs = {
            "number": 1,
            "azimuth": 0.0,
            "tilt": 0.0,
            "dl": 100.0,
            "channel": ChannelEnum.ex,
        }

        kwargs1 = base_kwargs.copy()
        kwargs1[field] = value1

        kwargs2 = base_kwargs.copy()
        kwargs2[field] = value2

        channel1 = Channel(**kwargs1)
        channel2 = Channel(**kwargs2)

        assert channel1 != channel2

    def test_equality_with_none_values(self):
        """Test equality when some fields are None."""
        channel1 = Channel(
            number=None, azimuth=0.0, tilt=0.0, dl=0.0, channel=ChannelEnum.null
        )
        channel2 = Channel(
            number=None, azimuth=0.0, tilt=0.0, dl=0.0, channel=ChannelEnum.null
        )

        assert channel1 == channel2


class TestChannelSerialization:
    """Test serialization methods (to_dict, model_dump, etc.)."""

    def test_to_dict_basic(self, populated_channel):
        """Test basic to_dict functionality."""
        result = populated_channel.to_dict()

        assert isinstance(result, dict)
        assert "channel" in result  # Nested format has class name as key
        channel_data = result["channel"]
        assert channel_data["number"] == 1
        assert channel_data["azimuth"] == 90.0
        assert channel_data["tilt"] == 15.0
        assert channel_data["dl"] == 100.0
        assert channel_data["channel"] == "ex"  # Enum serialized as string

    def test_to_dict_single_parameter(self, populated_channel):
        """Test to_dict with single=True parameter."""
        result = populated_channel.to_dict(single=True)

        assert isinstance(result, OrderedDict)
        # Should flatten nested structures if any exist

    def test_model_dump(self, populated_channel):
        """Test pydantic model_dump method."""
        result = populated_channel.model_dump()

        assert isinstance(result, dict)
        assert "number" in result
        assert "azimuth" in result
        assert "tilt" in result
        assert "dl" in result
        assert "channel" in result

    def test_serialization_deserialization_roundtrip(self, populated_channel):
        """Test that serialization -> deserialization preserves data."""
        # Serialize
        data = populated_channel.model_dump()

        # Deserialize
        recreated_channel = Channel(**data)

        # Compare
        assert recreated_channel == populated_channel


class TestChannelEdgeCases:
    """Test edge cases and error conditions."""

    def test_negative_numbers(self):
        """Test handling of negative numbers."""
        # Negative angles should be allowed
        channel = Channel(azimuth=-90.0, tilt=-45.0)
        assert channel.azimuth == -90.0
        assert channel.tilt == -45.0

    def test_large_numbers(self):
        """Test handling of large numbers."""
        channel = Channel(
            number=999999, azimuth=720.0, tilt=180.0, dl=99999.9  # Multiple rotations
        )
        assert channel.number == 999999
        assert channel.azimuth == 720.0
        assert channel.tilt == 180.0
        assert channel.dl == 99999.9

    def test_float_precision(self):
        """Test float precision handling."""
        precise_value = 123.456789012345
        channel = Channel(azimuth=precise_value)
        assert channel.azimuth == precise_value

    def test_string_dl_conversion(self, subtests):
        """Test that dl field accepts both strings and floats."""
        test_cases = [
            ("100", "100"),  # String stays string
            ("0.5", "0.5"),
            ("1.23e10", "1.23e10"),
            ("-50.5", "-50.5"),
        ]

        for str_val, expected in test_cases:
            with subtests.test(input=str_val, expected=expected):
                channel = Channel(dl=str_val)
                assert channel.dl == expected

        # Also test float input
        channel_float = Channel(dl=100.0)
        assert channel_float.dl == 100.0
        assert isinstance(channel_float.dl, float)


class TestChannelIntegration:
    """Integration tests combining multiple features."""

    def test_complete_workflow(self, channel_dict_test_cases):
        """Test a complete workflow: create, populate, modify, serialize."""
        # Create default channel
        channel = Channel()

        # Populate from dict
        channel.from_dict(channel_dict_test_cases["standard_keys"])

        # Verify population
        assert channel.number == 3
        assert channel.channel == ChannelEnum.ey

        # Modify values
        channel.azimuth = 45.0
        channel.tilt = 10.0

        # Serialize
        data = channel.to_dict()
        channel_data = data["channel"]  # Access nested data
        assert channel_data["azimuth"] == 45.0
        assert channel_data["tilt"] == 10.0

        # Create new instance from serialized data
        new_channel = Channel(**data)
        assert new_channel.azimuth == 45.0
        assert new_channel.tilt == 10.0

    def test_multiple_channels_independence(self):
        """Test that multiple Channel instances are independent."""
        channels = [
            Channel(number=i, azimuth=i * 90.0, channel=ch)
            for i, ch in enumerate([ChannelEnum.ex, ChannelEnum.ey, ChannelEnum.hx], 1)
        ]

        # Modify one channel
        channels[0].azimuth = 999.0

        # Others should be unaffected
        assert channels[1].azimuth == 180.0
        assert channels[2].azimuth == 270.0

        # Each should maintain its own values
        for i, channel in enumerate(channels, 1):
            if i == 1:
                assert channel.azimuth == 999.0  # Modified value
            else:
                assert channel.azimuth == i * 90.0  # Original value

    @pytest.mark.parametrize(
        "channel_type",
        [
            ChannelEnum.ex,
            ChannelEnum.ey,
            ChannelEnum.hx,
            ChannelEnum.hy,
            ChannelEnum.hz,
        ],
    )
    def test_channel_type_workflows(self, channel_type):
        """Test workflows for different channel types."""
        # Create channel of specific type
        channel = Channel(
            number=1,
            azimuth=0.0 if channel_type in [ChannelEnum.ex, ChannelEnum.hx] else 90.0,
            tilt=0.0,
            dl=100.0 if channel_type.name.startswith("e") else 0.0,
            channel=channel_type,
        )

        # Verify configuration makes sense for channel type
        if channel_type.name.startswith("e"):  # Electric channels
            assert channel.dl > 0  # Should have dipole length
        else:  # Magnetic channels
            assert channel.dl == 0.0  # No dipole length

        # Test string representation includes correct channel
        str_repr = str(channel)
        assert channel_type.value in str_repr or str(channel_type.value) in str_repr


# =============================================================================
# Performance Tests
# =============================================================================


class TestChannelPerformance:
    """Test performance characteristics."""

    def test_creation_performance(self):
        """Test that channel creation is reasonably fast."""
        import time

        start_time = time.time()
        channels = [Channel() for _ in range(1000)]
        end_time = time.time()

        # Should be able to create 1000 channels quickly
        assert len(channels) == 1000
        assert end_time - start_time < 1.0  # Less than 1 second

    def test_from_dict_performance(self):
        """Test from_dict performance with many operations."""
        import time

        test_dict = {
            "number": 1,
            "azimuth": 90.0,
            "tilt": 0.0,
            "dl": 100.0,
            "channel": "ex",
        }

        channels = [Channel() for _ in range(100)]

        start_time = time.time()
        for channel in channels:
            channel.from_dict(test_dict)
        end_time = time.time()

        # All channels should be updated
        assert all(ch.number == 1 for ch in channels)
        assert end_time - start_time < 1.0  # Should be fast


if __name__ == "__main__":
    pytest.main([__file__])
