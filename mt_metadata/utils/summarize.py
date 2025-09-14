# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:52:35 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

This module provides functionality to summarize metadata standards from both
legacy BaseDict-based objects and modern Pydantic v2 MetadataBase objects.

The main functions are:
- summarize_timeseries_standards(): Legacy function for BaseDict objects
- summarize_pydantic_standards(): New function for Pydantic v2 MetadataBase objects
- extract_metadata_fields_from_pydantic(): Extract fields from individual Pydantic classes
- summarize_standards(): Unified interface supporting both legacy and Pydantic systems

Example usage:
    # For Pydantic v2 objects (recommended)
    >>> df = summarize_standards(metadata_type="pydantic")

    # Extract fields from individual class
    >>> from mt_metadata.timeseries import Survey
    >>> fields = extract_metadata_fields_from_pydantic(Survey)

    # Get BaseDict-compatible summary
    >>> summary = summarize_pydantic_standards()
"""
from typing import get_args, get_origin, Union

# =============================================================================
# Imports
# =============================================================================
import numpy as np
import pandas as pd
from loguru import logger

from mt_metadata import __version__
from mt_metadata.base import BaseDict, MetadataBase
from mt_metadata.utils.validators import validate_name


# =============================================================================


def extract_metadata_fields_from_pydantic(metadata_class):
    """
    Extract field information from a Pydantic v2 MetadataBase class definition
    and convert it to a format compatible with BaseDict.

    :param metadata_class: A MetadataBase class (not instance)
    :type metadata_class: type
    :return: Dictionary with field information compatible with BaseDict
    :rtype: dict
    """
    if not (
        isinstance(metadata_class, type) and issubclass(metadata_class, MetadataBase)
    ):
        raise TypeError(
            f"Object must be a MetadataBase class, got {type(metadata_class)}"
        )

    field_dict = {}
    model_fields = metadata_class.model_fields

    for field_name, field_info in model_fields.items():
        # Extract basic field information
        field_data = {
            "type": _get_field_type(field_info),
            "required": _get_field_required(field_info),
            "style": _get_field_style(field_info),
            "units": _get_field_units(field_info),
            "description": _get_field_description(field_info),
            "options": _get_field_options(field_info),
            "alias": _get_field_alias(field_info),
            "example": _get_field_example(field_info),
            "default": _get_field_default(field_info),
        }

        field_dict[field_name] = field_data

    return field_dict


def _get_field_type(field_info):
    """Extract type information from Pydantic field"""
    annotation = field_info.annotation

    # Handle Union types (e.g., str | int)
    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)
        if origin is Union or (
            hasattr(origin, "__name__") and origin.__name__ == "UnionType"
        ):
            # For Union types, get the first non-None type
            for arg in args:
                if arg is not type(None):
                    annotation = arg
                    break

    # Map Python types to string representations that BaseDict now accepts
    type_mapping = {
        str: "string",
        int: "integer",
        float: "float",
        bool: "boolean",
        list: "list",  # Now supported by BaseDict
        dict: "dict",  # Now supported by BaseDict
    }

    if annotation in type_mapping:
        return type_mapping[annotation]
    elif hasattr(annotation, "__name__"):
        # For custom classes, map to appropriate types that BaseDict accepts
        name = annotation.__name__.lower()
        if name.endswith("enum"):
            return "string"  # Enums are essentially strings with options
        elif "list" in name or "array" in name:
            return "list"  # Use list type
        elif "dict" in name:
            return "dict"  # Use dict type
        elif (
            "comment" in name
            or "citation" in name
            or any(x in name for x in ["person", "location", "fdsn"])
        ):
            return "object"  # Complex objects as object type
        else:
            return "object"  # Default to object for complex types
    else:
        return "string"  # Default fallback


def _get_field_required(field_info):
    """Extract required status from Pydantic field"""
    # Check json_schema_extra first
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        if "required" in field_info.json_schema_extra:
            return field_info.json_schema_extra["required"]

    # Check if field has a default value - if no default, it's required
    from pydantic_core import PydanticUndefined

    return field_info.default is PydanticUndefined and (
        field_info.default_factory is None
        or field_info.default_factory is PydanticUndefined
    )


def _get_field_style(field_info):
    """Extract style information from Pydantic field"""
    # Check for pattern in field constraints
    if hasattr(field_info, "pattern") and field_info.pattern:
        return f"pattern: {field_info.pattern}"

    # Check json_schema_extra for style
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        if "style" in field_info.json_schema_extra:
            return field_info.json_schema_extra["style"]

    return "free form"


def _get_field_units(field_info):
    """Extract units information from Pydantic field"""
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        if "units" in field_info.json_schema_extra:
            return field_info.json_schema_extra["units"]
    return None


def _get_field_description(field_info):
    """Extract description from Pydantic field"""
    return getattr(field_info, "description", "No description available")


def _get_field_options(field_info):
    """Extract options/choices from Pydantic field"""
    # Check for enum or choices in constraints
    options = []

    # Check for enum type
    annotation = field_info.annotation
    if hasattr(annotation, "__members__"):  # Enum type
        options = list(annotation.__members__.keys())

    # Check json_schema_extra for options
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        if "options" in field_info.json_schema_extra:
            schema_options = field_info.json_schema_extra["options"]
            if isinstance(schema_options, (list, tuple)):
                options.extend(schema_options)

    return options  # Return empty list instead of None to avoid validation errors


def _get_field_alias(field_info):
    """Extract alias from Pydantic field"""
    alias = getattr(field_info, "alias", None)
    return alias if alias is not None else ""


def _get_field_example(field_info):
    """Extract example from Pydantic field"""
    examples = getattr(field_info, "examples", None)
    if hasattr(examples, "__iter__") and not isinstance(examples, str):
        if examples and len(examples) > 0:
            return str(examples[0])
    else:
        return str(examples) if examples is not None else ""


def _get_field_default(field_info):
    """Extract default value from Pydantic field"""
    from pydantic_core import PydanticUndefined

    if field_info.default is not PydanticUndefined:
        # Convert to string for storage
        default_val = field_info.default
        if isinstance(default_val, (str, int, float, bool)):
            return str(default_val)
        elif default_val is None:
            return ""
        else:
            return str(default_val)
    elif (
        field_info.default_factory is not None
        and field_info.default_factory is not PydanticUndefined
    ):
        try:
            default_val = field_info.default_factory()
            if isinstance(default_val, (str, int, float, bool)):
                return str(default_val)
            else:
                return str(type(default_val).__name__)
        except:
            return ""
    return ""


def collect_basemodel_objects(module: str) -> dict[type[MetadataBase], str]:
    """
    Collect all MetadataBase subclasses from a given module.

    :param module: The module to inspect (e.g., 'mt_metadata.timeseries')
    :type module: str
    :return: Dictionary mapping class objects to their names
    :rtype: dict[type[MetadataBase], str]
    """
    import importlib
    import inspect

    mod = importlib.import_module(f"mt_metadata.{module}")
    basemodel_classes = {}
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if issubclass(obj, MetadataBase) and obj is not MetadataBase:
            basemodel_classes[obj] = validate_name(name)
    return basemodel_classes


def summarize_pydantic_standards(module: str = "timeseries") -> BaseDict:
    """
    Summarize the standards for metadata using Pydantic v2 MetadataBase classes.
    Similar to summarize_timeseries_standards but works with the new Pydantic structure.

    :return: BaseDict object containing summarized field information
    :rtype: BaseDict
    """
    metadata_classes = collect_basemodel_objects(module)

    summary_dict = BaseDict()

    for metadata_class, class_name in metadata_classes.items():
        try:
            class_fields = extract_metadata_fields_from_pydantic(metadata_class)
            summary_dict.add_dict(class_fields, class_name)
        except Exception as e:
            logger.exception(e)
            logger.warning(f"Could not process {class_name} fields: {e}")

    return summary_dict


def summary_to_array(summary_dict):
    """
    Summarize all metadata from a summarized dictionary of standards

    :param summary_dict: Dictionary of summarized standards
    :type summary_dict: dict
    :return: numpy structured array
    :rtype: np.array

    """
    dtype = np.dtype(
        [
            ("attribute", "U72"),
            ("type", "U15"),
            ("required", np.bool_),
            ("style", "U72"),
            ("units", "U32"),
            ("description", "U300"),
            ("options", "U150"),
            ("alias", "U72"),
            ("example", "U72"),
        ]
    )

    entries = np.zeros(len(summary_dict.keys()) + 1, dtype=dtype)
    entries[0]["attribute"] = "mt_metadata.standards.version"
    entries[0]["description"] = f"Metadata standards version {__version__}"
    entries[0]["type"] = "string"
    entries[0]["style"] = "free form"
    count = 1
    for key, v_dict in summary_dict.items():
        entries[count]["attribute"] = key
        for dkey in dtype.names[1:]:
            value = v_dict[dkey]

            if isinstance(value, list):
                if len(value) == 0:
                    value = ""

                else:
                    value = ",".join(["{0}".format(ii) for ii in value])
            if value is None:
                value = ""

            entries[count][dkey] = value
        count += 1

    return entries


def summarize_standards(module="timeseries", csv_fn=None):
    """

    Summarize standards into a numpy array and write a csv if specified

    :param metadata_type: [ timeseries | pydantic ], defaults to "timeseries"
    :type metadata_type: string, optional
    :param csv_fn: full path to write a csv file, defaults to None
    :type csv_fn: string or Path, optional
    :return: structured numpy array
    :rtype: :class:`numpy.ndarray`

    """

    summary_dict = summarize_pydantic_standards(module)
    summary_df = pd.DataFrame(summary_to_array(summary_dict))

    if csv_fn:
        summary_df.to_csv(csv_fn, index=False)

    return summary_df
