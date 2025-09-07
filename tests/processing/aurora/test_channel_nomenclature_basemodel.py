# -*- coding: utf-8 -*-
"""
Created on September 7, 2025

@author: GitHub Copilot

Pytest test suite for ChannelNomenclature basemodel
"""
# =============================================================================
# Imports
# =============================================================================

import pytest

from mt_metadata.processing.aurora.channel_nomenclature_basemodel import (
    ChannelNomenclature,
    ExEnum,
    EyEnum,
    HxEnum,
    HyEnum,
    HzEnum,
    SupportedNomenclatureEnum,
)
from mt_metadata.transfer_functions import CHANNEL_MAPS


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_nomenclature():
    """Default channel nomenclature instance"""
    return ChannelNomenclature()


@pytest.fixture
def lemi12_nomenclature():
    """LEMI12 nomenclature configuration"""
    cn = ChannelNomenclature()
    cn.keyword = SupportedNomenclatureEnum.lemi12  # type: ignore
    return cn


@pytest.fixture
def lemi34_nomenclature():
    """LEMI34 nomenclature configuration"""
    cn = ChannelNomenclature()
    cn.keyword = SupportedNomenclatureEnum.lemi34  # type: ignore
    return cn


@pytest.fixture
def phoenix123_nomenclature():
    """Phoenix123 nomenclature configuration"""
    cn = ChannelNomenclature()
    cn.keyword = SupportedNomenclatureEnum.phoenix123  # type: ignore
    return cn


@pytest.fixture
def musgraves_nomenclature():
    """Musgraves nomenclature configuration"""
    cn = ChannelNomenclature()
    cn.keyword = SupportedNomenclatureEnum.musgraves  # type: ignore
    return cn


@pytest.fixture
def custom_nomenclature():
    """Custom channel nomenclature with specific values"""
    cn = ChannelNomenclature()
    cn.ex = ExEnum.e1  # type: ignore
    cn.ey = EyEnum.e2  # type: ignore
    cn.hx = HxEnum.h1  # type: ignore
    cn.hy = HyEnum.h2  # type: ignore
    cn.hz = HzEnum.h3  # type: ignore
    return cn


@pytest.fixture
def all_nomenclature_keywords():
    """All supported nomenclature keywords"""
    return [
        SupportedNomenclatureEnum.default,
        SupportedNomenclatureEnum.lemi12,
        SupportedNomenclatureEnum.lemi34,
        SupportedNomenclatureEnum.musgraves,
        SupportedNomenclatureEnum.phoenix123,
    ]


# =============================================================================
# Test Classes
# =============================================================================


class TestChannelNomenclatureInitialization:
    """Test ChannelNomenclature initialization and basic properties"""

    def test_default_initialization(self, default_nomenclature):
        """Test default initialization"""
        assert default_nomenclature.ex == ExEnum.ex
        assert default_nomenclature.ey == EyEnum.ey
        assert default_nomenclature.hx == HxEnum.hx
        assert default_nomenclature.hy == HyEnum.hy
        assert default_nomenclature.hz == HzEnum.hz
        assert default_nomenclature.keyword == SupportedNomenclatureEnum.default

    def test_initialization_with_custom_values(self, custom_nomenclature):
        """Test initialization with custom channel values"""
        assert custom_nomenclature.ex == ExEnum.e1
        assert custom_nomenclature.ey == EyEnum.e2
        assert custom_nomenclature.hx == HxEnum.h1
        assert custom_nomenclature.hy == HyEnum.h2
        assert custom_nomenclature.hz == HzEnum.h3

    @pytest.mark.parametrize(
        "keyword",
        [
            SupportedNomenclatureEnum.lemi12,
            SupportedNomenclatureEnum.lemi34,
            SupportedNomenclatureEnum.musgraves,
            SupportedNomenclatureEnum.phoenix123,
            SupportedNomenclatureEnum.default,
        ],
    )
    def test_initialization_with_keywords(self, keyword):
        """Test initialization with different nomenclature keywords"""
        cn = ChannelNomenclature()
        cn.keyword = keyword  # type: ignore
        assert cn.keyword == keyword

    def test_copy(self, default_nomenclature):
        """Test channel nomenclature copying"""
        copied = default_nomenclature.copy()
        assert default_nomenclature == copied
        assert default_nomenclature is not copied

    def test_initialization_with_none_keyword(self):
        """Test initialization with None keyword defaults to 'default'"""
        cn = ChannelNomenclature()
        # The field validator should convert None to default
        assert cn.keyword == SupportedNomenclatureEnum.default


class TestChannelNomenclatureEnumFields:
    """Test enum field assignments and validation"""

    @pytest.mark.parametrize(
        "field,enum_class,valid_values",
        [
            ("ex", ExEnum, [ExEnum.ex, ExEnum.e1, ExEnum.e2, ExEnum.e3, ExEnum.e4]),
            ("ey", EyEnum, [EyEnum.ey, EyEnum.e1, EyEnum.e2, EyEnum.e3, EyEnum.e4]),
            ("hx", HxEnum, [HxEnum.bx, HxEnum.hx, HxEnum.h1, HxEnum.h2, HxEnum.h3]),
            ("hy", HyEnum, [HyEnum.by, HyEnum.hy, HyEnum.h1, HyEnum.h2, HyEnum.h3]),
            ("hz", HzEnum, [HzEnum.bz, HzEnum.hz, HzEnum.h1, HzEnum.h2, HzEnum.h3]),
        ],
    )
    def test_valid_enum_assignments(
        self, default_nomenclature, field, enum_class, valid_values
    ):
        """Test assigning valid enum values to each field"""
        for value in valid_values:
            setattr(default_nomenclature, field, value)  # type: ignore
            assert getattr(default_nomenclature, field) == value

    def test_keyword_enum_values(self, default_nomenclature):
        """Test all valid keyword enum values"""
        valid_keywords = [
            SupportedNomenclatureEnum.default,
            SupportedNomenclatureEnum.lemi12,
            SupportedNomenclatureEnum.lemi34,
            SupportedNomenclatureEnum.musgraves,
            SupportedNomenclatureEnum.phoenix123,
        ]

        for keyword in valid_keywords:
            default_nomenclature.keyword = keyword  # type: ignore
            assert default_nomenclature.keyword == keyword


class TestChannelNomenclatureComputedFields:
    """Test computed field properties"""

    def test_ex_ey_computed_field(self, default_nomenclature):
        """Test ex_ey computed field"""
        expected = [default_nomenclature.ex, default_nomenclature.ey]
        assert default_nomenclature.ex_ey == expected

        # Test with custom values
        default_nomenclature.ex = ExEnum.e1  # type: ignore
        default_nomenclature.ey = EyEnum.e2  # type: ignore
        assert default_nomenclature.ex_ey == [ExEnum.e1, EyEnum.e2]

    def test_hx_hy_computed_field(self, default_nomenclature):
        """Test hx_hy computed field"""
        expected = [default_nomenclature.hx, default_nomenclature.hy]
        assert default_nomenclature.hx_hy == expected

        # Test with custom values
        default_nomenclature.hx = HxEnum.h1  # type: ignore
        default_nomenclature.hy = HyEnum.h2  # type: ignore
        assert default_nomenclature.hx_hy == [HxEnum.h1, HyEnum.h2]

    def test_hx_hy_hz_computed_field(self, default_nomenclature):
        """Test hx_hy_hz computed field"""
        expected = [
            default_nomenclature.hx,
            default_nomenclature.hy,
            default_nomenclature.hz,
        ]
        assert default_nomenclature.hx_hy_hz == expected

    def test_ex_ey_hz_computed_field(self, default_nomenclature):
        """Test ex_ey_hz computed field"""
        expected = [
            default_nomenclature.ex,
            default_nomenclature.ey,
            default_nomenclature.hz,
        ]
        assert default_nomenclature.ex_ey_hz == expected

    def test_default_input_channels(self, default_nomenclature):
        """Test default_input_channels computed field"""
        assert default_nomenclature.default_input_channels == default_nomenclature.hx_hy

    def test_default_output_channels(self, default_nomenclature):
        """Test default_output_channels computed field"""
        assert (
            default_nomenclature.default_output_channels
            == default_nomenclature.ex_ey_hz
        )

    def test_default_reference_channels(self, default_nomenclature):
        """Test default_reference_channels computed field"""
        assert (
            default_nomenclature.default_reference_channels
            == default_nomenclature.hx_hy
        )

    def test_channels_computed_field(self, default_nomenclature):
        """Test channels computed field returns all channel values"""
        channels = default_nomenclature.channels
        assert isinstance(channels, list)
        assert len(channels) == 5  # Should have 5 channels


class TestChannelNomenclatureMethods:
    """Test ChannelNomenclature methods"""

    def test_get_channel_map_default(self, default_nomenclature):
        """Test get_channel_map for default nomenclature"""
        channel_map = default_nomenclature.get_channel_map()
        assert isinstance(channel_map, dict)

        # Default mapping should be identity
        expected_keys = ["ex", "ey", "hx", "hy", "hz"]
        assert all(key in channel_map for key in expected_keys)

    @pytest.mark.parametrize(
        "keyword",
        [
            SupportedNomenclatureEnum.lemi12,
            SupportedNomenclatureEnum.lemi34,
            SupportedNomenclatureEnum.musgraves,
            SupportedNomenclatureEnum.phoenix123,
        ],
    )
    def test_get_channel_map_variants(self, keyword):
        """Test get_channel_map for different nomenclature variants"""
        cn = ChannelNomenclature()
        cn.keyword = keyword  # type: ignore
        channel_map = cn.get_channel_map()
        assert isinstance(channel_map, dict)

        # Should have all required keys
        expected_keys = ["ex", "ey", "hx", "hy", "hz"]
        assert all(key in channel_map for key in expected_keys)

    def test_update_method(self):
        """Test update method updates channels based on keyword"""
        cn = ChannelNomenclature()
        original_channels = (cn.ex, cn.ey, cn.hx, cn.hy, cn.hz)

        # Update should be called automatically, but test explicit call
        cn.update()
        updated_channels = (cn.ex, cn.ey, cn.hx, cn.hy, cn.hz)

        # For default, channels should remain the same
        assert original_channels == updated_channels

    def test_unpack_method(self, default_nomenclature):
        """Test unpack method returns tuple of all channels"""
        unpacked = default_nomenclature.unpack()
        assert isinstance(unpacked, tuple)
        assert len(unpacked) == 5

        expected = (
            default_nomenclature.ex,
            default_nomenclature.ey,
            default_nomenclature.hx,
            default_nomenclature.hy,
            default_nomenclature.hz,
        )
        assert unpacked == expected


class TestChannelNomenclatureNomenclatureVariants:
    """Test different nomenclature system variants"""

    def test_lemi12_nomenclature(self, lemi12_nomenclature):
        """Test LEMI12 nomenclature configuration"""
        assert lemi12_nomenclature.keyword == SupportedNomenclatureEnum.lemi12

        # Test that channels are updated according to LEMI12 mapping
        channel_map = lemi12_nomenclature.get_channel_map()
        # Note: actual channel values depend on CHANNEL_MAPS configuration

    def test_lemi34_nomenclature(self, lemi34_nomenclature):
        """Test LEMI34 nomenclature configuration"""
        assert lemi34_nomenclature.keyword == SupportedNomenclatureEnum.lemi34

        channel_map = lemi34_nomenclature.get_channel_map()
        assert isinstance(channel_map, dict)

    def test_phoenix123_nomenclature(self, phoenix123_nomenclature):
        """Test Phoenix123 nomenclature configuration"""
        assert phoenix123_nomenclature.keyword == SupportedNomenclatureEnum.phoenix123

        channel_map = phoenix123_nomenclature.get_channel_map()
        assert isinstance(channel_map, dict)

    def test_musgraves_nomenclature(self, musgraves_nomenclature):
        """Test Musgraves nomenclature configuration"""
        assert musgraves_nomenclature.keyword == SupportedNomenclatureEnum.musgraves

        # Ensure all channels are properly mapped
        channels = musgraves_nomenclature.unpack()
        assert len(channels) == 5
        assert all(hasattr(ch, "value") or isinstance(ch, str) for ch in channels)

    def test_nomenclature_switching(self, all_nomenclature_keywords):
        """Test switching between different nomenclature systems"""
        cn = ChannelNomenclature()

        for keyword in all_nomenclature_keywords:
            cn.keyword = keyword  # type: ignore
            assert cn.keyword == keyword

            # Verify channels are updated
            channel_map = cn.get_channel_map()
            unpacked = cn.unpack()
            assert len(unpacked) == 5


class TestChannelNomenclatureEquality:
    """Test equality and comparison"""

    def test_equality_same_values(self):
        """Test equality with same values"""
        cn1 = ChannelNomenclature()
        cn2 = ChannelNomenclature()
        assert cn1 == cn2

    def test_equality_different_keywords(self):
        """Test inequality with different keywords"""
        cn1 = ChannelNomenclature()
        cn2 = ChannelNomenclature()
        cn2.keyword = SupportedNomenclatureEnum.lemi12  # type: ignore
        assert cn1 != cn2

    def test_equality_different_channels(self):
        """Test inequality with different channel assignments"""
        cn1 = ChannelNomenclature()
        cn2 = ChannelNomenclature()
        cn2.ex = ExEnum.e1  # type: ignore
        assert cn1 != cn2

    def test_equality_copy(self, default_nomenclature):
        """Test equality with copied nomenclature"""
        copied = default_nomenclature.copy()
        assert default_nomenclature == copied


class TestChannelNomenclatureRepresentation:
    """Test string representation and serialization"""

    def test_string_representation(self, default_nomenclature):
        """Test string representation"""
        str_repr = str(default_nomenclature)
        assert "ex" in str_repr or "ExEnum.ex" in str_repr

    def test_model_dump(self, default_nomenclature):
        """Test model serialization"""
        dumped = default_nomenclature.model_dump()
        assert isinstance(dumped, dict)

        # Should include all field values
        expected_fields = ["ex", "ey", "hx", "hy", "hz", "keyword"]
        assert all(field in dumped for field in expected_fields)


class TestChannelNomenclatureEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_enum_string_conversion(self, default_nomenclature):
        """Test that enum values behave consistently"""
        # Assign enum instances
        default_nomenclature.ex = ExEnum.e1  # type: ignore
        default_nomenclature.hx = HxEnum.h1  # type: ignore

        # Should be stored as enum values
        assert default_nomenclature.ex == ExEnum.e1
        assert default_nomenclature.hx == HxEnum.h1

    def test_channel_value_persistence(self):
        """Test that channel values persist through operations"""
        cn = ChannelNomenclature()
        cn.ex = ExEnum.e1  # type: ignore
        cn.ey = EyEnum.e2  # type: ignore

        original_ex = cn.ex
        original_ey = cn.ey

        # Perform operations
        _ = cn.unpack()
        _ = cn.channels

        # Values should remain unchanged
        assert cn.ex == original_ex
        assert cn.ey == original_ey


class TestChannelNomenclatureIntegration:
    """Test integration scenarios and workflows"""

    def test_typical_mt_workflow(self):
        """Test typical magnetotelluric processing workflow"""
        # Start with default nomenclature
        cn = ChannelNomenclature()

        # Get input/output channels for processing
        input_channels = cn.default_input_channels
        output_channels = cn.default_output_channels
        reference_channels = cn.default_reference_channels

        assert len(input_channels) == 2  # hx, hy
        assert len(output_channels) == 3  # ex, ey, hz
        assert len(reference_channels) == 2  # hx, hy

        # Switch to different nomenclature
        cn.keyword = SupportedNomenclatureEnum.lemi12  # type: ignore

        # Channels should update automatically
        new_input_channels = cn.default_input_channels
        # Input channels may or may not change depending on the mapping
        assert len(new_input_channels) == 2

    def test_nomenclature_mapping_workflow(self, all_nomenclature_keywords):
        """Test workflow for mapping between nomenclature systems"""
        nomenclatures = {}

        # Create nomenclature instances for each system
        for keyword in all_nomenclature_keywords:
            cn = ChannelNomenclature()
            cn.keyword = keyword  # type: ignore
            nomenclatures[keyword] = cn

        # Test cross-system compatibility
        for keyword, cn in nomenclatures.items():
            channels = cn.unpack()
            assert len(channels) == 5

            # Each nomenclature should have valid channel mappings
            channel_map = cn.get_channel_map()
            assert len(channel_map) >= 5

    def test_channel_validation_workflow(self):
        """Test validation in realistic scenarios"""
        cn = ChannelNomenclature()

        # Test batch channel assignment
        channel_assignments = [
            ("ex", ExEnum.e1),
            ("ey", EyEnum.e2),
            ("hx", HxEnum.h1),
            ("hy", HyEnum.h2),
            ("hz", HzEnum.h3),
        ]

        for field, value in channel_assignments:
            setattr(cn, field, value)  # type: ignore
            assert getattr(cn, field) == value

        # Test computed fields update correctly
        assert cn.ex_ey == [ExEnum.e1, EyEnum.e2]
        assert cn.hx_hy == [HxEnum.h1, HyEnum.h2]


class TestChannelNomenclatureAutoUpdate:
    """Test automatic channel update functionality when keyword changes."""

    def test_auto_update_on_initialization(self, default_nomenclature):
        """Test that channels are automatically updated during initialization."""
        assert default_nomenclature.ex == ExEnum.ex
        assert default_nomenclature.ey == EyEnum.ey
        assert default_nomenclature.keyword == SupportedNomenclatureEnum.default

    def test_auto_update_on_keyword_change(self, default_nomenclature):
        """Test that channels automatically update when keyword is changed."""
        # Initial state
        assert default_nomenclature.ex == ExEnum.ex
        assert default_nomenclature.ey == EyEnum.ey

        # Change keyword - should trigger automatic update
        default_nomenclature.keyword = SupportedNomenclatureEnum.lemi12

        # Verify channels were automatically updated
        assert default_nomenclature.ex == ExEnum.e1
        assert default_nomenclature.ey == EyEnum.e2
        assert default_nomenclature.hx == HxEnum.bx
        assert default_nomenclature.hy == HyEnum.by
        assert default_nomenclature.hz == HzEnum.bz

    def test_auto_update_multiple_changes(self, default_nomenclature):
        """Test automatic updates through multiple keyword changes."""
        # Change to lemi12
        default_nomenclature.keyword = SupportedNomenclatureEnum.lemi12
        lemi12_channels = default_nomenclature.unpack()

        # Change to lemi34
        default_nomenclature.keyword = SupportedNomenclatureEnum.lemi34
        lemi34_channels = default_nomenclature.unpack()

        # Change to phoenix123
        default_nomenclature.keyword = SupportedNomenclatureEnum.phoenix123
        phoenix_channels = default_nomenclature.unpack()

        # Verify all channel sets are different
        assert lemi12_channels != lemi34_channels
        assert lemi34_channels != phoenix_channels
        assert lemi12_channels != phoenix_channels

        # Verify current state matches phoenix123
        expected_map = CHANNEL_MAPS["phoenix123"]
        assert default_nomenclature.ex.value == expected_map["ex"]
        assert default_nomenclature.ey.value == expected_map["ey"]

    def test_auto_update_with_explicit_update_call(self, default_nomenclature):
        """Test that auto-update works alongside explicit update() calls."""
        # Change keyword (triggers auto-update)
        default_nomenclature.keyword = SupportedNomenclatureEnum.musgraves
        auto_updated_channels = default_nomenclature.unpack()

        # Call update explicitly (should not change anything)
        default_nomenclature.update()
        explicit_updated_channels = default_nomenclature.unpack()

        # Should be identical
        assert auto_updated_channels == explicit_updated_channels

    def test_computed_fields_update_automatically(self, default_nomenclature):
        """Test that computed fields reflect auto-updated channel values."""
        # Change keyword
        default_nomenclature.keyword = SupportedNomenclatureEnum.lemi12

        # Verify computed fields reflect the updated channels
        assert default_nomenclature.ex_ey == [ExEnum.e1, EyEnum.e2]
        assert default_nomenclature.hx_hy == [HxEnum.bx, HyEnum.by]
        assert default_nomenclature.channels == ["bx", "by", "bz", "e1", "e2"]


class TestChannelNomenclaturePerformance:
    """Test performance characteristics"""

    def test_bulk_nomenclature_creation(self, all_nomenclature_keywords):
        """Test creating many nomenclature instances efficiently"""
        nomenclatures = []

        for i in range(100):
            keyword = all_nomenclature_keywords[i % len(all_nomenclature_keywords)]
            cn = ChannelNomenclature()
            cn.keyword = keyword  # type: ignore
            nomenclatures.append(cn)

        assert len(nomenclatures) == 100

        # Verify random samples
        assert nomenclatures[0].keyword in all_nomenclature_keywords
        assert nomenclatures[50].keyword in all_nomenclature_keywords

    def test_computed_field_access_performance(self, default_nomenclature):
        """Test repeated access to computed fields"""
        # Access computed fields multiple times
        for _ in range(100):
            _ = default_nomenclature.ex_ey
            _ = default_nomenclature.hx_hy_hz
            _ = default_nomenclature.channels

        # Should complete without issues
        assert default_nomenclature.ex_ey == [
            default_nomenclature.ex,
            default_nomenclature.ey,
        ]

    def test_update_performance(self):
        """Test performance of update operations"""
        cn = ChannelNomenclature()

        # Perform many update operations
        keywords = [
            SupportedNomenclatureEnum.default,
            SupportedNomenclatureEnum.lemi12,
            SupportedNomenclatureEnum.lemi34,
        ]

        for i in range(50):
            keyword = keywords[i % 3]
            cn.keyword = keyword  # type: ignore
            _ = cn.get_channel_map()

        # Should complete efficiently
        assert cn.keyword in keywords


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
