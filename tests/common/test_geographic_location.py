import pytest
from mt_metadata.common import GeographicLocation
from pydantic import ValidationError


def test_geographic_location_default_values():
    """
    Test the default values of the GeographicLocation model.
    """
    location = GeographicLocation()

    assert location.country is None
    assert location.state is None
    assert location.county is None
    assert location.township is None
    assert location.section is None
    assert location.quarter is None
    assert location.parcel is None


def test_geographic_location_custom_values():
    """
    Test the GeographicLocation model with custom values.
    """
    location = GeographicLocation(
        country="United States of America",
        state="Colorado",
        county="Douglas",
        township="090",
        section="012",
        quarter="400",
        parcel="46b29a",
    )

    assert location.country == "United States of America"
    assert location.state == "Colorado"
    assert location.county == "Douglas"
    assert location.township == "090"
    assert location.section == "012"
    assert location.quarter == "400"
    assert location.parcel == "46b29a"


def test_geographic_location_partial_values():
    """
    Test the GeographicLocation model with partial values.
    """
    location = GeographicLocation(
        country="Canada",
        state="Ontario",
    )

    assert location.country == "Canada"
    assert location.state == "Ontario"
    assert location.county is None
    assert location.township is None
    assert location.section is None
    assert location.quarter is None
    assert location.parcel is None


def test_geographic_location_invalid_country_type():
    """
    Test the GeographicLocation model with an invalid country type.
    """
    with pytest.raises(ValidationError):
        GeographicLocation(country=[])  # Country must be a string or None


def test_geographic_location_invalid_state_type():
    """
    Test the GeographicLocation model with an invalid state type.
    """
    with pytest.raises(ValidationError):
        GeographicLocation(state=["Colorado", "Utah"])  # State must be a string or None


def test_geographic_location_invalid_parcel_type():
    """
    Test the GeographicLocation model with an invalid parcel type.
    """
    with pytest.raises(ValidationError):
        GeographicLocation(parcel=[])  # Parcel must be a string or None
