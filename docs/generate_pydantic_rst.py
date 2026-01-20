#!/usr/bin/env python
"""
Generate RST files with autopydantic_model directives for Pydantic models.

This script walks through the mt_metadata package and generates RST documentation
files that use autopydantic_model for Pydantic BaseModel subclasses and autoclass
for regular classes.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Any

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None


def is_pydantic_model(obj: Any) -> bool:
    """Check if an object is a Pydantic model."""
    if BaseModel is None:
        return False
    try:
        return (
            inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel
        )
    except (TypeError, AttributeError):
        return False


def get_module_members(module_name: str) -> dict[str, list[str]]:
    """
    Get Pydantic models and regular classes from a module.

    Parameters
    ----------
    module_name : str
        Full module name (e.g., 'mt_metadata.common.band')

    Returns
    -------
    dict
        Dictionary with 'pydantic_models' and 'classes' keys
    """
    try:
        module = importlib.import_module(module_name)
    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not import {module_name}: {e}")
        return {"pydantic_models": [], "classes": [], "functions": []}

    pydantic_models = []
    classes = []
    functions = []

    for name in dir(module):
        if name.startswith("_"):
            continue

        try:
            obj = getattr(module, name)

            # Check if it's defined in this module (not imported)
            if hasattr(obj, "__module__") and obj.__module__ != module_name:
                continue

            if is_pydantic_model(obj):
                pydantic_models.append(name)
            elif inspect.isclass(obj):
                classes.append(name)
            elif inspect.isfunction(obj):
                functions.append(name)
        except (AttributeError, ImportError):
            continue

    return {
        "pydantic_models": sorted(pydantic_models),
        "classes": sorted(classes),
        "functions": sorted(functions),
    }


def generate_module_rst(
    module_name: str,
    output_dir: Path,
    members: dict[str, list[str]],
) -> None:
    """
    Generate RST file for a module with appropriate directives.

    Parameters
    ----------
    module_name : str
        Full module name
    output_dir : Path
        Directory to write RST files
    members : dict
        Dictionary of module members
    """
    # Create RST filename
    rst_filename = output_dir / f"{module_name}.rst"

    # Format module name for title
    title = f"{module_name} module"
    underline = "=" * len(title)

    lines = [
        title,
        underline,
        "",
        f".. automodule:: {module_name}",
        "   :no-members:",
        "   :no-inherited-members:",
        "",
    ]

    # Add Pydantic models
    if members["pydantic_models"]:
        for model_name in members["pydantic_models"]:
            full_name = f"{module_name}.{model_name}"
            lines.extend(
                [
                    f".. autopydantic_model:: {full_name}",
                    "   :members:",
                    "   :undoc-members:",
                    "   :show-inheritance:",
                    "   :member-order: bysource",
                    "",
                ]
            )

    # Add regular classes
    if members["classes"]:
        for class_name in members["classes"]:
            full_name = f"{module_name}.{class_name}"
            lines.extend(
                [
                    f".. autoclass:: {full_name}",
                    "   :members:",
                    "   :undoc-members:",
                    "   :show-inheritance:",
                    "",
                ]
            )

    # Add functions
    if members["functions"]:
        for func_name in members["functions"]:
            full_name = f"{module_name}.{func_name}"
            lines.extend(
                [
                    f".. autofunction:: {full_name}",
                    "",
                ]
            )

    # Write the file
    with open(rst_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated {rst_filename}")


def generate_package_rst(
    package_name: str,
    output_dir: Path,
    submodules: list[str],
    subpackages: list[str],
) -> None:
    """
    Generate RST file for a package with toctree of submodules.

    Parameters
    ----------
    package_name : str
        Full package name
    output_dir : Path
        Directory to write RST files
    submodules : list
        List of submodule names
    subpackages : list
        List of subpackage names
    """
    rst_filename = output_dir / f"{package_name}.rst"

    # Format package name for title
    title = f"{package_name} package"
    underline = "=" * len(title)

    lines = [
        title,
        underline,
        "",
        f".. automodule:: {package_name}",
        "   :members:",
        "   :undoc-members:",
        "   :show-inheritance:",
        "",
    ]

    # Add subpackages section
    if subpackages:
        lines.extend(
            [
                "Subpackages",
                "-----------",
                "",
                ".. toctree::",
                "   :maxdepth: 1",
                "",
            ]
        )
        for subpkg in sorted(subpackages):
            lines.append(f"   {subpkg}")
        lines.append("")

    # Add submodules section
    if submodules:
        lines.extend(
            [
                "Submodules",
                "----------",
                "",
                ".. toctree::",
                "   :maxdepth: 1",
                "",
            ]
        )
        for submod in sorted(submodules):
            lines.append(f"   {submod}")
        lines.append("")

    # Write the file
    with open(rst_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated {rst_filename}")


def walk_package(
    package_name: str,
    output_dir: Path,
    max_depth: int = 10,
) -> None:
    """
    Recursively walk through a package and generate RST files.

    Parameters
    ----------
    package_name : str
        Package name to document
    output_dir : Path
        Output directory for RST files
    max_depth : int
        Maximum recursion depth
    """
    if max_depth <= 0:
        return

    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        print(f"Warning: Could not import {package_name}: {e}")
        return

    if not hasattr(package, "__path__"):
        # It's a module, not a package
        members = get_module_members(package_name)
        generate_module_rst(package_name, output_dir, members)
        return

    submodules = []
    subpackages = []

    # Walk through the package
    for importer, modname, ispkg in pkgutil.iter_modules(
        package.__path__, prefix=f"{package_name}."
    ):
        if ispkg:
            subpackages.append(modname)
            # Recursively process subpackage
            walk_package(modname, output_dir, max_depth - 1)
        else:
            submodules.append(modname)
            # Generate RST for module
            members = get_module_members(modname)
            generate_module_rst(modname, output_dir, members)

    # Generate package RST with toctree
    generate_package_rst(package_name, output_dir, submodules, subpackages)


def main():
    """Main entry point."""
    # Get paths
    script_dir = Path(__file__).parent
    output_dir = script_dir / "source" / "api"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating RST files in {output_dir}")
    print("=" * 70)

    # Generate documentation for mt_metadata package
    walk_package("mt_metadata", output_dir)

    print("=" * 70)
    print("Done! RST files generated with autopydantic_model directives.")
    print(f"Run 'make html' to build the documentation.")


if __name__ == "__main__":
    main()
