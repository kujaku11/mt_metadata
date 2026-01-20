# -*- coding: utf-8 -*-
"""
Created on September 7, 2025

@author: GitHub Copilot

Pytest test suite for Band basemodel
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np
import pandas as pd
import pytest

from mt_metadata.common.band import Band, CenterAveragingTypeEnum, ClosedEnum

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def frequencies():
    """Standard frequency array for testing"""
    return 0.1 * np.arange(100)  # 0-10Hz


@pytest.fixture
def band_params():
    """Basic band parameters"""
    return {
        "frequency_min": 2.0,
        "frequency_max": 3.0,
        "decimation_level": 0,
        "index_min": 20,
        "index_max": 30,
        "center_averaging_type": CenterAveragingTypeEnum.geometric,
        "closed": ClosedEnum.left,
        "name": "test_band",
    }


@pytest.fixture
def band_default(band_params):
    """Default band with left-closed interval"""
    return Band(**band_params)


@pytest.fixture
def band_right_closed(band_params):
    """Band with right-closed interval"""
    params = band_params.copy()
    params["closed"] = "right"
    return Band(**params)


@pytest.fixture
def band_both_closed(band_params):
    """Band with both ends closed"""
    params = band_params.copy()
    params["closed"] = "both"
    return Band(**params)


@pytest.fixture
def band_arithmetic(band_params):
    """Band with arithmetic center averaging"""
    params = band_params.copy()
    params["center_averaging_type"] = "arithmetic"
    return Band(**params)


@pytest.fixture
def band_geometric(band_params):
    """Band with geometric center averaging"""
    params = band_params.copy()
    params["center_averaging_type"] = "geometric"
    return Band(**params)


# =============================================================================
# Test Classes
# =============================================================================


class TestBandInitialization:
    """Test Band initialization and basic properties"""

    def test_initialization_default(self):
        """Test default initialization"""
        # Based on Band field definitions, provide minimal required parameters
        band = Band(
            frequency_min=0.0,
            frequency_max=0.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            center_averaging_type=CenterAveragingTypeEnum.geometric,
            closed=ClosedEnum.left,
            name="test_band",
        )
        assert band.frequency_min == 0.0
        assert band.frequency_max == 0.0
        assert band.center_averaging_type == CenterAveragingTypeEnum.geometric
        assert band.closed == ClosedEnum.left
        assert band.decimation_level == 0
        assert band.index_min == 0
        assert band.index_max == 0

    def test_initialization_with_params(self, band_params):
        """Test initialization with parameters"""
        band = Band(**band_params)
        assert band.frequency_min == band_params["frequency_min"]
        assert band.frequency_max == band_params["frequency_max"]
        assert band.decimation_level == band_params["decimation_level"]

    @pytest.mark.parametrize("closed_type", ["left", "right", "both"])
    def test_closed_parameter(self, band_params, closed_type):
        """Test different closed parameter values"""
        params = band_params.copy()
        params["closed"] = closed_type
        band = Band(**params)
        assert band.closed == ClosedEnum(closed_type)

    @pytest.mark.parametrize("avg_type", ["arithmetic", "geometric"])
    def test_center_averaging_type(self, band_params, avg_type):
        """Test different center averaging types"""
        params = band_params.copy()
        params["center_averaging_type"] = avg_type
        band = Band(**params)
        assert band.center_averaging_type == CenterAveragingTypeEnum(avg_type)

    def test_copy(self, band_default):
        """Test band copying"""
        cloned = band_default.copy()
        assert band_default == cloned
        assert band_default is not cloned


class TestBandProperties:
    """Test computed properties and bounds"""

    def test_bounds_properties(self, band_default):
        """Test lower and upper bound properties"""
        assert band_default.lower_bound == 2.0
        assert band_default.upper_bound == 3.0
        assert band_default.width == 1.0

    @pytest.mark.parametrize(
        "closed_type,expected_lower,expected_upper",
        [
            ("left", True, False),
            ("right", False, True),
            ("both", True, True),
        ],
    )
    def test_closed_properties(
        self, band_params, closed_type, expected_lower, expected_upper
    ):
        """Test lower_closed and upper_closed properties"""
        params = band_params.copy()
        params["closed"] = closed_type
        band = Band(**params)

        assert band.lower_closed == expected_lower
        assert band.upper_closed == expected_upper

    def test_interval_conversion(self, band_default):
        """Test conversion to pandas Interval"""
        interval = band_default.to_interval()
        assert isinstance(interval, pd.Interval)
        assert interval.left == 2.0
        assert interval.right == 3.0
        assert interval.closed == "left"

    def test_fractional_bandwidth_and_q(self, band_default):
        """Test fractional bandwidth and Q factor calculations"""
        expected_center = np.sqrt(2.0 * 3.0)  # geometric mean
        expected_fb = 1.0 / expected_center  # width=1.0
        expected_q = 1.0 / expected_fb

        assert band_default.fractional_bandwidth == pytest.approx(expected_fb)
        assert band_default.Q == pytest.approx(expected_q)


class TestBandCenterFrequency:
    """Test center frequency calculations"""

    def test_geometric_center(self, band_geometric):
        """Test geometric center frequency calculation"""
        expected = np.sqrt(2.0 * 3.0)
        assert band_geometric.center_frequency == pytest.approx(expected)
        assert band_geometric.center_period == pytest.approx(1.0 / expected)

    def test_arithmetic_center(self, band_arithmetic):
        """Test arithmetic center frequency calculation"""
        expected = (2.0 + 3.0) / 2
        assert band_arithmetic.center_frequency == pytest.approx(expected)
        assert band_arithmetic.center_period == pytest.approx(1.0 / expected)


class TestBandIndicesAndHarmonics:
    """Test frequency indexing and harmonic calculations"""

    def test_indices_from_frequencies_left_closed(self, band_default, frequencies):
        """Test index calculation for left-closed band"""
        band_default.set_indices_from_frequencies(frequencies)

        assert band_default.index_min == 20  # frequencies[20] = 2.0
        assert band_default.index_max == 29  # frequencies[29] = 2.9

    def test_indices_from_frequencies_right_closed(
        self, band_right_closed, frequencies
    ):
        """Test index calculation for right-closed band"""
        band_right_closed.set_indices_from_frequencies(frequencies)

        assert band_right_closed.index_min == 21  # frequencies[21] = 2.1
        assert band_right_closed.index_max == 30  # frequencies[30] = 3.0

    def test_indices_from_frequencies_both_closed(self, band_both_closed, frequencies):
        """Test index calculation for both-closed band"""
        band_both_closed.set_indices_from_frequencies(frequencies)

        assert band_both_closed.index_min == 20  # frequencies[20] = 2.0
        assert band_both_closed.index_max == 30  # frequencies[30] = 3.0

    def test_harmonic_indices(self, band_default, frequencies):
        """Test harmonic indices property"""
        band_default.set_indices_from_frequencies(frequencies)
        expected = np.arange(20, 30)  # index_min to index_max + 1
        np.testing.assert_array_equal(band_default.harmonic_indices, expected)

    def test_in_band_harmonics_left_closed(self, band_default, frequencies):
        """Test in-band harmonics for left-closed band"""
        harmonics = band_default.in_band_harmonics(frequencies)

        assert harmonics[0] == pytest.approx(2.0)  # min frequency included
        assert harmonics[-1] == pytest.approx(2.9)  # max frequency excluded

    def test_in_band_harmonics_right_closed(self, band_right_closed, frequencies):
        """Test in-band harmonics for right-closed band"""
        harmonics = band_right_closed.in_band_harmonics(frequencies)

        assert harmonics[0] == pytest.approx(2.1)  # min frequency excluded
        assert harmonics[-1] == pytest.approx(3.0)  # max frequency included

    def test_in_band_harmonics_both_closed(self, band_both_closed, frequencies):
        """Test in-band harmonics for both-closed band"""
        harmonics = band_both_closed.in_band_harmonics(frequencies)

        assert harmonics[0] == pytest.approx(2.0)  # min frequency included
        assert harmonics[-1] == pytest.approx(3.0)  # max frequency included


class TestBandNameValidation:
    """Test name validation and generation"""

    def test_name_auto_generation_with_frequencies(self):
        """Test automatic name generation from center frequency when frequencies provided"""
        band = Band(
            frequency_min=2.0,
            frequency_max=4.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
        )
        # Should auto-generate name as center frequency: (2.0 + 4.0) / 2 = 3.0
        assert band.name == "3.000000"

    def test_name_empty_band_when_no_frequencies(self):
        """Test that 'empty_band' is generated when frequencies are zero"""
        band = Band(
            frequency_min=0.0,
            frequency_max=0.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
        )
        assert band.name == "empty_band"

    def test_name_custom_preserved(self):
        """Test custom name is preserved"""
        band = Band(
            frequency_min=2.0,
            frequency_max=4.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            name="custom_band",
        )
        assert band.name == "custom_band"

    def test_name_empty_string_generates_center_frequency(self):
        """Test that empty string generates center frequency name"""
        band = Band(
            frequency_min=1.0,
            frequency_max=3.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            name="",
        )
        # Should generate name as center frequency: (1.0 + 3.0) / 2 = 2.0
        assert band.name == "2.000000"

    def test_name_none_generates_center_frequency(self):
        """Test that None generates center frequency name"""
        band = Band(
            frequency_min=1.0,
            frequency_max=5.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            name=None,
        )
        # Should generate name as center frequency: (1.0 + 5.0) / 2 = 3.0
        assert band.name == "3.000000"

    def test_post_instantiation_frequency_update(self):
        """Test that name updates when frequencies are set after instantiation"""
        # Create band without frequencies (should get 'empty_band' name)
        band = Band(
            frequency_min=0.0,
            frequency_max=0.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
        )
        assert band.name == "empty_band"

        # Update frequencies - name should automatically update
        band.frequency_min = 2.0
        band.frequency_max = 6.0
        # Should update to center frequency: (2.0 + 6.0) / 2 = 4.0
        assert band.name == "4.000000"

    def test_post_instantiation_frequency_update_preserves_custom_name(self):
        """Test that custom names are preserved when frequencies are updated"""
        band = Band(
            frequency_min=1.0,
            frequency_max=2.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            name="my_custom_band",
        )
        assert band.name == "my_custom_band"

        # Update frequencies - custom name should be preserved
        band.frequency_min = 3.0
        band.frequency_max = 4.0
        assert band.name == "my_custom_band"

    def test_empty_band_to_frequencies_updates_name(self):
        """Test specific case of transitioning from empty_band to valid frequencies"""
        # Start with empty band
        band = Band(
            frequency_min=0.0,
            frequency_max=0.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
        )
        assert band.name == "empty_band"

        # Set frequencies one at a time
        band.frequency_min = 1.0
        # Still should be empty_band since max is still 0
        assert band.name == "empty_band"

        band.frequency_max = 3.0
        # Now should update to center frequency: (1.0 + 3.0) / 2 = 2.0
        assert band.name == "2.000000"

    def test_frequencies_to_zero_keeps_generated_name(self):
        """Test that setting frequencies back to zero doesn't change already generated name"""
        band = Band(
            frequency_min=1.0,
            frequency_max=2.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
        )
        # Should have auto-generated name
        original_name = band.name
        assert original_name == "1.500000"

        # Set frequencies back to zero
        band.frequency_min = 0.0
        band.frequency_max = 0.0
        # Name should remain the same (not change to empty_band)
        assert band.name == original_name


class TestBandRelationships:
    """Test band overlap and containment relationships"""

    def test_overlaps_true(self, band_params):
        """Test overlapping bands"""
        band1 = Band(**band_params)  # 2.0 - 3.0

        params2 = band_params.copy()
        params2.update({"frequency_min": 2.5, "frequency_max": 3.5})
        band2 = Band(**params2)  # 2.5 - 3.5

        assert band1.overlaps(band2)
        assert band2.overlaps(band1)

    def test_overlaps_false(self, band_params):
        """Test non-overlapping bands"""
        band1 = Band(**band_params)  # 2.0 - 3.0

        params2 = band_params.copy()
        params2.update({"frequency_min": 4.0, "frequency_max": 5.0})
        band2 = Band(**params2)  # 4.0 - 5.0

        assert not band1.overlaps(band2)
        assert not band2.overlaps(band1)

    def test_contains_true(self, band_params):
        """Test band containment"""
        # Larger band
        params1 = band_params.copy()
        params1.update({"frequency_min": 1.0, "frequency_max": 4.0})
        band1 = Band(**params1)  # 1.0 - 4.0

        # Smaller band inside
        band2 = Band(**band_params)  # 2.0 - 3.0

        assert band1.contains(band2)
        assert not band2.contains(band1)

    def test_contains_false(self, band_params):
        """Test band non-containment"""
        band1 = Band(**band_params)  # 2.0 - 3.0

        params2 = band_params.copy()
        params2.update({"frequency_min": 2.5, "frequency_max": 3.5})
        band2 = Band(**params2)  # 2.5 - 3.5 (overlaps but not contained)

        assert not band1.contains(band2)
        assert not band2.contains(band1)


class TestBandEdgeCases:
    """Test edge cases and error conditions"""

    def test_zero_width_band(self):
        """Test band with zero width"""
        band = Band(
            frequency_min=2.0,
            frequency_max=2.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            center_averaging_type=CenterAveragingTypeEnum.geometric,
            closed=ClosedEnum.left,
            name="zero_width",
        )
        assert band.width == 0.0
        assert band.fractional_bandwidth == 0.0
        assert np.isinf(band.Q)  # Q = 1/0 = inf

    def test_negative_frequencies(self):
        """Test band with negative frequencies"""
        band = Band(
            frequency_min=-1.0,
            frequency_max=1.0,
            decimation_level=0,
            index_min=0,
            index_max=0,
            center_averaging_type=CenterAveragingTypeEnum.geometric,
            closed=ClosedEnum.left,
            name="negative_freq",
        )
        assert band.lower_bound == -1.0
        assert band.upper_bound == 1.0
        assert band.width == 2.0

    def test_very_small_frequencies(self):
        """Test band with very small frequencies"""
        band = Band(
            frequency_min=1e-6,
            frequency_max=1e-5,
            decimation_level=0,
            index_min=0,
            index_max=0,
            center_averaging_type=CenterAveragingTypeEnum.geometric,
            closed=ClosedEnum.left,
            name="small_freq",
        )
        assert band.lower_bound == 1e-6
        assert band.upper_bound == 1e-5
        assert band.center_frequency == pytest.approx(np.sqrt(1e-6 * 1e-5))

    def test_private_indices_method(self, band_default, frequencies):
        """Test the private _indices_from_frequencies method"""
        indices = band_default._indices_from_frequencies(frequencies)
        expected = np.arange(20, 30)  # 2.0 <= freq < 3.0
        np.testing.assert_array_equal(indices, expected)


# =============================================================================
# Performance and Integration Tests
# =============================================================================


class TestBandPerformance:
    """Test performance characteristics"""

    def test_large_frequency_array(self, band_default):
        """Test with large frequency arrays"""
        large_freqs = np.linspace(0, 100, 10000)
        band_default.set_indices_from_frequencies(large_freqs)

        # Should complete without error
        assert band_default.index_min is not None
        assert band_default.index_max is not None
        assert band_default.index_min <= band_default.index_max

    def test_multiple_bands_operations(self, frequencies):
        """Test operations with multiple bands"""
        bands = []
        for i in range(10):
            band = Band(
                frequency_min=i * 0.5,
                frequency_max=(i + 1) * 0.5,
                decimation_level=i,
                index_min=0,
                index_max=0,
                center_averaging_type=CenterAveragingTypeEnum.geometric,
                closed=ClosedEnum.left,
                name=f"band_{i}",
            )
            band.set_indices_from_frequencies(frequencies)
            bands.append(band)

        # Test all bands were created and configured correctly
        assert len(bands) == 10
        for i, band in enumerate(bands):
            assert band.decimation_level == i
            assert band.frequency_min == i * 0.5
            assert band.frequency_max == (i + 1) * 0.5


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
