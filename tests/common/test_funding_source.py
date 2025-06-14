import pytest
from pydantic import ValidationError
from mt_metadata.common import FundingSource


def test_funding_source_default_values(subtests):
    """
    Test the default values of the FundingSource model.
    """
    funding_source = FundingSource()

    with subtests.test("name default is None"):
        assert funding_source.name is None

    with subtests.test("organization default is None"):
        assert funding_source.organization is None

    with subtests.test("email default is None"):
        assert funding_source.email is None

    with subtests.test("url default is None"):
        assert funding_source.url is None

    with subtests.test("comments default is None"):
        assert funding_source.comments.value is None

    with subtests.test("grant_id default is None"):
        assert funding_source.grant_id is None


def test_funding_source_custom_values(subtests):
    """
    Test the FundingSource model with custom values.
    """
    funding_source = FundingSource(
        name="John Doe",
        organization="MT Gurus",
        email="john.doe@mtgurus.org",
        url="https://mtgurus.org",
        comments="Primary funding contact",
        grant_id="MT-01-2020",
    )

    with subtests.test("name is set correctly"):
        assert funding_source.name == ["John Doe"]

    with subtests.test("organization is set correctly"):
        assert funding_source.organization == ["MT Gurus"]

    with subtests.test("email is set correctly"):
        assert funding_source.email == ["john.doe@mtgurus.org"]

    with subtests.test("url is set correctly"):
        assert [funding_source.url[0].unicode_string()] == ["https://mtgurus.org/"]

    with subtests.test("comments is set correctly"):
        assert funding_source.comments == "Primary funding contact"

    with subtests.test("grant_id is set correctly"):
        assert funding_source.grant_id == ["MT-01-2020"]


def test_funding_source_grant_id_as_list(subtests):
    """
    Test the FundingSource model with grant_id as a list.
    """
    funding_source = FundingSource(grant_id=["MT-01-2020", "MT-02-2021"])

    with subtests.test("grant_id as list is set correctly"):
        assert funding_source.grant_id == ["MT-01-2020", "MT-02-2021"]


def test_funding_source_partial_values(subtests):
    """
    Test the FundingSource model with partial values.
    """
    funding_source = FundingSource(
        name="Jane Smith",
        email="jane.smith@mtgurus.org",
    )

    with subtests.test("name is set correctly"):
        assert funding_source.name == ["Jane Smith"]

    with subtests.test("organization remains None"):
        assert funding_source.organization is None

    with subtests.test("email is set correctly"):
        assert funding_source.email == ["jane.smith@mtgurus.org"]

    with subtests.test("url remains None"):
        assert funding_source.url is None

    with subtests.test("comments remains None"):
        assert funding_source.comments.value is None

    with subtests.test("grant_id remains None"):
        assert funding_source.grant_id is None


def test_funding_source_invalid_email(subtests):
    """
    Test the FundingSource model with an invalid email.
    """
    with subtests.test("invalid email raises ValidationError"):
        with pytest.raises(ValidationError):
            FundingSource(email="invalid-email")  # Invalid email format


def test_funding_source_invalid_url(subtests):
    """
    Test the FundingSource model with an invalid URL.
    """
    with subtests.test("invalid URL raises ValidationError"):
        with pytest.raises(ValidationError):
            FundingSource(url="invalid-url")  # Invalid URL format


def test_funding_source_invalid_grant_id_type(subtests):
    """
    Test the FundingSource model with an invalid grant_id type.
    """
    with subtests.test("invalid grant_id type raises ValidationError"):
        with pytest.raises(TypeError):
            FundingSource(
                grant_id=True
            )  # grant_id must be a string, list of strings, or None


def test_funding_source_with_kwargs(subtests):
    """
    Test the FundingSource model initialization with kwargs.
    """
    # Create a dictionary of kwargs
    kwargs = {
        "name": "Research Foundation",
        "organization": "University Labs",
        "email": "grants@university.edu",
        "url": "https://research.university.edu",
        "comments": "Multi-year funding",
        "grant_id": ["GRANT-2023-001", "GRANT-2023-002"],
    }

    # Initialize using kwargs unpacking
    funding_source = FundingSource(**kwargs)

    with subtests.test("name from kwargs is set correctly"):
        assert funding_source.name == ["Research Foundation"]

    with subtests.test("organization from kwargs is set correctly"):
        assert funding_source.organization == ["University Labs"]

    with subtests.test("email from kwargs is set correctly"):
        assert funding_source.email == ["grants@university.edu"]

    with subtests.test("url from kwargs is set correctly"):
        assert [funding_source.url[0].unicode_string()] == [
            "https://research.university.edu/"
        ]

    with subtests.test("comments from kwargs is set correctly"):
        assert funding_source.comments == "Multi-year funding"

    with subtests.test("grant_id from kwargs is set correctly"):
        assert funding_source.grant_id == ["GRANT-2023-001", "GRANT-2023-002"]


def test_funding_source_with_partial_kwargs(subtests):
    """
    Test the FundingSource model initialization with partial kwargs.
    """
    # Create a dictionary with only some fields
    kwargs = {"name": "Industry Partner", "grant_id": "IND-2023-XYZ"}

    # Initialize using kwargs unpacking
    funding_source = FundingSource(**kwargs)

    with subtests.test("specified fields are set correctly"):
        assert funding_source.name == ["Industry Partner"]
        assert funding_source.grant_id == ["IND-2023-XYZ"]

    with subtests.test("unspecified fields have default values"):
        assert funding_source.organization is None
        assert funding_source.email is None
        assert funding_source.url is None
        assert funding_source.comments.value is None
