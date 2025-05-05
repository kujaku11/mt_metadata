import pytest
from pydantic import ValidationError
from mt_metadata.common import BasicLocation, Location


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


def test_basic_location_default_values(default_basic_location):
    """
    Test the default values of the BasicLocation model.
    """
    location = default_basic_location

    assert location.latitude is None
    assert location.longitude is None
    assert location.elevation is None


def test_basic_location_custom_values(custom_basic_location):
    """
    Test the BasicLocation model with custom values.
    """
    location = custom_basic_location

    assert location.latitude == 45.0
    assert location.longitude == -120.0
    assert location.elevation == 500.0


def test_location_default_values():
    """
    Test the default values of the Location model.
    """
    location = Location()

    assert location.latitude == 0.0
    assert location.longitude == 0.0
    assert location.elevation == 0.0
    assert location.latitude_uncertainty is None
    assert location.longitude_uncertainty is None
    assert location.elevation_uncertainty is None
    assert location.datum == "WGS 84"
    assert location.x is None
    assert location.y is None
    assert location.z is None
    assert location.x_uncertainty is None
    assert location.y_uncertainty is None
    assert location.z_uncertainty is None


def test_location_custom_values():
    """
    Test the Location model with custom values.
    """
    location = Location(
        latitude=23.134,
        longitude=14.23,
        elevation=123.4,
        latitude_uncertainty=0.01,
        longitude_uncertainty=0.02,
        elevation_uncertainty=0.03,
        datum="NAD83",
        x=10.0,
        y=20.0,
        z=30.0,
        x_uncertainty=0.1,
        y_uncertainty=0.2,
        z_uncertainty=0.3,
    )

    assert location.latitude == 23.134
    assert location.longitude == 14.23
    assert location.elevation == 123.4
    assert location.latitude_uncertainty == 0.01
    assert location.longitude_uncertainty == 0.02
    assert location.elevation_uncertainty == 0.03
    assert location.datum == "NAD 83"
    assert location.x == 10.0
    assert location.y == 20.0
    assert location.z == 30.0
    assert location.x_uncertainty == 0.1
    assert location.y_uncertainty == 0.2
    assert location.z_uncertainty == 0.3


def test_location_invalid_latitude():
    """
    Test the Location model with an invalid latitude value.
    """
    with pytest.raises(ValidationError):
        Location(latitude=100.0)  # Latitude must be between -90 and 90


def test_location_invalid_longitude():
    """
    Test the Location model with an invalid longitude value.
    """
    with pytest.raises(ValidationError):
        Location(longitude=200.0)  # Longitude must be between -180 and 180


def test_location_invalid_datum():
    """
    Test the Location model with an invalid datum value.
    """
    with pytest.raises(ValidationError):
        Location(datum="INVALID_DATUM")  # Datum must be a valid DatumEnum value


def test_location_partial_values():
    """
    Test the Location model with partial values.
    """
    location = Location(latitude=45.0, longitude=-120.0)

    assert location.latitude == 45.0
    assert location.longitude == -120.0
    assert location.elevation == 0.0
    assert location.datum == "WGS 84"
    assert location.latitude_uncertainty is None
    assert location.longitude_uncertainty is None
    assert location.elevation_uncertainty is None


def test_location_validate_position():
    """
    Test the validate_position method for latitude and longitude.
    """
    location = Location(latitude="45:30:00", longitude="-120:15:00")

    assert location.latitude == 45.5  # Converted from DMS to decimal
    assert location.longitude == -120.25  # Converted from DMS to decimal
