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
# =============================================================================
# Imports
# =============================================================================
import sys
import re
import logging

from mt_metadata import ACCEPTED_STYLES, REQUIRED_KEYS
from mt_metadata.utils.exceptions import MTValidatorError

# =============================================================================
# validator functions
# =============================================================================
def validate_header(header, attribute=False):
    """
    validate header to make sure it includes the required keys:
        * 'attribute'
        * 'type'
        * 'required'
        * 'style'
        * 'units'

    :param header: list of header names
    :type header: list

    :param attribute: include attribute in test or not
    :type attribute: [ True | False ]

    :return: validated header
    :rtype: list

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
            msg = (
                f"Keys is not correct, must include {required_keys}"
                + f". Currently has {header}"
            )
            raise MTValidatorError(msg)
    return header


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

    :param name: name name
    :type name: string
    :return: valid name name
    :rtype: string

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

    :param value: required value
    :type value: [ string | bool ]
    :return: validated required value
    :rtype: boolean

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

    :param value: required type
    :type value: [ type | string ]
    :return: validated type
    :rtype: string

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
        elif "h5py_reference" in value.lower():
            return value

        else:
            msg = "'type' must be type [ int | float " + f"| str | bool ].  Not {value}"
            raise MTValidatorError(msg)
    else:
        msg = (
            "'type' must be type [ int | float "
            + f"| str | bool ] or string.  Not {value}"
        )
        raise MTValidatorError(msg)


def validate_units(value):
    """
    Validate units

    ..todo:: make a list of acceptable unit names

    :param value: unit value to be validated
    :type value: string

    :return: validated units
    :rtype: string

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

    :param value: style to be validated
    :type value: string
    :return: validated style
    :rtype: string

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
    
    :param description: detailed description of an attribute
    :type description: str
    :return: validated string of description
    :rtype: string

    """
    if not isinstance(description, str):
        msg = f"Description must be a string, not {type(description)}"
        raise MTValidatorError(msg)

    return description


def validate_options(options):
    """
    turn options into a list of strings
    
    :param options: DESCRIPTION
    :type options: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

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
    :param alias: DESCRIPTION
    :type alias: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

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
    
    :param example: DESCRIPTION
    :type example: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    if not isinstance(example, str):
        example = "{0}".format(example)
    return example


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
        if isinstance(value_dict, logging.Logger):
            return value_dict
        msg = f"Input must be a dictionary, not {type(value_dict)}"
        raise MTValidatorError(msg)

    header = validate_header(list(value_dict.keys()))
    # loop over validating functions in this module
    for key in header:
        try:
            value_dict[key] = getattr(sys.modules[__name__], f"validate_{key}")(
                value_dict[key]
            )
        except KeyError:
            raise KeyError("Could not find {key} for validator {__name__}")

    return value_dict
