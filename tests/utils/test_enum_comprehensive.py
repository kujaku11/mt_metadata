#!/usr/bin/env python3
"""
Test script to verify comprehensive enum handling in to_dict method
"""
from enum import Enum
from typing import Any, List

from pydantic import Field

from mt_metadata.base.metadata import MetadataBase
from mt_metadata.common.enumerations import DataTypeEnum


# Create a test class that uses enums in various contexts
class TestComplexMetadata(MetadataBase):
    single_enum: DataTypeEnum = Field(
        default=DataTypeEnum.RMT, description="Single enum field"
    )
    enum_list: List[DataTypeEnum] = Field(
        default=[DataTypeEnum.RMT, DataTypeEnum.AMT], description="List of enums"
    )
    mixed_list: List[Any] = Field(
        default=["string", DataTypeEnum.BBMT, 42], description="Mixed list with enum"
    )


# Test comprehensive enum handling
test_obj = TestComplexMetadata()
test_obj.single_enum = DataTypeEnum.LPMT
test_obj.enum_list = [DataTypeEnum.MT, DataTypeEnum.BB, DataTypeEnum.WB]
test_obj.mixed_list = ["test", DataTypeEnum.MT_TF, 100, True]

print("Test object created:")
print(f"single_enum: {test_obj.single_enum} (type: {type(test_obj.single_enum)})")
print(f"enum_list: {test_obj.enum_list}")
print(f"mixed_list: {test_obj.mixed_list}")

# Test to_dict
print("\nto_dict result:")
result_dict = test_obj.to_dict(single=True)

print(
    f"single_enum in dict: {result_dict.get('single_enum')} (type: {type(result_dict.get('single_enum'))})"
)
print(f"enum_list in dict: {result_dict.get('enum_list')}")
print(f"mixed_list in dict: {result_dict.get('mixed_list')}")

# Verify enum values are properly extracted
single_enum_ok = result_dict.get("single_enum") == "LPMT"
enum_list_ok = all(isinstance(item, str) for item in result_dict.get("enum_list", []))
mixed_list_values = result_dict.get("mixed_list", [])
mixed_list_ok = (
    mixed_list_values[0] == "test"
    and mixed_list_values[1] == "MT_TF"  # enum converted to string
    and mixed_list_values[2] == 100
    and mixed_list_values[3] == True
)

print(f"\nEnum handling results:")
print(f"Single enum correct: {single_enum_ok}")
print(f"Enum list correct: {enum_list_ok}")
print(f"Mixed list correct: {mixed_list_ok}")
print(f"All enum handling working: {single_enum_ok and enum_list_ok and mixed_list_ok}")

# Also test with nested dictionaries (manual test since we can't easily create nested dict fields)
test_dict = {"key1": DataTypeEnum.ULPMT, "key2": "normal_string"}
print(f"\nManual dict test:")
print(f"Before processing: {test_dict}")

# Simulate the dict processing logic from to_dict
for key, obj in test_dict.items():
    if isinstance(obj, Enum):
        test_dict[key] = obj.value

print(f"After processing: {test_dict}")
print(f"Dict enum handling correct: {test_dict['key1'] == 'ULPMT'}")
