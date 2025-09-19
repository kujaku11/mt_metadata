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
from mt_metadata.base.helpers import write_block


FN_PATH = Path(__file__).parent.joinpath("source")
# =============================================================================


def to_caps(name):
    """
    convert class name into mixed upper case

    :param name: DESCRIPTION
    :type name: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    return "".join(name.replace("_", " ").title().split())


def write_attribute_table_file(obj, stem):
    """
    Write an attribute table for the given metadata class

    :param level: DESCRIPTION
    :type level: TYPE
    :param stem: DESCRIPTION
    :type stem: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    lines = [".. role:: red", ".. role:: blue", ".. role:: navy", ""]

    lines += [f"{to_caps(obj._class_name)}"]
    lines += ["=" * len(lines[-1])]
    lines += ["", ""]

    for key, k_field in obj.get_all_fields().items():
        if k_field.json_schema_extra["required"]:
            k_field.json_schema_extra["required"] = ":red:`True`"
        else:
            k_field.json_schema_extra["required"] = ":blue:`False`"
        lines += write_block(key, k_field)

    fn = FN_PATH.joinpath(f"{stem}_{obj._class_name}.rst")
    with fn.open(mode="w") as fid:
        fid.write("\n".join(lines))

    return fn


def write_metadata_standards(module_name, stem):
    """
    write a file for each metadata class in module

    :param module_name: DESCRIPTION
    :type module_name: TYPE
    :param stem: DESCRIPTION
    :type stem: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

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


def update_main_index_rst(generated_index_files):
    """
    Update the main index.rst file to ensure all generated _index files
    are present in their appropriate toctree sections.

    Parameters
    ----------
    generated_index_files : list
        List of generated index file stems (without .rst extension)
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
