# -*- coding: utf-8 -*-
"""
Tests for the Magnetic class in mt_metadata.timeseries using pytest

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import json
import pytest
import pandas as pd
from collections import OrderedDict
from operator import itemgetter

from mt_metadata.timeseries import Magnetic


@pytest.fixture
def magnetic_object():
    """Create a basic empty Magnetic object."""
    return Magnetic()


@pytest.fixture
def meta_dict():
    """
    Create a dictionary with typical Magnetic metadata.
    """
    meta_dict = {
        "magnetic": {
            "measurement_azimuth": 0.0,
            "measurement_tilt": 0.0,
            "channel_number": 2,
            "component": "hy",
            "data_quality.rating.author": "mt",
            "data_quality.rating.method": "ml",
            "data_quality.rating.value": 4,
            "data_quality.warnings": "No warnings",
            "location.elevation": 1230.9,
            "filter.comments": "filter comments",
            "filter.filter_list": [
                {
                    "applied_filter": OrderedDict(
                        [
                            ("applied", False),
                            ("name", "counts2mv"),
                            ("stage", 1),
                        ]
                    )
                },
            ],
            "h_field_max.end": 12.3,
            "h_field_max.start": 1200.1,
            "h_field_min.end": 12.3,
            "h_field_min.start": 1400.0,
            "location.latitude": 40.234,
            "location.longitude": -113.45,
            "location.datum": "WGS 84",
            "comments": "comments",
            "sample_rate": 256.0,
            "sensor.id": "ant2284",
            "sensor.manufacturer": "mt coils",
            "sensor.type": "induction coil",
            "sensor.model": "ant4",
            "type": "magnetic",
            "units": "millivolt",
            "time_period.start": "1980-01-01T00:00:00+00:00",
            "time_period.end": "1980-01-01T00:00:00+00:00",
            "translated_azimuth": 0.0,
            "translated_tilt": 0.0,
        }
    }

    meta_dict = {
        "magnetic": OrderedDict(
            sorted(meta_dict["magnetic"].items(), key=itemgetter(0))
        )
    }

    return meta_dict


@pytest.fixture
def populated_magnetic(magnetic_object, meta_dict):
    """Create a Magnetic object populated with test data."""
    mag = Magnetic()
    mag.from_dict(meta_dict)
    return mag


def test_in_out_dict(magnetic_object, meta_dict, subtests):
    """Test conversion from dict to Magnetic object and back to dict."""
    with subtests.test("dict to object to dict conversion preserves data"):
        magnetic_object.from_dict(meta_dict)
        assert meta_dict == magnetic_object.to_dict()


def test_in_out_series(magnetic_object, meta_dict, subtests):
    """Test conversion from pandas Series to Magnetic object and back to dict."""
    magnetic_series = pd.Series(meta_dict["magnetic"])

    with subtests.test("series to object conversion"):
        magnetic_object.from_series(magnetic_series)
        assert meta_dict == magnetic_object.to_dict()


def test_in_out_json(magnetic_object, meta_dict, subtests):
    """Test conversion from JSON to Magnetic object and back."""
    with subtests.test("JSON string to object conversion"):
        magnetic_json = json.dumps(meta_dict)
        magnetic_object.from_json(magnetic_json)
        assert meta_dict == magnetic_object.to_dict()

    with subtests.test("object to JSON and back preserves data"):
        magnetic_json = magnetic_object.to_json(nested=True)
        magnetic_object.from_json(magnetic_json)
        assert meta_dict == magnetic_object.to_dict()


# Additional pytest tests for Magnetic
def test_magnetic_initialization(subtests):
    """Test different ways to initialize a Magnetic object."""
    with subtests.test("default initialization"):
        mag = Magnetic()
        assert isinstance(mag, Magnetic)
        assert mag.type == "magnetic"

    with subtests.test("initialization with component"):
        mag = Magnetic(component="hx")
        assert mag.component == "hx"

    with subtests.test("initialization with kwargs"):
        mag = Magnetic(component="hz", sample_rate=128.0, units="nT")
        assert mag.component == "hz"
        assert mag.sample_rate == 128.0
        assert mag.units == "nanotesla"


def test_magnetic_properties(populated_magnetic, subtests):
    """Test properties of a populated Magnetic object."""
    mag = populated_magnetic

    with subtests.test("component is set correctly"):
        assert mag.component == "hy"

    with subtests.test("type is magnetic"):
        assert mag.type == "magnetic"

    with subtests.test("units are set correctly"):
        assert mag.units == "millivolt"

    with subtests.test("sample_rate is set correctly"):
        assert mag.sample_rate == 256.0

    with subtests.test("channel_number is set correctly"):
        assert mag.channel_number == 2

    with subtests.test("sensor type is set correctly"):
        assert mag.sensor.type == "induction coil"

    with subtests.test("sensor model is set correctly"):
        assert mag.sensor.model == "ant4"


def test_magnetic_location(populated_magnetic, subtests):
    """Test location properties of a Magnetic object."""
    mag = populated_magnetic

    with subtests.test("latitude is set correctly"):
        assert mag.location.latitude == 40.234

    with subtests.test("longitude is set correctly"):
        assert mag.location.longitude == -113.45

    with subtests.test("elevation is set correctly"):
        assert mag.location.elevation == 1230.9


def test_magnetic_time_period(populated_magnetic, subtests):
    """Test time period properties of a Magnetic object."""
    mag = populated_magnetic

    with subtests.test("time_period.start is set correctly"):
        assert mag.time_period.start == "1980-01-01T00:00:00+00:00"

    with subtests.test("time_period.end is set correctly"):
        assert mag.time_period.end == "1980-01-01T00:00:00+00:00"


def test_magnetic_data_quality(populated_magnetic, subtests):
    """Test data quality properties of a Magnetic object."""
    mag = populated_magnetic

    with subtests.test("data_quality.rating.author is set correctly"):
        assert mag.data_quality.rating.author == "mt"

    with subtests.test("data_quality.rating.method is set correctly"):
        assert mag.data_quality.rating.method == "ml"

    with subtests.test("data_quality.rating.value is set correctly"):
        assert mag.data_quality.rating.value == 4

    with subtests.test("data_quality.warnings is set correctly"):
        assert mag.data_quality.warnings == "No warnings"


def test_magnetic_h_field(populated_magnetic, subtests):
    """Test h_field properties of a Magnetic object."""
    mag = populated_magnetic

    with subtests.test("h_field_max.start is set correctly"):
        assert mag.h_field_max.start == 1200.1

    with subtests.test("h_field_max.end is set correctly"):
        assert mag.h_field_max.end == 12.3

    with subtests.test("h_field_min.start is set correctly"):
        assert mag.h_field_min.start == 1400.0

    with subtests.test("h_field_min.end is set correctly"):
        assert mag.h_field_min.end == 12.3


def test_magnetic_measurement(populated_magnetic, subtests):
    """Test measurement properties of a Magnetic object."""
    mag = populated_magnetic

    with subtests.test("measurement_azimuth is set correctly"):
        assert mag.measurement_azimuth == 0.0

    with subtests.test("measurement_tilt is set correctly"):
        assert mag.measurement_tilt == 0.0

    with subtests.test("translated_azimuth is set correctly"):
        assert mag.translated_azimuth == 0.0

    with subtests.test("translated_tilt is set correctly"):
        assert mag.translated_tilt == 0.0


def test_magnetic_filters(populated_magnetic, subtests):
    """Test filter properties of a Magnetic object."""
    mag = populated_magnetic

    with subtests.test("filter.applied is set correctly"):
        assert mag.filter.filter_list[0].applied is False

    with subtests.test("filter.name is set correctly"):
        assert mag.filter.filter_list[0].name == "counts2mv"

    with subtests.test("filter.comments is set correctly"):
        assert mag.filter.comments.value == "filter comments"


def test_magnetic_with_kwargs(subtests):
    """Test creating a Magnetic object with kwargs."""
    # Create with initial kwargs
    kwargs = {
        "component": "hz",
        "sample_rate": 128.0,
        "sensor.type": "fluxgate",
        "sensor.model": "fgm-5",
        "measurement_azimuth": 90.0,
        "measurement_tilt": 0.0,
        "location.latitude": 35.6,
        "location.longitude": -105.2,
        "location.elevation": 2200.0,
    }

    mag = Magnetic(**kwargs)

    with subtests.test("component is set from kwargs"):
        assert mag.component == "hz"

    with subtests.test("sample_rate is set from kwargs"):
        assert mag.sample_rate == 128.0

    with subtests.test("sensor.type is set from kwargs"):
        assert mag.sensor.type == "fluxgate"

    with subtests.test("sensor.model is set from kwargs"):
        assert mag.sensor.model == "fgm-5"

    with subtests.test("measurement_azimuth is set from kwargs"):
        assert mag.measurement_azimuth == 90.0

    with subtests.test("location properties are set from kwargs"):
        assert mag.location.latitude == 35.6
        assert mag.location.longitude == -105.2
        assert mag.location.elevation == 2200.0


# def test_magnetic_validation(subtests):
#     """Test validation of a Magnetic object."""
#     # Create a valid magnetic object
#     mag = Magnetic(component="hx")

#     with subtests.test("valid object passes validation"):
#         assert mag.validate() is True

#     # Test invalid component
#     invalid_mag = Magnetic()

#     with subtests.test("missing component fails validation"):
#         try:
#             result = invalid_mag.validate()
#             assert result is False
#         except Exception as e:
#             # If it raises an exception instead, that's also acceptable
#             assert "component" in str(e).lower()
