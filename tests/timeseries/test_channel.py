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
from mt_metadata.timeseries import Channel, ChannelBase, Filter


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
            "comments": "great",
            "component": "temperature",
            "channel_number": 1,
            "data_quality.rating.author": "mt",
            "data_quality.rating.method": "ml",
            "data_quality.rating.value": 4,
            "data_quality.warnings": "No warnings",
            "filter.comments": "test",
            "filter.filter_list": [
                {
                    "applied_filter": OrderedDict(
                        [
                            ("applied", False),
                            ("name", "low_pass"),
                            ("stage", 1),
                        ]
                    )
                },
                {
                    "applied_filter": OrderedDict(
                        [
                            ("applied", True),
                            ("name", "sensor_response"),
                            ("stage", 2),
                        ]
                    )
                },
            ],
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
        "filter": (Filter, None),
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
        "filter": (Filter, None),
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
