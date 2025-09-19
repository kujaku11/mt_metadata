#!/usr/bin/env python3
"""
Targeted script to move 'examples=' parameter into existing 'json_schema_extra' dictionaries.
"""

import os
import re


def migrate_examples_to_json_schema_extra(content):
    """
    Move examples= parameter into existing json_schema_extra dictionary.
    """
    changes = 0

    # Pattern to match Field definitions with examples= followed by json_schema_extra
    pattern = r"(\s+Field\(\s*\n.*?)examples\s*=\s*(\[[^\]]*\]|[^,\n]+),\s*\n(.*?)json_schema_extra\s*=\s*\{\s*\n([^}]*)\n(\s*)\}"

    def replace_match(match):
        nonlocal changes
        field_start = match.group(1)
        examples_value = match.group(2)
        middle_part = match.group(3)
        json_content = match.group(4)
        closing_indent = match.group(5)

        # Add examples to json_schema_extra
        new_json_content = (
            json_content.rstrip()
            + ",\n"
            + closing_indent
            + '    "examples": '
            + examples_value
            + ",\n"
            + closing_indent
        )
        new_json_content = new_json_content.replace(
            ",\n" + closing_indent + ",", ","
        )  # Remove duplicate commas

        result = (
            field_start + middle_part + "json_schema_extra={" + new_json_content + "}"
        )
        changes += 1
        return result

    content = re.sub(pattern, replace_match, content, flags=re.DOTALL)
    return content, changes


def process_file(file_path):
    """Process a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content, changes = migrate_examples_to_json_schema_extra(content)

        if changes > 0:
            # Create backup
            with open(file_path + ".backup", "w", encoding="utf-8") as f:
                f.write(content)

            # Write updated content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"✓ Updated {file_path}: {changes} changes")
            return changes
        else:
            print(f"- No changes needed for {file_path}")
            return 0

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return 0


def main():
    # List of common module files to process first
    common_files = [
        "mt_metadata/common/band.py",
        "mt_metadata/common/citation.py",
        "mt_metadata/common/comment.py",
        "mt_metadata/common/copyright.py",
        "mt_metadata/common/data_quality.py",
        "mt_metadata/common/declination.py",
        "mt_metadata/common/fdsn.py",
        "mt_metadata/common/funding_source.py",
        "mt_metadata/common/geographic_location.py",
        "mt_metadata/common/instrument.py",
        "mt_metadata/common/location.py",
        "mt_metadata/common/mttime.py",
        "mt_metadata/common/orientation.py",
        "mt_metadata/common/person.py",
        "mt_metadata/common/provenance.py",
        "mt_metadata/common/rating.py",
        "mt_metadata/common/software.py",
    ]

    total_changes = 0

    for file_path in common_files:
        if os.path.exists(file_path):
            changes = process_file(file_path)
            total_changes += changes
        else:
            print(f"⚠ File not found: {file_path}")

    print(f"\nCompleted: {total_changes} total changes across common/ module")


if __name__ == "__main__":
    main()
