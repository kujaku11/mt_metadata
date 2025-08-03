# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:37:52 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
import json
import logging

# =============================================================================
# Imports
# =============================================================================
import textwrap
from collections import defaultdict, OrderedDict
from collections.abc import MutableMapping
from operator import itemgetter
from typing import Any, Dict
from xml.dom import minidom
from xml.etree import cElementTree as et

import numpy as np
from loguru import logger
from pydantic import BaseModel


# from mt_metadata.utils.units import get_unit_object


filter_descriptions = {
    "zpk": "poles and zeros filter",
    "coefficient": "coefficient filter",
    "time delay": "time delay filter",
    "fir": "finite impaulse response filter",
    "fap": "frequency amplitude phase lookup table",
    "frequency response table": "frequency amplitude phase lookup table",
    "base": "base filter",
}

# =============================================================================
# write doc strings
# =============================================================================


def get_all_fields(model: BaseModel) -> Dict[str, Any]:
    """
    Recursively get all fields in a BaseModel, including nested BaseModel fields.

    Parameters
    ----------
    model : BaseModel
        metadata basemodel

    Returns
    -------
    Dict[str, Any]
        dictionary keyed by attributes. Will be nested for BaseModel fields.
        For simple fields, returns the FieldInfo object.
        For BaseModel fields, returns a nested dictionary of their fields.
    """

    fields = {}

    # Use __pydantic_fields__ instead of model_fields (which is deprecated)
    for field_name, field_info in model.__pydantic_fields__.items():
        # Skip deprecated fields
        if field_info.deprecated is not None:
            continue

        annotation = field_info.annotation

        # Handle different annotation types
        field_type = _extract_base_type(annotation)

        if field_type and _is_basemodel_subclass(field_type):
            # special case for MTime, which is a Basemodel, but we only want the value not all
            # the fields.
            if "MTime" == field_type.__name__:
                fields[field_name] = field_info
                continue
            # It's a BaseModel, recursively get its fields
            try:
                nested_instance = field_type()
                fields[field_name] = get_all_fields(nested_instance)
            except Exception:
                # If we can't instantiate it, just include the field info
                fields[field_name] = field_info
        else:
            # It's a simple field, include the field info
            fields[field_name] = field_info

    return fields


def _extract_base_type(annotation):
    """
    Extract the base type from a complex annotation like Union, Optional, List, etc.

    Parameters
    ----------
    annotation : type
        The type annotation to extract from

    Returns
    -------
    type or None
        The base type if found, None otherwise
    """
    from typing import get_args, get_origin

    # First check for generic types (Union, List, etc.)
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is not None:
        if origin is list or (
            hasattr(origin, "__name__") and origin.__name__ == "list"
        ):
            # For List types, get the element type
            if args:
                return _extract_base_type(args[0])
        elif hasattr(origin, "__name__") and origin.__name__ in ["UnionType", "Union"]:
            # For Union types, find the first non-None type
            for arg in args:
                if arg != type(None):
                    return _extract_base_type(arg)
        elif hasattr(origin, "__name__") and origin.__name__ in ["dict", "Dict"]:
            # For Dict types, we don't recurse into them
            return None

    # Handle direct types (only if not a generic type)
    if hasattr(annotation, "__mro__") and annotation != type(None):
        return annotation

    return None


def _is_basemodel_subclass(cls):
    """
    Check if a class is a subclass of BaseModel.

    Parameters
    ----------
    cls : type
        The class to check

    Returns
    -------
    bool
        True if cls is a BaseModel subclass, False otherwise
    """
    import inspect

    try:
        from pydantic import BaseModel

        return (
            inspect.isclass(cls)
            and issubclass(cls, BaseModel)
            and hasattr(cls, "__pydantic_fields__")
        )
    except (TypeError, AttributeError):
        return False


def wrap_description(description, column_width):
    """
    split a description into separate lines
    """
    d_lines = textwrap.wrap(description, column_width)
    if len(d_lines) < 11:
        d_lines += [""] * (11 - len(d_lines))
    return d_lines


def validate_c1(attr_dict, c1):
    """

    :param attr_dict: DESCRIPTION
    :type attr_dict: TYPE
    :param c1: DESCRIPTION
    :type c1: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    try:
        max_c1 = max([len(key) for key in attr_dict.keys()])

        if max_c1 > (c1 - 4):
            c1 = max_c1 + 6
    except ValueError:
        pass

    return c1


def write_lines(attr_dict, c1=45, c2=45, c3=15):
    """
    Takes the attribute dictionary from the json and parses it into a table
    Returns a string representation of this table.  This overwrites the doc.

    :param attr_dict: attribute dictionary
    :type attr_dict: dict
    :param c1: cloumn 1 width, defaults to 45
    :type c1: integer, optional
    :param c2: column 2 width, defaults to 45
    :type c2: integer, optional
    :param c3: column 3 width, defaults to 15
    :type c3: integer, optional
    :return: doc string
    :rtype: string

    """
    c1 = validate_c1(attr_dict, c1)

    line = "       | {0:<{1}}| {2:<{3}} | {4:<{5}}|"
    hline = "       +{0}+{1}+{2}+".format(
        "-" * (c1 + 1), "-" * (c2 + 2), "-" * (c3 + 1)
    )
    mline = "       +{0}+{1}+{2}+".format(
        "=" * (c1 + 1), "=" * (c2 + 2), "=" * (c3 + 1)
    )

    lines = [
        hline,
        line.format("**Metadata Key**", c1, "**Description**", c2, "**Example**", c3),
        mline,
    ]

    for key, entry in attr_dict.items():
        if isinstance(entry, logging.Logger):
            continue
        d_lines = wrap_description(entry["description"], c2)
        e_lines = wrap_description(entry["example"], c3)
        # line 1 is with the entry
        lines.append(line.format(f"**{key}**", c1, d_lines[0], c2, e_lines[0], c3))
        # line 2 skip an entry in the
        lines.append(line.format("", c1, d_lines[1], c2, e_lines[1], c3))
        # line 3 required
        lines.append(
            line.format(
                f"Required: {entry['required']}",
                c1,
                d_lines[2],
                c2,
                e_lines[2],
                c3,
            )
        )
        # line 4 blank
        lines.append(line.format("", c1, d_lines[3], c2, e_lines[3], c3))

        # line 5 units
        lines.append(
            line.format(f"Units: {entry['units']}", c1, d_lines[4], c2, e_lines[4], c3)
        )

        # line 6 blank
        lines.append(line.format("", c1, d_lines[5], c2, e_lines[5], c3))

        # line 7 type
        lines.append(
            line.format(f"Type: {entry['type']}", c1, d_lines[6], c2, e_lines[6], c3)
        )

        # line 8 blank
        lines.append(line.format("", c1, d_lines[7], c2, e_lines[7], c3))

        # line 9 type
        lines.append(
            line.format(f"Style: {entry['style']}", c1, d_lines[8], c2, e_lines[8], c3)
        )

        # line 10 blank
        lines.append(line.format("", c1, d_lines[9], c2, e_lines[9], c3))

        default = [entry["default"]] + [""] * 5
        if len(str(entry["default"])) > c1 - 15:
            default = [""] + wrap_description(entry["default"], c1)

        # line 9 type
        lines.append(
            line.format(
                f"**Default**: {default[0]}",
                c1,
                d_lines[8],
                c2,
                e_lines[8],
                c3,
            )
        )

        # line 10 blank
        lines.append(line.format(default[1], c1, d_lines[9], c2, e_lines[9], c3))

        # line 9 type
        lines.append(line.format(default[2], c1, d_lines[10], c2, e_lines[10], c3))

        # line 10 blank
        if len(d_lines) > 11:
            lines.append(line.format(default[3], c1, d_lines[11], c2, "", c3))
            for index, d_line in enumerate(d_lines[12:], 4):
                try:
                    lines.append(line.format(default[index], c1, d_line, c2, "", c3))
                except IndexError:
                    lines.append(line.format("", c1, d_line, c2, "", c3))

        # long default value
        if len(default) > 7:
            lines.append(line.format(default[3], c1, "", c2, "", c3))
            for index, d_line in enumerate(default[4:], 12):
                try:
                    lines.append(line.format(d_line, c1, d_lines[index], c2, "", c3))
                except IndexError:
                    lines.append(line.format(d_line, c1, "", c2, "", c3))
        lines.append(hline)
    return "\n".join(lines)


def write_block(key, attr_dict, c1=45, c2=45, c3=15):
    """

    :param key: key to write from attr dict
    :type key: string
    :param attr_dict: attribute dictionary
    :type attr_dict: dict
    :param c1: column 1 width, defaults to 45
    :type c1: int, optional
    :param c2: column 2 width, defaults to 45
    :type c2: int, optional
    :param c3: column 3 width, defaults to 15
    :type c3: int, optional
    :return: list of lines
    :rtype: list

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
        line.format(f"**{key}**", c1, "**Description**", c2, "**Example**", c3),
        mline,
    ]

    d_lines = wrap_description(attr_dict["description"], c2)
    e_lines = wrap_description(attr_dict["example"], c3)
    # line 1 is with the entry
    lines.append(
        line.format(
            f"**Required**: {attr_dict['required']}",
            c1,
            d_lines[0],
            c2,
            e_lines[0],
            c3,
        )
    )
    # line 2 skip an entry in the
    lines.append(line.format("", c1, d_lines[1], c2, e_lines[1], c3))
    # line 3 required
    lines.append(
        line.format(
            f"**Units**: {attr_dict['units']}",
            c1,
            d_lines[2],
            c2,
            e_lines[2],
            c3,
        )
    )
    # line 4 blank
    lines.append(line.format("", c1, d_lines[3], c2, e_lines[3], c3))

    # line 5 units
    lines.append(
        line.format(
            f"**Type**: {attr_dict['type']}",
            c1,
            d_lines[4],
            c2,
            e_lines[4],
            c3,
        )
    )

    # line 6 blank
    lines.append(line.format("", c1, d_lines[5], c2, e_lines[5], c3))

    # line 7 type
    lines.append(
        line.format(
            f"**Style**: {attr_dict['style']}",
            c1,
            d_lines[6],
            c2,
            e_lines[6],
            c3,
        )
    )

    # line 8 blank
    lines.append(line.format("", c1, d_lines[7], c2, e_lines[7], c3))

    default = [attr_dict["default"]] + [""] * 5
    if len(str(attr_dict["default"])) > c1 - 15:
        default = [""] + wrap_description(attr_dict["default"], c1)

    # line 9 type
    lines.append(
        line.format(
            f"**Default**: {default[0]}",
            c1,
            d_lines[8],
            c2,
            e_lines[8],
            c3,
        )
    )

    # line 10 blank
    lines.append(line.format(default[1], c1, d_lines[9], c2, e_lines[9], c3))

    # line 9 type
    lines.append(line.format(default[2], c1, d_lines[10], c2, e_lines[10], c3))

    # line 10 blank
    if len(d_lines) > 11:
        lines.append(line.format(default[3], c1, d_lines[11], c2, "", c3))
        for index, d_line in enumerate(d_lines[12:], 4):
            try:
                lines.append(line.format(default[index], c1, d_line, c2, "", c3))
            except IndexError:
                lines.append(line.format("", c1, d_line, c2, "", c3))

    # long default value
    if len(default) > 7:
        lines.append(line.format(default[3], c1, "", c2, "", c3))
        for index, d_line in enumerate(default[4:], 12):
            try:
                lines.append(line.format(d_line, c1, d_lines[index], c2, "", c3))
            except IndexError:
                lines.append(line.format(d_line, c1, "", c2, "", c3))

    lines.append(hline)
    lines.append("")

    return lines


# code to convert ini_dict to flattened dictionary
# default seperater '_'
def flatten_dict(meta_dict, parent_key=None, sep="."):
    """

    :param meta_dict: DESCRIPTION
    :type meta_dict: TYPE
    :param parent_key: DESCRIPTION, defaults to None
    :type parent_key: TYPE, optional
    :param sep: DESCRIPTION, defaults to '.'
    :type sep: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    """
    items = []
    for key, value in meta_dict.items():
        if parent_key:
            new_key = f"{parent_key}{sep}{key}"
        else:
            new_key = key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def flatten_list(x_list):
    """
    Flatten a nested list
    flatten = lambda l: [item for sublist in l for item in sublist]

    Returns
    -------
    None.

    """

    flat_list = [item for sublist in x_list for item in sublist]

    return flat_list


def recursive_split_dict(key, value, remainder, sep="."):
    """
    recursively split a dictionary

    :param key: DESCRIPTION
    :type key: TYPE
    :param value: DESCRIPTION
    :type value: TYPE
    :param remainder: DESCRIPTION
    :type remainder: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    key, *other = key.split(sep, 1)
    if other:
        recursive_split_dict(other[0], value, remainder.setdefault(key, {}))
    else:
        remainder[key] = value


def get_by_alias(model, alias_name):
    # Find the field name that corresponds to the given alias
    # Use __pydantic_fields__ instead of model_fields (which is deprecated)
    for field_name, field_info in model.__pydantic_fields__.items():
        if field_info.alias == alias_name:
            return getattr(model, field_name)
    return None


# def get_alias_key(model, key: str) -> str:
#     """
#     Try to find an alias for a field name in a Pydantic BaseModel

#     Parameters
#     ----------
#     model : BaseModel
#         The Pydantic model to search for the field
#     key : str
#         The field name to find the alias for

#     Returns
#     -------
#     str or None
#         The alias name if found, None otherwise
#     """
#     try:
#         field_info = model.__pydantic_fields__.get(key)
#         if field_info.validation_alias:

#         if field_info and field_info.alias:
#             return field_info.alias
#         return key  # Return the original key if no alias found
#     except (AttributeError, KeyError):
#         return key  # Return the original key if any errors occur


def recursive_split_getattr(base_object, name, sep="."):
    key, *other = name.split(sep, 1)

    if other:
        base_object = getattr(base_object, key)
        value, prop = recursive_split_getattr(base_object, other[0])
    else:
        # with Pydantic, if the attribute does not exist an attribute error
        # will be raised, which is desired. The only issue will be if the
        # attribute is an alias, then TODO create a get from alias method.
        try:
            value = getattr(base_object, key)
        except AttributeError:
            value = None
            prop = False
        try:
            if isinstance(getattr(type(base_object), key), property):
                prop = True
        except AttributeError:
            prop = False
    return value, prop


def recursive_split_setattr(base_object, name, value, sep=".", skip_validation=False):
    """
    Recursively split a name and set the value of the last key. Recursion splits on the separator present in the name.

    :param base_object: The object having its attribute set, or a "parent" object in the recursive/nested scenario
    :type base_object: object
    :param name: The name of the attribute to set
    :type name: str
    :param value: The value to set the attribute to
    :type value: any
    :param sep: The separator to split the name on, defaults to "."
    :type sep: str, optional
    :param skip_validation: Whether to skip validation/parse of the attribute, defaults to False
    :type skip_validation: Optional[bool]

    :return: None
    :rtype: NoneType

    """
    key, *other = name.split(sep, 1)

    if other:
        base_object = getattr(base_object, key)
        recursive_split_setattr(base_object, other[0], value)
    else:
        # if the value is a list or dict then we need to add accordingly
        if isinstance(value, list):
            if len(value) == 0:
                value = []
            elif isinstance(value[0], (dict, OrderedDict)):
                new_list = []
                for obj_dict in value:
                    obj_key = list(obj_dict.keys())[0]
                    try:
                        obj = base_object._objects_included[obj_key]()
                        obj.from_dict(obj_dict)
                        new_list.append(obj)
                    except KeyError:
                        raise KeyError(
                            f"Could not find {obj_key} in {base_object._objects_included}"
                        )
                value = new_list

        setattr(base_object, key, value)


def structure_dict(meta_dict, sep="."):
    """

    :param meta_dict: DESCRIPTION
    :type meta_dict: TYPE
    :param sep: DESCRIPTION, defaults to '.'
    :type sep: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    """
    structured_dict = {}
    for key, value in meta_dict.items():
        recursive_split_dict(key, value, structured_dict, sep=sep)
    return structured_dict


def get_units(name, attr_dict):
    """ """
    try:
        units = attr_dict["json_schema_extra"]["units"]
        if not isinstance(units, str):
            units = "{0}".format(units)
    except KeyError:
        units = None
    if units in [None, "None", "none"]:
        return None
    return units


def get_type(name, attr_dict):
    """ """
    try:
        v_type = attr_dict[name]["type"]
        if v_type in ["string", str, "str", "String"]:
            v_type = None
    except KeyError:
        v_type = None
    return v_type


def recursive_split_xml(element, item, base, name, attr_dict=None):
    """ """
    key = None
    if isinstance(item, dict):
        for key, value in item.items():
            attr_name = ".".join([base, key])

            sub_element = et.SubElement(element, key)
            recursive_split_xml(sub_element, value, attr_name, key, attr_dict)
    elif isinstance(item, (tuple, list)):
        for ii in item:
            sub_element = et.SubElement(element, "item")
            recursive_split_xml(sub_element, ii, base, name, attr_dict)
    elif isinstance(item, str):
        element.text = item
    elif isinstance(item, (float, int, type(None))):
        element.text = str(item)
    else:
        # if the value is an hdf5 reference make it a string
        if "reference" in str(type(item)).lower():
            element.text = str(item)
        else:
            raise ValueError("Value cannot be {0}".format(type(item)))
    if attr_dict:
        units = get_units(base, attr_dict)
        if units:
            element.set("units", str(units))
        # v_type = get_type(base, attr_dict)
        # if v_type:
        #     element.set("type", v_type)
    return element, name


def dict_to_xml(meta_dict, attr_dict=None):
    """
    Assumes dictionary is structured {class:{attribute_dict}}

    :param meta_dict: DESCRIPTION
    :type meta_dict: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    class_name = list(meta_dict.keys())[0]
    root = et.Element(class_name)

    for key, value in meta_dict[class_name].items():
        element = et.SubElement(root, key)
        recursive_split_xml(element, value, key, key, attr_dict)
    return root


def element_to_dict(element):
    """

    .. todo:: Add way to read in attritues like units and validate them.

    :param element: DESCRIPTION
    :type element: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    meta_dict = {element.tag: {} if element.attrib else None}
    children = list(element)
    if children:
        child_dict = defaultdict(list)
        for dc in map(element_to_dict, children):
            for k, v in dc.items():
                child_dict[k].append(v)
        meta_dict = {
            element.tag: {k: v[0] if len(v) == 1 else v for k, v in child_dict.items()}
        }
        if "item" in meta_dict[element.tag].keys():
            meta_dict[element.tag] = meta_dict[element.tag]["item"]
    # going to skip attributes for now, later can check them against
    # standards, neet to skip units and type
    if element.attrib:
        pop_units = False
        pop_type = False
        for k, v in element.attrib.items():
            if k in ["units"]:
                if "type" in element.attrib.keys():
                    pop_type = True
                if len(element.attrib.keys()) <= 2:
                    pop_units = True
                    continue
            if k in ["type"]:
                if len(element.attrib.keys()) <= 1:
                    if v in [
                        "float",
                        "string",
                        "integer",
                        "boolean",
                        "list",
                        "tuple",
                    ]:
                        pop_type = True
                        continue

            meta_dict[element.tag][k] = v
        if pop_units:
            element.attrib.pop("units")
        if pop_type:
            element.attrib.pop("type")
    if element.text:
        text = element.text.strip()
        if children or element.attrib:
            if text:
                if len(element.attrib.keys()) > 0:
                    meta_dict[element.tag]["value"] = text
                else:
                    meta_dict[element.tag] = text
        else:
            meta_dict[element.tag] = text
    return OrderedDict(sorted(meta_dict.items(), key=itemgetter(0)))


def element_to_string(element):
    return (
        minidom.parseString(et.tostring(element).decode())
        .toprettyxml(
            indent="    ",
            encoding="UTF-8",
        )
        .decode()
    )


# =============================================================================
# Helper function to be sure everything is encoded properly
# =============================================================================
class NumpyEncoder(json.JSONEncoder):
    """
    Need to encode numpy ints and floats for json to work
    """

    def default(self, obj):
        """

        :param obj:
        :type obj:
        :return:
        """
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray)):
            if obj.dtype == complex:
                return {"real": obj.real.tolist(), "imag": obj.imag.tolist()}
            else:
                return obj.tolist()
        # For now turn references into a generic string
        elif "h5" in str(type(obj)):
            return str(obj)
        elif hasattr(obj, "unicode_string"):
            return obj.unicode_string()
        return json.JSONEncoder.default(self, obj)


def validate_name(name, pattern=None):
    """
    Validate name

    :param name: DESCRIPTION
    :type name: TYPE
    :param pattern: DESCRIPTION, defaults to None
    :type pattern: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    """
    if name is None:
        return "unknown"
    return name.replace(" ", "_")


def requires(**requirements):
    """Decorate a function with optional dependencies.

    Parameters
    ----------
    **requirements : obj
        keywords of package name and the required object for
        a function.

    Returns
    -------
    decorated_function : function
        Original function if all soft dependencies are met, otherwise
        it returns an empty function which prints why it is not running.

    Examples
    --------
    ```
    try:
        import obspy
    except ImportError:
        obspy = None

    @requires(obspy=obspy)
    def obspy_function():
        ...
        # does something using obspy

    """
    # Check the requirements, add missing package name in the list `missing`.
    missing = []
    for key, item in requirements.items():
        if not item:
            missing.append(key)

    def decorated_function(function):
        """Wrap function."""
        if not missing:
            return function
        else:

            def passer(*args, **kwargs):
                logger.warning(f"Missing dependencies: {missing}.")
                logger.warning(f"Not running `{function.__name__}`.")

            return passer

    return decorated_function


def object_to_array(value, dtype=float):
    """
    Convert a value to a numpy array.

    Parameters
    ----------
    value : any
        The value to convert.

    Returns
    -------
    np.ndarray
        The converted numpy array.

    """
    if value is None:
        return np.empty(0)
    elif isinstance(value, (list, tuple)):
        return np.array(value, dtype=dtype)
    elif isinstance(value, np.ndarray):
        return value.astype(dtype)
    elif isinstance(value, str):
        # Handle string input (e.g., from JSON)
        try:
            value = np.fromstring(value, sep=",", dtype=dtype)
            if len(value) == 0:
                logger.warning(
                    "String input is empty or cannot parse properly, returning an empty array."
                )
            return value
        except ValueError:
            msg = (
                f"input values must be a list, tuple, or np.ndarray, not {type(value)}"
            )
            raise TypeError(msg)
    elif isinstance(value, (int, float)):
        # Handle single numeric input
        return np.array([float(value)], dtype=dtype)
    elif isinstance(value, bytes):
        # Handle bytes input (e.g., from binary files)
        try:
            return np.frombuffer(value, dtype=dtype)
        except ValueError:
            msg = (
                f"input values must be a list, tuple, or np.ndarray, not {type(value)}"
            )
            raise TypeError(msg)
    else:
        msg = f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
        raise TypeError(msg)
