#!/usr/bin/env python3
"""
Final demonstration of enum handling in to_dict method
"""
from typing import Any, List

from pydantic import Field

from mt_metadata.base.metadata import MetadataBase
from mt_metadata.common.enumerations import DataTypeEnum


# Test class demonstrating comprehensive enum handling
class ComprehensiveEnumTest(MetadataBase):
    """Test class for demonstrating enum handling in various contexts"""

    single_enum: DataTypeEnum = Field(
        default=DataTypeEnum.RMT, description="Single enum field"
    )
    enum_list: List[DataTypeEnum] = Field(
        default=[DataTypeEnum.RMT, DataTypeEnum.AMT], description="List of enums"
    )
    mixed_list: List[Any] = Field(
        default=["string", DataTypeEnum.BBMT, 42, True],
        description="Mixed list with enum",
    )
    regular_field: str = Field(
        default="test_string", description="Regular string field for comparison"
    )


def test_enum_handling():
    """Test comprehensive enum handling in to_dict"""
    print("Testing enum handling in to_dict method...")

    # Create test object
    test_obj = ComprehensiveEnumTest()
    test_obj.single_enum = DataTypeEnum.LPMT_TF
    test_obj.enum_list = [DataTypeEnum.MT, DataTypeEnum.BB, DataTypeEnum.WB]
    test_obj.mixed_list = ["test", DataTypeEnum.MT_TF, 100, False]
    test_obj.regular_field = "updated_string"

    print(f"\nBefore to_dict:")
    print(f"single_enum: {test_obj.single_enum} (type: {type(test_obj.single_enum)})")
    print(f"enum_list: {test_obj.enum_list}")
    print(f"mixed_list: {test_obj.mixed_list}")
    print(f"regular_field: {test_obj.regular_field}")

    # Convert to dict
    result_dict = test_obj.to_dict(single=True)

    print(f"\nAfter to_dict:")
    print(
        f"single_enum: {result_dict.get('single_enum')} (type: {type(result_dict.get('single_enum'))})"
    )
    print(f"enum_list: {result_dict.get('enum_list')}")
    print(f"mixed_list: {result_dict.get('mixed_list')}")
    print(f"regular_field: {result_dict.get('regular_field')}")

    # Verify enum handling
    tests = {
        "Single enum converted": result_dict.get("single_enum") == "LPMT_TF",
        "Enum list converted": result_dict.get("enum_list") == ["MT", "BB", "WB"],
        "Mixed list enum converted": result_dict.get("mixed_list")[1] == "MT_TF",
        "Mixed list non-enum preserved": (
            result_dict.get("mixed_list")[0] == "test"
            and result_dict.get("mixed_list")[2] == 100
            and result_dict.get("mixed_list")[3] == False
        ),
        "Regular field unchanged": result_dict.get("regular_field") == "updated_string",
    }

    print(f"\nTest Results:")
    all_passed = True
    for test_name, passed in tests.items():
        status = "✓" if passed else "✗"
        print(f"{status} {test_name}: {passed}")
        if not passed:
            all_passed = False

    print(
        f"\nOverall Result: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}"
    )
    return all_passed


if __name__ == "__main__":
    test_enum_handling()
