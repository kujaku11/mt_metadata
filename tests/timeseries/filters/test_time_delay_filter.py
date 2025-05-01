import pytest
import numpy as np
from mt_metadata.timeseries.filters import TimeDelayFilter
from pydantic import ValidationError

try:
    from obspy.core.inventory.response import CoefficientsTypeResponseStage
except ImportError:
    CoefficientsTypeResponseStage = None


@pytest.fixture
def time_delay_filter_default():
    """Fixture to create a default TimeDelayFilter instance."""
    return TimeDelayFilter(units_in="V", units_out="V", name="time delay")


@pytest.fixture
def time_delay_filter_with_data():
    """Fixture to create a TimeDelayFilter instance with sample data."""
    return TimeDelayFilter(units_in="V", units_out="V", name="time delay", delay=-0.250)


@pytest.fixture
def frequencies():
    """Fixture to provide a range of frequencies for testing."""
    return np.logspace(-5, 5, 100)


def test_default_time_delay_filter(time_delay_filter_default):
    """Test the default TimeDelayFilter instance."""
    assert time_delay_filter_default.delay == 0.0
    assert time_delay_filter_default.units_in == "volt"
    assert time_delay_filter_default.units_out == "volt"
    assert time_delay_filter_default.name == "time delay"
    assert time_delay_filter_default.type == "time delay"


def test_time_delay_filter_with_data(time_delay_filter_with_data):
    """Test the TimeDelayFilter instance with sample data."""
    assert time_delay_filter_with_data.delay == -0.250
    assert time_delay_filter_with_data.units_in == "volt"
    assert time_delay_filter_with_data.units_out == "volt"
    assert time_delay_filter_with_data.name == "time delay"
    assert time_delay_filter_with_data.type == "time delay"


def test_filter_type(time_delay_filter_with_data):
    """Test the filter type."""
    time_delay_filter_default.type = "fir"
    assert time_delay_filter_with_data.type == "time delay"


def test_delay_property(time_delay_filter_with_data, subtests):
    """Test the delay property."""
    with subtests.test(msg="string input"):
        time_delay_filter_with_data.delay = "-.25"
        assert time_delay_filter_with_data.delay == -0.25

    with subtests.test(msg="integer input"):
        time_delay_filter_with_data.delay = int(1)
        assert time_delay_filter_with_data.delay == 1

    with subtests.test(msg="failing input"):
        with pytest.raises(ValidationError):
            time_delay_filter_with_data.delay = "a"


def test_complex_response(time_delay_filter_with_data, frequencies, subtests):
    """Test the complex_response method."""
    cr = time_delay_filter_with_data.complex_response(frequencies)

    with subtests.test("test dtype"):
        assert cr.dtype == np.complex128

    with subtests.test("test amplitude"):
        cr_amp = np.abs(cr)
        amp = np.ones_like(frequencies)
        assert np.allclose(cr_amp, amp)

    with subtests.test("test phase"):
        cr_phase = np.angle(cr, deg=True)
        phase = np.zeros_like(frequencies)
        assert not np.allclose(cr_phase, phase)


def test_pass_band(time_delay_filter_with_data, frequencies):
    """Test the pass_band method."""
    pb = time_delay_filter_with_data.pass_band(frequencies)
    assert np.allclose(pb, np.array([frequencies.min(), frequencies.max()]))


@pytest.mark.skipif(
    CoefficientsTypeResponseStage is None, reason="obspy is not installed."
)
def test_to_obspy_stage(time_delay_filter_with_data, subtests):
    """Test the to_obspy method."""
    stage = time_delay_filter_with_data.to_obspy(
        2, sample_rate=10, normalization_frequency=1
    )

    with subtests.test("test stage number"):
        assert stage.stage_sequence_number == 2

    with subtests.test("test gain"):
        assert stage.stage_gain == time_delay_filter_with_data.gain

    with subtests.test("test decimation delay"):
        assert stage.decimation_delay == time_delay_filter_with_data.delay

    with subtests.test("test normalization frequency"):
        assert stage.stage_gain_frequency == 1

    with subtests.test("test units in"):
        assert stage.input_units == time_delay_filter_with_data.units_in_object.symbol

    with subtests.test("test units out"):
        assert stage.output_units == time_delay_filter_with_data.units_out_object.symbol

    with subtests.test("test units out description"):
        assert (
            stage.output_units_description
            == time_delay_filter_with_data.units_out_object.name
        )
    with subtests.test("test units in description"):
        assert (
            stage.input_units_description
            == time_delay_filter_with_data.units_in_object.name
        )

    with subtests.test("test description"):
        assert stage.description == "time delay filter"

    with subtests.test("test name"):
        assert stage.name == time_delay_filter_with_data.name

    with subtests.test("test type"):
        assert isinstance(stage, CoefficientsTypeResponseStage)
