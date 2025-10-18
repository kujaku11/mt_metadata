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
    This version handles complex multiline structures more robustly.
    """
    changes = 0
    field_lines = lines[start : end + 1]

    # Find json_schema_extra boundaries first
    json_schema_start = None
    json_schema_end = None

    for i, line in enumerate(field_lines):
        if "json_schema_extra=" in line:
            json_schema_start = i
            # Find the end of the json_schema_extra block by tracking braces
            brace_count = line.count("{") - line.count("}")
            j = i + 1
            while j < len(field_lines) and brace_count > 0:
                brace_count += field_lines[j].count("{") - field_lines[j].count("}")
                j += 1
            json_schema_end = j - 1
            break

    # If no json_schema_extra found, we can't migrate
    if json_schema_start is None:
        return lines[start : end + 1], 0

    # Find deprecated parameters using a more robust approach
    deprecated_params = {}
    i = 0
    while i < len(field_lines):
        line = field_lines[i].strip()

        # Check for deprecated parameter starts
        param_match = None
        param_name = None

        if re.match(r"\s*(examples|type|items)\s*=", field_lines[i]):
            if "examples=" in field_lines[i]:
                param_name = "examples"
            elif (
                "type=" in field_lines[i] and "json_schema_extra" not in field_lines[i]
            ):
                param_name = "type"
            elif (
                "items=" in field_lines[i] and "json_schema_extra" not in field_lines[i]
            ):
                param_name = "items"

        if param_name:
            # Extract the parameter value, handling multiline cases
            param_lines = [i]
            param_value = ""

            # Get the part after the equals sign
            line_content = field_lines[i]
            equals_pos = line_content.find(f"{param_name}=")
            if equals_pos != -1:
                after_equals = line_content[equals_pos + len(param_name) + 1 :].strip()
                param_value = after_equals

                # Handle multiline values (lists, dicts, etc.)
                if (
                    after_equals.endswith("[")
                    or after_equals.endswith("{")
                    or not after_equals.endswith(",")
                ):
                    # This might be a multiline value
                    bracket_count = after_equals.count("[") - after_equals.count("]")
                    brace_count = after_equals.count("{") - after_equals.count("}")
                    paren_count = after_equals.count("(") - after_equals.count(")")

                    j = i + 1
                    while j < len(field_lines) and (
                        bracket_count > 0
                        or brace_count > 0
                        or paren_count > 0
                        or not param_value.rstrip().endswith(",")
                    ):
                        param_lines.append(j)
                        next_line = field_lines[j]
                        param_value += next_line

                        bracket_count += next_line.count("[") - next_line.count("]")
                        brace_count += next_line.count("{") - next_line.count("}")
                        paren_count += next_line.count("(") - next_line.count(")")

                        # Break if we hit another parameter or the end of the field
                        if (
                            bracket_count <= 0
                            and brace_count <= 0
                            and paren_count <= 0
                            and (
                                param_value.rstrip().endswith(",")
                                or param_value.rstrip().endswith("}")
                            )
                        ):
                            break

                        j += 1
                        if j >= len(field_lines):
                            break

                # Clean up the parameter value
                param_value = param_value.rstrip().rstrip(",").strip()

                deprecated_params[param_name] = {
                    "value": param_value,
                    "lines": param_lines,
                }
                changes += 1

                # Skip the lines we just processed
                i = max(param_lines) + 1
                continue

        i += 1

    if changes == 0:
        return lines[start : end + 1], 0

    # Build new field block
    lines_to_remove = set()
    for param_info in deprecated_params.values():
        lines_to_remove.update(param_info["lines"])

    new_field_lines = []

    # Copy lines, skipping the deprecated parameter lines
    for i, line in enumerate(field_lines):
        if i in lines_to_remove:
            continue

        # Insert new parameters into json_schema_extra before closing brace
        if i == json_schema_end:
            indent = "                "  # Match typical indentation

            # Add each deprecated parameter to json_schema_extra
            for param_name, param_info in deprecated_params.items():
                new_field_lines.append(
                    f'{indent}"{param_name}": {param_info["value"]},\n'
                )

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
