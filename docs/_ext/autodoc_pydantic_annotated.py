"""
Custom Sphinx extension to improve display of Pydantic Annotated fields.

This extension processes type annotations to format Annotated[type, FieldInfo(...)]
in a more readable way, extracting key information and displaying it cleanly.
"""

from __future__ import annotations

import re
from typing import Any

from sphinx.application import Sphinx


def format_annotated_field(annotation_str: str) -> str:
    """
    Format Pydantic Annotated field annotations for better readability.

    Converts verbose Annotated[type, FieldInfo(...)] to a cleaner format by
    extracting just the base type and removing the verbose FieldInfo details.

    Parameters
    ----------
    annotation_str : str
        The raw annotation string from Pydantic

    Returns
    -------
    str
        Formatted annotation string containing just the base type

    Examples
    --------
    >>> format_annotated_field("Annotated[int, FieldInfo(...)]")
    'int'
    >>> format_annotated_field("Annotated[str | None, FieldInfo(...)]")
    'str | None'
    """
    # Check if this is an Annotated type
    if not annotation_str.startswith("Annotated["):
        return annotation_str

    # Extract content between Annotated[ and the matching ]
    # We need to handle nested brackets properly
    bracket_count = 0
    start_idx = len("Annotated[")

    for i, char in enumerate(annotation_str[start_idx:], start=start_idx):
        if char == "[":
            bracket_count += 1
        elif char == "]":
            if bracket_count == 0:
                # This is the closing bracket of Annotated
                content = annotation_str[start_idx:i]
                break
            bracket_count -= 1
    else:
        # Couldn't find matching bracket
        return annotation_str

    # Split by comma, but only at the top level (not within brackets)
    parts = []
    current_part = []
    bracket_count = 0

    for char in content:
        if char == "[":
            bracket_count += 1
        elif char == "]":
            bracket_count -= 1
        elif char == "," and bracket_count == 0:
            # Top-level comma - this separates type from FieldInfo
            parts.append("".join(current_part).strip())
            current_part = []
            continue
        current_part.append(char)

    if current_part:
        parts.append("".join(current_part).strip())

    # The first part is the base type
    if parts:
        base_type = parts[0]
        # Clean up any remaining artifacts
        base_type = re.sub(r"\s+", " ", base_type)
        return base_type

    return annotation_str


def extract_field_metadata(annotation_str: str) -> dict[str, Any]:
    """
    Extract metadata from FieldInfo in an Annotated type.

    Parameters
    ----------
    annotation_str : str
        The raw annotation string from Pydantic

    Returns
    -------
    dict
        Dictionary containing extracted metadata (description, units, examples, etc.)
    """
    metadata = {}

    # Check if this contains FieldInfo
    field_info_match = re.search(r"FieldInfo\((.*)\)", annotation_str, re.DOTALL)

    if not field_info_match:
        return metadata

    field_info_content = field_info_match.group(1)

    # Extract description
    desc_match = re.search(r"description='([^']*(?:''[^']*)*)'", field_info_content)
    if not desc_match:
        desc_match = re.search(r'description="([^"]*(?:""[^"]*)*)"', field_info_content)
    if desc_match:
        metadata["description"] = desc_match.group(1).replace("''", "'")

    # Extract default value
    default_match = re.search(r"default=([^,\)]+)", field_info_content)
    if default_match:
        default_val = default_match.group(1).strip()
        if default_val not in ("PydanticUndefined", "Undefined"):
            metadata["default"] = default_val

    # Extract required status from json_schema_extra
    required_match = re.search(r"'required':\s*(True|False)", field_info_content)
    if required_match:
        metadata["required"] = required_match.group(1) == "True"

    # Extract units from json_schema_extra
    units_match = re.search(r"'units':\s*'([^']*)'", field_info_content)
    if units_match:
        metadata["units"] = units_match.group(1)

    # Extract examples from json_schema_extra
    examples_match = re.search(r"'examples':\s*\[([^\]]+)\]", field_info_content)
    if examples_match:
        metadata["examples"] = examples_match.group(1)

    # Extract pattern validation
    pattern_match = re.search(r"pattern='([^']*)'", field_info_content)
    if not pattern_match:
        pattern_match = re.search(r'"pattern":\s*"([^"]*)"', field_info_content)
    if pattern_match:
        metadata["pattern"] = pattern_match.group(1)

    return metadata


def process_signature(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: dict,
    signature: str | None,
    return_annotation: str | None,
) -> tuple[str | None, str | None]:
    """
    Process function/method signatures to clean up Annotated types.

    This is called by Sphinx autodoc before rendering signatures.
    """
    if signature:
        # Process each parameter in the signature
        # Replace Annotated[...] with just the base type
        def replace_annotated(match):
            full_match = match.group(0)
            return format_annotated_field(full_match)

        # Use a more sophisticated regex that handles nested brackets
        # We'll process character by character when we find "Annotated["
        new_signature = signature
        while "Annotated[" in new_signature:
            start_idx = new_signature.find("Annotated[")
            if start_idx == -1:
                break

            # Find the matching closing bracket
            bracket_count = 0
            end_idx = start_idx + len("Annotated[")
            for i in range(end_idx, len(new_signature)):
                if new_signature[i] == "[":
                    bracket_count += 1
                elif new_signature[i] == "]":
                    if bracket_count == 0:
                        end_idx = i + 1
                        break
                    bracket_count -= 1

            # Extract and format this Annotated block
            annotated_block = new_signature[start_idx:end_idx]
            formatted = format_annotated_field(annotated_block)

            # Replace in the signature
            new_signature = (
                new_signature[:start_idx] + formatted + new_signature[end_idx:]
            )

        signature = new_signature

    return signature, return_annotation


def process_docstring(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: dict,
    lines: list[str],
) -> None:
    """
    Process docstrings to add formatted field information.

    For Pydantic model attributes with Annotated types, this adds
    formatted metadata to the docstring in a clean, readable format.
    """
    # Try to get the annotation if it's an attribute
    if what == "attribute" and hasattr(obj, "__annotations__"):
        # Extract field name from the full name (e.g., "Class.field" -> "field")
        field_name = name.split(".")[-1]

        # Check if this field has an annotation
        if field_name in obj.__annotations__:
            annotation = obj.__annotations__[field_name]
            annotation_str = str(annotation)

            # Extract metadata from the annotation
            metadata = extract_field_metadata(annotation_str)

            if metadata:
                # Add metadata to docstring in a clean format
                if lines and lines[0]:  # If there's existing content
                    lines.append("")

                # Add metadata lines
                if "description" in metadata:
                    # Description might already be in docstring, skip if so
                    pass

                if "units" in metadata and metadata["units"]:
                    lines.append(f":Units: {metadata['units']}")

                if "required" in metadata:
                    req_str = "Yes" if metadata["required"] else "No"
                    lines.append(f":Required: {req_str}")

                if "default" in metadata:
                    lines.append(f":Default: {metadata['default']}")

                if "examples" in metadata:
                    lines.append(f":Examples: {metadata['examples']}")

                if "pattern" in metadata:
                    lines.append(f":Pattern: ``{metadata['pattern']}``")


def setup(app: Sphinx) -> dict[str, Any]:
    """
    Setup function for the Sphinx extension.

    Parameters
    ----------
    app : Sphinx
        The Sphinx application instance

    Returns
    -------
    dict
        Extension metadata
    """
    # Connect to autodoc events
    app.connect("autodoc-process-signature", process_signature)
    app.connect("autodoc-process-docstring", process_docstring)

    # Add configuration for cleaner type hints
    app.setup_extension("sphinx.ext.autodoc.typehints")
    app.config.autodoc_typehints = "description"
    app.config.autodoc_typehints_description_target = "documented"

    # Custom CSS to improve display
    app.add_css_file("pydantic_annotated.css")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
