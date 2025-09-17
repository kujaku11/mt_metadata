#!/usr/bin/env python3
"""
Test script to reproduce the phases validation issue
"""
import numpy as np

from mt_metadata.timeseries.filters import FrequencyResponseTableFilter


def create_fap_filter_basic():
    """Create the same filter as in the test fixture"""
    fap = FrequencyResponseTableFilter(
        frequencies=np.array([0.001, 0.01, 0.1, 1.0, 10.0]),
        amplitudes=np.array([1e-3, 1e-2, 1e-1, 1.0, 10.0]),
        phases=np.array([-90, -45, 0, 45, 90]),
        instrument_type="example_instrument",
        units_in="Volt",
        units_out="nanoTesla",
        name="example_fap",
    )
    return fap


def test_phases_validation_direct():
    """Direct test without pytest fixtures"""
    fap_filter = create_fap_filter_basic()

    print("Testing phases validation...")

    # Test 1: Valid phases in degrees (should be converted to radians)
    print("1. Valid phases in degrees:")
    expected_radians = np.deg2rad([-90, -45, 0, 45, 90])
    print(f"   Expected: {expected_radians}")
    print(f"   Actual:   {fap_filter.phases}")
    assert np.allclose(fap_filter.phases, expected_radians)
    print("   ✓ PASS")

    # Test 2: Set phases in degrees (should be converted to radians)
    print("2. Phases in degrees converted to radians:")
    fap_filter.phases = [0, 90, 180]
    expected = np.deg2rad([0, 90, 180])
    print(f"   Expected: {expected}")
    print(f"   Actual:   {fap_filter.phases}")
    assert np.allclose(fap_filter.phases, expected)
    print("   ✓ PASS")

    # Test 3: Set phases in milli-radians (should be converted to radians)
    print("3. Phases in milli-radians converted to radians:")
    fap_filter.phases = [0, 1000 * np.pi / 2, 2000 * np.pi / 2]
    expected = [0, np.pi / 2, np.pi]
    print(f"   Expected: {expected}")
    print(f"   Actual:   {fap_filter.phases}")
    assert np.allclose(fap_filter.phases, expected)
    print("   ✓ PASS")

    # Test 4: Invalid string phases (should raise TypeError)
    print("4. Invalid string phases (should raise TypeError):")
    try:
        fap_filter.phases = "invalid"
        print("   ✗ FAIL: No exception was raised!")
        return False
    except TypeError as e:
        print(f"   ✓ PASS: TypeError raised as expected: {e}")
        return True
    except Exception as e:
        print(f"   ✗ FAIL: Wrong exception type: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    print("Running phases validation test...")
    success = test_phases_validation_direct()
    print(f"\nTest result: {'SUCCESS' if success else 'FAILURE'}")
