# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 19:53:04 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict
from xml.etree import cElementTree as et

from loguru import logger
from pydantic import HttpUrl

from mt_metadata import NULL_VALUES
from mt_metadata.base.helpers import element_to_string
from mt_metadata.utils.validators import validate_attribute


# =============================================================================


def _get_attributes(cls) -> list[str]:
    return [f for f in cls.__dict__.keys() if f[0] != "_" and f not in ["logger"]]


def _capwords(value: str) -> str:
    """
    Convert a string to capwords format.

    Could use string.capwords, but this seems
    easy enough

    Parameters
    ----------
    value : str
        The input string to convert.

    Returns
    -------
    str
        The converted string in capwords format.
    """

    if value.count("_") > 0:
        return value.replace("_", " ").title().replace(" ", "")
    elif sum(1 for c in value if c.isupper()) == 0:
        return value.title()

    return value


def _convert_tag_to_capwords(element: et.Element) -> et.Element:
    """
    Convert back to capwords representation for the tag.

    Parameters
    ----------
    element : et.Element
        The XML element to convert.

    Returns
    -------
    et.Element
        The converted XML element.
    """

    for item in element.iter():
        if item.tag != "value":
            item.tag = _capwords(item.tag)

    return element


def _read_single(cls: type, root_dict: dict, key: str) -> None:
    """
    Read a single value from a dictionary into a class attribute.

    Parameters
    ----------
    cls : type
        The class to update.
    root_dict : dict
        The dictionary containing the data.
    key : str
        The key to read from the dictionary.
    """

    try:
        setattr(cls, key, root_dict[key])
    except KeyError:
        logger.debug("no description in xml")


def _write_single(
    parent: et.Element, key: str, value: str, attributes: dict = {}
) -> et.Element:
    """
    Write a single value to an XML element.

    Parameters
    ----------
    parent : et.Element
        The parent XML element to append the new element to.
    key : str
        The key for the new XML element.
    value : str
        The value for the new XML element.
    attributes : dict, optional
        Additional attributes for the new XML element, by default {}

    Returns
    -------
    et.Element
        The newly created XML element.
    """

    element = et.SubElement(parent, _capwords(key), attributes)
    if value not in NULL_VALUES:
        element.text = str(value)
    return element


def _read_element(cls: type, root_dict: dict, element_name: str) -> None:
    """
    Read an XML element into a class instance.

    Parameters
    ----------
    cls : type
        The class to update.
    root_dict : dict
        The dictionary containing the data.
    element_name : str
        The name of the XML element to read.
    """

    try:
        element_dict = {element_name: root_dict[element_name]}
        cls.from_dict(element_dict)

    except KeyError:
        logger.warning(f"No {element_name} in EMTF XML")


def _convert_keys_to_lower_case(root_dict: dict) -> OrderedDict:
    """
    Convert all keys in the dictionary to lower case.

    Parameters
    ----------
    root_dict : dict
        The dictionary to convert.

    Returns
    -------
    OrderedDict
        The converted dictionary with lower case keys.
    """

    res = OrderedDict()
    if isinstance(root_dict, (dict, OrderedDict)):
        for key in root_dict.keys():
            new_key = validate_attribute(key)
            res[new_key] = root_dict[key]
            if isinstance(res[new_key], (dict, OrderedDict, list)):
                res[new_key] = _convert_keys_to_lower_case(res[new_key])
    elif isinstance(root_dict, list):
        res = []
        for item in root_dict:
            item = _convert_keys_to_lower_case(item)
            res.append(item)
    return res


def _remove_null_values(element: et.Element, replace: str = "") -> et.Element:
    """
    Remove null values from an XML element.

    Parameters
    ----------
    element : et.Element
        The XML element to process.
    replace : str, optional
        The value to replace null values with, by default "".

    Returns
    -------
    et.Element
        The processed XML element.
    """

    for item in element.iter():
        if item.text in NULL_VALUES:
            if replace == False:
                element.remove(item)
            else:
                item.text = replace
        for key, value in item.attrib.items():
            if value in NULL_VALUES:
                if replace == False:
                    element.remove(item)
                else:
                    item.attrib[key] = replace

    return element


def validate_doi(value: str) -> str:
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
        if value.startswith("10."):
            value = f"https://doi.org/{value}"
        elif value.startswith("doi:"):
            value = f"https://doi.org/{value.replace('doi:', '')}"
        elif not value.startswith("https://doi.org/"):
            raise ValueError(f"Invalid DOI: {value}")
        value = HttpUrl(value)
    elif isinstance(value, HttpUrl):
        if not value.startswith("https://doi.org/"):
            raise ValueError(f"Invalid DOI: {value}")

    return value


def to_xml(cls, string=False, required=True, order=None) -> str | et.Element:
    """
    Convert a class instance to an XML element.

    Parameters
    ----------
    string : bool, optional
        Whether to return the XML as a string, by default False
    required : bool, optional
        Whether the XML element is required, by default True
    order : list, optional
        The order of attributes to include, by default None

    Returns
    -------
    str | et.Element
        The XML representation of the class instance.
    """

    root = et.Element(cls.__class__.__name__)

    if order is None:
        order = _get_attributes(cls)
    for attr in order:
        c_attr = getattr(cls, attr)
        if c_attr is None:
            continue
        if hasattr(c_attr, "to_xml") and callable(getattr(c_attr, "to_xml")):
            element = c_attr.to_xml(required=required)
            if isinstance(element, list):
                for item in element:
                    root.append(item)
            else:
                root.append(element)
        elif isinstance(c_attr, list):
            if len(c_attr) == 0:
                continue
            if hasattr(c_attr[0], "to_xml") and callable(getattr(c_attr[0], "to_xml")):
                # If the first item has a to_xml method, assume all items do
                # and call to_xml on each item
                for item in c_attr:
                    if isinstance(item, et.Element):
                        root.append(item)
                    else:
                        root.append(item.to_xml(required=required))
            elif isinstance(c_attr[0], str):
                # If the first item is a string, write it directly
                value = " ".join(c_attr)
                _write_single(root, attr, value)

        else:
            _write_single(root, attr, c_attr)

    if not string:
        return root
    else:
        return element_to_string(_remove_null_values(root))
