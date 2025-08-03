#!/usr/bin/env python3
"""
Script to update all ListDict imports from utils.list_dict to common.list_dict
"""
import os
import re


# Files to update
files_to_update = [
    "tests/utils/test_list_dict.py",
    "mt_metadata/processing/fourier_coefficients/decimation.py",
    "mt_metadata/processing/fourier_coefficients/fc.py",
    "mt_metadata/timeseries/run.py",
    "mt_metadata/transfer_functions/tf/survey.py",
    "mt_metadata/transfer_functions/tf/station.py",
    "mt_metadata/timeseries/survey.py",
    "mt_metadata/timeseries/station.py",
    "mt_metadata/timeseries/experiment.py",
    "mt_metadata/transfer_functions/core.py",
    "mt_metadata/transfer_functions/io/zfiles/zmm.py",
]

# Replacement mappings
replacements = [
    (
        r"from mt_metadata\.utils\.list_dict import ListDict",
        "from mt_metadata.common.list_dict import ListDict",
    ),
]

base_path = r"c:\Users\peaco\OneDrive\Documents\GitHub\mt_metadata"

updated_files = []
errors = []

for file_path in files_to_update:
    full_path = os.path.join(base_path, file_path)
    if not os.path.exists(full_path):
        errors.append(f"File not found: {full_path}")
        continue

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        # Only write if changes were made
        if content != original_content:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            updated_files.append(file_path)
            print(f"✓ Updated: {file_path}")
        else:
            print(f"- No changes needed: {file_path}")

    except Exception as e:
        errors.append(f"Error processing {file_path}: {str(e)}")

print(f"\nSummary:")
print(f"Updated files: {len(updated_files)}")
print(f"Errors: {len(errors)}")

if errors:
    print("\nErrors:")
    for error in errors:
        print(f"  {error}")

if updated_files:
    print(f"\nUpdated files:")
    for file in updated_files:
        print(f"  {file}")
