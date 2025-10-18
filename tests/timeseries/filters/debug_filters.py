#!/usr/bin/env python3

from mt_metadata.timeseries.channel import Channel


# Test the current behavior
c = Channel()
print("=== Testing Channel filters behavior ===")
print(f"filters value: {c.filters}")
print(f"filters type: {type(c.filters)}")
print(f"filters in required fields: {'filters' in c._required_fields}")

# Test to_dict
result = c.to_dict()
print(f"to_dict() contains 'filters': {'filters' in result}")
if "filters" in result:
    print(f"filters value in to_dict: {result['filters']}")
else:
    print("filters NOT found in to_dict result")

# Test with single=True to get just the channel dict
result_single = c.to_dict(single=True)
print(f"to_dict(single=True) contains 'filters': {'filters' in result_single}")
if "filters" in result_single:
    print(f"filters value in to_dict(single=True): {result_single['filters']}")
else:
    print("filters NOT found in to_dict(single=True) result")

# Test with a filter added
print("\n=== Testing with filters added ===")


c.add_filter(name="test_filter", applied=True, stage=1)
print(f"filters after adding: {c.filters}")

result_with_filter = c.to_dict(single=True)
print(f"to_dict() with filter contains 'filters': {'filters' in result_with_filter}")
if "filters" in result_with_filter:
    print(f"filters value with content: {result_with_filter['filters']}")
