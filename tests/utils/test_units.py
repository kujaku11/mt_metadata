import pytest

from mt_metadata.common.units import (
    find_separator,
    get_unit_from_df,
    get_unit_object,
    parse_unit_string,
    Unit,
    UNITS_DF,
)


def test_unit_initialization():
    """
    Test the initialization of the Unit class.
    """
    unit = Unit(
        name="millivolt",
        description="Unit of electric potential",
        symbol="mV",
        plot_label="mV",
    )
    assert unit.name == "millivolt"
    assert unit.description == "Unit of electric potential"
    assert unit.symbol == "mV"
    assert unit.plot_label == "mV"


def test_unit_to_dict():
    """
    Test the to_dict method of the Unit class.
    """
    unit = Unit(
        name="millivolt",
        description="Unit of electric potential",
        symbol="mV",
        plot_label="mV",
    )
    unit_dict = unit.to_dict()
    expected = {
        "name": "millivolt",
        "description": "Unit of electric potential",
        "symbol": "mV",
        "plot_label": "mV",
    }
    assert unit_dict == expected


def test_unit_from_dict():
    """
    Test the from_dict method of the Unit class.
    """
    unit = Unit()
    unit.from_dict(
        {
            "name": "millivolt",
            "description": "Unit of electric potential",
            "symbol": "mV",
            "plot_label": "mV",
        }
    )
    assert unit.name == "millivolt"
    assert unit.description == "Unit of electric potential"
    assert unit.symbol == "mV"
    assert unit.plot_label == "mV"


def test_unit_combine():
    """
    Test the combine method of the Unit class.
    """
    unit1 = Unit(
        name="millivolt", symbol="mV", description="Millivolt", plot_label="mV"
    )
    unit2 = Unit(
        name="nanotesla", symbol="nT", description="Nanotesla", plot_label="nT"
    )

    combined_unit = unit1.combine(unit2, separator="/")
    assert combined_unit.name == "millivolt per nanotesla"
    assert combined_unit.symbol == "mV/nT"
    assert combined_unit.description == "Millivolt per Nanotesla"
    assert combined_unit.plot_label == "mV/nT"

    combined_unit = unit1.combine(unit2, separator=" ")
    assert combined_unit.name == "millivolt nanotesla"
    assert combined_unit.symbol == "mV nT"
    assert combined_unit.description == "Millivolt Nanotesla"
    assert combined_unit.plot_label == "mV nT"


def test_find_separator():
    """
    Test the find_separator function.
    """
    assert find_separator("mV nT/[km ohm]") == " "
    assert find_separator("mV/nT") == "/"
    assert find_separator("mV per nT") == " per "
    assert find_separator("mVnT") is None


def test_parse_unit_string():
    """
    Test the parse_unit_string function.
    """
    unit_string = "mV nT/[km ohm]"
    expected = [
        {"name": "mV", "sep": ""},
        {"name": "nT", "sep": " "},
        {"name": "km", "sep": "/"},
        {"name": "ohm", "sep": " "},
    ]
    assert parse_unit_string(unit_string) == expected

    unit_string = "mV/nT"
    expected = [
        {"name": "mV", "sep": ""},
        {"name": "nT", "sep": "/"},
    ]
    assert parse_unit_string(unit_string) == expected

    unit_string = "mV per nT"
    expected = [
        {"name": "mV", "sep": ""},
        {"name": "nT", "sep": " per "},
    ]
    assert parse_unit_string(unit_string) == expected

    with pytest.raises(ValueError):
        parse_unit_string("")


def test_get_unit_from_df():
    """
    Test the get_unit_from_df function.
    """
    unit = get_unit_from_df("mV")
    assert isinstance(unit, Unit)
    assert unit.name == "millivolt"
    assert unit.symbol == "mV"

    unit = get_unit_from_df("Hz")
    assert isinstance(unit, Unit)
    assert unit.name == "hertz"
    assert unit.symbol == "Hz"

    with pytest.raises(KeyError):
        get_unit_from_df("nonexistent_unit", allow_none=False)

    unit = get_unit_from_df("nonexistent_unit", allow_none=True)
    assert unit.name == "unknown"
    assert unit.symbol == "unknown"


def test_get_unit_object():
    """
    Test the get_unit_object function.
    """
    unit = get_unit_object("mV")
    assert isinstance(unit, Unit)
    assert unit.name == "millivolt"
    assert unit.symbol == "mV"

    unit = get_unit_object("mV/nT")
    assert isinstance(unit, Unit)
    assert unit.name == "millivolt per nanotesla"
    assert unit.symbol == "mV/nT"

    unit = get_unit_object("mV nT/[km ohm]")
    assert isinstance(unit, Unit)
    assert unit.name == "millivolt nanotesla per kilometer ohm"
    assert unit.symbol == "mV nT/km \u03a9"

    with pytest.raises(ValueError):
        get_unit_object("")


def test_units_df():
    """
    Test the UNITS_DF DataFrame.
    """
    assert not UNITS_DF.empty
    assert "name" in UNITS_DF.columns
    assert "symbol" in UNITS_DF.columns
    assert "description" in UNITS_DF.columns
    assert "plot_label" in UNITS_DF.columns

    # Check for a known unit
    row = UNITS_DF[UNITS_DF["symbol"] == "mV"]
    assert not row.empty
    assert row.iloc[0]["name"] == "millivolt"
    assert row.iloc[0]["description"] == "Milli Unit of electric potential"
