# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:20:59 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict

import numpy as np

from mt_metadata.base import Base, get_schema
from mt_metadata.base.helpers import write_lines
from mt_metadata.timeseries import TimePeriod
from mt_metadata.transfer_functions.processing.fourier_coefficients import Decimation
from mt_metadata.utils.list_dict import ListDict

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("fc", SCHEMA_FN_PATHS)
attr_dict.add_dict(TimePeriod()._attr_dict, "time_period")


# =============================================================================
class FC(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.time_period = TimePeriod()
        self.levels = ListDict()
        self._decimation_levels = []
        self._channels_estimated = []

        super().__init__(attr_dict=attr_dict, **kwargs)

    def __len__(self):
        return len(self.levels)

    def __add__(self, other):
        if isinstance(other, FC):
            self.levels.extend(other.levels)
            self.update_time_period()

            return self
        else:
            msg = f"Can only merge ch objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)

    def update(self, other, match=[]):
        """
        Update attribute values from another like element, skipping None

        :param other: DESCRIPTION
        :type other: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if not isinstance(other, type(self)):
            self.logger.warning("Cannot update %s with %s", type(self), type(other))
        for k in match:
            if self.get_attr_from_name(k) != other.get_attr_from_name(k):
                msg = "%s is not equal %s != %s"
                self.logger.error(
                    msg,
                    k,
                    self.get_attr_from_name(k),
                    other.get_attr_from_name(k),
                )
                raise ValueError(
                    msg,
                    k,
                    self.get_attr_from_name(k),
                    other.get_attr_from_name(k),
                )
        for k, v in other.to_dict(single=True).items():
            if hasattr(v, "size"):
                if v.size > 0:
                    self.set_attr_from_name(k, v)
            else:
                if v not in [None, 0.0, [], "", "1980-01-01T00:00:00+00:00"]:
                    self.set_attr_from_name(k, v)

        ## Need this because decimation_levels are set when setting decimation_levels_recorded
        ## and it initiates an empty decimation_level, but we need to fill it with
        ## the appropriate metadata.
        for dl in other.levels:
            self.add_decimation_level(dl)

    @property
    def decimation_levels(self):
        """list of decimation levels"""
        dl_list = []
        for dl in self.levels:
            dl_list.append(dl.decimation.level)
        dl_list = sorted(set([cc for cc in dl_list if cc is not None]))
        if self._decimation_levels == []:
            return dl_list

        elif dl_list == []:
            return self._decimation_levels

        elif len(self._decimation_levels) != dl_list:
            return dl_list

    @decimation_levels.setter
    def decimation_levels(self, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()

        if value in [None, "None", "none", "NONE", "null"]:
            return
        elif isinstance(value, (list, tuple)):
            self._decimation_levels = value

        elif isinstance(value, (str)):
            value = value.split(",")
            self._decimation_levels = value

        else:
            raise TypeError(
                "'channels_recorded' must be set with a list not " f"{type(value)}."
            )

    @property
    def channels_estimated(self):
        """list of decimation levels"""
        dl_list = []
        for dl in self.levels:
            dl_list += dl.channels_estimated
        dl_list = sorted(set([cc for cc in dl_list if cc is not None]))
        if self._channels_estimated == []:
            return dl_list

        elif dl_list == []:
            return self._channels_estimated

        elif len(self._channels_estimated) != dl_list:
            return dl_list

    @channels_estimated.setter
    def channels_estimated(self, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()

        if value in [None, "None", "none", "NONE", "null"]:
            return
        elif isinstance(value, (list, tuple)):
            self._channels_estimated = value

        elif isinstance(value, (str)):
            value = value.split(",")
            self._channels_estimated = value

        else:
            raise TypeError(
                "'channels_recorded' must be set with a list not " f"{type(value)}."
            )

    def has_decimation_level(self, level):
        """
        Check to see if the decimation_level already exists

        :param level: decimation_level level to look for
        :type level: string
        :return: True if found, False if not
        :rtype: boolean

        """

        if level in self.decimation_levels:
            return True
        return False

    def decimation_level_index(self, level):
        """
        get index of the decimation_level in the decimation_level list
        """
        if self.has_decimation_level(level):
            return self.levels.keys().index(str(level))
        return None

    def get_decimation_level(self, level):
        """
        Get a decimation_level

        :param level: decimation_level level to look for
        :type level: string
        :return: decimation_level object based on decimation_level type
        :rtype: :class:`mt_metadata.timeseries.decimation_level`

        """

        if self.has_decimation_level(level):
            return self.levels[str(level)]

    def add_decimation_level(self, fc_decimation):
        """
        Add a decimation_level to the list, check if one exists if it does overwrite it

        :param decimation_level_obj: decimation_level object to add
        :type decimation_level_obj: :class:`mt_metadata.transfer_functions.processing.fourier_coefficients.decimation_level`

        """
        if not isinstance(fc_decimation, (Decimation)):
            msg = f"Input must be metadata.decimation_level not {type(fc_decimation)}"
            self.logger.error(msg)
            raise ValueError(msg)

        if self.has_decimation_level(fc_decimation.decimation.level):
            self.levels[fc_decimation.decimation.level].update(
                fc_decimation
            )
            self.logger.debug(
                f"ch {fc_decimation.decimation.level} already exists, updating metadata"
            )

        else:
            self.levels.append(fc_decimation)

        self.update_time_period()

    def remove_decimation_level(self, decimation_level_id):
        """
        remove a ch from the survey

        :param level: decimation_level level to look for
        :type level: string

        """

        if self.has_decimation_level(decimation_level_id):
            self.levels.remove(decimation_level_id)
        else:
            self.logger.warning(f"Could not find {decimation_level_id} to remove.")

        self.update_time_period()

    @property
    def levels(self):
        """List of decimation_levels in the ch"""
        return self._levels

    @levels.setter
    def levels(self, value):
        """set the decimation_level list"""

        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input dl_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

        fails = []
        self._levels = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, decimation_level in enumerate(value_list):
            try:
                dl = Decimation()
                if hasattr(decimation_level, "to_dict"):
                    decimation_level = decimation_level.to_dict()
                dl.from_dict(decimation_level)
                self._levels.append(dl)
            except Exception as error:
                msg = "Could not create decimation_level from dictionary: %s"
                fails.append(msg % error)
                self.logger.error(msg, error)

        if len(fails) > 0:
            raise TypeError("\n".join(fails))

    @property
    def n_decimation_levels(self):
        return self.__len__()

    def update_time_period(self):
        """
        update time period from ch information
        """
        start = []
        end = []
        for dl in self.levels:
            if dl.time_period.start != "1980-01-01T00:00:00+00:00":
                start.append(dl.time_period.start)
            if dl.time_period.start != "1980-01-01T00:00:00+00:00":
                end.append(dl.time_period.end)
        if start:
            if self.time_period.start == "1980-01-01T00:00:00+00:00":
                self.time_period.start = min(start)
            else:
                if self.time_period.start > min(start):
                    self.time_period.start = min(start)
        if end:
            if self.time_period.end == "1980-01-01T00:00:00+00:00":
                self.time_period.end = max(end)
            else:
                if self.time_period.end < max(end):
                    self.time_period.end = max(end)
