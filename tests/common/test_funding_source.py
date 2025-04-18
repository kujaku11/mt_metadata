import pytest
from pydantic import ValidationError
from mt_metadata.common.funding_source_basemodel import FundingSource


def test_funding_source_default_values():
    """
    Test the default values of the FundingSource model.
    """
    funding_source = FundingSource()

    assert funding_source.name is None
    assert funding_source.organization is None
    assert funding_source.email is None
    assert funding_source.url is None
    assert funding_source.comments is None
    assert funding_source.grant_id is None


def test_funding_source_custom_values():
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

    assert funding_source.name == "John Doe"
    assert funding_source.organization == "MT Gurus"
    assert funding_source.email == "john.doe@mtgurus.org"
    assert funding_source.url.unicode_string() == "https://mtgurus.org/"
    assert funding_source.comments == "Primary funding contact"
    assert funding_source.grant_id == "MT-01-2020"


def test_funding_source_grant_id_as_list():
    """
    Test the FundingSource model with grant_id as a list.
    """
    funding_source = FundingSource(grant_id=["MT-01-2020", "MT-02-2021"])

    assert funding_source.grant_id == ["MT-01-2020", "MT-02-2021"]


def test_funding_source_partial_values():
    """
    Test the FundingSource model with partial values.
    """
    funding_source = FundingSource(
        name="Jane Smith",
        email="jane.smith@mtgurus.org",
    )

    assert funding_source.name == "Jane Smith"
    assert funding_source.organization is None
    assert funding_source.email == "jane.smith@mtgurus.org"
    assert funding_source.url is None
    assert funding_source.comments is None
    assert funding_source.grant_id is None


def test_funding_source_invalid_email():
    """
    Test the FundingSource model with an invalid email.
    """
    with pytest.raises(ValidationError):
        FundingSource(email="invalid-email")  # Invalid email format


def test_funding_source_invalid_url():
    """
    Test the FundingSource model with an invalid URL.
    """
    with pytest.raises(ValidationError):
        FundingSource(url="invalid-url")  # Invalid URL format


def test_funding_source_invalid_grant_id_type():
    """
    Test the FundingSource model with an invalid grant_id type.
    """
    with pytest.raises(ValidationError):
        FundingSource(
            grant_id=True
        )  # grant_id must be a string, list of strings, or None
