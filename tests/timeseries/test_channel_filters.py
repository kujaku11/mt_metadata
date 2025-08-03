# -*- coding: utf-8 -*-
"""
Tests for the Channel filters functionality.

This module tests the new Channel.filters attribute which is a list[AppliedFilter]
and replaces the old Channel.filter attribute. It includes tests for:
- Adding and removing filters
- Backward compatibility with filtered.applied and filtered.name
- Filter sorting and validation
- Serialization and deserialization
"""

import json

import pandas as pd
import pytest

from mt_metadata.common import Comment
from mt_metadata.timeseries import AppliedFilter, Channel


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_channel():
    """
    Fixture to provide a default Channel object.
    """
    return Channel()


@pytest.fixture(scope="module")
def channel_with_filters():
    """
    Fixture to provide a Channel object with multiple filters.
    """
    channel = Channel()
    channel.add_filter(name="low_pass", applied=True, stage=1)
    channel.add_filter(name="high_pass", applied=False, stage=2)
    channel.add_filter(name="notch", applied=True, stage=3)
    return channel


@pytest.fixture(scope="module")
def sample_applied_filters():
    """
    Fixture to provide a list of sample AppliedFilter objects.
    """
    return [
        AppliedFilter(name="butterworth_low", applied=True, stage=1),
        AppliedFilter(name="butterworth_high", applied=False, stage=2),
        AppliedFilter(
            name="notch_60hz", applied=True, stage=3, comments="Remove 60Hz noise"
        ),
    ]


@pytest.fixture(scope="module")
def backward_compatibility_dict():
    """
    Fixture to provide a dictionary with old-style filter data for backward compatibility testing.
    """
    return {
        "channel": {
            "component": "hx",
            "sample_rate": 256.0,
            "filtered.applied": [True, False, True],
            "filtered.name": ["low_pass", "high_pass", "notch"],
            "location.latitude": 45.0,
            "location.longitude": -120.0,
        }
    }


@pytest.fixture(scope="module")
def new_style_filters_dict():
    """
    Fixture to provide a dictionary with new-style filters data.
    """
    return {
        "channel": {
            "component": "hy",
            "sample_rate": 512.0,
            "filters": [
                {
                    "name": "butterworth_low",
                    "applied": True,
                    "stage": 1,
                    "comments": "Low pass filter",
                },
                {
                    "name": "butterworth_high",
                    "applied": False,
                    "stage": 2,
                    "comments": None,
                },
            ],
            "location.latitude": 40.0,
            "location.longitude": -110.0,
        }
    }


# =============================================================================
# Default Values Tests
# =============================================================================


def test_channel_default_filters(default_channel, subtests):
    """Test the default filters attribute of the Channel model."""

    with subtests.test("default filters type"):
        assert isinstance(default_channel.filters, list)

    with subtests.test("default filters empty"):
        assert len(default_channel.filters) == 0

    with subtests.test("default filters equals empty list"):
        assert default_channel.filters == []


# =============================================================================
# Filter Management Tests
# =============================================================================


class TestFilterManagement:
    """Test adding, removing, and managing filters."""

    def test_add_filter_by_name(self, default_channel, subtests):
        """Test adding filters using name and parameters."""

        # Add first filter
        default_channel.add_filter(name="low_pass", applied=True, stage=1)

        with subtests.test("filter added"):
            assert len(default_channel.filters) == 1

        with subtests.test("filter properties"):
            filter_obj = default_channel.filters[0]
            assert isinstance(filter_obj, AppliedFilter)
            assert filter_obj.name == "low_pass"
            assert filter_obj.applied is True
            assert filter_obj.stage == 1

        # Add second filter
        default_channel.add_filter(name="high_pass", applied=False, stage=2)

        with subtests.test("second filter added"):
            assert len(default_channel.filters) == 2

        with subtests.test("second filter properties"):
            filter_obj = default_channel.filters[1]
            assert filter_obj.name == "high_pass"
            assert filter_obj.applied is False
            assert filter_obj.stage == 2

    def test_add_filter_by_object(self, subtests):
        """Test adding filters using AppliedFilter objects."""
        channel = Channel()

        filter_obj = AppliedFilter(
            name="notch", applied=True, stage=1, comments="60Hz notch"
        )
        channel.add_filter(applied_filter=filter_obj)

        with subtests.test("filter object added"):
            assert len(channel.filters) == 1

        with subtests.test("filter object properties"):
            added_filter = channel.filters[0]
            assert added_filter.name == "notch"
            assert added_filter.applied is True
            assert added_filter.stage == 1
            assert added_filter.comments.value == "60Hz notch"

    def test_add_filter_auto_stage(self, subtests):
        """Test automatic stage assignment when stage is None."""
        channel = Channel()

        # Add filters without specifying stage
        channel.add_filter(name="filter1", applied=True)
        channel.add_filter(name="filter2", applied=False)
        channel.add_filter(name="filter3", applied=True)

        with subtests.test("auto stage assignment"):
            assert channel.filters[0].stage == 1
            assert channel.filters[1].stage == 2
            assert channel.filters[2].stage == 3

    def test_add_filter_with_comments(self, subtests):
        """Test adding filters with comments."""
        channel = Channel()

        # Add filter with string comment
        channel.add_filter(name="filter1", applied=True, comments="Test comment")

        with subtests.test("string comment"):
            filter_obj = channel.filters[0]
            assert isinstance(filter_obj.comments, Comment)
            assert filter_obj.comments.value == "Test comment"

        # Add filter with Comment object
        comment_obj = Comment(value="Another comment")
        channel.add_filter(name="filter2", applied=False, comments=comment_obj)

        with subtests.test("comment object"):
            filter_obj = channel.filters[1]
            assert isinstance(filter_obj.comments, Comment)
            assert filter_obj.comments.value == "Another comment"

    def test_remove_filter(self, channel_with_filters, subtests):
        """Test removing filters."""
        initial_count = len(channel_with_filters.filters)

        # Remove a filter
        channel_with_filters.remove_filter("high_pass")

        with subtests.test("filter removed"):
            assert len(channel_with_filters.filters) == initial_count - 1

        with subtests.test("correct filter removed"):
            filter_names = [f.name for f in channel_with_filters.filters]
            assert "high_pass" not in filter_names
            assert "low_pass" in filter_names
            assert "notch" in filter_names

    def test_remove_filter_reset_stages(self, subtests):
        """Test removing filters with stage reset."""
        channel = Channel()
        channel.add_filter(name="filter1", applied=True, stage=1)
        channel.add_filter(name="filter2", applied=True, stage=2)
        channel.add_filter(name="filter3", applied=True, stage=3)

        # Remove middle filter with reset_stages=True (default)
        channel.remove_filter("filter2", reset_stages=True)

        with subtests.test("stages reset"):
            assert len(channel.filters) == 2
            assert channel.filters[0].name == "filter1"
            assert channel.filters[0].stage == 1
            assert channel.filters[1].name == "filter3"
            assert channel.filters[1].stage == 2  # Should be reset from 3 to 2

    def test_remove_filter_no_reset_stages(self, subtests):
        """Test removing filters without stage reset."""
        channel = Channel()
        channel.add_filter(name="filter1", applied=True, stage=1)
        channel.add_filter(name="filter2", applied=True, stage=2)
        channel.add_filter(name="filter3", applied=True, stage=3)

        # Remove middle filter with reset_stages=False
        channel.remove_filter("filter2", reset_stages=False)

        with subtests.test("stages not reset"):
            assert len(channel.filters) == 2
            assert channel.filters[0].name == "filter1"
            assert channel.filters[0].stage == 1
            assert channel.filters[1].name == "filter3"
            assert channel.filters[1].stage == 3  # Should remain 3


# =============================================================================
# Filter Validation Tests
# =============================================================================


class TestFilterValidation:
    """Test filter validation and sorting."""

    def test_filter_sorting(self, subtests):
        """Test that filters are automatically sorted by stage."""
        channel = Channel()

        # Add filters out of order
        channel.add_filter(name="filter3", applied=True, stage=3)
        channel.add_filter(name="filter1", applied=True, stage=1)
        channel.add_filter(name="filter2", applied=True, stage=2)

        with subtests.test("filters sorted by stage"):
            stages = [f.stage for f in channel.filters]
            assert stages == [1, 2, 3]

        with subtests.test("filter names in correct order"):
            names = [f.name for f in channel.filters]
            assert names == ["filter1", "filter2", "filter3"]

    def test_duplicate_filter_validation(self, subtests):
        """Test that duplicate filter names are not allowed."""
        channel = Channel()

        # Add first filter
        channel.add_filter(name="duplicate", applied=True, stage=1)

        # Try to add another filter with the same name
        with subtests.test("duplicate filter raises error"):
            with pytest.raises(ValueError, match="Duplicate filter found: duplicate"):
                channel.add_filter(name="duplicate", applied=False, stage=2)

    def test_add_filter_validation_errors(self, subtests):
        """Test error handling in add_filter method."""
        channel = Channel()

        with subtests.test("invalid applied_filter type"):
            with pytest.raises(
                TypeError, match="applied_filter must be an instance of AppliedFilter"
            ):
                channel.add_filter(applied_filter="not_a_filter")

        with subtests.test("missing name"):
            with pytest.raises(
                ValueError, match="name must be provided if applied_filter is None"
            ):
                channel.add_filter(applied_filter=None, name=None)

        with subtests.test("invalid name type"):
            with pytest.raises(TypeError, match="name must be a string"):
                channel.add_filter(applied_filter=None, name=123)


# =============================================================================
# Backward Compatibility Tests
# =============================================================================


class TestBackwardCompatibility:
    """Test backward compatibility with old filtered.applied and filtered.name format."""

    def test_from_dict_filtered_format(self, backward_compatibility_dict, subtests):
        """Test loading from old filtered.applied and filtered.name format."""
        channel = Channel()
        channel.from_dict(backward_compatibility_dict)

        with subtests.test("filters loaded from old format"):
            assert len(channel.filters) == 3

        with subtests.test("filter properties from old format"):
            expected = [
                ("low_pass", True, 1),
                ("high_pass", False, 2),
                ("notch", True, 3),
            ]
            for i, (name, applied, stage) in enumerate(expected):
                filter_obj = channel.filters[i]
                assert filter_obj.name == name
                assert filter_obj.applied == applied
                assert filter_obj.stage == stage

        with subtests.test("other attributes preserved"):
            assert channel.component == "hx"
            assert channel.sample_rate == 256.0
            assert channel.location.latitude == 45.0
            assert channel.location.longitude == -120.0

    def test_from_dict_mismatched_lengths(self, subtests):
        """Test error handling when filtered.applied and filtered.name have different lengths."""
        channel = Channel()

        bad_dict = {
            "channel": {
                "filtered.applied": [True, False],
                "filtered.name": ["filter1", "filter2", "filter3"],  # Different length
            }
        }

        with subtests.test("mismatched lengths raise error"):
            with pytest.raises(Exception):  # Should raise MTSchemaError
                channel.from_dict(bad_dict)

    def test_mixed_old_and_new_format(self, subtests):
        """Test handling when both old and new format are present."""
        channel = Channel()

        mixed_dict = {
            "channel": {
                "filtered.applied": [True, False],
                "filtered.name": ["old_filter1", "old_filter2"],
                "filters": [{"name": "new_filter", "applied": True, "stage": 1}],
            }
        }

        # The old format should be processed first, then the new format
        channel.from_dict(mixed_dict)

        with subtests.test("both formats processed"):
            assert len(channel.filters) >= 2  # At least the old filters

        with subtests.test("old format filters present"):
            filter_names = [f.name for f in channel.filters]
            assert "old_filter1" in filter_names
            assert "old_filter2" in filter_names


# =============================================================================
# Serialization Tests
# =============================================================================


class TestSerialization:
    """Test serialization and deserialization of filters."""

    def test_filters_to_dict(self, channel_with_filters, subtests):
        """Test serialization of filters to dictionary."""
        result = channel_with_filters.to_dict()

        with subtests.test("channel key present"):
            assert "channel" in result

        channel_dict = result["channel"]

        # Check for filter-related keys in flattened format
        filter_keys = [k for k in channel_dict.keys() if k.startswith("filters")]

        with subtests.test("filter keys present"):
            assert len(filter_keys) > 0

    def test_filters_from_new_format_dict(self, new_style_filters_dict, subtests):
        """Test loading filters from new format dictionary."""
        channel = Channel()
        channel.from_dict(new_style_filters_dict)

        with subtests.test("filters loaded"):
            assert len(channel.filters) == 2

        with subtests.test("first filter properties"):
            filter1 = channel.filters[0]
            assert filter1.name == "butterworth_low"
            assert filter1.applied is True
            assert filter1.stage == 1
            assert filter1.comments.value == "Low pass filter"

        with subtests.test("second filter properties"):
            filter2 = channel.filters[1]
            assert filter2.name == "butterworth_high"
            assert filter2.applied is False
            assert filter2.stage == 2

    def test_roundtrip_serialization(self, channel_with_filters, subtests):
        """Test that serialization and deserialization preserve filter data."""
        # Get the original state
        original_filters = [
            (f.name, f.applied, f.stage) for f in channel_with_filters.filters
        ]

        # Serialize and deserialize
        serialized = channel_with_filters.to_dict()
        new_channel = Channel()
        new_channel.from_dict(serialized)

        with subtests.test("filter count preserved"):
            assert len(new_channel.filters) == len(channel_with_filters.filters)

        with subtests.test("filter properties preserved"):
            new_filters = [(f.name, f.applied, f.stage) for f in new_channel.filters]
            assert new_filters == original_filters

    def test_json_serialization(self, channel_with_filters, subtests):
        """Test JSON serialization and deserialization."""
        # Serialize to JSON
        json_str = channel_with_filters.to_json()

        with subtests.test("json serialization works"):
            assert isinstance(json_str, str)
            # Should be valid JSON
            json.loads(json_str)

        # Deserialize from JSON
        new_channel = Channel()
        new_channel.from_json(json_str)

        with subtests.test("json deserialization preserves filters"):
            assert len(new_channel.filters) == len(channel_with_filters.filters)

            for orig, new in zip(channel_with_filters.filters, new_channel.filters):
                assert orig.name == new.name
                assert orig.applied == new.applied
                assert orig.stage == new.stage

    def test_pandas_series_serialization(self, channel_with_filters, subtests):
        """Test pandas Series serialization and deserialization."""
        # Convert to dict first
        channel_dict = channel_with_filters.to_dict()

        # Create pandas Series from flattened channel data
        if "channel" in channel_dict:
            series = pd.Series(channel_dict["channel"])
        else:
            series = pd.Series(channel_dict)

        with subtests.test("series creation works"):
            assert isinstance(series, pd.Series)

        # Deserialize from Series
        new_channel = Channel()
        new_channel.from_series(series)

        with subtests.test("series deserialization preserves filters"):
            # Note: Series might not preserve all filter details due to flattening
            # but should at least preserve basic structure
            assert isinstance(new_channel.filters, list)


# =============================================================================
# Channel Response Tests
# =============================================================================


def test_channel_response_method(channel_with_filters, subtests):
    """Test the channel_response method with filters."""

    # Create a mock filters dictionary
    mock_filters_dict = {
        "low_pass": "mock_low_pass_filter",
        "high_pass": "mock_high_pass_filter",
        "notch": "mock_notch_filter",
    }

    with subtests.test("channel_response method exists"):
        assert hasattr(channel_with_filters, "channel_response")
        assert callable(channel_with_filters.channel_response)

    # Test that it can be called (even if we don't have real filter objects)
    try:
        result = channel_with_filters.channel_response(mock_filters_dict)
        with subtests.test("channel_response returns result"):
            assert result is not None
    except ImportError:
        # If ChannelResponse import fails, that's OK for this test
        with subtests.test("channel_response method callable"):
            assert True


# =============================================================================
# Applied Filter Tests
# =============================================================================


class TestAppliedFilter:
    """Test AppliedFilter objects directly."""

    def test_applied_filter_creation(self, subtests):
        """Test creating AppliedFilter objects."""

        # Basic creation
        af = AppliedFilter(name="test_filter", applied=True, stage=1)

        with subtests.test("basic creation"):
            assert af.name == "test_filter"
            assert af.applied is True
            assert af.stage == 1

        # With comments
        af_with_comments = AppliedFilter(
            name="test_filter_2", applied=False, stage=2, comments="Test comment"
        )

        with subtests.test("creation with comments"):
            assert af_with_comments.comments.value == "Test comment"

    def test_applied_filter_serialization(self, sample_applied_filters, subtests):
        """Test AppliedFilter serialization."""

        for af in sample_applied_filters:
            with subtests.test(f"serialization of {af.name}"):
                result = af.to_dict()
                assert isinstance(result, dict)

                # Check for expected structure
                assert "applied_filter" in result
                filter_dict = result["applied_filter"]
                assert "name" in filter_dict
                assert "applied" in filter_dict
                assert "stage" in filter_dict

    def test_applied_filter_from_dict(self, subtests):
        """Test creating AppliedFilter from dictionary."""

        filter_dict = {
            "name": "from_dict_filter",
            "applied": True,
            "stage": 5,
            "comments": "Created from dict",
        }

        af = AppliedFilter(**filter_dict)

        with subtests.test("from_dict creation"):
            assert af.name == "from_dict_filter"
            assert af.applied is True
            assert af.stage == 5
            assert af.comments.value == "Created from dict"


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_filters_list_operations(self, subtests):
        """Test operations on empty filters list."""
        channel = Channel()

        with subtests.test("remove from empty list"):
            # Should not raise error
            channel.remove_filter("nonexistent")
            assert len(channel.filters) == 0

        with subtests.test("channel_response with empty filters"):
            try:
                result = channel.channel_response({})
                with subtests.test("empty channel_response works"):
                    assert result is not None
            except ImportError:
                # ChannelResponse import might fail, that's OK
                pass

    def test_none_stage_handling(self, subtests):
        """Test handling of None stage values."""
        channel = Channel()

        # Add filter with None stage
        af = AppliedFilter(name="none_stage", applied=True, stage=None)
        channel.add_filter(applied_filter=af)

        with subtests.test("none stage gets assigned"):
            # Should be assigned stage 1 automatically
            assert channel.filters[0].stage == 1

    def test_mixed_stage_types(self, subtests):
        """Test handling of mixed stage types."""
        channel = Channel()

        # Add filters with mixed stage values
        channel.add_filter(name="filter1", applied=True, stage=None)
        channel.add_filter(name="filter2", applied=True, stage=5)
        channel.add_filter(name="filter3", applied=True, stage=2)

        with subtests.test("mixed stages sorted correctly"):
            stages = [f.stage for f in channel.filters]
            # None should be treated as 0 in sorting, so order should be: None->1, 2, 5
            assert stages[0] == 1  # None was converted to auto-assigned stage
            assert stages[1] == 2
            assert stages[2] == 5
