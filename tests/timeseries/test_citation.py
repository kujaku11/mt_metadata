import pytest
from pydantic import ValidationError
from mt_metadata.timeseries.citation_basemodel import Citation


def test_citation_default_values():
    """
    Test the default values of the Citation model.
    """
    citation = Citation()

    assert citation.doi == ""
    assert citation.authors is None
    assert citation.title is None
    assert citation.year is None
    assert citation.volume is None
    assert citation.pages is None
    assert citation.journal is None


def test_citation_custom_values():
    """
    Test the Citation model with custom values.
    """
    citation = Citation(
        doi="http://doi.org/10.1234/example",
        authors="M.Tee A. Roura",
        title="A Study on Geophysical Phenomena",
        year="2020",
        volume="12",
        pages="10-15",
        journal="Journal of Geophysical Research",
    )

    assert citation.doi.unicode_string() == "http://doi.org/10.1234/example"
    assert citation.authors == "M.Tee A. Roura"
    assert citation.title == "A Study on Geophysical Phenomena"
    assert citation.year == "2020"
    assert citation.volume == "12"
    assert citation.pages == "10-15"
    assert citation.journal == "Journal of Geophysical Research"


def test_citation_invalid_doi():
    """
    Test the Citation model with an invalid DOI URL.
    """
    with pytest.raises(ValidationError):
        Citation(doi="invalid-url")


def test_citation_invalid_year():
    """
    Test the Citation model with an invalid year format.
    """
    with pytest.raises(ValidationError):
        Citation(year="20AB")  # Invalid year format


def test_citation_partial_values():
    """
    Test the Citation model with partial values.
    """
    citation = Citation(
        doi="http://doi.org/10.5678/example",
        title="Partial Citation Test",
    )

    assert citation.doi.unicode_string() == "http://doi.org/10.5678/example"
    assert citation.authors is None
    assert citation.title == "Partial Citation Test"
    assert citation.year is None
    assert citation.volume is None
    assert citation.pages is None
    assert citation.journal is None
