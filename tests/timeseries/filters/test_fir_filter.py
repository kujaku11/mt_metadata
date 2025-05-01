import pytest
import numpy as np
from mt_metadata.timeseries.filters import FirFilter
from mt_metadata.common import SymmetryEnum


@pytest.fixture
def fir_filter_default():
    """Fixture to create a default FirFilter instance."""
    return FirFilter()


@pytest.fixture
def fir_filter_with_data():
    """Fixture to create a FirFilter instance with sample data."""
    return FirFilter(
        coefficients=[0.25, 0.5, 0.3],
        decimation_factor=4.0,
        gain_frequency=0.1,
        symmetry=SymmetryEnum.EVEN,
    )


def test_default_fir_filter(fir_filter_default):
    """Test the default FirFilter instance."""
    assert fir_filter_default.coefficients.size == 0
    assert fir_filter_default.decimation_factor == 1.0
    assert fir_filter_default.gain_frequency == 0.0
    assert fir_filter_default.symmetry == SymmetryEnum.NONE
    assert fir_filter_default.type == "fir"


def test_fir_filter_with_data(fir_filter_with_data):
    """Test the FirFilter instance with sample data."""
    assert np.allclose(fir_filter_with_data.coefficients, [0.25, 0.5, 0.3])
    assert fir_filter_with_data.decimation_factor == 4.0
    assert fir_filter_with_data.gain_frequency == 0.1
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
        (0.1, 1.15841916),  # Gain frequency is in the passband
    ]

    for gain_frequency, expected_gain in test_cases:
        with subtests.test(gain_frequency=gain_frequency):
            fir_filter_with_data.gain_frequency = gain_frequency
            assert np.isclose(fir_filter_with_data.coefficient_gain, expected_gain)


def test_corrective_scalar(fir_filter_with_data):
    """Test the corrective_scalar property."""
    fir_filter_with_data.gain = 1.0
    assert np.isclose(fir_filter_with_data.corrective_scalar, 1.15841916)


def test_unscaled_complex_response(fir_filter_with_data):
    """Test the unscaled_complex_response method."""
    frequencies = np.array([0.1, 0.2, 0.3])
    response = fir_filter_with_data.unscaled_complex_response(frequencies)
    assert response is not None
    assert len(response) == len(frequencies)


def test_complex_response(fir_filter_with_data):
    """Test the complex_response method."""
    frequencies = np.array([0.1, 0.2, 0.3])
    response = fir_filter_with_data.complex_response(frequencies)
    assert response is not None
    assert len(response) == len(frequencies)
