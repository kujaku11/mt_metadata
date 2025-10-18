import numpy as np
import pytest

from mt_metadata.common import SymmetryEnum
from mt_metadata.timeseries.filters import FIRFilter


try:
    from obspy.core.inventory.response import FIRResponseStage

    OBSPY_AVAILABLE = True
except ImportError:
    OBSPY_AVAILABLE = False
    FIRResponseStage = None


@pytest.fixture
def fir_filter_default():
    """Fixture to create a default FIRFilter instance."""
    return FIRFilter()


@pytest.fixture
def fir_filter_with_data():
    """Fixture to create a FIRFilter instance with sample data."""
    return FIRFilter(
        coefficients=[0.25, 0.5, 0.3],
        decimation_factor=4.0,
        decimation_input_sample_rate=100.0,
        gain_frequency=1.0,
        symmetry=SymmetryEnum.EVEN,
        units_in="V/m",
        units_out="count",
    )


def test_default_fir_filter(fir_filter_default, subtests):
    """Test the default FIRFilter instance."""
    with subtests.test("test coefficients"):
        assert fir_filter_default.coefficients.size == 0

    with subtests.test("test decimation factor"):
        assert fir_filter_default.decimation_factor == 1.0

    with subtests.test("test gain frequency"):
        assert fir_filter_default.gain_frequency == 0.0

    with subtests.test("test symmetry"):
        assert fir_filter_default.symmetry == SymmetryEnum.NONE

    with subtests.test("test type"):
        assert fir_filter_default.type == "fir"


def test_fir_filter_with_data(fir_filter_with_data, subtests):
    """Test the FIRFilter instance with sample data."""
    with subtests.test("test coefficients"):
        assert np.allclose(fir_filter_with_data.coefficients, [0.25, 0.5, 0.3])

    with subtests.test("test decimation factor"):
        assert fir_filter_with_data.decimation_factor == 4.0

    with subtests.test("test gain frequency"):
        assert fir_filter_with_data.gain_frequency == 1.0

    with subtests.test("test symmetry"):
        assert fir_filter_with_data.symmetry == SymmetryEnum.EVEN


def test_symmetry_corrected_coefficients(fir_filter_with_data, subtests):
    """Test the symmetry_corrected_coefficients property."""
    test_cases = [
        (SymmetryEnum.EVEN, [0.25, 0.5, 0.3, 0.3, 0.5, 0.25]),
        (SymmetryEnum.ODD, [0.25, 0.5, 0.3, 0.3, 0.5]),
        (SymmetryEnum.NONE, [0.25, 0.5, 0.3]),
    ]

    for symmetry, expected in test_cases:
        with subtests.test(symmetry=symmetry):
            fir_filter_with_data.symmetry = symmetry
            assert np.allclose(
                fir_filter_with_data.symmetry_corrected_coefficients, expected
            )


def test_coefficient_gain(fir_filter_with_data, subtests):
    """Test the coefficient_gain property."""
    test_cases = [
        (0.0, 2.1),  # Gain frequency is 0.0
        (0.1, 2.09989094),  # Gain frequency is in the passband
    ]

    for gain_frequency, expected_gain in test_cases:
        with subtests.test(gain_frequency=gain_frequency):
            fir_filter_with_data.gain_frequency = gain_frequency
            assert np.isclose(fir_filter_with_data.coefficient_gain, expected_gain)


def test_corrective_scalar(fir_filter_with_data, subtests):
    """Test the corrective_scalar property."""
    with subtests.test("test with gain=1.0"):
        fir_filter_with_data.gain = 1.0
        assert np.isclose(fir_filter_with_data.corrective_scalar, 2.08911007)


def test_unscaled_complex_response(fir_filter_with_data, subtests):
    """Test the unscaled_complex_response method."""
    frequencies = np.array([0.1, 0.2, 0.3])
    response = fir_filter_with_data.unscaled_complex_response(frequencies)

    with subtests.test("test response is not None"):
        assert response is not None

    with subtests.test("test response length"):
        assert len(response) == len(frequencies)

    with subtests.test("test response type"):
        assert response.dtype == np.complex128


def test_complex_response(fir_filter_with_data, subtests):
    """Test the complex_response method."""
    frequencies = np.array([0.1, 0.2, 0.3])
    response = fir_filter_with_data.complex_response(frequencies)

    with subtests.test("test response is not None"):
        assert response is not None

    with subtests.test("test response length"):
        assert len(response) == len(frequencies)

    with subtests.test("test response type"):
        assert response.dtype == np.complex128

    with subtests.test("test response amplitudes"):
        # Verify the response is properly scaled by the corrective scalar
        unscaled = fir_filter_with_data.unscaled_complex_response(frequencies)
        corrective_scalar = fir_filter_with_data.corrective_scalar
        assert np.allclose(response, unscaled / corrective_scalar)


@pytest.mark.skipif(not OBSPY_AVAILABLE, reason="obspy is not installed.")
def test_to_obspy_stage(fir_filter_with_data, subtests):
    """Test the to_obspy method converts FirFilter to obspy FIRResponseStage correctly."""
    # Create an obspy stage from the filter
    stage = fir_filter_with_data.to_obspy(2, normalization_frequency=0.1)

    with subtests.test("test instance type"):
        assert isinstance(stage, FIRResponseStage)

    with subtests.test("test stage number"):
        assert stage.stage_sequence_number == 2

    with subtests.test("test gain"):
        assert stage.stage_gain == fir_filter_with_data.gain

    with subtests.test("test gain frequency"):
        assert stage.stage_gain_frequency == 0.1

    with subtests.test("test coefficients"):
        assert np.allclose(stage.coefficients, fir_filter_with_data.coefficients)

    with subtests.test("test symmetry"):
        assert stage.symmetry == "EVEN"  # FirFilter had SymmetryEnum.EVEN

    with subtests.test("test decimation factor"):
        assert stage.decimation_factor == fir_filter_with_data.decimation_factor

    with subtests.test("test input sample rate"):
        assert stage.decimation_input_sample_rate == 100

    with subtests.test("test units in"):
        assert stage.input_units == fir_filter_with_data.units_in_object.symbol

    with subtests.test("test units out"):
        assert stage.output_units == fir_filter_with_data.units_out_object.symbol

    with subtests.test("test units in description"):
        assert (
            stage.input_units_description == fir_filter_with_data.units_in_object.name
        )

    with subtests.test("test units out description"):
        assert (
            stage.output_units_description == fir_filter_with_data.units_out_object.name
        )

    with subtests.test("test description"):
        assert stage.description == "finite impaulse response filter"

    with subtests.test("test name"):
        assert stage.name == fir_filter_with_data.name


@pytest.mark.skipif(not OBSPY_AVAILABLE, reason="obspy is not installed.")
def test_to_obspy_stage_with_different_symmetry(subtests):
    """Test to_obspy with different symmetry values."""
    symmetry_mapping = [
        (SymmetryEnum.EVEN, "EVEN"),
        (SymmetryEnum.ODD, "ODD"),
        (SymmetryEnum.NONE, "NONE"),
    ]

    for enum_value, expected_string in symmetry_mapping:
        with subtests.test(symmetry=enum_value):
            fir_filter = FIRFilter(
                coefficients=[0.1, 0.5, 0.1],
                symmetry=enum_value,
                name=f"test_{expected_string.lower()}_symmetry",
                units_in="V/m",
                units_out="count",
            )

            stage = fir_filter.to_obspy(1, sample_rate=100, normalization_frequency=0.1)
            assert stage.symmetry == expected_string


@pytest.mark.skipif(not OBSPY_AVAILABLE, reason="obspy is not installed.")
def test_to_obspy_with_custom_parameters(subtests):
    """Test to_obspy with custom parameters."""
    # Create a filter with specific parameters
    custom_filter = FIRFilter(
        units_in="V/m",
        units_out="count",
        name="custom test filter",
        coefficients=[0.1, 0.3, 0.5, 0.3, 0.1],
        decimation_factor=8,
        gain=5.5,
        gain_frequency=0.25,
        symmetry=SymmetryEnum.EVEN,
        decimation_input_sample_rate=200.0,
    )

    # Set specific parameters for conversion
    stage_number = 4
    sample_rate = 200
    norm_freq = 0.2

    # Convert to obspy
    stage = custom_filter.to_obspy(stage_number, normalization_frequency=norm_freq)

    with subtests.test("test stage number"):
        assert stage.stage_sequence_number == stage_number

    with subtests.test("test sample rate"):
        assert stage.decimation_input_sample_rate == sample_rate

    with subtests.test("test normalization frequency"):
        assert stage.stage_gain_frequency == norm_freq

    with subtests.test("test gain"):
        assert stage.stage_gain == custom_filter.gain

    with subtests.test("test units"):
        assert stage.input_units == "V/m"
        assert stage.output_units == "count"

    with subtests.test("test coefficients"):
        assert np.allclose(stage.coefficients, custom_filter.coefficients)

    with subtests.test("test decimation"):
        assert stage.decimation_factor == 8


@pytest.mark.skipif(not OBSPY_AVAILABLE, reason="obspy is not installed.")
def test_from_obspy_stage(fir_filter_with_data, subtests):
    """Test the from_obspy_stage method."""
    # First, create an obspy stage from our filter
    obspy_stage = fir_filter_with_data.to_obspy(2, normalization_frequency=1)

    # Then create a new filter from the obspy stage
    new_filter = FIRFilter.from_obspy_stage(obspy_stage)

    with subtests.test("test coefficients"):
        assert np.allclose(new_filter.coefficients, fir_filter_with_data.coefficients)

    with subtests.test("test decimation factor"):
        assert new_filter.decimation_factor == fir_filter_with_data.decimation_factor

    with subtests.test("test gain"):
        assert np.isclose(new_filter.gain, fir_filter_with_data.gain)

    with subtests.test("test symmetry"):
        assert new_filter.symmetry == fir_filter_with_data.symmetry

    with subtests.test("test units in"):
        assert new_filter.units_in == fir_filter_with_data.units_in

    with subtests.test("test units out"):
        assert new_filter.units_out == fir_filter_with_data.units_out

    with subtests.test("test name"):
        assert new_filter.name == fir_filter_with_data.name

    with subtests.test("test type"):
        assert new_filter.type == "fir"


@pytest.mark.skipif(not OBSPY_AVAILABLE, reason="obspy is not installed.")
def test_from_obspy_stage_with_custom_parameters(subtests):
    """Test from_obspy_stage with manually created obspy stage."""
    # Create sample coefficients
    coeffs = [0.1, 0.2, 0.4, 0.2, 0.1]

    # Create an obspy stage with custom parameters
    custom_stage = FIRResponseStage(
        stage_sequence_number=3,
        stage_gain=2.5,
        stage_gain_frequency=0.25,
        input_units="V",
        input_units_description="volts",
        output_units="counts",
        output_units_description="digital counts",
        symmetry="EVEN",
        name="Custom FIR Filter",
        coefficients=coeffs,
        decimation_input_sample_rate=100.0,
        decimation_factor=2,
        decimation_offset=0,
        decimation_delay=0.01,
        decimation_correction=0.0,
    )

    # Create filter from stage
    filter_from_stage = FIRFilter.from_obspy_stage(custom_stage)

    with subtests.test("test filter type"):
        assert filter_from_stage.type == "fir"

    with subtests.test("test name"):
        assert filter_from_stage.name == "Custom FIR Filter"

    with subtests.test("test coefficients"):
        assert np.allclose(filter_from_stage.coefficients, coeffs)

    with subtests.test("test symmetry"):
        assert filter_from_stage.symmetry == SymmetryEnum.EVEN

    with subtests.test("test decimation factor"):
        assert filter_from_stage.decimation_factor == 2

    with subtests.test("test gain"):
        assert filter_from_stage.gain == 2.5

    with subtests.test("test gain frequency"):
        assert filter_from_stage.gain_frequency == 0.25

    with subtests.test("test units in"):
        assert filter_from_stage.units_in == "Volt"

    with subtests.test("test units out"):
        assert filter_from_stage.units_out == "digital counts"


@pytest.mark.skipif(not OBSPY_AVAILABLE, reason="obspy is not installed.")
def test_roundtrip_conversion(subtests):
    """Test round-trip conversion from FIRFilter to obspy and back."""
    # Create original filter with specific values
    coeffs = [0.05, 0.25, 0.4, 0.25, 0.05]
    original_filter = FIRFilter(
        units_in="mV",
        units_out="nT",
        name="test fir filter",
        coefficients=coeffs,
        decimation_factor=4,
        gain=2.0,
        gain_frequency=0.2,
        symmetry=SymmetryEnum.EVEN,
    )

    # Convert to obspy stage
    obspy_stage = original_filter.to_obspy(
        1, sample_rate=200, normalization_frequency=1
    )

    # Convert back to FIRFilter
    round_trip_filter = FIRFilter.from_obspy_stage(obspy_stage)

    with subtests.test("test coefficients preserved"):
        assert np.allclose(round_trip_filter.coefficients, original_filter.coefficients)

    with subtests.test("test decimation factor preserved"):
        assert round_trip_filter.decimation_factor == original_filter.decimation_factor

    with subtests.test("test gain preserved"):
        assert np.isclose(round_trip_filter.gain, original_filter.gain)

    with subtests.test("test symmetry preserved"):
        assert round_trip_filter.symmetry == original_filter.symmetry

    with subtests.test("test units in preserved"):
        assert round_trip_filter.units_in == original_filter.units_in

    with subtests.test("test units out preserved"):
        assert round_trip_filter.units_out == original_filter.units_out

    with subtests.test("test name preserved"):
        assert round_trip_filter.name == original_filter.name

    with subtests.test("test type preserved"):
        assert round_trip_filter.type == "fir"
