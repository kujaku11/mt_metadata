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

from mt_metadata import NULL_VALUES
from mt_metadata.base.helpers import element_to_string
from mt_metadata.utils.validators import validate_attribute


# =============================================================================


def _get_attributes(cls):
    return [f for f in cls.__dict__.keys() if f[0] != "_" and f not in ["logger"]]


def _capwords(value):
    """
    convert to capwords, could use string.capwords, but this seems
    easy enough

    :param value: DESCRIPTION
    :type value: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    if value.count("_") > 0:
        return value.replace("_", " ").title().replace(" ", "")
    elif sum(1 for c in value if c.isupper()) == 0:
        return value.title()

    return value


def _convert_tag_to_capwords(element):
    """
    convert back to capwords representation for the tag

    :param element: DESCRIPTION
    :type element: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    for item in element.iter():
        if item.tag != "value":
            item.tag = _capwords(item.tag)

    return element


def _read_single(cls, root_dict, key):
    try:
        setattr(cls, key, root_dict[key])
    except KeyError:
        logger.debug("no description in xml")


def _write_single(parent, key, value, attributes={}):
    element = et.SubElement(parent, _capwords(key), attributes)
    if value not in NULL_VALUES:
        element.text = str(value)
    return element


def _read_element(cls, root_dict, element_name):
    try:
        element_dict = {element_name: root_dict[element_name]}
        cls.from_dict(element_dict)

    except KeyError:
        logger.warning(f"No {element_name} in EMTF XML")


def _convert_keys_to_lower_case(root_dict):
    """
    Convert the key names to lower case and separated by _ if
    needed

    :param root_dict: DESCRIPTION
    :type root_dict: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

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


def _remove_null_values(element, replace=""):
    """
    remove null values

    :param element: DESCRIPTION
    :type element: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

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


def to_xml(cls, string=False, required=True, order=None) -> str | et.Element:
    """ """

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
