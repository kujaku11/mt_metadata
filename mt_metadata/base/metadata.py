# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:41:16 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
import json
from collections import OrderedDict
from enum import Enum

# =============================================================================
# Imports
# =============================================================================
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Union
from xml.etree import cElementTree as et

import numpy as np
import pandas as pd
from loguru import logger
from pydantic import BaseModel, computed_field, ConfigDict, create_model
from pydantic.fields import FieldInfo, PrivateAttr
from typing_extensions import deprecated

from mt_metadata import NULL_VALUES
from mt_metadata.utils.exceptions import MTSchemaError
from mt_metadata.utils.validators import validate_attribute, validate_name

from . import helpers


attr_dict = {}


# =============================================================================
#  Base class that everything else will inherit
# =============================================================================


@deprecated("Base is deprecated, use MetadataBase instead")
class Base:
    pass
    # __doc__ = write_lines(attr_dict)
    # _base_attr_loaded = False

    # def __init__(self, attr_dict={}, **kwargs):
    #     self._changed = False

    #     self._class_name = validate_attribute(self.__class__.__name__)

    #     self.logger = logger
    #     self._debug = False

    #     # attr_dict from subclass has already been validated on json load, so
    #     # we shouldn't need to validate it again re-validation of the attribute
    #     # dictionary used to contribute to some slowness in instantiation of
    #     # subclasses
    #     # self._set_attr_dict(deepcopy(attr_dict), skip_validation=True)
    #     self._set_attr_dict(attr_dict, skip_validation=True)

    #     for name, value in kwargs.items():
    #         self.set_attr_from_name(name, value, skip_validation=False)

    # def _set_attr_dict(self, attr_dict, skip_validation=False):
    #     """
    #     Set attribute dictionary and variables.

    #     should have the proper keys.

    #     :param attr_dict: attribute dictionary
    #     :type attr_dict: dict
    #     :param skip_validation: skip validation/parse of the attribute dictionary
    #     :type skip_validation: bool

    #     """

    #     self._attr_dict = attr_dict

    #     for key, value_dict in attr_dict.items():
    #         self.set_attr_from_name(key, value_dict["default"], skip_validation)

    # def __str__(self):
    #     """

    #     :return: table describing attributes
    #     :rtype: string

    #     """
    #     meta_dict = self.to_dict()[self._class_name.lower()]
    #     lines = [f"{self._class_name}:"]
    #     for name, value in meta_dict.items():
    #         lines.append(f"\t{name} = {value}")
    #     return "\n".join(lines)

    # def __repr__(self):
    #     return self.to_json()

    # def __eq__(self, other):
    #     if other in [None]:
    #         return False
    #     elif isinstance(other, (Base, dict, str, pd.Series)):
    #         home_dict = self.to_dict(single=True, required=False)
    #         if isinstance(other, Base):
    #             other_dict = other.to_dict(single=True, required=False)
    #         elif isinstance(other, dict):
    #             other_dict = other
    #         elif isinstance(other, str):
    #             if other.lower() in ["none", "null", "unknown"]:
    #                 return False
    #             other_dict = OrderedDict(
    #                 sorted(json.loads(other).items(), key=itemgetter(0))
    #             )
    #         elif isinstance(other, pd.Series):
    #             other_dict = OrderedDict(
    #                 sorted(other.to_dict().items(), key=itemgetter(0))
    #             )
    #         else:
    #             raise ValueError(
    #                 f"Cannot compare {self._class_name} with {type(other)}"
    #             )
    #         fail = False
    #         for key, value in home_dict.items():
    #             if "creation_time" in key:
    #                 continue
    #             try:
    #                 other_value = other_dict[key]
    #                 if isinstance(value, np.ndarray):
    #                     if value.size != other_value.size:
    #                         msg = f"Array sizes for {key} differ: {value.size} != {other_value.size}"
    #                         self.logger.info(msg)
    #                         fail = True
    #                         continue
    #                     if not (value == other_value).all():
    #                         msg = f"{key}: {value} != {other_value}"
    #                         self.logger.info(msg)
    #                         fail = True
    #                 elif isinstance(value, (float, int, complex)):
    #                     if not np.isclose(value, other_value):
    #                         msg = f"{key}: {value} != {other_value}"
    #                         self.logger.info(msg)
    #                         fail = True
    #                 else:
    #                     if value != other_value:
    #                         msg = f"{key}: {value} != {other_value}"
    #                         self.logger.info(msg)
    #                         fail = True
    #             except KeyError:
    #                 msg = "Cannot find {0} in other".format(key)
    #                 self.logger.info(msg)
    #         if fail:
    #             return False
    #         else:
    #             return True
    #     else:
    #         return False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def __len__(self):
    #     return len(self.get_attribute_list())

    # def update(self, other, match=[]):
    #     """
    #     Update attribute values from another like element, skipping None

    #     :param other: other Base object
    #     :type other: :class:`mt_metadata.base.metadata.Base`

    #     """
    #     if not isinstance(other, type(self)):
    #         self.logger.warning(f"Cannot update {type(self)} with {type(other)}")
    #     for k in match:
    #         if self.get_attr_from_name(k) != other.get_attr_from_name(k):
    #             msg = (
    #                 f"{k} is not equal {self.get_attr_from_name(k)} != "
    #                 f"{other.get_attr_from_name(k)}"
    #             )
    #             self.logger.error(msg)
    #             raise ValueError(msg)
    #     for k, v in other.to_dict(single=True).items():
    #         if hasattr(v, "size"):
    #             if v.size > 0:
    #                 self.set_attr_from_name(k, v)
    #         else:
    #             if v not in [None, 0.0, [], "", "1980-01-01T00:00:00+00:00"]:
    #                 self.set_attr_from_name(k, v)

    # @property
    # def changed(self):
    #     return self._changed

    # @changed.setter
    # def changed(self, value):
    #     self._changed = value

    # def __deepcopy__(self, memodict={}):
    #     """
    #     Need to skip copying the logger
    #     need to copy properties as well.

    #     :return: Deep copy
    #     :rtype: :class:`mt_metadata.base.metadata.Base`

    #     """
    #     copied = type(self)()
    #     for key in self.to_dict(single=True, required=False).keys():
    #         try:
    #             copied.set_attr_from_name(
    #                 key, deepcopy(self.get_attr_from_name(key), memodict)
    #             )
    #         # Need the TypeError for objects that have no __reduce__ method
    #         # like H5 references.
    #         except (AttributeError, TypeError) as error:
    #             self.logger.debug(error)
    #             continue
    #     # need to copy and properties
    #     for key in self.__dict__.keys():
    #         if key.startswith("_"):
    #             test_property = getattr(self.__class__, key[1:], None)
    #             if isinstance(test_property, property):
    #                 value = getattr(self, key[1:])
    #                 if hasattr(value, "copy"):
    #                     setattr(copied, key[1:], value.copy())
    #                 else:
    #                     setattr(copied, key[1:], value)

    #     return copied

    # def copy(self):
    #     """
    #     Copy object

    #     """

    #     return self.__deepcopy__()

    # def get_attribute_list(self):
    #     """
    #     return a list of the attributes
    #     """

    #     return sorted(list(self._attr_dict.keys()))

    # def attribute_information(self, name=None):
    #     """
    #     return a descriptive string of the attribute if none returns for all

    #     :param name: attribute name for a specifice attribute, defaults to None
    #     :type name: string, optional
    #     :return: description of the attributes or specific attribute if asked
    #     :rtype: string

    #     """

    #     if name:
    #         try:
    #             v_dict = OrderedDict(
    #                 sorted(self._attr_dict[name].items(), key=itemgetter(0))
    #             )
    #         except KeyError as error:
    #             msg = "{0} not attribute {1} found".format(error, name)
    #             self.logger.error(msg)
    #             raise MTSchemaError(msg)
    #         lines = ["{0}:".format(name)]
    #         for key, value in v_dict.items():
    #             lines.append("\t{0}: {1}".format(key, value))
    #     else:
    #         lines = []
    #         for name, v_dict in self._attr_dict.items():
    #             lines.append("{0}:".format(name))
    #             v_dict = OrderedDict(sorted(v_dict.items(), key=itemgetter(0)))
    #             for key, value in v_dict.items():
    #                 lines.append("\t{0}: {1}".format(key, value))
    #             lines.append("=" * 50)
    #     print("\n".join(lines))

    # def _validate_name(self, name):
    #     """
    #     validate the name to conform to the standards
    #     name must be:
    #         * all lower case {a-z; 1-9}
    #         * must start with a letter
    #         * categories are separated by '.'
    #         * words separated by '_'

    #     {object}.{name_name}

    #     '/' will be replaced with '.'
    #     converted to all lower case

    #     :param name: name name
    #     :type name: string
    #     :return: valid name name
    #     :rtype: string

    #     """
    #     return validate_attribute(name)

    # def _validate_type(self, value, v_type, style=None):
    #     """
    #     validate type from standards

    #     """

    #     try:
    #         return validate_value_type(value, v_type, style=style)
    #     except MTSchemaError as error:
    #         self.logger.exception(error)
    #         raise MTSchemaError(error)

    # def _validate_option(self, name, value, option_list):
    #     """
    #     validate the given attribute name agains possible options and check
    #     for aliases

    #     :param name: DESCRIPTION
    #     :type name: TYPE
    #     :param option_list: DESCRIPTION
    #     :type option_list: TYPE
    #     :param alias_list: DESCRIPTION
    #     :type alias_list: TYPE
    #     :return: DESCRIPTION
    #     :rtype: TYPE

    #     """
    #     if value is None:
    #         return True, False, None
    #     options = [ss.lower() for ss in option_list]
    #     other_possible = False
    #     if "other" in options:
    #         other_possible = True
    #     if value.lower() in options:
    #         return True, other_possible, None
    #     elif value.lower() not in options and other_possible:
    #         msg = (
    #             f"Value '{value}' not found for metadata field '{name}' in options list {option_list}, but other options"
    #             + f" are allowed.  Allowing {option_list} to be set to {value}."
    #         )
    #         return True, other_possible, msg
    #     return (
    #         False,
    #         other_possible,
    #         f"Value '{value}' for metadata field '{name}' not found in options list {option_list}",
    #     )

    # def __setattr__(self, name, value):
    #     """
    #     set attribute based on metadata standards

    #     Something here doesnt allow other objects to be set as attributes

    #     """
    #     # skip these attribute because they are validated in the property
    #     # setter.
    #     skip_list = [
    #         "latitude",
    #         "longitude",
    #         "elevation",
    #         "start_date",
    #         "end_date",
    #         "start",
    #         "end",
    #         "applied",
    #         "logger",
    #         "changed",
    #         "hdf5_reference",
    #         "obspy_mapping",
    #         "surveys",
    #         "filters",
    #         "stations",
    #         "runs",
    #         "channels",
    #         "channels_recorded_all",
    #         "channels_recorded_electric"
    #         "channels_recorded_magnetic"
    #         "channels_recorded_auxiliary",
    #         "electrode",
    #         "estimates_list",
    #         "input_channels",
    #         "output_channels",
    #         "data_types_list",
    #         "info_list",
    #         "info_dict",
    #         "filters_list",
    #         "fn",
    #     ]

    #     if name in skip_list:
    #         super().__setattr__(name, value)
    #         return
    #     if not name.startswith("_"):
    #         # test if the attribute is a property first, if it is, then
    #         # it will have its own defined setter, so use that one and
    #         # skip validation.
    #         try:
    #             test_property = getattr(self.__class__, name, None)
    #             if isinstance(test_property, property):
    #                 self.logger.debug(f"Identified {name} as property, using fset")
    #                 test_property.fset(self, value)
    #                 return
    #         except AttributeError:
    #             pass
    #     if hasattr(self, "_attr_dict") and not name.startswith("_"):
    #         self.logger.debug(f"Setting {name} to {value}")
    #         try:
    #             v_dict = self._attr_dict[name]
    #             v_type = self._get_standard_type(name)
    #             value = self._validate_type(value, v_type, v_dict["style"])
    #             # check options
    #             if v_dict["style"] == "controlled vocabulary":
    #                 options = v_dict["options"]
    #                 accept, other, msg = self._validate_option(name, value, options)
    #                 if not accept:
    #                     self.logger.error(msg.format(value, options))
    #                     raise MTSchemaError(msg.format(value, options))
    #                 if other and not accept:
    #                     self.logger.warning(msg.format(value, options, name))
    #             super().__setattr__(name, value)
    #         except KeyError as error:
    #             raise KeyError(error)
    #     else:
    #         super().__setattr__(name, value)

    # def _get_standard_type(self, name):
    #     """
    #     helper function to get the standard type for the given name
    #     """
    #     name = self._validate_name(name)
    #     try:
    #         standards = self._attr_dict[name]
    #         if isinstance(standards, type(logger)):
    #             return None
    #         return standards["type"]
    #     except KeyError:
    #         if name[0] != "_":
    #             msg = (
    #                 f"{name} is not defined in the standards. "
    #                 " Should add attribute information with "
    #                 "add_base_attribute if the attribute is going to "
    #                 "propogate via to_dict, to_json, to_series"
    #             )
    #             self.logger.info(msg)
    #         return None

    # def get_attr_from_name(self, name):
    #     """
    #     Access attribute from the given name.

    #     The name can contain the name of an object which must be separated
    #     by a '.' for  e.g. {object_name}.{name} --> location.latitude

    #     .. note:: this is a helper function for names with '.' in the name for
    #      easier getting when reading from dictionary.

    #     :param name: name of attribute to get.
    #     :type name: string
    #     :return: attribute value
    #     :rtype: type is defined by the attribute name

    #     :Example:

    #     >>> b = Base(**{'category.test_attr':10})
    #     >>> b.get_attr_from_name('category.test_attr')
    #     10

    #     """

    #     name = self._validate_name(name)
    #     v_type = self._get_standard_type(name)

    #     if "." in name:
    #         value, prop = helpers.recursive_split_getattr(self, name)
    #         if prop:
    #             return value
    #     else:
    #         value = getattr(self, name)
    #         try:
    #             if isinstance(getattr(type(self), name), property):
    #                 return value
    #         except AttributeError:
    #             pass
    #     if hasattr(value, "to_dict"):
    #         return value
    #     return self._validate_type(value, v_type)

    # def setattr_skip_validation(self, name, value):
    #     """
    #     Set attribute without validation

    #     :param name: name of attribute
    #     :type name: string

    #     :param value: value of the new attribute
    #     :type value: described in value_dict

    #     """
    #     self.__dict__[name] = value

    # def set_attr_from_name(self, name, value, skip_validation=False):
    #     """
    #     Helper function to set attribute from the given name.

    #     The name can contain the name of an object which must be separated
    #     by a '.' for  e.g. {object_name}.{name} --> location.latitude

    #     .. note:: this is a helper function for names with '.' in the name for
    #      easier getting when reading from dictionary.

    #     :param name: name of attribute to get.
    #     :type name: string
    #     :param value: attribute value
    #     :type value: type is defined by the attribute name
    #     :param skip_validation: skip validation/parse of the key-value pair
    #     :type skip_validation: bool

    #     :Example:

    #     >>> b = Base(**{'category.test_attr':10})
    #     >>> b.set_attr_from_name('category.test_attr', '10')
    #     >>> print(b.category.test_attr)
    #     '10'
    #     """
    #     if "." in name:
    #         try:
    #             helpers.recursive_split_setattr(
    #                 self, name, value, skip_validation=skip_validation
    #             )
    #         except AttributeError as error:
    #             msg = (
    #                 "{0} is not in the current standards.  "
    #                 + "To properly add the attribute use "
    #                 + "add_base_attribute."
    #             )

    #             self.logger.error(msg.format(name))
    #             raise AttributeError(error)
    #     else:
    #         if skip_validation:
    #             self.setattr_skip_validation(name, value)
    #         else:
    #             setattr(self, name, value)

    # def add_base_attribute(self, name, value, value_dict):
    #     """
    #     Add an attribute to _attr_dict so it will be included in the
    #     output dictionary

    #     :param name: name of attribute
    #     :type name: string

    #     :param value: value of the new attribute
    #     :type value: described in value_dict

    #     :param value_dict: dictionary describing the attribute, must have keys
    #      ['type', 'required', 'style', 'units', 'alias', 'description',
    #       'options', 'example']
    #     :type name: string

    #     * type --> the data type [ str | int | float | bool ]
    #     * required --> required in the standards [ True | False ]
    #     * style --> style of the string
    #     * units --> units of the attribute, must be a string
    #     * alias --> other possible names for the attribute
    #     * options --> if only a few options are accepted, separated by | or
    #        comma.b [ option_01 | option_02 | other ]. 'other' means other options
    #        available but not yet defined.
    #     * example --> an example of the attribute

    #     :Example:

    #     >>> extra = {'type': str,
    #     >>> ...      'style': 'controlled vocabulary',
    #     >>> ...      'required': False,
    #     >>> ...      'units': celsius,
    #     >>> ...      'description': 'local temperature',
    #     >>> ...      'alias': ['temp'],
    #     >>> ...      'options': [ 'ambient', 'air', 'other'],
    #     >>> ...      'example': 'ambient'}
    #     >>> r = Run()
    #     >>> r.add_base_attribute('temperature', 'ambient', extra)

    #     """
    #     name = self._validate_name(name)
    #     self._attr_dict.update({name: value_dict})
    #     self.set_attr_from_name(name, value)

    # def to_dict(self, nested=False, single=False, required=True):
    #     """
    #     make a dictionary from attributes, makes dictionary from _attr_list.

    #     :param nested: make the returned dictionary nested
    #     :type nested: [ True | False ] , default is False

    #     :param single: return just metadata dictionary -> meta_dict[class_name]
    #     :type single: [ True | False ], default is False

    #     :param required: return just the required elements and any elements with
    #                      non-None values

    #     """

    #     meta_dict = {}
    #     for name in list(self._attr_dict.keys()):
    #         try:
    #             value = self.get_attr_from_name(name)
    #             if hasattr(value, "to_dict"):
    #                 value = value.to_dict(nested=nested, required=required)
    #             elif isinstance(value, dict):
    #                 for key, obj in value.items():
    #                     if hasattr(obj, "to_dict"):
    #                         value[key] = obj.to_dict(nested=nested, required=required)
    #                     else:
    #                         value[key] = obj
    #             elif isinstance(value, list):
    #                 v_list = []
    #                 for obj in value:
    #                     if hasattr(obj, "to_dict"):
    #                         v_list.append(obj.to_dict(nested=nested, required=required))
    #                     else:
    #                         v_list.append(obj)
    #                 value = v_list
    #         except AttributeError as error:
    #             self.logger.debug(error)
    #             value = None
    #         if required:
    #             if isinstance(value, (np.ndarray)):
    #                 if name == "zeros" or name == "poles":
    #                     meta_dict[name] = value
    #                 elif value.all() != 0:
    #                     meta_dict[name] = value
    #             elif hasattr(value, "size"):
    #                 if value.size > 0:
    #                     meta_dict[name] = value
    #             elif (
    #                 value not in [None, "1980-01-01T00:00:00+00:00", "1980", [], ""]
    #                 or self._attr_dict[name]["required"]
    #             ):
    #                 meta_dict[name] = value
    #         else:
    #             meta_dict[name] = value
    #     if nested:
    #         meta_dict = helpers.structure_dict(meta_dict)
    #     meta_dict = {
    #         self._class_name.lower(): OrderedDict(
    #             sorted(meta_dict.items(), key=itemgetter(0))
    #         )
    #     }

    #     if single:
    #         meta_dict = meta_dict[list(meta_dict.keys())[0]]
    #     return meta_dict

    # def from_dict(self, meta_dict, skip_none=False):
    #     """
    #     fill attributes from a dictionary

    #     :param meta_dict: dictionary with keys equal to metadata.
    #     :type meta_dict: dictionary

    #     """
    #     if not isinstance(meta_dict, (dict, OrderedDict)):
    #         msg = f"Input must be a dictionary not {type(meta_dict)}"
    #         self.logger.error(msg)
    #         raise MTSchemaError(msg)
    #     keys = list(meta_dict.keys())
    #     if len(keys) == 1:
    #         class_name = keys[0]
    #         if class_name.lower() != self._class_name.lower():
    #             msg = (
    #                 "name of input dictionary is not the same as class type "
    #                 f"input = {class_name}, class type = {self._class_name}"
    #             )
    #             self.logger.debug(msg, class_name, self._class_name)
    #         meta_dict = helpers.flatten_dict(meta_dict[class_name])
    #     else:
    #         self.logger.debug(
    #             f"Assuming input dictionary is of type {self._class_name}",
    #         )
    #         meta_dict = helpers.flatten_dict(meta_dict)
    #     # set attributes by key.
    #     for name, value in meta_dict.items():
    #         if skip_none:
    #             if value in [
    #                 None,
    #                 "None",
    #                 "none",
    #                 "NONE",
    #                 "null",
    #                 "Null",
    #                 "NULL",
    #                 "1980-01-01T00:00:00+00:00",
    #             ]:
    #                 continue
    #         self.set_attr_from_name(name, value)

    # def to_json(self, nested=False, indent=" " * 4, required=True):
    #     """
    #     Write a json string from a given object, taking into account other
    #     class objects contained within the given object.

    #     :param nested: make the returned json nested
    #     :type nested: [ True | False ] , default is False

    #     """

    #     return json.dumps(
    #         self.to_dict(nested=nested, required=required),
    #         cls=helpers.NumpyEncoder,
    #         indent=indent,
    #     )

    # def from_json(self, json_str):
    #     """
    #     read in a json string and update attributes of an object

    #     :param json_str: json string or file path
    #     :type json_str: string or :class:`pathlib.Path`

    #     """
    #     if isinstance(json_str, str):
    #         try:
    #             json_path = Path(json_str)
    #             if json_path.exists():
    #                 with open(json_path, "r") as fid:
    #                     json_dict = json.load(fid)
    #         except OSError:
    #             pass
    #         json_dict = json.loads(json_str)
    #     elif isinstance(json_str, Path):
    #         if json_str.exists():
    #             with open(json_str, "r") as fid:
    #                 json_dict = json.load(fid)
    #     elif not isinstance(json_str, (str, Path)):
    #         msg = f"Input must be valid JSON string not {type(json_str)}"
    #         self.logger.error(msg)
    #         raise MTSchemaError(msg)
    #     self.from_dict(json_dict)

    # def from_series(self, pd_series):
    #     """
    #     Fill attributes from a Pandas series

    #     .. note:: Currently, the series must be single layered with key names
    #               separated by dots. (location.latitude)

    #     :param pd_series: Series containing metadata information
    #     :type pd_series: pandas.Series

    #     .. todo:: Force types in series

    #     """
    #     if not isinstance(pd_series, pd.Series):
    #         msg = f"Input must be a Pandas.Series not type {type(pd_series)}"
    #         self.logger.error(msg)
    #         raise MTSchemaError(msg)
    #     for key, value in pd_series.items():
    #         self.set_attr_from_name(key, value)

    # def to_series(self, required=True):
    #     """
    #     Convert attribute list to a pandas.Series

    #     .. note:: this is a flattened version of the metadata

    #     :return: pandas.Series
    #     :rtype: pandas.Series

    #     """

    #     return pd.Series(self.to_dict(single=True, required=required))

    # def to_xml(self, string=False, required=True):
    #     """
    #     make an xml element for the attribute that will add types and
    #     units.

    #     :param string: output a string instead of an XML element
    #     :type string: [ True | False ], default is False

    #     :return: XML element or string

    #     """
    #     element = helpers.dict_to_xml(
    #         self.to_dict(nested=True, required=required), self._attr_dict
    #     )
    #     if not string:
    #         return element
    #     else:
    #         return helpers.element_to_string(element)

    # def from_xml(self, xml_element):
    #     """

    #     :param xml_element: XML element
    #     :type xml_element: etree.Element

    #     :return: Fills attributes accordingly

    #     """

    #     self.from_dict(helpers.element_to_dict(xml_element))


class DotNotationBaseModel(BaseModel):
    """Base model that supports dot notation for setting nested attributes."""

    def __init__(self, **data):
        # Process dot notation fields first
        flat_data = {}
        nested_data = {}

        for key, value in data.items():
            if "." in key:
                # This is a dotted field, handle specially
                self._set_nested_attribute(nested_data, key, value)
            else:
                # Regular field, pass to Pydantic as-is
                if key == validate_name(self.__class__.__name__):
                    if isinstance(value, dict):
                        # If the value is a dict, we need to flatten it
                        for nested_key, nested_value in value.items():
                            if isinstance(nested_value, dict):
                                # Flatten nested dicts
                                self._set_nested_attribute(
                                    nested_data, nested_key, nested_value
                                )
                            else:
                                flat_data[nested_key] = nested_value
                else:
                    flat_data[key] = value

        # Merge the nested dict into flat dict (nested takes precedence)
        flat_data.update(nested_data)

        # Call parent constructor with processed data
        super().__init__(**flat_data)

    def _set_nested_attribute(
        self, data_dict: Dict, dotted_key: str, value: Any
    ) -> None:
        """
        Set a nested attribute in data_dict based on dotted key notation.

        Example: time_period.start => {"time_period": {"start": value}}
        """
        parts = dotted_key.split(".")
        current = data_dict

        # Navigate to the deepest level, creating dicts along the way
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                # Convert to dict if it's not already
                current[part] = {}
            current = current[part]

        # Set the final value
        current[parts[-1]] = value

    def update_attribute(self, attr_name: str, attr_value: Any) -> None:
        """
        Update a nested attribute using dot notation.

        Example: update_attribute("time_period.start", "2020-01-01")
        """
        if "." not in attr_name:
            # Directly set the attribute
            setattr(self, attr_name, attr_value)
            return

        # For nested attributes, we need to navigate the object graph
        parts = attr_name.split(".")
        current = self

        # Navigate to the deepest level
        for part in parts[:-1]:
            if not hasattr(current, part):
                raise AttributeError(
                    f"'{type(current).__name__}' has no attribute '{part}'"
                )
            current = getattr(current, part)

        # Set the final attribute
        setattr(current, parts[-1], attr_value)


class MetadataBase(DotNotationBaseModel):
    """
    MetadataBase is the base class for all metadata objects.  `pydantic.BaseModel`
    is inherited, thus Pydantic takes care of all the validating accoring to the
    metadata given.

    Functionality of pydantic.BaseModel are extended including ingesting more than
    just a dictionary.

    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_attribute_docstrings=True,
        extra="allow",
        arbitrary_types_allowed=True,  # need this for numpy and pd types
        use_enum_values=True,
        coerce_numbers_to_str=True,
    )

    _default_keys: List[str] = PrivateAttr(
        ["annotation", "default", "examples", "description"]
    )
    _json_extras: List[str] = PrivateAttr(["units", "required"])

    @computed_field
    @property
    def _class_name(self) -> str:
        return validate_attribute(self.__class__.__name__)

    # def __init__(self, **kwargs):
    #     """
    #     Initialize the MetadataBase object.  This will take in a dictionary or
    #     other objects and convert them to a dictionary.

    #     :param kwargs: keyword arguments for the metadata object

    #     """
    #     self.from_dict(kwargs, skip_none=True)
    #     super().__init__()

    def __str__(self) -> str:
        """

        :return: table describing attributes
        :rtype: string

        """
        return str(self.model_dump())

    def __repr__(self) -> str:
        return self.to_json()

    def __eq__(
        self, other: Union["MetadataBase", dict, str, pd.Series, et.Element]
    ) -> bool:
        """
           create a self.load that will take in a dict, str, pd.Series, xml, etc
           which will create a MetadataBase object.  Then Pydantic will deal
           with the __eq__:

           if isinstance(other, BaseModel):
            # When comparing instances of generic types for equality, as long as all field values are equal,
            # only require their generic origin types to be equal, rather than exact type equality.
            # This prevents headaches like MyGeneric(x=1) != MyGeneric[Any](x=1).
            self_type = self.__pydantic_generic_metadata__['origin'] or self.__class__
            other_type = other.__pydantic_generic_metadata__['origin'] or other.__class__

            # Perform common checks first
            if not (
                self_type == other_type
                and getattr(self, '__pydantic_private__', None) == getattr(other, '__pydantic_private__', None)
                and self.__pydantic_extra__ == other.__pydantic_extra__
            ):
                return False

            # We only want to compare pydantic fields but ignoring fields is costly.
            # We'll perform a fast check first, and fallback only when needed
            # See GH-7444 and GH-7825 for rationale and a performance benchmark

            # First, do the fast (and sometimes faulty) __dict__ comparison
            if self.__dict__ == other.__dict__:
                # If the check above passes, then pydantic fields are equal, we can return early
                return True

            # We don't want to trigger unnecessary costly filtering of __dict__ on all unequal objects, so we return
            # early if there are no keys to ignore (we would just return False later on anyway)
            model_fields = type(self).model_fields.keys()
            if self.__dict__.keys() <= model_fields and other.__dict__.keys() <= model_fields:
                return False

            # If we reach here, there are non-pydantic-fields keys, mapped to unequal values, that we need to ignore
            # Resort to costly filtering of the __dict__ objects
            # We use operator.itemgetter because it is much faster than dict comprehensions
            # NOTE: Contrary to standard python class and instances, when the Model class has a default value for an
            # attribute and the model instance doesn't have a corresponding attribute, accessing the missing attribute
            # raises an error in BaseModel.__getattr__ instead of returning the class attribute
            # So we can use operator.itemgetter() instead of operator.attrgetter()
            getter = operator.itemgetter(*model_fields) if model_fields else lambda _: _utils._SENTINEL
            try:
                return getter(self.__dict__) == getter(other.__dict__)
            except KeyError:
                # In rare cases (such as when using the deprecated BaseModel.copy() method),
                # the __dict__ may not contain all model fields, which is how we can get here.
                # getter(self.__dict__) is much faster than any 'safe' method that accounts
                # for missing keys, and wrapping it in a `try` doesn't slow things down much
                # in the common case.
                self_fields_proxy = _utils.SafeGetItemProxy(self.__dict__)
                other_fields_proxy = _utils.SafeGetItemProxy(other.__dict__)
                return getter(self_fields_proxy) == getter(other_fields_proxy)

        # other instance is not a BaseModel
        else:
            return NotImplemented  # delegate to the other item in the comparison
        """
        if other in [None]:
            return False

        elif isinstance(other, (dict, str, pd.Series, et.Element)):
            try:
                # Attempt to load the other object into a new instance of MetadataBase
                # This will ensure that the other object has the same attributes as self
                other_obj = __class__().load(other)
            except Exception as e:
                logger.error(
                    f"Failed to load other object of type {type(other)}: {other}. Error is: {e} "
                )
                return False
            if not other_obj:
                return False

            if hasattr(other_obj, "to_dict") and callable(other_obj.to_dict):
                other_dict = other_obj.to_dict(single=True, required=False)
            else:
                return False

        elif isinstance(other, MetadataBase):
            other_dict = other.to_dict(single=True, required=False)
        else:
            raise ValueError(
                f"Cannot compare {self.__class__.__name__} with {type(other)}"
            )
        home_dict = self.to_dict(single=True, required=False)
        if home_dict == other_dict:
            return True

        fail = False
        for key, value in home_dict.items():
            try:
                other_value = other_dict[key]
                if isinstance(value, np.ndarray):
                    if value.size != other_value.size:
                        msg = f"Array sizes for {key} differ: {value.size} != {other_value.size}"
                        logger.info(msg)
                        fail = True
                        continue
                    if not (value == other_value).all():
                        msg = f"{key}: {value} != {other_value}"
                        logger.info(msg)
                        fail = True
                elif isinstance(value, (float, int, complex)):
                    if not np.isclose(value, other_value):
                        msg = f"{key}: {value} != {other_value}"
                        logger.info(msg)
                        fail = True
                else:
                    if value != other_value:
                        msg = f"{key}: {value} != {other_value}"
                        logger.info(msg)
                        fail = True
            except KeyError:
                msg = "Cannot find {0} in other".format(key)
                logger.info(msg)
        return fail

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.get_attribute_list())

    def load(
        self, other: Union["MetadataBase", dict, str, pd.Series, et.Element]
    ) -> None:
        """
        Load in an other object and populate attributes.  The other object
        should have the same attributes as the current object.  If there are
        attributes different than the current object validation will not be
        accurate.  Consider making a new model if you want a different object.

        Excepted types are:

         - MetadataBase
         - Dict
         - JSON string
         - Pandas Series
         - XML element

        Parameters
        ----------
        other : Union[MetadataBase, Dict, str, pd.Series, et.Element]
            other object from which to fill attributes with.  Must have the
            same attribute names as the current object.
            If a different object is passed in validation will not be
            accurate.
        """
        if isinstance(other, MetadataBase):
            self.update(other)
        elif isinstance(other, dict):
            self.from_dict(other)
        elif isinstance(other, str):
            if other.lower() in NULL_VALUES:
                return
            self.from_json(other)
        elif isinstance(other, pd.Series):
            self.from_series(other)
        elif isinstance(other, et.Element):
            self.from_xml(other)
        else:
            msg = f"Cannot load {type(other)} into {self.__class__.__name__}"
            logger.error(msg)
            raise MTSchemaError(msg)

    def update(self, other: "MetadataBase", match: list[str] = []) -> None:
        """
        Update attribute values from another like element, skipping None

        :param other: other Base object
        :type other: :class:`mt_metadata.base.metadata.Base`

        """
        if not isinstance(other, type(self)):
            logger.warning(f"Cannot update {type(self)} with {type(other)}")
        for k in match:
            if self.get_attr_from_name(k) != other.get_attr_from_name(k):
                msg = (
                    f"{k} is not equal {self.get_attr_from_name(k)} != "
                    f"{other.get_attr_from_name(k)}"
                )
                logger.error(msg)
                raise ValueError(msg)
        for k, v in other.to_dict(single=True).items():
            if hasattr(v, "size"):
                if v.size > 0:
                    self.update_attribute(k, v)
            else:
                if (
                    v
                    not in [None, 0.0, [], "", "1980-01-01T00:00:00+00:00"]
                    + NULL_VALUES
                ):
                    self.update_attribute(k, v)

    ## cannot override the __deepcopy__ method in pydantic.BaseModel otherwise bad
    ## things happen
    def copy(
        self, update: Mapping[str, Any] | None = None, deep: bool = True
    ) -> "MetadataBase":
        """
        Create a copy of the current object.  This is a wrapper around the
        pydantic copy method.

        Parameters
        ----------
        update : Mapping[str, Any]
            Values to change/add in the new model.
            Note: the data is not validated before creating the new model.
            You should trust this data.

        deep : bool, optional
            If True, create a deep copy of the object. The default is True.

        Returns
        -------
        MetadataBase
            A copy of the current object.
        """

        return self.model_copy(update=update, deep=deep)

    def get_all_fields(self) -> dict:
        """
        Get all field attributes in the Metadata class.  Will
        search recursively and return dotted keys.  For
        instance `{location.latitude: ...}`.

        Returns
        -------
        Dict
            A flattened dictionary of dotted keys of all attributes
            within the class.
        """

        return helpers.flatten_dict(helpers.get_all_fields(self))

    def get_attribute_list(self) -> list[str]:
        """
        return a list of the attributes
        """

        return sorted(self.get_all_fields().keys())

    @property
    def _required_fields(self) -> list[str]:
        """
        Get a list of required fields, here required is defined
        from the metadata standards.  There is a difference
        between required in Pydantic, in that required means
        it needs to be defined on instantiation.  The metadata
        required means that the field needs to be in the standard
        even though the value may be None.

        Returns
        -------
        List[str]
            List of required fields in the metadata standards.
        """
        required_fields = []
        for name, field_info in self.get_all_fields().items():
            if field_info.json_schema_extra is None:
                continue
            if field_info.json_schema_extra.get("required", False):
                required_fields.append(name)

        return required_fields
        # return [
        #     name
        #     for name, field_info in self.get_all_fields().items()
        #     if field_info.json_schema_extra["required"]
        # ]

    def _field_info_to_string(self, name: str, field_info: FieldInfo) -> str:
        """
        Create a string from a FieldInfo object for pretty printing

        Parameters
        ----------
        name : str
            name of the Field

        field_info : FieldInfo
            _description_

        Returns
        -------
        str
            _description_
        """

        line = [f"{name}:"]
        for key in self._default_keys:
            line.append(f"\t{key}: {getattr(field_info, key)}")
        json_extras = field_info.json_schema_extra
        if json_extras is not None:
            for key in self._json_extras:
                try:
                    line.append(f"\t{key}: {json_extras[key]}")
                except KeyError:
                    pass
        if "enum" in str(field_info.annotation).lower():
            options = []
            if "|" in str(field_info.annotation).lower():
                for ii, ktype in enumerate(field_info.annotation.__args__):
                    if "enum" in str(ktype):
                        options += [obj.value for obj in ktype]
            else:
                options += [obj.value for obj in field_info.annotation.__args__]

            line.append(f"\taccepted options: [{', '.join(options)}]")

        return "\n".join(line)

    def attribute_information(self, name: str | None = None) -> None:
        """
        return a descriptive string of the attribute if none returns for all

        :param name: attribute name for a specifice attribute, defaults to None
        :type name: string, optional
        :return: description of the attributes or specific attribute if asked
        :rtype: string

        """
        attr_dict = self.get_all_fields()
        lines = []
        if name:
            try:
                v_dict = attr_dict[name]
            except KeyError as error:
                msg = f"{error} not attribute {name} found."
                logger.error(msg)
                raise MTSchemaError(msg)
            lines.append(self._field_info_to_string(name, v_dict))
        else:
            lines = []
            for name, v_dict in attr_dict.items():
                lines.append(self._field_info_to_string(name, v_dict))
                lines.append("=" * 50)
        print("\n".join(lines))

    def get_attr_from_name(self, name: str) -> Any:
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

        value, _ = helpers.recursive_split_getattr(self, name)
        return value

    @deprecated(
        "set_attr_from_name will be deprecated in the future. Use update_attribute."
    )
    def set_attr_from_name(self, name: str, value: Any) -> None:
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

        :Example:

        >>> b = Base(**{'category.test_attr':10})
        >>> b.set_attr_from_name('category.test_attr', '10')
        >>> print(b.category.test_attr)
        '10'
        """

        try:
            self.update_attribute(name, value)
        except AttributeError as error:
            msg = (
                f"{name} is not in the current standards.  "
                + "To properly add the attribute use "
                + "add_base_attribute."
            )

            logger.error(msg)
            raise AttributeError(error)

    @deprecated("add_base_attribute is deprecated. Use add_new_field.")
    def add_base_attribute(
        self,
    ):
        pass

    def add_new_field(self, name: str, new_field_info: FieldInfo) -> BaseModel:
        """
        This is going to be much different from older versions of mt_metadata.

        This will return a new BaseModel with the added attribute.  Going to use
        `pydantid.create_model` from the exsiting attribute information and the
        added attribute.

        Add an attribute to _attr_dict so it will be included in the
        output dictionary

        :param name: name of attribute
        :type name: string

        :param new_field_info: value of the new attribute
        :type new_field_info: pydantic.fields.FieldInfo

        Should include:

        * annotated --> the data type [ str | int | float | bool ]
        * required --> required in the standards [ True | False ]
        * units --> units of the attribute, must be a string
        * alias --> other possible names for the attribute
        * options --> if only a few options are accepted, separated by | or
           comma.b [ option_01 | option_02 | other ]. 'other' means other options
           available but not yet defined.
        * example --> an example of the attribute

        :Example:

        .. code-block:: python

        from pydantic.fields import FieldInfo
        new_field = FieldInfo(
            annotated=str,
            default="default_value",
            required=False,
            description="new field description",
            alias="new_field_alias",
            json_schema_extra={"units":"km"}
            )

        existing_basemodel = MetadataBase()
        new_basemodel = existing_basemodel.add_new_field("new_attribute", new_field)
        new_basemodel_object = new_basemodel()

        """
        existing_model_fields = self.__pydantic_fields__
        existing_model_fields[name] = new_field_info
        all_fields = {k: (v.annotation, v) for k, v in existing_model_fields.items()}

        return create_model(
            name,
            __base__=MetadataBase,
            **all_fields,
        )

    def to_dict(self, nested=False, single=False, required=True) -> dict[str, Any]:
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
        for name in self.get_attribute_list():
            # if "comments" in name:
            #     # this is a hack to get around the fact that comments are not
            #     # in the standard.  Need to remove the last part of the name
            #     # to get the attribute name.
            #     # will change in the future.
            #     name = ".".join(name.split(".")[:-1])
            #     if "time_stamp" in name or "author" in name:
            #         continue
            #     try:
            #         value = self.get_attr_from_name(name).to_dict()
            #     except AttributeError:
            #         # if the attribute is not a BaseModel, then just get the value
            #         # this is for comments which are not BaseModels.
            #         logger.debug(f"Attribute {name} is not a BaseModel.")
            #         continue

            #     if value is not None:
            #         meta_dict[name] = value
            #     continue
            try:
                value = self.get_attr_from_name(name)
                if hasattr(value, "to_dict"):
                    value = value.to_dict(nested=nested, required=required)
                elif isinstance(value, dict):
                    for key, obj in value.items():
                        if hasattr(obj, "to_dict"):
                            value[key] = obj.to_dict(nested=nested, required=required)
                        elif isinstance(obj, Enum):
                            value[key] = obj.value
                        else:
                            value[key] = obj
                elif isinstance(value, list):
                    v_list = []
                    for obj in value:
                        if hasattr(obj, "to_dict"):
                            v_list.append(obj.to_dict(nested=nested, required=required))
                        elif isinstance(obj, Enum):
                            v_list.append(obj.value)
                        else:
                            v_list.append(obj)
                    value = v_list
                elif isinstance(value, Enum):
                    value = value.value
                elif hasattr(value, "unicode_string"):
                    value = value.unicode_string()
                elif isinstance(value, (str, int, float, bool)):
                    value = value
            except AttributeError as error:
                logger.debug(error)
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
                    value not in [None, "1980-01-01T00:00:00+00:00", "1980", [], ""]
                    or name in self._required_fields
                ):
                    meta_dict[name] = value
            else:
                meta_dict[name] = value
        if nested:
            meta_dict = helpers.structure_dict(meta_dict)
        meta_dict = {
            validate_name(self.__class__.__name__): OrderedDict(
                sorted(meta_dict.items(), key=itemgetter(0))
            )
        }

        if single:
            meta_dict = meta_dict[list(meta_dict.keys())[0]]
        return meta_dict

    def from_dict(self, meta_dict: dict, skip_none: bool = False) -> None:
        """
        fill attributes from a dictionary

        :param meta_dict: dictionary with keys equal to metadata.
        :type meta_dict: dictionary

        """
        if not isinstance(meta_dict, (dict, OrderedDict)):
            msg = f"Input must be a dictionary not {type(meta_dict)}"
            logger.error(msg)
            raise MTSchemaError(msg)
        keys = list(meta_dict.keys())
        if len(keys) == 1:
            if isinstance(meta_dict[keys[0]], (dict, OrderedDict)):
                class_name = keys[0]
                if class_name.lower() != validate_name(self.__class__.__name__):
                    msg = (
                        "name of input dictionary is not the same as class type "
                        f"input = {class_name}, class type = {self.__class__.__name__}"
                    )
                    logger.debug(msg, class_name, self.__class__.__name__)
                meta_dict = helpers.flatten_dict(meta_dict[class_name])
            else:
                meta_dict = helpers.flatten_dict(meta_dict)

        else:
            logger.debug(
                f"Assuming input dictionary is of type {self.__class__.__name__}",
            )
            meta_dict = helpers.flatten_dict(meta_dict)
        # set attributes by key.
        for name, value in meta_dict.items():
            if skip_none:
                if value in NULL_VALUES:
                    continue
            self.update_attribute(name, value)

    def to_json(
        self, nested: bool = False, indent: str = " " * 4, required: bool = True
    ) -> str:
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

    def from_json(self, json_str: str | Path) -> None:
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
            logger.error(msg)
            raise MTSchemaError(msg)
        self.from_dict(json_dict)

    def from_series(self, pd_series: pd.Series) -> None:
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
            logger.error(msg)
            raise MTSchemaError(msg)
        for key, value in pd_series.items():
            key = str(key)
            self.update_attribute(key, value)

    def to_series(self, required: bool = True) -> pd.Series:
        """
        Convert attribute list to a pandas.Series

        .. note:: this is a flattened version of the metadata

        :return: pandas.Series
        :rtype: pandas.Series

        """

        return pd.Series(self.to_dict(single=True, required=required))

    def to_xml(self, string: bool = False, required: bool = True) -> str | et.Element:
        """
        make an xml element for the attribute that will add types and
        units.

        :param string: output a string instead of an XML element
        :type string: [ True | False ], default is False

        :return: XML element or string

        """
        attr_dict = self.get_all_fields()
        element = helpers.dict_to_xml(
            self.to_dict(nested=True, required=required), attr_dict
        )
        if not string:
            return element
        else:
            return helpers.element_to_string(element)

    def from_xml(self, xml_element: et.Element) -> None:
        """

        :param xml_element: XML element
        :type xml_element: etree.Element

        :return: Fills attributes accordingly

        """

        self.from_dict(helpers.element_to_dict(xml_element))
