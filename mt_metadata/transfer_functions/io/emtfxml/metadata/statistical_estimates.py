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
from xml.etree import cElementTree as et

from mt_metadata.base.helpers import write_lines, element_to_string
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from .estimate import Estimate

# =============================================================================
attr_dict = get_schema("statistical_estimates", SCHEMA_FN_PATHS)
# =============================================================================


class StatisticalEstimates(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._estimates_list = []
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def estimates_list(self):
        return self._estimates_list

    @estimates_list.setter
    def estimates_list(self, value):
        if not isinstance(value, list):
            value = [value]
        self._estimates_list = []
        for item in value:
            est = Estimate()
            est.from_dict(item)
            self._estimates_list.append(est)

    def read_dict(self, input_dict):
        """
        Read in statistical estimate descriptions

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        self.estimates_list = input_dict["statistical_estimates"]["estimate"]

    def to_xml(self, string=False, required=True):
        """

        :param string: DESCRIPTION, defaults to False
        :type string: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        root = et.Element(self.__class__.__name__.capitalize())

        for estimate in self.estimate_list:
            root.append(estimate.to_xml(required=required))

        if string:
            return element_to_string(root)
        return root
