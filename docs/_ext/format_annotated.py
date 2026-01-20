"""
Custom Sphinx extension to format Annotated field signatures.

This extension reformats how Annotated type hints are displayed by:
1. Splitting on brackets [ ] and commas for better color targeting
2. Wrapping each component in separate spans with semantic classes
"""

import re

from sphinx.application import Sphinx


def process_signature(app, what, name, obj, options, signature, return_annotation):
    """
    Process function/class signatures to reformat Annotated types.
    """
    if signature and "Annotated[" in signature:
        # Split Annotated signature into semantic parts
        # Pattern: Annotated[type, Field(...)]
        pattern = r"Annotated\[(.*?)\]"

        def reformat_annotated(match):
            content = match.group(1)
            # Split on commas at the top level (not inside parentheses)
            parts = split_on_comma(content)

            if len(parts) >= 2:
                type_part = parts[0].strip()
                field_part = ", ".join(parts[1:]).strip()

                # Reformat as: Annotated [ type , Field ]
                return f"Annotated [ {type_part} , {field_part} ]"

            return match.group(0)

        signature = re.sub(pattern, reformat_annotated, signature)

    return signature, return_annotation


def split_on_comma(text):
    """
    Split text on commas, but only at the top level (not inside parentheses/brackets).
    """
    parts = []
    current = []
    depth = 0

    for char in text:
        if char in "([{":
            depth += 1
            current.append(char)
        elif char in ")]}":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)

    if current:
        parts.append("".join(current))

    return parts


def process_docstring(app, what, name, obj, options, lines):
    """
    Process docstrings to reformat Annotated type references.
    """
    # This can be used to reformat type hints in docstrings if needed


def setup(app: Sphinx):
    """
    Setup the Sphinx extension.
    """
    app.connect("autodoc-process-signature", process_signature)
    app.connect("autodoc-process-docstring", process_docstring)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
