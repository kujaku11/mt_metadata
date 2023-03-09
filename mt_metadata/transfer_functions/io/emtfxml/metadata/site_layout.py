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
from . import Magnetic, Electric

# =============================================================================
attr_dict = get_schema("site_layout", SCHEMA_FN_PATHS)
# =============================================================================


class SiteLayout(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._input_channels = []
        self._output_channels = []

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def input_channels(self):
        return self._input_channels

    @input_channels.setter
    def input_channels(self, value):
        if not isinstance(value, list):
            value = [value]

        for item in value:

            ch_type = list(item.keys())[0]
            if ch_type in ["magnetic"]:
                ch = Magnetic()
            elif ch_type in ["electric"]:
                ch = Electric()
            else:
                msg = "Channel type %s not supported"
                self.logger.error(msg, ch_type)
                raise ValueError(msg % ch_type)
            ch.from_dict(item)
            self._input_channels.append(ch)

    @property
    def output_channels(self):
        return self._output_channels

    @output_channels.setter
    def output_channels(self, value):
        if not isinstance(value, list):
            value = [value]

        for item in value:
            ch_type = list(item.keys())[0]
            if ch_type in ["magnetic"]:
                ch = Magnetic()
            elif ch_type in ["electric"]:
                ch = Electric()
            else:
                msg = "Channel type %s not supported"
                self.logger.error(msg, ch_type)
                raise ValueError(msg % ch_type)

            ch.from_dict(item)
            self._output_channels.append(ch)

    def read_dict(self, input_dict):
        """
        read site layout into the proper input/output channels

        :param input_dict: DESCRIPTION
        :type input_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        # read input channels
        for ch in ["input_channels", "output_channels"]:
            ch_list = []
            try:
                c_list = input_dict["site_layout"][ch]["magnetic"]
                if c_list is None:
                    continue
                if not isinstance(c_list, list):
                    c_list = [c_list]
                ch_list += [{"magnetic": ch_dict} for ch_dict in c_list]

            except (KeyError, TypeError):
                pass

            try:
                c_list = input_dict["site_layout"][ch]["electric"]
                if c_list is None:
                    continue
                if not isinstance(c_list, list):
                    c_list = [c_list]
                ch_list += [{"electric": ch_dict} for ch_dict in c_list]
            except (KeyError, TypeError):
                pass

            setattr(self, ch, ch_list)

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

        section = et.SubElement(root, "InputChannels")
        for ch in self.input_channels:
            section.append(ch.to_xml(required=required))
        section = et.SubElement(root, "OutputChannels")
        for ch in self.output_channels:
            section.append(ch.to_xml(required=required))

        if string:
            return element_to_string(root)
        return root
