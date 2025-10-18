# -*- coding: utf-8 -*-
"""
Tests for the Electric class.

This module tests the Electric class functionality including inheritance,
custom values, validation, and serialization.
"""

import json
from collections import OrderedDict

import pandas as pd
import pytest
from pydantic import ValidationError

from mt_metadata.common import StartEndRange
from mt_metadata.timeseries import ChannelBase, Electric, Electrode


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def empty_electric():
    """Create an empty Electric object."""
    return Electric()


@pytest.fixture(scope="module")
def positive_electrode():
    """Create a sample positive electrode."""
    return Electrode(
        name="Positive Electrode", id="POS01", latitude=45.0, longitude=-120.0
    )


@pytest.fixture(scope="module")
def negative_electrode():
    """Create a sample negative electrode."""
    return Electrode(
        name="Negative Electrode", id="NEG01", latitude=45.1, longitude=-120.1
    )


@pytest.fixture(scope="module")
def sample_ranges():
    """Create sample range objects for Electric."""
    return {
        "contact_resistance": StartEndRange(start=10.0, end=20.0),
        "ac": StartEndRange(start=0.1, end=0.5),
        "dc": StartEndRange(start=0.01, end=0.02),
    }


@pytest.fixture(scope="module")
def populated_electric(positive_electrode, negative_electrode, sample_ranges):
    """Create a fully populated Electric object."""
    return Electric(
        component="ex",
        dipole_length=55.25,
        positive=positive_electrode,
        negative=negative_electrode,
        contact_resistance=sample_ranges["contact_resistance"],
        ac=sample_ranges["ac"],
        dc=sample_ranges["dc"],
        sample_rate=256.0,
        units="mV",
        channel_number=1,
        time_period={"start": "2020-01-01T00:00:00", "end": "2020-01-02T00:00:00"},
    )


@pytest.fixture(scope="module")
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
            "filters": [
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


@pytest.fixture
def invalid_value_tests():
    """
    Return a list of test cases for invalid values.
    Each test case has input parameter name, invalid value, and expected exception.
    """
    return [
        ("component", "invalid_component", ValidationError),
        ("dipole_length", "invalid", ValueError),
        ("positive", "invalid", ValueError),
        ("negative", "invalid", ValueError),
        ("contact_resistance", "invalid", ValueError),
        ("ac", "invalid", ValueError),
        ("dc", "invalid", ValueError),
    ]


# =============================================================================
# Tests
# =============================================================================


class TestElectricStructure:
    """Tests for the structure and inheritance of the Electric class."""

    def test_inheritance(self, empty_electric, subtests):
        """Test that Electric inherits correctly from ChannelBase."""
        with subtests.test("inherits from ChannelBase"):
            assert isinstance(empty_electric, ChannelBase)

    def test_default_attributes(self, empty_electric, subtests):
        """Test the default values of Electric attributes."""
        attribute_tests = [
            ("component", "e_default"),
            ("dipole_length", 0.0),
            ("positive", Electrode),
            ("negative", Electrode),
            ("contact_resistance", StartEndRange),
            ("ac", StartEndRange),
            ("dc", StartEndRange),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"default {attr}"):
                obj = empty_electric.get_attr_from_name(attr)
                if isinstance(obj, (Electrode, StartEndRange)):
                    assert isinstance(obj, expected)
                else:
                    assert obj == expected


class TestElectricValidation:
    """Tests for Electric validation and error handling."""

    @pytest.mark.parametrize(
        "param_name,invalid_value,expected_exception",
        [
            ("component", "invalid_component", ValidationError),
            ("dipole_length", "invalid", ValueError),
            ("positive", "invalid", ValueError),
            ("negative", "invalid", ValueError),
            ("contact_resistance", "invalid", ValueError),
            ("ac", "invalid", ValueError),
            ("dc", "invalid", ValueError),
        ],
    )
    def test_invalid_values(self, param_name, invalid_value, expected_exception):
        """Test Electric with invalid values."""
        with pytest.raises(expected_exception):
            kwargs = {param_name: invalid_value}
            Electric(**kwargs)


class TestElectricCustomValues:
    """Tests for Electric with custom values."""

    def test_custom_values(
        self,
        populated_electric,
        positive_electrode,
        negative_electrode,
        sample_ranges,
        subtests,
    ):
        """Test the Electric model with fully custom values."""
        attribute_tests = [
            ("component", "ex"),
            ("dipole_length", 55.25),
            ("sample_rate", 256.0),
            ("units", "milliVolt"),
            ("positive.name", positive_electrode.name),
            ("positive.id", positive_electrode.id),
            ("positive.latitude", positive_electrode.latitude),
            ("positive.longitude", positive_electrode.longitude),
            ("negative.name", negative_electrode.name),
            ("negative.id", negative_electrode.id),
            ("negative.latitude", negative_electrode.latitude),
            ("negative.longitude", negative_electrode.longitude),
            ("contact_resistance.start", sample_ranges["contact_resistance"].start),
            ("contact_resistance.end", sample_ranges["contact_resistance"].end),
            ("ac.start", sample_ranges["ac"].start),
            ("ac.end", sample_ranges["ac"].end),
            ("dc.start", sample_ranges["dc"].start),
            ("dc.end", sample_ranges["dc"].end),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"custom {attr}"):
                value = populated_electric.get_attr_from_name(attr)
                assert value == expected

    def test_partial_values(self, subtests):
        """Test the Electric model with partial values."""
        electric = Electric(
            component="ey",
            dipole_length=100.0,
        )

        attribute_tests = [
            ("component", "ey"),
            ("dipole_length", 100.0),
            ("positive", Electrode),
            ("positive.name", None),
            ("negative", Electrode),
            ("negative.name", None),
            ("contact_resistance", StartEndRange),
            ("contact_resistance.start", 0.0),
            ("ac", StartEndRange),
            ("ac.start", 0.0),
            ("dc", StartEndRange),
            ("dc.start", 0.0),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"partial {attr}"):
                obj = electric.get_attr_from_name(attr)
                if isinstance(obj, (StartEndRange, Electrode)):
                    assert isinstance(obj, expected)
                else:
                    assert obj == expected

    def test_kwargs_initialization(self, subtests):
        """Test initializing Electric with kwargs including nested objects."""
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

        attribute_tests = [
            ("component", "ex"),
            ("dipole_length", 75.5),
            ("sample_rate", 1024.0),
            ("positive.name", "Electrode A"),
            ("positive.latitude", 40.0),
            ("positive.longitude", -110.0),
            ("negative.name", "Electrode B"),
            ("negative.latitude", 40.01),
            ("negative.longitude", -110.01),
            ("contact_resistance.start", 3.5),
            ("ac.end", 0.8),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"kwargs {attr}"):
                value = electric.get_attr_from_name(attr)
                assert value == expected


class TestElectricSerialization:
    """Tests for Electric serialization and deserialization."""

    def test_from_dict(self, electric_dict, subtests):
        """Test creating an Electric object from a dictionary."""
        electric = Electric()
        electric.from_dict(electric_dict)

        attribute_tests = [
            ("component", "ex"),
            ("dipole_length", 100.0),
            ("sample_rate", 128.0),
            ("units", "milliVolt"),
            ("positive.name", "A"),
            ("positive.id", "EL001"),
            ("positive.latitude", 45.0),
            ("positive.longitude", -120.0),
            ("negative.name", "B"),
            ("negative.id", "EL002"),
            ("negative.latitude", 45.1),
            ("negative.longitude", -120.1),
            ("contact_resistance.start", 5.0),
            ("contact_resistance.end", 8.0),
            ("ac.start", 0.2),
            ("ac.end", 0.3),
            ("dc.start", 1.5),
            ("dc.end", 2.0),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"from_dict {attr}"):
                value = electric.get_attr_from_name(attr)
                assert value == expected

    def test_to_dict(self, populated_electric, subtests):
        """Test converting an Electric object to a dictionary."""
        electric_dict = populated_electric.to_dict(single=True, required=False)

        with subtests.test("dictionary has electric key"):
            assert "electric" in electric_dict["type"]

        dict_tests = [
            ("component", "ex"),
            ("dipole_length", 55.25),
            ("sample_rate", 256.0),
            ("units", "milliVolt"),
            ("positive.name", "Positive Electrode"),
            ("positive.id", "POS01"),
            ("positive.latitude", 45.0),
            ("positive.longitude", -120.0),
            ("negative.name", "Negative Electrode"),
            ("negative.id", "NEG01"),
            ("negative.latitude", 45.1),
            ("negative.longitude", -120.1),
            ("contact_resistance.start", 10.0),
            ("contact_resistance.end", 20.0),
            ("ac.start", 0.1),
            ("ac.end", 0.5),
            ("dc.start", 0.01),
            ("dc.end", 0.02),
        ]

        for attr, expected in dict_tests:
            with subtests.test(f"to_dict {attr}"):
                value = electric_dict[attr]
                assert value == expected

    def test_to_from_json(self, populated_electric, subtests):
        """Test converting an Electric object to and from JSON."""
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

        attribute_tests = [
            ("component", populated_electric.component),
            ("dipole_length", populated_electric.dipole_length),
            ("sample_rate", populated_electric.sample_rate),
            ("positive.name", populated_electric.positive.name),
            ("positive.latitude", populated_electric.positive.latitude),
            ("negative.name", populated_electric.negative.name),
            ("negative.latitude", populated_electric.negative.latitude),
            ("contact_resistance.start", populated_electric.contact_resistance.start),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"from_json {attr}"):
                value = new_electric.get_attr_from_name(attr)
                assert value == expected

    def test_to_from_series(self, populated_electric, subtests):
        """Test converting an Electric object to and from pandas Series."""
        # Convert to Series
        series = populated_electric.to_series()

        with subtests.test("to_series produces pandas Series"):
            assert isinstance(series, pd.Series)

        # Create new object from Series
        new_electric = Electric()
        new_electric.from_series(series)

        attribute_tests = [
            ("component", populated_electric.component),
            ("dipole_length", populated_electric.dipole_length),
            ("sample_rate", populated_electric.sample_rate),
            ("positive.name", populated_electric.positive.name),
            ("positive.latitude", populated_electric.positive.latitude),
            ("negative.name", populated_electric.negative.name),
            ("negative.latitude", populated_electric.negative.latitude),
        ]

        for attr, expected in attribute_tests:
            with subtests.test(f"from_series {attr}"):
                value = new_electric.get_attr_from_name(attr)
                assert value == expected
