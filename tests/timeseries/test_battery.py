import pytest
from mt_metadata.timeseries import Battery
from mt_metadata.common import StartEndRange
from pydantic import ValidationError


def test_battery_default_values():
    """
    Test the default values of the Battery model.
    """
    battery = Battery()

    assert battery.type is None
    assert battery.id is None
    assert battery.voltage == StartEndRange()
    assert battery.comments is None


def test_battery_custom_values():
    """
    Test the Battery model with custom values.
    """
    battery = Battery(
        type="pb-acid gel cell",
        id="battery01",
        voltage=StartEndRange(minimum=11.5, maximum=12.6),
        comments="Battery discharged too quickly.",
    )

    assert battery.type == "pb-acid gel cell"
    assert battery.id == "battery01"
    assert battery.voltage.minimum == 11.5
    assert battery.voltage.maximum == 12.6
    assert battery.comments == "Battery discharged too quickly."


def test_battery_invalid_voltage():
    """
    Test the Battery model with invalid voltage values.
    """
    with pytest.raises(ValidationError):
        Battery(voltage=StartEndRange(start="invalid"))

    with pytest.raises(ValidationError):
        Battery(voltage=StartEndRange(end="invalid"))


def test_battery_partial_values():
    """
    Test the Battery model with partial values.
    """
    battery = Battery(type="lithium-ion", comments="Backup battery.")

    assert battery.type == "lithium-ion"
    assert battery.id is None
    assert battery.voltage == StartEndRange()
    assert battery.comments == "Backup battery."
