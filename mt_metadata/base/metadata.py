# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:41:16 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from copy import deepcopy
from collections import OrderedDict
from operator import itemgetter
from pathlib import Path
from loguru import logger

import json
import pandas as pd
import numpy as np

from mt_metadata.utils.validators import (
    validate_attribute,
    validate_value_type,
)
from mt_metadata.utils.exceptions import MTSchemaError
from . import helpers

from mt_metadata.base.helpers import write_lines

attr_dict = {}


# =============================================================================
#  Base class that everything else will inherit
# =============================================================================


class Base:
    __doc__ = write_lines(attr_dict)
    _base_attr_loaded = False

    def __init__(self, attr_dict={}, **kwargs):
        self._changed = False

        self._class_name = validate_attribute(self.__class__.__name__)

        self.logger = logger
        self._debug = False

        # attr_dict from subclass has already been validated on json load, so
        # we shouldn't need to validate it again re-validation of the attribute
        # dictionary used to contribute to some slowness in instantiation of
        # subclasses
        self._set_attr_dict(deepcopy(attr_dict), skip_validation=True)

        for name, value in kwargs.items():
            self.set_attr_from_name(name, value, skip_validation=False)

    def _set_attr_dict(self, attr_dict, skip_validation=False):
        """
        Set attribute dictionary and variables.

        should have the proper keys.

        :param attr_dict: attribute dictionary
        :type attr_dict: dict
        :param skip_validation: skip validation/parse of the attribute dictionary
        :type skip_validation: bool

        """

        self._attr_dict = attr_dict

        for key, value_dict in attr_dict.items():
            self.set_attr_from_name(key, value_dict["default"], skip_validation)

    def __str__(self):
        """

        :return: table describing attributes
        :rtype: string

        """
        meta_dict = self.to_dict()[self._class_name.lower()]
        lines = [f"{self._class_name}:"]
        for name, value in meta_dict.items():
            lines.append(f"\t{name} = {value}")
        return "\n".join(lines)

    def __repr__(self):
        return self.to_json()

    def __eq__(self, other):
        if other in [None]:
            return False
        elif isinstance(other, (Base, dict, str, pd.Series)):
            home_dict = self.to_dict(single=True, required=False)
            if isinstance(other, Base):
                other_dict = other.to_dict(single=True, required=False)
            elif isinstance(other, dict):
                other_dict = other
            elif isinstance(other, str):
                if other.lower() in ["none", "null", "unknown"]:
                    return False
                other_dict = OrderedDict(
                    sorted(json.loads(other).items(), key=itemgetter(0))
                )
            elif isinstance(other, pd.Series):
                other_dict = OrderedDict(
                    sorted(other.to_dict().items(), key=itemgetter(0))
                )
            else:
                raise ValueError(
                    f"Cannot compare {self._class_name} with {type(other)}"
                )
            fail = False
            for key, value in home_dict.items():
                if "creation_time" in key:
                    continue
                try:
                    other_value = other_dict[key]
                    if isinstance(value, np.ndarray):
                        if value.size != other_value.size:
                            msg = f"Array sizes for {key} differ: {value.size} != {other_value.size}"
                            self.logger.info(msg)
                            fail = True
                            continue
                        if not (value == other_value).all():
                            msg = f"{key}: {value} != {other_value}"
                            self.logger.info(msg)
                            fail = True
                    elif isinstance(value, (float, int, complex)):
                        if not np.isclose(value, other_value):
                            msg = f"{key}: {value} != {other_value}"
                            self.logger.info(msg)
                            fail = True
                    else:
                        if value != other_value:
                            msg = f"{key}: {value} != {other_value}"
                            self.logger.info(msg)
                            fail = True
                except KeyError:
                    msg = "Cannot find {0} in other".format(key)
                    self.logger.info(msg)
            if fail:
                return False
            else:
                return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.get_attribute_list())

    def update(self, other, match=[]):
        """
        Update attribute values from another like element, skipping None

        :param other: other Base object
        :type other: :class:`mt_metadata.base.metadata.Base`

        """
        if not isinstance(other, type(self)):
            self.logger.warning(
                f"Cannot update {type(self)} with {type(other)}"
            )
        for k in match:
            if self.get_attr_from_name(k) != other.get_attr_from_name(k):
                msg = (
                    f"{k} is not equal {self.get_attr_from_name(k)} != "
                    f"{other.get_attr_from_name(k)}"
                )
                self.logger.error(msg)
                raise ValueError(msg)
        for k, v in other.to_dict(single=True).items():
            if hasattr(v, "size"):
                if v.size > 0:
                    self.set_attr_from_name(k, v)
            else:
                if v not in [None, 0.0, [], "", "1980-01-01T00:00:00+00:00"]:
                    self.set_attr_from_name(k, v)

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, value):
        self._changed = value

    def __deepcopy__(self, memodict={}):
        """
        Need to skip copying the logger
        need to copy properties as well.

        :return: Deep copy
        :rtype: :class:`mt_metadata.base.metadata.Base`

        """
        copied = type(self)()
        for key in self.to_dict(single=True, required=False).keys():
            try:

                copied.set_attr_from_name(
                    key, deepcopy(self.get_attr_from_name(key), memodict)
                )
            # Need the TypeError for objects that have no __reduce__ method
            # like H5 references.
            except (AttributeError, TypeError) as error:
                self.logger.debug(error)
                continue
        # need to copy and properties
        for key in self.__dict__.keys():
            if key.startswith("_"):
                test_property = getattr(self.__class__, key[1:], None)
                if isinstance(test_property, property):
                    value = getattr(self, key[1:])
                    if hasattr(value, "copy"):
                        setattr(copied, key[1:], value.copy())
                    else:
                        setattr(copied, key[1:], value)

        return copied

    def copy(self):
        """
        Copy object

        """

        return self.__deepcopy__()

    def get_attribute_list(self):
        """
        return a list of the attributes
        """

        return sorted(list(self._attr_dict.keys()))

    def attribute_information(self, name=None):
        """
        return a descriptive string of the attribute if none returns for all

        :param name: attribute name for a specifice attribute, defaults to None
        :type name: string, optional
        :return: description of the attributes or specific attribute if asked
        :rtype: string

        """

        if name:
            try:
                v_dict = OrderedDict(
                    sorted(self._attr_dict[name].items(), key=itemgetter(0))
                )
            except KeyError as error:
                msg = "{0} not attribute {1} found".format(error, name)
                self.logger.error(msg)
                raise MTSchemaError(msg)
            lines = ["{0}:".format(name)]
            for key, value in v_dict.items():
                lines.append("\t{0}: {1}".format(key, value))
        else:
            lines = []
            for name, v_dict in self._attr_dict.items():
                lines.append("{0}:".format(name))
                v_dict = OrderedDict(sorted(v_dict.items(), key=itemgetter(0)))
                for key, value in v_dict.items():
                    lines.append("\t{0}: {1}".format(key, value))
                lines.append("=" * 50)
        print("\n".join(lines))

    def _validate_name(self, name):
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
        return validate_attribute(name)

    def _validate_type(self, value, v_type, style=None):
        """
        validate type from standards

        """

        try:
            return validate_value_type(value, v_type, style=style)
        except MTSchemaError as error:
            self.logger.exception(error)
            raise MTSchemaError(error)

    def _validate_option(self, name, value, option_list):
        """
        validate the given attribute name agains possible options and check
        for aliases

        :param name: DESCRIPTION
        :type name: TYPE
        :param option_list: DESCRIPTION
        :type option_list: TYPE
        :param alias_list: DESCRIPTION
        :type alias_list: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if value is None:
            return True, False, None
        options = [ss.lower() for ss in option_list]
        other_possible = False
        if "other" in options:
            other_possible = True
        if value.lower() in options:
            return True, other_possible, None
        elif value.lower() not in options and other_possible:
            msg = (
                f"Value '{value}' not found for metadata field '{name}' in options list {option_list}, but other options"
                + f" are allowed.  Allowing {option_list} to be set to {value}."
            )
            return True, other_possible, msg
        return (
            False,
            other_possible,
            f"Value '{value}' for metadata field '{name}' not found in options list {option_list}",
        )

    def __setattr__(self, name, value):
        """
        set attribute based on metadata standards

        Something here doesnt allow other objects to be set as attributes

        """
        # skip these attribute because they are validated in the property
        # setter.
        skip_list = [
            "latitude",
            "longitude",
            "elevation",
            "start_date",
            "end_date",
            "start",
            "end",
            "applied",
            "logger",
            "changed",
            "hdf5_reference",
            "obspy_mapping",
            "surveys",
            "filters",
            "stations",
            "runs",
            "channels",
            "channels_recorded_all",
            "channels_recorded_electric"
            "channels_recorded_magnetic"
            "channels_recorded_auxiliary",
            "electrode",
            "estimates_list",
            "input_channels",
            "output_channels",
            "data_types_list",
            "info_list",
            "info_dict",
            "filters_list",
            "fn",
        ]

        if name in skip_list:
            super().__setattr__(name, value)
            return
        if not name.startswith("_"):
            # test if the attribute is a property first, if it is, then
            # it will have its own defined setter, so use that one and
            # skip validation.
            try:
                test_property = getattr(self.__class__, name, None)
                if isinstance(test_property, property):
                    self.logger.debug(
                        f"Identified {name} as property, using fset"
                    )
                    test_property.fset(self, value)
                    return
            except AttributeError:
                pass
        if hasattr(self, "_attr_dict") and not name.startswith("_"):
            self.logger.debug(f"Setting {name} to {value}")
            try:
                v_dict = self._attr_dict[name]
                v_type = self._get_standard_type(name)
                value = self._validate_type(value, v_type, v_dict["style"])
                # check options
                if v_dict["style"] == "controlled vocabulary":
                    options = v_dict["options"]
                    accept, other, msg = self._validate_option(
                        name, value, options
                    )
                    if not accept:
                        self.logger.error(msg.format(value, options))
                        raise MTSchemaError(msg.format(value, options))
                    if other and not accept:
                        self.logger.warning(msg.format(value, options, name))
                super().__setattr__(name, value)
            except KeyError as error:
                raise KeyError(error)
        else:
            super().__setattr__(name, value)

    def _get_standard_type(self, name):
        """
        helper function to get the standard type for the given name
        """
        name = self._validate_name(name)
        try:
            standards = self._attr_dict[name]
            if isinstance(standards, type(logger)):
                return None
            return standards["type"]
        except KeyError:
            if name[0] != "_":
                msg = (
                    f"{name} is not defined in the standards. "
                    " Should add attribute information with "
                    "add_base_attribute if the attribute is going to "
                    "propogate via to_dict, to_json, to_series"
                )
                self.logger.info(msg)
            return None

    def get_attr_from_name(self, name):
        """
        Access attribute from the given name.

        The name can contain the name of an object which must be separated
        by a '.' for  e.g. {object_name}.{name} --> location.latitude

        .. note:: this is a helper function for names with '.' in the name for
         easier getting when reading from dictionary.

        :param name: name of attribute to get.
        :type name: string
        :return: attribute value
        :rtype: type is defined by the attribute name

        :Example:

        >>> b = Base(**{'category.test_attr':10})
        >>> b.get_attr_from_name('category.test_attr')
        10

        """

        name = self._validate_name(name)
        v_type = self._get_standard_type(name)

        if "." in name:
            value, prop = helpers.recursive_split_getattr(self, name)
            if prop:
                return value
        else:
            value = getattr(self, name)
            try:
                if isinstance(getattr(type(self), name), property):
                    return value
            except AttributeError:
                pass
        if hasattr(value, "to_dict"):
            return value
        return self._validate_type(value, v_type)

    def setattr_skip_validation(self, name, value):
        """
        Set attribute without validation

        :param name: name of attribute
        :type name: string

        :param value: value of the new attribute
        :type value: described in value_dict

        """
        self.__dict__[name] = value

    def set_attr_from_name(self, name, value, skip_validation=False):
        """
        Helper function to set attribute from the given name.

        The name can contain the name of an object which must be separated
        by a '.' for  e.g. {object_name}.{name} --> location.latitude

        .. note:: this is a helper function for names with '.' in the name for
         easier getting when reading from dictionary.

        :param name: name of attribute to get.
        :type name: string
        :param value: attribute value
        :type value: type is defined by the attribute name
        :param skip_validation: skip validation/parse of the key-value pair
        :type skip_validation: bool

        :Example:

        >>> b = Base(**{'category.test_attr':10})
        >>> b.set_attr_from_name('category.test_attr', '10')
        >>> print(b.category.test_attr)
        '10'
        """
        if "." in name:
            try:
                helpers.recursive_split_setattr(
                    self, name, value, skip_validation=skip_validation
                )
            except AttributeError as error:
                msg = (
                    "{0} is not in the current standards.  "
                    + "To properly add the attribute use "
                    + "add_base_attribute."
                )

                self.logger.error(msg.format(name))
                raise AttributeError(error)
        else:
            if skip_validation:
                self.setattr_skip_validation(name, value)
            else:
                setattr(self, name, value)

    def add_base_attribute(self, name, value, value_dict):
        """
        Add an attribute to _attr_dict so it will be included in the
        output dictionary

        :param name: name of attribute
        :type name: string

        :param value: value of the new attribute
        :type value: described in value_dict

        :param value_dict: dictionary describing the attribute, must have keys
         ['type', 'required', 'style', 'units', 'alias', 'description',
          'options', 'example']
        :type name: string

        * type --> the data type [ str | int | float | bool ]
        * required --> required in the standards [ True | False ]
        * style --> style of the string
        * units --> units of the attribute, must be a string
        * alias --> other possible names for the attribute
        * options --> if only a few options are accepted, separated by | or
           comma.b [ option_01 | option_02 | other ]. 'other' means other options
           available but not yet defined.
        * example --> an example of the attribute

        :Example:

        >>> extra = {'type': str,
        >>> ...      'style': 'controlled vocabulary',
        >>> ...      'required': False,
        >>> ...      'units': celsius,
        >>> ...      'description': 'local temperature',
        >>> ...      'alias': ['temp'],
        >>> ...      'options': [ 'ambient', 'air', 'other'],
        >>> ...      'example': 'ambient'}
        >>> r = Run()
        >>> r.add_base_attribute('temperature', 'ambient', extra)

        """
        name = self._validate_name(name)
        self._attr_dict.update({name: value_dict})
        self.set_attr_from_name(name, value)

    def to_dict(self, nested=False, single=False, required=True):
        """
        make a dictionary from attributes, makes dictionary from _attr_list.

        :param nested: make the returned dictionary nested
        :type nested: [ True | False ] , default is False

        :param single: return just metadata dictionary -> meta_dict[class_name]
        :type single: [ True | False ], default is False

        :param required: return just the required elements and any elements with
                         non-None values

        """

        meta_dict = {}
        for name in list(self._attr_dict.keys()):
            try:
                value = self.get_attr_from_name(name)
                if hasattr(value, "to_dict"):
                    value = value.to_dict(nested=nested, required=required)
                elif isinstance(value, dict):
                    for key, obj in value.items():
                        if hasattr(obj, "to_dict"):
                            value[key] = obj.to_dict(
                                nested=nested, required=required
                            )
                        else:
                            value[key] = obj
                elif isinstance(value, list):
                    v_list = []
                    for obj in value:
                        if hasattr(obj, "to_dict"):
                            v_list.append(
                                obj.to_dict(nested=nested, required=required)
                            )
                        else:
                            v_list.append(obj)
                    value = v_list
            except AttributeError as error:
                self.logger.debug(error)
                value = None
            if required:
                if isinstance(value, (np.ndarray)):
                    if name == "zeros" or name == "poles":
                        meta_dict[name] = value
                    elif value.all() != 0:
                        meta_dict[name] = value
                elif hasattr(value, "size"):
                    if value.size > 0:
                        meta_dict[name] = value
                elif (
                    value
                    not in [None, "1980-01-01T00:00:00+00:00", "1980", [], ""]
                    or self._attr_dict[name]["required"]
                ):
                    meta_dict[name] = value
            else:
                meta_dict[name] = value
        if nested:
            meta_dict = helpers.structure_dict(meta_dict)
        meta_dict = {
            self._class_name.lower(): OrderedDict(
                sorted(meta_dict.items(), key=itemgetter(0))
            )
        }

        if single:
            meta_dict = meta_dict[list(meta_dict.keys())[0]]
        return meta_dict

    def from_dict(self, meta_dict, skip_none=False):
        """
        fill attributes from a dictionary

        :param meta_dict: dictionary with keys equal to metadata.
        :type meta_dict: dictionary

        """
        if not isinstance(meta_dict, (dict, OrderedDict)):
            msg = f"Input must be a dictionary not {type(meta_dict)}"
            self.logger.error(msg)
            raise MTSchemaError(msg)
        keys = list(meta_dict.keys())
        if len(keys) == 1:
            class_name = keys[0]
            if class_name.lower() != self._class_name.lower():
                msg = (
                    "name of input dictionary is not the same as class type "
                    f"input = {class_name}, class type = {self._class_name}"
                )
                self.logger.debug(msg, class_name, self._class_name)
            meta_dict = helpers.flatten_dict(meta_dict[class_name])
        else:
            self.logger.debug(
                f"Assuming input dictionary is of type {self._class_name}",
            )
            meta_dict = helpers.flatten_dict(meta_dict)
        # set attributes by key.
        for name, value in meta_dict.items():
            if skip_none:
                if value in [
                    None,
                    "None",
                    "none",
                    "NONE",
                    "null",
                    "Null",
                    "NULL",
                    "1980-01-01T00:00:00+00:00",
                ]:
                    continue
            self.set_attr_from_name(name, value)

    def to_json(self, nested=False, indent=" " * 4, required=True):
        """
        Write a json string from a given object, taking into account other
        class objects contained within the given object.

        :param nested: make the returned json nested
        :type nested: [ True | False ] , default is False

        """

        return json.dumps(
            self.to_dict(nested=nested, required=required),
            cls=helpers.NumpyEncoder,
            indent=indent,
        )

    def from_json(self, json_str):
        """
        read in a json string and update attributes of an object

        :param json_str: json string or file path
        :type json_str: string or :class:`pathlib.Path`

        """
        if isinstance(json_str, str):
            try:
                json_path = Path(json_str)
                if json_path.exists():
                    with open(json_path, "r") as fid:
                        json_dict = json.load(fid)
            except OSError:
                pass
            json_dict = json.loads(json_str)
        elif isinstance(json_str, Path):
            if json_str.exists():
                with open(json_str, "r") as fid:
                    json_dict = json.load(fid)
        elif not isinstance(json_str, (str, Path)):
            msg = f"Input must be valid JSON string not {type(json_str)}"
            self.logger.error(msg)
            raise MTSchemaError(msg)
        self.from_dict(json_dict)

    def from_series(self, pd_series):
        """
        Fill attributes from a Pandas series

        .. note:: Currently, the series must be single layered with key names
                  separated by dots. (location.latitude)

        :param pd_series: Series containing metadata information
        :type pd_series: pandas.Series

        .. todo:: Force types in series

        """
        if not isinstance(pd_series, pd.Series):
            msg = f"Input must be a Pandas.Series not type {type(pd_series)}"
            self.logger.error(msg)
            raise MTSchemaError(msg)
        for key, value in pd_series.items():
            self.set_attr_from_name(key, value)

    def to_series(self, required=True):
        """
        Convert attribute list to a pandas.Series

        .. note:: this is a flattened version of the metadata

        :return: pandas.Series
        :rtype: pandas.Series

        """

        return pd.Series(self.to_dict(single=True, required=required))

    def to_xml(self, string=False, required=True):
        """
        make an xml element for the attribute that will add types and
        units.

        :param string: output a string instead of an XML element
        :type string: [ True | False ], default is False

        :return: XML element or string

        """
        element = helpers.dict_to_xml(
            self.to_dict(nested=True, required=required), self._attr_dict
        )
        if not string:
            return element
        else:
            return helpers.element_to_string(element)

    def from_xml(self, xml_element):
        """

        :param xml_element: XML element
        :type xml_element: etree.Element

        :return: Fills attributes accordingly

        """

        self.from_dict(helpers.element_to_dict(xml_element))
