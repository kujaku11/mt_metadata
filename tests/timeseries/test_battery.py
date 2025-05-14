# -*- coding: utf-8 -*-
"""
Tests for the Battery class.

This module tests the Battery class functionality including default values,
custom values, validation, and partial initialization.
"""

import pytest
from pydantic import ValidationError

from mt_metadata.common import StartEndRange
from mt_metadata.timeseries import Battery


@pytest.fixture(scope="module")
def default_battery():
    """Return a Battery instance with default values."""
    return Battery()


@pytest.fixture(scope="module")
def custom_battery():
    """Return a Battery instance with custom values."""
    return Battery(
        type="pb-acid gel cell",
        id="battery01",
        voltage=StartEndRange(minimum=11.5, maximum=12.6),
        comments="Battery discharged too quickly.",
    )


@pytest.fixture(scope="module")
def partial_battery():
    """Return a Battery instance with partial values."""
    return Battery(type="lithium-ion", comments="Backup battery.")


@pytest.fixture(
    params=[
        {"voltage": "not a StartEndRange"},
    ]
)
def invalid_battery_params(request):
    """Return invalid battery parameters that should trigger validation errors."""
    return request.param


def test_battery_default_values(default_battery, subtests):
    """Test the default values of the Battery model."""
    test_cases = [
        ("type", None),
        ("id", None),
        ("voltage.__class__", StartEndRange),
        ("comments", None),
    ]

    for attr, expected in test_cases:
        with subtests.test(msg=f"default {attr}"):
            if attr == "voltage.__class__":
                assert isinstance(default_battery.voltage, expected)
            else:
                assert getattr(default_battery, attr) == expected


def test_battery_custom_values(custom_battery, subtests):
    """Test the Battery model with custom values."""
    test_cases = [
        ("type", "pb-acid gel cell"),
        ("id", "battery01"),
        ("voltage.minimum", 11.5),
        ("voltage.maximum", 12.6),
        ("comments", "Battery discharged too quickly."),
    ]

    for attr, expected in test_cases:
        with subtests.test(msg=f"custom {attr}"):
            if "." in attr:
                obj_attr, sub_attr = attr.split(".")
                obj = getattr(custom_battery, obj_attr)
                assert getattr(obj, sub_attr) == expected
            else:
                assert getattr(custom_battery, attr) == expected


def test_battery_invalid_voltage(invalid_battery_params):
    """Test the Battery model with invalid voltage values."""
    with pytest.raises(ValidationError):
        Battery(**invalid_battery_params)


def test_battery_partial_values(partial_battery, subtests):
    """Test the Battery model with partial values."""
    test_cases = [
        ("type", "lithium-ion"),
        ("id", None),
        ("voltage.__class__", StartEndRange),
        ("comments", "Backup battery."),
    ]

    for attr, expected in test_cases:
        with subtests.test(msg=f"partial {attr}"):
            if attr == "voltage.__class__":
                assert isinstance(partial_battery.voltage, expected)
            else:
                assert getattr(partial_battery, attr) == expected


def test_battery_voltage_update(default_battery, subtests):
    """Test updating battery voltage values."""
    # Update the voltage
    default_battery.voltage.minimum = 10.5
    default_battery.voltage.maximum = 13.2

    with subtests.test(msg="updated minimum"):
        assert default_battery.voltage.minimum == 10.5

    with subtests.test(msg="updated maximum"):
        assert default_battery.voltage.maximum == 13.2


def test_battery_attributes_update(default_battery, subtests):
    """Test updating battery attributes."""
    updates = {
        "type": "nickel-metal hydride",
        "id": "battery02",
        "comments": "Updated battery info",
    }

    # Apply updates
    for attr, value in updates.items():
        setattr(default_battery, attr, value)

    # Verify updates
    for attr, expected in updates.items():
        with subtests.test(msg=f"updated {attr}"):
            assert getattr(default_battery, attr) == expected
