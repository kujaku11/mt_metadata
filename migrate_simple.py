#!/usr/bin/env python3
"""
Simple and robust Pydantic Field migration script.

This script migrates Field definitions by using regex replacement patterns
specifically tailored to the mt_metadata codebase structure.
"""

import os
import re
import shutil


def migrate_field_in_content(content):
    """
    Migrate Field definitions using regex patterns.
    """
    changes = 0

    # Pattern 1: Field with examples parameter (most common case)
    pattern1 = r"(Field\s*\(\s*)(.*?)(examples\s*=\s*(\[[^\]]*\]|[^,\s]+))(.*?)(\))"

    def replace_examples(match):
        nonlocal changes
        prefix = match.group(1)
        before_examples = match.group(2)
        examples_part = match.group(3)
        examples_value = match.group(4)
        after_examples = match.group(5)
        suffix = match.group(6)

        # Check if json_schema_extra already exists
        if "json_schema_extra" in before_examples + after_examples:
            # Need to merge with existing json_schema_extra
            existing_match = re.search(
                r"json_schema_extra\s*=\s*\{([^}]*)\}", before_examples + after_examples
            )
            if existing_match:
                existing_content = existing_match.group(1).strip()

                # Remove the existing json_schema_extra from the parts
                before_examples = re.sub(
                    r"json_schema_extra\s*=\s*\{[^}]*\},?\s*", "", before_examples
                )
                after_examples = re.sub(
                    r"json_schema_extra\s*=\s*\{[^}]*\},?\s*", "", after_examples
                )

                # Create new json_schema_extra with examples added
                if existing_content:
                    new_extra = f'json_schema_extra={{"examples": {examples_value}, {existing_content}}}'
                else:
                    new_extra = f'json_schema_extra={{"examples": {examples_value}}}'
            else:
                new_extra = f'json_schema_extra={{"examples": {examples_value}}}'
        else:
            new_extra = f'json_schema_extra={{"examples": {examples_value}}}'

        # Clean up commas
        combined_params = before_examples + after_examples
        combined_params = re.sub(r",\s*,", ",", combined_params)  # Remove double commas
        combined_params = re.sub(
            r"^\s*,\s*", "", combined_params
        )  # Remove leading comma
        combined_params = re.sub(r",\s*$", "", combined_params)  # Remove trailing comma

        if combined_params.strip():
            result = f"{prefix}{combined_params}, {new_extra}{suffix}"
        else:
            result = f"{prefix}{new_extra}{suffix}"

        changes += 1
        return result

    # Apply the replacement
    content = re.sub(pattern1, replace_examples, content, flags=re.DOTALL)

    # Pattern 2: Field with type parameter
    pattern2 = r"(Field\s*\([^)]*)(type\s*=\s*([^,\)]+))([^)]*\))"

    def replace_type(match):
        nonlocal changes
        before_type = match.group(1)
        type_part = match.group(2)
        type_value = match.group(3)
        after_type = match.group(4)

        # Check if json_schema_extra already exists
        if "json_schema_extra" in before_type + after_type:
            # Merge with existing
            existing_match = re.search(
                r"json_schema_extra\s*=\s*\{([^}]*)\}", before_type + after_type
            )
            if existing_match:
                existing_content = existing_match.group(1).strip()
                modified_after = re.sub(
                    r"json_schema_extra\s*=\s*\{[^}]*\}",
                    f'json_schema_extra={{"type": {type_value}, {existing_content}}}',
                    after_type,
                )
                result = before_type + modified_after
            else:
                result = before_type + after_type.replace(
                    ")", f', json_schema_extra={{"type": {type_value}}})'
                )
        else:
            result = before_type + after_type.replace(
                ")", f', json_schema_extra={{"type": {type_value}}})'
            )

        changes += 1
        return result

    content = re.sub(pattern2, replace_type, content, flags=re.DOTALL)

    # Pattern 3: Field with items parameter
    pattern3 = r"(Field\s*\([^)]*)(items\s*=\s*([^,\)]+))([^)]*\))"

    def replace_items(match):
        nonlocal changes
        before_items = match.group(1)
        items_part = match.group(2)
        items_value = match.group(3)
        after_items = match.group(4)

        # Check if json_schema_extra already exists
        if "json_schema_extra" in before_items + after_items:
            # Merge with existing
            existing_match = re.search(
                r"json_schema_extra\s*=\s*\{([^}]*)\}", before_items + after_items
            )
            if existing_match:
                existing_content = existing_match.group(1).strip()
                modified_after = re.sub(
                    r"json_schema_extra\s*=\s*\{[^}]*\}",
                    f'json_schema_extra={{"items": {items_value}, {existing_content}}}',
                    after_items,
                )
                result = before_items + modified_after
            else:
                result = before_items + after_items.replace(
                    ")", f', json_schema_extra={{"items": {items_value}}})'
                )
        else:
            result = before_items + after_items.replace(
                ")", f', json_schema_extra={{"items": {items_value}}})'
            )

        changes += 1
        return result

    content = re.sub(pattern3, replace_items, content, flags=re.DOTALL)

    return content, changes


def migrate_file_simple(file_path, dry_run=False):
    """
    Migrate a single file using simple pattern matching.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        migrated_content, changes = migrate_field_in_content(original_content)

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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python migrate_simple.py <file_path> [--dry-run]")
        sys.exit(1)

    file_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    if os.path.isfile(file_path):
        changes = migrate_file_simple(file_path, dry_run)
        print(f"Completed: {changes} changes made")
    else:
        print(f"Error: {file_path} is not a valid file")
