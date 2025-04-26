import pytest

from mt_metadata.timeseries.channel_basemodel import (
    Channel,
    PartialLocation,
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


def test_channel_default_values():
    """
    Test the default values of the Channel model.
    """
    channel = Channel()

    assert channel.channel_number is None
    assert channel.channel_id is None
    assert isinstance(channel.comments, Comment)
    assert channel.comments.value == None
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
    assert isinstance(channel.location, PartialLocation)
    assert channel.location.latitude is None
    assert channel.location.longitude is None
    assert channel.location.elevation is None


def test_channel_custom_values():
    """
    Test the Channel model with custom values.
    """
    channel = Channel(
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
        location=PartialLocation(latitude=45.0, longitude=-120.0, elevation=500.0),
    )

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
    assert isinstance(channel.location, PartialLocation)
    assert channel.location.latitude == 45.0
    assert channel.location.longitude == -120.0
    assert channel.location.elevation == 500.0


def test_channel_partial_values():
    """
    Test the Channel model with partial values.
    """
    channel = Channel(
        channel_number=2,
        component="hx",
        location=PartialLocation(latitude="30.0"),
    )

    assert channel.channel_number == 2
    assert channel.component == "hx"
    assert isinstance(channel.location, PartialLocation)
    assert channel.location.latitude == 30.0
    assert channel.location.longitude is None
    assert channel.location.elevation is None


def test_channel_invalid_channel_number():
    """
    Test the Channel model with an invalid channel_number.
    """
    with pytest.raises(ValueError):
        Channel(channel_number="invalid")  # channel_number must be an integer


def test_channel_invalid_component():
    """
    Test the Channel model with an invalid component.
    """
    with pytest.raises(ValueError):
        Channel(component=[])  # component must be a string


def test_channel_invalid_units():
    """
    Test the Channel model with an invalid units value.
    """
    with pytest.raises(TypeError):
        Channel(units=12345)  # units must be a string or a valid UnitsEnum value


def test_channel_validate_comments_with_string():
    """
    Test the validate_comments method with a string input.
    """
    channel = Channel(comments="This is a test comment.")

    assert isinstance(channel.comments, Comment)
    assert channel.comments.value == "This is a test comment."


def test_channel_validate_comments_with_comment_object():
    """
    Test the validate_comments method with a Comment object.
    """
    comment = Comment(value="This is a test comment.")
    channel = Channel(comments=comment)

    assert channel.comments == comment


def test_partial_location_default_values():
    """
    Test the default values of the PartialLocation model.
    """
    location = PartialLocation()

    assert location.latitude is None
    assert location.longitude is None
    assert location.elevation is None


def test_partial_location_custom_values():
    """
    Test the PartialLocation model with custom values.
    """
    location = PartialLocation(latitude=45.0, longitude=-120.0, elevation=500.0)

    assert location.latitude == 45.0
    assert location.longitude == -120.0
    assert location.elevation == 500.0


def test_partial_location_invalid_latitude():
    """
    Test the PartialLocation model with an invalid latitude.
    """
    with pytest.raises(ValueError):
        PartialLocation(latitude="invalid")  # latitude must be a float or None


def test_partial_location_invalid_longitude():
    """
    Test the PartialLocation model with an invalid longitude.
    """
    with pytest.raises(TypeError):
        PartialLocation(longitude=["invalid"])  # longitude must be a float or None


def test_partial_location_invalid_elevation():
    """
    Test the PartialLocation model with an invalid elevation.
    """
    with pytest.raises(ValueError):
        PartialLocation(
            elevation={"invalid": "value"}
        )  # elevation must be a float or None


def test_channel_base_default_values():
    """
    Test the default values of the ChannelBase model.
    """
    channel_base = ChannelBase()

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


def test_channel_base_custom_values():
    """
    Test the ChannelBase model with custom values.
    """
    channel_base = ChannelBase(
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


def test_channel_base_invalid_component():
    """
    Test the ChannelBase model with an invalid component.
    """
    with pytest.raises(ValueError):
        ChannelBase(component=[])  # component must be a string


def test_channel_base_invalid_units():
    """
    Test the ChannelBase model with an invalid units value.
    """
    with pytest.raises(TypeError):
        ChannelBase(units=12345)  # units must be a string or a valid UnitsEnum value
