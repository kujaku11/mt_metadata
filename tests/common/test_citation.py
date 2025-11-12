# -*- coding: utf-8 -*-
"""
Tests for the Citation model.

This module tests the Citation model's functionality including validation,
default values, and custom values.
"""

import pytest
from pydantic import ValidationError

from mt_metadata.common import Citation


@pytest.fixture(scope="module")
def default_citation():
    """Return a Citation instance with default values."""
    return Citation()


@pytest.fixture(scope="module")
def custom_citation():
    """Return a Citation instance with custom values."""
    return Citation(
        doi="https://doi.org/10.1234/example",
        authors="M.Tee A. Roura",
        title="A Study on Geophysical Phenomena",
        year="2020",
        volume="12",
        pages="10-15",
        journal="Journal of Geophysical Research",
    )


@pytest.fixture(scope="module")
def partial_citation():
    """Return a Citation instance with partial values."""
    return Citation(
        doi="https://doi.org/10.5678/example",
        title="Partial Citation Test",
    )


@pytest.fixture(
    params=[
        {"doi": "invalid-url", "error_message": "URL"},
        {"year": "20AB", "error_message": "validation error"},
    ]
)
def invalid_citation_inputs(request):
    """Return invalid citation inputs with expected error messages."""
    return request.param


def test_citation_default_values(default_citation, subtests):
    """Test the default values of the Citation model."""

    test_cases = [
        ("doi", None),
        ("authors", None),
        ("title", None),
        ("year", None),
        ("volume", None),
        ("pages", None),
        ("journal", None),
    ]

    for attribute, expected in test_cases:
        with subtests.test(msg=f"Default {attribute}"):
            assert getattr(default_citation, attribute) == expected


def test_citation_custom_values(custom_citation, subtests):
    """Test the Citation model with custom values."""

    test_cases = [
        ("doi.unicode_string()", "https://doi.org/10.1234/example"),
        ("authors", "M.Tee A. Roura"),
        ("title", "A Study on Geophysical Phenomena"),
        ("year", "2020"),
        ("volume", "12"),
        ("pages", "10-15"),
        ("journal", "Journal of Geophysical Research"),
    ]

    for attribute_expr, expected in test_cases:
        with subtests.test(msg=f"Custom {attribute_expr}"):
            if "." in attribute_expr:
                # Handle method calls like doi.unicode_string()
                obj_attr, method = attribute_expr.split(".")
                result = getattr(getattr(custom_citation, obj_attr), method[:-2])()
            else:
                result = getattr(custom_citation, attribute_expr)
            assert result == expected


def test_citation_invalid_values(invalid_citation_inputs):
    """Test the Citation model with invalid values."""
    with pytest.raises(ValidationError) as excinfo:
        Citation(**invalid_citation_inputs)

    assert invalid_citation_inputs["error_message"] in str(excinfo.value)


def test_citation_partial_values(partial_citation, subtests):
    """Test the Citation model with partial values."""

    test_cases = [
        ("doi.unicode_string()", "https://doi.org/10.5678/example"),
        ("authors", None),
        ("title", "Partial Citation Test"),
        ("year", None),
        ("volume", None),
        ("pages", None),
        ("journal", None),
    ]

    for attribute_expr, expected in test_cases:
        with subtests.test(msg=f"Partial {attribute_expr}"):
            if "." in attribute_expr:
                # Handle method calls like doi.unicode_string()
                obj_attr, method = attribute_expr.split(".")
                result = getattr(getattr(partial_citation, obj_attr), method[:-2])()
            else:
                result = getattr(partial_citation, attribute_expr)
            assert result == expected
