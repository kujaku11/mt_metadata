#!/usr/bin/env python3
"""
Robust Pydantic Field Converter

This script uses regex replacement to carefully migrate Field definitions
while preserving exact formatting and handling edge cases.
"""

import argparse
import os
import re
import shutil
from typing import Tuple


def migrate_examples_parameter(content: str) -> Tuple[str, int]:
    """
    Migrate examples= parameter to json_schema_extra using careful regex replacement.

    This function looks for patterns where examples= appears before json_schema_extra=
    and moves the examples into the existing json_schema_extra dictionary.
    """
    changes = 0

    # Pattern to match Field with examples= parameter followed by json_schema_extra
    # This pattern captures the entire Field definition structure
    pattern = re.compile(
        r"(Field\s*\(\s*\n"  # Field opening
        r"(?:[^)]*\n)*?"  # Any parameters before examples
        r".*?)"  # Capture everything up to examples
        r"examples\s*=\s*"  # The examples parameter
        r'(\[[^\]]*\]|["\'][^"\']*["\']|[^,\n]+)'  # Capture examples value (list, quoted string, or simple value)
        r"(,?\s*\n)"  # Capture comma and whitespace after examples
        r"((?:[^)]*\n)*?"  # Any parameters between examples and json_schema_extra
        r".*?json_schema_extra\s*=\s*\{\s*\n)"  # Everything up to json_schema_extra opening
        r"([^}]*)"  # Content inside json_schema_extra
        r"(\n\s*\})"  # Closing brace of json_schema_extra
        r"([^)]*\),)",  # Rest of Field definition
        re.DOTALL,
    )

    def replace_field(match):
        nonlocal changes

        field_prefix = match.group(1)
        examples_value = match.group(2).strip().rstrip(",")
        examples_suffix = match.group(3)
        middle_part = match.group(4)
        json_content = match.group(5)
        json_closing = match.group(6)
        field_suffix = match.group(7)

        # Clean up the middle part (remove trailing comma if present)
        middle_part = middle_part.rstrip()
        if middle_part.endswith(","):
            middle_part = middle_part[:-1]
        if middle_part:
            middle_part += ",\n"

        # Add examples to json_schema_extra
        # Determine indentation from the json_closing
        indent_match = re.search(r"(\s*)\}", json_closing)
        if indent_match:
            base_indent = indent_match.group(1)
            examples_indent = base_indent + "    "
        else:
            examples_indent = "                "

        # Add comma to existing json content if it doesn't end with one
        if json_content.strip() and not json_content.rstrip().endswith(","):
            json_content = json_content.rstrip() + ","

        new_json_content = (
            json_content + f'\n{examples_indent}"examples": {examples_value},'
        )

        result = (
            field_prefix
            + middle_part
            + "json_schema_extra={"
            + new_json_content
            + json_closing
            + field_suffix
        )

        changes += 1
        return result

    content = pattern.sub(replace_field, content)
    return content, changes


def migrate_type_parameter(content: str) -> Tuple[str, int]:
    """
    Migrate type= parameter to json_schema_extra.
    """
    changes = 0

    # Similar pattern for type parameter
    pattern = re.compile(
        r"(Field\s*\([^)]*?)"  # Field opening and parameters before type
        r"type\s*=\s*"  # The type parameter
        r"([^,\n]+)"  # Capture type value
        r"(,?\s*[^)]*json_schema_extra\s*=\s*\{\s*\n)"  # Everything up to json_schema_extra
        r"([^}]*)"  # Content inside json_schema_extra
        r"(\n\s*\}[^)]*\),)",  # Rest of Field definition
        re.DOTALL,
    )

    def replace_field(match):
        nonlocal changes

        field_prefix = match.group(1)
        type_value = match.group(2).strip().rstrip(",")
        middle_part = match.group(3)
        json_content = match.group(4)
        field_suffix = match.group(5)

        # Add type to json_schema_extra
        if json_content.strip() and not json_content.rstrip().endswith(","):
            json_content = json_content.rstrip() + ","

        new_json_content = json_content + f'\n                "type": {type_value},'

        result = field_prefix + middle_part + new_json_content + field_suffix

        changes += 1
        return result

    content = pattern.sub(replace_field, content)
    return content, changes


def migrate_items_parameter(content: str) -> Tuple[str, int]:
    """
    Migrate items= parameter to json_schema_extra.
    """
    changes = 0

    # Similar pattern for items parameter
    pattern = re.compile(
        r"(Field\s*\([^)]*?)"  # Field opening and parameters before items
        r"items\s*=\s*"  # The items parameter
        r"([^,\n]+)"  # Capture items value
        r"(,?\s*[^)]*json_schema_extra\s*=\s*\{\s*\n)"  # Everything up to json_schema_extra
        r"([^}]*)"  # Content inside json_schema_extra
        r"(\n\s*\}[^)]*\),)",  # Rest of Field definition
        re.DOTALL,
    )

    def replace_field(match):
        nonlocal changes

        field_prefix = match.group(1)
        items_value = match.group(2).strip().rstrip(",")
        middle_part = match.group(3)
        json_content = match.group(4)
        field_suffix = match.group(5)

        # Add items to json_schema_extra
        if json_content.strip() and not json_content.rstrip().endswith(","):
            json_content = json_content.rstrip() + ","

        new_json_content = json_content + f'\n                "items": {items_value},'

        result = field_prefix + middle_part + new_json_content + field_suffix

        changes += 1
        return result

    content = pattern.sub(replace_field, content)
    return content, changes


def migrate_file_content(content: str) -> Tuple[str, int]:
    """
    Migrate all deprecated Field parameters in the content.
    """
    total_changes = 0

    # Migrate each parameter type
    content, changes1 = migrate_examples_parameter(content)
    total_changes += changes1

    content, changes2 = migrate_type_parameter(content)
    total_changes += changes2

    content, changes3 = migrate_items_parameter(content)
    total_changes += changes3

    return content, total_changes


def migrate_file(file_path: str, dry_run: bool = False, verbose: bool = False) -> int:
    """
    Migrate a single Python file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        migrated_content, changes = migrate_file_content(original_content)

        if changes > 0:
            if not dry_run:
                # Create backup
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)

                # Write migrated content
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(migrated_content)

                print(f"✓ Migrated {file_path}: {changes} Field definitions updated")
                if verbose:
                    print(f"  Backup created: {backup_path}")
            else:
                print(
                    f"[DRY RUN] Would migrate {file_path}: {changes} Field definitions"
                )
        elif verbose:
            print(f"- No changes needed for {file_path}")

        return changes

    except Exception as e:
        print(f"✗ Error migrating {file_path}: {e}")
        return 0


def migrate_directory(
    directory_path: str, dry_run: bool = False, verbose: bool = False
) -> Tuple[int, int]:
    """
    Migrate all Python files in a directory recursively.
    """
    files_changed = 0
    total_changes = 0

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                changes = migrate_file(file_path, dry_run, verbose)
                if changes > 0:
                    files_changed += 1
                    total_changes += changes

    return files_changed, total_changes


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Robust Pydantic Field parameter migration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("path", help="Path to file or directory to migrate")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        return 1

    if os.path.isfile(args.path):
        changes = migrate_file(args.path, args.dry_run, args.verbose)
        if args.dry_run:
            print(f"\nDry run completed: {changes} changes would be made")
        else:
            print(f"\nMigration completed: {changes} changes made")
    elif os.path.isdir(args.path):
        files_changed, total_changes = migrate_directory(
            args.path, args.dry_run, args.verbose
        )
        if args.dry_run:
            print(
                f"\nDry run completed: {files_changed} files would be changed, {total_changes} total changes"
            )
        else:
            print(
                f"\nMigration completed: {files_changed} files changed, {total_changes} total changes"
            )
    else:
        print(f"Error: '{args.path}' is not a valid file or directory")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
