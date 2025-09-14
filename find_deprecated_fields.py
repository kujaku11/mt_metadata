#!/usr/bin/env python3
"""
Script to identify Pydantic Field definitions that still use deprecated parameters
and need to be migrated to json_schema_extra format.
"""

import os
import re


def find_deprecated_field_usage(directory_path):
    """
    Find all Python files with deprecated Pydantic Field usage.

    Returns:
        dict: Dictionary mapping file paths to line numbers with deprecated usage
    """
    deprecated_files = {}

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    lines = content.split("\n")
                    deprecated_lines = []
                    in_field_definition = False
                    field_start_line = None

                    for i, line in enumerate(lines, 1):
                        # Check if we're starting a Field definition
                        if "Field(" in line:
                            in_field_definition = True
                            field_start_line = i

                        # If we're in a Field definition, look for deprecated parameters
                        if in_field_definition:
                            if (
                                re.search(r"\bexamples\s*=", line)
                                or re.search(r"\btype\s*=", line)
                                or re.search(r"\bitems\s*=", line)
                            ):
                                if field_start_line not in deprecated_lines:
                                    deprecated_lines.append(field_start_line)

                        # Check if Field definition is closed
                        if in_field_definition and ")," in line:
                            in_field_definition = False
                            field_start_line = None

                    if deprecated_lines:
                        relative_path = os.path.relpath(file_path, directory_path)
                        deprecated_files[relative_path] = deprecated_lines

                except (UnicodeDecodeError, FileNotFoundError):
                    continue

    return deprecated_files


def count_files_by_module(deprecated_files):
    """Group files by their module directory."""
    modules = {}

    for file_path in deprecated_files.keys():
        parts = file_path.split(os.sep)
        if len(parts) > 1:
            module = parts[0]
        else:
            module = "root"

        if module not in modules:
            modules[module] = []
        modules[module].append(file_path)

    return modules


if __name__ == "__main__":
    # Run from the mt_metadata directory
    base_path = "mt_metadata"

    print("Scanning for deprecated Pydantic Field usage...")
    deprecated_files = find_deprecated_field_usage(base_path)

    if deprecated_files:
        print(f"\nFound {len(deprecated_files)} files with deprecated Field usage:")

        # Group by module
        modules = count_files_by_module(deprecated_files)

        for module, files in sorted(modules.items()):
            print(f"\n{module}/ ({len(files)} files):")
            for file_path in sorted(files):
                lines = deprecated_files[file_path]
                print(f"  {file_path} (lines: {', '.join(map(str, lines))})")

        print(f"\nTotal files needing migration: {len(deprecated_files)}")

        # Priority order for migration
        priority_modules = [
            "common",
            "timeseries",
            "transfer_functions",
            "processing",
            "features",
        ]

        print("\nRecommended migration order:")
        for i, module in enumerate(priority_modules, 1):
            if module in modules:
                count = len(modules[module])
                print(f"{i}. {module}/ - {count} files")

        # List any other modules
        other_modules = [
            m for m in modules.keys() if m not in priority_modules and m != "root"
        ]
        if other_modules:
            print(
                f"{len(priority_modules)+1}. Other modules: {', '.join(other_modules)}"
            )

    else:
        print("No files found with deprecated Field usage!")
