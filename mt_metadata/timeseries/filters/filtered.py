# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from typing import Optional, Union

# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base import Base, get_schema
from mt_metadata.base.helpers import write_lines
from mt_metadata.timeseries.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.exceptions import MTSchemaError


# =============================================================================
attr_dict = get_schema("filtered", SCHEMA_FN_PATHS)


# =============================================================================
class Filtered(Base):
    """
    List of filter names booleans tracking if filter has been
        applied.   May want to dict(zip(name, applied))

    """

    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """
        Constructor

        :param kwargs:

        TODO: Consider not setting self.applied = None, as this has the effect of self._applied = [True,]
        """
        self._applied_values_map = _applied_values_map()
        self._name = []
        self._applied = []
        self.name = None
        self.applied = None
        self.comments = None
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, names):
        if names is None:
            self._name = []
            return

        if isinstance(names, str):
            self._name = [ss.strip().lower() for ss in names.split(",")]
        elif isinstance(names, list):
            self._name = [ss.strip().lower() for ss in names]
        elif isinstance(names, np.ndarray):
            names = names.astype(np.str_)
            self._name = [ss.strip().lower() for ss in names]
        else:
            msg = "names must be a string or list of strings not {0}, type {1}"
            self.logger.error(msg.format(names, type(names)))
            raise MTSchemaError(msg.format(names, type(names)))

        check = self._check_consistency()
        if not check:
            msg = (
                f"Filter names and applied lists are not the same size. "
                f"Be sure to check the inputs. "
                f"names = {self._name}, applied = {self._applied}"
            )
            self.logger.warning(msg)

    @property
    def applied(self) -> list:
        return self._applied

    @applied.setter
    def applied(
        self,
        applied: Union[list, str, None, int, tuple, np.ndarray, bool],
    ) -> None:
        """
        Sets the value of the booleans for whether each filter has been applied or not

        :type applied: Union[list, str, None, int, tuple]
        :param applied: The value to set self._applied.

        Notes:
        self._applied is a list, but we allow this to be assigned by single values as well,
        such as None, True, 0. Supporting these other values makes the logic a little bit involved.
        If a null value is received, the filters are assumed to be applied.
        If a simple value, such as True, None, 0, etc. is not received, the input argument
        applied (which is iterable) is first converted to `applied_list`.
        The values in `applied_list` are then mapped to booleans.


        """
        # Handle cases where we did not pass an iterable
        if not hasattr(applied, "__iter__"):
            self._applied = [
                self._applied_values_map[applied],
            ]
            return

        # the returned type from a hdf5 dataset is a numpy array.
        if isinstance(applied, np.ndarray):
            applied = applied.tolist()

        # sets an empty list to one default value
        if isinstance(applied, list) and len(applied) == 0:
            self._applied = [True]
            return

        # Handle string case
        if isinstance(applied, str):
            # Handle simple strings
            if applied in self._applied_values_map.keys():
                self._applied = [
                    self._applied_values_map[applied],
                ]
                return

            # Handle string-lists (e.g. from json)
            if applied.find("[") >= 0:
                applied = applied.replace("[", "").replace("]", "")
            if applied.count(",") > 0:
                applied_list = [ss.strip().lower() for ss in applied.split(",")]
            else:
                applied_list = [ss.lower() for ss in applied.split()]
        elif isinstance(applied, list):
            applied_list = applied
        elif isinstance(applied, tuple):
            applied_list = list(applied)
        else:
            msg = f"Input applied cannot be of type {type(applied)}"
            self.logger.error(msg)
            raise MTSchemaError(msg)

        # Now we have a simple list -- map to bools
        try:
            bool_list = [self._applied_values_map[x] for x in applied_list]
        except KeyError:
            msg = f"A key in {applied_list} is not mapped to a boolean"
            msg += "\n fix this by adding to _applied_values_map"
            self.logger.error(msg)
        self._applied = bool_list

        # check for consistency
        check = self._check_consistency()
        if not check:
            msg = (
                f"Filter names and applied lists are not the same size. "
                f"Be sure to check the inputs. "
                f"names = {self._name}, applied = {self._applied}"
            )
            self.logger.warning(msg)

    def _check_consistency(self) -> bool:
        """
        Logic to look for inconstencies in the configuration of the filter names and applied values.

        In general, list of filter names should be same length as list of applied booleans.

        Cases:
        The filter has no name -- this could happen on intialization.

        :return: bool
            True if OK, False if not.

        """
        # This inconsistency is ok -- the filter may not have been assigned a name yet
        if self._name == [] and len(self._applied) > 0:
            self.logger.debug(
                "Name probably not yet initialized -- skipping consitency check"
            )
            return True

        # Otherwise self._name != []

        # Applied not assigned - this is not OK
        if self._applied is None:
            self.logger.warning("Need to input filter.applied")
            return False

        # Name and applied have same length, 1. This is OK
        if len(self._name) == 1:
            if len(self._applied) == 1:
                return True

        # Multiple filter names (name not of length 0 or 1)
        if len(self._name) > 1:
            # If only one applied boolean, we allow it.
            # TODO: consider being less tolerant here
            if len(self._applied) == 1:
                msg = f"Assuming all filters have been applied as {self._applied[0]}"
                self.logger.debug(msg)
                self._applied = len(self.name) * [
                    self._applied[0],
                ]
                msg = f"Explicitly set filter applied state to {self._applied[0]}"
                self.logger.debug(msg)
                return True
            elif len(self._applied) > 1:
                # need to check the lists are really the same length
                if len(self._applied) != len(self._name):
                    msg = "Applied and filter names should be the same length. "
                    msg += f"Appied={len(self._applied)}, names={len(self._name)}"
                    self.logger.warning(msg)
                    return False
                else:
                    return True
        else:
            # Some unknown configuration we have not yet encountered
            msg = "Filter consistency check failed for an unknown reason"
            self.logger.warning(msg)
            return False


def _applied_values_map(treat_null_values_as: Optional[bool] = True) -> dict:
    """
    helper function to simplify logic in applied setter.

    Notes:
    The logic in the setter was getting quite complicated handling many types.
    A reasonable solution seemed to be to map each of the allowed values to a bool
    via dict and then use this dict when setting applied values.

    :return: dict
    Mapping of all tolerated single-values for setting applied booleans
    """
    null_values = [None, "none", "None", "NONE", "null"]
    null_values_map = {x: treat_null_values_as for x in null_values}
    true_values = [True, 1, "1", "True", "true"]
    true_values_map = {x: True for x in true_values}
    false_values = [False, 0, "0", "False", "false"]
    false_values_map = {x: False for x in false_values}
    values_map = {**null_values_map, **true_values_map, **false_values_map}
    return values_map
