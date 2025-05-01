import pytest
import numpy as np
import pandas as pd
from mt_metadata.timeseries.filters import FilterBase
from mt_metadata.common import Comment, FilterTypeEnum
from mt_metadata.utils.mttime import MTime
from pydantic import ValidationError


@pytest.fixture
def default_filter():
    """Fixture to create a default FilterBase object."""
    return FilterBase()


@pytest.fixture
def custom_filter():
    """Fixture to create a custom FilterBase object."""
    return FilterBase(
        name="lowpass_filter",
        comments="Test filter for lowpass data",
        type=FilterTypeEnum.fap_table,
        units_in="volt",
        units_out="ampere",
        calibration_date="2023-01-01",
        gain=2.5,
    )


@pytest.fixture
def frequency_array():
    """Fixture to provide a frequency array for testing."""
    return np.logspace(-5, 5, 100)


def test_default_filter(default_filter, subtests):
    """Test the default values of the FilterBase model."""
    with subtests.test("Default name"):
        assert default_filter.name == ""

    with subtests.test("Default comments"):
        assert isinstance(default_filter.comments, Comment)
        assert default_filter.comments.value == None

    with subtests.test("Default type"):
        assert default_filter.type == ""

    with subtests.test("Default units_in"):
        assert default_filter.units_in == ""

    with subtests.test("Default units_out"):
        assert default_filter.units_out == ""

    with subtests.test("Default calibration_date"):
        assert isinstance(default_filter.calibration_date, MTime)

    with subtests.test("Default gain"):
        assert default_filter.gain == 1.0


def test_custom_filter(custom_filter, subtests):
    """Test a custom FilterBase object."""
    with subtests.test("Custom name"):
        assert custom_filter.name == "lowpass_filter"

    with subtests.test("Custom comments"):
        assert isinstance(custom_filter.comments, Comment)
        assert custom_filter.comments.value == "Test filter for lowpass data"

    with subtests.test("Custom type"):
        assert custom_filter.type == FilterTypeEnum.fap_table

    with subtests.test("Custom units_in"):
        assert custom_filter.units_in == "volt"

    with subtests.test("Custom units_out"):
        assert custom_filter.units_out == "ampere"

    with subtests.test("Custom calibration_date"):
        assert isinstance(custom_filter.calibration_date, MTime)
        assert custom_filter.calibration_date.isoformat() == "2023-01-01T00:00:00+00:00"

    with subtests.test("Custom gain"):
        assert custom_filter.gain == 2.5


def test_invalid_calibration_date(default_filter, subtests):
    """Test invalid calibration_date values."""
    with subtests.test("Invalid string format"):
        with pytest.raises(ValidationError):
            default_filter.calibration_date = "invalid_date"

    with subtests.test("Invalid type"):
        with pytest.raises(TypeError):
            default_filter.calibration_date = {"date": "2023-01-01"}


def test_units_validation(default_filter, subtests):
    """Test validation of units_in and units_out."""
    with subtests.test("Valid units_in"):
        default_filter.units_in = "volt"
        assert default_filter.units_in == "volt"

    with subtests.test("Valid units_out"):
        default_filter.units_out = "ampere"
        assert default_filter.units_out == "ampere"

    with subtests.test("Invalid units_in"):
        with pytest.raises(KeyError):
            default_filter.units_in = "invalid_unit"

    with subtests.test("Invalid units_out"):
        with pytest.raises(KeyError):
            default_filter.units_out = "invalid_unit"


def test_comments_validation(default_filter, subtests):
    """Test validation of comments."""
    with subtests.test("Valid string comment"):
        default_filter.comments = "This is a test comment"
        assert isinstance(default_filter.comments, Comment)
        assert default_filter.comments.value == "This is a test comment"

    with subtests.test("Invalid comment type"):
        with pytest.raises(ValidationError):
            default_filter.comments = 12345


def test_complex_response(default_filter, frequency_array, subtests):
    """Test the complex_response method."""
    response = default_filter.complex_response(frequency_array)

    with subtests.test("Response is None"):
        assert response is None


def test_pass_band(default_filter, frequency_array, subtests):
    """Test the pass_band method."""
    pass_band = default_filter.pass_band(frequency_array)

    with subtests.test("Pass band is None"):
        assert pass_band is None


def test_total_gain(custom_filter, subtests):
    """Test the total_gain computed property."""
    with subtests.test("Total gain matches gain"):
        assert custom_filter.total_gain == custom_filter.gain


def test_obspy_mapping(default_filter, subtests):
    """Test the obspy_mapping property."""
    mapping = default_filter.obspy_mapping

    with subtests.test("Mapping is a dictionary"):
        assert isinstance(mapping, dict)

    with subtests.test("Mapping contains expected keys"):
        assert "stage_gain" in mapping
        assert "input_units" in mapping
        assert "output_units" in mapping
