#!/usr/bin/env python3
"""
Test script to verify enum handling in to_dict method
"""

from pydantic import Field

from mt_metadata.base.metadata import MetadataBase
from mt_metadata.common.enumerations import DataTypeEnum


# Create a test class that uses enums
class TestMetadata(MetadataBase):
    data_type: DataTypeEnum = Field(
        default=DataTypeEnum.RMT, description="Test data type enum"
    )
    normal_string: str = Field(default="test_string", description="Normal string field")


# Test the enum handling
test_obj = TestMetadata()
test_obj.data_type = DataTypeEnum.AMT
test_obj.normal_string = "updated_string"

print("Test object created:")
print(f"data_type: {test_obj.data_type} (type: {type(test_obj.data_type)})")
print(f"normal_string: {test_obj.normal_string} (type: {type(test_obj.normal_string)})")

# Test to_dict with and without enum handling
print("\nto_dict result:")
result_dict = test_obj.to_dict(single=True)
print(
    f"data_type in dict: {result_dict.get('data_type')} (type: {type(result_dict.get('data_type'))})"
)
print(
    f"normal_string in dict: {result_dict.get('normal_string')} (type: {type(result_dict.get('normal_string'))})"
)

# Check if the enum value is properly extracted
expected_value = "AMT"
actual_value = result_dict.get("data_type")
print(f"\nExpected data_type value: {expected_value}")
print(f"Actual data_type value: {actual_value}")
print(f"Enum handling working correctly: {actual_value == expected_value}")
