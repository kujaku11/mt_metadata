# -*- coding: utf-8 -*-
"""
Basic functionality test to verify our modernized testing approach works.
"""
import pytest

from mt_metadata.transfer_functions.io.zfiles.metadata import Channel


class TestChannelBasicFunctionality:
    """Test basic Channel functionality without complex ZMM integration."""

    def test_channel_creation(self):
        """Test that we can create a Channel object."""
        channel = Channel(channel="ex", number=4, dl="300.0", azimuth=0.0, tilt=0.0)

        assert channel.channel == "ex"
        assert channel.number == 4
        assert channel.dl == "300.0"
        assert channel.azimuth == 0.0
        assert channel.tilt == 0.0

    @pytest.mark.parametrize("channel_name", ["ex", "ey", "hx", "hy", "hz"])
    def test_parametrized_channel_creation(self, channel_name, subtests):
        """Test parametrized channel creation with subtests."""
        channel = Channel(
            channel=channel_name, number=1, dl="300.0", azimuth=0.0, tilt=0.0
        )

        with subtests.test(attribute="channel"):
            assert channel.channel == channel_name

        with subtests.test(attribute="string_representation"):
            str_repr = str(channel)
            assert channel_name in str_repr
            assert "300" in str_repr

    def test_channel_validation(self, subtests):
        """Test channel validation with invalid values."""

        with subtests.test(test="invalid_channel"):
            with pytest.raises(Exception):  # Will catch validation errors
                Channel(channel="invalid", number=1, dl="300.0", azimuth=0.0, tilt=0.0)
