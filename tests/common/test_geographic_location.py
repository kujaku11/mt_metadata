import pytest
from pydantic import ValidationError

from mt_metadata.common import GeographicLocation


def test_geographic_location_default_values(subtests):
    """
    Test the default values of the GeographicLocation model.
    """
    location = GeographicLocation()

    with subtests.test("country default is None"):
        assert location.country is None

    with subtests.test("state default is None"):
        assert location.state is None

    with subtests.test("county default is None"):
        assert location.county is None

    with subtests.test("township default is None"):
        assert location.township is None

    with subtests.test("section default is None"):
        assert location.section is None

    with subtests.test("quarter default is None"):
        assert location.quarter is None

    with subtests.test("parcel default is None"):
        assert location.parcel is None


def test_geographic_location_custom_values(subtests):
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

    with subtests.test("country is set correctly"):
        assert location.country == "United States of America"

    with subtests.test("state is set correctly"):
        assert location.state == "Colorado"

    with subtests.test("county is set correctly"):
        assert location.county == "Douglas"

    with subtests.test("township is set correctly"):
        assert location.township == "090"

    with subtests.test("section is set correctly"):
        assert location.section == "012"

    with subtests.test("quarter is set correctly"):
        assert location.quarter == "400"

    with subtests.test("parcel is set correctly"):
        assert location.parcel == "46b29a"


def test_geographic_location_partial_values(subtests):
    """
    Test the GeographicLocation model with partial values.
    """
    location = GeographicLocation(
        country="Canada",
        state="Ontario",
    )

    with subtests.test("country is set correctly"):
        assert location.country == "Canada"

    with subtests.test("state is set correctly"):
        assert location.state == "Ontario"

    with subtests.test("county remains None"):
        assert location.county is None

    with subtests.test("township remains None"):
        assert location.township is None

    with subtests.test("section remains None"):
        assert location.section is None

    with subtests.test("quarter remains None"):
        assert location.quarter is None

    with subtests.test("parcel remains None"):
        assert location.parcel is None


def test_geographic_location_invalid_country_type(subtests):
    """
    Test the GeographicLocation model with an invalid country type.
    """
    with subtests.test("invalid country type raises ValidationError"):
        with pytest.raises(ValidationError):
            GeographicLocation(country=True)  # Country must be a string or None


def test_geographic_location_invalid_state_type(subtests):
    """
    Test the GeographicLocation model with an invalid state type.
    """
    with subtests.test("invalid state type raises ValidationError"):
        with pytest.raises(ValidationError):
            GeographicLocation(state=True)  # State must be a string or None


def test_geographic_location_invalid_parcel_type(subtests):
    """
    Test the GeographicLocation model with an invalid parcel type.
    """
    with subtests.test("invalid parcel type raises ValidationError"):
        with pytest.raises(ValidationError):
            GeographicLocation(parcel=True)  # Parcel must be a string or None


def test_geographic_location_with_kwargs(subtests):
    """
    Test the GeographicLocation model initialization with kwargs.
    """
    # Create a dictionary of kwargs
    kwargs = {
        "country": "Germany",
        "state": "Bavaria",
        "county": "Munich",
        "township": "123",
        "section": "456",
        "quarter": "789",
        "parcel": "abc123",
    }

    # Initialize using kwargs unpacking
    location = GeographicLocation(**kwargs)

    with subtests.test("country from kwargs is set correctly"):
        assert location.country == "Germany"

    with subtests.test("state from kwargs is set correctly"):
        assert location.state == "Bavaria"

    with subtests.test("county from kwargs is set correctly"):
        assert location.county == "Munich"

    with subtests.test("township from kwargs is set correctly"):
        assert location.township == "123"

    with subtests.test("section from kwargs is set correctly"):
        assert location.section == "456"

    with subtests.test("quarter from kwargs is set correctly"):
        assert location.quarter == "789"

    with subtests.test("parcel from kwargs is set correctly"):
        assert location.parcel == "abc123"


def test_geographic_location_with_partial_kwargs(subtests):
    """
    Test the GeographicLocation model initialization with partial kwargs.
    """
    # Create a dictionary with only some fields
    kwargs = {"country": "Australia", "state": "New South Wales"}

    # Initialize using kwargs unpacking
    location = GeographicLocation(**kwargs)

    with subtests.test("specified fields are set correctly"):
        assert location.country == "Australia"
        assert location.state == "New South Wales"

    with subtests.test("unspecified fields have default values"):
        assert location.county is None
        assert location.township is None
        assert location.section is None
        assert location.quarter is None
        assert location.parcel is None
