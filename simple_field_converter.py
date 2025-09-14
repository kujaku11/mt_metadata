#!/usr/bin/env python3
"""
Simple Field Converter - A more reliable approach to migrate Pydantic Field parameters.

This script uses a simpler line-by-line approach to avoid regex complexity issues.
"""

import argparse
import os
import re
import shutil
from typing import List, Tuple


def find_field_definitions(lines: List[str]) -> List[Tuple[int, int]]:
    """
    Find Field definition blocks in the file.
    Returns list of (start_line, end_line) tuples.
    """
    field_blocks = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "Field(" in line:
            start_line = i
            # Find the matching closing parenthesis
            paren_count = line.count("(") - line.count(")")
            j = i + 1
            while j < len(lines) and paren_count > 0:
                paren_count += lines[j].count("(") - lines[j].count(")")
                j += 1
            if paren_count == 0:
                field_blocks.append((start_line, j - 1))
                i = j
            else:
                i += 1
        else:
            i += 1
    return field_blocks


def migrate_field_block(
    lines: List[str], start: int, end: int
) -> Tuple[List[str], int]:
    """
    Migrate a single Field block by moving deprecated parameters into json_schema_extra.
    Returns (updated_lines, changes_count).
    """
    changes = 0
    field_lines = lines[start : end + 1]

    # Find deprecated parameters
    examples_line = None
    type_line = None
    items_line = None
    json_schema_start = None
    json_schema_end = None

    for i, line in enumerate(field_lines):
        stripped = line.strip()
        if stripped.startswith("examples="):
            examples_line = i
        elif stripped.startswith("type="):
            type_line = i
        elif stripped.startswith("items="):
            items_line = i
        elif "json_schema_extra=" in line:
            json_schema_start = i
            # Find the end of the json_schema_extra block
            brace_count = line.count("{") - line.count("}")
            j = i + 1
            while j < len(field_lines) and brace_count > 0:
                brace_count += field_lines[j].count("{") - field_lines[j].count("}")
                j += 1
            json_schema_end = j - 1

    # If no json_schema_extra found, we can't migrate
    if json_schema_start is None:
        return lines[start : end + 1], 0

    # Extract parameter values
    examples_value = None
    type_value = None
    items_value = None

    if examples_line is not None:
        examples_match = re.search(
            r"examples\s*=\s*(.+?)(?:,\s*)?$", field_lines[examples_line]
        )
        if examples_match:
            examples_value = examples_match.group(1).rstrip(",")
            changes += 1

    if type_line is not None:
        type_match = re.search(r"type\s*=\s*(.+?)(?:,\s*)?$", field_lines[type_line])
        if type_match:
            type_value = type_match.group(1).rstrip(",")
            changes += 1

    if items_line is not None:
        items_match = re.search(r"items\s*=\s*(.+?)(?:,\s*)?$", field_lines[items_line])
        if items_match:
            items_value = items_match.group(1).rstrip(",")
            changes += 1

    if changes == 0:
        return lines[start : end + 1], 0

    # Build new field block
    new_field_lines = []

    # Add lines before deprecated parameters
    for i, line in enumerate(field_lines):
        if i in [examples_line, type_line, items_line]:
            continue  # Skip deprecated parameter lines

        if i == json_schema_end:
            # Insert new parameters before closing brace
            indent = "                "  # Match typical indentation
            if examples_value:
                new_field_lines.append(f'{indent}"examples": {examples_value},\n')
            if type_value:
                new_field_lines.append(f'{indent}"type": {type_value},\n')
            if items_value:
                new_field_lines.append(f'{indent}"items": {items_value},\n')

        new_field_lines.append(line)

    return new_field_lines, changes


def migrate_file_content(content: str) -> Tuple[str, int]:
    """
    Migrate all deprecated Field parameters in the content.
    """
    lines = content.splitlines(keepends=True)
    field_blocks = find_field_definitions(lines)

    total_changes = 0
    new_lines = lines.copy()

    # Process blocks in reverse order to maintain line numbers
    for start, end in reversed(field_blocks):
        updated_block, changes = migrate_field_block(lines, start, end)
        new_lines[start : end + 1] = updated_block
        total_changes += changes

    return "".join(new_lines), total_changes


def migrate_file(file_path: str, dry_run: bool = False, verbose: bool = False) -> int:
    """
    Migrate a single Python file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Check if file has deprecated Field usage
        if not any(
            pattern in original_content for pattern in ["examples=", "type=", "items="]
        ):
            if verbose:
                print(f"- No changes needed for {file_path}")
            return 0

        migrated_content, changes = migrate_file_content(original_content)

        if changes == 0:
            if verbose:
                print(f"- No changes needed for {file_path}")
            return 0

        if dry_run:
            print(f"Would migrate {file_path}: {changes} Field definitions")
            return changes

        # Create backup
        backup_path = f"{file_path}.backup"
        if not os.path.exists(backup_path):
            shutil.copy2(file_path, backup_path)

        # Write migrated content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(migrated_content)

        print(f"✓ Migrated {file_path}: {changes} Field definitions updated")
        if verbose:
            print(f"  Backup created: {backup_path}")

        return changes

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Migrate Pydantic Field parameters to json_schema_extra"
    )
    parser.add_argument("path", help="File or directory path to migrate")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        files_to_process = [args.path]
    elif os.path.isdir(args.path):
        files_to_process = []
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith(".py"):
                    files_to_process.append(os.path.join(root, file))
    else:
        print(f"Error: {args.path} is not a valid file or directory")
        return 1

    total_changes = 0
    files_changed = 0

    for file_path in files_to_process:
        changes = migrate_file(file_path, args.dry_run, args.verbose)
        if changes > 0:
            files_changed += 1
            total_changes += changes

    if args.dry_run:
        print(
            f"\nDry run completed: {files_changed} files with {total_changes} total changes"
        )
    else:
        print(
            f"\nMigration completed: {files_changed} files changed, {total_changes} total changes"
        )


if __name__ == "__main__":
    main()
