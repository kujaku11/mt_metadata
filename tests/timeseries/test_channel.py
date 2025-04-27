import pytest
import json
import pandas as pd
from collections import OrderedDict
from operator import itemgetter

from mt_metadata.timeseries.channel_basemodel import (
    Channel,
    BasicLocation,
    ChannelBase,
)
from mt_metadata.common import (
    Comment,
    Instrument,
    DataQuality,
    TimePeriod,
    Fdsn,
)
from mt_metadata.timeseries.filtered_basemodel import Filtered


@pytest.fixture
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
            "location.datum": "WGS84",
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
            "type": "auxiliary",
            "units": "celsius",
        }
    }
    meta_dict["channel"] = OrderedDict(
        sorted(meta_dict["channel"].items(), key=itemgetter(0))
    )
    return meta_dict


@pytest.fixture
def channel_object():
    """
    Fixture to provide a Channel object for testing.
    """
    return Channel()


def test_in_out_dict(channel_object, meta_dict):
    """
    Test the from_dict and to_dict methods of the Channel class.
    """
    channel_object.from_dict(meta_dict)
    assert meta_dict == channel_object.to_dict()


def test_in_out_series(channel_object, meta_dict):
    """
    Test the from_series and to_dict methods of the Channel class.
    """
    channel_series = pd.Series(meta_dict["channel"])
    channel_object.from_series(channel_series)
    assert meta_dict == channel_object.to_dict()


def test_in_out_json(channel_object, meta_dict):
    """
    Test the from_json and to_json methods of the Channel class.
    """
    survey_json = json.dumps(meta_dict)
    channel_object.from_json(survey_json)
    assert meta_dict == channel_object.to_dict()

    survey_json = channel_object.to_json(nested=True)
    channel_object.from_json(survey_json)
    assert meta_dict == channel_object.to_dict()


@pytest.fixture
def default_channel():
    """
    Fixture to provide a default Channel object.
    """
    return Channel()


@pytest.fixture
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
        type="electric",
        units="volt",
        location=BasicLocation(latitude=45.0, longitude=-120.0, elevation=500.0),
    )


@pytest.fixture
def default_basic_location():
    """
    Fixture to provide a default BasicLocation object.
    """
    return BasicLocation()


@pytest.fixture
def custom_basic_location():
    """
    Fixture to provide a BasicLocation object with custom values.
    """
    return BasicLocation(latitude=45.0, longitude=-120.0, elevation=500.0)


@pytest.fixture
def default_channel_base():
    """
    Fixture to provide a default ChannelBase object.
    """
    return ChannelBase()


@pytest.fixture
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
        type="electric",
        units="volt",
    )


def test_channel_default_values(default_channel):
    """
    Test the default values of the Channel model.
    """
    channel = default_channel

    assert channel.channel_number is None
    assert channel.channel_id is None
    assert isinstance(channel.comments, Comment)
    assert channel.comments.value is None
    assert channel.component == ""
    assert channel.measurement_azimuth == 0.0
    assert channel.measurement_tilt == 0.0
    assert channel.sample_rate == 0.0
    assert channel.translated_azimuth is None
    assert channel.translated_tilt is None
    assert channel.type == ""
    assert channel.units == ""
    assert isinstance(channel.data_quality, DataQuality)
    assert isinstance(channel.filter, Filtered)
    assert isinstance(channel.time_period, TimePeriod)
    assert isinstance(channel.sensor, Instrument)
    assert isinstance(channel.fdsn, Fdsn)
    assert isinstance(channel.location, BasicLocation)
    assert channel.location.latitude is None
    assert channel.location.longitude is None
    assert channel.location.elevation is None


def test_channel_custom_values(custom_channel):
    """
    Test the Channel model with custom values.
    """
    channel = custom_channel

    assert channel.channel_number == 1
    assert channel.channel_id == "1001.11"
    assert isinstance(channel.comments, Comment)
    assert channel.comments.value == "Test comment"
    assert channel.component == "ex"
    assert channel.measurement_azimuth == 45.0
    assert channel.measurement_tilt == 10.0
    assert channel.sample_rate == 8.0
    assert channel.translated_azimuth == 50.0
    assert channel.translated_tilt == 5.0
    assert channel.type == "electric"
    assert channel.units == "volt"
    assert isinstance(channel.location, BasicLocation)
    assert channel.location.latitude == 45.0
    assert channel.location.longitude == -120.0
    assert channel.location.elevation == 500.0


def test_channel_base_default_values(default_channel_base):
    """
    Test the default values of the ChannelBase model.
    """
    channel_base = default_channel_base

    assert channel_base.channel_number is None
    assert channel_base.channel_id is None
    assert isinstance(channel_base.comments, Comment)
    assert channel_base.comments.value is None
    assert channel_base.component == ""
    assert channel_base.measurement_azimuth == 0.0
    assert channel_base.measurement_tilt == 0.0
    assert channel_base.sample_rate == 0.0
    assert channel_base.translated_azimuth is None
    assert channel_base.translated_tilt is None
    assert channel_base.type == ""
    assert channel_base.units == ""
    assert isinstance(channel_base.data_quality, DataQuality)
    assert isinstance(channel_base.filter, Filtered)
    assert isinstance(channel_base.time_period, TimePeriod)
    assert isinstance(channel_base.fdsn, Fdsn)


def test_channel_base_custom_values(custom_channel_base):
    """
    Test the ChannelBase model with custom values.
    """
    channel_base = custom_channel_base

    assert channel_base.channel_number == 1
    assert channel_base.channel_id == "1001.11"
    assert isinstance(channel_base.comments, Comment)
    assert channel_base.comments.value == "Test comment"
    assert channel_base.component == "ex"
    assert channel_base.measurement_azimuth == 45.0
    assert channel_base.measurement_tilt == 10.0
    assert channel_base.sample_rate == 8.0
    assert channel_base.translated_azimuth == 50.0
    assert channel_base.translated_tilt == 5.0
    assert channel_base.type == "electric"
    assert channel_base.units == "volt"
