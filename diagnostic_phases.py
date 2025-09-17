#!/usr/bin/env python3
"""
Comprehensive diagnostic for the phases validation issue
"""
import sys
import traceback

import numpy as np
from pydantic import ValidationError

from mt_metadata.base.helpers import object_to_array
from mt_metadata.timeseries.filters import FrequencyResponseTableFilter


def test_object_to_array_directly():
    """Test object_to_array function directly with various inputs"""
    print("=== Testing object_to_array function directly ===")

    test_cases = [
        "invalid",
        "",
        "1,2,3",
        "not_a_number",
        "123.45",
        ["1", "2", "3"],
        [1, 2, 3],
        np.array([1, 2, 3]),
        123,
        123.45,
        None,
        {"invalid": "dict"},
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {repr(test_case)} (type: {type(test_case).__name__})")
        try:
            result = object_to_array(test_case)
            print(f"  SUCCESS: {result} (shape: {result.shape}, dtype: {result.dtype})")
        except Exception as e:
            print(f"  EXCEPTION: {type(e).__name__}: {e}")


def test_pydantic_validation():
    """Test Pydantic validation directly"""
    print("\n=== Testing Pydantic validation directly ===")

    # Test the validator function directly
    from mt_metadata.timeseries.filters.frequency_response_table_filter import (
        FrequencyResponseTableFilter,
    )

    print("Testing validate_phases class method directly...")
    try:
        result = FrequencyResponseTableFilter.validate_phases("invalid", None)
        print(f"  UNEXPECTED: validate_phases returned: {result}")
    except Exception as e:
        print(f"  EXPECTED: validate_phases raised: {type(e).__name__}: {e}")


def test_filter_creation_and_assignment():
    """Test the complete filter creation and assignment process"""
    print("\n=== Testing complete filter creation and assignment ===")

    # Create filter
    print("Creating FrequencyResponseTableFilter...")
    try:
        fap = FrequencyResponseTableFilter()
        print("  Filter created successfully with defaults")

        # Try setting valid phases first
        print("Setting valid phases...")
        fap.phases = [-90, -45, 0, 45, 90]
        print(f"  Valid phases set: {fap.phases}")

        # Now try setting invalid phases
        print("Setting invalid phases...")
        try:
            fap.phases = "invalid"
            print("  PROBLEM: Invalid phases assignment succeeded!")
            print(f"  Current phases value: {fap.phases}")
            print(f"  Current phases type: {type(fap.phases)}")
            return False
        except TypeError as e:
            print(f"  EXPECTED: TypeError raised: {e}")
            return True
        except ValidationError as e:
            print(f"  EXPECTED: ValidationError raised: {e}")
            return True
        except Exception as e:
            print(f"  UNEXPECTED: Other exception raised: {type(e).__name__}: {e}")
            return False

    except Exception as e:
        print(f"  ERROR: Failed to create filter: {type(e).__name__}: {e}")
        traceback.print_exc()
        return False


def check_numpy_behavior():
    """Check numpy version and behavior"""
    print(f"\n=== NumPy Information ===")
    print(f"NumPy version: {np.__version__}")

    # Test np.fromstring behavior
    print("\nTesting np.fromstring behavior:")
    test_strings = ["invalid", "", "1,2,3", "not_a_number"]

    for test_str in test_strings:
        print(f"  np.fromstring({repr(test_str)}, sep=',', dtype=float):")
        try:
            result = np.fromstring(test_str, sep=",", dtype=float)
            print(f"    SUCCESS: {result} (len: {len(result)})")
        except Exception as e:
            print(f"    EXCEPTION: {type(e).__name__}: {e}")


def main():
    """Run all diagnostic tests"""
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")

    check_numpy_behavior()
    test_object_to_array_directly()
    test_pydantic_validation()

    print("\n" + "=" * 60)
    print("FINAL TEST: Complete workflow")
    success = test_filter_creation_and_assignment()

    print(f"\nFinal result: {'SUCCESS' if success else 'FAILURE'}")
    return success


if __name__ == "__main__":
    main()
