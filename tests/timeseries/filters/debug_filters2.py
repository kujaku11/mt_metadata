#!/usr/bin/env python3

from mt_metadata.timeseries.channel import Channel


# Test different to_dict parameter combinations
c = Channel()
print("=== Testing different to_dict parameters ===")

# Test default parameters
print("1. to_dict() - default parameters:")
result1 = c.to_dict()
print(f"   Result type: {type(result1)}")
print(f"   Top level keys: {list(result1.keys())}")
if "channel" in result1:
    print(f"   'filters' in channel dict: {'filters' in result1['channel']}")

# Test nested=False explicitly
print("\n2. to_dict(nested=False):")
result2 = c.to_dict(nested=False)
print(f"   Result type: {type(result2)}")
print(f"   Top level keys: {list(result2.keys())}")
if "channel" in result2:
    print(f"   'filters' in channel dict: {'filters' in result2['channel']}")

# Test nested=True explicitly
print("\n3. to_dict(nested=True):")
result3 = c.to_dict(nested=True)
print(f"   Result type: {type(result3)}")
print(f"   Top level keys: {list(result3.keys())}")
if "channel" in result3:
    print(f"   'filters' in channel dict: {'filters' in result3['channel']}")

# Test single=True
print("\n4. to_dict(single=True):")
result4 = c.to_dict(single=True)
print(f"   Result type: {type(result4)}")
print(f"   'filters' in result: {'filters' in result4}")
