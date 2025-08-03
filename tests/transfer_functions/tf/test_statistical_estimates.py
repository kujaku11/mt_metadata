# -*- coding: utf-8 -*-
"""
Tests for StatisticalEstimate BaseModel

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""
from typing import Any, Dict

import pytest

from mt_metadata.common import ArrayDTypeEnum
from mt_metadata.common.units import get_unit_object
from mt_metadata.transfer_functions.tf.statistical_estimate_basemodel import (
    StatisticalEstimate,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def valid_params() -> Dict[str, Any]:
    """Return valid parameters for creating a StatisticalEstimate"""
    return {
        "name": "transfer function",
        "data_type": "complex",
        "description": "test estimate",
        "input_channels": ["hx", "hy"],
        "output_channels": ["ex", "ey"],
        "units": "millivolts per kilometer per nanotesla",
    }


@pytest.fixture(scope="module")
def valid_instance(valid_params: Dict[str, Any]) -> StatisticalEstimate:
    """Return a valid StatisticalEstimate instance"""
    return StatisticalEstimate(**valid_params)


@pytest.fixture(
    params=[
        (
            "millivolts per kilometer per nanotesla",
            "millivolts per kilometer per nanotesla",
        ),
        ("mV/km/nT", "millivolts per kilometer per nanotesla"),
        ("ohm-m", "ohm meter"),
    ]
)
def unit_test_cases(request):
    """Parameterized fixture for testing various unit inputs"""
    return request.param


@pytest.fixture(
    params=[
        (["hx", "hy"], ["hx", "hy"]),
        ("hx, hy", ["hx", "hy"]),
        ("hx,hy", ["hx", "hy"]),
        (["hx", "hy", "hz"], ["hx", "hy", "hz"]),
    ]
)
def channel_test_cases(request):
    """Parameterized fixture for testing channel inputs"""
    return request.param


# =============================================================================
# Tests
# =============================================================================


class TestStatisticalEstimateCreation:
    """Tests for creating StatisticalEstimate instances"""

    def test_create_with_valid_params(self, valid_params, valid_instance, subtests):
        """Test creating a StatisticalEstimate with valid parameters"""
        with subtests.test("instance creation"):
            assert isinstance(valid_instance, StatisticalEstimate)

        with subtests.test("name"):
            assert valid_instance.name == valid_params["name"]

        with subtests.test("data_type"):
            assert valid_instance.data_type == valid_params["data_type"]

        with subtests.test("description"):
            assert valid_instance.description == valid_params["description"]

        with subtests.test("input_channels"):
            assert valid_instance.input_channels == valid_params["input_channels"]

        with subtests.test("output_channels"):
            assert valid_instance.output_channels == valid_params["output_channels"]

        with subtests.test("units"):
            # Units are normalized to full name
            unit_obj = get_unit_object(valid_params["units"])
            assert valid_instance.units == unit_obj.name

    def test_create_empty(self):
        """Test creating a StatisticalEstimate with no parameters"""
        instance = StatisticalEstimate()
        assert instance.name == ""
        assert instance.data_type == ArrayDTypeEnum.COMPLEX
        assert instance.description == ""
        assert instance.input_channels == []
        assert isinstance(
            instance.output_channels, list
        )  # Empty string becomes empty list
        assert instance.units == ""

    def test_create_with_invalid_data_type(self):
        """Test creating a StatisticalEstimate with an invalid data type"""
        with pytest.raises(ValueError):
            StatisticalEstimate(data_type="invalid_type")


class TestStatisticalEstimateValidation:
    """Tests for validating StatisticalEstimate inputs"""

    def test_units_validation(self, unit_test_cases, valid_params, subtests):
        """Test validation of units"""
        input_unit, expected_name = unit_test_cases

        # Create with this unit
        params = valid_params.copy()
        params["units"] = input_unit
        instance = StatisticalEstimate(**params)

        with subtests.test(f"unit_validation: {input_unit}"):
            assert instance.units == expected_name

    def test_invalid_units(self):
        """Test invalid units raise an error"""
        with pytest.raises(KeyError):
            StatisticalEstimate(units="invalid!units!here")

    def test_empty_units(self, valid_params):
        """Test empty units are allowed"""
        params = valid_params.copy()
        params["units"] = ""
        instance = StatisticalEstimate(**params)
        assert instance.units == ""

        params["units"] = None
        instance = StatisticalEstimate(**params)
        assert instance.units == ""

    def test_channel_validation(self, channel_test_cases, valid_params, subtests):
        """Test validation of channels"""
        input_channels, expected_channels = channel_test_cases

        # Test input_channels
        params = valid_params.copy()
        params["input_channels"] = input_channels
        instance = StatisticalEstimate(**params)

        with subtests.test(f"input channel validation: {input_channels}"):
            assert instance.input_channels == expected_channels

        # Test output_channels
        params = valid_params.copy()
        params["output_channels"] = input_channels
        instance = StatisticalEstimate(**params)

        with subtests.test(f"output channel validation: {input_channels}"):
            assert instance.output_channels == expected_channels

    def test_invalid_channel_type(self):
        """Test invalid channel types raise an error"""
        with pytest.raises(TypeError):
            StatisticalEstimate(input_channels=123)

        with pytest.raises(TypeError):
            StatisticalEstimate(output_channels=True)


class TestStatisticalEstimateMethods:
    """Tests for StatisticalEstimate methods"""

    def test_model_dump(self, valid_instance):
        """Test the model_dump method"""
        data = valid_instance.model_dump()
        assert isinstance(data, dict)
        assert set(data.keys()) >= {
            "name",
            "data_type",
            "description",
            "input_channels",
            "output_channels",
            "units",
        }
        assert data["name"] == valid_instance.name
        assert data["data_type"] == valid_instance.data_type
        assert isinstance(data["input_channels"], list)
        assert isinstance(data["output_channels"], list)

    def test_model_dump_json(self, valid_instance):
        """Test serialization to JSON"""
        json_str = valid_instance.model_dump_json()
        assert isinstance(json_str, str)
        assert '"name":"transfer function"' in json_str.replace(" ", "")
        assert '"data_type":"complex"' in json_str.replace(" ", "")

    def test_from_dict(self):
        """Test creating from dictionary"""
        data = {
            "name": "impedance",
            "data_type": "complex",
            "description": "Z estimate",
            "input_channels": "hx,hy",
            "output_channels": ["ex", "ey"],
            "units": "mV/km/nT",
        }
        instance = StatisticalEstimate.model_validate(data)
        assert instance.name == "impedance"
        assert instance.input_channels == ["hx", "hy"]  # String converted to list
        assert (
            instance.units == "millivolts per kilometer per nanotesla"
        )  # Normalized unit


class TestStatisticalEstimateEnums:
    """Tests specifically for enum handling"""

    @pytest.mark.parametrize(
        "dtype",
        [
            "complex",
            "real",
            "integer",
            "float",
            ArrayDTypeEnum.COMPLEX,
            ArrayDTypeEnum.REAL,
        ],
    )
    def test_valid_data_types(self, dtype):
        """Test valid data types are accepted"""
        instance = StatisticalEstimate(data_type=dtype)
        # Ensure it's converted to enum
        assert instance.data_type in list(ArrayDTypeEnum)


if __name__ == "__main__":
    pytest.main([__file__])
