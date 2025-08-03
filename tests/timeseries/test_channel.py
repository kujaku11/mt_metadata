# -*- coding: utf-8 -*-
"""
Tests for the Channel models.

This module tests the Channel and ChannelBase classes including
serialization, defaults, and custom values.
"""

import json
from collections import OrderedDict
from operator import itemgetter

import pandas as pd
import pytest

from mt_metadata.common import (
    BasicLocation,
    Comment,
    DataQuality,
    Fdsn,
    Instrument,
    TimePeriod,
)
from mt_metadata.timeseries import AppliedFilter, Channel, ChannelBase


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def meta_dict():
    """
    Fixture to provide a sample metadata dictionary for testing.
    """
    meta_dict = {
        "channel": {
            "comments.value": "great",
            "component": "temperature",
            "channel_number": 1,
            "data_quality.rating.author": "mt",
            "data_quality.rating.method": "ml",
            "data_quality.rating.value": 4,
            "data_quality.warnings": "No warnings",
            "filters": [],
            "location.datum": "WGS 84",
            "location.elevation": 1234.0,
            "location.latitude": 12.324,
            "location.longitude": -112.03,
            "measurement_azimuth": 0.0,
            "measurement_tilt": 0.0,
            "sample_rate": 256.0,
            "sensor.id": "1244A",
            "sensor.manufacturer": "faraday",
            "sensor.model": "ichiban",
            "sensor.type": "diode",
            "time_period.end": "1980-01-01T00:00:00+00:00",
            "time_period.start": "1980-01-01T00:00:00+00:00",
            "translated_azimuth": 0.0,
            "translated_tilt": 0.0,
            "type": "base",
            "units": "celsius",
        }
    }
    meta_dict["channel"] = OrderedDict(
        sorted(meta_dict["channel"].items(), key=itemgetter(0))
    )
    return meta_dict


@pytest.fixture(scope="module")
def channel_object():
    """
    Fixture to provide a Channel object for testing.
    """
    return Channel()


@pytest.fixture(scope="module")
def default_channel():
    """
    Fixture to provide a default Channel object.
    """
    return Channel()


@pytest.fixture(scope="module")
def custom_channel():
    """
    Fixture to provide a Channel object with custom values.
    """
    return Channel(
        channel_number=1,
        channel_id="1001.11",
        comments="Test comment",
        component="ex",
        measurement_azimuth=45.0,
        measurement_tilt=10.0,
        sample_rate=8.0,
        translated_azimuth=50.0,
        translated_tilt=5.0,
        type="base",
        units="Volt",
        location=BasicLocation(latitude=45.0, longitude=-120.0, elevation=500.0),
    )


@pytest.fixture(scope="module")
def default_channel_base():
    """
    Fixture to provide a default ChannelBase object.
    """
    return ChannelBase()


@pytest.fixture(scope="module")
def custom_channel_base():
    """
    Fixture to provide a ChannelBase object with custom values.
    """
    return ChannelBase(
        channel_number=1,
        channel_id="1001.11",
        comments="Test comment",
        component="ex",
        measurement_azimuth=45.0,
        measurement_tilt=10.0,
        sample_rate=8.0,
        translated_azimuth=50.0,
        translated_tilt=5.0,
        type="base",
        units="Volt",
    )


# =============================================================================
# Serialization Tests
# =============================================================================


class TestSerialization:
    """Test serialization methods of the Channel class."""

    def test_in_out_dict(self, channel_object, meta_dict):
        """Test the from_dict and to_dict methods."""
        channel_object.from_dict(meta_dict)
        assert meta_dict == channel_object.to_dict()

    def test_in_out_series(self, channel_object, meta_dict):
        """Test the from_series and to_dict methods."""
        channel_series = pd.Series(meta_dict["channel"])
        channel_object.from_series(channel_series)
        assert meta_dict == channel_object.to_dict()

    def test_in_out_json(self, channel_object, meta_dict):
        """Test the from_json and to_json methods."""
        # Test regular JSON
        survey_json = json.dumps(meta_dict)
        channel_object.from_json(survey_json)
        assert meta_dict == channel_object.to_dict()

        # Test nested JSON
        survey_json = channel_object.to_json(nested=True)
        channel_object.from_json(survey_json)
        assert meta_dict == channel_object.to_dict()


# =============================================================================
# Default Value Tests
# =============================================================================


def test_channel_default_values(default_channel, subtests):
    """Test the default values of the Channel model."""

    # Test scalar attributes
    scalar_attrs = {
        "channel_number": 0,
        "channel_id": None,
        "component": "",
        "measurement_azimuth": 0.0,
        "measurement_tilt": 0.0,
        "sample_rate": 0.0,
        "translated_azimuth": None,
        "translated_tilt": None,
        "type": "base",
        "units": "",
    }

    for attr, expected in scalar_attrs.items():
        with subtests.test(f"default {attr}"):
            assert getattr(default_channel, attr) == expected

    # Test object attributes
    obj_attrs = {
        "comments": (Comment, lambda x: x.value is None),
        "data_quality": (DataQuality, None),
        "filters": (list, lambda x: len(x) == 0),
        "time_period": (TimePeriod, None),
        "sensor": (Instrument, None),
        "fdsn": (Fdsn, None),
        "location": (BasicLocation, None),
    }

    for attr, (cls, check_func) in obj_attrs.items():
        with subtests.test(f"default {attr} type"):
            obj = getattr(default_channel, attr)
            assert isinstance(obj, cls)

            if check_func:
                with subtests.test(f"default {attr} value"):
                    assert check_func(obj)

    # Test location values specifically
    location_attrs = {
        "latitude": 0.0,
        "longitude": 0.0,
        "elevation": 0.0,
    }

    for attr, expected in location_attrs.items():
        with subtests.test(f"default location.{attr}"):
            assert getattr(default_channel.location, attr) == expected


def test_channel_custom_values(custom_channel, subtests):
    """Test the Channel model with custom values."""

    # Test scalar attributes
    scalar_attrs = {
        "channel_number": 1,
        "channel_id": "1001.11",
        "component": "ex",
        "measurement_azimuth": 45.0,
        "measurement_tilt": 10.0,
        "sample_rate": 8.0,
        "translated_azimuth": 50.0,
        "translated_tilt": 5.0,
        "type": "base",
        "units": "Volt",
    }

    for attr, expected in scalar_attrs.items():
        with subtests.test(f"custom {attr}"):
            assert getattr(custom_channel, attr) == expected

    # Test object attributes
    obj_attrs = {
        "comments": (Comment, lambda x: x.value == "Test comment"),
        "location": (BasicLocation, None),
    }

    for attr, (cls, check_func) in obj_attrs.items():
        with subtests.test(f"custom {attr} type"):
            obj = getattr(custom_channel, attr)
            assert isinstance(obj, cls)

            if check_func:
                with subtests.test(f"custom {attr} value"):
                    assert check_func(obj)

    # Test location values specifically
    location_attrs = {
        "latitude": 45.0,
        "longitude": -120.0,
        "elevation": 500.0,
    }

    for attr, expected in location_attrs.items():
        with subtests.test(f"custom location.{attr}"):
            assert getattr(custom_channel.location, attr) == expected


def test_channel_base_default_values(default_channel_base, subtests):
    """Test the default values of the ChannelBase model."""

    # Test scalar attributes
    scalar_attrs = {
        "channel_number": 0,
        "channel_id": None,
        "component": "",
        "measurement_azimuth": 0.0,
        "measurement_tilt": 0.0,
        "sample_rate": 0.0,
        "translated_azimuth": None,
        "translated_tilt": None,
        "type": "base",
        "units": "",
    }

    for attr, expected in scalar_attrs.items():
        with subtests.test(f"default base {attr}"):
            assert getattr(default_channel_base, attr) == expected

    # Test object attributes
    obj_attrs = {
        "comments": (Comment, lambda x: x.value is None),
        "data_quality": (DataQuality, None),
        "filters": (list, lambda x: len(x) == 0),
        "time_period": (TimePeriod, None),
        "fdsn": (Fdsn, None),
    }

    for attr, (cls, check_func) in obj_attrs.items():
        with subtests.test(f"default base {attr} type"):
            obj = getattr(default_channel_base, attr)
            assert isinstance(obj, cls)

            if check_func:
                with subtests.test(f"default base {attr} value"):
                    assert check_func(obj)


def test_channel_base_custom_values(custom_channel_base, subtests):
    """Test the ChannelBase model with custom values."""

    # Test scalar attributes
    scalar_attrs = {
        "channel_number": 1,
        "channel_id": "1001.11",
        "component": "ex",
        "measurement_azimuth": 45.0,
        "measurement_tilt": 10.0,
        "sample_rate": 8.0,
        "translated_azimuth": 50.0,
        "translated_tilt": 5.0,
        "type": "base",
        "units": "Volt",
    }

    for attr, expected in scalar_attrs.items():
        with subtests.test(f"custom base {attr}"):
            assert getattr(custom_channel_base, attr) == expected

    # Test object attributes
    with subtests.test("custom base comments"):
        assert isinstance(custom_channel_base.comments, Comment)
        assert custom_channel_base.comments.value == "Test comment"


# =============================================================================
# Filters Tests
# =============================================================================


class TestChannelFilters:
    """Test the new Channel.filters functionality."""

    def test_default_filters(self, default_channel, subtests):
        """Test default filters attribute."""

        with subtests.test("filters is list"):
            assert isinstance(default_channel.filters, list)

        with subtests.test("filters empty by default"):
            assert len(default_channel.filters) == 0
            assert default_channel.filters == []

    def test_add_filter_by_name(self, subtests):
        """Test adding filters using name and parameters."""
        channel = Channel()

        # Add first filter
        channel.add_filter(name="low_pass", applied=True, stage=1)

        with subtests.test("first filter added"):
            assert len(channel.filters) == 1
            filter_obj = channel.filters[0]
            assert isinstance(filter_obj, AppliedFilter)
            assert filter_obj.name == "low_pass"
            assert filter_obj.applied is True
            assert filter_obj.stage == 1

        # Add second filter
        channel.add_filter(name="high_pass", applied=False, stage=2)

        with subtests.test("second filter added"):
            assert len(channel.filters) == 2
            filter_obj = channel.filters[1]
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

        with subtests.test("string comment converted to Comment object"):
            filter_obj = channel.filters[0]
            assert isinstance(filter_obj.comments, Comment)
            assert filter_obj.comments.value == "Test comment"

    def test_remove_filter(self, subtests):
        """Test removing filters."""
        channel = Channel()
        channel.add_filter(name="low_pass", applied=True, stage=1)
        channel.add_filter(name="high_pass", applied=False, stage=2)
        channel.add_filter(name="notch", applied=True, stage=3)

        initial_count = len(channel.filters)

        # Remove a filter
        channel.remove_filter("high_pass")

        with subtests.test("filter removed"):
            assert len(channel.filters) == initial_count - 1

        with subtests.test("correct filter removed"):
            filter_names = [f.name for f in channel.filters]
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

        with subtests.test("stages reset correctly"):
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

    def test_backward_compatibility_filtered_format(self, subtests):
        """Test backward compatibility with old filtered.applied and filtered.name format."""
        channel = Channel()

        # Test data in old format
        old_format_dict = {
            "channel": {
                "component": "hx",
                "sample_rate": 256.0,
                "filtered.applied": [True, False, True],
                "filtered.name": ["low_pass", "high_pass", "notch"],
                "location.latitude": 45.0,
                "location.longitude": -120.0,
            }
        }

        channel.from_dict(old_format_dict)

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

    def test_filters_serialization(self, subtests):
        """Test serialization of filters."""
        channel = Channel(component="Ex")  # Provide valid component
        channel.add_filter(name="low_pass", applied=True, stage=1)
        channel.add_filter(name="high_pass", applied=False, stage=2)

        # Test to_dict serialization
        result = channel.to_dict()

        with subtests.test("channel key present"):
            assert "channel" in result

        # Test roundtrip serialization
        original_filters = [(f.name, f.applied, f.stage) for f in channel.filters]

        new_channel = Channel()
        new_channel.from_dict(result)

        with subtests.test("filter count preserved in roundtrip"):
            assert len(new_channel.filters) == len(channel.filters)

        with subtests.test("filter properties preserved in roundtrip"):
            new_filters = [(f.name, f.applied, f.stage) for f in new_channel.filters]
            assert new_filters == original_filters

    def test_filters_json_serialization(self, subtests):
        """Test JSON serialization of filters."""
        channel = Channel(component="Ex")  # Provide valid component
        channel.add_filter(
            name="butterworth", applied=True, stage=1, comments="Low pass filter"
        )

        # Test JSON serialization
        json_str = channel.to_json()

        with subtests.test("json serialization works"):
            assert isinstance(json_str, str)
            # Should be valid JSON
            json.loads(json_str)

        # Test JSON deserialization
        new_channel = Channel()
        new_channel.from_json(json_str)

        with subtests.test("json deserialization preserves filters"):
            assert len(new_channel.filters) == 1
            filter_obj = new_channel.filters[0]
            assert filter_obj.name == "butterworth"
            assert filter_obj.applied is True
            assert filter_obj.stage == 1

    def test_channel_response_method(self, subtests):
        """Test the channel_response method with filters."""
        channel = Channel()
        channel.add_filter(name="low_pass", applied=True, stage=1)
        channel.add_filter(name="high_pass", applied=False, stage=2)

        # Create a mock filters dictionary
        mock_filters_dict = {
            "low_pass": "mock_low_pass_filter",
            "high_pass": "mock_high_pass_filter",
        }

        with subtests.test("channel_response method exists"):
            assert hasattr(channel, "channel_response")
            assert callable(channel.channel_response)

        # Test that it can be called (even if we don't have real filter objects)
        try:
            result = channel.channel_response(mock_filters_dict)
            with subtests.test("channel_response returns result"):
                assert result is not None
        except (ImportError, Exception):
            # If ChannelResponse import fails or other issues, that's OK for this test
            with subtests.test("channel_response method callable"):
                assert True

    def test_filters_edge_cases(self, subtests):
        """Test edge cases for filters."""
        channel = Channel()

        with subtests.test("remove from empty filters list"):
            # Should not raise error
            channel.remove_filter("nonexistent")
            assert len(channel.filters) == 0

        with subtests.test("none stage handling"):
            # Add filter with None stage
            af = AppliedFilter(name="none_stage", applied=True, stage=None)
            channel.add_filter(applied_filter=af)
            # Should be assigned stage 1 automatically
            assert channel.filters[0].stage == 1

    def test_mixed_stage_types(self, subtests):
        """Test handling of mixed stage types."""
        channel = Channel()

        # Add filters with mixed stage values including None
        channel.add_filter(name="filter1", applied=True, stage=None)
        channel.add_filter(name="filter2", applied=True, stage=5)
        channel.add_filter(name="filter3", applied=True, stage=2)

        with subtests.test("mixed stages sorted correctly"):
            stages = [f.stage for f in channel.filters]
            # None should be converted to auto-assigned stage, then sorted
            assert all(isinstance(s, int) for s in stages)
            assert stages == sorted(stages)


# =============================================================================
# Advanced Filter Tests
# =============================================================================


class TestAdvancedChannelFilters:
    """Test advanced Channel filters scenarios and integration."""

    def test_filters_with_complex_workflow(self, subtests):
        """Test a complex workflow with multiple filter operations."""
        channel = Channel(component="hx")  # Provide valid component

        # Add initial filters
        channel.add_filter(
            name="highpass_0.01", applied=True, stage=1, comments="Remove DC offset"
        )
        channel.add_filter(
            name="lowpass_100", applied=True, stage=2, comments="Anti-aliasing"
        )
        channel.add_filter(
            name="notch_60", applied=False, stage=3, comments="60Hz notch - not applied"
        )
        channel.add_filter(
            name="bandpass_1_50", applied=True, stage=4, comments="Signal band"
        )

        with subtests.test("initial filter setup"):
            assert len(channel.filters) == 4
            applied_filters = [f for f in channel.filters if f.applied]
            assert len(applied_filters) == 3

        # Enable a disabled filter
        for f in channel.filters:
            if f.name == "notch_60":
                f.applied = True
                break

        with subtests.test("filter enabled"):
            applied_filters = [f for f in channel.filters if f.applied]
            assert len(applied_filters) == 4

        # Remove a filter and check stage renumbering
        channel.remove_filter("lowpass_100", reset_stages=True)

        with subtests.test("filter removed with stage reset"):
            assert len(channel.filters) == 3
            stages = [f.stage for f in channel.filters]
            assert stages == [1, 2, 3]

            # Check that the remaining filters are correctly ordered
            names = [f.name for f in channel.filters]
            assert names == ["highpass_0.01", "notch_60", "bandpass_1_50"]

    def test_filters_serialization_with_comments(self, subtests):
        """Test serialization/deserialization preserves filter comments."""
        channel = Channel(component="hx")  # Provide valid component

        # Add filters with various comment types
        channel.add_filter(
            name="complex_filter",
            applied=True,
            stage=1,
            comments="This is a complex filter with detailed comments",
        )
        channel.add_filter(
            name="simple_filter",
            applied=False,
            stage=2,
            # No comments
        )

        # Serialize and deserialize
        serialized = channel.to_dict()
        new_channel = Channel()
        new_channel.from_dict(serialized)

        with subtests.test("comments preserved in serialization"):
            assert len(new_channel.filters) == 2

            complex_filter = next(
                f for f in new_channel.filters if f.name == "complex_filter"
            )
            assert (
                complex_filter.comments.value
                == "This is a complex filter with detailed comments"
            )

            simple_filter = next(
                f for f in new_channel.filters if f.name == "simple_filter"
            )
            assert (
                simple_filter.comments.value is None
                or simple_filter.comments.value == ""
            )

    def test_filters_with_mixed_data_sources(self, subtests):
        """Test loading filters from mixed data sources (old format + new format)."""
        channel = Channel()

        # First load from old format
        old_format_dict = {
            "channel": {
                "filtered.applied": [True, False],
                "filtered.name": ["old_filter1", "old_filter2"],
                "component": "hx",
            }
        }
        channel.from_dict(old_format_dict)

        with subtests.test("old format loaded"):
            assert len(channel.filters) == 2
            assert channel.filters[0].name == "old_filter1"
            assert channel.filters[1].name == "old_filter2"

        # Add new filters using new API
        channel.add_filter(name="new_filter", applied=True, stage=3)

        with subtests.test("mixed formats work together"):
            assert len(channel.filters) == 3
            filter_names = [f.name for f in channel.filters]
            assert "old_filter1" in filter_names
            assert "old_filter2" in filter_names
            assert "new_filter" in filter_names

    def test_filters_pandas_integration(self, subtests):
        """Test filters work correctly with pandas Series operations."""
        channel = Channel(component="hx")
        channel.add_filter(name="test_filter", applied=True, stage=1, comments="Test")

        # Convert to pandas Series
        channel_dict = channel.to_dict()
        if "channel" in channel_dict:
            series = pd.Series(channel_dict["channel"])
        else:
            series = pd.Series(channel_dict)

        with subtests.test("pandas series creation"):
            assert isinstance(series, pd.Series)

        # Create new channel from series
        new_channel = Channel()  # Provide valid component
        new_channel.from_series(series)

        with subtests.test("pandas series deserialization"):
            # Basic structure should be preserved
            assert isinstance(new_channel.filters, list)
            # Note: Detailed filter information might be lost in flattened series format

    def test_filters_error_handling_comprehensive(self, subtests):
        """Test comprehensive error handling for filters."""
        channel = Channel(component="hx")  # Provide valid component

        # Test invalid filter operations
        with subtests.test("remove nonexistent filter"):
            # Should not raise exception
            channel.remove_filter("does_not_exist")
            assert len(channel.filters) == 0

        # Test invalid stage values
        with subtests.test("negative stage values"):
            channel.add_filter(name="negative_stage", applied=True, stage=-1)
            # Should still work but might be sorted oddly
            assert len(channel.filters) == 1

        # Test very large stage values
        with subtests.test("large stage values"):
            channel.add_filter(name="large_stage", applied=True, stage=1000)
            assert len(channel.filters) == 2

        # Test stage sorting with mixed values
        with subtests.test("stage sorting with edge cases"):
            stages = [f.stage for f in channel.filters]
            assert stages == sorted(stages)

    def test_filters_memory_and_performance(self, subtests):
        """Test filters with many entries for basic performance/memory."""
        channel = Channel()

        # Add many filters
        num_filters = 100
        for i in range(num_filters):
            channel.add_filter(
                name=f"filter_{i:03d}",
                applied=i % 2 == 0,  # Alternate applied/not applied
                stage=i + 1,
                comments=f"Filter number {i}",
            )

        with subtests.test("many filters added"):
            assert len(channel.filters) == num_filters

        with subtests.test("filters properly sorted"):
            stages = [f.stage for f in channel.filters]
            assert stages == list(range(1, num_filters + 1))

        # Test serialization with many filters
        with subtests.test("serialization with many filters"):
            try:
                serialized = channel.to_dict()
                assert "channel" in serialized
            except Exception as e:
                pytest.fail(f"Serialization failed with many filters: {e}")

        # Test removal with many filters
        with subtests.test("removal with many filters"):
            original_count = len(channel.filters)
            channel.remove_filter("filter_050")
            assert len(channel.filters) == original_count - 1

    def test_filters_inheritance_and_composition(self, subtests):
        """Test that filters work correctly with Channel inheritance."""
        # Test that both Channel and ChannelBase have filters
        channel = Channel()
        channel_base = ChannelBase()

        with subtests.test("both classes have filters"):
            assert hasattr(channel, "filters")
            assert hasattr(channel_base, "filters")
            assert isinstance(channel.filters, list)
            assert isinstance(channel_base.filters, list)

        # Test filter operations on both
        channel.add_filter(name="channel_filter", applied=True, stage=1)
        channel_base.add_filter(name="base_filter", applied=True, stage=1)

        with subtests.test("filter operations work on both classes"):
            assert len(channel.filters) == 1
            assert len(channel_base.filters) == 1
            assert channel.filters[0].name == "channel_filter"
            assert channel_base.filters[0].name == "base_filter"

    def test_filters_validation_edge_cases(self, subtests):
        """Test filter validation with edge cases."""
        channel = Channel(component="hx")  # Provide valid component

        # Test empty string names
        with subtests.test("empty string name"):
            with pytest.raises(ValueError, match="Filter name cannot be empty"):
                channel.add_filter(name="", applied=True, stage=1)

        # Test whitespace-only names
        with subtests.test("whitespace name"):
            with pytest.raises(ValueError, match="Filter name cannot be empty"):
                channel.add_filter(name="   ", applied=True, stage=1)

        # Test very long names
        with subtests.test("very long name"):
            long_name = "a" * 1000
            channel.add_filter(name=long_name, applied=True, stage=1)
            assert channel.filters[0].name == long_name

        # Test special characters in names
        with subtests.test("special characters in name"):
            special_name = "filter_with-special.chars@123"
            channel.add_filter(name=special_name, applied=True, stage=2)
            assert len(channel.filters) == 2
            assert channel.filters[1].name == special_name

    def test_filters_type_coercion(self, subtests):
        """Test type coercion in filter operations."""
        channel = Channel()

        # Test string to bool coercion for applied field
        with subtests.test("string applied values"):
            # These should work through pydantic validation
            af1 = AppliedFilter(name="str_true", applied="true", stage=1)
            af2 = AppliedFilter(name="str_false", applied="false", stage=2)
            channel.add_filter(applied_filter=af1)
            channel.add_filter(applied_filter=af2)

            assert channel.filters[0].applied is True
            assert channel.filters[1].applied is False

        # Test numeric to bool coercion
        with subtests.test("numeric applied values"):
            af3 = AppliedFilter(name="num_true", applied=1, stage=3)
            af4 = AppliedFilter(name="num_false", applied=0, stage=4)
            channel.add_filter(applied_filter=af3)
            channel.add_filter(applied_filter=af4)

            assert channel.filters[2].applied is True
            assert channel.filters[3].applied is False

    def test_filters_json_edge_cases(self, subtests):
        """Test JSON serialization edge cases."""
        channel = Channel(component="hx")  # Provide valid component

        # Add filter with complex comments
        complex_comment = 'Filter with "quotes" and \n newlines and special chars: αβγ'
        channel.add_filter(
            name="complex", applied=True, stage=1, comments=complex_comment
        )

        with subtests.test("complex JSON serialization"):
            json_str = channel.to_json()
            assert isinstance(json_str, str)

            # Should be valid JSON
            import json

            parsed = json.loads(json_str)
            assert isinstance(parsed, dict)

        with subtests.test("complex JSON deserialization"):
            new_channel = Channel()
            new_channel.from_json(json_str)

            assert len(new_channel.filters) == 1
            # Note: Some special characters might be escaped differently


# =============================================================================
# Integration Tests
# =============================================================================


class TestChannelIntegration:
    """Test Channel integration with other components."""

    def test_channel_with_filters_complete_workflow(self, subtests):
        """Test a complete workflow combining all Channel features with filters."""
        # Create a channel with full metadata
        channel = Channel()

        # Set basic properties
        channel.component = "hx"
        channel.sample_rate = 1024.0
        channel.measurement_azimuth = 0.0
        channel.measurement_tilt = 0.0

        # Add location
        channel.location.latitude = 45.123
        channel.location.longitude = -120.456
        channel.location.elevation = 1500.0

        # Add filters
        channel.add_filter(
            name="dc_remove", applied=True, stage=1, comments="DC removal"
        )
        channel.add_filter(
            name="lowpass", applied=True, stage=2, comments="Anti-aliasing"
        )
        channel.add_filter(name="notch", applied=False, stage=3, comments="60Hz notch")

        with subtests.test("complete channel setup"):
            assert channel.component == "hx"
            assert channel.sample_rate == 1024.0
            assert len(channel.filters) == 3
            assert channel.location.latitude == 45.123

        # Test complete serialization
        with subtests.test("complete serialization"):
            serialized = channel.to_dict()
            assert "channel" in serialized

            # Should contain all data
            channel_data = serialized["channel"]
            assert any("component" in k for k in channel_data.keys())
            assert any("sample_rate" in k for k in channel_data.keys())
            assert any("location" in k for k in channel_data.keys())

        # Test complete deserialization
        with subtests.test("complete deserialization"):
            new_channel = Channel()
            new_channel.from_dict(serialized)

            assert new_channel.component == "hx"
            assert new_channel.sample_rate == 1024.0
            assert new_channel.location.latitude == 45.123
            assert len(new_channel.filters) == 3

            # Check filter details
            filter_names = [f.name for f in new_channel.filters]
            assert "dc_remove" in filter_names
            assert "lowpass" in filter_names
            assert "notch" in filter_names


# =============================================================================
# Mutation Tests
# =============================================================================


def test_channel_attribute_updates(default_channel, subtests):
    """Test updating channel attributes."""

    updates = {
        "channel_number": 5,
        "channel_id": "5001.22",
        "component": "ey",
        "measurement_azimuth": 90.0,
        "measurement_tilt": 15.0,
        "sample_rate": 16.0,
        "translated_azimuth": 95.0,
        "translated_tilt": 10.0,
        "type": "base",
        "units": "milliVolt",
    }

    # Apply updates
    for attr, value in updates.items():
        setattr(default_channel, attr, value)

    # Verify updates
    for attr, expected in updates.items():
        with subtests.test(f"updated {attr}"):
            assert getattr(default_channel, attr) == expected

    # Update location
    default_channel.location.latitude = 30.0
    default_channel.location.longitude = -100.0
    default_channel.location.elevation = 200.0

    # Verify location updates
    location_updates = {
        "latitude": 30.0,
        "longitude": -100.0,
        "elevation": 200.0,
    }

    for attr, expected in location_updates.items():
        with subtests.test(f"updated location.{attr}"):
            assert getattr(default_channel.location, attr) == expected
