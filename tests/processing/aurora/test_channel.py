# -*- coding: utf-8 -*-
"""
Created on September 7, 2025

@author: GitHub Copilot

Pytest test suite for Channel basemodel
"""
# =============================================================================
# Imports
# =============================================================================

import pytest
from pydantic import ValidationError

from mt_metadata.processing.aurora.channel import Channel


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def channel_params():
    """Basic channel parameters"""
    return {
        "id": "test_channel",
        "scale_factor": 1.0,
    }


@pytest.fixture
def channel_default(channel_params):
    """Default channel instance"""
    return Channel(**channel_params)


@pytest.fixture
def channel_electric():
    """Electric field channel"""
    return Channel(id="ex", scale_factor=10.0)


@pytest.fixture
def channel_magnetic():
    """Magnetic field channel"""
    return Channel(id="hx", scale_factor=0.1)


@pytest.fixture
def channel_high_scale():
    """Channel with high scale factor"""
    return Channel(id="high_scale", scale_factor=1000.0)


@pytest.fixture
def channel_low_scale():
    """Channel with low scale factor"""
    return Channel(id="low_scale", scale_factor=0.001)


# =============================================================================
# Test Classes
# =============================================================================


class TestChannelInitialization:
    """Test Channel initialization and basic properties"""

    def test_initialization_default(self):
        """Test default initialization with minimal required parameters"""
        channel = Channel(id="test", scale_factor=1.0)
        assert channel.id == "test"
        assert channel.scale_factor == 1.0

    def test_initialization_with_params(self, channel_params):
        """Test initialization with fixture parameters"""
        channel = Channel(**channel_params)
        assert channel.id == channel_params["id"]
        assert channel.scale_factor == channel_params["scale_factor"]

    def test_initialization_empty_id(self):
        """Test initialization with empty ID"""
        channel = Channel(id="", scale_factor=1.0)
        assert channel.id == ""
        assert channel.scale_factor == 1.0

    def test_copy(self, channel_default):
        """Test channel copying"""
        cloned = channel_default.copy()
        assert channel_default == cloned
        assert channel_default is not cloned

    @pytest.mark.parametrize(
        "channel_id,expected",
        [
            ("ex", "ex"),
            ("ey", "ey"),
            ("hx", "hx"),
            ("hy", "hy"),
            ("hz", "hz"),
            ("e1", "e1"),
            ("h1", "h1"),
            ("electric_x", "electric_x"),
            ("magnetic_y", "magnetic_y"),
            ("test123", "test123"),
            ("MT001", "MT001"),
        ],
    )
    def test_id_assignment(self, channel_params, channel_id, expected):
        """Test various channel ID assignments"""
        params = channel_params.copy()
        params["id"] = channel_id
        channel = Channel(**params)
        assert channel.id == expected


class TestChannelScaleFactor:
    """Test scale factor functionality"""

    @pytest.mark.parametrize(
        "scale_factor",
        [
            0.001,
            0.1,
            1.0,
            10.0,
            100.0,
            1000.0,
            0.000001,
            1000000.0,
        ],
    )
    def test_scale_factor_values(self, channel_params, scale_factor):
        """Test various scale factor values"""
        params = channel_params.copy()
        params["scale_factor"] = scale_factor
        channel = Channel(**params)
        assert channel.scale_factor == pytest.approx(scale_factor)

    def test_scale_factor_zero(self, channel_params):
        """Test zero scale factor"""
        params = channel_params.copy()
        params["scale_factor"] = 0.0
        channel = Channel(**params)
        assert channel.scale_factor == 0.0

    def test_scale_factor_negative(self, channel_params):
        """Test negative scale factor"""
        params = channel_params.copy()
        params["scale_factor"] = -1.0
        channel = Channel(**params)
        assert channel.scale_factor == -1.0

    def test_scale_factor_precision(self, channel_params):
        """Test high precision scale factor"""
        params = channel_params.copy()
        params["scale_factor"] = 1.23456789123456789
        channel = Channel(**params)
        assert channel.scale_factor == pytest.approx(1.23456789123456789)


class TestChannelFieldValidation:
    """Test field validation and type coercion"""

    def test_id_string_coercion(self, channel_params):
        """Test ID string coercion from various types"""
        params = channel_params.copy()

        # Test integer to string conversion
        params["id"] = 123
        channel = Channel(**params)
        assert channel.id == "123"
        assert isinstance(channel.id, str)

    def test_scale_factor_type_coercion(self, channel_params):
        """Test scale factor type coercion"""
        params = channel_params.copy()

        # Test integer to float conversion
        params["scale_factor"] = 5
        channel = Channel(**params)
        assert channel.scale_factor == 5.0
        assert isinstance(channel.scale_factor, float)

        # Test string to float conversion
        params["scale_factor"] = "2.5"
        channel = Channel(**params)
        assert channel.scale_factor == 2.5
        assert isinstance(channel.scale_factor, float)

    def test_invalid_scale_factor_type(self, channel_params):
        """Test invalid scale factor types that cannot be converted"""
        params = channel_params.copy()

        # Test with non-convertible string
        params["scale_factor"] = "not_a_number"
        with pytest.raises(ValidationError):
            Channel(**params)

        # Test with complex type
        params["scale_factor"] = {"invalid": "type"}
        with pytest.raises(ValidationError):
            Channel(**params)


class TestChannelEquality:
    """Test channel equality and comparison"""

    def test_equality_same_values(self):
        """Test equality with same values"""
        channel1 = Channel(id="test", scale_factor=1.0)
        channel2 = Channel(id="test", scale_factor=1.0)
        assert channel1 == channel2

    def test_inequality_different_id(self):
        """Test inequality with different IDs"""
        channel1 = Channel(id="test1", scale_factor=1.0)
        channel2 = Channel(id="test2", scale_factor=1.0)
        assert channel1 != channel2

    def test_inequality_different_scale_factor(self):
        """Test inequality with different scale factors"""
        channel1 = Channel(id="test", scale_factor=1.0)
        channel2 = Channel(id="test", scale_factor=2.0)
        assert channel1 != channel2

    def test_equality_copy(self, channel_default):
        """Test equality with copied channel"""
        channel_copy = channel_default.copy()
        assert channel_default == channel_copy


class TestChannelRepresentation:
    """Test channel string representation and serialization"""

    def test_string_representation(self, channel_default):
        """Test string representation"""
        str_repr = str(channel_default)
        assert "test_channel" in str_repr
        assert "1.0" in str_repr

    def test_repr(self, channel_default):
        """Test repr representation"""
        repr_str = repr(channel_default)
        # Channel uses custom JSON-style repr from MetadataBase
        assert "test_channel" in repr_str
        assert "1.0" in repr_str

    def test_model_dump(self, channel_default):
        """Test model serialization"""
        channel_dict = channel_default.model_dump()
        assert channel_dict["id"] == "test_channel"
        assert channel_dict["scale_factor"] == 1.0
        assert isinstance(channel_dict, dict)


class TestChannelEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_empty_string_id(self):
        """Test empty string ID"""
        channel = Channel(id="", scale_factor=1.0)
        assert channel.id == ""

    def test_very_long_id(self, channel_params):
        """Test very long channel ID"""
        long_id = "a" * 1000
        params = channel_params.copy()
        params["id"] = long_id
        channel = Channel(**params)
        assert channel.id == long_id
        assert len(channel.id) == 1000

    def test_special_characters_in_id(self, channel_params):
        """Test special characters in channel ID"""
        special_ids = [
            "test-channel",
            "test_channel",
            "test.channel",
            "test@channel",
            "test#channel",
            "test channel",
            "test/channel",
            "test\\channel",
        ]

        for special_id in special_ids:
            params = channel_params.copy()
            params["id"] = special_id
            channel = Channel(**params)
            assert channel.id == special_id

    def test_unicode_characters_in_id(self, channel_params):
        """Test unicode characters in channel ID"""
        unicode_ids = [
            "测试",
            "тест",
            "テスト",
            "채널",
            "canal",
            "canale",
        ]

        for unicode_id in unicode_ids:
            params = channel_params.copy()
            params["id"] = unicode_id
            channel = Channel(**params)
            assert channel.id == unicode_id

    def test_extreme_scale_factors(self, channel_params):
        """Test extreme scale factor values"""
        extreme_values = [
            1e-100,
            1e-10,
            1e10,
            1e100,
            float("inf"),
            -float("inf"),
        ]

        for value in extreme_values:
            params = channel_params.copy()
            params["scale_factor"] = value
            channel = Channel(**params)
            assert channel.scale_factor == value


class TestChannelFixtureVariations:
    """Test different fixture variations"""

    def test_electric_channel(self, channel_electric):
        """Test electric field channel fixture"""
        assert channel_electric.id == "ex"
        assert channel_electric.scale_factor == 10.0

    def test_magnetic_channel(self, channel_magnetic):
        """Test magnetic field channel fixture"""
        assert channel_magnetic.id == "hx"
        assert channel_magnetic.scale_factor == 0.1

    def test_high_scale_channel(self, channel_high_scale):
        """Test high scale factor channel"""
        assert channel_high_scale.id == "high_scale"
        assert channel_high_scale.scale_factor == 1000.0

    def test_low_scale_channel(self, channel_low_scale):
        """Test low scale factor channel"""
        assert channel_low_scale.id == "low_scale"
        assert channel_low_scale.scale_factor == 0.001


class TestChannelIntegration:
    """Test integration scenarios and realistic use cases"""

    def test_typical_mt_channels(self):
        """Test typical magnetotelluric channel configurations"""
        # Standard MT channels
        channels = [
            Channel(id="hx", scale_factor=0.01),
            Channel(id="hy", scale_factor=0.01),
            Channel(id="hz", scale_factor=0.01),
            Channel(id="ex", scale_factor=100.0),
            Channel(id="ey", scale_factor=100.0),
        ]

        # Verify all channels created successfully
        assert len(channels) == 5

        # Check magnetic channels
        mag_channels = [c for c in channels if c.id.startswith("h")]
        assert len(mag_channels) == 3
        for channel in mag_channels:
            assert channel.scale_factor == 0.01

        # Check electric channels
        elec_channels = [c for c in channels if c.id.startswith("e")]
        assert len(elec_channels) == 2
        for channel in elec_channels:
            assert channel.scale_factor == 100.0

    def test_channel_list_operations(self):
        """Test operations with lists of channels"""
        channels = []

        # Create multiple channels
        for i in range(10):
            channel = Channel(id=f"channel_{i:02d}", scale_factor=float(i + 1))
            channels.append(channel)

        # Test list operations
        assert len(channels) == 10

        # Test all channels are unique by ID
        ids = [c.id for c in channels]
        assert len(set(ids)) == 10

        # Test scale factors are correct
        for i, channel in enumerate(channels):
            assert channel.scale_factor == float(i + 1)

    def test_channel_dictionary_mapping(self):
        """Test channel mapping in dictionary structures"""
        channel_configs = {
            "magnetic": {
                "hx": {"scale_factor": 0.01},
                "hy": {"scale_factor": 0.01},
                "hz": {"scale_factor": 0.01},
            },
            "electric": {
                "ex": {"scale_factor": 100.0},
                "ey": {"scale_factor": 100.0},
            },
        }

        channels = {}

        # Create channels from configuration
        for field_type, field_configs in channel_configs.items():
            for channel_id, config in field_configs.items():
                channels[channel_id] = Channel(
                    id=channel_id, scale_factor=config["scale_factor"]
                )

        # Verify channels created correctly
        assert len(channels) == 5
        assert "hx" in channels
        assert "ex" in channels
        assert channels["hx"].scale_factor == 0.01
        assert channels["ex"].scale_factor == 100.0


class TestChannelPerformance:
    """Test performance characteristics"""

    def test_bulk_channel_creation(self):
        """Test creating many channels efficiently"""
        channels = []

        # Create a large number of channels
        for i in range(1000):
            channel = Channel(id=f"bulk_channel_{i:04d}", scale_factor=i * 0.1)
            channels.append(channel)

        # Verify all channels created
        assert len(channels) == 1000

        # Verify random samples
        assert channels[0].id == "bulk_channel_0000"
        assert channels[999].id == "bulk_channel_0999"
        assert channels[500].scale_factor == pytest.approx(50.0)

    def test_channel_modification_performance(self, channel_default):
        """Test performance of channel modifications"""
        original_id = channel_default.id
        original_scale = channel_default.scale_factor

        # Perform many modifications
        for i in range(100):
            channel_default.id = f"modified_{i}"
            channel_default.scale_factor = float(i)

        # Verify final state
        assert channel_default.id == "modified_99"
        assert channel_default.scale_factor == 99.0

        # Restore original state
        channel_default.id = original_id
        channel_default.scale_factor = original_scale


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
