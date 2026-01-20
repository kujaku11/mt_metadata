#!/usr/bin/env python3
"""
Test script to demonstrate enum handling in to_dict method
"""

from enum import Enum

from mt_metadata.common.enumerations import DataTypeEnum

# Create a simple test to demonstrate the enum issue
test_enum = DataTypeEnum.RMT
print(f"Original enum: {test_enum}")
print(f"Type: {type(test_enum)}")
print(f"Is Enum: {isinstance(test_enum, Enum)}")
print(f"Value: {test_enum.value}")
print(f"String conversion: {str(test_enum)}")

# Test if an enum should return its value instead of the enum object
if isinstance(test_enum, Enum):
    print(f"Should return: {test_enum.value}")
else:
    print(f"Would return as-is: {test_enum}")
