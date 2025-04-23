import pytest
from pydantic import ValidationError
from mt_metadata.timeseries.electric_basemodel import Electric
from mt_metadata.timeseries.electrode_basemodel import Electrode
from mt_metadata.common import StartEndRange
from mt_metadata.timeseries.channel_basemodel import Channel


def test_electric_inherits_channel():
    """
    Test that Electric inherits from Channel and has all its attributes.
    """
    electric = Electric()

    assert isinstance(electric, Channel)
    assert electric.component == ""
    assert electric.dipole_length == 0.0
    assert isinstance(electric.positive, Electrode)
    assert isinstance(electric.negative, Electrode)
    assert isinstance(electric.contact_resistance, StartEndRange)
    assert isinstance(electric.ac, StartEndRange)
    assert isinstance(electric.dc, StartEndRange)


def test_electric_custom_values():
    """
    Test the Electric model with custom values.
    """
    positive_electrode = Electrode(
        name="Positive Electrode", latitude=45.0, longitude=-120.0
    )
    negative_electrode = Electrode(
        name="Negative Electrode", latitude=45.1, longitude=-120.1
    )
    contact_resistance = StartEndRange(start=10.0, end=20.0)
    ac_range = StartEndRange(start=0.1, end=0.5)
    dc_range = StartEndRange(start=0.01, end=0.02)

    electric = Electric(
        component="ex",
        dipole_length=55.25,
        positive=positive_electrode,
        negative=negative_electrode,
        contact_resistance=contact_resistance,
        ac=ac_range,
        dc=dc_range,
    )

    assert electric.component == "ex"
    assert electric.dipole_length == 55.25
    assert electric.positive == positive_electrode
    assert electric.negative == negative_electrode
    assert electric.contact_resistance == contact_resistance
    assert electric.ac == ac_range
    assert electric.dc == dc_range


def test_electric_partial_values():
    """
    Test the Electric model with partial values.
    """
    electric = Electric(
        component="ey",
        dipole_length=100.0,
    )

    assert electric.component == "ey"
    assert electric.dipole_length == 100.0
    assert isinstance(electric.positive, Electrode)
    assert isinstance(electric.negative, Electrode)
    assert isinstance(electric.contact_resistance, StartEndRange)
    assert isinstance(electric.ac, StartEndRange)
    assert isinstance(electric.dc, StartEndRange)


def test_electric_invalid_component():
    """
    Test the Electric model with an invalid component value.
    """
    with pytest.raises(ValidationError):
        Electric(component="invalid_component")  # Must match the pattern r"e\w+"


def test_electric_invalid_dipole_length():
    """
    Test the Electric model with an invalid dipole_length value.
    """
    with pytest.raises(ValueError):
        Electric(dipole_length="invalid")  # Must be a float


def test_electric_invalid_positive_electrode():
    """
    Test the Electric model with an invalid positive electrode.
    """
    with pytest.raises(ValueError):
        Electric(positive="invalid")  # Must be an Electrode object


def test_electric_invalid_negative_electrode():
    """
    Test the Electric model with an invalid negative electrode.
    """
    with pytest.raises(ValueError):
        Electric(negative="invalid")  # Must be an Electrode object


def test_electric_invalid_contact_resistance():
    """
    Test the Electric model with an invalid contact_resistance.
    """
    with pytest.raises(ValueError):
        Electric(contact_resistance="invalid")  # Must be a StartEndRange object


def test_electric_invalid_ac_range():
    """
    Test the Electric model with an invalid AC range.
    """
    with pytest.raises(ValueError):
        Electric(ac="invalid")  # Must be a StartEndRange object


def test_electric_invalid_dc_range():
    """
    Test the Electric model with an invalid DC range.
    """
    with pytest.raises(ValueError):
        Electric(dc="invalid")  # Must be a StartEndRange object
