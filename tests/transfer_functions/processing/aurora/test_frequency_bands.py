# -*- coding: utf-8 -*-
"""
Tests for FrequencyBands class.
"""

# Standard library imports
from types import GeneratorType

# Third-party imports
from loguru import logger
import numpy as np
import pandas as pd
import pytest

# Local imports
from mt_metadata.transfer_functions.processing.aurora import Band
from mt_metadata.transfer_functions.processing.aurora.frequency_bands import FrequencyBands


@pytest.fixture
def basic_band_edges():
    """Original test data from unittest version"""
    return np.vstack(([1, 10], [11, 20]))


@pytest.fixture
def sample_band_edges():
    """Sample band edges for new tests"""
    return np.array([
        [0.1, 0.2],
        [0.2, 0.3],
        [0.3, 0.4]
    ])


@pytest.fixture(autouse=True)
def setup_loguru(caplog):
    """Configure loguru to work with pytest's caplog"""
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level="WARNING",
        filter=lambda record: record["level"].name == "WARNING"
    )
    yield
    logger.remove(handler_id)


class TestFrequencyBands:
    """Test suite for FrequencyBands class"""

    def test_init_empty(self):
        """Test initialization with no arguments"""
        fb = FrequencyBands()
        assert fb.number_of_bands == 0
        assert isinstance(fb.band_edges, pd.DataFrame)
        assert list(fb.band_edges.columns) == ['lower_bound', 'upper_bound']

    def test_basic_functionality(self, basic_band_edges):
        """Test core functionality using original test data"""
        fb = FrequencyBands(basic_band_edges)
        
        # Test number of bands
        assert fb.number_of_bands == basic_band_edges.shape[0]
        
        # Test validate method
        assert fb.validate() is None
        
        # Test bands default return type (list)
        bands = fb.bands()
        assert isinstance(bands, list)
        assert len(bands) == basic_band_edges.shape[0]
        
        # Test bands generator return type
        bands_gen = fb.bands(rtype="generator")
        assert isinstance(bands_gen, GeneratorType)
        
        # Test single band access
        b = fb.band(0)
        other = Band(frequency_min=1, frequency_max=10)
        assert b == other
        
        # Test band centers
        expected_centers = np.array([3.16227766, 14.83239697])
        assert np.allclose(fb.band_centers(), expected_centers)

    def test_init_with_numpy(self, sample_band_edges):
        """Test initialization with numpy array"""
        fb = FrequencyBands(sample_band_edges)
        assert isinstance(fb.band_edges, pd.DataFrame)
        assert fb.number_of_bands == 3
        assert np.array_equal(fb.array, sample_band_edges)

    def test_init_with_dataframe(self):
        """Test initialization with DataFrame"""
        df = pd.DataFrame({
            'lower_bound': [0.1, 0.2, 0.3],
            'upper_bound': [0.2, 0.3, 0.4]
        })
        fb = FrequencyBands(df)
        assert fb.number_of_bands == 3
        assert np.array_equal(fb.array, df.values)

    def test_invalid_inputs(self):
        """Test error handling for invalid inputs"""
        # Wrong shape numpy array
        with pytest.raises(ValueError, match="must be 2D with shape"):
            FrequencyBands(np.array([1, 2, 3]))
        
        # DataFrame missing required columns
        with pytest.raises(ValueError, match="must contain columns"):
            FrequencyBands(pd.DataFrame({'wrong_col': [1, 2, 3]}))

        # Invalid type
        with pytest.raises(TypeError, match="must be numpy array or DataFrame"):
            FrequencyBands([1, 2, 3])

    def test_bands_generator(self, sample_band_edges):
        """Test band generator functionality"""
        fb = FrequencyBands(sample_band_edges)
        
        # Test increasing frequency
        bands = list(fb.bands("increasing_frequency"))
        assert len(bands) == 3
        assert bands[0].frequency_min == 0.1
        assert bands[-1].frequency_max == 0.4
        
        # Test increasing period
        bands = list(fb.bands("increasing_period"))
        assert len(bands) == 3
        assert bands[0].frequency_max == 0.4
        assert bands[-1].frequency_min == 0.1

    def test_validation_reordering(self, caplog):
        """Test validation and reordering of bands"""
        edges = np.array([
            [0.3, 0.4],
            [0.1, 0.2],
            [0.2, 0.3]
        ])
        fb = FrequencyBands(edges)
        
        # Check if warning is logged
        fb.validate()
        assert "Band centers are not monotonic" in caplog.text
        
        # Check if bands were reordered
        assert fb.band(0).frequency_min == 0.1
        assert fb.band(1).frequency_min == 0.2
        assert fb.band(2).frequency_min == 0.3

    def test_bands_return_types(self, sample_band_edges):
        """Test different return types from bands method"""
        fb = FrequencyBands(sample_band_edges)
        
        # Test default return type (list)
        default_bands = fb.bands()
        assert isinstance(default_bands, list)
        assert len(default_bands) == 3
        assert all(isinstance(b, Band) for b in default_bands)
        
        # Test explicit list return type
        list_bands = fb.bands(rtype="list")
        assert isinstance(list_bands, list)
        assert len(list_bands) == 3
        assert all(isinstance(b, Band) for b in list_bands)
        
        # Test generator return type
        gen_bands = fb.bands(rtype="generator")
        assert isinstance(gen_bands, GeneratorType)
        
        # Convert generator to list to check contents
        gen_bands_list = list(gen_bands)
        assert len(gen_bands_list) == 3
        assert all(isinstance(b, Band) for b in gen_bands_list)
        
        # Test that list and generator versions give same results
        for list_band, gen_band in zip(list_bands, gen_bands_list):
            assert list_band.frequency_min == gen_band.frequency_min
            assert list_band.frequency_max == gen_band.frequency_max
        
        # Test invalid rtype
        with pytest.raises(ValueError, match="rtype must be either 'list' or 'generator'"):
            fb.bands(rtype="invalid")

    def test_bands_sorting_with_return_types(self, sample_band_edges):
        """Test sorting works correctly with different return types"""
        # Create bands in reverse order
        reversed_edges = sample_band_edges[::-1]
        fb = FrequencyBands(reversed_edges)
        
        # Test list return type with sorting
        list_bands = fb.bands(sortby="lower_bound", rtype="list")
        assert isinstance(list_bands, list)
        assert list_bands[0].frequency_min == 0.1
        assert list_bands[-1].frequency_min == 0.3
        
        # Test generator return type with sorting
        gen_bands = fb.bands(sortby="lower_bound", rtype="generator")
        assert isinstance(gen_bands, GeneratorType)
        gen_bands_list = list(gen_bands)
        assert gen_bands_list[0].frequency_min == 0.1
        assert gen_bands_list[-1].frequency_min == 0.3
        
        # Test that both return types give same sorted results
        for list_band, gen_band in zip(list_bands, gen_bands_list):
            assert list_band.frequency_min == gen_band.frequency_min
            assert list_band.frequency_max == gen_band.frequency_max
