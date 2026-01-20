# -*- coding: utf-8 -*-
"""

Make a block for each metadata keyword so that a user can search the documents
easier.

Created on Thu Jul 30 17:01:34 2020

:author: Jared Peacock

:license: MIT

"""


import importlib
import inspect

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path

from pydantic import ValidationError

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import wrap_description


FN_PATH = Path(__file__).parent.joinpath("source")
# =============================================================================


def write_block_from_dict(
    key: str,
    field_dict: dict[str, str | bool | None],
    c1: int = 45,
    c2: int = 45,
    c3: int = 15,
) -> list[str]:
    """
    Write a documentation block for a metadata field from its serializable dictionary.

    Creates a reStructuredText formatted table block for a single metadata field,
    including its description, type information, units, examples, and required status.

    Parameters
    ----------
    key : str
        The field name/key to document.
    field_dict : dict[str, str | bool | None]
        Serializable field information dictionary containing keys:
        - 'type': Type annotation string
        - 'description': Field description text
        - 'examples': Example values
        - 'required': Whether field is required (bool)
        - 'units': Unit of measurement
    c1 : int, optional
        Column 1 width in characters, by default 45.
    c2 : int, optional
        Column 2 (description) width in characters, by default 45.
    c3 : int, optional
        Column 3 (examples) width in characters, by default 15.

    Returns
    -------
    list[str]
        List of formatted reStructuredText lines for the field documentation block.
    """
    if len(key) > c1 - 4:
        c1 = len(key) + 6

    line = "       | {0:<{1}}| {2:<{3}} | {4:<{5}}|"
    hline = "       +{0}+{1}+{2}+".format(
        "-" * (c1 + 1), "-" * (c2 + 2), "-" * (c3 + 1)
    )
    mline = "       +{0}+{1}+{2}+".format(
        "=" * (c1 + 1), "=" * (c2 + 2), "=" * (c3 + 1)
    )
    section = f":navy:`{key}`"

    lines = [
        section,
        "~" * len(section),
        "",
        ".. container::",
        "",
        "   .. table::",
        "       :class: tight-table",
        f"       :widths: {c1} {c2} {c3}",
        "",
        hline,
        line.format(f"**{key}**", c1, "**Description**", c2, "**Example**", c3),
        mline,
    ]

    # Extract field info from the serializable dictionary
    type_str = field_dict.get("type", "")
    description = field_dict.get("description", "")
    examples = field_dict.get("examples", "")
    required = field_dict.get("required", "False")
    units = field_dict.get("units", "")

    # Wrap text for columns
    t_lines = wrap_description(type_str, c1 - 10)
    d_lines = wrap_description(description, c2)
    e_lines = wrap_description(examples, c3)

    # line 1 is with the entry
    lines.append(
        line.format(
            f"**Required**: {required}",
            c1,
            d_lines[0],
            c2,
            e_lines[0],
            c3,
        )
    )
    # line 2 skip an entry in the first column
    lines.append(line.format("", c1, d_lines[1], c2, e_lines[1], c3))
    # line 3 with type
    lines.append(
        line.format(
            f"**Type**: {t_lines[0]}",
            c1,
            d_lines[2],
            c2,
            e_lines[2],
            c3,
        )
    )
    # line 4 skip type
    lines.append(line.format(t_lines[1], c1, d_lines[3], c2, e_lines[3], c3))

    # line 5 with units
    lines.append(
        line.format(
            f"**Units**: {units}",
            c1,
            d_lines[4],
            c2,
            e_lines[4],
            c3,
        )
    )
    # fill up the rest of the description
    for ii, d_line in enumerate(d_lines[5:], 5):
        try:
            lines.append(line.format("", c1, d_line, c2, e_lines[ii], c3))
        except IndexError:
            lines.append(line.format("", c1, d_line, c2, "", c3))
    lines.append(hline)
    lines.append("")

    return lines


# =============================================================================


def to_caps(name: str) -> str:
    """
    Convert a class name to title case with spaces removed.

    Replaces underscores with spaces, converts to title case, then removes
    all spaces to create a CamelCase string.

    Parameters
    ----------
    name : str
        The class name to convert (e.g., 'my_class_name').

    Returns
    -------
    str
        Title-cased name with spaces removed (e.g., 'MyClassName').

    Examples
    --------
    >>> to_caps('my_metadata_class')
    'MyMetadataClass'
    """

    return "".join(name.replace("_", " ").title().split())


def write_attribute_table_file(obj: MetadataBase, stem: str) -> Path:
    """
    Write a reStructuredText file documenting all attributes of a metadata class.

    Creates a .rst file containing formatted documentation tables for all fields
    in the provided metadata object. The output file is named using the pattern:
    {stem}_{obj._class_name}.rst

    Parameters
    ----------
    obj : MetadataBase
        An instance of a metadata class to document. The instance's fields will
        be extracted using `get_all_fields()`.
    stem : str
        File name prefix/stem for the output file (e.g., 'base', 'ts', 'tf').

    Returns
    -------
    Path
        Path to the written .rst documentation file.

    Notes
    -----
    - Required fields are marked with red 'True', optional fields with blue 'False'
    - Output files are written to the FN_PATH directory (docs/source)
    """

    lines = [".. role:: red", ".. role:: blue", ".. role:: navy", ""]

    lines += [f"{to_caps(obj._class_name)}"]
    lines += ["=" * len(lines[-1])]
    lines += ["", ""]

    for key, field_dict in obj.get_all_fields().items():
        # field_dict is now a serializable dictionary, not a FieldInfo object
        # Convert required flag to colored text
        required = field_dict.get("required", False)
        if required:
            field_dict["required"] = ":red:`True`"
        else:
            field_dict["required"] = ":blue:`False`"

        lines += write_block_from_dict(key, field_dict)

    fn = FN_PATH.joinpath(f"{stem}_{obj._class_name}.rst")
    with fn.open(mode="w") as fid:
        fid.write("\n".join(lines))

    return fn


def write_metadata_standards(module_name: str, stem: str) -> list[Path]:
    """
    Generate documentation files for all MetadataBase classes in a module.

    Discovers all classes in the specified module, instantiates those that are
    MetadataBase subclasses, and generates .rst documentation files for each.

    Parameters
    ----------
    module_name : str
        Fully qualified module name to scan (e.g., 'mt_metadata.timeseries').
    stem : str
        File name prefix for generated documentation files.

    Returns
    -------
    list[Path]
        List of Path objects for all successfully written documentation files.

    Notes
    -----
    - Classes requiring constructor arguments are skipped with a message
    - Only classes that are instances of MetadataBase are documented
    - Handles ValidationError exceptions from pydantic models
    """
    mod = importlib.import_module(module_name)

    mod_dict = dict(inspect.getmembers(mod, inspect.isclass))
    fn_list = []
    for obj in mod_dict.values():
        try:
            init_obj = obj()
            if isinstance(init_obj, MetadataBase):
                fn_list.append(write_attribute_table_file(init_obj, stem))
        except (TypeError, ValidationError):
            print(f"Skipping {obj}...")
            # likely a required argument in __init__
    return fn_list


def update_main_index_rst(generated_index_files: list[str]) -> None:
    """
    Update the main index.rst to include all generated documentation index files.

    Ensures that all generated *_index.rst files are properly referenced in the
    appropriate toctree sections of the main documentation index. Adds missing
    references while preserving existing structure.

    Parameters
    ----------
    generated_index_files : list[str]
        List of generated index file stems without .rst extension
        (e.g., ['base_index', 'ts_index', 'tf_index']).

    Notes
    -----
    - Modifies docs/index.rst in place if changes are needed
    - Maps index files to appropriate documentation sections:
      * Base Metadata Object
      * Common Metadata Objects
      * Feature Metadata
      * Processing Metadata
      * Time Series Metadata
      * Transfer Functions
    - Prints summary of changes made and validation results
    - Does not modify file if all references already exist
    """
    main_index_path = Path(__file__).parent.joinpath("index.rst")

    if not main_index_path.exists():
        print(f"Warning: {main_index_path} not found, skipping index update")
        return

    # Read the current index.rst content
    with open(main_index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Define the mapping of index files to their section captions
    section_mappings = {
        "Base Metadata Object": ["base_index"],
        "Common Metadata Objects": ["common_index"],
        "Feature Metadata": ["features_index", "weights_index"],
        "Processing Metadata": [
            "processing_index",
            "processing_aurora_index",
            "processing_fcs_index",
        ],
        "Time Series Metadata": ["ts_index", "ts_filter_index", "stationxml_index"],
        "Transfer Functions": [
            "tf_index",
            "tf_base_index",
            "tf_emtfxml_index",
            "tf_edi_index",
            "tf_zmm_index",
            "tf_jfile_index",
            "tf_zonge_index",
        ],
    }

    updated_content = []
    i = 0
    changes_made = 0

    while i < len(lines):
        line = lines[i]
        updated_content.append(line)

        # Check if this line contains a toctree caption we care about
        if ":caption:" in line:
            for section_name, expected_files in section_mappings.items():
                if section_name in line:
                    # Found a section we need to update
                    # Add lines until we get to the end of the toctree
                    i += 1
                    toctree_lines = []
                    existing_files = []

                    # Collect existing toctree entries
                    while i < len(lines):
                        current_line = lines[i]
                        if current_line.strip() == "":
                            # Empty line might end the toctree
                            if i + 1 < len(lines) and not lines[i + 1].startswith(
                                "    "
                            ):
                                # Next non-empty line doesn't start with spaces, end of toctree
                                break
                        elif current_line.startswith(
                            "    source/"
                        ) and current_line.strip().endswith("_index"):
                            # This is an index file entry
                            file_stem = current_line.strip().replace("source/", "")
                            existing_files.append(file_stem)
                        elif (
                            current_line.startswith("    ")
                            or current_line.strip() == ""
                        ):
                            # Part of this toctree
                            pass
                        else:
                            # Not part of this toctree anymore
                            i -= 1  # Back up one line
                            break

                        toctree_lines.append(current_line)
                        i += 1

                    # Check which expected files are missing from existing files
                    missing_files = []
                    for expected_file in expected_files:
                        if (
                            expected_file in generated_index_files
                            and expected_file not in existing_files
                        ):
                            missing_files.append(expected_file)

                    # Add missing files to the toctree
                    if missing_files:
                        print(f"  Adding to '{section_name}': {missing_files}")
                        # Find the right place to insert (before non-index entries or at the end)
                        insert_pos = len(toctree_lines)
                        for j, toctree_line in enumerate(toctree_lines):
                            if (
                                toctree_line.startswith("    source/")
                                and not toctree_line.strip().endswith("_index")
                                and "notebooks" not in toctree_line
                            ):
                                insert_pos = j
                                break

                        # Insert the missing files
                        for missing_file in missing_files:
                            toctree_lines.insert(
                                insert_pos, f"    source/{missing_file}\n"
                            )
                            insert_pos += 1

                        changes_made += len(missing_files)

                    # Add all toctree lines to updated content
                    updated_content.extend(toctree_lines)
                    break

        i += 1

    # Write back to file if changes were made
    if changes_made > 0:
        with open(main_index_path, "w", encoding="utf-8") as f:
            f.writelines(updated_content)
        print(
            f"Updated {main_index_path} - added {changes_made} missing index file references"
        )
    else:
        print(
            f"No updates needed for {main_index_path} - all index files already present"
        )

    # Verify all generated files are properly referenced
    missing_overall = []
    for idx_file in generated_index_files:
        content_str = "".join(updated_content)
        if f"source/{idx_file}" not in content_str:
            missing_overall.append(idx_file)

    if missing_overall:
        print(
            f"Warning: These generated files are still not referenced: {missing_overall}"
        )
    else:
        print(
            f"✓ All {len(generated_index_files)} generated index files are properly referenced"
        )


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    module_dict = {
        "mt_metadata.base": ("base", "Base Metadata Objects"),
        "mt_metadata.common": ("common", "Common Metadata Objects"),
        "mt_metadata.features": ("features", "Features"),
        "mt_metadata.features.weights": (
            "weights",
            "Weights and Weighting Specifications",
        ),
        "mt_metadata.processing": ("processing", "Processing Steps"),
        "mt_metadata.processing.aurora": (
            "processing_aurora",
            "Aurora Processing",
        ),
        "mt_metadata.processing.fourier_coefficients": (
            "processing_fcs",
            "Fourier Coefficients",
        ),
        "mt_metadata.timeseries": ("ts", "Time Series"),
        "mt_metadata.timeseries.filters": ("ts_filter", "Time Series Filters"),
        "mt_metadata.timeseries.stationxml": (
            "stationxml",
            "MT and StationXML Translation",
        ),
        "mt_metadata.transfer_functions": ("tf_base", "Transfer Function Base"),
        "mt_metadata.transfer_functions.tf": ("tf", "Transfer Function"),
        "mt_metadata.transfer_functions.io.emtfxml.metadata": (
            "tf_emtfxml",
            "EMTF XML",
        ),
        "mt_metadata.transfer_functions.io.edi.metadata": ("tf_edi", "EDI"),
        "mt_metadata.transfer_functions.io.zfiles.metadata": (
            "tf_zmm",
            "Z-Files",
        ),
        "mt_metadata.transfer_functions.io.jfiles.metadata": (
            "tf_jfile",
            "J-Files",
        ),
        "mt_metadata.transfer_functions.io.zonge.metadata": (
            "tf_zonge",
            "Zonge AVG",
        ),
    }

    generated_index_files = []

    for module, stem in module_dict.items():
        fn_list = write_metadata_standards(module, stem[0])

        lines = [
            ".. role:: red",
            ".. role:: blue",
            ".. role:: navy",
            stem[1],
            "=" * 30,
            "",
            ".. toctree::",
            "    :maxdepth: 1",
            "    :caption: Metadata Definitions",
            "",
        ]
        lines += [f"{' '*4}{f.stem}" for f in fn_list]
        lines.append("")

        index_filename = f"{stem[0]}_index"
        generated_index_files.append(index_filename)

        with open(FN_PATH.joinpath(f"{index_filename}.rst"), "w") as fid:
            fid.write("\n".join(lines))

    # Update the main index.rst file with all generated index files
    print(f"\nGenerated {len(generated_index_files)} index files:")
    for idx_file in generated_index_files:
        print(f"  - {idx_file}.rst")

    print("\nUpdating main index.rst file...")
    update_main_index_rst(generated_index_files)
