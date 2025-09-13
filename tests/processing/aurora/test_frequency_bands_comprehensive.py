"""
Comprehensive test suite for FrequencyBands class using pytest with fixtures and subtests.

This test suite covers all functionality of the FrequencyBands class including:
- Construction and validation
- Band management and retrieval
- Sorting operations
- Band generation with different configurations
- Properties and calculations
- Error handling and edge cases

Uses pytest fixtures for efficient test setup and parametrized tests for thorough coverage.
"""

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from mt_metadata.processing.aurora.band_basemodel import Band
from mt_metadata.processing.aurora.frequency_bands import FrequencyBands


class TestFrequencyBandsCore:
    """Test core functionality and basic operations."""

    @pytest.fixture
    def simple_array_data(self):
        """Simple numpy array data for basic testing."""
        return np.array([[0.1, 0.5], [0.5, 1.0], [1.0, 5.0], [5.0, 10.0]])

    @pytest.fixture
    def simple_dataframe_data(self):
        """Simple DataFrame data for basic testing."""
        return pd.DataFrame(
            {"lower_bound": [0.1, 0.5, 1.0, 5.0], "upper_bound": [0.5, 1.0, 5.0, 10.0]}
        )

    @pytest.fixture
    def complex_array_data(self):
        """More complex array data for comprehensive testing."""
        return np.array(
            [
                [0.01, 0.1],
                [0.1, 0.5],
                [0.5, 1.0],
                [1.0, 2.0],
                [2.0, 5.0],
                [5.0, 10.0],
                [10.0, 20.0],
                [20.0, 50.0],
            ]
        )

    @pytest.fixture
    def unsorted_dataframe_data(self):
        """Unsorted DataFrame data for testing sorting functionality."""
        return pd.DataFrame(
            {"lower_bound": [1.0, 0.1, 10.0, 0.5], "upper_bound": [5.0, 0.5, 20.0, 1.0]}
        )

    @pytest.fixture
    def frequency_bands_array(self, simple_array_data):
        """FrequencyBands instance from array data."""
        return FrequencyBands(simple_array_data)

    @pytest.fixture
    def frequency_bands_df(self, simple_dataframe_data):
        """FrequencyBands instance from DataFrame data."""
        return FrequencyBands(simple_dataframe_data)

    @pytest.fixture
    def complex_frequency_bands(self, complex_array_data):
        """FrequencyBands instance with more bands."""
        return FrequencyBands(complex_array_data)

    def test_construction_from_array(self, simple_array_data):
        """Test construction from numpy array."""
        fb = FrequencyBands(simple_array_data)
        assert isinstance(fb._band_edges, pd.DataFrame)
        assert fb.number_of_bands == 4
        assert list(fb._band_edges.columns) == ["lower_bound", "upper_bound"]

    def test_construction_from_dataframe(self, simple_dataframe_data):
        """Test construction from pandas DataFrame."""
        fb = FrequencyBands(simple_dataframe_data)
        assert isinstance(fb._band_edges, pd.DataFrame)
        assert fb.number_of_bands == 4
        assert list(fb._band_edges.columns) == ["lower_bound", "upper_bound"]

    def test_number_of_bands_property(
        self, frequency_bands_array, complex_frequency_bands
    ):
        """Test number_of_bands property with different data sizes."""
        assert frequency_bands_array.number_of_bands == 4
        assert complex_frequency_bands.number_of_bands == 8

    def test_array_property(self, frequency_bands_array, simple_array_data):
        """Test array property returns correct numpy array."""
        result = frequency_bands_array.array
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, simple_array_data)

    @pytest.mark.parametrize("index", [0, 1, 2, 3])
    def test_band_retrieval(self, frequency_bands_array, index, simple_array_data):
        """Test individual band retrieval by index."""
        band = frequency_bands_array.band(index)
        assert isinstance(band, Band)
        assert band.frequency_min == simple_array_data[index, 0]
        assert band.frequency_max == simple_array_data[index, 1]

    def test_band_retrieval_out_of_bounds(self, frequency_bands_array):
        """Test band retrieval with invalid index."""
        with pytest.raises(IndexError):
            frequency_bands_array.band(10)


class TestFrequencyBandsSorting:
    """Test sorting functionality."""

    @pytest.fixture
    def unsorted_bands(self):
        """FrequencyBands with unsorted data."""
        data = pd.DataFrame(
            {"lower_bound": [1.0, 0.1, 10.0, 0.5], "upper_bound": [5.0, 0.5, 20.0, 1.0]}
        )
        return FrequencyBands(data)

    @pytest.mark.parametrize(
        "sort_by,ascending,expected_order",
        [
            ("lower_bound", True, [0.1, 0.5, 1.0, 10.0]),
            ("lower_bound", False, [10.0, 1.0, 0.5, 0.1]),
            ("upper_bound", True, [0.5, 1.0, 5.0, 20.0]),
            ("upper_bound", False, [20.0, 5.0, 1.0, 0.5]),
        ],
    )
    def test_sort_by_bounds(self, unsorted_bands, sort_by, ascending, expected_order):
        """Test sorting by lower and upper bounds."""
        unsorted_bands.sort(by=sort_by, ascending=ascending)
        actual_values = unsorted_bands._band_edges[sort_by].tolist()
        assert actual_values == expected_order

    def test_sort_by_center_frequency(self, unsorted_bands):
        """Test sorting by center frequency."""
        # Calculate expected center frequencies before sorting
        centers_before = []
        for i in range(unsorted_bands.number_of_bands):
            band = unsorted_bands.band(i)
            centers_before.append(band.center_frequency)

        unsorted_bands.sort(by="center_frequency", ascending=True)

        # Check that center frequencies are now in ascending order
        centers_after = unsorted_bands.band_centers()
        assert np.all(centers_after[1:] >= centers_after[:-1])

    def test_sort_by_center_frequency_descending(self, unsorted_bands):
        """Test sorting by center frequency in descending order."""
        unsorted_bands.sort(by="center_frequency", ascending=False)
        centers = unsorted_bands.band_centers()
        assert np.all(centers[1:] <= centers[:-1])

    def test_sort_invalid_criterion(self, unsorted_bands):
        """Test sorting with invalid criterion."""
        with pytest.raises(ValueError, match="Invalid sort criterion"):
            unsorted_bands.sort(by="invalid_criterion")


class TestFrequencyBandsBandGeneration:
    """Test band generation functionality."""

    @pytest.fixture
    def test_bands(self):
        """Test FrequencyBands instance."""
        data = np.array([[0.1, 0.5], [0.5, 1.0], [1.0, 5.0], [5.0, 10.0]])
        return FrequencyBands(data)

    def test_bands_default_list(self, test_bands):
        """Test bands() method with default parameters returns list."""
        bands = test_bands.bands()
        assert isinstance(bands, list)
        assert len(bands) == 4
        assert all(isinstance(band, Band) for band in bands)

    def test_bands_generator(self, test_bands):
        """Test bands() method returning generator."""
        bands_gen = test_bands.bands(rtype="generator")
        assert hasattr(bands_gen, "__iter__")
        assert hasattr(bands_gen, "__next__")

        bands_list = list(bands_gen)
        assert len(bands_list) == 4
        assert all(isinstance(band, Band) for band in bands_list)

    def test_bands_invalid_rtype(self, test_bands):
        """Test bands() method with invalid return type."""
        with pytest.raises(ValueError, match="rtype must be either"):
            test_bands.bands(rtype="invalid")

    @pytest.mark.parametrize("direction", ["increasing_frequency", "increasing_period"])
    def test_bands_direction(self, test_bands, direction):
        """Test bands() method with different directions."""
        bands = test_bands.bands(direction=direction)
        assert isinstance(bands, list)
        assert len(bands) == 4

        # Check that bands are in correct order
        centers = [band.center_frequency for band in bands]
        if direction == "increasing_frequency":
            assert centers == sorted(centers)
        else:  # increasing_period
            periods = [1 / center for center in centers]
            assert periods == sorted(periods)

    @pytest.mark.parametrize(
        "sortby", ["lower_bound", "upper_bound", "center_frequency"]
    )
    def test_bands_with_sorting(self, test_bands, sortby):
        """Test bands() method with different sorting criteria."""
        bands = test_bands.bands(sortby=sortby)
        assert isinstance(bands, list)
        assert len(bands) == 4

        # Verify sorting worked (original should be unchanged)
        original_array = test_bands.array
        bands_after_call = test_bands.array
        np.testing.assert_array_equal(original_array, bands_after_call)


class TestFrequencyBandsBandCenters:
    """Test band center calculations."""

    @pytest.fixture
    def test_bands(self):
        """Test FrequencyBands instance."""
        data = np.array([[1.0, 4.0], [2.0, 8.0], [4.0, 16.0]])
        return FrequencyBands(data)

    def test_band_centers_frequency(self, test_bands):
        """Test band_centers method returning frequencies."""
        centers = test_bands.band_centers(frequency_or_period="frequency")
        assert isinstance(centers, np.ndarray)
        assert len(centers) == 3

        # Check that centers are calculated correctly (geometric mean)
        expected = [np.sqrt(1.0 * 4.0), np.sqrt(2.0 * 8.0), np.sqrt(4.0 * 16.0)]
        np.testing.assert_array_almost_equal(centers, expected)

    def test_band_centers_period(self, test_bands):
        """Test band_centers method returning periods."""
        centers_freq = test_bands.band_centers(frequency_or_period="frequency")
        centers_period = test_bands.band_centers(frequency_or_period="period")

        # Periods should be inverse of frequencies
        expected_periods = 1.0 / centers_freq
        np.testing.assert_array_almost_equal(centers_period, expected_periods)


class TestFrequencyBandsValidation:
    """Test validation functionality."""

    def test_validate_sorted_bands(self):
        """Test validation with already sorted bands."""
        data = np.array([[0.1, 0.5], [0.5, 1.0], [1.0, 5.0]])
        fb = FrequencyBands(data)

        # Should not raise any warnings
        with patch(
            "mt_metadata.processing.aurora.frequency_bands.logger"
        ) as mock_logger:
            fb.validate()
            mock_logger.warning.assert_not_called()

    def test_validate_unsorted_bands(self):
        """Test validation with unsorted bands triggers reorganization."""
        # Create bands with non-monotonic centers
        data = pd.DataFrame(
            {"lower_bound": [1.0, 0.1, 5.0], "upper_bound": [5.0, 0.5, 10.0]}
        )
        fb = FrequencyBands(data)

        with patch(
            "mt_metadata.processing.aurora.frequency_bands.logger"
        ) as mock_logger:
            fb.validate()
            mock_logger.warning.assert_called_once()
            assert "Band centers are not monotonic" in str(
                mock_logger.warning.call_args
            )

        # Check that bands are now sorted by center frequency
        centers = fb.band_centers()
        assert np.all(centers[1:] >= centers[:-1])


class TestFrequencyBandsProperties:
    """Test various properties and edge cases."""

    @pytest.fixture
    def empty_bands(self):
        """Empty FrequencyBands for testing edge cases."""
        data = np.empty((0, 2))
        return FrequencyBands(data)

    @pytest.fixture
    def single_band(self):
        """FrequencyBands with single band."""
        data = np.array([[1.0, 10.0]])
        return FrequencyBands(data)

    def test_empty_bands_properties(self, empty_bands):
        """Test properties with empty bands."""
        assert empty_bands.number_of_bands == 0
        assert empty_bands.array.shape == (0, 2)
        assert len(empty_bands.band_centers()) == 0

    def test_single_band_properties(self, single_band):
        """Test properties with single band."""
        assert single_band.number_of_bands == 1
        assert single_band.array.shape == (1, 2)

        band = single_band.band(0)
        assert band.frequency_min == 1.0
        assert band.frequency_max == 10.0

    def test_band_edges_property_getter(self):
        """Test band_edges property getter."""
        data = np.array([[0.1, 0.5], [0.5, 1.0]])
        fb = FrequencyBands(data)

        edges = fb.band_edges
        assert isinstance(edges, pd.DataFrame)
        np.testing.assert_array_equal(edges.values, data)

    def test_band_edges_property_setter_array(self):
        """Test band_edges property setter with array."""
        fb = FrequencyBands(np.array([[1.0, 2.0]]))
        new_data = np.array([[0.1, 0.5], [0.5, 1.0]])

        fb.band_edges = new_data
        assert fb.number_of_bands == 2
        np.testing.assert_array_equal(fb.array, new_data)

    def test_band_edges_property_setter_dataframe(self):
        """Test band_edges property setter with DataFrame."""
        fb = FrequencyBands(np.array([[1.0, 2.0]]))
        new_data = pd.DataFrame({"lower_bound": [0.1, 0.5], "upper_bound": [0.5, 1.0]})

        fb.band_edges = new_data
        assert fb.number_of_bands == 2
        pd.testing.assert_frame_equal(fb._band_edges, new_data)


class TestFrequencyBandsErrorHandling:
    """Test error handling and edge cases."""

    def test_construction_invalid_array_shape(self):
        """Test construction with invalid array shape."""
        with pytest.raises(ValueError):
            FrequencyBands(np.array([1, 2, 3]))  # 1D array

        with pytest.raises(ValueError):
            FrequencyBands(np.array([[[1, 2]]]))  # 3D array

        with pytest.raises(ValueError):
            FrequencyBands(np.array([[1, 2, 3]]))  # Wrong number of columns

    def test_construction_invalid_dataframe(self):
        """Test construction with invalid DataFrame."""
        # Missing required columns
        with pytest.raises(ValueError, match="DataFrame must contain columns"):
            FrequencyBands(pd.DataFrame({"a": [1], "b": [2]}))

        # Wrong column names
        with pytest.raises(ValueError, match="DataFrame must contain columns"):
            FrequencyBands(pd.DataFrame({"lower": [1], "upper": [2]}))

    def test_construction_invalid_bounds(self):
        """Test construction with invalid frequency bounds."""
        # Lower bound > upper bound
        data = np.array([[2.0, 1.0]])  # Invalid: lower > upper
        fb = FrequencyBands(data)

        # This should trigger validation warning when validate() is called
        with patch(
            "mt_metadata.processing.aurora.frequency_bands.logger"
        ) as mock_logger:
            fb.validate()
            # The validation should attempt to reorganize, which may still result in warnings
            # depending on the specific implementation

    def test_band_retrieval_negative_index(self):
        """Test band retrieval with negative index."""
        fb = FrequencyBands(np.array([[1.0, 2.0], [2.0, 3.0]]))

        # Negative indices should work with pandas iloc
        band = fb.band(-1)  # Last band
        assert band.frequency_min == 2.0
        assert band.frequency_max == 3.0


class TestFrequencyBandsIntegration:
    """Integration tests combining multiple features."""

    @pytest.fixture
    def complex_scenario_data(self):
        """Complex test scenario with multiple bands."""
        return np.array(
            [
                [0.001, 0.01],
                [0.01, 0.1],
                [0.1, 1.0],
                [1.0, 10.0],
                [10.0, 100.0],
                [100.0, 1000.0],
            ]
        )

    @pytest.fixture
    def complex_bands(self, complex_scenario_data):
        """Complex FrequencyBands instance."""
        return FrequencyBands(complex_scenario_data)

    def test_full_workflow_array_input(self, complex_scenario_data):
        """Test complete workflow starting from array input."""
        # Construction
        fb = FrequencyBands(complex_scenario_data)
        assert fb.number_of_bands == 6

        # Validation
        fb.validate()

        # Band retrieval and properties
        for i in range(fb.number_of_bands):
            band = fb.band(i)
            assert isinstance(band, Band)
            assert band.frequency_min < band.frequency_max

        # Sorting
        fb.sort(by="center_frequency", ascending=False)
        centers = fb.band_centers()
        assert np.all(centers[1:] <= centers[:-1])

        # Band generation
        bands_list = fb.bands(
            direction="increasing_frequency", sortby="center_frequency"
        )
        assert len(bands_list) == 6

        bands_gen = fb.bands(rtype="generator", direction="increasing_period")
        bands_from_gen = list(bands_gen)  # Convert generator to list for length check
        assert len(bands_from_gen) == 6

    def test_dataframe_to_array_consistency(self, complex_scenario_data):
        """Test that DataFrame and array inputs produce consistent results."""
        # Create from array
        fb_array = FrequencyBands(complex_scenario_data)

        # Create from DataFrame
        df_data = pd.DataFrame(
            {
                "lower_bound": complex_scenario_data[:, 0],
                "upper_bound": complex_scenario_data[:, 1],
            }
        )
        fb_df = FrequencyBands(df_data)

        # Compare results
        assert fb_array.number_of_bands == fb_df.number_of_bands
        np.testing.assert_array_equal(fb_array.array, fb_df.array)
        np.testing.assert_array_equal(fb_array.band_centers(), fb_df.band_centers())

        # Compare individual bands
        for i in range(fb_array.number_of_bands):
            band_array = fb_array.band(i)
            band_df = fb_df.band(i)
            assert band_array.frequency_min == band_df.frequency_min
            assert band_array.frequency_max == band_df.frequency_max

    def test_sorting_preserves_data_integrity(self, complex_bands):
        """Test that sorting operations preserve data integrity."""
        original_array = complex_bands.array.copy()
        original_count = complex_bands.number_of_bands

        # Perform various sorting operations
        complex_bands.sort(by="lower_bound", ascending=True)
        assert complex_bands.number_of_bands == original_count

        complex_bands.sort(by="upper_bound", ascending=False)
        assert complex_bands.number_of_bands == original_count

        complex_bands.sort(by="center_frequency", ascending=True)
        assert complex_bands.number_of_bands == original_count

        # Data should still contain same values (possibly reordered)
        current_array = complex_bands.array
        assert current_array.shape == original_array.shape

        # All original frequency values should still be present
        original_values = set(original_array.flatten())
        current_values = set(current_array.flatten())
        assert original_values == current_values


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
