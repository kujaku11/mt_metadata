# -*- coding: utf-8 -*-
"""
=======================
schema
=======================

Convenience Classes and Functions to deal with the base metadata standards
described by the csv file.

The hope is that only the csv files will need to be changed as the standards
are modified.  The attribute dictionaries are stored in ATTRICT

Created on Wed Apr 29 11:11:31 2020

@author: jpeacock
"""
import re

# =============================================================================
# Imports
# =============================================================================
import sys
from collections.abc import Iterable

import numpy as np
from loguru import logger
from pydantic import HttpUrl

from mt_metadata import ACCEPTED_STYLES, REQUIRED_KEYS
from mt_metadata.utils.exceptions import MTSchemaError, MTValidatorError


# from mt_metadata.common.comment import Comment


# =============================================================================
# validator functions
# =============================================================================


def validate_doi(value: str | HttpUrl | None) -> HttpUrl | None:
    """
    Validate a DOI string.

    Parameters
    ----------
    value : str
        The DOI string to validate.

    Returns
    -------
    str
        The validated DOI string.

    Raises
    ------
    ValueError
        If the DOI string is not valid.
    """
    if value is None:
        return None
    elif isinstance(value, str):
        if value == "":
            return None
        if value.startswith("10."):
            value = f"https://doi.org/{value}"
        elif value.startswith("doi:"):
            value = f"https://doi.org/{value.replace('doi:', '')}"
        value = HttpUrl(value)
    elif isinstance(value, HttpUrl):
        pass
    # Check if the URL starts with a valid DOI prefix
    if not value.unicode_string().startswith("https://doi.org/"):
        if not value.unicode_string().startswith("https://dx.doi.org/"):
            raise ValueError(f"Invalid DOI: {value}")

    return value


# def validate_comments(comments: str | Comment | None) -> Comment | None:
#     """
#     Validate comments string.

#     Parameters
#     ----------
#     comments : str | None
#         The comments to validate.

#     Returns
#     -------
#     str | None
#         The validated comments string or None if empty.
#     """
#     if isinstance(comments, str):
#         return Comment(value=comments)  # type: ignore
#     return comments


def validate_header(header, attribute=False):
    """
    validate header to make sure it includes the required keys:
        * 'attribute'
        * 'type'
        * 'required'
        * 'style'
        * 'units'

    Parameters
    ----------
    header : list
        list of header names
    attribute : bool, optional
        include attribute in test or not, by default False

    Returns
    -------
    list
        validated header
    """
    if not isinstance(header, list):
        msg = "input header must be a list, not {type(header)}"
        raise MTValidatorError(msg)

    if attribute:
        if sorted(header) != sorted(REQUIRED_KEYS):
            msg = (
                f"Keys is not correct, must include {REQUIRED_KEYS}"
                + f". Currently has {header}"
            )
            raise MTValidatorError(msg)
    else:
        required_keys = [key for key in REQUIRED_KEYS if key != "attribute"]
        if sorted(header) != sorted(required_keys):
            missing_keys = [x for x in required_keys if x not in header]
            msg = (
                f"Keys is not correct, must include {required_keys}\n"
                + f". Currently has {header}\n"
                + f"Need to add keys: {missing_keys}"
            )
            raise MTValidatorError(msg)
    return header


def validate_name(name):
    """
    validate the name to conform to the standards
    name must be:

        * all lower case {a-z; 1-9}
        * must start with a letter
        * categories are separated by '.'
        * words separated by '_'

    {object}.{name_name}

    '/' will be replaced with '.'
    converted to all lower case

    Parameters
    ----------
    name : str
        name name

    Returns
    -------
    str
        valid name name
    """
    if not isinstance(name, str):
        msg = f"Attribute name must be a string, not {type(name)}"
        raise MTValidatorError(msg)

    original = str(name)

    if re.match("^[0-9]", name):
        msg = f"Attribute name cannot start with a number, {original}"
        raise MTValidatorError(msg)

    if "/" in name:
        name = name.replace("/", ".")

    if re.search("[A-Z].*?", name):
        name = "_".join(re.findall(".[^A-Z]*", name))
        name = name.replace("._", ".")
        name = name.lower()

    if original != name:
        msg = "input name {0} converted to {1} following MTH5 standards"

    return name


def validate_station_name(name: str | int | float) -> str:
    """
    validate station name to conform to general standards

    - must be a string
    - must only contain letters, numbers, and underscores

    Parameters
    ----------
    name : str | int | float
        The station name to validate

    Returns
    -------
    str
        The validated station name

    Raises
    ------
    MTValidatorError
        If name is not a string or contains invalid characters
    """
    name = str(name).strip()
    original = str(name)

    # Replace spaces with underscores
    name = name.replace(" ", "_").replace("-", "_")

    # Test if string contains only letters, numbers, and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", name):
        msg = f"Station name '{original}' contains invalid characters. Only letters, numbers, and underscores are allowed."
        raise MTValidatorError(msg)

    return name


def validate_attribute(name):
    """
    validate the name to conform to the standards
    name must be:

        * all lower case {a-z; 1-9}
        * must start with a letter
        * categories are separated by '.'
        * words separated by '_'

    {object}.{name_name}

    '/' will be replaced with '.'
    converted to all lower case

    Parameters
    ----------
    name : str
        name name

    Returns
    -------
    str
        valid name name
    """
    if not isinstance(name, str):
        msg = f"Attribute name must be a string, not {type(name)}"
        raise MTValidatorError(msg)

    original = str(name)

    if re.match("^[0-9]", name):
        msg = f"Attribute name cannot start with a number, {original}"
        raise MTValidatorError(msg)

    if "/" in name:
        name = name.replace("/", ".")

    if re.search("[A-Z].*?", name):
        name = "_".join(re.findall(".[^A-Z]*", name))
        name = name.replace("._", ".")
        name = name.lower()

    if original != name:
        msg = "input name {0} converted to {1} following MTH5 standards"

    return name


def validate_required(value):
    """
    Validate required, must be True or False

    Parameters
    ----------
    value : str or bool
        required value

    Returns
    -------
    bool
        validated required value
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() in ["false"]:
            return False
        elif value.lower() in ["true"]:
            return True
        else:
            msg = "Required value must be True or False, not {value}"
            raise MTValidatorError(msg)
    else:
        msg = "Required value must be True or False, not {type(value)}"
        raise MTValidatorError(msg)


def validate_type(value):
    """
    Validate required type. Must be:
        * str
        * float
        * int
        * bool
        * list
        * dict
        * object

    Parameters
    ----------
    value : type or str
        required type

    Returns
    -------
    str
        validated type
    """
    if isinstance(value, type):
        value = "{0}".format(value).replace("<class", "").replace(">", "")

    if isinstance(value, str):
        value = value.replace("<class", "").replace(">", "")
        if "int" in value.lower():
            return "integer"
        elif "float" in value.lower():
            return "float"
        elif "str" in value.lower():
            return "string"
        elif "bool" in value.lower():
            return "boolean"
        elif "list" in value.lower() or "array" in value.lower():
            return "list"
        elif "dict" in value.lower():
            return "dict"
        elif "object" in value.lower():
            return "object"
        elif "h5py_reference" in value.lower():
            return value

        else:
            msg = (
                "'type' must be type [ int | float "
                + f"| str | bool | list | dict | object ].  Not {value}"
            )
            raise MTValidatorError(msg)
    else:
        msg = (
            "'type' must be type [ int | float "
            + f"| str | bool | list | dict | object ] or string.  Not {value}"
        )
        raise MTValidatorError(msg)


def validate_units(value):
    """
    Validate units

    ..todo:: make a list of acceptable unit names

    Parameters
    ----------
    value : str
        unit value to be validated

    Returns
    -------
    str
        validated units
    """
    if value is None:
        return value
    if isinstance(value, str):
        if value.lower() in ["none", "empty", ""]:
            return None
        else:
            return value.lower()
    else:
        msg = f"'units' must be a string or None, not {type(value)}"
        raise MTValidatorError(msg)


def validate_style(value):
    """
    Validate string style

    ..todo:: make list of accepted style formats

    Parameters
    ----------
    value : str
        style to be validated

    Returns
    -------
    str
        validated style
    """
    # if None then return the generic name style
    if value is None:
        return "name"

    if not isinstance(value, str):
        msg = f"'value' must be a string. Not {type(value)}"
        raise MTValidatorError(msg)

    if value.lower() not in ACCEPTED_STYLES:
        msg = f"style {value} unknown, must be in {ACCEPTED_STYLES}"
        raise MTValidatorError(msg)

    return value.lower()


def validate_description(description):
    """
    make sure the description is a string

    Parameters
    ----------
    description : str
        detailed description of an attribute

    Returns
    -------
    str
        validated string of description
    """
    if not isinstance(description, str):
        msg = f"Description must be a string, not {type(description)}"
        raise MTValidatorError(msg)

    return description


def validate_options(options):
    """
    turn options into a list of strings

    Parameters
    ----------
    options : TYPE
        DESCRIPTION

    Returns
    -------
    TYPE
        DESCRIPTION
    """
    if isinstance(options, str):
        options = options.replace("[", "").replace("]", "").strip().split("|")
        names = []
        for name in options:
            if not name.lower() in ["none", ""]:
                names.append(name.strip())
        options = names

    elif isinstance(options, (list, tuple)):
        options = [str(option) for option in options]
    elif isinstance(options, (float, int, bool)):
        options = ["{0}".format(options)]

    else:
        msg = "Option type not understood {type(options)}"
        raise MTValidatorError(msg)
    return options


def validate_alias(alias):
    """
    validate alias names

    Parameters
    ----------
    alias : TYPE
        DESCRIPTION

    Returns
    -------
    TYPE
        DESCRIPTION
    """

    if isinstance(alias, str):
        alias = alias.replace("[", "").replace("]", "").strip().split("|")
        names = []
        for name in alias:
            if not name.lower() in ["none", ""]:
                names.append(name.strip())
        alias = names

    elif isinstance(alias, (list, tuple)):
        alias = [str(option) for option in alias]
    elif isinstance(alias, (float, int, bool)):
        alias = [f"{alias}"]

    else:
        msg = f"Alias type not understood {alias}"
        raise MTValidatorError(msg)
    return alias


def validate_example(example):
    """
    Validate example values

    Parameters
    ----------
    example : TYPE
        DESCRIPTION

    Returns
    -------
    TYPE
        DESCRIPTION
    """
    if not isinstance(example, str):
        example = "{0}".format(example)
    return example


def validate_default(value_dict):
    """
    validate default value

    Parameters
    ----------
    value_dict : TYPE
        DESCRIPTION

    Returns
    -------
    TYPE
        DESCRIPTION
    """

    if value_dict["required"]:
        if value_dict["default"] in [None]:
            if "list" in value_dict["style"]:
                value = []
            elif "date" in value_dict["style"] or "time" in value_dict["style"]:
                value = "1980-01-01T00:00:00+00:00"
            elif "controlled" in value_dict["style"]:
                if "other" in value_dict["options"]:
                    value = None
                else:
                    value = value_dict["options"][0]
            else:
                if value_dict["type"] in ["integer", "float", int, float]:
                    value = 0
                elif value_dict["type"] in ["string", str]:
                    value = "none"
                elif value_dict["type"] in ["bool", bool]:
                    value = False
                elif value_dict["type"] in ["h5py_reference"]:
                    value = None
        else:
            value = validate_value_type(
                value_dict["default"], value_dict["type"], value_dict["style"]
            )

    else:
        if "date" in value_dict["style"] or "time" in value_dict["style"]:
            value = "1980-01-01T00:00:00+00:00"
        else:
            value = None
    return value


def validate_value_type(value, v_type, style=None):
    """
    validate type from standards

    Parameters
    ----------
    value : TYPE
        DESCRIPTION
    v_type : TYPE
        DESCRIPTION
    style : TYPE, optional
        DESCRIPTION, by default None

    Returns
    -------
    TYPE
        DESCRIPTION
    """

    # if the value is a metadata type skip cause the individual components
    # will be validated separately
    if "metadata" in str(type(value)):
        return value
    # return if the value is None, this may need to change in the future
    # if an empty list or something else should be returned
    if not isinstance(value, (list, tuple, np.ndarray)):
        if value in [None, "None", "none", "unknown"]:
            return None
    # hack to get around h5py reference types, in the future will need
    # a more robust test.
    if v_type == "h5py_reference":
        return value

    # return value if the value type is not defined.
    if v_type is None:
        msg = (
            "standards data type is unknown, if you want to "
            + "propogate this attribute using to_dict, to_json or "
            + "to_series, you need to add attribute description using "
            + "class function add_base_attribute."
        )
        logger.warning(msg)
        return value

    # if not a python type but a string organize into a dictionary
    if not isinstance(v_type, type) and isinstance(v_type, str):
        type_dict = {
            "string": str,
            "integer": int,
            "float": float,
            "boolean": bool,
            "list": list,
            "dict": dict,
            "object": object,
        }
        v_type = type_dict[validate_type(v_type)]
    else:
        msg = "v_type must be a string or type not {0}".format(v_type)

    # check style for a list, if it is split the string
    if style:
        if "list" in style and isinstance(value, str):
            delimeter = " "
            if value.count(",") > 0:
                delimeter = ","
            elif value.strip().count(" ") > 0:
                delimeter = " "
            elif value.count(";") > 0:
                delimeter = ";"
            value = value.replace("[", "").replace("]", "").split(delimeter)
            value = [ss.strip() for ss in value]

    # if value is not of v_type
    if not isinstance(value, v_type):
        msg = "value=%s must be %s not %s"
        # if the value is a string, convert to appropriate type
        if isinstance(value, str):
            if v_type is int:
                try:
                    if value.lower() in ["none", "nan", ""]:
                        return None
                    return int(value)
                except ValueError:
                    raise MTSchemaError(msg, value, v_type, type(value))
            elif v_type is float:
                try:
                    return float(value)
                except ValueError:
                    raise MTSchemaError(msg, value, v_type, type(value))
            elif v_type is bool:
                if value.lower() in ["false", "0"]:
                    return False
                elif value.lower() in ["true", "1"]:
                    return True
                else:
                    raise MTSchemaError(msg, value, v_type, type(value))
            elif v_type is str:
                return value

        # if a number convert to appropriate type
        elif isinstance(value, (int, np.int_, np.int64, np.int32, np.int16, np.int8)):
            if v_type is float:
                return float(value)
            elif v_type is str:
                return "{0:.0f}".format(value)
            return int(value)

        # if a number convert to appropriate type
        elif isinstance(value, (float, np.float16, np.float32, np.float64)):
            if v_type is int:
                return int(value)
            elif v_type is str:
                return f"{value}"
            return float(value)

        # if a list convert to appropriate entries to given type
        elif isinstance(value, Iterable):
            if v_type is str:
                if isinstance(value, np.ndarray):
                    value = value.astype(np.str_)
                value = [f"{v}".replace("'", "").replace('"', "") for v in value]
            elif v_type is int:
                value = [int(float(v)) for v in value]
            elif v_type is float:
                value = [float(v) for v in value]
            elif v_type is bool:
                value_list = []
                for v in value:
                    if v in [True, "true", "True", "TRUE", 1, "1"]:
                        value_list.append(True)
                    elif v in [False, "false", "False", "FALSE", 0, "0"]:
                        value_list.append(False)
                value = value_list
            return value

        elif isinstance(value, (np.bool_)):
            return bool(value)

        else:
            raise MTSchemaError(msg, value, v_type, type(value))
    else:
        return value


def validate_value_dict(value_dict):
    """
    Validate an input value dictionary

    Must be of the form:
        {'type': str, 'required': True, 'style': 'name', 'units': units}

    :param value_dict: DESCRIPTION
    :type value_dict: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    if not isinstance(value_dict, dict):
        if isinstance(value_dict, type(logger)):
            return value_dict
        msg = f"Input must be a dictionary, not {type(value_dict)}"
        raise MTValidatorError(msg)

    header = validate_header(list(value_dict.keys()))
    # loop over validating functions in this module
    for key in header:
        if key == "default":
            continue
        try:
            value_dict[key] = getattr(sys.modules[__name__], f"validate_{key}")(
                value_dict[key]
            )
        except KeyError:
            raise KeyError("Could not find {key} for validator {__name__}")

    # need to validate the default value after all other keys have been validated
    value_dict["default"] = validate_default(value_dict)

    return value_dict
