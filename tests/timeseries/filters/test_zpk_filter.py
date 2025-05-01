import pytest
import numpy as np
from mt_metadata.timeseries.filters import PoleZeroFilter
from pydantic import ValidationError

try:
    from obspy.core.inventory.response import PolesZerosResponseStage
except ImportError:
    PolesZerosResponseStage = None


@pytest.fixture
def pole_zero_filter_default():
    """Fixture to create a default PoleZeroFilter instance."""
    return PoleZeroFilter(
        units_in="volt", units_out="nanotesla", name="example_zpk_response"
    )


@pytest.fixture
def pole_zero_filter_with_data():
    """Fixture to create a PoleZeroFilter instance with sample data."""
    pz = PoleZeroFilter(
        units_in="volt", units_out="nanotesla", name="example_zpk_response"
    )
    pz.poles = [
        (-6.283185 + 10.882477j),
        (-6.283185 - 10.882477j),
        (-12.566371 + 0j),
    ]
    pz.zeros = []
    pz.normalization_factor = 2002.269
    return pz


@pytest.fixture
def frequencies():
    """Fixture to provide a range of frequencies for testing."""
    return np.logspace(-5, 5, 500)


def test_default_pole_zero_filter(pole_zero_filter_default):
    """Test the default PoleZeroFilter instance."""
    assert pole_zero_filter_default.poles.size == 0
    assert pole_zero_filter_default.zeros.size == 0
    assert pole_zero_filter_default.normalization_factor == 1.0
    assert pole_zero_filter_default.units_in == "volt"
    assert pole_zero_filter_default.units_out == "nanotesla"
    assert pole_zero_filter_default.name == "example_zpk_response"
    assert pole_zero_filter_default.type == "zpk"
    assert pole_zero_filter_default._filter_type == "zpk"


def test_pole_zero_filter_with_data(pole_zero_filter_with_data):
    """Test the PoleZeroFilter instance with sample data."""
    assert pole_zero_filter_with_data.poles.size == 3
    assert pole_zero_filter_with_data.zeros.size == 0
    assert pole_zero_filter_with_data.normalization_factor == 2002.269
    assert pole_zero_filter_with_data.units_in == "volt"
    assert pole_zero_filter_with_data.units_out == "nanotesla"
    assert pole_zero_filter_with_data.type == "zpk"
    assert pole_zero_filter_with_data._filter_type == "zpk"


def test_type(pole_zero_filter_with_data, subtests):
    """Test the type property."""
    with subtests.test(msg="string input"):
        pole_zero_filter_with_data.type = "fir"
        assert pole_zero_filter_with_data.type == "zpk"


def test_gain(pole_zero_filter_with_data, subtests):
    """Test the gain property."""
    with subtests.test(msg="string input"):
        pole_zero_filter_with_data.gain = ".25"
        assert pole_zero_filter_with_data.gain == 0.25

    with subtests.test(msg="integer input"):
        pole_zero_filter_with_data.gain = int(1)
        assert pole_zero_filter_with_data.gain == 1

    with subtests.test(msg="failing input"):
        with pytest.raises(ValidationError):
            pole_zero_filter_with_data.gain = {}


def test_poles_and_zeros_type(pole_zero_filter_with_data, subtests):
    """Test the types of poles and zeros."""
    with subtests.test("poles type"):
        assert isinstance(pole_zero_filter_with_data.poles, np.ndarray)

    with subtests.test("zeros type"):
        assert isinstance(pole_zero_filter_with_data.zeros, np.ndarray)


def test_pass_band(pole_zero_filter_with_data, frequencies):
    """Test the pass_band method."""
    pb = pole_zero_filter_with_data.pass_band(frequencies, tol=1e-2)
    assert np.allclose(pb, np.array([1.00000000e-05, 5.36363132e-01]))


def test_complex_response(pole_zero_filter_with_data, frequencies, subtests):
    """Test the complex_response method."""
    cr = pole_zero_filter_with_data.complex_response(frequencies)
    pb = pole_zero_filter_with_data.pass_band(frequencies, tol=1e-2)
    index_0 = np.where(frequencies == pb[0])[0][0]
    index_1 = np.where(frequencies == pb[-1])[0][0]

    with subtests.test("test dtype"):
        assert cr.dtype == np.complex128

    with subtests.test("test amplitude"):
        cr_amp = np.abs(cr)
        slope = np.log10(cr_amp[index_1] / cr_amp[index_0]) / np.log10(
            frequencies[index_1] / frequencies[index_0]
        )
        assert abs(slope) < 1e-4

    with subtests.test("test phase"):
        cr_phase = np.unwrap(np.angle(cr, deg=False))
        slope = (cr_phase[index_1] - cr_phase[index_0]) / np.log10(
            frequencies[index_1] / frequencies[index_0]
        )
        assert abs(slope) < 1


@pytest.mark.skipif(PolesZerosResponseStage is None, reason="obspy is not installed.")
def test_to_obspy_stage(pole_zero_filter_with_data, subtests):
    """Test the to_obspy method."""
    stage = pole_zero_filter_with_data.to_obspy(
        2, sample_rate=10, normalization_frequency=1
    )

    with subtests.test("test instance"):
        assert isinstance(stage, PolesZerosResponseStage)

    with subtests.test("test stage number"):
        assert stage.stage_sequence_number == 2

    with subtests.test("test gain"):
        assert stage.stage_gain == pole_zero_filter_with_data.gain

    with subtests.test("test poles"):
        assert np.allclose(stage.poles, pole_zero_filter_with_data.poles)

    with subtests.test("test zeros"):
        assert np.allclose(stage.zeros, pole_zero_filter_with_data.zeros)

    with subtests.test("test normalization frequency"):
        assert stage.stage_gain_frequency == 1

    with subtests.test("test units in"):
        assert stage.input_units == pole_zero_filter_with_data.units_in_object.symbol

    with subtests.test("test units out"):
        assert stage.output_units == pole_zero_filter_with_data.units_out_object.symbol

    with subtests.test("test units in description"):
        assert (
            stage.input_units_description
            == pole_zero_filter_with_data.units_in_object.name
        )
    with subtests.test("test units out description"):
        assert (
            stage.output_units_description
            == pole_zero_filter_with_data.units_out_object.name
        )

    with subtests.test("test description"):
        assert stage.description == "poles and zeros filter"

    with subtests.test("test name"):
        assert stage.name == pole_zero_filter_with_data.name


@pytest.mark.skipif(PolesZerosResponseStage is None, reason="obspy is not installed.")
def test_from_obspy_stage(pole_zero_filter_with_data, subtests):
    """Test the from_obspy_stage method."""
    # First, create an obspy stage from our filter
    obspy_stage = pole_zero_filter_with_data.to_obspy(
        2, sample_rate=10, normalization_frequency=1
    )

    # Then create a new filter from the obspy stage
    new_filter = PoleZeroFilter.from_obspy_stage(obspy_stage)

    with subtests.test("test poles"):
        assert np.allclose(new_filter.poles, pole_zero_filter_with_data.poles)

    with subtests.test("test zeros"):
        assert np.allclose(new_filter.zeros, pole_zero_filter_with_data.zeros)

    with subtests.test("test normalization factor"):
        assert (
            pytest.approx(new_filter.normalization_factor)
            == pole_zero_filter_with_data.normalization_factor
        )

    with subtests.test("test units"):
        assert new_filter.units_in == pole_zero_filter_with_data.units_in
        assert new_filter.units_out == pole_zero_filter_with_data.units_out

    with subtests.test("test name"):
        assert new_filter.name == pole_zero_filter_with_data.name

    with subtests.test("test type"):
        assert new_filter.type == "zpk"


@pytest.mark.skipif(PolesZerosResponseStage is None, reason="obspy is not installed.")
def test_from_obspy_stage_with_different_params(subtests):
    """Test from_obspy_stage with explicitly constructed obspy stage."""
    # Create an obspy stage with custom parameters
    custom_stage = PolesZerosResponseStage(
        stage_sequence_number=1,
        stage_gain=5.5,
        stage_gain_frequency=0.1,
        input_units="V",
        input_units_description="volts",
        output_units="counts",
        output_units_description="digital counts",
        pz_transfer_function_type="LAPLACE (RADIANS/SECOND)",
        normalization_frequency=0.5,
        normalization_factor=2.5,
        zeros=[(0 + 0j), (10 + 5j), (10 - 5j)],
        poles=[(-1 + 1j), (-1 - 1j), (-5 + 0j)],
        description="Custom PZ Filter",
        name="Custom Filter Name",
        resource_id=None,
        resource_id2=None,
    )

    # Create filter from stage
    filter_from_stage = PoleZeroFilter.from_obspy_stage(custom_stage)

    # Verify the filter properties using subtests
    with subtests.test("test type"):
        assert filter_from_stage.type == "zpk"

    with subtests.test("test name"):
        assert filter_from_stage.name == "Custom Filter Name"

    with subtests.test("test gain"):
        assert filter_from_stage.gain == 5.5

    with subtests.test("test poles"):
        assert np.allclose(filter_from_stage.poles, [(-1 + 1j), (-1 - 1j), (-5 + 0j)])

    with subtests.test("test zeros"):
        assert np.allclose(filter_from_stage.zeros, [(0 + 0j), (10 + 5j), (10 - 5j)])

    with subtests.test("test normalization factor"):
        assert filter_from_stage.normalization_factor == 2.5

    with subtests.test("test normalization frequency"):
        assert filter_from_stage.normalization_frequency() != 0.5

    with subtests.test("test units in"):
        assert filter_from_stage.units_in == "volt"

    with subtests.test("test units out"):
        assert filter_from_stage.units_out == "digital counts"
