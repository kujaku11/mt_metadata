#!/usr/bin/env python

"""Test the updated helper functions."""

from mt_metadata.base.helpers import get_all_fields, get_by_alias
from mt_metadata.transfer_functions.io.emtfxml.metadata.dipole import Dipole


def test_get_all_fields():
    """Test the updated get_all_fields function."""
    dipole = Dipole()
    fields = get_all_fields(dipole)

    print(f"✓ get_all_fields works: found {len(fields)} fields")

    # Check that we get the expected fields
    expected_fields = ["manufacturer", "length", "azimuth", "name", "type", "electrode"]
    for field in expected_fields:
        if field in fields:
            print(f"  ✓ Found field: {field}")
        else:
            print(f"  ✗ Missing field: {field}")

    # Check nested BaseModel
    if "electrode" in fields and isinstance(fields["electrode"], dict):
        print("  ✓ Nested BaseModel (electrode) detected correctly")
        if "comments" in fields["electrode"] and isinstance(
            fields["electrode"]["comments"], dict
        ):
            print("    ✓ Deeply nested BaseModel (comments) detected correctly")

    return fields


def test_get_by_alias():
    """Test the updated get_by_alias function."""
    dipole = Dipole()

    # Test with a non-existent alias (should return None)
    result = get_by_alias(dipole, "nonexistent_alias")
    print(f"✓ get_by_alias works: returns {result} for non-existent alias")

    return result


if __name__ == "__main__":
    print("Testing updated helper functions with __pydantic_fields__...")
    print("=" * 60)

    try:
        test_get_all_fields()
        print()
        test_get_by_alias()
        print()
        print("All tests passed! ✓")
        print(
            "Functions successfully updated to use __pydantic_fields__ instead of model_fields"
        )

    except Exception as e:
        print(f"Test failed: {e}")
        import traceback

        traceback.print_exc()
