#!/usr/bin/env python3
"""
Comprehensive Pydantic Field Migration Script

This script converts deprecated Pydantic Field parameters to the new json_schema_extra format.
It handles the specific patterns found in the mt_metadata codebase where Field definitions
have existing json_schema_extra dictionaries that need to be updated.

Usage:
    python field_converter.py <file_or_directory> [--dry-run] [--verbose]
"""

import argparse
import os
import re
import shutil
from typing import Dict, Tuple


def parse_field_content(field_content: str) -> Dict[str, str]:
    """
    Parse the content inside a Field() definition to extract parameters.

    Args:
        field_content: The content inside Field(...)

    Returns:
        Dictionary mapping parameter names to their values
    """
    params = {}

    # Handle multiline content by removing extra whitespace
    normalized_content = re.sub(r"\s+", " ", field_content.strip())

    # Patterns for different parameter types
    patterns = {
        "default": r"default\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "description": r'description\s*=\s*(["\'][^"\']*["\'])',
        "alias": r"alias\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "validation_alias": r"validation_alias\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "pattern": r"pattern\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "examples": r"examples\s*=\s*(\[[^\]]*\])",
        "type": r"type\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "items": r"items\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "json_schema_extra": r"json_schema_extra\s*=\s*(\{[^}]*\})",
    }

    for param_name, pattern in patterns.items():
        match = re.search(pattern, field_content)
        if match:
            params[param_name] = match.group(1).strip()

    return params


def merge_json_schema_extra(
    existing_extra: str, deprecated_params: Dict[str, str]
) -> str:
    """
    Merge deprecated parameters into existing json_schema_extra dictionary.

    Args:
        existing_extra: The existing json_schema_extra content (without braces)
        deprecated_params: Dictionary of deprecated parameters to add

    Returns:
        The new json_schema_extra content
    """
    # Parse existing content
    existing_content = existing_extra.strip("{}").strip()

    # Build new parameters list
    new_params = []

    # Add existing parameters first
    if existing_content:
        # Split by commas, but be careful of nested structures
        parts = []
        current_part = ""
        brace_level = 0
        bracket_level = 0

        for char in existing_content + ",":
            if char == "{":
                brace_level += 1
            elif char == "}":
                brace_level -= 1
            elif char == "[":
                bracket_level += 1
            elif char == "]":
                bracket_level -= 1
            elif char == "," and brace_level == 0 and bracket_level == 0:
                if current_part.strip():
                    parts.append(current_part.strip())
                current_part = ""
                continue

            current_part += char

        new_params.extend(parts)

    # Add deprecated parameters
    for key, value in deprecated_params.items():
        new_params.append(f'"{key}": {value}')

    return "{" + ", ".join(new_params) + "}"


def migrate_field_block(field_block: str) -> Tuple[str, bool]:
    """
    Migrate a complete Field definition block.

    Args:
        field_block: The complete Field definition including parameters

    Returns:
        Tuple of (migrated_block, was_changed)
    """
    # Extract the content inside Field(...)
    field_match = re.match(r"(\s*Field\s*\()(.*?)(\),?\s*)", field_block, re.DOTALL)
    if not field_match:
        return field_block, False

    prefix = field_match.group(1)
    content = field_match.group(2)
    suffix = field_match.group(3)

    # Parse parameters
    params = parse_field_content(content)

    # Check for deprecated parameters
    deprecated_params = {}
    deprecated_keys = ["examples", "type", "items"]

    for key in deprecated_keys:
        if key in params:
            deprecated_params[key] = params.pop(key)

    if not deprecated_params:
        return field_block, False

    # Handle json_schema_extra
    if "json_schema_extra" in params:
        # Merge with existing
        existing_extra = params["json_schema_extra"]
        new_extra = merge_json_schema_extra(existing_extra, deprecated_params)
        params["json_schema_extra"] = new_extra
    else:
        # Create new json_schema_extra
        extra_items = [f'"{key}": {value}' for key, value in deprecated_params.items()]
        params["json_schema_extra"] = "{" + ", ".join(extra_items) + "}"

    # Reconstruct the Field definition
    param_parts = []
    param_order = [
        "default",
        "description",
        "alias",
        "validation_alias",
        "pattern",
        "json_schema_extra",
    ]

    # Add parameters in preferred order
    for param_name in param_order:
        if param_name in params:
            param_parts.append(f"{param_name}={params[param_name]}")
            del params[param_name]

    # Add any remaining parameters
    for param_name, param_value in params.items():
        param_parts.append(f"{param_name}={param_value}")

    # Format the parameters with proper indentation
    if len(param_parts) <= 2:
        # Short format on one line
        params_str = ", ".join(param_parts)
    else:
        # Multi-line format with proper indentation
        indent = " " * 12  # Standard indentation for Field parameters
        params_str = ",\n" + indent + f",\n{indent}".join(param_parts) + ",\n        "

    new_field_block = prefix + params_str + suffix
    return new_field_block, True


def migrate_file_content(content: str) -> Tuple[str, int]:
    """
    Migrate all Field definitions in file content.

    Args:
        content: File content to migrate

    Returns:
        Tuple of (migrated_content, number_of_changes)
    """
    changes = 0

    # Pattern to match complete Field definitions with their parameters
    # This pattern captures multiline Field definitions
    field_pattern = r"(\s*Field\s*\([^)]*(?:\([^)]*\)[^)]*)*\),?)"

    def replace_field(match):
        nonlocal changes
        field_block = match.group(1)
        migrated_block, was_changed = migrate_field_block(field_block)
        if was_changed:
            changes += 1
        return migrated_block

    # Find and replace all Field definitions
    migrated_content = re.sub(field_pattern, replace_field, content, flags=re.DOTALL)

    # Alternative approach for complex nested Field definitions
    if changes == 0:
        # Try line-by-line approach for stubborn cases
        lines = content.split("\n")
        in_field = False
        field_lines = []
        field_start_idx = 0

        for i, line in enumerate(lines):
            if "Field(" in line and not in_field:
                in_field = True
                field_start_idx = i
                field_lines = [line]
            elif in_field:
                field_lines.append(line)
                if ")," in line or (line.strip().endswith(")") and line.strip() != ")"):
                    # End of field definition
                    field_content = "\n".join(field_lines)
                    migrated_field, was_changed = migrate_field_block(field_content)
                    if was_changed:
                        # Replace the lines
                        migrated_lines = migrated_field.split("\n")
                        lines[field_start_idx : i + 1] = migrated_lines
                        changes += 1
                    in_field = False
                    field_lines = []

        migrated_content = "\n".join(lines)

    return migrated_content, changes


def migrate_file(file_path: str, dry_run: bool = False, verbose: bool = False) -> int:
    """
    Migrate a single Python file.

    Args:
        file_path: Path to the file to migrate
        dry_run: If True, don't write changes, just report what would be done
        verbose: If True, show detailed output

    Returns:
        Number of Field definitions changed
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

    Args:
        directory_path: Path to directory to migrate
        dry_run: If True, don't write changes
        verbose: If True, show detailed output

    Returns:
        Tuple of (files_changed, total_changes)
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
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Migrate deprecated Pydantic Field parameters to json_schema_extra format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Migrate a single file
    python field_converter.py mt_metadata/common/band.py

    # Dry run on a directory
    python field_converter.py mt_metadata/common/ --dry-run --verbose

    # Migrate entire mt_metadata module
    python field_converter.py mt_metadata/ --verbose
        """,
    )

    parser.add_argument("path", help="Path to file or directory to migrate")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output including files with no changes",
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
