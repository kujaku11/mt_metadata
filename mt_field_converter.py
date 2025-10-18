#!/usr/bin/env python3
"""
MT Metadata Field Converter - Specialized for mt_metadata codebase patterns

This script is specifically designed to handle the Field definition patterns
found in the mt_metadata codebase, where Field definitions span multiple lines
with specific indentation and have existing json_schema_extra dictionaries.

Usage:
    python mt_field_converter.py <file_or_directory> [--dry-run] [--verbose]
"""

import argparse
import os
import re
import shutil
from typing import Tuple


def migrate_field_multiline(content: str) -> Tuple[str, int]:
    """
    Migrate multiline Field definitions by moving examples= into json_schema_extra.

    This handles the specific pattern:
    Field(
        default=...,
        description="...",
        examples=[...],
        alias=None,
        json_schema_extra={
            "units": ...,
            "required": ...,
        },
    )

    And converts it to:
    Field(
        default=...,
        description="...",
        alias=None,
        json_schema_extra={
            "units": ...,
            "required": ...,
            "examples": [...],
        },
    )
    """
    changes = 0
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Look for the start of a Field definition
        if "Field(" in line and "examples=" not in line:
            # This is the start of a multiline Field definition
            field_start = i
            field_lines = [line]
            i += 1

            # Collect all lines until we find the closing ),
            examples_line_idx = None
            examples_content = None
            json_schema_start = None
            json_schema_end = None

            while i < len(lines):
                current_line = lines[i]
                field_lines.append(current_line)

                # Check for examples= parameter
                if "examples=" in current_line and examples_line_idx is None:
                    examples_line_idx = len(field_lines) - 1
                    # Extract the examples content more carefully - handle both quoted strings and lists
                    examples_match = re.search(
                        r"examples\s*=\s*(\[[^\]]*\])", current_line
                    )
                    if examples_match:
                        examples_content = examples_match.group(1)
                    else:
                        # Handle quoted string examples
                        examples_match = re.search(
                            r'examples\s*=\s*(["\'][^"\']*["\'])', current_line
                        )
                        if examples_match:
                            examples_content = examples_match.group(1)
                        else:
                            # Handle other examples types
                            examples_match = re.search(
                                r"examples\s*=\s*([^,\n]+)", current_line
                            )
                            if examples_match:
                                examples_content = (
                                    examples_match.group(1).strip().rstrip(",")
                                )

                # Check for json_schema_extra start
                if "json_schema_extra=" in current_line and json_schema_start is None:
                    json_schema_start = len(field_lines) - 1

                # Check for the end of json_schema_extra (closing brace)
                if (
                    json_schema_start is not None
                    and "}" in current_line
                    and json_schema_end is None
                ):
                    json_schema_end = len(field_lines) - 1

                # Check if this is the end of the Field definition
                if ")," in current_line or (
                    current_line.strip().endswith(")") and "Field(" not in current_line
                ):
                    break

                i += 1

            # If we found both examples and json_schema_extra, perform the migration
            if (
                examples_line_idx is not None
                and examples_content is not None
                and json_schema_start is not None
                and json_schema_end is not None
            ):
                # Remove the examples line
                field_lines.pop(examples_line_idx)

                # Adjust indices after removal
                if json_schema_start > examples_line_idx:
                    json_schema_start -= 1
                if json_schema_end > examples_line_idx:
                    json_schema_end -= 1

                # Add the examples to the json_schema_extra
                # Find the line just before the closing brace
                insert_line = field_lines[json_schema_end]

                # Determine the indentation
                base_indent = len(insert_line) - len(insert_line.lstrip())
                if insert_line.strip() == "}":
                    # The closing brace is on its own line
                    examples_line = (
                        " " * (base_indent + 4) + f'"examples": {examples_content},'
                    )
                    field_lines.insert(json_schema_end, examples_line)
                else:
                    # The closing brace is at the end of a line with content
                    # Add a comma to the previous line and insert the examples
                    if not field_lines[json_schema_end - 1].rstrip().endswith(","):
                        field_lines[json_schema_end - 1] = (
                            field_lines[json_schema_end - 1].rstrip() + ","
                        )

                    examples_line = (
                        " " * (base_indent + 4) + f'"examples": {examples_content},'
                    )
                    field_lines.insert(json_schema_end, examples_line)

                # Replace the original lines with the modified field definition
                lines[field_start : field_start + len(field_lines)] = field_lines
                changes += 1

                # Adjust the index to continue after this field
                i = field_start + len(field_lines)
            else:
                i += 1
        else:
            i += 1

    return "\n".join(lines), changes


def migrate_field_inline_examples(content: str) -> Tuple[str, int]:
    """
    Handle inline examples= parameters that appear on the same line as Field(.
    """
    changes = 0

    # Pattern for inline examples with existing json_schema_extra
    pattern = r"(Field\s*\([^)]*examples\s*=\s*(\[[^\]]*\]|[^,)]+)[^)]*json_schema_extra\s*=\s*\{[^}]*)\}"

    def replace_inline(match):
        nonlocal changes
        field_content = match.group(0)
        examples_value = match.group(2)

        # Remove the examples parameter
        field_without_examples = re.sub(
            r",?\s*examples\s*=\s*(\[[^\]]*\]|[^,)]+),?", "", field_content
        )

        # Add examples to json_schema_extra
        field_with_examples = re.sub(
            r"(\{[^}]*)}",
            rf'\1, "examples": {examples_value}}}',
            field_without_examples,
        )

        changes += 1
        return field_with_examples

    content = re.sub(pattern, replace_inline, content, flags=re.DOTALL)
    return content, changes


def migrate_file_content(content: str) -> Tuple[str, int]:
    """
    Migrate all Field definitions in the file content.
    """
    total_changes = 0

    # First handle multiline Field definitions
    content, changes1 = migrate_field_multiline(content)
    total_changes += changes1

    # Then handle any remaining inline examples
    content, changes2 = migrate_field_inline_examples(content)
    total_changes += changes2

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
        description="Migrate Pydantic Field examples to json_schema_extra for mt_metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Test on a single file
    python mt_field_converter.py mt_metadata/processing/short_time_fourier_transform.py --dry-run

    # Migrate the common module
    python mt_field_converter.py mt_metadata/common/ --verbose

    # Migrate everything (use with caution!)
    python mt_field_converter.py mt_metadata/ --dry-run --verbose
        """,
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
