import numpy as np
import pytest
from mt_metadata.features.weights.taper_weight_kernel import TaperWeightKernel

class DummyBaseWeightKernel:
    def __init__(self, **kwargs):
        pass

def test_taper_weight_kernel_basic():
    # Simple test: low_cut and high_cut regions do not overlap
    low_cut = (0.1, 0.3)
    high_cut = (0.7, 0.9)
    kernel = TaperWeightKernel(low_cut, high_cut, style="hann")
    x = np.linspace(0, 1, 100)
    y = kernel.evaluate(x)
    # Should be 1 in the passband (between 0.3 and 0.7), 0 outside transition regions
    assert np.all(y[x < 0.1] == 0)
    assert np.all(y[x > 0.9] == 0)
    assert np.all(y[(x > 0.3) & (x < 0.7)] > 0.9)
    assert np.all(y >= 0)
    assert np.all(y <= 1)

def test_taper_weight_kernel_overlap():
    # Overlapping low_cut and high_cut
    low_cut = (0.2, 0.6)
    high_cut = (0.4, 0.8)
    kernel = TaperWeightKernel(low_cut, high_cut, style="hann")
    x = np.linspace(0, 1, 100)
    y = kernel.evaluate(x)
    # Should be 0 outside [0.2, 0.8]
    assert np.all(y[x < 0.2] == 0)
    assert np.all(y[x > 0.8] == 0)
    assert np.all(y[(x > 0.6) & (x < 0.8)] < 1)
    assert np.all(y[(x > 0.2) & (x < 0.4)] < 1)
    assert np.all(y >= 0)
    assert np.all(y <= 1)

def test_taper_weight_kernel_rectangle():
    # Rectangle style should be 1 in passband, 0 outside
    low_cut = (0.2, 0.4)
    high_cut = (0.6, 0.8)
    kernel = TaperWeightKernel(low_cut, high_cut, style="rectangle")
    x = np.linspace(0, 1, 100)
    y = kernel.evaluate(x)
    assert np.all(y[x < 0.2] == 0)
    assert np.all(y[x > 0.8] == 0)
    assert np.all(y[(x >= 0.4) & (x <= 0.6)] == 1)
    assert np.all(y >= 0)
    assert np.all(y <= 1)

def test_taper_weight_kernel_typehints():
    # Check type hints and docstring presence
    assert TaperWeightKernel.__init__.__annotations__["low_cut"] == tuple[float, float]
    assert TaperWeightKernel.__init__.__annotations__["high_cut"] == tuple[float, float]
    assert TaperWeightKernel.__init__.__annotations__["style"] == str
    assert TaperWeightKernel.evaluate.__annotations__["values"] == np.ndarray
    assert TaperWeightKernel.evaluate.__annotations__["return"] == np.ndarray
    assert TaperWeightKernel.__doc__ is not None
    assert TaperWeightKernel.evaluate.__doc__ is not None
