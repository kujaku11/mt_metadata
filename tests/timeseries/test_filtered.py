# -*- coding: utf-8 -*-
"""
Tests for the Filter and AppliedFilter classes.

This module tests functionality of Filter and AppliedFilter classes including
default values, custom values, validation, serialization, and filter operations.
"""

import pytest

from mt_metadata.common import Comment
from mt_metadata.timeseries import AppliedFilter, Filter


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


# =============================================================================
# Filter Tests
# =============================================================================


class TestFilter:
    """Tests for the Filter class."""

    def test_default_values(self, default_filter, subtests):
        """Test the default values of the Filter model."""
        with subtests.test(msg="default filter_list"):
            assert default_filter.filter_list == []

        with subtests.test(msg="default comments"):
            assert default_filter.comments.value is None

    def test_with_applied_filters(self, filter_with_applied_filters, subtests):
        """Test the Filter model with a list of AppliedFilter objects."""
        with subtests.test(msg="filter_list length"):
            assert len(filter_with_applied_filters.filter_list) == 2

        with subtests.test(msg="first filter name"):
            assert filter_with_applied_filters.filter_list[0].name == "low pass"

        with subtests.test(msg="second filter name"):
            assert filter_with_applied_filters.filter_list[1].name == "high pass"

    def test_with_comments(self, filter_with_comments, subtests):
        """Test the Filter model with comments."""
        with subtests.test(msg="comments type"):
            assert isinstance(filter_with_comments.comments, Comment)

        with subtests.test(msg="comments value"):
            assert filter_with_comments.comments.value == "low pass filter applied"

    def test_to_dict(self, filter_with_applied_filters, subtests):
        """Test the to_dict method of the Filter model."""
        result = filter_with_applied_filters.to_dict(single=True)

        with subtests.test(msg="to_dict structure"):
            assert "filter_list" in result
            assert len(result["filter_list"]) == 2

        expected_filters = [
            {"applied_filter": {"name": "low pass", "applied": True, "stage": 1}},
            {"applied_filter": {"name": "high pass", "applied": False, "stage": 2}},
        ]

        for i, expected in enumerate(expected_filters):
            with subtests.test(msg=f"to_dict filter {i}"):
                assert result["filter_list"][i] == expected

    def test_from_dict(self, filter_dict, subtests):
        """Test the from_dict method of the Filter model."""
        filtered = Filter()
        filtered.from_dict(filter_dict)

        with subtests.test(msg="filter_list length"):
            assert len(filtered.filter_list) == 2

        with subtests.test(msg="first filter"):
            assert filtered.filter_list[0].name == "low pass"
            assert filtered.filter_list[0].applied is True
            assert filtered.filter_list[0].stage == 1

        with subtests.test(msg="second filter"):
            assert filtered.filter_list[1].name == "high pass"
            assert filtered.filter_list[1].applied is False
            assert filtered.filter_list[1].stage == 2

        with subtests.test(msg="comments"):
            assert isinstance(filtered.comments, Comment)
            assert filtered.comments.value == "Test comment"

    def test_from_kwargs(self, filter_dict, subtests):
        """Test initializing Filter with keyword arguments."""
        filtered = Filter(**filter_dict)

        with subtests.test(msg="filter_list length"):
            assert len(filtered.filter_list) == 2

        with subtests.test(msg="first filter"):
            assert filtered.filter_list[0].name == "low pass"
            assert filtered.filter_list[0].stage == 1

        with subtests.test(msg="second filter"):
            assert filtered.filter_list[1].name == "high pass"
            assert filtered.filter_list[1].stage == 2

        with subtests.test(msg="comments"):
            assert filtered.comments.value == "Test comment"

    def test_from_dict_without_stage(self, filter_dict_no_stages, subtests):
        """Test the from_dict method when the stage is not provided."""
        filtered = Filter()
        filtered.from_dict(filter_dict_no_stages)

        with subtests.test(msg="filter_list length"):
            assert len(filtered.filter_list) == 2

        for i, name in enumerate(["low pass", "high pass"]):
            with subtests.test(msg=f"filter {i} name"):
                assert filtered.filter_list[i].name == name

            with subtests.test(msg=f"filter {i} stage"):
                assert filtered.filter_list[i].stage is None

    def test_invalid_filter_list(self):
        """Test the Filter model with an invalid filter_list type."""
        with pytest.raises(ValueError):
            Filter(
                filter_list="invalid"
            )  # filter_list must be a list of AppliedFilter objects


class TestFilterModifications:
    """Tests for Filter modification operations."""

    def test_add_filter_object(self, default_filter, subtests):
        """Test adding an AppliedFilter object to the Filter."""
        applied_filter = AppliedFilter(name="low pass", applied=True, stage=1)
        default_filter.add_filter(applied_filter)

        with subtests.test(msg="filter_list length after add"):
            assert len(default_filter.filter_list) == 1

        with subtests.test(msg="added filter name"):
            assert default_filter.filter_list[0].name == "low pass"

        with subtests.test(msg="added filter applied"):
            assert default_filter.filter_list[0].applied is True

        with subtests.test(msg="added filter stage"):
            assert default_filter.filter_list[0].stage == 1

    def test_add_filter_from_parameters(self, default_filter, subtests):
        """Test adding a filter by parameters to the Filter."""
        # Clear any previously added filters
        default_filter.filter_list = []

        default_filter.add_filter(name="high pass", applied=False, stage=2)

        with subtests.test(msg="filter_list length after add"):
            assert len(default_filter.filter_list) == 1

        with subtests.test(msg="added filter name"):
            assert default_filter.filter_list[0].name == "high pass"

        with subtests.test(msg="added filter applied"):
            assert default_filter.filter_list[0].applied is False

        with subtests.test(msg="added filter stage"):
            assert default_filter.filter_list[0].stage == 2

    def test_remove_filter_with_reset(self, subtests):
        """Test removing a filter with stage reset."""
        applied_filters = [
            AppliedFilter(name="low pass", applied=True, stage=1),
            AppliedFilter(name="high pass", applied=False, stage=2),
        ]
        filtered = Filter(filter_list=applied_filters)

        filtered.remove_filter("low pass")

        with subtests.test(msg="filter_list length after remove"):
            assert len(filtered.filter_list) == 1

        with subtests.test(msg="remaining filter name"):
            assert filtered.filter_list[0].name == "high pass"

        with subtests.test(msg="remaining filter stage reset"):
            assert filtered.filter_list[0].stage == 1

    def test_remove_filter_without_reset(self, subtests):
        """Test removing a filter without stage reset."""
        applied_filters = [
            AppliedFilter(name="low pass", applied=True, stage=1),
            AppliedFilter(name="high pass", applied=False, stage=2),
        ]
        filtered = Filter(filter_list=applied_filters)

        filtered.remove_filter("low pass", reset_stages=False)

        with subtests.test(msg="filter_list length after remove"):
            assert len(filtered.filter_list) == 1

        with subtests.test(msg="remaining filter name"):
            assert filtered.filter_list[0].name == "high pass"

        with subtests.test(msg="remaining filter stage unchanged"):
            assert filtered.filter_list[0].stage == 2

    def test_remove_nonexistent_filter(self, filter_with_applied_filters, subtests):
        """Test removing a filter that doesn't exist."""
        original_length = len(filter_with_applied_filters.filter_list)

        filter_with_applied_filters.remove_filter("bandpass")

        with subtests.test(msg="filter_list unchanged"):
            assert len(filter_with_applied_filters.filter_list) == original_length
