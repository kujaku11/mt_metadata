# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.exceptions import MTSchemaError
from typing import Union

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
            msg = (f"Filter names and applied lists are not the same size. "
                   f"Be sure to check the inputs. "
                   f"names = {self._name}, applied = {self._applied}")
            self.logger.warning(msg)

    @property
    def applied(self):
        return self._applied

    @applied.setter
    def applied(self, applied: Union[list, str, None, int, tuple]) -> None:
        """
        Sets the value of the booleans for whether each filter has been applied or not

        :type applied: Union[list, str, None, int, tuple]
        :param applied: The value to set self._applied.

        Notes:
        self._applied is a list, but we allow this to be assigned by null values as well.
        If a null value is received, the filters are assumed to have been applied
        If a non-iterable False

        """
        # Handle cases where we did not pass an iterable
        if not hasattr(applied, "__iter__"):
            null_values = [None, ]  # filter applied is True
            false_values = [0, "0", False]  # filter applied is False
            if applied in null_values:
                self._applied = [True]
                return
            elif applied in false_values:
                self._applied = [False]
                return

        #sets an empty list to one default value
        if isinstance(applied, list) and len(applied) == 0:
            self.applied = [True]
            return

        # Handle string case -- Note that these should be removed from hasattr __iter__ logic above
        if isinstance(applied, str):
            if applied.find("[") >= 0:
                applied = applied.replace("[", "").replace("]", "")
            if applied.count(",") > 0:
                applied_list = [
                    ss.strip().lower() for ss in applied.split(",")
                ]
            else:
                applied_list = [ss.lower() for ss in applied.split()]
        elif isinstance(applied, list):
            applied_list = applied
            # set integer strings to integers ["0","1"]--> [0, 1]
            for i, elt in enumerate(applied_list):
                if elt in ["0", "1",]:
                    applied_list[i] = int(applied_list[i])
            # set integers to bools [0,1]--> [False, True]
            for i, elt in enumerate(applied_list):
                if elt in [0, 1,]:
                    applied_list[i] = bool(applied_list[i])
        # We should never get here becasue bools are not iterable
        elif isinstance(applied, bool):
            applied_list = [applied]
        # the returned type from a hdf5 dataset is a numpy array.
        elif isinstance(applied, np.ndarray):
            applied_list = list(applied)
            if applied_list == []:
                applied_list = [True]
        else:
            msg = "applied must be a string or list of strings not {0}"
            self.logger.error(msg.format(applied))
            raise MTSchemaError(msg.format(applied))

        bool_list = []
        for app_bool in applied_list:
            if app_bool is None:
                bool_list.append(True)
            elif isinstance(app_bool, str):
                if app_bool.lower() in ["false", "0"]:
                    bool_list.append(False)
                elif app_bool.lower() in ["true", "1"]:
                    bool_list.append(True)
                else:
                    msg = "Filter.applied must be [ True | False ], not {0}"
                    self.logger.error(msg.format(app_bool))
                    raise MTSchemaError(msg.format(app_bool))
            elif isinstance(app_bool, (bool, np.bool_)):
                bool_list.append(bool(app_bool))
            else:
                msg = "Filter.applied must be [True | False], not {0}"
                self.logger.error(msg.format(app_bool))
        self._applied = bool_list

        # check for consistency
        check = self._check_consistency()
        if not check:
            msg = (f"Filter names and applied lists are not the same size. "
                   f"Be sure to check the inputs. "
                   f"names = {self._name}, applied = {self._applied}")
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
            self.logger.debug("Name probably not yet initialized -- skipping consitency check")
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
                self._applied = len(self.name) * [self._applied[0],]
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
