# -*- coding: utf-8 -*-
"""
Tests for the TransferFunction base model.

This module tests the TransferFunction base class functionality including validation,
default values, custom values, and serialization.
"""

import json
from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.tf.transfer_function_basemodel import (
    TransferFunction,
)
from mt_metadata.utils.mttime import MTime


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_tf():
    """Return a TransferFunction instance with default values."""
    return TransferFunction()


@pytest.fixture(scope="module")
def custom_tf():
    """Return a TransferFunction instance with custom values."""
    return TransferFunction(
        id="mt01_256",
        sign_convention="-",
        units="volts_per_meter_per_tesla",
        runs_processed="[MT001a MT001b]",
        remote_references="[MT002a]",
        processed_date="2023-05-01T12:00:00",
        processing_parameters=["nfft=4096", "n_windows=16"],
        processing_type="robust remote reference",
        coordinate_system="geographic",
        processing_config="aurora.config",
    )


@pytest.fixture(scope="module")
def tf_dict():
    """Return a dictionary for TransferFunction testing."""
    return {
        "transfer_function": {
            "id": "mt01_256",
            "sign_convention": "-",
            "units": "volts_per_meter_per_tesla",
            "runs_processed": "[MT001a MT001b]",
            "remote_references": "[MT002a]",
            "processed_date": "2023-05-01T12:00:00+00:00",
            "processing_parameters": ["nfft=4096", "n_windows=16"],
            "processing_type": "robust remote reference",
            "coordinate_system": "geographic",
            "processing_config": "aurora.config",
        }
    }


@pytest.fixture(
    scope="module",
    params=[
        1682942400.0,  # Epoch time
        np.datetime64("2023-05-01T12:00:00"),  # numpy datetime64
        pd.Timestamp("2023-05-01T12:00:00"),  # pandas Timestamp
        "2023-05-01T12:00:00",  # ISO format string
        datetime(2023, 5, 1, 12, 0, 0),  # Python datetime
    ],
)
def time_formats(request):
    """Return different valid time format values for testing."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        "millivolts_per_kilometer_per_nanotesla",
        "volts_per_meter_per_tesla",
        "[mV/km]/[nT]",
        "V/m/T",
    ],
)
def valid_units(request):
    """Return different valid unit formats for testing."""
    return request.param


@pytest.fixture(
    params=[
        {"field": "units", "value": "invalid_units", "error": KeyError},
        {"field": "sign_convention", "value": "invalid_sign", "error": ValidationError},
        {
            "field": "coordinate_system",
            "value": "invalid_coords",
            "error": ValidationError,
        },
    ]
)
def invalid_values(request):
    """Return invalid values for different fields with expected errors."""
    return request.param


# =============================================================================
# Tests
# =============================================================================


class TestDefaultValues:
    """Test default values of the TransferFunction class."""

    def test_default_values(self, default_tf, subtests):
        """Test the default values of TransferFunction attributes."""
        scalar_attrs = {
            "id": "",
            "sign_convention": "+",
            "units": "millivolts_per_kilometer_per_nanotesla",
            "runs_processed": "[]",
            "remote_references": "[]",
            "processing_type": "",
            "coordinate_system": "geopgraphic",
            "processing_config": None,
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"default {attr}"):
                assert getattr(default_tf, attr) == expected

        with subtests.test(msg="default processed_date"):
            assert isinstance(default_tf.processed_date, MTime)
            # The default date will be None internally
            assert default_tf.processed_date.isutc

        with subtests.test(msg="default processing_parameters"):
            assert default_tf.processing_parameters == []


class TestCustomValues:
    """Test custom values for the TransferFunction class."""

    def test_custom_values(self, custom_tf, subtests):
        """Test TransferFunction with custom attribute values."""
        scalar_attrs = {
            "id": "mt01_256",
            "sign_convention": "-",
            "units": "volts_per_meter_per_tesla",
            "runs_processed": "[MT001a MT001b]",
            "remote_references": "[MT002a]",
            "processing_type": "robust remote reference",
            "coordinate_system": "geographic",
            "processing_config": "aurora.config",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"custom {attr}"):
                assert getattr(custom_tf, attr) == expected

        with subtests.test(msg="custom processed_date"):
            assert isinstance(custom_tf.processed_date, MTime)
            assert custom_tf.processed_date.isoformat() == "2023-05-01T12:00:00+00:00"

        with subtests.test(msg="custom processing_parameters"):
            assert custom_tf.processing_parameters == ["nfft=4096", "n_windows=16"]


class TestValidation:
    """Test validation for the TransferFunction class."""

    def test_processed_date_formats(self, time_formats, subtests):
        """Test that processed_date accepts multiple formats."""
        tf = TransferFunction(processed_date=time_formats)

        with subtests.test(msg="processed_date type"):
            assert isinstance(tf.processed_date, MTime)

        with subtests.test(msg="processed_date value"):
            # All formats should convert to the same timestamp
            expected = "2023-05-01"
            assert expected in tf.processed_date.isoformat()

    def test_units_validation(self, valid_units, subtests):
        """Test that units are properly validated and normalized."""
        tf = TransferFunction(units=valid_units)

        with subtests.test(msg="units validation"):
            # Units should be normalized to a standard format
            assert tf.units in [
                "millivolts_per_kilometer_per_nanotesla",
                "volts_per_meter_per_tesla",
            ]

    def test_invalid_values(self, invalid_values):
        """Test that invalid values raise appropriate errors."""
        with pytest.raises(invalid_values["error"]):
            TransferFunction(**{invalid_values["field"]: invalid_values["value"]})


class TestSerialization:
    """Test serialization functionality for the TransferFunction class."""

    def test_to_dict(self, custom_tf, subtests):
        """Test converting TransferFunction to a dictionary."""
        tf_dict = custom_tf.to_dict()

        with subtests.test(msg="dict structure"):
            assert "transfer_function" in tf_dict

        dict_obj = tf_dict["transfer_function"]

        attrs_to_check = [
            "id",
            "sign_convention",
            "units",
            "runs_processed",
            "remote_references",
            "processing_type",
            "coordinate_system",
        ]

        for attr in attrs_to_check:
            with subtests.test(msg=f"to_dict {attr}"):
                assert dict_obj[attr] == getattr(custom_tf, attr)

        with subtests.test(msg="to_dict processed_date"):
            assert dict_obj["processed_date"] == custom_tf.processed_date.isoformat()

    def test_from_dict(self, tf_dict, subtests):
        """Test creating TransferFunction from a dictionary."""
        tf = TransferFunction()
        tf.from_dict(tf_dict)

        attrs_to_check = [
            "id",
            "sign_convention",
            "units",
            "runs_processed",
            "remote_references",
            "processing_type",
            "coordinate_system",
            "processing_config",
        ]

        for attr in attrs_to_check:
            with subtests.test(msg=f"from_dict {attr}"):
                assert getattr(tf, attr) == tf_dict["transfer_function"][attr]

        with subtests.test(msg="from_dict processed_date"):
            assert (
                tf.processed_date.isoformat()
                == tf_dict["transfer_function"]["processed_date"]
            )

    def test_to_json(self, custom_tf, subtests):
        """Test converting TransferFunction to JSON string."""
        json_str = custom_tf.to_json()

        with subtests.test(msg="to_json produces valid string"):
            assert isinstance(json_str, str)

        parsed_json = json.loads(json_str)

        with subtests.test(msg="to_json structure"):
            assert "transfer_function" in parsed_json

        # Test a sample of fields
        sample_fields = ["id", "units", "processing_type"]
        for field in sample_fields:
            with subtests.test(msg=f"to_json {field}"):
                assert parsed_json["transfer_function"][field] == getattr(
                    custom_tf, field
                )

    def test_from_json(self, custom_tf, subtests):
        """Test creating TransferFunction from JSON string."""
        json_str = custom_tf.to_json()

        # Create new TF from JSON
        new_tf = TransferFunction()
        new_tf.from_json(json_str)

        attrs_to_check = [
            "id",
            "sign_convention",
            "units",
            "runs_processed",
            "remote_references",
            "processing_type",
            "coordinate_system",
            "processing_config",
        ]

        for attr in attrs_to_check:
            with subtests.test(msg=f"from_json {attr}"):
                assert getattr(new_tf, attr) == getattr(custom_tf, attr)

        with subtests.test(msg="from_json processed_date"):
            assert (
                new_tf.processed_date.isoformat()
                == custom_tf.processed_date.isoformat()
            )


class TestModification:
    """Test modification functionality for the TransferFunction class."""

    def test_attribute_updates(self, default_tf, subtests):
        """Test updating attributes after initialization."""
        updates = {
            "id": "mt02_1024",
            "sign_convention": "-",
            "units": "volts_per_meter_per_tesla",
            "runs_processed": "[MT003a]",
            "remote_references": "[MT004a MT004b]",
            "processed_date": "2023-06-01T00:00:00",
            "processing_parameters": ["nfft=8192", "n_windows=32"],
            "processing_type": "single site",
            "coordinate_system": "geographic",
            "processing_config": "razorback.config",
        }

        # Apply updates
        for attr, value in updates.items():
            setattr(default_tf, attr, value)

        # Verify updates
        for attr, expected in updates.items():
            if attr == "processed_date":
                with subtests.test(msg=f"updated {attr}"):
                    assert (
                        default_tf.processed_date.isoformat()
                        == "2023-06-01T00:00:00+00:00"
                    )
            else:
                with subtests.test(msg=f"updated {attr}"):
                    assert getattr(default_tf, attr) == expected


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
