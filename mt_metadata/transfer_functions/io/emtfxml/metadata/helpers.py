# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 19:53:04 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from xml.etree import cElementTree as et

# =============================================================================


def _read_single(cls, root_dict, key):
    try:
        setattr(cls, key, root_dict[key])
    except KeyError:
        cls.logger.debug("no description in xml")


def _write_single(cls, parent, key, value, attributes={}):
    element = et.SubElement(parent, cls._capwords(key), attributes)
    if value is not None:
        element.text = str(value)
    return element


def _read_element(cls, root_dict, element_name):
    try:
        value = root_dict[element_name]
        element_dict = {element_name: value}
        getattr(cls, element_name).from_dict(element_dict)

    except KeyError:
        print(f"No {element_name} in EMTF XML")
        cls.logger.debug(f"No {element_name} in EMTF XML")


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


def _capwords(value):
    """
    convert to capwords, could use string.capwords, but this seems
    easy enough

    :param value: DESCRIPTION
    :type value: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    return value.replace("_", " ").title().replace(" ", "")


def _convert_tag_to_capwords(element):
    """
    convert back to capwords representation for the tag

    :param element: DESCRIPTION
    :type element: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """

    for item in element.iter():
        item.tag = _capwords(item.tag)

    return element
