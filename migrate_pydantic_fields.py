#!/usr/bin/env python3
"""
Script to migrate deprecated Pydantic Field parameters to json_schema_extra format.

This script converts Field definitions from:
    Field(default=..., description=..., examples=..., type=..., items=...)

To:
    Field(default=..., description=..., json_schema_extra={"examples": ..., "type": ..., "items": ...})
"""

import os
import re
import shutil


def migrate_field_definition(content):
    """
    Migrate Field definitions in the given content.

    Args:
        content (str): File content with Field definitions

    Returns:
        tuple: (migrated_content, number_of_changes)
    """
    changes = 0

    # Pattern to match Field() definitions
    field_pattern = r"(Field\s*\()"

    # Find all Field() calls
    field_matches = list(re.finditer(field_pattern, content))

    # Process from end to beginning to maintain indices
    for match in reversed(field_matches):
        start_pos = match.start()

        # Find the matching closing parenthesis
        paren_count = 0
        pos = start_pos
        while pos < len(content):
            if content[pos] == "(":
                paren_count += 1
            elif content[pos] == ")":
                paren_count -= 1
                if paren_count == 0:
                    end_pos = pos + 1
                    break
            pos += 1
        else:
            continue  # No matching closing paren found

        # Extract the Field definition
        field_def = content[start_pos:end_pos]

        # Check if it contains deprecated parameters
        deprecated_params = ["examples", "type", "items"]
        has_deprecated = any(
            re.search(rf"\b{param}\s*=", field_def) for param in deprecated_params
        )

        if not has_deprecated:
            continue

        # Parse and migrate the Field definition
        migrated_def = migrate_single_field(field_def)
        if migrated_def != field_def:
            content = content[:start_pos] + migrated_def + content[end_pos:]
            changes += 1

    return content, changes


def migrate_single_field(field_def):
    """
    Migrate a single Field definition.

    Args:
        field_def (str): Single Field definition

    Returns:
        str: Migrated Field definition
    """
    # Extract parameters inside Field()
    inner_match = re.match(r"Field\s*\((.*)\)", field_def, re.DOTALL)
    if not inner_match:
        return field_def

    inner_content = inner_match.group(1)

    # Parse parameters
    params = parse_field_parameters(inner_content)

    # Extract deprecated parameters
    deprecated_params = {}
    deprecated_keys = ["examples", "type", "items"]

    for key in deprecated_keys:
        if key in params:
            deprecated_params[key] = params.pop(key)

    if not deprecated_params:
        return field_def

    # Handle existing json_schema_extra
    if "json_schema_extra" in params:
        # Parse existing json_schema_extra
        existing_extra = params["json_schema_extra"]

        # Remove outer braces if they exist
        if existing_extra.strip().startswith("{") and existing_extra.strip().endswith(
            "}"
        ):
            existing_inner = existing_extra.strip()[1:-1]

            # Add deprecated params to existing json_schema_extra
            new_params = []
            if existing_inner.strip():
                new_params.append(existing_inner.strip())

            for key, value in deprecated_params.items():
                new_params.append(f'"{key}": {value}')

            params["json_schema_extra"] = "{" + ", ".join(new_params) + "}"
        else:
            # Existing json_schema_extra is not a dict, handle carefully
            return field_def
    else:
        # Create new json_schema_extra
        extra_items = [f'"{key}": {value}' for key, value in deprecated_params.items()]
        params["json_schema_extra"] = "{" + ", ".join(extra_items) + "}"

    # Reconstruct Field definition
    param_strings = []
    for key, value in params.items():
        param_strings.append(f"{key}={value}")

    return f"Field({', '.join(param_strings)})"


def parse_field_parameters(param_string):
    """
    Parse parameters from a Field definition string.

    This is a simplified parser that handles basic cases.
    """
    params = {}

    # Simple regex-based parsing for common parameter patterns
    patterns = {
        "default": r"default\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "description": r"description\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "examples": r"examples\s*=\s*(\[[^\]]*\]|[^,]+?)(?=\s*,|\s*$)",
        "type": r"type\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "items": r"items\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "alias": r"alias\s*=\s*([^,]+?)(?=\s*,|\s*$)",
        "json_schema_extra": r"json_schema_extra\s*=\s*(\{[^}]*\})",
    }

    for param_name, pattern in patterns.items():
        match = re.search(pattern, param_string, re.DOTALL)
        if match:
            value = match.group(1).strip()
            # Handle multiline values by removing extra whitespace
            if "\n" in value:
                lines = value.split("\n")
                value = " ".join(line.strip() for line in lines if line.strip())
            params[param_name] = value

    return params


def migrate_file(file_path, dry_run=False):
    """
    Migrate a single file.

    Args:
        file_path (str): Path to the file to migrate
        dry_run (bool): If True, don't write changes

    Returns:
        int: Number of changes made
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        migrated_content, changes = migrate_field_definition(original_content)

        if changes > 0 and not dry_run:
            # Create backup
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)

            # Write migrated content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(migrated_content)

            print(f"✓ Migrated {file_path}: {changes} Field definitions updated")
        elif changes > 0:
            print(f"[DRY RUN] Would migrate {file_path}: {changes} Field definitions")

        return changes

    except Exception as e:
        print(f"✗ Error migrating {file_path}: {e}")
        return 0


def migrate_module(module_path, dry_run=False):
    """
    Migrate all files in a module directory.

    Args:
        module_path (str): Path to the module directory
        dry_run (bool): If True, don't write changes

    Returns:
        tuple: (files_changed, total_changes)
    """
    files_changed = 0
    total_changes = 0

    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                changes = migrate_file(file_path, dry_run)
                if changes > 0:
                    files_changed += 1
                    total_changes += changes

    return files_changed, total_changes


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate Pydantic Field definitions")
    parser.add_argument("path", help="Path to file or directory to migrate")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )

    args = parser.parse_args()

    if os.path.isfile(args.path):
        changes = migrate_file(args.path, args.dry_run)
        print(f"Completed: {changes} changes made")
    elif os.path.isdir(args.path):
        files_changed, total_changes = migrate_module(args.path, args.dry_run)
        print(
            f"Completed: {files_changed} files changed, {total_changes} total changes"
        )
    else:
        print(f"Error: {args.path} is not a valid file or directory")
