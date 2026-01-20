# -*- coding: utf-8 -*-
"""
Tests for the Filter and AppliedFilter classes.

This module tests functionality of Filter and AppliedFilter classes including
default values, custom values, validation, serialization, and filter operations.
"""

import pytest

from mt_metadata.timeseries import AppliedFilter

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_applied_filter():
    """Create a default AppliedFilter instance."""
    return AppliedFilter()


@pytest.fixture(scope="module")
def custom_applied_filter():
    """Create a custom AppliedFilter instance."""
    return AppliedFilter(name="low pass", applied=True, stage=1)


@pytest.fixture(scope="module")
def default_filter():
    """Create a default Filter instance."""
    return Filter()


@pytest.fixture(scope="module")
def filter_with_applied_filters():
    """Create a Filter instance with multiple AppliedFilter objects."""
    applied_filters = [
        AppliedFilter(name="low pass", applied=True, stage=1),
        AppliedFilter(name="high pass", applied=False, stage=2),
    ]
    return Filter(filter_list=applied_filters)


@pytest.fixture(scope="module")
def filter_with_comments():
    """Create a Filter instance with comments."""
    return Filter(comments="low pass filter applied")


@pytest.fixture(scope="module")
def filter_dict():
    """Create a sample dictionary for Filter testing."""
    return {
        "filter": {
            "filter_list": [
                {"applied_filter": {"name": "low pass", "applied": True, "stage": 1}},
                {"applied_filter": {"name": "high pass", "applied": False, "stage": 2}},
            ],
            "comments": {"value": "Test comment"},
        }
    }


@pytest.fixture(scope="module")
def filter_dict_no_stages():
    """Create a sample dictionary with no stages for Filter testing."""
    return {
        "filter": {
            "filter_list": [
                {"applied_filter": {"name": "low pass", "applied": True}},
                {"applied_filter": {"name": "high pass", "applied": False}},
            ],
            "comments": {"value": "Test comment"},
        }
    }


# =============================================================================
# AppliedFilter Tests
# =============================================================================


class TestAppliedFilter:
    """Tests for the AppliedFilter class."""

    def test_default_values(self, default_applied_filter, subtests):
        """Test the default values of the AppliedFilter model."""
        defaults = [
            ("name", None),
            ("applied", True),
            ("stage", None),
        ]

        for attr, expected in defaults:
            with subtests.test(msg=f"default {attr}"):
                assert getattr(default_applied_filter, attr) == expected

    def test_custom_values(self, custom_applied_filter, subtests):
        """Test the AppliedFilter model with custom values."""
        values = [
            ("name", "low pass"),
            ("applied", True),
            ("stage", 1),
        ]

        for attr, expected in values:
            with subtests.test(msg=f"custom {attr}"):
                assert getattr(custom_applied_filter, attr) == expected

    def test_invalid_name(self):
        """Test the AppliedFilter model with an invalid name type."""
        with pytest.raises(ValueError):
            AppliedFilter(name=True)  # Name must be a string
