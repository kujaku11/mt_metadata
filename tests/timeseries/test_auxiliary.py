# -*- coding: utf-8 -*-
"""
Tests for the Auxiliary class.

This module tests the Auxiliary class functionality including inheritance,
initialization, and default field values.
"""

import pytest

from mt_metadata.timeseries import Auxiliary, Channel


@pytest.fixture(scope="module")
def auxiliary_instance():
    """
    Module-scoped fixture to create a single instance of Auxiliary for all tests.

    Returns:
        Auxiliary: An instance of the Auxiliary class
    """
    return Auxiliary()


def test_auxiliary_properties(auxiliary_instance, subtests):
    """Test various properties of the Auxiliary class using subtests."""

    with subtests.test(msg="initialization"):
        assert isinstance(auxiliary_instance, Auxiliary)

    with subtests.test(msg="inheritance"):
        assert isinstance(auxiliary_instance, Channel)

    # Test for expected attributes
    attributes = [
        "component",
        "measurement_azimuth",
        "measurement_tilt",
        "time_period",
        "sample_rate",
        "type",
    ]

    for attr in attributes:
        with subtests.test(msg=f"has attribute '{attr}'"):
            assert hasattr(auxiliary_instance, attr)


def test_auxiliary_default_values(auxiliary_instance, subtests):
    """Test that default values are correctly set."""
    default_values = {
        "type": "auxiliary",
        "component": "",
        "measurement_azimuth": 0.0,
        "measurement_tilt": 0.0,
    }

    for attr, expected in default_values.items():
        with subtests.test(msg=f"default '{attr}'"):
            assert getattr(auxiliary_instance, attr) == expected


def test_auxiliary_with_custom_values(subtests):
    """Test Auxiliary with custom attribute values."""
    custom_values = {
        "type": "auxiliary",
        "component": "voltage",
        "measurement_azimuth": 90.0,
        "measurement_tilt": 45.0,
        "sample_rate": 1.0,
    }

    aux = Auxiliary(**custom_values)

    for attr, expected in custom_values.items():
        with subtests.test(msg=f"custom '{attr}'"):
            assert getattr(aux, attr) == expected


def test_auxiliary_properties_update(auxiliary_instance, subtests):
    """Test that properties can be updated."""
    updates = {
        "type": "auxiliary",
        "component": "relative_humidity",
        "measurement_azimuth": 180.0,
        "measurement_tilt": 30.0,
    }

    # Update properties
    for attr, value in updates.items():
        setattr(auxiliary_instance, attr, value)

    # Verify updates
    for attr, expected in updates.items():
        with subtests.test(msg=f"updated '{attr}'"):
            assert getattr(auxiliary_instance, attr) == expected
