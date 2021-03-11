# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:02:12 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from copy import deepcopy
from collections import OrderedDict
from collections.abc import MutableMapping
from operator import itemgetter
import json

from mt_metadata.utils import validators
from mt_metadata.utils.exceptions import MTSchemaError
from mt_metadata import REQUIRED_KEYS
from mt_metadata.base.helpers import NumpyEncoder
from mt_metadata.utils.mt_logger import setup_logger

logger = setup_logger(__name__, fn="metadata_schema")
# =============================================================================
# base dictionary
# =============================================================================
class BaseDict(MutableMapping):
    """
    BaseDict is a convenience class that can help the metadata dictionaries 
    act like classes so you can access variables by .name or [name]
    
    .. note:: If the attribute has a . in the name then you will not be able
              to access that attribute by class.name.name  You will get an 
              attribute error.  You need to access the attribute like a 
              dictionary class['name.name']
              
    You can add an attribute by:
        
        >>> b = BaseDict()
        >>> b.update({name: value_dict})
        
    Or you can add a whole dictionary:
        
        >>> b.add_dict(ATTR_DICT['run'])
        
    All attributes have a descriptive dictionary of the form:
        
        >>> {'type': data type, 'required': [True | False],
        >>> ... 'style': 'string style', 'units': attribute units}
    
        * **type** --> the data type [ str | int | float | bool ]
        * **required** --> required in the standards [ True | False ]
        * **style** --> style of the string
        * **units** --> units of the attribute, must be a string
    """

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __setitem__(self, key, value):
        self.__dict__[key] = validators.validate_value_dict(value)

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as error:
            msg = (
                "{0} {1} is not in dictionary yet. ".format(error, key)
                + "Returning default schema dictionary."
            )
            logger.debug(msg)
            return {
                "type": "string",
                "required": False,
                "style": "free form",
                "units": None,
                "options": None,
                "description": "user defined",
                "example": None,
            }

    def __delitem__(self, key):
        try:
            del self.__dict__[key]
        except KeyError:
            msg = "Key: {0} does not exist".format(key)
            logger.info(msg)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        """returns simple dict representation of the mapping"""
        s = dict(sorted(self.__dict__.items(), key=itemgetter(0)))
        lines = []
        for key, value in s.items():
            if key in ["logger"]:
                continue
            lines.append("{0}:".format(key))
            for name, info in value.items():
                lines.append("\t{0}: {1}".format(name, info))
        return "\n".join(lines)

    def __repr__(self):
        """echoes class, id, & reproducible representation in the REPL"""
        return "{}, BaseDict({})".format(
            super(BaseDict, self).__repr__(), self.__dict__
        )

    @property
    def name(self):
        try:
            return list(self.keys())[0]
        except KeyError:
            return None

    def add_dict(self, add_dict, name=None, keys=None):
        """
        Add a dictionary to.  If name is input it is added to the keys of
        the input dictionary
        
        :param add_dict: dictionary to add
        :type add_dict: dictionary, or MutableMapping
        :param name: name to add to keys
        :type name: string or None
    
        :Example: :: 
            
            >>> s_obj = Standards()
            >>> run_dict = s_obj.run_dict
            >>> run_dict.add_dict(s_obj.declination_dict, 'declination')
            
        """
        if not isinstance(add_dict, (dict, MutableMapping)):
            msg = "add_dict takes only a dictionary not type {0}".format(type(add_dict))
            logger.error(msg)
            raise TypeError(msg)

        if keys:
            small_dict = {}
            for key, value in add_dict.items():
                if key in keys:
                    small_dict[key] = value
            add_dict = small_dict

        if name:
            add_dict = dict(
                [
                    ("{0}.{1}".format(name, key), value)
                    for key, value in add_dict.items()
                ]
            )

        self.update(**add_dict)

    def copy(self):
        return deepcopy(self)

    def to_latex(self, max_entries=7, first_table_len=7):
        """
        
        :param level_dict: DESCRIPTION
        :type level_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE
    
        """
        beginning = [
            r"\clearpage",
            r"\\newpage",
            r"\\begin{table}[h!]",
            r"\caption*{{Attributes for {0} Category}}".format(self.name),
            r"\\begin{tabular}{p{.305\\textwidth}p{.47\\textwidth}p{.2\\textwidth}}",
        ]

        end = [r"\end{tabular}", r"\label{tab:}", r"\end{table}"]
        header = [
            " & ".join(
                [r"\textbf{Metadata Key}", r"\textbf{Description}", r"\textbf{Example}"]
            )
            + " \\ \toprule"
        ]

        order = ["name", "required", "units", "type", "style", "description", "example"]

        level_dict = OrderedDict(sorted(self.items(), key=itemgetter(0)))

        ntables = int(len(level_dict) / max_entries)
        if len(level_dict) // max_entries > 0:
            ntables += 1

        lines = []
        for name, v_dict in level_dict.items():
            if not v_dict["options"] in [None, "none", "None", []]:
                v_dict["description"] += ".  Options: {0}".format(v_dict["options"])
            line = [
                r"\entry{{{0}}}".format(name)
                + "".join(["{{{0}}}".format(v_dict[ii]) for ii in order[1:]])
            ]
            lines.append(line[0])

        all_lines = beginning + header + ["\n".join(lines[0:first_table_len])] + end
        for ii in range(ntables - 1):
            stable = beginning + header
            for kk in range(max_entries):
                index = first_table_len + max_entries * ii + kk
                try:
                    stable.append(lines[index].replace("_", r"\_"))
                except IndexError:
                    break
            stable += end
            all_lines.append("\n".join(stable))

        return all_lines

    def from_csv(self, csv_fn):
        """
        Read in CSV file as a dictionary
    
        :param csv_fn: csv file to read metadata standards from
        :type csv_fn: pathlib.Path or string
    
        :return: dictionary of the contents of the file
        :rtype: Dictionary
    
        :Example: ::
    
            >>> run_dict = BaseDict()
            >>> run_dict.from_csv(get_level_fn('run'))
    
        """
        csv_fn = Path(csv_fn)
        if not csv_fn.exists():
            msg = f"Schema file {csv_fn} does not exist."
            logger.error(msg)
            raise MTSchemaError(msg)

        with open(csv_fn, "r") as fid:
            logger.debug("Reading schema CSV {0}".format(csv_fn))
            lines = fid.readlines()

        header = validators.validate_header(
            [ss.strip().lower() for ss in lines[0].strip().split(",")], attribute=True
        )
        attribute_dict = {}
        for line in lines[1:]:
            if len(line) < 2:
                continue
            line_dict = dict(
                [
                    (key, ss.strip())
                    for key, ss in zip(header, line.strip().split(",", len(header) - 1))
                ]
            )

            key_name = validators.validate_attribute(line_dict["attribute"])
            line_dict.pop("attribute")

            attribute_dict[key_name] = validators.validate_value_dict(line_dict)

        self.update(attribute_dict)

    def to_csv(self, csv_fn):
        """
        write dictionary to csv file
        
        :param level_dict: DESCRIPTION
        :type level_dict: TYPE
        :param csv_fn: DESCRIPTION
        :type csv_fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE
    
        """

        if not isinstance(csv_fn, Path):
            csv_fn = Path(csv_fn)

        # sort dictionary first
        lines = [",".join(REQUIRED_KEYS)]
        for key in sorted(list(self.keys())):
            line = [key]
            for rkey in REQUIRED_KEYS[1:]:
                value = self[key][rkey]
                if isinstance(value, (list, tuple)):
                    if len(value) == 0:
                        line.append("None")
                    else:
                        line.append(
                            '"{0}"'.format(value).replace(",", "|").replace("'", "")
                        )
                else:
                    line.append("{0}".format(self[key][rkey]))
            lines.append(",".join(line))

        with csv_fn.open("w") as fid:
            fid.write("\n".join(lines))
        logger.info("Wrote dictionary to {0}".format(csv_fn))
        return csv_fn

    def to_json(self, json_fn, indent=" " * 4):
        """
        Write schema standards to json
        
        :param json_fn: full path to json file
        :type json_fn: string or Path
        :return: full path to json file
        :rtype: Path

        """

        json_fn = Path(json_fn)

        json_dict = dict([(k, v) for k, v in self.items() if k not in ["logger"]])
        with open(json_fn, "w") as fid:
            json.dump(json_dict, fid, cls=NumpyEncoder, indent=indent)

        return json_fn

    def from_json(self, json_fn):
        """
        
        Read schema standards from json
        
        :param json_fn: full path to json file
        :type json_fn: string or Path
        :return: full path to json file
        :rtype: Path

        """

        json_fn = Path(json_fn)
        if not json_fn.exists():
            msg = f"JSON schema file {json_fn} does not exist"
            logger.error(msg)
            MTSchemaError(msg)

        with open(json_fn, "r") as fid:
            json_dict = json.load(fid)

        valid_dict = {}
        for k, v in json_dict.items():
            valid_dict[k] = validators.validate_value_dict(v)
        self.update(valid_dict)


def get_schema_fn(schema_element, paths):
    """
    Get the correct file name for the given schema element from the provided
    list of valid file names
    
    :param schema_element: name of the schema element to get filename for
    :type schema_element: string
    :return: correct file name for given element
    :rtype: :class:`pathlib.Path`

    """
    for fn in paths:
        if schema_element == fn.stem:
            return fn
    msg = f"Could not find schema element {schema_element}.json in {paths[0].parent}."
    raise MTSchemaError(msg)


def get_schema(schema_element, paths):
    """
    Get a :class:`mt_metadata.schema_base.BaseDict` object of the element
    
    :param schema_element: name of the schema element to get filename for
    :type schema_element: string
    :return: return a dictionary that describes the standards for the element
    :rtype: :class:`mt_metadata.schema_base.BaseDict`

    """

    schema_fn = get_schema_fn(schema_element, paths)
    element_dict = BaseDict()
    element_dict.from_json(schema_fn)

    return element_dict
