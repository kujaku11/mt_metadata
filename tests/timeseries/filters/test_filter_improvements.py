#!/usr/bin/env python3

from mt_metadata.timeseries.electric import Electric

# Test edge cases and comprehensive scenarios
print("=== Test: Comprehensive scenarios ===")

# Test with mixed old format keys to ensure f-string works correctly
electric = Electric(component="ex")

# Test the method with various combinations
test_cases = [
    # Should find 'filter' as base key
    {"filter.applied": [True], "filter.name": ["test_filter"]},
    # Should find 'filtered' as base key
    {"filtered.applied": [True], "filtered.name": ["old_filter"]},
    # Should find nothing
    {"some_other_key": "value"},
    # Multiple keys with different bases - should find 'filter' first
    {"filter": "legacy", "filtered.applied": [True]},
    # Complex keys
    {"filter.stage.1": "value", "filter.complex.nested": "other"},
    {"filtered.complex.nested.key": "value"},
]

for i, test_dict in enumerate(test_cases, 1):
    result = electric._find_filter_keys(test_dict)
    print(f'Test {i}: {list(test_dict.keys())} -> "{result}"')

    # If we have a filter format, test the f-string construction
    if result:
        if result == "filtered":
            applied_key = f"{result}.applied"
            name_key = f"{result}.name"
            print(f'  Would look for: "{applied_key}" and "{name_key}"')
        elif result == "filter":
            filter_key = f"{result}"
            print(f'  Would look for: "{filter_key}"')
    print()

print("=== Test: Actual from_dict behavior with f-strings ===")

# Test actual from_dict behavior to ensure f-strings work
test_filtered = {
    "component": "ex",
    "filtered.applied": [True, False],
    "filtered.name": ["lowpass", "highpass"],
}

electric_test = Electric(component="ex")
electric_test.from_dict(test_filtered)
print(
    f"Filtered format conversion successful: {len(electric_test.filters)} filters created"
)
for f in electric_test.filters:
    print(f"  Filter: {f.name}, Applied: {f.applied}")
