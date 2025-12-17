# -*- coding: utf-8 -*-
"""
Tests for the Provenance model.

This module tests the Provenance model's functionality including validation,
default values, custom values, and time format handling.
"""

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from mt_metadata.common import AuthorPerson, Person, Provenance, Software


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_provenance():
    """Return a Provenance instance with default values."""
    return Provenance()


@pytest.fixture(scope="module")
def custom_provenance():
    """Return a Provenance instance with custom values."""
    return Provenance(
        creation_time="2023-05-01T12:00:00+00:00",
        comments="Data created for testing.",
        log="2023-05-02T14:00:00+00:00 updated metadata",
        creator=AuthorPerson(name="J. Pedantic", email="jped@mt.com"),
        submitter=AuthorPerson(name="Submitter Name", email="submitter@email.com"),
        archive=Person(name="Archive Name", url="https://archive.url"),
        software=Software(name="mt_metadata", version="0.1"),
    )


@pytest.fixture(scope="module")
def partial_provenance():
    """Return a Provenance instance with partial values."""
    return Provenance(
        comments="Partial data",
        creator=AuthorPerson(name="J. Pedantic"),
    )


@pytest.fixture(
    scope="module",
    params=[
        1682942400.0,  # Epoch time
        np.datetime64("2023-05-01T12:00:00"),  # numpy datetime64 (UTC assumed)
        pd.Timestamp("2023-05-01T12:00:00+00:00"),  # pandas Timestamp
    ],
)
def time_formats(request):
    """Return different valid time format values for testing."""
    return request.param


@pytest.fixture(
    params=[
        {
            "attr": "creator",
            "value": "invalid_creator",
            "error_msg": "validation error",
        },
        {
            "attr": "software",
            "value": "invalid_software",
            "error_msg": "validation error",
        },
    ]
)
def invalid_types(request):
    """Return invalid type values with expected error messages."""
    return request.param


# =============================================================================
# Tests
# =============================================================================


def test_provenance_default_values(default_provenance, subtests):
    """Test the default values of the Provenance model."""
    test_cases = [
        ("creation_time", "1980-01-01T00:00:00+00:00"),
        ("comments.value", None),
        ("log", None),
        ("creator", AuthorPerson),
        ("submitter", AuthorPerson),
        ("archive", Person),
        ("software", Software),
    ]

    for attr_expr, expected in test_cases:
        with subtests.test(attr_expr):
            obj = default_provenance.get_attr_from_name(attr_expr)
            if isinstance(expected, type):
                assert isinstance(obj, expected)
            else:
                assert obj == expected


def test_provenance_custom_values(custom_provenance, subtests):
    """Test the Provenance model with custom values."""
    test_cases = [
        ("creation_time", "2023-05-01T12:00:00+00:00"),
        ("comments.value", "Data created for testing."),
        ("log", "2023-05-02T14:00:00+00:00 updated metadata"),
        ("creator.author", "J. Pedantic"),
        ("creator.email", "jped@mt.com"),
        ("submitter.author", "Submitter Name"),
        ("submitter.email", "submitter@email.com"),
        ("archive.name", "Archive Name"),
        ("archive.url.unicode_string()", "https://archive.url/"),
        ("software.name", "mt_metadata"),
        ("software.version", "0.1"),
    ]

    for attr_expr, expected in test_cases:
        with subtests.test(attr_expr):
            result = _get_attr_or_method_result(custom_provenance, attr_expr)
            assert result == expected


def test_provenance_partial_values(partial_provenance, subtests):
    """Test the Provenance model with partial values."""
    test_cases = [
        ("comments.value", "Partial data"),
        ("creator.author", "J. Pedantic"),
        ("creator.email", None),
        ("submitter.author", ""),
        ("archive.name", ""),
        ("software.name", ""),
    ]

    for attr_expr, expected in test_cases:
        with subtests.test(attr_expr):
            result = _get_attr_or_method_result(partial_provenance, attr_expr)
            assert result == expected


def test_provenance_invalid_creation_time():
    """Test the Provenance model with an invalid creation_time value."""
    with pytest.raises(ValidationError) as excinfo:
        Provenance(creation_time="invalid-date")
    assert "time data" in str(excinfo.value) or "format" in str(excinfo.value)


def test_provenance_creation_time_formats(time_formats, subtests):
    """Test the Provenance model with different valid time formats."""
    provenance = Provenance(creation_time=time_formats)
    with subtests.test("creation_time conversion"):
        assert provenance.creation_time.isoformat() == "2023-05-01T12:00:00+00:00"


def test_provenance_invalid_types(invalid_types):
    """Test the Provenance model with invalid types."""
    with pytest.raises((ValidationError, AttributeError)) as excinfo:
        kwargs = {invalid_types["attr"]: invalid_types["value"]}
        Provenance(**kwargs)
    assert invalid_types["error_msg"] in str(excinfo.value)


# =============================================================================
# Helper functions
# =============================================================================


def _get_nested_attr(obj, attr_path):
    """Get nested attribute from object using dot notation."""
    parts = attr_path.split(".")
    for part in parts:
        obj = getattr(obj, part)
    return obj


def _get_attr_or_method_result(obj, attr_expr):
    """Get attribute value or method result from object expression."""
    if "(" in attr_expr and ")" in attr_expr:
        # Extract method name and arguments
        parts = attr_expr.split(".")
        for i, part in enumerate(parts):
            if "(" in part:
                method_name = part.split("(")[0]
                args_str = part.split("(")[1].split(")")[0]
                args = [arg.strip() for arg in args_str.split(",")] if args_str else []

                # Navigate to the object
                current_obj = obj
                for j in range(i):
                    current_obj = getattr(current_obj, parts[j])

                # Call the method
                method = getattr(current_obj, method_name)
                return method(*args)
    elif "." in attr_expr:
        parts = attr_expr.split(".")
        current = obj
        for part in parts:
            current = getattr(current, part)
        return current
    else:
        return getattr(obj, attr_expr)
