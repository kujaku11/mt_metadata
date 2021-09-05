# -*- coding: utf-8 -*-
"""
EMTFXML
==========

This is meant to follow Anna's XML schema for transfer functions

Created on Sat Sep  4 17:59:53 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import inspect
from pathlib import Path
from collections import OrderedDict
from xml.etree import cElementTree as et

from mt_metadata.transfer_functions import emtf_xml
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.base import helpers
from mt_metadata.utils.validators import validate_attribute

meta_classes = dict([(validate_attribute(k), v) for k, v in inspect.getmembers(emtf_xml, inspect.isclass)])

# =============================================================================
# EMTFXML
# =============================================================================

class EMTFXML(emtf_xml.EMTF):
    """
    This is meant to follow Anna's XML schema for transfer functions
    """
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger(self.__class__.__name__)
        self.external_url = emtf_xml.ExternalUrl()
        self.primary_data = emtf_xml.PrimaryData()
        self.attachment = emtf_xml.Attachment()
        self.provenance = emtf_xml.Provenance()
        self.copyright = emtf_xml.Copyright()
        self.site = emtf_xml.Site()
        self.field_notes = [emtf_xml.FieldNotes()]
        
        
        self.element_keys = [
            "external_url",
            "primary_data",
            "attachment",
            "provenance",
            "copyright",
            "site",
            "field_notes",
            ]
        
    def read(self, fn):
        """
        Read xml file
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        fn = Path(fn)
        if not fn.exists():
            raise IOError(f"Cannot find: {fn}")
            
        root = et.parse(fn).getroot()
        root_dict = helpers.element_to_dict(root)
        root_dict = root_dict[list(root_dict.keys())[0]]
        root_dict = self._convert_keys_to_lower_case(root_dict)
        
        
        self._read_description(root_dict)
        self._read_product_id(root_dict)
        self._read_notes(root_dict)
        self._read_tags(root_dict)
        for element in self.element_keys:
            self._read_element(root_dict, element)
        
    def _read_description(self, root_dict):
        try:
            self.description = root_dict["description"]
        except KeyError:
            self.logger.debug("no description in xml")
            
        
    def _read_product_id(self, root_dict):
        try:
            self.product_id = root_dict["product_id"]
        except KeyError:
            self.logger.debug("no product_id in xml")
    
    def _read_notes(self, root_dict):
        try:
            self.notes = root_dict["notes"]
        except KeyError:
            self.logger.debug("no notes in xml")
        
    def _read_tags(self, root_dict):
        try:
            self.tags = root_dict["tags"]
        except KeyError:
            self.logger.debug("no tags in xml")
            
    def _read_element(self, root_dict, element_name):
        """
        generic read an element given a name 
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :param element_name: DESCRIPTION
        :type element_name: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        element_name = validate_attribute(element_name)
        try:
            value = root_dict[element_name]
            if isinstance(value, (dict, OrderedDict)):
                element_dict = {element_name: value}
                getattr(self, element_name).from_dict(element_dict)
            elif isinstance(value, list):
                xml_attr = []
                
                for item in value:
                    print(element_name, type(item))
                    element_dict = {element_name: item}
                    obj = meta_classes[element_name]()
                    obj.from_dict(element_dict)
                    xml_attr.append(obj)
                setattr(self, element_name, xml_attr)
                    
                    
        except KeyError:
            print(f"No {element_name} in EMTF XML")
            self.logger.debug(f"No {element_name} in EMTF XML")
        
    def _convert_keys_to_lower_case(self, root_dict):
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
                   res[new_key] = self._convert_keys_to_lower_case(res[new_key])
        elif isinstance(root_dict, list):
            res = []
            for item in root_dict:
                item = self._convert_keys_to_lower_case(item)
                res.append(item)
        return res
            
        
    
        
        
            
        
        
