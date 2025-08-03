#!/usr/bin/env python3

import os
import re


# List of files that need updates based on the search results
files_to_update = [
    "mt_metadata/transfer_functions/io/edi/metadata/header.py",
    "tests/utils/test_units.py",
    "mt_metadata/transfer_functions/tf/transfer_function_basemodel.py",
    "mt_metadata/transfer_functions/tf/statistical_estimate_basemodel.py",
    "mt_metadata/transfer_functions/io/edi/metadata/define_measurement.py",
    "mt_metadata/transfer_functions/io/emtfxml/metadata/channels.py",
    "mt_metadata/transfer_functions/io/emtfxml/metadata/data_type.py",
    "mt_metadata/utils/converters.py",
    "mt_metadata/timeseries/stationxml/xml_channel_mt_channel.py",
    "tests/timeseries/stationxml/test_fap.py",
    "tests/timeseries/stationxml/test_channel.py",
    "mt_metadata/timeseries/filters/channel_response.py",
    "mt_metadata/timeseries/filters/helper_functions.py",
    "tests/transfer_functions/tf/test_statistical_estimates.py",
    "mt_metadata/timeseries/filters/filter_base.py",
    "mt_metadata/processing/fourier_coefficients/fc_channel_basemodel.py",
    "mt_metadata/timeseries/channel.py",
    "mt_metadata/features/feature_decimation_channel_basemodel.py",
    "examples/notebooks/pydantic_examples.ipynb",
]

# Define the replacement patterns
replacement_patterns = [
    # Pattern 1: from mt_metadata.utils.units import ...
    (r"from mt_metadata\.utils\.units import", "from mt_metadata.common.units import"),
    # Pattern 2: from mt_metadata.utils import units
    (r"from mt_metadata\.utils import units", "from mt_metadata.common import units"),
    # Pattern 3: import mt_metadata.utils.units
    (r"import mt_metadata\.utils\.units", "import mt_metadata.common.units"),
]


def update_imports_in_file(file_path):
    """Update imports in a single file."""
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        updated = False

        # Apply all replacement patterns
        for pattern, replacement in replacement_patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                updated = True

        # Write back if changes were made
        if updated:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ Updated: {file_path}")
            return True
        else:
            print(f"- No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False


def main():
    """Main function to update all files."""
    print("Updating units imports from utils to common...")
    print("=" * 50)

    updated_files = []
    error_count = 0

    for file_path in files_to_update:
        if update_imports_in_file(file_path):
            updated_files.append(file_path)

    print("=" * 50)
    print("Summary:")
    print(f"Updated files: {len(updated_files)}")
    print(f"Errors: {error_count}")

    if updated_files:
        print("Updated files:")
        for file_path in updated_files:
            print(f"  {file_path}")


if __name__ == "__main__":
    main()
