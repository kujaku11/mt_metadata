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
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from mt_metadata.timeseries.standards import (
    SCHEMA_FN_PATHS as TS_SCHEMA_FN_PATHS,
)
from mt_metadata.utils.mttime import MTime
from . import Person, Software, DataQuality
from mt_metadata.transfer_functions.processing import aurora

# =============================================================================
attr_dict = get_schema("transfer_function", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("person", TS_SCHEMA_FN_PATHS), "processed_by")
attr_dict.add_dict(get_schema("software", TS_SCHEMA_FN_PATHS), "software")
attr_dict.add_dict(DataQuality()._attr_dict, "data_quality")


# =============================================================================
class TransferFunction(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.processed_by = Person()
        self.software = Software()
        self._processed_date = MTime()
        self.data_quality = DataQuality()
        self.processing_parameters = []
        self.processing_config = None

        super().__init__(attr_dict=attr_dict)
        self.processing_parameters = []

        for key, value in kwargs.items():
            self.set_attr_from_name(key, value)

    @property
    def processed_date(self):
        return self._processed_date.date

    @processed_date.setter
    def processed_date(self, value):
        self._processed_date.parse(value)

    @property
    def processing_config(self):
        """

        :return: processing configuration

        """
        if self._processing_config is None:
            if len(self.processing_parameters) > 0:
                processing_dict = {}
                for item in self.processing_parameters:
                    if item.startswith("aurora"):
                        default_key = "aurora"
                        key, value = item.split("=")
                        key = key.replace(f"{default_key}.", "")
                        processing_dict[key] = value
                self._processing_config = aurora.Processing()
                self._processing_config.from_dict(
                    {"processing": processing_dict}
                )

        return self._processing_config

    def _dict_to_params(self, object_dict, base_key):
        """
        dictionary to parameters

        key_base.key = value

        :param object_dict: DESCRIPTION
        :type object_dict: TYPE
        :param key_base: DESCRIPTION
        :type key_base: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for key, value in object_dict.items():
            if isinstance(value, list):
                if len(value) > 0:
                    if isinstance(value[0], dict):
                        for item in value:
                            if len(item.keys()) == 1:
                                item_key = list(item.keys())[0]
                                self._dict_to_params(
                                    item[item_key],
                                    f"{base_key}.{key}.{item_key}",
                                )
                            else:
                                self._dict_to_params(item, f"{base_key}.{key}")
                    else:
                        self.processing_parameters.append(
                            f"{base_key}.{key}={value}"
                        )
                else:
                    self.processing_parameters.append(
                        f"{base_key}.{key}={value}"
                    )

            elif isinstance(value, dict):
                self._dict_to_params(value, f"{base_key}.{key}")
            else:
                self.processing_parameters.append(f"{base_key}.{key}={value}")

    @processing_config.setter
    def processing_config(self, processing_config):
        """
        set processing config, if a Base object, processing parameters are
        filled.

        To add more processing schemes need to create a Processing object for
        that specific program and then add in

        :param processing_config: DESCRIPTION
        :type processing_config: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if processing_config is not None:
            if isinstance(processing_config, aurora.Processing):
                default_key = "aurora"
                processing_dict = processing_config.to_dict(single=True)
                self._dict_to_params(processing_dict, default_key)
                self._processing_config = processing_config
        else:
            self._processing_config = None
