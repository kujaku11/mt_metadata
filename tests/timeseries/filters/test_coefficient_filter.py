import numpy as np
import pytest
from pydantic import ValidationError

from mt_metadata.timeseries.filters import CoefficientFilter
from mt_metadata.timeseries.filters.helper_functions import MT2SI_MAGNETIC_FIELD_FILTER


@pytest.fixture
def default_coefficient_filter():
    """Fixture to create a default CoefficientFilter object."""
    return CoefficientFilter()


@pytest.fixture
def custom_coefficient_filter():
    """Fixture to create a custom CoefficientFilter object."""
    return CoefficientFilter(
        name="test_coefficient_filter",
        gain=100.0,
        comments="This is a test coefficient filter.",
    )


def test_default_coefficient_filter(default_coefficient_filter, subtests):
    """Test the default values of the CoefficientFilter model."""
    with subtests.test("Default name"):
        assert default_coefficient_filter.name == ""

    with subtests.test("Default gain"):
        assert default_coefficient_filter.gain == 1.0

    with subtests.test("Default comments"):
        assert default_coefficient_filter.comments.value == None

    with subtests.test("Default filter type"):
        assert default_coefficient_filter.type == "coefficient"


def test_custom_coefficient_filter(custom_coefficient_filter, subtests):
    """Test a custom CoefficientFilter object."""
    with subtests.test("Custom name"):
        assert custom_coefficient_filter.name == "test_coefficient_filter"

    with subtests.test("Custom gain"):
        assert custom_coefficient_filter.gain == 100.0

    with subtests.test("Custom comments"):
        assert (
            custom_coefficient_filter.comments.value
            == "This is a test coefficient filter."
        )


def test_invalid_gain(default_coefficient_filter, subtests):
    """Test invalid gain values."""
    with subtests.test("Non-numeric gain"):
        with pytest.raises(ValidationError):
            default_coefficient_filter.gain = "invalid_gain"


def test_update_gain(default_coefficient_filter, subtests):
    """Test updating the gain value."""
    with subtests.test("Valid gain update"):
        default_coefficient_filter.gain = 50.0
        assert default_coefficient_filter.gain == 50.0


@pytest.fixture
def default_coefficient_filter_with_units():
    """Fixture to create a default CoefficientFilter object."""
    return CoefficientFilter(units_in="V", units_out="V", name="coefficient", gain=10)


@pytest.fixture
def frequency_array():
    """Fixture to provide a frequency array for testing."""
    return np.logspace(-5, 5, 100)


def test_gain(default_coefficient_filter_with_units, subtests):
    """Test setting and validating the gain attribute."""
    with subtests.test("String input"):
        default_coefficient_filter_with_units.gain = "10.5"
        assert default_coefficient_filter_with_units.gain == 10.5

    with subtests.test("Integer input"):
        default_coefficient_filter_with_units.gain = int(10)
        assert default_coefficient_filter_with_units.gain == 10.0

    with subtests.test("Invalid input"):
        with pytest.raises(ValidationError):
            default_coefficient_filter_with_units.gain = "a"


def test_complex_response(
    default_coefficient_filter_with_units, frequency_array, subtests
):
    """Test the complex response of the CoefficientFilter."""
    cr = default_coefficient_filter_with_units.complex_response(frequency_array)

    with subtests.test("Test dtype"):
        assert cr.dtype.type == np.complex128

    with subtests.test("Test amplitude"):
        cr_amp = np.abs(cr)
        amp = np.repeat(10, frequency_array.size)
        assert np.isclose(cr_amp, amp).all()

    with subtests.test("Test phase"):
        cr_phase = np.angle(cr, deg=True)
        phase = np.repeat(0, frequency_array.size)
        assert np.isclose(cr_phase, phase).all()


@pytest.mark.skipif("obspy" not in globals(), reason="obspy is not installed.")
def test_to_obspy_stage(default_coefficient_filter_with_units, subtests):
    """Test converting CoefficientFilter to an ObsPy stage."""
    stage = default_coefficient_filter_with_units.to_obspy(
        2, sample_rate=10, normalization_frequency=1
    )

    with subtests.test("Test stage number"):
        assert stage.stage_sequence_number == 2

    with subtests.test("Test gain"):
        assert stage.stage_gain == default_coefficient_filter_with_units.gain

    with subtests.test("Test normalization frequency"):
        assert stage.stage_gain_frequency == 1

    with subtests.test("Test units in"):
        assert stage.input_units == default_coefficient_filter_with_units.units_in

    with subtests.test("Test units out"):
        assert stage.output_units == default_coefficient_filter_with_units.units_out

    with subtests.test("Test units out description"):
        assert (
            stage.output_units_description
            == default_coefficient_filter_with_units._units_out_obj.name
        )

    with subtests.test("Test description"):
        assert stage.description == "coefficient filter"

    with subtests.test("Test name"):
        assert stage.name == default_coefficient_filter_with_units.name


def test_helper_functions(subtests):
    """Test helper functions related to CoefficientFilter."""
    with subtests.test("MT2SI_MAGNETIC_FIELD_FILTER units_in"):
        assert MT2SI_MAGNETIC_FIELD_FILTER.units_in == "nanoTesla"
