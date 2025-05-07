import pytest
from pydantic import ValidationError
from mt_metadata.timeseries import Electric, Electrode, ChannelBase
from mt_metadata.common import StartEndRange
from collections import OrderedDict
import pandas as pd
import json


def test_electric_inherits_channel():
    """
    Test that Electric inherits from Channel and has all its attributes.
    """
    electric = Electric()

    assert isinstance(electric, ChannelBase)
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


@pytest.fixture
def empty_electric():
    """Create an empty Electric object."""
    return Electric()


@pytest.fixture
def sample_electrodes():
    """Create sample positive and negative electrodes."""
    positive_electrode = Electrode(
        name="Positive Electrode", latitude=45.0, longitude=-120.0
    )
    negative_electrode = Electrode(
        name="Negative Electrode", latitude=45.1, longitude=-120.1
    )
    return {"positive": positive_electrode, "negative": negative_electrode}


@pytest.fixture
def sample_ranges():
    """Create sample range objects for Electric."""
    return {
        "contact_resistance": StartEndRange(start=10.0, end=20.0),
        "ac": StartEndRange(start=0.1, end=0.5),
        "dc": StartEndRange(start=0.01, end=0.02),
    }


@pytest.fixture
def populated_electric(sample_electrodes, sample_ranges):
    """Create a fully populated Electric object."""
    return Electric(
        component="ex",
        dipole_length=55.25,
        positive=sample_electrodes["positive"],
        negative=sample_electrodes["negative"],
        contact_resistance=sample_ranges["contact_resistance"],
        ac=sample_ranges["ac"],
        dc=sample_ranges["dc"],
        sample_rate=256.0,
        units="mV",
        channel_number=1,
        time_period={"start": "2020-01-01T00:00:00", "end": "2020-01-02T00:00:00"},
    )


@pytest.fixture
def electric_dict():
    """Create a dictionary with Electric metadata."""
    return {
        "electric": {
            "component": "ex",
            "dipole_length": 100.0,
            "positive.name": "A",
            "positive.id": "EL001",
            "positive.latitude": 45.0,
            "positive.longitude": -120.0,
            "negative.name": "B",
            "negative.id": "EL002",
            "negative.latitude": 45.1,
            "negative.longitude": -120.1,
            "contact_resistance.start": 5.0,
            "contact_resistance.end": 8.0,
            "ac.start": 0.2,
            "ac.end": 0.3,
            "dc.start": 1.5,
            "dc.end": 2.0,
            "filter.filter_list": [
                {
                    "applied_filter": OrderedDict(
                        [
                            ("applied", False),
                            ("name", "low_pass"),
                            ("stage", 1),
                        ]
                    )
                },
            ],
            "sample_rate": 128.0,
            "units": "millivolt",
            "type": "electric",
        }
    }


def test_electric_inherits_channel(empty_electric, subtests):
    """
    Test that Electric inherits from Channel and has all its attributes.
    """
    electric = empty_electric

    with subtests.test("inherits from ChannelBase"):
        assert isinstance(electric, ChannelBase)

    with subtests.test("default component is empty string"):
        assert electric.component == ""

    with subtests.test("default dipole_length is 0.0"):
        assert electric.dipole_length == 0.0

    with subtests.test("positive is Electrode instance"):
        assert isinstance(electric.positive, Electrode)

    with subtests.test("negative is Electrode instance"):
        assert isinstance(electric.negative, Electrode)

    with subtests.test("contact_resistance is StartEndRange instance"):
        assert isinstance(electric.contact_resistance, StartEndRange)

    with subtests.test("ac is StartEndRange instance"):
        assert isinstance(electric.ac, StartEndRange)

    with subtests.test("dc is StartEndRange instance"):
        assert isinstance(electric.dc, StartEndRange)


def test_electric_custom_values(
    populated_electric, sample_electrodes, sample_ranges, subtests
):
    """
    Test the Electric model with custom values.
    """
    electric = populated_electric

    with subtests.test("component is set correctly"):
        assert electric.component == "ex"

    with subtests.test("dipole_length is set correctly"):
        assert electric.dipole_length == 55.25

    with subtests.test("positive electrode is set correctly"):
        assert electric.positive == sample_electrodes["positive"]

    with subtests.test("negative electrode is set correctly"):
        assert electric.negative == sample_electrodes["negative"]

    with subtests.test("contact_resistance is set correctly"):
        assert electric.contact_resistance == sample_ranges["contact_resistance"]

    with subtests.test("ac range is set correctly"):
        assert electric.ac == sample_ranges["ac"]

    with subtests.test("dc range is set correctly"):
        assert electric.dc == sample_ranges["dc"]


def test_electric_partial_values(subtests):
    """
    Test the Electric model with partial values.
    """
    electric = Electric(
        component="ey",
        dipole_length=100.0,
    )

    with subtests.test("component is set correctly"):
        assert electric.component == "ey"

    with subtests.test("dipole_length is set correctly"):
        assert electric.dipole_length == 100.0

    with subtests.test("positive is default Electrode instance"):
        assert isinstance(electric.positive, Electrode)
        assert electric.positive.name == None

    with subtests.test("negative is default Electrode instance"):
        assert isinstance(electric.negative, Electrode)
        assert electric.negative.name == None

    with subtests.test("contact_resistance is default StartEndRange instance"):
        assert isinstance(electric.contact_resistance, StartEndRange)
        assert electric.contact_resistance.start == 0.0

    with subtests.test("ac is default StartEndRange instance"):
        assert isinstance(electric.ac, StartEndRange)
        assert electric.ac.start == 0.0

    with subtests.test("dc is default StartEndRange instance"):
        assert isinstance(electric.dc, StartEndRange)
        assert electric.dc.start == 0.0


def test_electric_invalid_component(subtests):
    """
    Test the Electric model with an invalid component value.
    """
    with subtests.test("invalid component raises ValidationError"):
        with pytest.raises(ValidationError):
            Electric(component="invalid_component")  # Must match the pattern r"e\w+"


def test_electric_invalid_values(subtests):
    """
    Test the Electric model with various invalid values.
    """
    with subtests.test("invalid dipole_length raises ValueError"):
        with pytest.raises(ValueError):
            Electric(dipole_length="invalid")  # Must be a float

    with subtests.test("invalid positive electrode raises ValueError"):
        with pytest.raises(ValueError):
            Electric(positive="invalid")  # Must be an Electrode object

    with subtests.test("invalid negative electrode raises ValueError"):
        with pytest.raises(ValueError):
            Electric(negative="invalid")  # Must be an Electrode object

    with subtests.test("invalid contact_resistance raises ValueError"):
        with pytest.raises(ValueError):
            Electric(contact_resistance="invalid")  # Must be a StartEndRange object

    with subtests.test("invalid ac range raises ValueError"):
        with pytest.raises(ValueError):
            Electric(ac="invalid")  # Must be a StartEndRange object

    with subtests.test("invalid dc range raises ValueError"):
        with pytest.raises(ValueError):
            Electric(dc="invalid")  # Must be a StartEndRange object


def test_electric_from_dict(electric_dict, subtests):
    """
    Test creating an Electric object from a dictionary.
    """
    electric = Electric()
    electric.from_dict(electric_dict)

    with subtests.test("component is set correctly"):
        assert electric.component == "ex"

    with subtests.test("dipole_length is set correctly"):
        assert electric.dipole_length == 100.0

    with subtests.test("sample_rate is set correctly"):
        assert electric.sample_rate == 128.0

    with subtests.test("positive electrode name is set correctly"):
        assert electric.positive.name == "A"

    with subtests.test("positive electrode id is set correctly"):
        assert electric.positive.id == "EL001"

    with subtests.test("positive electrode latitude is set correctly"):
        assert electric.positive.latitude == 45.0

    with subtests.test("negative electrode name is set correctly"):
        assert electric.negative.name == "B"

    with subtests.test("contact_resistance start is set correctly"):
        assert electric.contact_resistance.start == 5.0

    with subtests.test("contact_resistance end is set correctly"):
        assert electric.contact_resistance.end == 8.0

    with subtests.test("ac start is set correctly"):
        assert electric.ac.start == 0.2

    with subtests.test("dc range is set correctly"):
        assert electric.dc.start == 1.5
        assert electric.dc.end == 2.0


def test_electric_to_dict(populated_electric, subtests):
    """
    Test converting an Electric object to a dictionary.
    """
    electric_dict = populated_electric.to_dict()

    with subtests.test("dictionary has electric key"):
        assert "electric" in electric_dict

    with subtests.test("component is preserved"):
        assert electric_dict["electric"]["component"] == "ex"

    with subtests.test("dipole_length is preserved"):
        assert electric_dict["electric"]["dipole_length"] == 55.25

    with subtests.test("positive electrode data is preserved"):
        assert electric_dict["electric"]["positive.name"] == "Positive Electrode"
        assert electric_dict["electric"]["positive.latitude"] == 45.0

    with subtests.test("negative electrode data is preserved"):
        assert electric_dict["electric"]["negative.name"] == "Negative Electrode"
        assert electric_dict["electric"]["negative.longitude"] == -120.1

    with subtests.test("contact_resistance data is preserved"):
        assert electric_dict["electric"]["contact_resistance.start"] == 10.0
        assert electric_dict["electric"]["contact_resistance.end"] == 20.0


def test_electric_to_from_json(populated_electric, subtests):
    """
    Test converting an Electric object to and from JSON.
    """
    # Convert to JSON
    json_str = populated_electric.to_json(nested=True)

    with subtests.test("to_json produces valid string"):
        assert isinstance(json_str, str)
        # Check if it's valid JSON by parsing it
        json_data = json.loads(json_str)
        assert "electric" in json_data

    # Create new object from JSON
    new_electric = Electric()
    new_electric.from_json(json_str)

    with subtests.test("from_json preserves component"):
        assert new_electric.component == populated_electric.component

    with subtests.test("from_json preserves dipole_length"):
        assert new_electric.dipole_length == populated_electric.dipole_length

    with subtests.test("from_json preserves electrode data"):
        assert new_electric.positive.name == populated_electric.positive.name
        assert new_electric.negative.latitude == populated_electric.negative.latitude


def test_electric_to_from_series(populated_electric, subtests):
    """
    Test converting an Electric object to and from pandas Series.
    """
    # Convert to Series
    series = populated_electric.to_series()

    with subtests.test("to_series produces pandas Series"):
        assert isinstance(series, pd.Series)

    # Create new object from Series
    new_electric = Electric()
    new_electric.from_series(series)

    with subtests.test("from_series preserves component"):
        assert new_electric.component == populated_electric.component

    with subtests.test("from_series preserves dipole_length"):
        assert new_electric.dipole_length == populated_electric.dipole_length

    with subtests.test("from_series preserves electrode data"):
        assert new_electric.positive.name == populated_electric.positive.name
        assert new_electric.negative.latitude == populated_electric.negative.latitude


def test_electric_with_kwargs(subtests):
    """
    Test initializing Electric with kwargs including nested objects.
    """
    kwargs = {
        "component": "ex",
        "dipole_length": 75.5,
        "sample_rate": 1024.0,
        "positive.name": "Electrode A",
        "positive.latitude": 40.0,
        "positive.longitude": -110.0,
        "negative.name": "Electrode B",
        "negative.latitude": 40.01,
        "negative.longitude": -110.01,
        "contact_resistance.start": 3.5,
        "ac.end": 0.8,
    }

    electric = Electric(**kwargs)

    with subtests.test("top-level kwargs are set correctly"):
        assert electric.component == "ex"
        assert electric.dipole_length == 75.5
        assert electric.sample_rate == 1024.0

    with subtests.test("nested positive electrode kwargs are set correctly"):
        assert electric.positive.name == "Electrode A"
        assert electric.positive.latitude == 40.0
        assert electric.positive.longitude == -110.0

    with subtests.test("nested negative electrode kwargs are set correctly"):
        assert electric.negative.name == "Electrode B"
        assert electric.negative.latitude == 40.01
        assert electric.negative.longitude == -110.01

    with subtests.test("nested range kwargs are set correctly"):
        assert electric.contact_resistance.start == 3.5
        assert electric.ac.end == 0.8


# TODO: does dipole length need to be calculated from the electrodes?
# def test_electric_calculate_dipole_length(subtests):
#     """
#     Test calculating dipole length from electrode positions.
#     """
#     electric = Electric(
#         component="ex",
#         positive=Electrode(latitude=40.0, longitude=-110.0),
#         negative=Electrode(latitude=40.01, longitude=-110.01),
#     )

#     # Calculate dipole length
#     calculated_length = electric.calculate_dipole_length()

#     with subtests.test("calculation returns float value"):
#         assert isinstance(calculated_length, float)

#     with subtests.test("calculated value is reasonable"):
#         # Approximate distance in meters between these coordinates
#         # should be roughly 1.5-1.6 km
#         assert 1400 < calculated_length < 1700

#     with subtests.test("dipole_length property is updated"):
#         assert electric.dipole_length == calculated_length


# def test_electric_validation(subtests):
#     """
#     Test validation of Electric objects.
#     """
#     # Valid electric
#     valid_electric = Electric(component="ex", dipole_length=100.0)

#     with subtests.test("valid object passes validation"):
#         assert valid_electric.validate() is True

#     # Invalid electric (missing required component)
#     invalid_electric = Electric(dipole_length=100.0)
#     invalid_electric.component = None

#     with subtests.test("invalid object fails validation"):
#         try:
#             result = invalid_electric.validate()
#             assert result is False
#         except Exception as e:
#             # If it raises an exception instead of returning False
#             assert "component" in str(e).lower()
