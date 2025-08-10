#!/usr/bin/env python3
"""
Debug script to test BirrpBlock list conversion handling.
"""

from mt_metadata.transfer_functions.io.jfiles.metadata.birrp_block import BirrpBlock


def test_conversion():
    """Test how BirrpBlock handles different value assignments."""
    block = BirrpBlock()

    print("Testing ncomp assignments:")

    # Test list assignment (should work)
    try:
        block.ncomp = [1, 2, 3]
        print(f"✓ List [1, 2, 3]: {block.ncomp}")
    except Exception as e:
        print(f"✗ List [1, 2, 3]: {e}")

    # Test single value assignment (should fail)
    try:
        block.ncomp = 4
        print(f"✓ Single 4: {block.ncomp}")
    except Exception as e:
        print(f"✗ Single 4: {e}")

    # Test string list assignment
    try:
        block.ncomp = ["1", "2"]
        print(f"✓ String list ['1', '2']: {block.ncomp}")
    except Exception as e:
        print(f"✗ String list ['1', '2']: {e}")

    print("\nTesting indices assignments:")

    # Test list assignment (should work)
    try:
        block.indices = [1, 2, 3, 4]
        print(f"✓ List [1, 2, 3, 4]: {block.indices}")
    except Exception as e:
        print(f"✗ List [1, 2, 3, 4]: {e}")

    # Test single value assignment (should fail)
    try:
        block.indices = 5
        print(f"✓ Single 5: {block.indices}")
    except Exception as e:
        print(f"✗ Single 5: {e}")


if __name__ == "__main__":
    test_conversion()
